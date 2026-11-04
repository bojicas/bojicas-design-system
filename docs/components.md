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

Every link to a site of someone else ends in a small orange `↗`, always in the mono font at label size (13 px), wherever it is: in running text, in a caption, in a list of facts. Only the text is underlined; the arrow has no line under it, like the arrow of the back link. A line never breaks between the last word and the arrow. On hover the arrow moves 1.5 px up and to the right, a little less than the arrow of a button, unless the reader asked for less motion. Screen readers skip the arrow. Links to your own sites, which link to each other, carry no mark. Links open in the same tab.

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
