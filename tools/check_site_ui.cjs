/* Real Chromium checks against the Jekyll artifact, never a substitute renderer. */
const { chromium } = require('playwright');
const { spawn } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const nav = require('../navigation.json');
const siteRoot = path.resolve(__dirname, '../_site');
const evidence = path.resolve(__dirname, '../site-qa');
fs.mkdirSync(evidence, { recursive: true });
// Serve the production subpath without copying the site to a second source tree.
const server = spawn('python', ['-c', `
from http.server import HTTPServer, SimpleHTTPRequestHandler
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=${JSON.stringify(siteRoot)}, **kwargs)
    def do_GET(self):
        if not self.path.startswith('/ai-systems-notes/'):
            self.send_error(404)
            return
        self.path = self.path[len('/ai-systems-notes'):]
        super().do_GET()
HTTPServer(('127.0.0.1', 8765), Handler).serve_forever()
`], { stdio: 'ignore' });
const root = 'http://127.0.0.1:8765/ai-systems-notes';
const report = { checks: [], errors: [] };

(async () => {
  let browser;
  try {
    for (let retry = 0; retry < 100; retry++) {
      try { if ((await fetch(root + '/')).ok) break; } catch (_) {}
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    browser = await chromium.launch({ headless: true });
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, colorScheme: 'light' });
    page.on('pageerror', error => report.errors.push(String(error)));
    page.on('console', message => { if (message.type() === 'error') report.errors.push(message.text()); });
    async function open(url) {
      const response = await page.goto(root + url, { waitUntil: 'networkidle' });
      assert.equal(response.status(), 200, url);
      await page.waitForFunction(() => [...document.querySelectorAll('.mermaid')].every(node => node.dataset.rendered === 'true'), { timeout: 30000 });
      assert.equal(await page.locator('.render-error, .katex-error').count(), 0, url);
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'Page overflow: ' + url);
    }
    await open('/');
    assert.equal(await page.locator('.knowledge-group').count(), 6);
    assert.equal(await page.locator('.knowledge-topic').count(), 8);
    assert.equal(await page.locator('.knowledge-overview a').count(), 6);
    assert.deepEqual(await page.locator('.knowledge-group h3').allTextContents(), nav.groups.map(g => g.title));
    await page.screenshot({ animations: 'disabled', path: path.join(evidence, 'home-desktop-light.png'), fullPage: true });
    report.checks.push('home: six groups, eight topics, production baseurl');
    await page.locator('#modeToggle').click();
    assert.equal(await page.locator('html').getAttribute('data-mode'), 'dark');
    await page.screenshot({ animations: 'disabled', path: path.join(evidence, 'home-desktop-dark.png'), fullPage: true });
    await page.reload();
    assert.equal(await page.locator('html').getAttribute('data-mode'), 'dark');
    await page.locator('#modeToggle').click();
    await page.keyboard.press('/');
    await page.locator('#searchInput').fill('KV Cache');
    await page.waitForFunction(() => document.querySelectorAll('.search-result').length > 0);
    await page.keyboard.press('ArrowDown');
    await page.keyboard.press('Enter');
    await page.waitForURL('**/docs/**');
    await page.keyboard.press('Control+k');
    await page.locator('#searchInput').fill('检查点');
    await page.waitForFunction(() => [...document.querySelectorAll('.search-result')].some(node => /训练|生命周期/.test(node.textContent)));
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('#searchModal').getAttribute('aria-hidden'), 'true');
    report.checks.push('mode persistence; search hotkeys, Chinese/English, keyboard result navigation');
    // Visit every knowledge page so no diagram or formula is hidden by sampling.
    const pages = nav.groups.flatMap(group => group.pages).concat(nav.reference_pages);
    for (const item of pages) {
      await open('/docs/' + path.basename(item.path, '.md') + '/');
      const source = fs.readFileSync(path.resolve(__dirname, '..', item.path), 'utf8');
      const math = (source.match(/^```math\s*$|\$`[^`]+`\$/gm) || []).length;
      assert.equal(await page.locator('[data-tex] .katex').count(), math, item.path);
      assert.equal(await page.locator('.mermaid svg').count(), (source.match(/```mermaid/g) || []).length, item.path);
      assert.equal(await page.locator('#sidebar .sidebar__nav .sidebar__link.is-active').count(), 1, item.path);
      const headings = (source.match(/^#{2,3} /gm) || []).length;
      assert.equal(await page.locator('#tocNav a').count(), headings >= 2 ? headings : 0, item.path);
      for (const link of await page.locator('.doc-pager a').evaluateAll(nodes => nodes.map(node => node.getAttribute('href')))) {
        assert.ok(link && link.startsWith('/ai-systems-notes/docs/'), 'Pager URL');
      }
    }
    report.checks.push('all 30 knowledge pages: formula/diagram rendering, active sidebar, TOC, pager');
    await open('/docs/04-transformer/');
    await page.screenshot({ animations: 'disabled', path: path.join(evidence, 'transformer-desktop-light.png'), fullPage: true });
    const diagramBefore = await page.locator('.mermaid svg').first().getAttribute('id');
    await page.locator('#modeToggle').click();
    await page.waitForFunction(before => document.querySelector('.mermaid svg').id !== before, diagramBefore);
    await page.screenshot({ animations: 'disabled', path: path.join(evidence, 'transformer-desktop-dark.png'), fullPage: true });
    report.checks.push('Mermaid rerenders after dark-mode toggle');
    await page.locator('#modeToggle').click();
    await page.setViewportSize({ width: 390, height: 844 });
    await open('/');
    await page.screenshot({ animations: 'disabled', path: path.join(evidence, 'home-mobile.png') });
    await page.locator('#sidebarToggle').click();
    assert.equal(await page.locator('#sidebarToggle').getAttribute('aria-expanded'), 'true');
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('#sidebarToggle').getAttribute('aria-expanded'), 'false');
    await open('/docs/04-transformer/');
    await page.locator('.mobile-toc summary').click();
    const target = await page.locator('.mobile-toc a').first().getAttribute('href');
    await page.locator('.mobile-toc a').first().click();
    await page.waitForFunction(hash => decodeURIComponent(location.hash) === decodeURIComponent(hash), target);
    assert.equal(decodeURIComponent(new URL(page.url()).hash), decodeURIComponent(target));
    assert.equal(await page.locator('.mobile-toc').getAttribute('open'), null);
    await page.screenshot({ animations: 'disabled', path: path.join(evidence, 'transformer-mobile.png') });
    await page.locator('#sidebarToggle').click();
    await page.screenshot({ animations: 'disabled', path: path.join(evidence, 'sidebar-mobile.png') });
    await page.keyboard.press('Escape');
    await page.setViewportSize({ width: 320, height: 720 });
    await open('/');
    await open('/docs/10-serving-and-distributed/');
    report.checks.push('390px and 320px: no page overflow, home/doc drawer, mobile TOC');
    assert.deepEqual(report.errors, [], 'Browser console errors');
    console.log(JSON.stringify(report, null, 2));
  } catch (error) {
    report.errors.push(String(error.stack || error));
    throw error;
  } finally {
    fs.writeFileSync(path.join(evidence, 'report.json'), JSON.stringify(report, null, 2));
    if (browser) await browser.close();
    server.kill();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
