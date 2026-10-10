/* Main theme: starts by itself where the browser allows it, otherwise on the first click, tap or key press. */
(() => {
  const button = document.querySelector('.sound');
  if (!button) return;

  const SRC = new URL('../assets/audio/main-theme.mp3', document.currentScript.src).href;
  const MUTED_KEY = 'cof-music-muted';
  const TIME_KEY = 'cof-music-time';
  const VOLUME = 0.4;
  const store = (area, key, value) => { try { area.setItem(key, value); } catch { /* private mode */ } };
  const read = (area, key) => { try { return area.getItem(key); } catch { return null; } };

  let muted = read(localStorage, MUTED_KEY) === '1';
  let fade = 0;
  const audio = new Audio();
  audio.loop = true;
  audio.volume = 0;
  audio.preload = muted ? 'none' : 'auto';
  audio.src = SRC;

  // carry on from where the previous page left off
  const resumeAt = Number(read(sessionStorage, TIME_KEY)) || 0;
  if (resumeAt > 0) audio.addEventListener('loadedmetadata', () => { audio.currentTime = resumeAt % audio.duration; }, { once: true });

  function setState(state) {
    button.dataset.state = state;
    button.setAttribute('aria-pressed', String(state === 'muted'));
    const label = { playing: 'Mute music', muted: 'Play music', waiting: 'Play music' }[state];
    button.setAttribute('aria-label', label);
    button.title = label;
  }

  function fadeTo(target, then) {
    cancelAnimationFrame(fade);
    const from = audio.volume;
    const t0 = performance.now();
    const step = (t) => {
      const k = Math.min(Math.max((t - t0) / 900, 0), 1);
      audio.volume = Math.min(Math.max(from + (target - from) * k, 0), 1);
      if (k < 1) fade = requestAnimationFrame(step);
      else then?.();
    };
    fade = requestAnimationFrame(step);
  }

  const gestures = ['pointerdown', 'keydown', 'touchend'];
  const onGesture = (e) => { if (!e.target.closest?.('.sound')) start(); };
  const listen = (on) => gestures.forEach((g) => (on ? addEventListener(g, onGesture, { passive: true }) : removeEventListener(g, onGesture)));

  async function start() {
    if (muted) return;
    try {
      await audio.play();
      listen(false);
      setState('playing');
      fadeTo(VOLUME);
    } catch {
      // the browser wants a click first
      setState('waiting');
      listen(true);
    }
  }

  button.addEventListener('click', () => {
    if (button.dataset.state === 'waiting') { start(); return; }
    muted = !muted;
    store(localStorage, MUTED_KEY, muted ? '1' : '0');
    if (muted) {
      listen(false);
      setState('muted');
      fadeTo(0, () => audio.pause());
    } else {
      start();
    }
  });

  addEventListener('pagehide', () => store(sessionStorage, TIME_KEY, String(audio.currentTime)));
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) audio.pause();
    else if (!muted && button.dataset.state === 'playing') audio.play().catch(() => {});
  });

  setState(muted ? 'muted' : 'waiting');
  start();
})();
