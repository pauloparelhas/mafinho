/* ═══════════════════════════════════════════════════
   base.js — Mafinho Shared System v2.1
   Fase 2 | 17/03/2026
   Importar em todos os jogos fase 2:
     <script src="base.js"><\/script>
   Cada jogo define inline: LANG, Nav overrides
   (startGame, restartGame, _applyLang), objetos de jogo.
   Chamar Nav.boot([...screenIds]) ao final do inline script.
   ═══════════════════════════════════════════════════ */

/* ── UTILITÁRIOS ── */
function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
function delay(ms) { return new Promise(r => setTimeout(r, ms)); }

/* ═══════════════════════════════════════════════════
   MF — tema, fonte, som, lock, confirmHome
═══════════════════════════════════════════════════ */
const MF = {
  _soundOn: true,
  _locked:  false,

  init() {
    this.applyTheme(localStorage.getItem('mf-theme') || 'light');
    this.applyFont(parseFloat(localStorage.getItem('mf-font') || '1'));
    this._soundOn = (localStorage.getItem('mf-sound') || 'on') === 'on';
    this._updateSoundBtn();
  },

  /* ── Tema ── */
  applyTheme(t) {
    document.documentElement.dataset.theme = t;
    const b = document.getElementById('btnTheme');
    if (b) b.textContent = t === 'dark' ? '☀️' : '🌙';
    localStorage.setItem('mf-theme', t);
  },
  toggleTheme() {
    this.applyTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
  },

  /* ── Fonte ── */
  applyFont(s) {
    document.documentElement.style.setProperty('--fs', s);
    localStorage.setItem('mf-font', s);
  },

  /* ── Som ── */
  toggleSound() {
    this._soundOn = !this._soundOn;
    localStorage.setItem('mf-sound', this._soundOn ? 'on' : 'off');
    this._updateSoundBtn();
    if (!this._soundOn) speechSynthesis && speechSynthesis.cancel();
  },
  _updateSoundBtn() {
    const b = document.getElementById('btnSound');
    if (b) b.textContent = this._soundOn ? '🔊' : '🔇';
  },

  /* ── Lock ── */
  handleLock() {
    if (!this._locked) {
      this._locked = true;
      document.body.dataset.locked = 'true';
      document.getElementById('btnLock').textContent = '🔓';
      document.documentElement.requestFullscreen?.().catch(() => {});
    } else {
      document.getElementById('lockOverlay').classList.add('show');
    }
  },
  _unlock() {
    this._locked = false;
    document.body.dataset.locked = 'false';
    document.getElementById('btnLock').textContent = '🔒';
    document.getElementById('lockOverlay').classList.remove('show');
    document.exitFullscreen?.().catch(() => {});
  },

  /* ── Lock helpers (chamados pelos overlays) ── */
  unlock()       { this._unlock(); },
  cancelUnlock() { document.getElementById('lockOverlay').classList.remove('show'); },

  /* ── Registro de jogos para menu de navegação ── */
  GAMES: [
    { id:'colors',  icon:'🎨', pt:'Cores',    en:'Colors',  href:'colors.html'  },
    { id:'numbers', icon:'🔢', pt:'Números',   en:'Numbers', href:'numbers.html' },
    { id:'animals', icon:'🐾', pt:'Animais',   en:'Animals', href:'animals.html' },
    { id:'shapes',  icon:'🔷', pt:'Formas',    en:'Shapes',  href:'shapes.html'  },
  ],
  currentGameId: null,

  /* ── Menu de navegação cross-game ── */
  confirmHome(e) {
    e && e.preventDefault();
    const overlay = document.getElementById('homeOverlay');
    const lang = localStorage.getItem('mf-lang') || 'pt';
    const games = this.GAMES;
    const curIdx = games.findIndex(g => g.id === this.currentGameId);

    let html = '<div class="mf-modal game-menu-modal">';
    html += '<div class="mf-modal-icon">🎮</div>';
    html += '<div class="mf-modal-msg">' + (lang === 'en' ? 'Games' : 'Jogos') + '</div>';

    /* Grid de jogos */
    html += '<div class="game-menu-grid">';
    games.forEach((g, i) => {
      const isCurrent = i === curIdx;
      const cls = 'game-menu-item' + (isCurrent ? ' current' : '');
      const name = lang === 'en' ? g.en : g.pt;
      if (isCurrent) {
        html += '<div class="' + cls + '"><span class="gm-icon">' + g.icon + '</span><span class="gm-name">' + name + '</span></div>';
      } else {
        html += '<a href="' + g.href + '" class="' + cls + '"><span class="gm-icon">' + g.icon + '</span><span class="gm-name">' + name + '</span></a>';
      }
    });
    html += '</div>';

    /* Prev / Next dentro do mesmo grupo */
    if (curIdx >= 0) {
      html += '<div class="game-menu-nav">';
      if (curIdx > 0) {
        const prev = games[curIdx - 1];
        const pName = lang === 'en' ? prev.en : prev.pt;
        html += '<a href="' + prev.href + '" class="game-menu-btn gm-prev">◀ ' + pName + '</a>';
      } else {
        html += '<span class="game-menu-btn gm-disabled"></span>';
      }
      if (curIdx < games.length - 1) {
        const next = games[curIdx + 1];
        const nName = lang === 'en' ? next.en : next.pt;
        html += '<a href="' + next.href + '" class="game-menu-btn gm-next">' + nName + ' ▶</a>';
      } else {
        html += '<span class="game-menu-btn gm-disabled"></span>';
      }
      html += '</div>';
    }

    /* Botões: Início + Ficar */
    html += '<div class="mf-modal-btns">';
    html += '<button class="mf-btn-yes" onclick="window.location.href=\'index.html\'">🏠 ' + (lang === 'en' ? 'Home' : 'Início') + '</button>';
    html += '<button class="mf-btn-no" onclick="document.getElementById(\'homeOverlay\').classList.remove(\'show\')">❌ ' + (lang === 'en' ? 'Stay' : 'Ficar') + '</button>';
    html += '</div></div>';

    overlay.innerHTML = html;
    overlay.classList.add('show');
  },

  /* Compat — chamado por overlays antigos */
  goHome()     { window.location.href = 'index.html'; },
  cancelHome() { document.getElementById('homeOverlay').classList.remove('show'); }
};

/* ═══════════════════════════════════════════════════
   TTS — Web Speech API
   speak(): fala + atualiza lastText + pulse no btnSpeak
   speakAndWait(): retorna Promise que resolve ao terminar
   replay(): repete lastText
   activate(): desbloqueia TTS no primeiro toque
═══════════════════════════════════════════════════ */
const TTS = {
  supported: !!window.speechSynthesis,
  unlocked:  false,
  langCode:  'pt-BR',
  lastText:  '',

  init() {
    if (!this.supported) {
      document.getElementById('soundBanner').classList.add('hidden');
      return;
    }
    speechSynthesis.getVoices();
    speechSynthesis.addEventListener('voiceschanged', () => speechSynthesis.getVoices());
    document.addEventListener('pointerdown', () => this.activate(), {once:true});
    /* Tenta ativar imediatamente — o user acabou de tocar no botão de idioma,
       então o browser geralmente permite speechSynthesis neste ponto */
    if (!this.unlocked) this.activate();
  },

  setLang(code) { this.langCode = code; },

  getBestVoice() {
    const voices = speechSynthesis.getVoices();
    const lang   = this.langCode;
    const tests  = [
      v => v.lang === lang && (v.name.includes('Natural') || v.name.includes('Online')),
      v => v.lang === lang,
      v => v.lang.startsWith(lang.split('-')[0]),
    ];
    for (const fn of tests) { const f = voices.find(fn); if (f) return f; }
    return null;
  },

  speak(text) {
    this.lastText = text;
    if (!this.supported || !this.unlocked || !MF._soundOn) return;
    speechSynthesis.cancel();
    const utt   = new SpeechSynthesisUtterance(text);
    utt.lang    = this.langCode;
    utt.rate    = 0.85;
    const voice = this.getBestVoice();
    if (voice) utt.voice = voice;
    this._pulse(true);
    utt.onend   = () => this._pulse(false);
    utt.onerror = () => this._pulse(false);
    speechSynthesis.speak(utt);
  },

  speakAndWait(text) {
    return new Promise(resolve => {
      this.lastText = text;
      if (!this.supported || !this.unlocked || !MF._soundOn) {
        setTimeout(resolve, Math.max(400, text.length * 80));
        return;
      }
      const utt   = new SpeechSynthesisUtterance(text);
      utt.lang    = this.langCode;
      utt.rate    = 0.85;
      const voice = this.getBestVoice();
      if (voice) utt.voice = voice;
      this._pulse(true);
      this.lastText = text;
      let done = false;
      const finish = () => { if (!done) { done = true; this._pulse(false); resolve(); } };
      utt.onend   = finish;
      utt.onerror = finish;
      setTimeout(finish, 4000);
      speechSynthesis.speak(utt);
    });
  },

  /* Fala com empolgação (mais lento, pitch alto) — para destaque */
  speakExcitedAndWait(text) {
    return new Promise(resolve => {
      this.lastText = text;
      if (!this.supported || !this.unlocked || !MF._soundOn) {
        setTimeout(resolve, Math.max(400, text.length * 100));
        return;
      }
      speechSynthesis.cancel();
      const utt   = new SpeechSynthesisUtterance(text);
      utt.lang    = this.langCode;
      utt.rate    = 0.80;
      utt.pitch   = 1.12;
      utt.volume  = 1.0;
      const voice = this.getBestVoice();
      if (voice) utt.voice = voice;
      this._pulse(true);
      this.lastText = text;
      let done = false;
      const finish = () => { if (!done) { done = true; this._pulse(false); resolve(); } };
      utt.onend   = finish;
      utt.onerror = finish;
      setTimeout(finish, 4000);
      speechSynthesis.speak(utt);
    });
  },

  activate() {
    if (this.unlocked) { this.replay(); return; }
    if (!this.supported) return;
    const s = new SpeechSynthesisUtterance(' ');
    s.volume = 0.01;
    s.onend  = () => {
      this.unlocked = true;
      document.getElementById('soundBanner').classList.add('hidden');
      this.replay();
    };
    speechSynthesis.speak(s);
  },

  replay() { if (this.lastText) this.speak(this.lastText); },

  _pulse(on) {
    const el = document.getElementById('btnSpeak');
    if (!el) return;
    if (on) el.classList.add('speaking'); else el.classList.remove('speaking');
  }
};

/* ═══════════════════════════════════════════════════
   SFX — Web Audio
   playCorrect(): Dó-Mi-Sol ascendente (festivo)
   playWrong():   dois bwoops descendentes (engraçado)
═══════════════════════════════════════════════════ */
const SFX = {
  _ctx: null,
  _ac() {
    if (!this._ctx) this._ctx = new (window.AudioContext || window.webkitAudioContext)();
    return this._ctx;
  },

  playCorrect() {
    if (!MF._soundOn) return;
    try {
      const ctx = this._ac(), t = ctx.currentTime;
      [[523, t], [659, t + 0.13], [784, t + 0.26]].forEach(([freq, t0]) => {
        const o = ctx.createOscillator(), g = ctx.createGain();
        o.connect(g); g.connect(ctx.destination);
        o.type = 'sine';
        o.frequency.value = freq;
        g.gain.setValueAtTime(0.28, t0);
        g.gain.exponentialRampToValueAtTime(0.001, t0 + 0.28);
        o.start(t0); o.stop(t0 + 0.28);
      });
    } catch(e) {}
  },

  /* Sons discretos variados — sinalizam acerto sem superestimulação */
  _chimeIdx: 0,
  _chimes: [
    /* 1: sininho ascendente A5→D6 */
    [[880, 0, 0.18], [1175, 0.09, 0.22]],
    /* 2: ding suave Dó6 */
    [[1047, 0, 0.30]],
    /* 3: dois toques piano Sol5→Dó6 */
    [[784, 0, 0.16], [1047, 0.12, 0.20]],
    /* 4: toque agudo Mi6 */
    [[1319, 0, 0.25]],
    /* 5: harpa Fá5→Lá5 */
    [[698, 0, 0.14], [880, 0.08, 0.22]],
  ],
  playChime() {
    if (!MF._soundOn) return;
    try {
      const ctx = this._ac(), t = ctx.currentTime;
      const notes = this._chimes[this._chimeIdx % this._chimes.length];
      this._chimeIdx++;
      notes.forEach(([freq, offset, dur]) => {
        const o = ctx.createOscillator(), g = ctx.createGain();
        o.connect(g); g.connect(ctx.destination);
        o.type = 'sine';
        o.frequency.value = freq;
        g.gain.setValueAtTime(0.16, t + offset);
        g.gain.exponentialRampToValueAtTime(0.001, t + offset + dur);
        o.start(t + offset); o.stop(t + offset + dur);
      });
    } catch(e) {}
  },

  playWrong() {
    if (!MF._soundOn) return;
    try {
      const ctx = this._ac(), t = ctx.currentTime;
      [[420, 95, t,      t + 0.38],
       [310, 75, t + 0.50, t + 0.85]].forEach(([f0, f1, t0, t1]) => {
        const o = ctx.createOscillator(), g = ctx.createGain();
        o.connect(g); g.connect(ctx.destination);
        o.type = 'sawtooth';
        o.frequency.setValueAtTime(f0, t0);
        o.frequency.exponentialRampToValueAtTime(f1, t1);
        g.gain.setValueAtTime(0.28, t0);
        g.gain.exponentialRampToValueAtTime(0.001, t1);
        o.start(t0); o.stop(t1);
      });
    } catch(e) {}
  }
};

/* ═══════════════════════════════════════════════════
   Nav — gerenciador de telas (base)
   Cada jogo SOBRESCREVE:
     Nav.startGame = function(lang) { ... };
     Nav.restartGame = function() { ... };
     Nav._applyLang = function(lang) { ... };
     Nav._onLeave = function() { ... }; // opcional
═══════════════════════════════════════════════════ */
const Nav = {
  currentGame: null,
  _screens:    [],
  _onLeave:    null,

  /* Registra telas e exibe o hub — chamar ao final do inline script */
  boot(screens) {
    this._screens = screens;
    MF.init();
    screens.forEach(id => {
      const el = document.getElementById(id);
      if (el) el.style.display = 'none';
    });
    document.getElementById('sHub').style.display = 'flex';
  },

  _show(id) {
    this._screens.forEach(s => {
      const el = document.getElementById(s);
      if (!el) return;
      el.style.display       = (s === id) ? 'flex' : 'none';
      el.style.flexDirection = 'column';
    });
    if (id === 'sCelebrate') {
      document.getElementById('sCelebrate').classList.add('show');
    }
  },

  goLang(game) {
    this.currentGame = game;
    this._show('sLang');
    document.getElementById('navLangBadge').style.display = 'none';
  },

  /* Stubs — sobrescritos por cada jogo inline */
  startGame(lang) {},
  restartGame() {},
  _applyLang(lang) {},

  backToHub() {
    if (this._onLeave) this._onLeave();
    speechSynthesis && speechSynthesis.cancel();
    document.body.style.touchAction = '';
    document.body.style.overflow    = '';
    document.getElementById('sCelebrate').classList.remove('show');
    document.getElementById('navLangBadge').style.display = 'none';
    this._show('sHub');
    document.documentElement.dataset.country = 'br';
    this._setCorners('⭐');
  },

  backToLang() {
    if (this._onLeave) this._onLeave();
    speechSynthesis && speechSynthesis.cancel();
    document.body.style.touchAction = '';
    document.body.style.overflow    = '';
    document.getElementById('sCelebrate').classList.remove('show');
    this._show('sLang');
    document.getElementById('navLangBadge').style.display = 'none';
    document.documentElement.dataset.country = 'br';
    this._setCorners('⭐');
  },

  _setCorners(ch) {
    ['dc1','dc2','dc3','dc4'].forEach(id =>
      document.getElementById(id).textContent = ch
    );
  }
};
