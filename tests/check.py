#!/usr/bin/env python3
"""Check the design system: the build, the parts, and the rule "no requests to other servers".

    python3 tests/check.py

It builds the stylesheet into a temporary file and checks:
  1. dist/bojicas.css is up to date with tokens.json and src/.
  2. Every component, the five parts for a sports site included, has its classes in the stylesheet,
     its section in docs/components.md, and an example on example/index.html.
  3. The stylesheet asks no other server for anything: no @import, and every url() is a local path.
  4. The example page and the SVG files load nothing from another server.
  5. Every image on the example page has a real alt text.
  6. The icons are inline SVG that hide from screen readers.
  7. The stylesheets in src/ take every colour from the tokens.
  8. The words: no em dash, no en dash and no contractions in the docs, the README, the changelog and the example.

It prints one line per check and ends with exit code 1 when a check fails. Only the Python standard library is needed.
"""
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST_CSS = ROOT / "dist" / "bojicas.css"
EXAMPLE = ROOT / "example" / "index.html"
COMPONENTS_DOC = ROOT / "docs" / "components.md"

# Each part: its heading in docs/components.md, and the classes it needs in the stylesheet and on the example page.
PARTS = {
    "Icon": ["icon"],
    "Hero": ["hero", "hero-photo", "hero-text", "hero-credit"],
    "Stat row": ["stats", "stat", "stat-value", "stat-label", "stat-note"],
    "Results by season": ["results", "results-season", "results-year", "results-table", "results-date",
                          "results-win", "results-row-win", "results-none"],
    "Photo grid": ["photo-grid", "photo", "photo-credit"],
    "Icon list": ["icon-list"],
}
ICONS = ["money", "package", "eye", "suitcase", "star", "trophy"]
# The only address that may appear in an SVG file: the name of the SVG language, which is never loaded.
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
# Words that the alt text of an image must not be on its own.
EMPTY_ALT = {"", "image", "photo", "picture", "img", "icon"}

failures = []


def check(ok, message):
    print(("ok    " if ok else "FAIL  ") + message)
    if not ok:
        failures.append(message)


def strip_css_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def is_remote(address):
    address = address.strip().strip("'\"").lower()
    return address.startswith(("http:", "https:", "//", "ftp:")) or bool(re.match(r"^[a-z][a-z0-9+.-]*://", address))


class Page(HTMLParser):
    """Collects the classes, the images and every address the page would load."""

    # Attributes that make the browser load something, by tag. Links in <a href> are only followed on a click.
    LOADS = {"img": ["src", "srcset"], "source": ["src", "srcset"], "script": ["src"], "iframe": ["src"],
             "video": ["src", "poster"], "audio": ["src"], "embed": ["src"], "object": ["data"],
             "image": ["href", "xlink:href"], "use": ["href", "xlink:href"]}

    def __init__(self):
        super().__init__()
        self.classes, self.images, self.loads, self.styles = set(), [], [], []
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.classes.update((a.get("class") or "").split())
        if tag == "img":
            self.images.append(a)
        if tag == "link" and "stylesheet" in (a.get("rel") or "") or tag == "link" and "preload" in (a.get("rel") or ""):
            self.loads.append(a.get("href") or "")
        for name in self.LOADS.get(tag, []):
            for part in (a.get(name) or "").split(","):
                if part.strip():
                    self.loads.append(part.split()[0])
        if a.get("style"):
            self.styles.append(a["style"])
        self._in_style = tag == "style"

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_style:
            self.styles.append(data)


def main():
    # 1. The build.
    with tempfile.TemporaryDirectory() as tmp:
        built = Path(tmp) / "bojicas.css"
        run = subprocess.run([sys.executable, str(ROOT / "build.py"), "--out", str(built)], capture_output=True, text=True)
        check(run.returncode == 0, "build.py runs without errors" + ("" if run.returncode == 0 else ": " + run.stderr.strip()))
        css = built.read_text() if built.exists() else ""
    check(DIST_CSS.exists() and DIST_CSS.read_text() == css, "dist/bojicas.css is up to date (run python3 build.py)")

    # 2. Every part: classes in the stylesheet, a section in the docs, an example on the page.
    rules = strip_css_comments(css)
    doc = COMPONENTS_DOC.read_text()
    page = Page()
    page.feed(EXAMPLE.read_text())
    for part, classes in PARTS.items():
        missing_css = [c for c in classes if not re.search(r"\." + re.escape(c) + r"(?![\w-])", rules)]
        check(not missing_css, f"{part}: classes in dist/bojicas.css" + (f", missing {missing_css}" if missing_css else ""))
        check(re.search(r"^## " + re.escape(part) + r"\s*$", doc, flags=re.M) is not None, f"{part}: section in docs/components.md")
        missing_page = [c for c in classes if c not in page.classes]
        check(not missing_page, f"{part}: shown on example/index.html" + (f", missing {missing_page}" if missing_page else ""))

    # 3. The stylesheet asks no other server for anything.
    check("@import" not in rules, "dist/bojicas.css has no @import")
    urls = re.findall(r"url\(\s*([^)]*?)\s*\)", rules)
    remote = [u for u in urls if is_remote(u)]
    check(bool(urls) and not remote, f"dist/bojicas.css: all {len(urls)} url() are local" + (f", remote: {remote}" if remote else ""))
    addresses = re.findall(r"(?:https?:)?//[\w.-]+\.[a-z]{2,}", rules, flags=re.I)
    check(not addresses, "dist/bojicas.css holds no address of another server outside its comments" + (f": {addresses}" if addresses else ""))

    # 4. The example page and the SVG files load nothing from another server.
    remote = [u for u in page.loads if is_remote(u)]
    for style in page.styles:
        remote += [u for u in re.findall(r"url\(\s*([^)]*?)\s*\)", style) if is_remote(u)] + (["@import"] if "@import" in style else [])
    check(not remote, f"example/index.html loads all {len(page.loads)} files from its own site" + (f", remote: {remote}" if remote else ""))
    for svg in sorted((ROOT / "example").rglob("*.svg")) + sorted((ROOT / "dist" / "icons").glob("*.svg")):
        text = svg.read_text().replace(SVG_NAMESPACE, "")
        found = re.findall(r"(?:https?:|ftp:)?//[\w.-]+|url\(|href\s*=|<script|<foreignObject", text, flags=re.I)
        check(not found, f"{svg.relative_to(ROOT)} loads nothing" + (f": {found}" if found else ""))

    # 5. Real alt texts.
    bad = [i.get("src") for i in page.images if (i.get("alt") or "").strip().lower() in EMPTY_ALT]
    check(page.images and not bad, f"example/index.html: all {len(page.images)} images have a real alt text" + (f", not: {bad}" if bad else ""))

    # 6. The icons: inline SVG, hidden from screen readers, drawn with the text colour.
    for name in ICONS:
        path = ROOT / "dist" / "icons" / f"{name}.svg"
        ok = path.exists()
        if ok:
            root = ET.fromstring(path.read_text())
            ok = (root.tag == "{%s}svg" % SVG_NAMESPACE and root.get("aria-hidden") == "true"
                  and root.get("stroke") == "currentColor" and "icon" in (root.get("class") or "").split())
        check(ok, f"dist/icons/{name}.svg is a hidden SVG icon in the text colour")

    # 7. Every colour in src/ comes from the tokens, as a CSS variable.
    for source in sorted((ROOT / "src").glob("*.css")):
        found = re.findall(r"#[0-9a-f]{3,8}\b|\b(?:rgba?|hsla?|oklch|lab|lch)\(|\b(?:red|black)\b", strip_css_comments(source.read_text()), flags=re.I)
        check(not found, f"{source.relative_to(ROOT)} takes its colours from the tokens" + (f": {found}" if found else ""))

    # 8. The words.
    contraction = re.compile(r"\b\w+n[’']t\b|\b(?:it|that|there|here|what|let|who)[’']s\b|\b(?:i|you|we|they)[’'](?:m|re|ve|ll|d)\b", re.I)
    texts = [ROOT / "README.md", ROOT / "CHANGELOG.md", EXAMPLE, *sorted((ROOT / "docs").glob("*.md")), *sorted((ROOT / "src").glob("*.css"))]
    for path in texts:
        dashes, contractions = [], []
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if "—" in line or "–" in line:
                dashes.append(number)
            # The rule itself quotes the contractions it forbids.
            if "No contractions" not in line and contraction.search(line):
                contractions.append(number)
        check(not dashes and not contractions, f"{path.relative_to(ROOT)}: no em dash, no en dash, no contraction"
              + (f" (dash on line {dashes}, contraction on line {contractions})" if dashes or contractions else ""))

    print()
    if failures:
        print(f"{len(failures)} check(s) failed.")
        sys.exit(1)
    print("All checks passed.")


if __name__ == "__main__":
    main()
