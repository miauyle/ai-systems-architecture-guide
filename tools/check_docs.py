"""Check document links, fences and known GitHub math compatibility hazards.

This is a source check. It cannot replace a browser typesetting check.
"""
from pathlib import Path
import re
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]


def check_formula(formula, location, errors):
    if "<" in formula:
        errors.append(f"{location}: literal less-than in TeX; write explicit history or a supported macro")
    if r"\operatorname" in formula:
        errors.append(f"{location}: unsupported operator macro")
    depth = 0
    for index, char in enumerate(formula):
        if char not in "{}":
            continue
        preceding = 0
        j = index - 1
        while j >= 0 and formula[j] == "\\":
            preceding += 1
            j -= 1
        if preceding % 2:
            continue
        depth += 1 if char == "{" else -1
        if depth < 0:
            errors.append(f"{location}: unmatched close brace")
            return
    if depth:
        errors.append(f"{location}: unmatched open brace")


def main():
    errors = []
    display_count = inline_count = 0
    files = sorted(ROOT.rglob("*.md"))
    for path in files:
        if ".git" in path.parts:
            continue
        text = path.read_text()
        fence = None
        math_lines = []
        start_line = 0
        for number, line in enumerate(text.splitlines(), 1):
            if line.startswith("```"):
                if fence is None:
                    fence = line[3:].strip()
                    start_line = number
                    math_lines = []
                else:
                    if fence == "math":
                        display_count += 1
                        check_formula("\n".join(math_lines), f"{path.relative_to(ROOT)}:{start_line}", errors)
                    fence = None
                continue
            if fence is not None:
                if fence == "math":
                    math_lines.append(line)
                continue
            if line.strip() == "$$":
                errors.append(f"{path.relative_to(ROOT)}:{number}: use a math fence")
            if line.startswith("|") and "$" in line:
                errors.append(f"{path.relative_to(ROOT)}:{number}: table depends on math parsing")
            for formula in re.findall(r"\$`([^`]+)`\$", line):
                inline_count += 1
                check_formula(formula, f"{path.relative_to(ROOT)}:{number}", errors)
        if fence is not None:
            errors.append(f"{path.relative_to(ROOT)}: unclosed fence")
        for link in re.findall(r"\]\(([^)]+)\)", text):
            if link.startswith(("https://", "http://", "#", "mailto:")):
                continue
            target = unquote(link.split("#")[0])
            if target and not (path.parent / target).exists():
                errors.append(f"{path.relative_to(ROOT)}: broken link {link}")
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print(f"Markdown files: {len(files)}")
    print(f"Display formulas: {display_count}; inline formulas: {inline_count}")
    print("Source links, fences and known math hazards passed.")


if __name__ == "__main__":
    main()
