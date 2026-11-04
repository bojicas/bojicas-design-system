# Changelog

## 0.3.0 (Wednesday, 4 November 2026)

- Links to sites of someone else end in a small orange ↗, also in running text, outside the underline (`a.out`). Links to your own sites carry no mark. Links open in the same tab. The language docs show in one table how buttons and links use the arrows.
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
