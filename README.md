# Crystals of Fate website

Static site for [Crystals of Fate](https://www.crystalsoffate.com/), served with GitHub Pages (`SkymarchEntertainment/crystalsoffate`, `main` branch root) at https://www.crystalsoffate.com/. DNS is managed in Wix

## Pages

| Page | File |
| --- | --- |
| Home | `index.html` |
| News and patch notes | `news.html`, `patch-0-6-4-4-notes.html`, `patch-0-6-3-4-notes.html` |
| Genesis Sale | `genesis-sale.html` |
| Media | `media.html` |
| Support, Terms | `support.html`, `terms.html` |
| The game, in the browser | `play/` (generated, see "Play in browser") |

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

## Play in browser

The "Play Now" buttons (top bar, hero, bottom call to action) open `play/`, the browser build of the game. Players sign in or create an account there; nothing is downloaded.

- `play/` is generated: run `npm run deploy:site` in the game project (`cof-playcanvas`). It replaces the folder but keeps `play/config.js`.
- Accounts and online matches need the game's server (`node server/match-server.mjs` in the game project) running somewhere reachable over `wss://`. Put its address in `play/config.js` (`window.COF_SERVER = 'wss://...'`). Without it the sign-in screen answers "Could not connect to the server".
- To send the buttons somewhere else (for example to the server itself, which can also serve the game), change `PLAY` in `build.py`.

## Preview locally

```bash
python -m http.server 4173
```
