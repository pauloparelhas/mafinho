/* ═══════════════════════════════════════════════════
   base.js — Mafinho Shared System v2.0
   Fase 2 | 16/03/2026
   Importar em todos os jogos fase 2:
     <script src="base.js"></script>
   Chamar MF.init() ao final do script de cada jogo.
   ═══════════════════════════════════════════════════ */

const MF = {

  /* ── INIT ── */
  init() {
    this.applyTheme(localStorage.getItem('mf-theme') || 'light');
    this.applyFont(parseFloat(localStorage.getItem('mf-font') || '1'));
    this.applyLang(localStorage.getItem('mf-lang') || 'pt');
    this._soundOn = (localStorage.getItem('mf-sound') || 'on') === 'on';
    this._updateSoundBtn();
    this._locked = false;
  },

  /* ── TEMA ── */
  applyTheme(t) {
    document.documentElement.dataset.theme = t;
    const b = document.getElementById('themeBtn');
    if (b) b.textContent = t === 'dark' ? '☀️' : '🌙';
    localStorage.setItem('mf-theme', t);
  },
  toggleTheme() {
    this.applyTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
  },

  /* ── FONTE ── */
  applyFont(s) {
    document.documentElement.style.setProperty('--fs', s);
    localStorage.setItem('mf-font', s);
  },
  adjustFont(d) {
    const s = parseFloat(localStorage.getItem('mf-font') || '1');
    this.applyFont(Math.max(0.7, Math.min(1.5, +(s + d * 0.1).toFixed(2))));
  },

  /* ── IDIOMA ── */
  applyLang(lang) {
    document.documentElement.dataset.lang = lang;
    const b = document.getElementById('btnLang');
    if (b) b.textContent = lang === 'en' ? '🇨🇦' : '🇧🇷';
    document.querySelectorAll('[data-pt]').forEach(el => {
      el.textContent = lang === 'en' ? (el.dataset.en || el.dataset.pt) : el.dataset.pt;
    });
    localStorage.setItem('mf-lang', lang);
  },
  toggleLang() {
    this.applyLang(document.documentElement.dataset.lang === 'en' ? 'pt' : 'en');
  },
  getLang() {
    return document.documentElement.dataset.lang || 'pt';
  },

  /* ── SOM ── */
  _soundOn: true,
  toggleSound() {
    this._soundOn = !this._soundOn;
    localStorage.setItem('mf-sound', this._soundOn ? 'on' : 'off');
    this._updateSoundBtn();
  },
  _updateSoundBtn() {
    const b = document.getElementById('soundBtn');
    if (b) b.textContent = this._soundOn ? '🔊' : '🔇';
  },

  /* ── TTS ── */
  speak(text, lang) {
    if (!this._soundOn) return;
    if (!window.speechSynthesis) return;
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang  = lang === 'en' ? 'en-US' : 'pt-BR';
    u.rate  = 0.85;
    u.pitch = 1.1;
    speechSynthesis.speak(u);
  },

  /* ── LOCK ── */
  _locked: false,
  handleLock() {
    if (!this._locked) {
      this._locked = true;
      const b = document.getElementById('lockBtn');
      if (b) b.textContent = '🔓';
      document.body.dataset.locked = 'true';
      document.documentElement.requestFullscreen?.().catch(() => {});
    } else {
      this._showUnlockOverlay();
    }
  },
  _showUnlockOverlay() {
    let ov = document.getElementById('mf-lock-overlay');
    if (!ov) {
      ov = document.createElement('div');
      ov.id = 'mf-lock-overlay';
      ov.innerHTML = `
        <div class="lock-modal">
          <div class="lock-emoji">🔒</div>
          <div class="lock-msg">Desbloquear tela?</div>
          <div class="lock-btns">
            <button onclick="MF._unlock()">✅ Sim</button>
            <button onclick="document.getElementById('mf-lock-overlay').style.display='none'">❌ Não</button>
          </div>
        </div>`;
      document.body.appendChild(ov);
    }
    ov.style.display = 'flex';
  },
  _unlock() {
    this._locked = false;
    document.body.dataset.locked = 'false';
    const b = document.getElementById('lockBtn');
    if (b) b.textContent = '🔒';
    const ov = document.getElementById('mf-lock-overlay');
    if (ov) ov.style.display = 'none';
    document.exitFullscreen?.().catch(() => {});
  },

  /* ── NAVEGAÇÃO ── */
  goToIndex() {
    window.location.href = 'index.html';
  }
};

/* ── FUNÇÕES GLOBAIS (chamadas pelo HTML via onclick) ── */

function goToIndex() { MF.goToIndex(); }

function confirmHome() {
  let ov = document.getElementById('mf-home-overlay');
  if (!ov) {
    ov = document.createElement('div');
    ov.id = 'mf-home-overlay';
    ov.innerHTML = `
      <div class="lock-modal">
        <div class="lock-emoji">🏠</div>
        <div class="lock-msg">Sair do jogo?</div>
        <div class="lock-btns">
          <button onclick="MF.goToIndex()">✅ Sim</button>
          <button onclick="document.getElementById('mf-home-overlay').style.display='none'">❌ Ficar</button>
        </div>
      </div>`;
    document.body.appendChild(ov);
  }
  ov.style.display = 'flex';
}

/* prevPhase / nextPhase — sobrescrever em cada arquivo de jogo */
function prevPhase() {}
function nextPhase() {}
