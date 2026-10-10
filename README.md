# Crystals of Fate website

Static site for [Crystals of Fate](https://www.crystalsoffate.com/), served with GitHub Pages from the `main` branch root: https://remiclassic.github.io/crystalsoffate/

## Pages

| Page | File |
| --- | --- |
| Home | `index.html` |
| News and patch notes | `news.html`, `patch-0-6-4-4-notes.html`, `patch-0-6-3-4-notes.html` |
| Genesis Sale | `genesis-sale.html` |
| Media | `media.html` |
| Support, Terms | `support.html`, `terms.html` |

## Editing

The HTML files are generated. Edit `build.py` (page content, nav, footer) or `content/` (terms text, icon sprite), then run:

```bash
python build.py
```

`css/styles.css` and `js/main.js` are edited directly. `build.py` needs Pillow to read image sizes.

To add a news post, add an entry to `POSTS` and its body to `POST_BODY` in `build.py`.

## Hero animation

`assets/img/hero.webp` is the key art with the logo painted in. The motion is layered on top of it in CSS and a canvas:

- `mask-logo.png` limits the shine sweep to the gold lettering and keeps the light rays behind it
- `mask-water.png` limits the falling shimmer to the waterfalls
- `.hero__motes` canvas draws the drifting motes and petals

All of it is disabled under `prefers-reduced-motion`.

## Preview locally

```bash
python -m http.server 4173
```
