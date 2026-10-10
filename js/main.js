const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;

/* ---- nav ---- */
const toggle = document.querySelector('.nav__toggle');
const menu = document.getElementById('menu');

function setMenu(open) {
  menu.classList.toggle('is-open', open);
  toggle.setAttribute('aria-expanded', String(open));
}

toggle.addEventListener('click', () => setMenu(!menu.classList.contains('is-open')));
menu.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });

document.getElementById('year').textContent = new Date().getFullYear();

/* ---- scroll reveal, lazy video ---- */
const revealIO = new IntersectionObserver((entries) => {
  for (const entry of entries) {
    if (!entry.isIntersecting) continue;
    entry.target.classList.add('is-in');
    revealIO.unobserve(entry.target);
  }
}, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
document.querySelectorAll('[data-reveal], [data-stagger]').forEach((el) => revealIO.observe(el));

const videoIO = new IntersectionObserver((entries) => {
  for (const { target, isIntersecting } of entries) {
    if (isIntersecting && !reduceMotion) target.play().catch(() => {});
    else target.pause();
  }
}, { threshold: 0.25 });
document.querySelectorAll('video[data-autoplay]').forEach((v) => videoIO.observe(v));

/* ---- card tilt ---- */
if (finePointer && !reduceMotion) {
  document.querySelectorAll('.tilt').forEach((el) => {
    el.addEventListener('pointermove', (e) => {
      const r = el.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5;
      const y = (e.clientY - r.top) / r.height - 0.5;
      el.style.setProperty('--ry', `${x * 14}deg`);
      el.style.setProperty('--rx', `${-y * 14}deg`);
    });
    el.addEventListener('pointerleave', () => {
      el.style.removeProperty('--rx');
      el.style.removeProperty('--ry');
    });
  });
}

/* ---- lightbox ---- */
const lightbox = document.querySelector('.lightbox');
const shots = [...document.querySelectorAll('[data-lightbox]')];
if (lightbox && shots.length) {
  const image = lightbox.querySelector('img');
  const caption = lightbox.querySelector('figcaption');
  let index = 0;
  let opener = null;

  const show = (i) => {
    index = (i + shots.length) % shots.length;
    image.classList.add("is-loading");
    image.onload = () => image.classList.remove("is-loading");
    image.src = shots[index].href;
    image.alt = caption.textContent = shots[index].dataset.caption;
  };
  const close = () => {
    lightbox.hidden = true;
    document.body.style.overflow = '';
    opener?.focus();
  };

  shots.forEach((a, i) => a.addEventListener('click', (e) => {
    e.preventDefault();
    opener = a;
    show(i);
    lightbox.hidden = false;
    document.body.style.overflow = 'hidden';
    lightbox.querySelector('.lightbox__close').focus();
  }));
  lightbox.querySelector('.lightbox__close').addEventListener('click', close);
  lightbox.querySelector('.lightbox__prev').addEventListener('click', () => show(index - 1));
  lightbox.querySelector('.lightbox__next').addEventListener('click', () => show(index + 1));
  lightbox.addEventListener('click', (e) => { if (e.target === lightbox || e.target.tagName === 'FIGURE') close(); });
  document.addEventListener('keydown', (e) => {
    if (lightbox.hidden) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(index - 1);
    if (e.key === 'ArrowRight') show(index + 1);
  });
}

/* ---- hero scene: pointer parallax, drifting motes and petals ---- */
const hero = document.querySelector('.hero');
if (hero && !reduceMotion) {
  const art = hero.querySelector('.hero__art');
  const inner = hero.querySelector('.scene__inner');
  const canvas = hero.querySelector('.hero__motes');
  const ctx = canvas.getContext('2d');
  let w = 0, h = 0, dpr = 1, running = false, last = 0, mx = 0, my = 0;

  if (finePointer) {
    hero.addEventListener('pointermove', (e) => {
      const r = art.getBoundingClientRect();
      mx = (e.clientX - r.left) / r.width - 0.5;
      my = (e.clientY - r.top) / r.height - 0.5;
      inner.style.setProperty('--px', `${-mx * 16}px`);
      inner.style.setProperty('--py', `${-my * 10}px`);
    });
    hero.addEventListener('pointerleave', () => {
      mx = my = 0;
      inner.style.setProperty('--px', '0px');
      inner.style.setProperty('--py', '0px');
    });
  }

  const rand = (a, b) => a + Math.random() * (b - a);
  const mote = (fresh) => ({
    petal: false,
    x: rand(0, 1), y: fresh ? rand(0, 1) : 1.05,
    r: rand(0.8, 2.6), vy: rand(0.012, 0.045), sway: rand(0.4, 1.4), phase: rand(0, 6.28),
    depth: rand(0.3, 1), hue: Math.random() < 0.25 ? 45 : rand(195, 215),
  });
  const petal = (fresh) => ({
    petal: true,
    x: fresh ? rand(-0.1, 1) : rand(-0.3, 0.6), y: fresh ? rand(0, 1) : -0.05,
    r: rand(3, 7), vy: rand(0.03, 0.07), vx: rand(0.02, 0.06), spin: rand(-2, 2), phase: rand(0, 6.28),
    depth: rand(0.6, 1.4), blue: Math.random() < 0.35,
  });
  let parts = [];

  function resize() {
    const r = canvas.getBoundingClientRect();
    if (Math.abs(r.width - w) < 1 && Math.abs(r.height - h) < 1) return;
    dpr = Math.min(devicePixelRatio || 1, 2);
    w = r.width; h = r.height;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    const motes = Math.round(Math.min(90, w / 16));
    const petals = Math.round(Math.min(16, w / 90));
    parts = [...Array.from({ length: motes }, () => mote(true)), ...Array.from({ length: petals }, () => petal(true))];
  }

  function frame(t) {
    if (!running) return;
    const dt = Math.min((t - last) / 1000, 0.05);
    last = t;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    for (let i = 0; i < parts.length; i++) {
      const p = parts[i];
      p.phase += dt;
      const ox = -mx * 26 * p.depth, oy = -my * 16 * p.depth;
      if (p.petal) {
        p.y += p.vy * dt;
        p.x += (p.vx + Math.sin(p.phase * 0.9) * 0.02) * dt;
        if (p.y > 1.06 || p.x > 1.1) { parts[i] = petal(false); continue; }
        ctx.save();
        ctx.translate(p.x * w + ox, p.y * h + oy);
        ctx.rotate(p.phase * p.spin);
        ctx.scale(1, 0.45 + 0.35 * Math.sin(p.phase * 2.2));
        ctx.globalAlpha = 0.75;
        ctx.fillStyle = p.blue ? '#5fa8ff' : '#fdfbf1';
        ctx.beginPath();
        ctx.ellipse(0, 0, p.r * p.depth, p.r * p.depth * 0.55, 0, 0, 6.2832);
        ctx.fill();
        ctx.restore();
      } else {
        p.y -= p.vy * dt;
        if (p.y < -0.05) { parts[i] = mote(false); continue; }
        const x = (p.x + Math.sin(p.phase * p.sway) * 0.012) * w + ox;
        const y = p.y * h + oy;
        const a = (0.35 + 0.65 * Math.abs(Math.sin(p.phase * 1.3))) * p.depth;
        const r = p.r * p.depth * 3.2;
        const g = ctx.createRadialGradient(x, y, 0, x, y, r);
        g.addColorStop(0, `hsla(${p.hue}, 100%, 92%, ${a})`);
        g.addColorStop(0.3, `hsla(${p.hue}, 100%, 70%, ${a * 0.45})`);
        g.addColorStop(1, `hsla(${p.hue}, 100%, 60%, 0)`);
        ctx.globalAlpha = 1;
        ctx.fillStyle = g;
        ctx.fillRect(x - r, y - r, r * 2, r * 2);
      }
    }
    requestAnimationFrame(frame);
  }

  let onScreen = true;
  function sync() {
    const should = onScreen && !document.hidden;
    if (should && !running) {
      running = true;
      last = performance.now();
      requestAnimationFrame(frame);
    } else if (!should) {
      running = false;
    }
  }
  new ResizeObserver(resize).observe(canvas);
  new IntersectionObserver(([entry]) => { onScreen = entry.isIntersecting; sync(); }).observe(hero);
  document.addEventListener('visibilitychange', sync);
  resize();
  sync();
}
