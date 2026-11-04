# Bojicas Design System

One look and one voice for every public page of Silviu Bojica: [bojica.com](https://bojica.com/), [silviu.bojica.com](https://silviu.bojica.com/), [orgthread.dev](https://orgthread.dev/), and the slides, documents and images that go with them.

It is small on purpose: eight colours, two fonts, a handful of components, and a set of rules for how the words read. Think of it as a recipe card that several kitchens share. Change the recipe once, and every kitchen cooks the same dish.

**Status:** version 0.3.0. It is used by [silviu.bojica.com](https://silviu.bojica.com/). The family page [bojica.com](https://bojica.com/) still uses 0.2.0. It looks the same, since it has no tags.

## What is in it

| Part | Where |
|---|---|
| **Tokens:** colours for light and dark mode, fonts, sizes, spacing | [`tokens.json`](tokens.json), explained in [Foundations](docs/foundations.md) |
| **Web:** one stylesheet with the tokens and the components | [`dist/bojicas.css`](dist/bojicas.css), shown on the [example page](example/index.html), explained in [Components](docs/components.md) |
| **Language:** tone, punctuation, dates, names, arrows, alt texts | [Language](docs/language.md) |
| **Slides, documents, social images** | [Slides and documents](docs/slides-and-documents.md) |
| **Fonts:** [Space Grotesk](https://floriankarsten.github.io/space-grotesk/) and [JetBrains Mono](https://www.jetbrains.com/lp/mono/), with their licences | [`dist/fonts/`](dist/fonts/) |

## The rules in one minute

- Blue and orange on a light or a deep navy ground. Never red, never black as an accent.
- Every page works in light and dark mode, from 360 px to wide screens.
- Buttons and links that stand alone are at least 44 px high; a link inside a sentence follows the line height. Every image has a real alt text.
- No requests to other servers: fonts and images come from the site itself.
- Simple English, short sentences, no contractions, no em dashes, metric units, dates with the day name.
- → for your own sites, ↗ for sites of someone else, also after links in running text.

## Use it on a website

Copy the whole `dist/` folder into your site, so that `bojicas.css` and `fonts/` sit side by side, and link the stylesheet:

```html
<link rel="stylesheet" href="dist/bojicas.css?v=0.3.0">
```

The `?v=` mark matters: many servers let browsers keep a stylesheet for weeks. Give every new version a new mark, or visitors see new pages with old styles.

If your fonts live at another address, build the stylesheet for it. Only the Python standard library is needed:

```sh
python3 build.py --font-path /fonts/
```

## Change it

1. Change a value in `tokens.json`, or a component in `src/`.
2. Run `python3 build.py`. Never edit `dist/bojicas.css` by hand.
3. Open the example page in light and dark mode, at 360 px and on a wide screen:

   ```sh
   python3 -m http.server 8098 --bind 127.0.0.1
   ```

   then http://localhost:8098/example/
4. Raise the version in `tokens.json` and note the change in [`CHANGELOG.md`](CHANGELOG.md).

## Licence

- **Code** (`tokens.json`, `src/`, `dist/bojicas.css`, `build.py`, `example/`): [MIT](LICENSE).
- **Docs** (`docs/` and this README): [CC BY 4.0](LICENSE-docs.md).
- **Fonts:** SIL Open Font License 1.1, as they come; see `dist/fonts/`.
- **Names and logos** (Silviu Bojica, orgthread, the orgthread logo, the pen drawings) are not licensed.

Built by Silviu Bojica, with AI agents as the crew.
