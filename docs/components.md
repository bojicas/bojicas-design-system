# Components

Every component is in `dist/bojicas.css` and shown on the [example page](../example/index.html). Each one works in light and dark mode and from 360 px to wide screens.

## Button

A blue pill with an arrow. The arrow says where the link goes.

```html
<a class="button" href="https://silviu.bojica.com/">silviu.bojica.com<span class="arrow arrow-own" aria-hidden="true">→</span></a>
<a class="button" href="https://github.com/bojicas" rel="noopener">GitHub<span class="arrow" aria-hidden="true">↗</span></a>
```

- `→` with `arrow arrow-own` for your own sites. `↗` with `arrow` for sites of someone else.
- A row of buttons goes in `<ul class="buttons">`, one `<li>` each.
- On hover the button fills with blue, and the arrow moves its way.

## Card

A raised panel, for example one person on a family page. Put cards in `<div class="cards">`: side by side on wide screens, one above the other on phones.

```html
<div class="cards">
  <section class="card">
    <img class="avatar" src="drawing-200.webp" srcset="drawing-200.webp 1x, drawing-400.webp 2x" width="200" height="200" alt="Pen drawing of …">
    <h2 class="title">Name</h2>
    <p class="role">Role</p>
    <p class="about">One short line.</p>
    <a class="button" href="…">…</a>
  </section>
</div>
```

## Avatar

A pen drawing in a circle, `168 px`, on its white paper in both modes. Give it two sizes, 200 and 400 px, as WebP without metadata.

## Eyebrow

A small mono label with a short orange bar. The bar sits above the label; add `bar-below` to put it under a centred label.

```html
<p class="eyebrow">Software architect</p>
<p class="eyebrow bar-below">The Bojicas</p>
```

## Titles

- `display`: the name on a home page.
- `title`: a page title.
- `lead`: the line under a title, in `muted`.
- `role`: a mono line under a name.

## Back link

`← Name` at the top of a page. On hover only the name is underlined; the arrow is part of the link but has no line under it.

```html
<a class="back-link" href="/"><span class="arrow" aria-hidden="true">←</span><span class="back-link-text">Silviu Bojica</span></a>
```

## Link to someone else's site

Every link to a site of someone else ends in a small orange `↗`, always in the mono font at label size (13 px), wherever it is: in running text, in a caption, in a list of facts. Only the text is underlined; the arrow has no line under it, like the arrow of the back link. A line never breaks between the last word and the arrow. On hover the arrow moves 1.5 px up and to the right, a little less than the arrow of a button, unless the reader asked for less motion. Screen readers skip the arrow. Links to your own sites, which link to each other, carry no mark. Links open in the same tab. A button always has its own arrow instead: → to your own sites, ↗ to others (see the table in the language docs).

```html
<a class="out" href="https://unsplash.com/"><span class="out-text">Unsplash</span><span class="arrow-out" aria-hidden="true">↗</span></a>
```

## Tags

A row of `#name` links, for example under the title of a post. Each tag is 44 px high. The orange `#` is part of the link, but it has no line under it: only the name is underlined, the same rule as the arrow of the back link. The `#` is hidden from screen readers, so they read only the name.

```html
<ul class="tags" aria-label="Tags">
  <li><a class="tag" href="/tags/design-system/"><span class="tag-mark" aria-hidden="true">#</span><span class="tag-name">design system</span></a></li>
</ul>
```

## Facts

A list of labels and values, for an owner, contact details or documents. Label beside value on wide screens, above it on phones. A value that is a link is 44 px high.

```html
<dl class="facts">
  <dt>Owner</dt><dd>Silviu-Dumitrel Bojica</dd>
  <dt>Email</dt><dd><a href="mailto:…">…</a></dd>
</dl>
```

## Footer

Copyright and place, then the legal links. The orange dots sit outside the links, so the underline stays under the words. On phones the legal links get their own line, without a leading dot.

```html
<footer class="footer">
  <p class="footer-meta"><span>© 2026 Silviu Bojica</span><span>Vienna, Austria</span></p>
  <ul class="footer-links">
    <li><a href="https://silviu.bojica.com/imprint/">Imprint</a></li>
    <li><a href="https://silviu.bojica.com/privacy/">Privacy</a></li>
  </ul>
</footer>
```

## Running text

Wrap an article in `<div class="prose">`: headings, paragraphs, lists with orange markers, and underlined blue links.

## Icon

A small line drawing in inline SVG, 24 px, in the colour of the text around it. The icons live in [`dist/icons/`](../dist/icons/): copy the SVG into the page, for example with Hugo's `readFile`. Never load an icon font or an icon from another server. An icon is for the eye only: it carries `aria-hidden="true"`, and the words next to it say what it means.

| File | Shows | Use |
|---|---|---|
| `money.svg` | a banknote | financial support |
| `package.svg` | a box | product sponsorship |
| `eye.svg` | an eye | brand visibility |
| `suitcase.svg` | a suitcase | travel and logistics support |
| `star.svg` | a star | brand ambassador |
| `trophy.svg` | a trophy | a win in the results |

## Hero

A large photo with a headline, one line under it, and up to two buttons, at the top of a home page. The text sits on a solid panel in the card colour, never on the photo itself. So the contrast of the text is the same as on any card, whatever the photo shows, in light and dark mode. There is no gradient, no shadow and no blur. On phones the panel sits under the photo and overlaps it a little. From 760 px it lies on the lower left part of the photo.

```html
<div class="hero">
  <img class="hero-photo" src="/photos/hero-1600.webp" srcset="/photos/hero-1200.webp 1200w, /photos/hero-1600.webp 1600w, /photos/hero-2400.webp 2400w" sizes="(min-width: 900px) 860px, 100vw" width="1600" height="900" alt="Alex Example serves on a clay court">
  <div class="hero-text">
    <h1 class="display">Alex Example</h1>
    <p class="lead">Professional tennis player from Example City.</p>
    <ul class="buttons">
      <li><a class="button" href="/results/">See results<span class="arrow arrow-own" aria-hidden="true">→</span></a></li>
      <li><a class="button" href="/partners/">Become a partner<span class="arrow arrow-own" aria-hidden="true">→</span></a></li>
    </ul>
  </div>
  <p class="hero-credit">Photo: Sam Example</p>
</div>
```

- The photo is a local file of the site, at most 2400 px wide, with its metadata stripped (see [Images](language.md#images)).
- The photo is cut to fit: 4 : 3 on phones, and 440 to 560 px high on wide screens, whatever the shape of the photo. Only a panel with more text makes it higher. Keep the subject away from the lower left corner, where the panel lies. To move the cut, add `style="object-position: 50% 30%"` to the image.
- The credit line is optional. A photo by someone else needs one.

## Stat row

Two to four big numbers, each with a label, for example "484, career-high WTA singles". A number may carry a small second line, for example "current 660". The digits have equal width, so a number that changes each week does not make the row jump. Two numbers per line on phones, all in one line on wide screens.

```html
<dl class="stats">
  <div class="stat">
    <dt class="stat-label">career-high WTA singles</dt>
    <dd class="stat-value">484</dd>
    <dd class="stat-note">current 660</dd>
  </div>
  <div class="stat">
    <dt class="stat-label">titles, all levels</dt>
    <dd class="stat-value">17</dd>
  </div>
</dl>
```

- The label comes first in the code, so a screen reader reads "career-high WTA singles, 484". On screen the number comes first.
- Keep labels short and in lower case, as they continue the number: "titles, all levels", not "Titles".
- The second line is optional.

## Results by season

One block per season, newest first. Each row is one event: its name, the place, the date of the first day, and the round reached in singles and in doubles. The design system shows every row it gets. The site decides which rows to show, for example only quarterfinals and up.

A win is never marked by colour alone. It shows the word "Winner", a trophy before it, in bold, and a short orange bar at the start of its row. The colour only adds to these.

From 760 px the season is a table with fixed columns, so the seasons line up under each other. Below 760 px each row becomes a small stack: the event on top, then each value with its label beside it. There is no sideways scroll.

```html
<div class="results">
  <section class="results-season" aria-labelledby="season-2026">
    <h2 class="results-year" id="season-2026">2026</h2>
    <table class="results-table" role="table" aria-labelledby="season-2026">
      <thead role="rowgroup">
        <tr role="row"><th role="columnheader" scope="col">Event</th><th role="columnheader" scope="col">Place</th><th role="columnheader" scope="col">Date</th><th role="columnheader" scope="col">Singles</th><th role="columnheader" scope="col">Doubles</th></tr>
      </thead>
      <tbody role="rowgroup">
        <tr role="row" class="results-row-win">
          <th role="rowheader" scope="row">W15 Example City</th>
          <td role="cell" data-label="Place">Example City, Austria</td>
          <td role="cell" data-label="Date" class="results-date"><time datetime="2026-11-02">2026-11-02 Mon</time></td>
          <td role="cell" data-label="Singles">Quarterfinal</td>
          <td role="cell" data-label="Doubles"><span class="results-win"><!-- trophy.svg -->Winner</span></td>
        </tr>
        <tr role="row">
          <th role="rowheader" scope="row">W15 Testville</th>
          <td role="cell" data-label="Place">Testville, Romania</td>
          <td role="cell" data-label="Date" class="results-date"><time datetime="2026-09-14">2026-09-14 Mon</time></td>
          <td role="cell" data-label="Singles">Semifinal</td>
          <td role="cell" data-label="Doubles" class="results-none">Not played</td>
        </tr>
      </tbody>
    </table>
  </section>
</div>
```

- The `role` attributes keep the table a table for screen readers in every browser, also when the CSS stacks it. Some browsers drop the table meaning of an element whose display changes.
- `data-label` holds the column name that shows beside each value on phones. Screen readers skip it there, as they already read the column head. In another language, translate it with the column heads.
- The round names are "Winner", "Final", "Semifinal", "Quarterfinal". A round that was not played shows "Not played" with `results-none`. Never a dash.
- Add `results-row-win` to a row with a win in singles or doubles, and wrap the word in `results-win` with the trophy icon before it.
- Dates follow the [language rules](language.md#numbers-units-and-dates) for tables: "2026-11-02 Mon".

## Photo grid

6 to 10 photos in even tiles, each with a real alt text and an optional credit line. Two columns on phones. From 640 px each tile is at least 220 px wide, so three or more columns appear as the room allows. Each tile is cut to 4 : 3.

```html
<ul class="photo-grid">
  <li>
    <figure class="photo">
      <img src="/photos/serve-800.webp" srcset="/photos/serve-800.webp 1x, /photos/serve-1600.webp 2x" width="800" height="600" loading="lazy" alt="Alex Example serves at W15 Example City, seen from behind the baseline">
      <figcaption class="photo-credit">Photo: Sam Example</figcaption>
    </figure>
  </li>
</ul>
```

- Every photo is a local file of the site. Give it two sizes, 800 and 1600 px wide, without metadata.
- The alt text says what the photo shows, as the [language rules](language.md#images) ask. Not "photo".
- A credit with a link to someone else's site uses `a.out` with its small ↗. In a credit, a link follows the line height, like a link in a sentence.
- To move the cut of one photo, add `style="object-position: 50% 20%"` to it.

## Icon list

Short items, each with an icon in a round tile and one line, for example the ways to partner. One column on phones, two or three on wide screens.

```html
<ul class="icon-list">
  <li><!-- money.svg -->Financial support</li>
  <li><!-- package.svg -->Product sponsorship</li>
  <li><!-- eye.svg -->Brand visibility</li>
  <li><!-- suitcase.svg -->Travel and logistics support</li>
  <li><!-- star.svg -->Brand ambassador</li>
</ul>
```

- Put the SVG of the icon in place of each comment. The icon is orange, in a tile with a hairline border.
- Keep each item to one short line. The icon list is not for links: a link list uses buttons.
