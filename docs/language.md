# Language

A design system usually stops at colours and buttons. This one also sets how the words read, because a page that looks calm but reads in a hurry is not consistent. These rules apply to every page, post, slide, document, commit message and caption.

## Tone

- **Simple English.** Write for a smart reader who is not an expert and may not be a native speaker.
- **Short sentences.** One idea per sentence. Split a sentence that needs a semicolon.
- **Plain words.** "Use", not "utilise". "Help", not "facilitate".
- **Be thorough, not verbose.** Say everything that matters once.
- **An analogy helps** when a concept is new. One per idea is enough.

## Punctuation and form

- **No em dashes and no en dashes.** Use a full stop, a colon or a comma instead. A plain hyphen is fine inside words such as "open-source".
- **No contractions.** Write "do not", "it is", "there is", not "don't", "it's", "there's".
- **Sentence case** in headings: "How it works", not "How It Works".

## Numbers, units and dates

- **Metric units only:** Celsius, kilometres, kilograms, grams, millilitres.
- **Dates carry the day name.** On pages and slides: "Wednesday, 4 November 2026". In tables and notes: "2026-11-04 Wed".
- **Months for plans,** without a day: "February 2027".

## Names

- **orgthread** is always written in lower case, also in titles.
- **Never start a sentence with "orgthread".** Rephrase instead: "With orgthread in between, AI agents never touch your files directly." A lower-case word at the start of a sentence looks like a typo to readers who do not know the name.
- **Markdown** and **Org** keep their capital letters. They are names of formats.
- **Name the person before "he" or "his".** In each paragraph, the first mention is the name.

## Links and arrows

An arrow tells the reader, before the click, where a link goes. Buttons and links use it differently:

| Where the link goes | Button | Link in text, a caption or a list |
|---|---|---|
| A page of the same site | → | no mark |
| Another of your own sites | → | no mark |
| A site of someone else | ↗ | ↗, small and orange, after the text |

- **A button always has an arrow.** It stands alone, with no sentence around it, so the arrow turns it into a "go there". → means you stay with the same owner, for example a button from [bojica.com](https://bojica.com/) to [silviu.bojica.com](https://silviu.bojica.com/). ↗ means you go to someone else, for example LinkedIn, GitHub or Instagram.
- **A link in text only marks what leaves your sites.** The words around it already say where it goes. So only a link to a site of someone else gets the small ↗, as a warning that the reader leaves. Your own sites link to each other and carry no mark.
- **Links open in the same tab.** The reader can still open a new tab on purpose, and the Back button keeps working.
- **Link text says where it goes:** "orgthread on GitHub", not "click here".
- **Every web address in a text is a link.** When a text names a site, such as [bojica.com](https://bojica.com/), [silviu.bojica.com](https://silviu.bojica.com/) or [orgthread.dev](https://orgthread.dev/), the name links to it. This holds for pages, legal texts, posts and READMEs. On slides and in print, where nothing can be clicked, write the address in full.
- **Do not start a sentence with a lower-case address** either. Rephrase: "My own site", "The family page".

## Images

- **Every image has a real alt text** that says what it shows: "Pen drawing of Silviu Bojica, standing, hands in his pockets". Not "image" or "photo".
- **A logo's alt text** names the logo and what it shows: "orgthread logo: a thread woven through a star".
- **A photo by someone else carries a credit under it:** "Photo: Mika Baumeister on Unsplash", with the name and the source as links, each with its small ↗. A site with several such photos also lists them on a credits page, with the photo, its author, its source, its licence and where it is used.
- **A cover has the shape of a share card,** 1.91 : 1, so the same picture works above a post and in a shared link.
- **The source of a photo is at most 2400 px wide, with its metadata stripped** (for example `jpegtran -copy none`), so no camera data or C2PA block travels along. The site serves its own copy, in the sizes it needs; it never loads the photo from the photo service.

## What stays out

- **No framing around an employer** and no work content on personal pages.
- **No health data** on any public page.
