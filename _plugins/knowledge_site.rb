# Keep GitHub Markdown and navigation.json as the only maintained content sources.
require "json"
require "cgi"
require "pathname"

module AISystems
  class KnowledgeSite < Jekyll::Generator
    safe true
    priority :normal

    def generate(site)
      nav = JSON.parse(File.read(File.join(site.source, "navigation.json")))
      pages = nav.fetch("groups").flat_map { |g| g.fetch("pages") } + nav.fetch("reference_pages")
      routes = pages.to_h { |p| [p.fetch("path"), "/docs/#{File.basename(p.fetch('path'), '.md')}/"] }
      routes["README.md"] = "/"
      routes["docs/README.md"] = "/docs/"
      groups = nav.fetch("groups").map do |group|
        group.merge("pages" => group.fetch("pages").map { |p| p.merge("url" => routes.fetch(p.fetch("path"))) })
      end
      refs = nav.fetch("reference_pages").map { |p| p.merge("url" => routes.fetch(p.fetch("path"))) }
      site.data["knowledge_map"] = { "groups" => groups, "reference_pages" => refs }
      site.data["navigation"] = {
        "main" => [
          { "title" => "知识地图", "url" => "/#knowledge-map", "icon" => "fa-solid fa-diagram-project" },
          { "title" => "文档", "url" => "/docs/", "icon" => "fa-solid fa-book-open" },
          { "title" => "GitHub", "url" => "https://github.com/miauyle/ai-systems-notes", "icon" => "fa-brands fa-github" }
        ],
        "sidebar" => (groups + [{ "title" => "查询与来源", "pages" => refs }]).map do |g|
          { "title" => g.fetch("title"), "children" => g.fetch("pages").map { |p| { "title" => p.fetch("title"), "url" => p.fetch("url") } } }
        end
      }
      collection = site.collections.fetch("docs")
      pages.each do |p|
        group = groups.find { |g| g.fetch("pages").any? { |item| item["id"] == p["id"] } }
        add_document(site, collection, p.fetch("path"), p.fetch("title"), p.fetch("summary"), group ? group.fetch("title") : "查询与来源", routes)
      end
      add_document(site, collection, "docs/README.md", "完整专题目录", "六个分组、核心专题与原始资料入口", "AI Systems Notes", routes)
    end

    def add_document(site, collection, path, title, description, category, routes)
      source = File.read(File.join(site.source, path))
      # The theme supplies the H1, sidebar, and prev/next controls. Source stays unchanged.
      body = source.sub(/\A# [^\n]+\n+/, "").sub(/\A\[(?:返回首页|返回目录|首页)\][^\n]*\n+/, "")
      body = rewrite_links(body, path, routes, site.config.fetch("baseurl", ""))
      has_math = body.include?("```math") || body.match?(/\$`[^`]+`\$/)
      has_mermaid = body.include?("```mermaid")
      body = body.gsub(/^```math\s*\n(.*?)^```\s*$/m) { "<div class=\"math-display\" data-tex=\"#{CGI.escapeHTML(Regexp.last_match(1).strip)}\"></div>\n" }
      body = body.gsub(/\$`([^`]+)`\$/) { "<span class=\"math-inline\" data-tex=\"#{CGI.escapeHTML(Regexp.last_match(1))}\"></span>" }
      body = body.gsub(/^```mermaid\s*\n(.*?)^```\s*$/m) { "<div class=\"mermaid\">#{CGI.escapeHTML(Regexp.last_match(1).strip)}</div>\n" }
      doc = Jekyll::Document.new(File.join(site.source, path), :site => site, :collection => collection)
      doc.content = body
      doc.data.merge!("layout" => "doc", "title" => title, "description" => description,
                      "category" => category, "permalink" => routes.fetch(path),
                      "has_math" => has_math, "has_mermaid" => has_mermaid,
                      "render_with_liquid" => false)
      collection.docs << doc
    end

    def rewrite_links(body, source, routes, baseurl)
      # Only Markdown destinations, never code or external URLs. Fences are preserved.
      body.split(/(^```[^\n]*\n.*?^```[^\n]*$)/m).map do |part|
        next part if part.start_with?("```")
        part.gsub(/(\]\()([^\s)]+)(\))/) do
          prefix, target, suffix = Regexp.last_match.captures
          next "#{prefix}#{target}#{suffix}" if target.match?(%r{\A(?:[a-z]+:|/|#)}i)
          file, fragment = target.split("#", 2)
          resolved = Pathname.new(File.join(File.dirname(source), file)).cleanpath.to_s
          url = routes[resolved]
          if url
            "#{prefix}#{baseurl}#{url}#{fragment ? '#' + fragment : ''}#{suffix}"
          else
            "#{prefix}https://github.com/miauyle/ai-systems-notes/blob/master/#{resolved}#{fragment ? '#' + fragment : ''}#{suffix}"
          end
        end
      end.join
    end
  end
end
