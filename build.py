"""Generates the static pages. Run: python build.py"""
import hashlib
import os
from html import escape
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://remiclassic.github.io/crystalsoffate/'
DOCS = 'https://docs.crystalsoffate.com/crystals-of-fate/'
DESC = ('Crystals of Fate is a multi-platform esports driven collectible card game, '
        'featuring real-time simultaneous interactive gameplay.')
PC = 'https://d33pj9i8vfml2r.cloudfront.net/Builds/CoF-PC.zip'
APK = 'https://d33pj9i8vfml2r.cloudfront.net/Builds/CoF-Android.apk'
HYPERPLAY = 'https://store.hyperplay.xyz/game/crystalsoffate'
DISCORD = 'https://discord.gg/9n9v3V9'
TWITTER = 'https://twitter.com/crystalsoffate'
YOUTUBE = 'https://www.youtube.com/channel/UCmg9NPExNEJ2cwftz03y1BA'
TELEGRAM = 'https://t.me/Skymarch_Collectors'
FACEBOOK = 'https://www.facebook.com/CrystalsofFate'

SPRITE = open(os.path.join(ROOT, 'content', 'sprite.html'), encoding='utf-8').read()
NAV = [('index.html', 'Home', 'home'), ('news.html', 'News', 'news'),
       ('genesis-sale.html', 'Genesis Sale', 'genesis'), (DOCS, 'Whitepaper', None),
       ('media.html', 'Media', 'media')]
SOCIAL = [(DISCORD, 'Discord', 'discord'), (TWITTER, 'Twitter', 'twitter'),
          (YOUTUBE, 'YouTube', 'youtube'), (TELEGRAM, 'Telegram', 'telegram')]


def stamp(path):
    """Content hash appended to CSS/JS URLs so browsers never show a stale copy."""
    with open(os.path.join(ROOT, path), 'rb') as f:
        return f'{path}?v={hashlib.md5(f.read()).hexdigest()[:8]}'


def icon(name, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} aria-hidden="true"><use href="#i-{name}"/></svg>'


def size(path):
    with Image.open(os.path.join(ROOT, path)) as im:
        return im.size


def img(path, alt, cls='', lazy=True):
    w, h = size(path)
    c = f' class="{cls}"' if cls else ''
    l = ' loading="lazy" decoding="async"' if lazy else ''
    # stamped so a replaced image is fetched again instead of being served from the browser's cache
    return f'<img{c} src="{stamp(path)}" alt="{escape(alt)}" width="{w}" height="{h}"{l}>'


def holo(path, alt, cls=''):
    """Card image with holographic foil and glare layers masked to its own shape."""
    w, h = size(path)
    m = f' style="-webkit-mask-image:url({path});mask-image:url({path})"'
    return (f'<span class="holo {cls}" style="--ar:{w / h:.4f}">'
            f'<img src="{path}" alt="{escape(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async">'
            f'<span class="holo__foil"{m}></span><span class="holo__glare"{m}></span></span>')


def ext(url):
    return ' target="_blank" rel="noopener"' if url.startswith('http') else ''


RULE = '<div class="rule rule--gold" aria-hidden="true">' + icon('diamond') + '</div>'


def social(extra=()):
    return ''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{icon(i)}</a>'
                   for u, n, i in list(SOCIAL) + list(extra))


def downloads(cls=''):
    return f'''<div class="downloads {cls}">
          <a class="dl dl--gold" href="{PC}">{icon('windows')}<span class="dl__text"><b>PC</b><small>Download Now</small></span></a>
          <a class="dl dl--blue" href="{HYPERPLAY}" target="_blank" rel="noopener">{icon('hyperplay')}<span class="dl__text dl__text--hp"><small>Download on</small><b>HyperPlay</b></span></a>
          <a class="dl dl--silver" href="{APK}">{icon('android')}<span class="dl__text"><b>Android</b><small>Download Now</small></span></a>
        </div>'''


def page(filename, title, active, main, desc=DESC, og='assets/img/og.jpg', preload=''):
    links = ''.join(
        f'<a{" class=\"is-active\" aria-current=\"page\"" if key == active else ""} href="{u}"{ext(u)}>{n}</a>'
        for u, n, key in NAV)
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <meta name="theme-color" content="#070d1f">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Crystals of Fate">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:image" content="{SITE}{og}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
  {preload}<link rel="stylesheet" href="{stamp('css/styles.css')}">
  <script>document.documentElement.className = 'js';</script>
</head>
<body class="page-{active or 'plain'}">
  <a class="skip" href="#main">Skip to content</a>
  {SPRITE}
  <header class="nav" id="top">
    <div class="nav__inner">
      <a class="brand" href="index.html" aria-label="Crystals of Fate home">
        {icon('crystal', 'brand__gem')}
        <span class="brand__text">Crystals <small>of</small> Fate</span>
      </a>
      <button class="sound" type="button" data-state="waiting" aria-label="Play music" aria-pressed="false">
        <span class="sound__bars" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
      </button>
      <button class="nav__toggle" aria-label="Menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
      <div class="nav__menu" id="menu">
        <nav class="nav__links" aria-label="Primary">{links}</nav>
        <div class="nav__social">{social()}</div>
        <a class="signup" href="{DISCORD}" target="_blank" rel="noopener"><span>Sign Up</span></a>
      </div>
    </div>
    <span class="nav__progress" aria-hidden="true"></span>
  </header>

  <main id="main">
{main}
  </main>

  <footer class="footer">
    <a class="footer__studio" href="https://www.skymarch-entertainment.com/" target="_blank" rel="noopener">{img('assets/img/skymarch-logo.webp', 'Skymarch Entertainment')}</a>
    <div class="footer__social">{social([(FACEBOOK, 'Facebook', 'facebook')])}</div>
    <nav class="footer__links" aria-label="Footer">
      <a href="news.html">News</a><a href="genesis-sale.html">Genesis Sale</a><a href="media.html">Media</a>
      <a href="support.html">Support</a><a href="terms.html">Terms of Use</a>
    </nav>
    <p class="footer__copy">&copy; <span id="year">2026</span> Skymarch Entertainment Inc.</p>
  </footer>

  <a class="to-top" href="#top" aria-label="Back to top">{icon('chevron')}</a>

  <div class="lightbox" hidden role="dialog" aria-modal="true" aria-label="Image viewer">
    <button class="lightbox__btn lightbox__close" aria-label="Close">{icon('close')}</button>
    <button class="lightbox__btn lightbox__prev" aria-label="Previous">{icon('chevron')}</button>
    <figure><img alt=""><figcaption></figcaption></figure>
    <button class="lightbox__btn lightbox__next" aria-label="Next">{icon('chevron')}</button>
  </div>

  <script src="{stamp('js/music.js')}" defer></script>
  <script src="{stamp('js/main.js')}" defer onerror="document.documentElement.className=''"></script>
</body>
</html>
'''
    with open(os.path.join(ROOT, filename), 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print('wrote', filename)


def banner(name, title, kicker=''):
    k = f'<p class="page-hero__kicker">{kicker}</p>' if kicker else ''
    return f'''    <section class="page-hero">
      <div class="page-hero__art" style="background-image:url(assets/img/banner-{name}.webp)"></div>
      <canvas class="motes" data-motes="0.6" aria-hidden="true"></canvas>
      <div class="page-hero__inner">{k}<h1>{title}</h1>{RULE}</div>
    </section>'''


def zoom(name, caption, cls=''):
    """Thumbnail that opens the full image in the lightbox."""
    t = f'assets/img/{name}-thumb.webp'
    return (f'<a class="shot {cls}" href="assets/img/{name}.webp" data-lightbox data-caption="{escape(caption)}">'
            f'{img(t, caption)}<span class="shot__label">{escape(caption)}</span></a>')


# ---------------------------------------------------------------- news data

POSTS = [
    dict(slug='patch-0-6-4-4-notes', title='Patch 0.6.4.4 Notes', date='Nov 25, 2024', iso='2024-11-25',
         read='2 min read', cover='p1-ui-title', banner='news',
         excerpt='New card art, user interface updates, wallet account interface, quality of life updates, '
                 'an account wide reset and bug fixes.'),
    dict(slug='patch-0-6-3-4-notes', title='Patch 0.6.3.4 Notes', date='Nov 20, 2024', iso='2024-11-20',
         read='2 min read', cover='p2-cover', banner='news',
         excerpt='New card art, two new battlegrounds, what is coming next and bug fixes.'),
]
MUST = ('<p class="callout">Make sure to delete any previous installed versions, you MUST download the new '
        'version in order to play!</p>')


def cards(prefix, n):
    return '<div class="card-wall" data-stagger>' + ''.join(
        holo(f'assets/img/{prefix}-card-{i:02d}.webp', 'New card art') for i in range(1, n + 1)) + '</div>'


def ul(items):
    return '<ul>' + ''.join(f'<li>{escape(i)}</li>' for i in items) + '</ul>'


POST_BODY = {
    'patch-0-6-4-4-notes': MUST + '<h2>New Card Art</h2>' + cards('p1', 12) + f'''
<h2>User Interface Updates</h2>
<h3>Main Title / Downloading Interface</h3>
{zoom('p1-ui-title', 'Main Title / Downloading Interface', 'shot--wide')}
<h3>Loading Interface</h3>
{zoom('p1-ui-loading', 'Loading Interface', 'shot--wide')}
<h2>Open Card Packs Update</h2>
{zoom('p1-ui-packs', 'Open Card Packs', 'shot--wide')}
<h2>Wallet Account Interface</h2>
{zoom('p1-ui-wallet', 'Wallet Account Interface', 'shot--wide')}
<h3>NFTs In Your Wallet</h3>
<p>As we prepare for the launch of the card pack opening, we have conducted thorough testing over the past few months, and we are fully confident that all card NFTs will operate flawlessly. To access your card NFTs, log into your account and enter your wallet credentials. If you own the corresponding NFTs, you will gain full access to utilize them as you wish.</p>
<h2>New Quality of Life Updates</h2>''' + ul([
        'Added "Drop Here" highlighted area in Edit Deck User Interface, when interacting with adding or removing cards from your deck or collection.',
        'Added "Waiting for Opponent" text and animations during PvP matchmaking cinematic introduction scene.',
        'Greyed out cards that can no longer be added with the new cards per deck limitations.',
    ]) + f'''
<h2>Account Wide Reset Complete</h2>
{zoom('p1-extra', 'Account Wide Reset Complete', 'shot--wide')}
<p>In light of the recent patch release, all accounts have been reset to prepare for the upcoming card pack opening feature. Rest assured, all NFTs you hold in your wallets will continue to grant you access to your in-game assets.</p>
<h2>Bug Fixes</h2>''' + ul([
        'Fixed an issue where many players get "stuck" on connecting indefinitely when downloading and playing the game for the first time.',
        'Fixed an issue in edit deck interface when adding or removing cards would create visual display bugs duplicating the cards in both the card collection area and the deck area.',
        'Fixed an issue in card collection interface that would show cards that the player did not own and would let them play with them.',
        'Fixed an issue in card collection interface that was not "syncing" NFT card assets to be able to be used.',
        'Fixed an issue when in wallet account area when logging in for the first time, cards would be stretched out and not showing up at the right resolution.',
        'Fixed an issue when attempting to change the skin of a hero on the edit deck screen then going back to the previous screen the selected skin was not being changed.',
        'Fixed an issue with poor resolution of assets in the wallet interface area.',
        'Fixed an issue on the PC build when exiting the game a crash bug would occur.',
    ]),
    'patch-0-6-3-4-notes': MUST + '<h2>New Card Art</h2>' + cards('p2', 9) + f'''
<h2>New Battlegrounds</h2>
<h3>Fireridge Dungeon</h3>
{zoom('p2-cover', 'Fireridge Dungeon', 'shot--wide')}
<p>Goblin King Ghorvok and his horde of goblins and ogres have taken over Fireridge Palace and are plotting something devious in the depths of Fireridge Dungeon.</p>
<h3>Colosseum</h3>
<p>In the distant reaches of the piercing sands region, the clash of combat and the cheers of the crowd resonate fiercely. The Colosseum stands ready, inviting those who dare to carve out their legacy and seize treasures through bold feats of bravery.</p>
<h2>Coming Soon</h2>
<h3>Account Wide Reset Coming Soon</h3>
<p>All accounts will be reset in preparation for the official release of the card pack feature, when this happens all of the available cards we have let everyone play with will be removed and you will have to find / trade / purchase them through card pack pulls or the marketplaces. Also as a gentle reminder card rewards from the campaign, are "soulbound" meaning non-tradeable (Non NFTs).</p>
<h3>Open Card Packs</h3>
<p>We have tested this feature and it works very well, all of the card pack pull rates and allocations are all working as intended from our extensive testing.</p>
<p>We are working on all the fancy graphics and animations for a fully immersive player experience. This is the biggest priority for our developers so stay tuned! There will be another mini update to ensure all art placeholder illustrations are completely replaced by all of our new card illustrations and then we will flip on the switch for everyone to turn in the card packs.</p>
<h3>Character Animations Update</h3>
<p>We are close to finishing our animations for all of the heroes, which means in the next big update before year's end you will finally see all your favorite characters fully animated.</p>
<h2>Bug Fixes</h2>''' + ul([
        'Fixed an issue where players would play with a hero then change and would end up playing with the previous selected heroes cards/deck.',
        'Fixed an issue where players could select a locked hero and be able to play with it in-game.',
    ]),
}


def post_card(p):
    return f'''<a class="post-card" href="{p['slug']}.html">
          <span class="post-card__img">{img(f"assets/img/{p['cover']}-thumb.webp", p['title'])}</span>
          <span class="post-card__body">
            <time datetime="{p['iso']}">{p['date']} &middot; {p['read']}</time>
            <strong>{p['title']}</strong>
            <span class="post-card__excerpt">{p['excerpt']}</span>
            <span class="more">Read more {icon('arrow')}</span>
          </span>
        </a>'''


# ---------------------------------------------------------------- home

# Home showcases: (title, background, kind, [(image, name, subtitle)]). Each becomes a swipeable carousel.
FEATURES = [
    ('Choose Your Hero', 'bg-hero', 'tall', [
        ('hero-celleste', 'Celleste', 'Guardian'), ('hero-davarok', 'Davarok', 'Warrior'), ('hero-saria', 'Saria', 'Assassin')]),
    ('Choose Your Cards', 'bg-cards', 'tall', [
        ('card-sylvana-allure', 'Sylvana Allure', 'Card'), ('card-dark-etheralite', 'Dark Etheralite', 'Card'),
        ('card-sprite-scout', 'Sprite Scout', 'Card')]),
    ('Choose From Multiple Pets', 'bg-pets', 'pets', [
        ('pet-nightmare', 'Nightmare', 'Pet'), ('pet-finley', 'Finley', 'Pet'), ('pet-hexx', 'Hexx', 'Pet')]),
    ('Choose Your Loadout', 'bg-battleground', 'tall', [
        ('emote-celleste', 'Celleste', 'Emote'), ('emote-corvax', 'Corvax', 'Emote'), ('emote-zarah', 'Zarah', 'Emote')]),
]


# Campaign region paintings from the game, shown in the battlegrounds gallery
REALMS = [('realm-ashmyst-falls', 'Ashmyst Falls'), ('realm-daunting-narrows', 'Daunting Narrows'),
          ('realm-deaths-summit', "Death's Summit"), ('realm-dragon-isle-2', 'Dragon Isle'), ('realm-dragon-isle', 'Dragon Isle'),
          ('realm-fireridge-crater', 'Fireridge Crater'), ('realm-mordania', 'Mordania'),
          ('realm-piercing-sands', 'Piercing Sands'), ('realm-reapers-glade', "Reaper's Glade")]


def showcase(title, kind, items):
    def slide(f, n, sub):
        path = f'assets/img/{f}.webp'
        # wide showcases frame a landscape painting; the others hold a card with holographic foil
        return img(path, n, 'slide__art') if kind == 'wide' else holo(path, f'{n} {sub.lower()}')
    slides = ''.join(
        f'<li class="slide" data-name="{escape(n)}" data-sub="{escape(sub)}">{slide(f, n, sub)}</li>'
        for f, n, sub in items)
    return f'''<div class="showcase showcase--{kind}" data-showcase data-reveal tabindex="0" role="group" aria-roledescription="carousel" aria-label="{title}">
          <i class="showcase__corner"></i><i class="showcase__corner"></i><i class="showcase__corner"></i><i class="showcase__corner"></i>
          <div class="showcase__beam" aria-hidden="true"></div>
          <div class="showcase__stage">
            <div class="showcase__pedestal" aria-hidden="true"></div>
            <ul class="showcase__track">{slides}</ul>
          </div>
          <div class="showcase__bar">
            <button class="showcase__nav showcase__nav--prev" type="button" aria-label="Previous">{icon('chevron')}</button>
            <div class="showcase__caption" aria-live="polite"><strong></strong><small></small></div>
            <button class="showcase__nav showcase__nav--next" type="button" aria-label="Next">{icon('chevron')}</button>
          </div>
          <div class="showcase__dots" aria-hidden="true"></div>
        </div>'''


# Hero scene layers, back to front. Position is % of the 1672x873 scene (left, top, width).
# depth: how far the layer shifts with the pointer; scroll: how much it lags behind the page as it scrolls.
# Scroll values stay >= 0: a layer that ran ahead of the page would lift its bottom edge into view.
LAYERS = {
    'clouds-back': dict(img='layer-clouds', pos=(-8, 18, 116), depth=.3, scroll=0.3),
    'island-d': dict(img='layer-island-d', pos=(26.5, 7, 3.2), depth=.4, scroll=0.38),
    'island-b': dict(img='layer-island-b', pos=(76.5, 5, 7.5), depth=.5, scroll=0.36),
    'island-c': dict(img='layer-island-c', pos=(86, 4, 11), depth=.7, scroll=0.34),
    'island-a': dict(img='layer-island-a', pos=(93, 44, 5), depth=.6, scroll=0.34),
    'castle': dict(img='layer-castle', pos=(9, -3, 100), depth=.9, scroll=0.22, inner='<div class="fx fx-water"></div>'),
    'clouds-front': dict(img='layer-clouds', pos=(-8, 38, 116), depth=1.6, scroll=0.12),
    'arch': dict(img='layer-arch', pos=(-3, -14, 46), depth=2.6, scroll=0.05),
    # the knight shares the arch's depth so he stays planted, and sits behind it so the parapet hides his feet
    'knight': dict(img='layer-knight', pos=(13.8, 50.6, 10.5), depth=2.6, scroll=.05, inner='<canvas class="cape"></canvas>'),
    'foliage': dict(img='layer-foliage', pos=(-3, -9, 106), depth=4.2, scroll=0),
}


def layer(key):
    l = LAYERS[key]
    left, top, width = l['pos']
    w, h = size(f"assets/img/{l['img']}.webp")
    kind = key.split('-')[0]
    return (f'<div class="layer layer--{kind} layer--{key}" aria-hidden="true" '
            f'style="left:{left}%;top:{top}%;width:{width}%;--d:{l["depth"]};--s:{l["scroll"]}">'
            f'<div class="layer__in"><img src="assets/img/{l["img"]}.webp" alt="" width="{w}" height="{h}" decoding="async">'
            f'{l.get("inner", "")}</div></div>')


LOGO_X, LOGO_Y, LOGO_W, LOGO_H = 29.486, 6.071, 41.029, 58.534  # logo box, % of the 1672x873 scene
SPARKS = [(50, 6.5, 0, 1.3), (35.3, 38, 1.1, 1), (41.3, 48, 2.3, .7), (58.9, 48, 3.1, .7), (41.6, 15.5, 1.7, .8),
          (58.6, 14, .6, .8), (50, 27, 2.8, 1.5), (64.6, 36, 3.7, .8), (46.2, 58.5, 4.3, .7), (30.5, 33, 4.9, .7)]


def home():
    feats = ''.join(f'''
    <section class="feature" style="--bg:url(../assets/img/{bg}.webp)">
      <div class="feature__inner">
        <h2 data-reveal>{title}</h2>{RULE}
        {showcase(title, kind, items)}
      </div>
    </section>''' for title, bg, kind, items in FEATURES)
    # SPARKS are placed in scene coordinates; the logo layer has its own box inside the scene
    sparks = ''.join(f'<i style="--x:{(x - LOGO_X) / LOGO_W * 100:.1f}%;--y:{(y - LOGO_Y) / LOGO_H * 100:.1f}%;--d:{d}s;--k:{k}"></i>'
                     for x, y, d, k in SPARKS)
    main = f'''    <section class="hero" aria-label="Crystals of Fate: a castle of waterfalls among floating islands">
      <div class="hero__art">
        <div class="scene">
          <div class="scene__inner">
            <img class="scene__img" src="assets/img/hero.webp" width="1672" height="873" fetchpriority="high" alt="">
            {''.join(layer(k) for k in ('clouds-back', 'island-d', 'island-b', 'island-c', 'island-a', 'castle'))}
            <div class="fx fx-fog fx-fog--a" aria-hidden="true"></div>
            <div class="fx fx-fog fx-fog--b" aria-hidden="true"></div>
            {layer('clouds-front')}
            <div class="fx fx-shade" aria-hidden="true"></div>
            <div class="fx fx-rays" aria-hidden="true"></div>
            <div class="fx fx-glow" aria-hidden="true"></div>
            <div class="logo3d">
              <div class="logo3d__body">
                <img class="logo3d__img" src="assets/img/logo.webp" width="1448" height="1078" fetchpriority="high" alt="Crystals of Fate">
                <div class="fx logo3d__glow" aria-hidden="true"></div>
                <div class="fx fx-shine" aria-hidden="true"></div>
                <div class="fx fx-sparks" aria-hidden="true">{sparks}</div>
              </div>
            </div>
            {layer('knight')}
            {layer('arch')}
            {layer('foliage')}
            <div class="fx fx-flash" aria-hidden="true"></div>
          </div>
        </div>
        <canvas class="hero__motes" aria-hidden="true"></canvas>
      </div>
      <div class="hero__content">
        <h1 class="hero__tagline">A Greater World Awaits</h1>
        <div class="rule rule--blue" aria-hidden="true">{icon('diamond')}</div>
        <ul class="hero__pillars">
          <li>Adventure</li><li>{icon('star')}Collect</li><li>{icon('star')}Battle</li><li>{icon('star')}Shape Your Fate</li>
        </ul>
        {downloads()}
        <div class="hero__motto">{RULE}<p>Fantasy Lives Forever</p></div>
      </div>
    </section>

    <section class="feature feature--intro feature--realms" style="--bg:url(../assets/img/bg-battleground.webp)">
      <div class="feature__backdrop" aria-hidden="true"><i></i><i></i></div>
      <div class="feature__inner">
        <h2 data-reveal>Battle In Immersive Battlegrounds</h2>{RULE}
        <p data-reveal>A multi-platform collectible card game with real-time, simultaneous, interactive gameplay.</p>
        {showcase('Battlegrounds', 'wide', [(f, n, 'Realm') for f, n in REALMS])}
      </div>
    </section>
{feats}

    <section class="feature feature--news" style="--bg:url(../assets/img/bg-packs.webp)">
      <div class="feature__inner">
        <h2 data-reveal>Latest News</h2>{RULE}
        <div class="post-grid" data-stagger>
        {''.join(post_card(p) for p in POSTS)}
        </div>
        <a class="btn" href="news.html">All news {icon('arrow')}</a>
      </div>
    </section>

    <section class="feature feature--cta" id="download" style="--bg:url(../assets/img/bg-cards.webp)">
      <canvas class="motes" data-motes="0.8" aria-hidden="true"></canvas>
      <div class="feature__inner">
        <h2 data-reveal>Battle For Glory</h2>{RULE}
        <p data-reveal>Download and play today.</p>
        {downloads('downloads--static')}
      </div>
    </section>'''
    page('index.html', 'Crystals of Fate | A Greater World Awaits', 'home', main,
         preload='<link rel="preload" as="image" href="assets/img/hero.webp"><link rel="preload" as="image" href="assets/img/logo.webp">\n  ')


# ---------------------------------------------------------------- news

def news():
    main = banner('news', 'News') + f'''
    <section class="section">
      <div class="wrap">
        <div class="post-grid post-grid--list" data-stagger>
        {''.join(post_card(p) for p in POSTS)}
        </div>
      </div>
    </section>'''
    page('news.html', 'News | Crystals of Fate', 'news', main,
         desc='Patch notes and announcements for Crystals of Fate.')
    for i, p in enumerate(POSTS):
        other = POSTS[1 - i]
        main = banner(p['banner'], p['title'], f'<time datetime="{p["iso"]}">{p["date"]}</time> &middot; {p["read"]}') + f'''
    <article class="section">
      <div class="wrap wrap--narrow prose">
        <a class="back" href="news.html">{icon('arrow')} All news</a>
        {POST_BODY[p['slug']]}
        <div class="post-nav">
          <a class="btn" href="index.html#download">Download the game {icon('download')}</a>
          <a class="btn btn--ghost" href="{other['slug']}.html">{other['title']} {icon('arrow')}</a>
        </div>
      </div>
    </article>'''
        page(p['slug'] + '.html', f"{p['title']} | Crystals of Fate", 'news', main, desc=p['excerpt'],
             og=f"assets/img/{p['cover']}-thumb.webp")


# ---------------------------------------------------------------- genesis sale

G = DOCS + 'genesis-sale/genesis-sale-packages/'
GENESIS = [
    ('Genesis Card Packs', 'bg-packs', [], [
        ('g-pack-rare', 'Genesis Rare Card Pack', 'rare', 'Card Pack', G + 'card-packs/genesis-rare-card-pack'),
        ('g-pack-epic', 'Genesis Epic Card Pack', 'epic', 'Card Pack', G + 'card-packs/genesis-epic-card-pack'),
        ('g-pack-legendary', 'Genesis Legendary Card Pack', 'legendary', 'Card Pack', G + 'card-packs/genesis-legendary-card-pack'),
    ]),
    ('Hero Skin Packages', 'bg-battleground', [], [
        ('g-skin-saria', 'Blood Dragon Saria', 'rare', 'Assassin', G + 'hero-skin-packages/rare-limited-edition-skin-blood-dragon-saria-assassin'),
        ('g-skin-grahn', 'Earth Breaker Grahn', 'rare', 'Guardian', G + 'hero-skin-packages/rare-limited-edition-skin-earth-breaker-grahn-guardian'),
        ('g-skin-lilly', 'Shadowborn Lilly', 'rare', 'Support', G + 'hero-skin-packages/rare-limited-edition-skin-shadowborn-lilly-support'),
        ('g-skin-valanar', 'Dark Prince Valanar', 'epic', 'Necromancer', G + 'hero-skin-packages/epic-limited-edition-skin-dark-prince-valanar-necromancer'),
        ('g-skin-aveena', 'Fireborn Aveena', 'epic', 'Mage', G + 'hero-skin-packages/epic-limited-edition-skin-fireborn-aveena-mage'),
        ('g-skin-corvax', 'Sacred Knight Corvax', 'epic', 'Warrior', G + 'hero-skin-packages/epic-limited-edition-skin-sacred-knight-corvax-warrior'),
    ]),
    ('Epic Hero Packages', 'bg-cards', [], [
        ('g-hero-morghar', 'Morghar', 'epic', 'Guardian', G + 'epic-hero-packages/epic-hero-package-morghar-guardian'),
        ('g-hero-viphorra', 'Viphorra', 'epic', 'Necromancer', G + 'epic-hero-packages/epic-hero-package-viphorra-necromancer'),
    ]),
    ('Legendary Founder Token Packages', 'bg-hero',
     ['Only 500 total of each available', 'Each package comes with one Founder Token'], [
        ('g-founder-bellina', 'Bellina', 'legendary', 'Support', G + 'founder-token-packages/legendary-packages/genesis-founder-token-legendary-edition-bellina-support'),
        ('g-founder-jester', 'Jester', 'legendary', 'Mage', G + 'founder-token-packages/legendary-packages/genesis-founder-token-legendary-edition-jester-mage'),
        ('g-founder-zamir', 'Zamir', 'legendary', 'Assassin', G + 'founder-token-packages/legendary-packages/genesis-founder-token-legendary-edition-zamir-assasin'),
        ('g-founder-zarah', 'Zarah', 'legendary', 'Necromancer', G + 'founder-token-packages/legendary-packages/genesis-founder-token-legendary-edition-zarah-necromancer'),
    ]),
    ('Mythic Founder Token Packages', 'bg-mythic',
     ['Only 250 of each available', "Each Founder's Token package comes with one Founder Token"], [
        ('g-founder-celleste', 'Celleste', 'mythic', 'Guardian', G + 'founder-token-packages/mythic-packages/genesis-founder-token-mythic-edition-celleste-guardian'),
        ('g-founder-davarok', 'Davarok', 'mythic', 'Warrior', G + 'founder-token-packages/mythic-packages/genesis-founder-token-mythic-edition-davarok-warrior'),
    ]),
]


def notes(lines):
    return '<p class="notes" data-reveal>' + ''.join(f'<span>{escape(l)}</span>' for l in lines) + '</p>' if lines else ''


def item(name, title, rarity, role, url):
    return f'''<a class="item item--{rarity} tilt" href="{url}" target="_blank" rel="noopener">
            <span class="item__media"><video muted loop playsinline preload="none" poster="assets/img/{name}.webp" data-autoplay aria-label="{escape(title)}"><source src="assets/video/{name}.mp4" type="video/mp4"></video><span class="holo__foil"></span><span class="holo__glare"></span></span>
            <span class="item__meta"><em>{rarity}</em><strong>{escape(title)}</strong><small>{role}</small></span>
            <span class="more">View details {icon('external')}</span>
          </a>'''


def genesis():
    info = DOCS + 'genesis-sale/genesis-sale-information'
    uniques = ''
    for count, label, bg, odds, names in (
            ('2', 'Unique Mythic Cards', 'bg-cards', '1 / 1', ('g-mythic-1', 'g-mythic-2')),
            ('2', 'Ultra Unique Legendary Cards', 'bg-battleground', '1 / 10', ('g-legendary-1', 'g-legendary-2'))):
        cells = ''.join(f'''<a class="unique" href="{info}" target="_blank" rel="noopener">
            <span class="unique__odds">{odds}</span>{holo(f'assets/img/{n}.webp', label, 'holo--rare')}</a>''' for n in names)
        uniques += f'''
    <section class="feature" style="--bg:url(../assets/img/{bg}.webp)">
      <div class="feature__inner">
        <h2 data-reveal><span class="count">{count}</span> {label}</h2>{RULE}
        <div class="uniques" data-stagger>{cells}</div>
      </div>
    </section>'''
    groups = ''
    for title, bg, lines, items in GENESIS:
        if title.startswith('Legendary Founder'):
            groups += f'''
    <section class="feature" id="founder-tokens" style="--bg:url(../assets/img/bg-hero.webp)">
      <div class="feature__inner">
        <h2 data-reveal>Founder Tokens</h2>{RULE}
        <a class="token" data-reveal href="{DOCS}token-nfts-and-economics/nft-information/founders-tokens" target="_blank" rel="noopener">{img('assets/img/g-founder-token.webp', 'Crystals of Fate Founder Token')}</a>
        {notes(['Only 2500 total available', 'Only available in Founder Token packages'])}
      </div>
    </section>'''
        groups += f'''
    <section class="feature" style="--bg:url(../assets/img/{bg}.webp)">
      <div class="feature__inner">
        <h2 data-reveal>{title}</h2>{RULE}
        {notes(lines)}
        <div class="items items--{len(items)}" data-stagger>
          {''.join(item(*i) for i in items)}
        </div>
      </div>
    </section>'''
    main = banner('genesis', 'Genesis Sale') + f'''
    <section class="section section--tight">
      <div class="wrap">
        <h2 class="section__title" data-reveal>Get Your NFTs Here</h2>
        <div class="markets" data-stagger>
          <a class="market" href="https://agora.elysiumchain.tech/Collections/Profile/?collectionId=41e67133-d7b1-4c73-8cc7-03136dd8ae77" target="_blank" rel="noopener">{img('assets/img/g-market-agora.webp', 'Agora marketplace on Elysium')}<span class="more">Agora on Elysium {icon('external')}</span></a>
          <a class="market" href="https://myria.com/marketplace/collection/?id=2e611b42-adbb-43ed-9d23-46275950ea8d" target="_blank" rel="noopener">{img('assets/img/g-market-myria.webp', 'Myria marketplace')}<span class="more">Myria Marketplace {icon('external')}</span></a>
        </div>
        <a class="btn btn--ghost" href="{info}" target="_blank" rel="noopener">Genesis Sale information {icon('external')}</a>
      </div>
    </section>{uniques}{groups}'''
    page('genesis-sale.html', 'Genesis Sale | Crystals of Fate', 'genesis', main,
         desc='Genesis Sale: unique cards, card packs, hero skin packages and Founder Token packages for Crystals of Fate.')


# ---------------------------------------------------------------- media

SHOTS = [('shot-main-interface', 'Main Interface'), ('shot-hero-selection', 'Hero Selection'),
         ('shot-edit-deck', 'Edit Deck'), ('shot-battle', 'Battle'), ('shot-emotes', 'Emotes'),
         ('shot-pets', 'Pets'), ('shot-versus', 'Versus Screen')]
ART = [('art-aveena-moonfrost', 'Aveena Moonfrost'), ('art-corvax-bladefire', 'Corvax Bladefire'),
       ('art-grahn-stormhammer', 'Grahn Stormhammer'), ('art-lilly-goldheart', 'Lilly Goldheart'),
       ('art-saria-shadowblade', 'Saria Shadowblade'), ('art-valanar-dreadmire', 'Valanar Dreadmire')]


def media():
    def brand(key, title):
        f = f'assets/press/crystals-of-fate-{key}.png'
        mb = os.path.getsize(os.path.join(ROOT, f)) / 1e6
        return f'''<a class="brand-tile" href="{f}" download>
            <span class="brand-tile__img">{img(f'assets/img/press-{key}.webp', title)}</span>
            <strong>{title}</strong><small>{mb:.1f} MB PNG</small>
            <span class="more">Download {icon('download')}</span>
          </a>'''
    main = banner('media', 'Media') + f'''
    <section class="section">
      <div class="wrap">
        <h2 class="section__title" data-reveal>Visual Identity</h2>
        <div class="brand-tiles" data-stagger>
          {brand('logo', 'Crystals of Fate Logo')}
          {brand('monogram', 'Crystals of Fate Monogram')}
        </div>
      </div>
    </section>
    <section class="section section--alt">
      <div class="wrap">
        <h2 class="section__title" data-reveal>Gameplay Screenshots</h2>
        <div class="shots" data-stagger>{''.join(zoom(n, c) for n, c in SHOTS)}</div>
      </div>
    </section>
    <section class="section">
      <div class="wrap">
        <h2 class="section__title" data-reveal>Main Character Art Illustrations</h2>
        <div class="shots shots--art" data-stagger>{''.join(zoom(n, c) for n, c in ART)}</div>
      </div>
    </section>'''
    page('media.html', 'Media | Crystals of Fate', 'media', main,
         desc='Crystals of Fate logos, gameplay screenshots and character art.')


# ---------------------------------------------------------------- support / terms / 404

def support():
    main = banner('support', 'Support') + f'''
    <section class="section">
      <div class="wrap wrap--narrow">
        <p class="lead" data-reveal>If you have a question or problem, reach the team on one of these channels.</p>
        <div class="channels" data-stagger>
          <a class="channel" href="{DISCORD}" target="_blank" rel="noopener">{icon('discord')}<strong>Discord</strong><small>Ask in the community server</small><span class="more">Open Discord {icon('external')}</span></a>
          <a class="channel" href="{TELEGRAM}" target="_blank" rel="noopener">{icon('telegram')}<strong>Telegram</strong><small>Skymarch Collectors group</small><span class="more">Open Telegram {icon('external')}</span></a>
          <a class="channel" href="{TWITTER}" target="_blank" rel="noopener">{icon('twitter')}<strong>Twitter</strong><small>@crystalsoffate</small><span class="more">Open Twitter {icon('external')}</span></a>
        </div>
        <div class="post-nav">
          <a class="btn btn--ghost" href="{DOCS}" target="_blank" rel="noopener">Read the whitepaper {icon('external')}</a>
          <a class="btn btn--ghost" href="news.html">Latest patch notes {icon('arrow')}</a>
        </div>
      </div>
    </section>'''
    page('support.html', 'Support | Crystals of Fate', 'support', main, desc='Get help with Crystals of Fate.')


def terms():
    body = open(os.path.join(ROOT, 'content', 'terms.html'), encoding='utf-8').read()
    main = banner('support', 'Terms of Service') + f'''
    <section class="section">
      <div class="wrap wrap--narrow prose prose--legal">
{body}
      </div>
    </section>'''
    page('terms.html', 'Terms of Service | Crystals of Fate', 'terms', main,
         desc='Terms of service for Skymarch Entertainment games, apps, websites and other services.')


def not_found():
    main = banner('media', 'Page Not Found') + f'''
    <section class="section">
      <div class="wrap wrap--narrow" style="text-align:center">
        <p class="lead">This path leads nowhere.</p>
        <a class="btn" href="{SITE}">Return home {icon('arrow')}</a>
      </div>
    </section>'''
    page('404.html', 'Page Not Found | Crystals of Fate', None, main)
    # 404 can be served from any depth, so its assets need absolute URLs
    p = os.path.join(ROOT, '404.html')
    s = open(p, encoding='utf-8').read()
    for a in ('assets/', 'css/', 'js/'):
        s = s.replace(f'="{a}', f'="{SITE}{a}').replace(f'url({a}', f'url({SITE}{a}')
    for f in ('index', 'news', 'genesis-sale', 'media', 'support', 'terms'):
        s = s.replace(f'href="{f}.html"', f'href="{SITE}{f}.html"')
    open(p, 'w', encoding='utf-8', newline='\n').write(s)


if __name__ == '__main__':
    home(); news(); genesis(); media(); support(); terms(); not_found()
