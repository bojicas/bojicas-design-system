#!/usr/bin/env python3
"""Build dist/bojicas.css from tokens.json and the stylesheets in src/.

    python3 build.py                     fonts are looked for in fonts/ next to the stylesheet (dist/fonts/)
    python3 build.py --font-path /fonts/ fonts live at another address, for example on a Hugo site
    python3 build.py --tokens-out PATH   also write the tokens as JSON, for a page that shows them

Only the Python standard library is needed.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# The font files in fonts/, by family, weight and character range.
FONT_FILES = [
    ("sans", 400, "latin"), ("sans", 400, "latin-ext"),
    ("sans", 600, "latin"), ("sans", 600, "latin-ext"),
    ("mono", 400, "latin"), ("mono", 400, "latin-ext"),
]
FILE_STEM = {"sans": "space-grotesk", "mono": "jetbrains-mono"}
RANGES = {
    "latin": "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD",
    "latin-ext": "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF",
}


def font_faces(tokens, font_path):
    out = []
    for role, weight, rng in FONT_FILES:
        family = tokens["font"][role]["family"]
        url = f"{font_path}{FILE_STEM[role]}-{rng}-{weight}-normal.woff2"
        out.append(
            f'@font-face {{ font-family: "{family}"; font-style: normal; font-weight: {weight}; font-display: swap;\n'
            f'  src: url("{url}") format("woff2"); unicode-range: {RANGES[rng]}; }}'
        )
    return "\n".join(out)


def variables(tokens, theme):
    lines = [f"  --{name}: {c[theme]};" for name, c in tokens["color"].items()]
    # Focus rings: blue on the light background, orange on the dark one, where blue is too faint.
    lines.append("  --focus: var(--blue);" if theme == "light" else "  --focus: var(--orange);")
    if theme == "light":
        for role, f in tokens["font"].items():
            lines.append(f'  --{role}: "{f["family"]}", {f["fallback"]};')
        for group in ("size", "space", "radius", "touch"):
            for name, value in tokens[group].items():
                lines.append(f"  --{group}-{name}: {value};")
        lines.append("  color-scheme: light dark;")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--font-path", default="fonts/", help="address of the fonts folder, ending in /")
    parser.add_argument("--out", default=str(ROOT / "dist" / "bojicas.css"))
    parser.add_argument("--tokens-out", help="also write tokens.json here, for example into a Hugo site's data/ folder")
    args = parser.parse_args()

    tokens = json.loads((ROOT / "tokens.json").read_text())
    parts = [
        f"/* {tokens['name']} {tokens['version']}. Made by build.py from tokens.json and src/; do not edit by hand.\n"
        "   Code under the MIT licence; fonts under the SIL Open Font License 1.1.\n"
        "   https://github.com/bojicas/bojicas-design-system */",
        "/* Fonts: served from your own site, so no visitor data goes to a font service. */",
        font_faces(tokens, args.font_path),
        "/* Colours and sizes, for light and dark mode. */",
        ":root {\n" + variables(tokens, "light") + "\n}",
        "@media (prefers-color-scheme: dark) {\n  :root {\n"
        + "\n".join("  " + line for line in variables(tokens, "dark").splitlines())
        + "\n  }\n}",
        (ROOT / "src" / "base.css").read_text().strip(),
        (ROOT / "src" / "components.css").read_text().strip(),
    ]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n\n".join(parts) + "\n")
    print(f"Wrote {out} ({out.stat().st_size} bytes)")
    if args.tokens_out:
        # The same tokens the stylesheet was made from, so a page can show the version and the colours.
        data = Path(args.tokens_out)
        data.parent.mkdir(parents=True, exist_ok=True)
        data.write_text((ROOT / "tokens.json").read_text())
        print(f"Wrote {data}")


if __name__ == "__main__":
    main()
