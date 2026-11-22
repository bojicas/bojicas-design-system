# Foundations: colour, type, space

All values live in [`tokens.json`](../tokens.json). `build.py` turns them into CSS variables in `dist/bojicas.css`. For slides and documents, copy the values from the tables below.

## Colour

Blue and orange on a light or a deep navy ground. **Never red, and never black as an accent.** Text is a deep navy, not black.

| Token | Light | Dark | Use |
|---|---|---|---|
| `bg` | `#FAFBFC` | `#0F1B2D` | Page background |
| `card` | `#FFFFFF` | `#15243A` | Cards and raised panels |
| `ink` | `#14233A` | `#E4ECF5` | Body text and headings |
| `muted` | `#4A5A70` | `#9AAABD` | Labels, captions, footer |
| `line` | `#DDE3EA` | `#2A3A52` | Hairline borders, dividers |
| `blue` | `#226DBD` | `#6AA6E8` | Links, buttons, focus in light mode |
| `orange` | `#E8740C` | `#F28C28` | Accent bars, arrows, dots, list markers, focus in dark mode |
| `paper` | `#FAFBFC` | `#F2F4F7` | The ground behind pen drawings |

- **Orange is an accent, not a text colour** on the light background. It is too faint for small text there.
- **Focus rings** are blue in light mode and orange in dark mode, where blue is too faint.
- **Every page works in both modes.** The CSS follows the visitor's system setting.

### Kinship with the Life Org Design System

The blue `#226DBD` and the orange `#E8740C` / `#F28C28` are the same hues as in Silviu Bojica's private Life Org Design System. Text and line colours are close. The two systems share no files and depend on each other in no way: this one copies the values and goes its own way from there.

## Type

| Role | Font | Weights | Use |
|---|---|---|---|
| `sans` | [Space Grotesk](https://floriankarsten.github.io/space-grotesk/) | 400, 600 | All text: headings, body, buttons |
| `mono` | [JetBrains Mono](https://www.jetbrains.com/lp/mono/) | 400 | Small labels, the role line, fact labels, the footer, back links, code |

| Size token | Value | Use |
|---|---|---|
| `size-display` | 42 to 64 px | The name on a home page |
| `size-title` | 36 to 48 px | Page titles |
| `size-lead` | 21 px | The line under a title |
| `size-h2` | 22 px | Section headings |
| `size-body` | 17 px | Running text, line height 1.6 |
| `size-small` | 14 px | Mono labels |
| `size-label` | 13 px | Footer |

**Fonts are served from your own site,** never from a font service, so no visitor data leaves the page. Both fonts are under the SIL Open Font License and may be shared with their licence files.

## Space and shape

| Token | Value |
|---|---|
| `space-xs` / `s` / `m` / `l` / `xl` | 6 / 12 / 24 / 40 / 72 px |
| `radius-card` | 16 px |
| `radius-pill` | fully round, for buttons |
| `touch-min` | 44 px: the least height of every button and of every link that stands alone |

## Rules that hold everywhere

- **Light and dark mode,** from a phone width of 360 px to wide screens, with no sideways scroll.
- **Buttons and links that stand alone at least 44 px high,** such as the back link, tags, footer links and list items. A link inside a sentence follows the line height instead: in running text, and in a short credit such as "Photo: name on Unsplash". A 44 px line would tear the text apart, and the accessibility rules (WCAG 2.2, target size) exempt such links.
- **No requests to other servers:** no CDNs, no font services, no analytics, no embeds. Links to other sites are fine.
- **Flat surfaces:** no gradients, no shadows, no glow.
- **Text never sits on a photo by itself.** It sits on a solid panel in the card colour, as in the hero, so it keeps its contrast whatever the photo shows.
- **Numbers that are compared have digits of equal width** (`font-variant-numeric: tabular-nums`), as in the stat row and the results.
- **Icons are inline SVG,** from [`dist/icons/`](../dist/icons/). No icon font. An icon never carries a meaning alone: a word next to it does.
