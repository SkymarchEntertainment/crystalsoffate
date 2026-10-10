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

## Hero scene

The hero is built from separate layers so they can move at different depths. Back to front: sky plate (`hero.webp`), far clouds, floating islands, castle, near clouds, logo, stone arch, foreground foliage.

- Layer positions, pointer depth and scroll drift are set in `LAYERS` in `build.py`
- `logo.webp` tilts toward the pointer; `mask-logo.png` limits its shine sweep to the gold lettering
- `mask-water.png` limits the falling shimmer to the castle's waterfalls
- `.hero__motes` canvas draws the drifting motes and petals

All motion is disabled under `prefers-reduced-motion`.

## Music

`js/music.js` plays `assets/audio/main-theme.mp3` (the game's main menu theme) on a loop. Browsers block sound until the visitor interacts with the page, so it starts on the first click, tap or key press when autoplay is refused. The nav button mutes it; the choice is remembered, and playback carries on from the same point across pages.

## Preview locally

```bash
python -m http.server 4173
```
