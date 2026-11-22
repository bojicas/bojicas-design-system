#!/usr/bin/env python3
"""Check the design system: the build, the parts, and the rule "no requests to other servers".

    python3 tests/check.py

It builds the stylesheet into a temporary file and checks:
  1. dist/bojicas.css is up to date with tokens.json and src/.
  2. Every component, the five parts for a sports site included, has its classes in the stylesheet,
     its section in docs/components.md, and an example on example/index.html.
  3. The stylesheet asks no other server for anything: no @import, and every url() is a local path.
  4. The example page and the SVG files load nothing from another server.
  5. Every image on the example page has a real alt text. The language switch has lang, hreflang and
     one current page, marked by more than colour.
  6. The icons are inline SVG that hide from screen readers.
  7. The stylesheets in src/ take every colour from the tokens, and draw no gradient and no shadow.
  8. The words: no em dash, no en dash and no contractions in the docs, the README, the changelog and the example.

It prints one line per check and ends with exit code 1 when a check fails. Only the Python standard library is needed.
"""
import html
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
    "Language switch": ["lang-switch", "lang-name"],
}
ICONS = ["money", "package", "eye", "suitcase", "star", "trophy"]
# The only address that may appear in an SVG file: the name of the SVG language, which is never loaded.
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
# The named colours of CSS. A stylesheet in src/ may use none of them: every colour comes from a token.
NAMED_COLOURS = (
    "aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond blue blueviolet brown burlywood "
    "cadetblue chartreuse chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan darkgoldenrod darkgray "
    "darkgreen darkgrey darkkhaki darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon darkseagreen "
    "darkslateblue darkslategray darkslategrey darkturquoise darkviolet deeppink deepskyblue dimgray dimgrey dodgerblue "
    "firebrick floralwhite forestgreen fuchsia gainsboro ghostwhite gold goldenrod gray green greenyellow grey honeydew "
    "hotpink indianred indigo ivory khaki lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan "
    "lightgoldenrodyellow lightgray lightgreen lightgrey lightpink lightsalmon lightseagreen lightskyblue lightslategray "
    "lightslategrey lightsteelblue lightyellow lime limegreen linen magenta maroon mediumaquamarine mediumblue "
    "mediumorchid mediumpurple mediumseagreen mediumslateblue mediumspringgreen mediumturquoise mediumvioletred "
    "midnightblue mintcream mistyrose moccasin navajowhite navy oldlace olive olivedrab orange orangered orchid "
    "palegoldenrod palegreen paleturquoise palevioletred papayawhip peachpuff peru pink plum powderblue purple "
    "rebeccapurple red rosybrown royalblue saddlebrown salmon sandybrown seagreen seashell sienna silver skyblue "
    "slateblue slategray slategrey snow springgreen steelblue tan teal thistle tomato turquoise violet wheat white "
    "whitesmoke yellow yellowgreen canvas canvastext linktext visitedtext activetext buttonface buttontext field fieldtext "
    "highlight highlighttext graytext mark marktext"
).split()
COLOUR = re.compile(
    r"#[0-9a-f]{3,8}\b"                                                          # hex
    r"|(?:rgba?|hsla?|hwb|oklab|oklch|lab|lch|color|color-mix)\("               # colour functions
    r"|(?<![\w-])(?:" + "|".join(NAMED_COLOURS) + r")(?![\w-])",               # named colours, not inside --orange
    re.I)
# Flat surfaces: no gradients, no shadows, no glow.
NOT_FLAT = re.compile(r"gradient\(|box-shadow|text-shadow|drop-shadow|backdrop-filter", re.I)

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
    # rel values of <link> that fetch nothing.
    NAMES_ONLY = {"alternate", "canonical", "author", "license", "me", "next", "prev", "help", "search", "bookmark"}

    def __init__(self):
        super().__init__()
        self.classes, self.images, self.loads, self.styles = set(), [], [], []
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.classes.update((a.get("class") or "").split())
        if tag == "img":
            self.images.append(a)
        # Every <link> makes the browser fetch or contact its address (stylesheet, icon, preconnect, manifest, ...),
        # except the few kinds that only name a page.
        if tag == "link" and not set((a.get("rel") or "").lower().split()) <= self.NAMES_ONLY:
            self.loads.append(a.get("href") or "")
        if tag == "input" and (a.get("type") or "").lower() == "image":
            self.loads.append(a.get("src") or "")
        if tag == "meta" and (a.get("http-equiv") or "").lower() == "refresh":
            self.loads.append((a.get("content") or "").partition("url=")[2] or "")
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

    # 4b. The language switch: plain links, each with lang and hreflang, one marked as the current page,
    # and the current one marked by more than colour, with every link 44 px high and wide.
    navs = re.findall(r'<nav class="lang-switch"[^>]*>(.*?)</nav>', EXAMPLE.read_text(), flags=re.S)
    links = re.findall(r"<a\b([^>]*)>", navs[0]) if navs else []
    check(len(links) >= 2 and all(re.search(r'\blang="[a-z-]+"', a) and re.search(r'\bhreflang="[a-z-]+"', a) for a in links),
          f"Language switch: all {len(links)} links on example/index.html have lang and hreflang")
    current = [a for a in links if 'aria-current="page"' in a]
    check(len(current) == 1, f"Language switch: exactly one link is the current page (found {len(current)})")
    check(not re.search(r"<script|\bon[a-z]+=", navs[0] if navs else "<script"), "Language switch: no JavaScript")
    block = re.search(r'\.lang-switch a\[aria-current="page"\]\s*\{([^}]*)\}', rules)
    check(bool(block) and "text-decoration: none" in block.group(1) and "border-color" in block.group(1),
          "Language switch: the current language is marked by more than colour (no underline, an outline)")
    block = re.search(r"\.lang-switch a\s*\{([^}]*)\}", rules)
    check(bool(block) and "min-height: var(--touch-min)" in block.group(1) and "min-width: var(--touch-min)" in block.group(1),
          "Language switch: every link is at least 44 px high and wide")

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

    # 7. Every colour in src/ comes from the tokens, as a CSS variable, and every surface is flat.
    for source in sorted((ROOT / "src").glob("*.css")):
        rules_only = strip_css_comments(source.read_text())
        # Strings such as content: "·" and attribute names are not colours.
        rules_only = re.sub(r'"[^"]*"|attr\([^)]*\)', "", rules_only)
        found = COLOUR.findall(rules_only)
        check(not found, f"{source.relative_to(ROOT)} takes its colours from the tokens" + (f": {found}" if found else ""))
        found = NOT_FLAT.findall(rules_only)
        check(not found, f"{source.relative_to(ROOT)} has flat surfaces: no gradient, no shadow" + (f": {found}" if found else ""))

    # 8. The words.
    contraction = re.compile(r"\b\w+n[’']t\b|\b(?:it|that|there|here|what|let|who)[’']s\b|\b(?:i|you|we|they)[’'](?:m|re|ve|ll|d)\b", re.I)
    texts = [ROOT / "README.md", ROOT / "CHANGELOG.md", EXAMPLE, *sorted((ROOT / "docs").glob("*.md")), *sorted((ROOT / "src").glob("*.css"))]
    for path in texts:
        dashes, contractions = [], []
        for number, line in enumerate(path.read_text().splitlines(), 1):
            # Decode entities first, so &mdash; and &#8211; count as dashes too.
            line = html.unescape(line)
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
