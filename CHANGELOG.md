# Changelog

## 0.4.0 (Sunday, 22 November 2026)

Six parts for a sports site, first for [stefania.bojica.com](https://stefania.bojica.com/). Every family site can use them.

- Hero: a large photo with a headline, one line and up to two buttons. The text sits on a solid panel, never on the photo itself, so it reads the same on any photo, in light and dark mode.
- Stat row: two to four big numbers, each with a label and an optional second line. The digits have equal width.
- Results by season: one table per season, with event, place, date and the round in singles and doubles. A win shows the word "Winner", a trophy and an orange bar at the start of its row, never colour alone. Below 760 px each row becomes a stack, with no sideways scroll.
- Photo grid: 6 to 10 photos in even tiles, each with an alt text and an optional credit line.
- Icon list: short items, each with an icon in a round tile and one line, for example the ways to partner.
- Language switch: a row of links to the same page in other languages, for example EN, DE, RO. Each link is 44 px high, with `lang` and `hreflang`. The current language has `aria-current="page"`, a round outline and no underline, not only another colour. No JavaScript.
- Icons: six line icons as inline SVG in `dist/icons/`, and an `.icon` class. No icon font.
- `tests/check.py`: builds the stylesheet and checks that `dist/bojicas.css` is up to date, that every part is in it, that it asks no other server for anything, and that the example page loads nothing from another server.
- Foundations: text on a photo sits on a solid panel; numbers that are compared have digits of equal width; icons are inline SVG.

## 0.3.0 (Wednesday, 4 November 2026)

- Links to sites of someone else end in a small orange ↗, also in running text, outside the underline (`a.out`). Links to your own sites carry no mark. Links open in the same tab. The language docs show in one table how buttons and links use the arrows.
- `build.py --tokens-out PATH` also writes the tokens as JSON, for a page that shows them.
- Foundations and README: the 44 px rule holds for buttons and links that stand alone; a link inside a sentence follows the line height.
- Images: a photo by someone else carries a credit, covers are 1.91 : 1, and the source is at most 2400 px wide with its metadata stripped.
- Tags: a row of `#name` links, 44 px high. The orange `#` is part of the link but not underlined, like the arrow of the back link. The posts on [silviu.bojica.com](https://silviu.bojica.com/) need this.

## 0.2.0 (Wednesday, 4 November 2026)

- A definition list inside `.prose` looks like `.facts`, since Markdown cannot add a class. silviu.bojica.com needs this for its imprint and privacy statement.

## 0.1.0 (Wednesday, 4 November 2026)

The first version, taken from what [silviu.bojica.com](https://silviu.bojica.com/) and [bojica.com](https://bojica.com/) already use.

- Tokens for colour (light and dark), type, size, space, radius and touch targets, in `tokens.json`.
- `build.py` makes `dist/bojicas.css` from the tokens and `src/`.
- Components: button with the arrow rule, card, avatar, eyebrow, titles, back link, facts, footer, running text.
- Docs: foundations, components, language, slides and documents.
- An example page with every token and component.
