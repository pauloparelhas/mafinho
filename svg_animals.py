#!/usr/bin/env python3
"""
svg_animals.py — Mafinho Explora
Gera SVGs elaborados de animais estilo kawaii e renderiza para PNG via PyMuPDF.

Uso:
  python svg_animals.py              # gera todos os PNGs em img/animals/
  python svg_animals.py dog          # gera apenas o cachorro
  python svg_animals.py --inline     # imprime SVGs para uso inline no HTML

Cada SVG usa:
  - Curvas bezier para contornos organicos
  - Multiplas camadas (corpo, cabeca, orelhas, patas, rabo)
  - Olhos elaborados (esclera, iris, pupila, brilho)
  - Bochechas rosadas semi-transparentes
  - Proporcoes kawaii (cabeca grande, corpo menor)
  - Cores com contraste (nenhum animal todo branco)
  - SEM gradientes (PyMuPDF nao suporta bem) — profundidade via camadas
"""

import sys
from pathlib import Path

OUT_DIR = Path(__file__).parent / "img" / "animals"
SIZE = 512

ANIMALS = {}

# ── 0: Cachorro / Dog ──
ANIMALS["dog"] = """<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Rabo -->
  <path d="M138,148 C156,138 166,122 158,112" stroke="#C49A5C" stroke-width="8" stroke-linecap="round" fill="none"/>

  <!-- Corpo -->
  <ellipse cx="100" cy="152" rx="38" ry="28" fill="#D4A56A" stroke="#8B6508" stroke-width="2.5"/>
  <!-- Barriga -->
  <ellipse cx="100" cy="156" rx="22" ry="16" fill="#F5E6C8" opacity="0.7"/>

  <!-- Patas -->
  <ellipse cx="78" cy="180" rx="12" ry="14" fill="#C49A5C" stroke="#8B6508" stroke-width="2"/>
  <ellipse cx="122" cy="180" rx="12" ry="14" fill="#C49A5C" stroke="#8B6508" stroke-width="2"/>
  <ellipse cx="78" cy="192" rx="13" ry="6" fill="#F0DCC0" stroke="#8B6508" stroke-width="1.5"/>
  <ellipse cx="122" cy="192" rx="13" ry="6" fill="#F0DCC0" stroke="#8B6508" stroke-width="1.5"/>

  <!-- Cabeca -->
  <circle cx="100" cy="82" r="55" fill="#D4A56A" stroke="#8B6508" stroke-width="2.5"/>
  <!-- Highlight testa -->
  <ellipse cx="90" cy="60" rx="22" ry="14" fill="#E8C48A" opacity="0.5"/>

  <!-- Orelha esquerda -->
  <path d="M50,62 C36,40 28,68 38,95 C42,106 56,100 54,88" fill="#A07528" stroke="#8B6508" stroke-width="2"/>
  <path d="M48,66 C40,50 34,72 40,90 C44,98 52,94 51,85" fill="#D4A0B0" opacity="0.3"/>
  <!-- Orelha direita -->
  <path d="M150,62 C164,40 172,68 162,95 C158,106 144,100 146,88" fill="#A07528" stroke="#8B6508" stroke-width="2"/>
  <path d="M152,66 C160,50 166,72 160,90 C156,98 148,94 149,85" fill="#D4A0B0" opacity="0.3"/>

  <!-- Focinho -->
  <ellipse cx="100" cy="98" rx="24" ry="17" fill="#F5E6C8" stroke="#8B6508" stroke-width="1.5"/>

  <!-- Olho esquerdo -->
  <ellipse cx="78" cy="76" rx="14" ry="15" fill="white" stroke="#8B6508" stroke-width="1.5"/>
  <circle cx="80" cy="78" r="9" fill="#5D3516"/>
  <circle cx="81" cy="79" r="5.5" fill="#1A0800"/>
  <circle cx="84" cy="73" r="3.5" fill="white"/>
  <circle cx="78" cy="80" r="1.5" fill="white" opacity="0.5"/>
  <!-- Olho direito -->
  <ellipse cx="122" cy="76" rx="14" ry="15" fill="white" stroke="#8B6508" stroke-width="1.5"/>
  <circle cx="120" cy="78" r="9" fill="#5D3516"/>
  <circle cx="119" cy="79" r="5.5" fill="#1A0800"/>
  <circle cx="116" cy="73" r="3.5" fill="white"/>
  <circle cx="122" cy="80" r="1.5" fill="white" opacity="0.5"/>

  <!-- Sobrancelhas -->
  <path d="M65,64 C70,60 78,60 84,63" stroke="#8B6508" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="M116,63 C122,60 130,60 135,64" stroke="#8B6508" stroke-width="2" fill="none" stroke-linecap="round"/>

  <!-- Nariz -->
  <ellipse cx="100" cy="92" rx="8" ry="6" fill="#2D1B0E"/>
  <ellipse cx="98" cy="90" rx="2.5" ry="1.5" fill="white" opacity="0.3"/>

  <!-- Boca -->
  <path d="M90,100 Q96,108 100,100" stroke="#8B6508" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="M100,100 Q104,108 110,100" stroke="#8B6508" stroke-width="2" fill="none" stroke-linecap="round"/>
  <!-- Lingua -->
  <ellipse cx="100" cy="106" rx="5" ry="6" fill="#FF7B8F"/>
  <line x1="100" y1="103" x2="100" y2="110" stroke="#E8607A" stroke-width="0.8"/>

  <!-- Bochechas -->
  <circle cx="58" cy="92" r="10" fill="#FFB6C1" opacity="0.4"/>
  <circle cx="142" cy="92" r="10" fill="#FFB6C1" opacity="0.4"/>
</svg>"""

# ── 1: Gato / Cat ──
ANIMALS["cat"] = """<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Rabo -->
  <path d="M140,155 C165,150 175,130 168,115 C165,108 158,112 162,120 C166,132 155,148 140,150"
        fill="#8888A0" stroke="#5A5A72" stroke-width="2"/>

  <!-- Corpo -->
  <ellipse cx="100" cy="152" rx="36" ry="28" fill="#9898B0" stroke="#5A5A72" stroke-width="2.5"/>
  <ellipse cx="100" cy="156" rx="20" ry="16" fill="#D0D0E0" opacity="0.5"/>

  <!-- Patas -->
  <ellipse cx="76" cy="178" rx="12" ry="14" fill="#8888A0" stroke="#5A5A72" stroke-width="2"/>
  <ellipse cx="124" cy="178" rx="12" ry="14" fill="#8888A0" stroke="#5A5A72" stroke-width="2"/>
  <ellipse cx="76" cy="190" rx="13" ry="5.5" fill="#D0D0E0" stroke="#5A5A72" stroke-width="1.5"/>
  <ellipse cx="124" cy="190" rx="13" ry="5.5" fill="#D0D0E0" stroke="#5A5A72" stroke-width="1.5"/>

  <!-- Cabeca -->
  <circle cx="100" cy="80" r="52" fill="#9898B0" stroke="#5A5A72" stroke-width="2.5"/>
  <ellipse cx="90" cy="58" rx="20" ry="12" fill="#A8A8C0" opacity="0.5"/>

  <!-- Orelha esquerda -->
  <path d="M58,52 L48,14 L80,42 Z" fill="#8888A0" stroke="#5A5A72" stroke-width="2" stroke-linejoin="round"/>
  <path d="M60,50 L52,22 L76,44 Z" fill="#F0A0B8" opacity="0.5"/>
  <!-- Orelha direita -->
  <path d="M142,52 L152,14 L120,42 Z" fill="#8888A0" stroke="#5A5A72" stroke-width="2" stroke-linejoin="round"/>
  <path d="M140,50 L148,22 L124,44 Z" fill="#F0A0B8" opacity="0.5"/>

  <!-- Focinho -->
  <ellipse cx="100" cy="95" rx="18" ry="12" fill="#D0D0E0" stroke="#5A5A72" stroke-width="1.2"/>

  <!-- Olho esquerdo -->
  <ellipse cx="78" cy="76" rx="13" ry="14" fill="white" stroke="#5A5A72" stroke-width="1.5"/>
  <ellipse cx="79" cy="78" rx="6" ry="8" fill="#4CAF50"/>
  <ellipse cx="79" cy="78" rx="3" ry="7" fill="#1A0A00"/>
  <circle cx="82" cy="73" r="3" fill="white"/>
  <!-- Olho direito -->
  <ellipse cx="122" cy="76" rx="13" ry="14" fill="white" stroke="#5A5A72" stroke-width="1.5"/>
  <ellipse cx="121" cy="78" rx="6" ry="8" fill="#4CAF50"/>
  <ellipse cx="121" cy="78" rx="3" ry="7" fill="#1A0A00"/>
  <circle cx="118" cy="73" r="3" fill="white"/>

  <!-- Nariz -->
  <path d="M96,90 L100,94 L104,90 Z" fill="#F08090"/>
  <!-- Boca -->
  <path d="M92,97 C96,102 100,102 100,97" stroke="#5A5A72" stroke-width="1.5" fill="none"/>
  <path d="M100,97 C100,102 104,102 108,97" stroke="#5A5A72" stroke-width="1.5" fill="none"/>

  <!-- Bigodes -->
  <line x1="62" y1="82" x2="40" y2="78" stroke="#5A5A72" stroke-width="1.2"/>
  <line x1="62" y1="88" x2="38" y2="88" stroke="#5A5A72" stroke-width="1.2"/>
  <line x1="62" y1="94" x2="40" y2="98" stroke="#5A5A72" stroke-width="1.2"/>
  <line x1="138" y1="82" x2="160" y2="78" stroke="#5A5A72" stroke-width="1.2"/>
  <line x1="138" y1="88" x2="162" y2="88" stroke="#5A5A72" stroke-width="1.2"/>
  <line x1="138" y1="94" x2="160" y2="98" stroke="#5A5A72" stroke-width="1.2"/>

  <!-- Bochechas -->
  <circle cx="58" cy="92" r="9" fill="#FFB6C1" opacity="0.35"/>
  <circle cx="142" cy="92" r="9" fill="#FFB6C1" opacity="0.35"/>
</svg>"""

# ── 2: Vaca / Cow (creme com manchas marrons, NAO branca) ──
ANIMALS["cow"] = """<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Corpo creme -->
  <ellipse cx="100" cy="148" rx="48" ry="32" fill="#F5E8D0" stroke="#8B7355" stroke-width="2.5"/>
  <!-- Manchas -->
  <ellipse cx="80" cy="140" rx="14" ry="10" fill="#6B4226" opacity="0.7" transform="rotate(-15 80 140)"/>
  <ellipse cx="120" cy="152" rx="12" ry="9" fill="#6B4226" opacity="0.7" transform="rotate(20 120 152)"/>

  <!-- Pernas -->
  <rect x="68" y="170" width="16" height="22" rx="5" fill="#F0DDB8" stroke="#8B7355" stroke-width="2"/>
  <rect x="68" y="185" width="16" height="7" rx="2" fill="#4A3520"/>
  <rect x="116" y="170" width="16" height="22" rx="5" fill="#F0DDB8" stroke="#8B7355" stroke-width="2"/>
  <rect x="116" y="185" width="16" height="7" rx="2" fill="#4A3520"/>

  <!-- Cabeca -->
  <circle cx="100" cy="78" r="50" fill="#F5E8D0" stroke="#8B7355" stroke-width="2.5"/>
  <!-- Manchas na cabeca -->
  <ellipse cx="75" cy="60" rx="16" ry="12" fill="#6B4226" opacity="0.7" transform="rotate(-10 75 60)"/>
  <ellipse cx="130" cy="68" rx="10" ry="8" fill="#6B4226" opacity="0.6"/>

  <!-- Orelhas -->
  <ellipse cx="52" cy="62" rx="18" ry="10" fill="#F0DDB8" stroke="#8B7355" stroke-width="2" transform="rotate(-25 52 62)"/>
  <ellipse cx="52" cy="62" rx="12" ry="6" fill="#F0A8B8" transform="rotate(-25 52 62)"/>
  <ellipse cx="148" cy="62" rx="18" ry="10" fill="#F0DDB8" stroke="#8B7355" stroke-width="2" transform="rotate(25 148 62)"/>
  <ellipse cx="148" cy="62" rx="12" ry="6" fill="#F0A8B8" transform="rotate(25 148 62)"/>

  <!-- Chifres -->
  <path d="M78,34 C74,18 84,12 88,26" fill="#F5E6A0" stroke="#C8B060" stroke-width="1.5"/>
  <path d="M122,34 C126,18 116,12 112,26" fill="#F5E6A0" stroke="#C8B060" stroke-width="1.5"/>

  <!-- Olhos -->
  <ellipse cx="82" cy="72" rx="10" ry="11" fill="white" stroke="#8B7355" stroke-width="1.5"/>
  <circle cx="83" cy="74" r="6" fill="#3E2723"/>
  <circle cx="84" cy="75" r="3.5" fill="#1A0800"/>
  <circle cx="86" cy="70" r="3" fill="white"/>
  <ellipse cx="118" cy="72" rx="10" ry="11" fill="white" stroke="#8B7355" stroke-width="1.5"/>
  <circle cx="117" cy="74" r="6" fill="#3E2723"/>
  <circle cx="116" cy="75" r="3.5" fill="#1A0800"/>
  <circle cx="114" cy="70" r="3" fill="white"/>

  <!-- Focinho rosa -->
  <ellipse cx="100" cy="98" rx="22" ry="15" fill="#F0A8B8" stroke="#C0808F" stroke-width="2"/>
  <circle cx="92" cy="96" r="3.5" fill="#C06070"/>
  <circle cx="108" cy="96" r="3.5" fill="#C06070"/>
  <path d="M92,105 C96,110 104,110 108,105" stroke="#C06070" stroke-width="2" fill="none" stroke-linecap="round"/>

  <!-- Bochechas -->
  <circle cx="64" cy="90" r="8" fill="#FFB6C1" opacity="0.35"/>
  <circle cx="136" cy="90" r="8" fill="#FFB6C1" opacity="0.35"/>
</svg>"""

# ── 3: Cavalo / Horse ──
ANIMALS["horse"] = """<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Rabo (crina) -->
  <path d="M148,140 C168,130 175,110 165,95" stroke="#3E2723" stroke-width="6" stroke-linecap="round" fill="none"/>
  <path d="M150,142 C172,128 178,105 170,90" stroke="#3E2723" stroke-width="4" stroke-linecap="round" fill="none"/>

  <!-- Corpo -->
  <ellipse cx="100" cy="148" rx="45" ry="30" fill="#A0622A" stroke="#5D3A1A" stroke-width="2.5"/>

  <!-- Pernas -->
  <rect x="65" y="168" width="15" height="24" rx="4" fill="#8B5220" stroke="#5D3A1A" stroke-width="2"/>
  <rect x="65" y="186" width="15" height="6" rx="2" fill="#3E2723"/>
  <rect x="120" y="168" width="15" height="24" rx="4" fill="#8B5220" stroke="#5D3A1A" stroke-width="2"/>
  <rect x="120" y="186" width="15" height="6" rx="2" fill="#3E2723"/>

  <!-- Cabeca -->
  <ellipse cx="100" cy="78" rx="46" ry="52" fill="#A0622A" stroke="#5D3A1A" stroke-width="2.5"/>
  <ellipse cx="90" cy="56" rx="18" ry="12" fill="#B87A3A" opacity="0.5"/>

  <!-- Crina -->
  <path d="M82,30 C78,18 88,12 92,24" stroke="#3E2723" stroke-width="5" stroke-linecap="round" fill="none"/>
  <path d="M92,28 C90,14 100,10 102,22" stroke="#3E2723" stroke-width="5" stroke-linecap="round" fill="none"/>
  <path d="M102,30 C102,16 112,14 112,26" stroke="#3E2723" stroke-width="5" stroke-linecap="round" fill="none"/>

  <!-- Orelhas -->
  <path d="M70,42 L62,18 L82,36 Z" fill="#A0622A" stroke="#5D3A1A" stroke-width="2" stroke-linejoin="round"/>
  <path d="M72,40 L66,22 L80,36 Z" fill="#D4A0B0" opacity="0.35"/>
  <path d="M130,42 L138,18 L118,36 Z" fill="#A0622A" stroke="#5D3A1A" stroke-width="2" stroke-linejoin="round"/>
  <path d="M128,40 L134,22 L120,36 Z" fill="#D4A0B0" opacity="0.35"/>

  <!-- Focinho -->
  <ellipse cx="100" cy="102" rx="20" ry="16" fill="#C8905A" stroke="#5D3A1A" stroke-width="1.5"/>

  <!-- Olhos -->
  <ellipse cx="80" cy="72" rx="11" ry="12" fill="white" stroke="#5D3A1A" stroke-width="1.5"/>
  <circle cx="81" cy="74" r="7" fill="#3E2723"/>
  <circle cx="82" cy="75" r="4" fill="#1A0800"/>
  <circle cx="84" cy="70" r="3" fill="white"/>
  <ellipse cx="120" cy="72" rx="11" ry="12" fill="white" stroke="#5D3A1A" stroke-width="1.5"/>
  <circle cx="119" cy="74" r="7" fill="#3E2723"/>
  <circle cx="118" cy="75" r="4" fill="#1A0800"/>
  <circle cx="116" cy="70" r="3" fill="white"/>

  <!-- Narinas -->
  <circle cx="92" cy="100" r="3.5" fill="#5D3A1A"/>
  <circle cx="108" cy="100" r="3.5" fill="#5D3A1A"/>
  <!-- Boca -->
  <path d="M92,110 C96,114 104,114 108,110" stroke="#5D3A1A" stroke-width="1.8" fill="none" stroke-linecap="round"/>

  <!-- Bochechas -->
  <circle cx="62" cy="88" r="8" fill="#FFB6C1" opacity="0.35"/>
  <circle cx="138" cy="88" r="8" fill="#FFB6C1" opacity="0.35"/>
</svg>"""

# ── 4: Porco / Pig ──
ANIMALS["pig"] = """<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Rabinho enrolado -->
  <path d="M155,130 C168,125 172,115 165,110 C160,106 155,112 160,116 C165,120 162,128 155,130"
        stroke="#E0809A" stroke-width="3" fill="none" stroke-linecap="round"/>

  <!-- Corpo -->
  <ellipse cx="100" cy="145" rx="45" ry="35" fill="#FFB0C4" stroke="#C0607A" stroke-width="2.5"/>
  <ellipse cx="100" cy="150" rx="25" ry="18" fill="#FFD0DC" opacity="0.5"/>

  <!-- Patas -->
  <rect x="68" y="170" width="18" height="18" rx="6" fill="#F098B0" stroke="#C0607A" stroke-width="2"/>
  <rect x="68" y="182" width="18" height="6" rx="2" fill="#C0607A"/>
  <rect x="114" y="170" width="18" height="18" rx="6" fill="#F098B0" stroke="#C0607A" stroke-width="2"/>
  <rect x="114" y="182" width="18" height="6" rx="2" fill="#C0607A"/>

  <!-- Cabeca -->
  <circle cx="100" cy="80" r="52" fill="#FFB0C4" stroke="#C0607A" stroke-width="2.5"/>
  <ellipse cx="90" cy="58" rx="18" ry="10" fill="#FFC8D8" opacity="0.5"/>

  <!-- Orelhas -->
  <path d="M58,48 C42,28 52,15 68,32 L65,50 Z" fill="#F098B0" stroke="#C0607A" stroke-width="2"/>
  <path d="M60,46 C48,32 56,22 66,34 L64,48 Z" fill="#D87090" opacity="0.4"/>
  <path d="M142,48 C158,28 148,15 132,32 L135,50 Z" fill="#F098B0" stroke="#C0607A" stroke-width="2"/>
  <path d="M140,46 C152,32 144,22 134,34 L136,48 Z" fill="#D87090" opacity="0.4"/>

  <!-- Olhos -->
  <ellipse cx="80" cy="74" rx="11" ry="12" fill="white" stroke="#C0607A" stroke-width="1.5"/>
  <circle cx="81" cy="76" r="7" fill="#3E2723"/>
  <circle cx="82" cy="77" r="4" fill="#1A0800"/>
  <circle cx="84" cy="72" r="3" fill="white"/>
  <ellipse cx="120" cy="74" rx="11" ry="12" fill="white" stroke="#C0607A" stroke-width="1.5"/>
  <circle cx="119" cy="76" r="7" fill="#3E2723"/>
  <circle cx="118" cy="77" r="4" fill="#1A0800"/>
  <circle cx="116" cy="72" r="3" fill="white"/>

  <!-- Focinho -->
  <ellipse cx="100" cy="98" rx="22" ry="16" fill="#F098B0" stroke="#C0607A" stroke-width="2.5"/>
  <ellipse cx="91" cy="97" rx="5" ry="6" fill="#D06880"/>
  <ellipse cx="109" cy="97" rx="5" ry="6" fill="#D06880"/>

  <!-- Boca -->
  <path d="M90,112 C95,116 105,116 110,112" stroke="#C0607A" stroke-width="2" fill="none" stroke-linecap="round"/>

  <!-- Bochechas -->
  <circle cx="60" cy="92" r="9" fill="#FF8FA0" opacity="0.4"/>
  <circle cx="140" cy="92" r="9" fill="#FF8FA0" opacity="0.4"/>
</svg>"""

# ── 5: Galinha / Chicken (creme/amarelada, NAO branca) ──
ANIMALS["chicken"] = """<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Corpo -->
  <ellipse cx="100" cy="140" rx="42" ry="38" fill="#F5E0A8" stroke="#B8963C" stroke-width="2.5"/>

  <!-- Asa esquerda -->
  <path d="M60,125 C42,135 45,160 62,160 C70,160 68,145 60,125Z" fill="#E8D090" stroke="#B8963C" stroke-width="2"/>
  <!-- Asa direita -->
  <path d="M140,125 C158,135 155,160 138,160 C130,160 132,145 140,125Z" fill="#E8D090" stroke="#B8963C" stroke-width="2"/>

  <!-- Patas -->
  <path d="M82,175 L78,195 M82,175 L82,198 M82,175 L86,195" stroke="#E88020" stroke-width="3.5" stroke-linecap="round"/>
  <path d="M118,175 L114,195 M118,175 L118,198 M118,175 L122,195" stroke="#E88020" stroke-width="3.5" stroke-linecap="round"/>

  <!-- Cabeca -->
  <circle cx="100" cy="75" r="42" fill="#F5E0A8" stroke="#B8963C" stroke-width="2.5"/>
  <ellipse cx="92" cy="55" rx="16" ry="10" fill="#FFF0C0" opacity="0.5"/>

  <!-- Crista -->
  <path d="M82,38 C76,20 88,12 96,28 C98,14 108,14 108,28 C114,12 126,20 118,38" fill="#E03030" stroke="#B02020" stroke-width="2"/>

  <!-- Olhos -->
  <ellipse cx="82" cy="72" rx="10" ry="11" fill="white" stroke="#B8963C" stroke-width="1.5"/>
  <circle cx="83" cy="74" r="6" fill="#3E2723"/>
  <circle cx="84" cy="75" r="3.5" fill="#1A0800"/>
  <circle cx="86" cy="70" r="2.5" fill="white"/>
  <ellipse cx="118" cy="72" rx="10" ry="11" fill="white" stroke="#B8963C" stroke-width="1.5"/>
  <circle cx="117" cy="74" r="6" fill="#3E2723"/>
  <circle cx="116" cy="75" r="3.5" fill="#1A0800"/>
  <circle cx="114" cy="70" r="2.5" fill="white"/>

  <!-- Bico -->
  <path d="M100,84 L88,94 L100,98 L112,94 Z" fill="#F0A020" stroke="#D08018" stroke-width="1.5"/>

  <!-- Barbela -->
  <path d="M95,98 C92,108 98,114 100,108 C102,114 108,108 105,98" fill="#E03030" opacity="0.8"/>

  <!-- Bochechas -->
  <circle cx="66" cy="86" r="7" fill="#FFB6C1" opacity="0.35"/>
  <circle cx="134" cy="86" r="7" fill="#FFB6C1" opacity="0.35"/>
</svg>"""

# ── 6: Pato / Duck ──
ANIMALS["duck"] = """<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Corpo -->
  <ellipse cx="100" cy="148" rx="45" ry="32" fill="#F0C820" stroke="#C8A018" stroke-width="2.5"/>
  <ellipse cx="100" cy="155" rx="28" ry="18" fill="#FFF0A0" opacity="0.5"/>

  <!-- Asas -->
  <path d="M55,135 C38,145 42,168 60,168 C68,168 65,152 55,135Z" fill="#E0B818" stroke="#C8A018" stroke-width="2"/>
  <path d="M145,135 C162,145 158,168 140,168 C132,168 135,152 145,135Z" fill="#E0B818" stroke="#C8A018" stroke-width="2"/>

  <!-- Patas -->
  <path d="M80,178 C75,188 68,192 80,195 L88,190 Z" fill="#E87020" stroke="#C86018" stroke-width="1.5"/>
  <path d="M120,178 C125,188 132,192 120,195 L112,190 Z" fill="#E87020" stroke="#C86018" stroke-width="1.5"/>

  <!-- Cabeca -->
  <circle cx="100" cy="78" r="48" fill="#FFD830" stroke="#C8A018" stroke-width="2.5"/>
  <ellipse cx="90" cy="56" rx="18" ry="12" fill="#FFE860" opacity="0.5"/>

  <!-- Topete -->
  <path d="M95,32 C90,22 100,18 102,28" stroke="#E0B818" stroke-width="4" stroke-linecap="round" fill="none"/>
  <path d="M102,30 C104,20 112,22 108,32" stroke="#E0B818" stroke-width="4" stroke-linecap="round" fill="none"/>

  <!-- Olhos -->
  <ellipse cx="80" cy="72" rx="12" ry="13" fill="white" stroke="#C8A018" stroke-width="1.5"/>
  <circle cx="82" cy="74" r="7" fill="#3E2723"/>
  <circle cx="83" cy="75" r="4" fill="#1A0800"/>
  <circle cx="85" cy="70" r="3" fill="white"/>
  <ellipse cx="120" cy="72" rx="12" ry="13" fill="white" stroke="#C8A018" stroke-width="1.5"/>
  <circle cx="118" cy="74" r="7" fill="#3E2723"/>
  <circle cx="117" cy="75" r="4" fill="#1A0800"/>
  <circle cx="115" cy="70" r="3" fill="white"/>

  <!-- Bico -->
  <path d="M100,88 C80,88 72,100 100,108 C128,100 120,88 100,88Z" fill="#E87020" stroke="#C86018" stroke-width="2"/>

  <!-- Bochechas -->
  <circle cx="60" cy="88" r="8" fill="#FFB6C1" opacity="0.35"/>
  <circle cx="140" cy="88" r="8" fill="#FFB6C1" opacity="0.35"/>
</svg>"""

# ── 7: Leao / Lion ──
ANIMALS["lion"] = """<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Corpo -->
  <ellipse cx="100" cy="155" rx="35" ry="26" fill="#E8C450" stroke="#8B6914" stroke-width="2.5"/>
  <!-- Patas -->
  <ellipse cx="76" cy="178" rx="12" ry="14" fill="#DDB840" stroke="#8B6914" stroke-width="2"/>
  <ellipse cx="124" cy="178" rx="12" ry="14" fill="#DDB840" stroke="#8B6914" stroke-width="2"/>
  <ellipse cx="76" cy="190" rx="13" ry="5.5" fill="#F0DCA0" stroke="#8B6914" stroke-width="1.5"/>
  <ellipse cx="124" cy="190" rx="13" ry="5.5" fill="#F0DCA0" stroke="#8B6914" stroke-width="1.5"/>

  <!-- Juba -->
  <circle cx="100" cy="82" r="62" fill="#C07828" stroke="#8B5A10" stroke-width="2.5"/>
  <!-- Pontas da juba -->
  <path d="M100,18 L104,30 L96,30 Z" fill="#A06018"/>
  <path d="M68,24 L76,34 L66,36 Z" fill="#A06018"/>
  <path d="M132,24 L124,34 L134,36 Z" fill="#A06018"/>
  <path d="M42,48 L52,54 L44,60 Z" fill="#A06018"/>
  <path d="M158,48 L148,54 L156,60 Z" fill="#A06018"/>
  <path d="M36,80 L46,82 L40,90 Z" fill="#A06018"/>
  <path d="M164,80 L154,82 L160,90 Z" fill="#A06018"/>
  <path d="M40,110 L50,108 L46,116 Z" fill="#A06018"/>
  <path d="M160,110 L150,108 L154,116 Z" fill="#A06018"/>

  <!-- Rosto -->
  <circle cx="100" cy="82" r="48" fill="#F0D060" stroke="#8B6914" stroke-width="2"/>
  <ellipse cx="90" cy="60" rx="18" ry="10" fill="#F8E080" opacity="0.5"/>

  <!-- Olhos -->
  <ellipse cx="80" cy="76" rx="12" ry="13" fill="white" stroke="#8B6914" stroke-width="1.5"/>
  <circle cx="82" cy="78" r="7" fill="#8B5A2B"/>
  <circle cx="83" cy="79" r="4" fill="#1A0800"/>
  <circle cx="85" cy="74" r="3" fill="white"/>
  <ellipse cx="120" cy="76" rx="12" ry="13" fill="white" stroke="#8B6914" stroke-width="1.5"/>
  <circle cx="118" cy="78" r="7" fill="#8B5A2B"/>
  <circle cx="117" cy="79" r="4" fill="#1A0800"/>
  <circle cx="115" cy="74" r="3" fill="white"/>

  <!-- Nariz -->
  <path d="M95,90 L100,96 L105,90 Z" fill="#8B4513"/>
  <!-- Boca -->
  <path d="M100,96 L100,102" stroke="#8B6914" stroke-width="2" stroke-linecap="round"/>
  <path d="M92,104 C96,108 100,108 100,104" stroke="#8B6914" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="M100,104 C100,108 104,108 108,104" stroke="#8B6914" stroke-width="2" fill="none" stroke-linecap="round"/>

  <!-- Bochechas -->
  <circle cx="62" cy="95" r="9" fill="#FF9060" opacity="0.4"/>
  <circle cx="138" cy="95" r="9" fill="#FF9060" opacity="0.4"/>
</svg>"""

# ── 8: Elefante / Elephant ──
ANIMALS["elephant"] = """<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Corpo -->
  <ellipse cx="100" cy="148" rx="50" ry="32" fill="#8898A8" stroke="#4A5A6A" stroke-width="2.5"/>

  <!-- Pernas -->
  <rect x="60" y="168" width="22" height="24" rx="6" fill="#788898" stroke="#4A5A6A" stroke-width="2"/>
  <rect x="118" y="168" width="22" height="24" rx="6" fill="#788898" stroke="#4A5A6A" stroke-width="2"/>

  <!-- Cabeca -->
  <circle cx="100" cy="82" r="52" fill="#8898A8" stroke="#4A5A6A" stroke-width="2.5"/>
  <ellipse cx="88" cy="58" rx="20" ry="12" fill="#98A8B8" opacity="0.5"/>

  <!-- Orelha esquerda -->
  <ellipse cx="46" cy="82" rx="32" ry="42" fill="#788898" stroke="#4A5A6A" stroke-width="2" transform="rotate(-8 46 82)"/>
  <ellipse cx="48" cy="82" rx="22" ry="32" fill="#E0A0B0" opacity="0.4" transform="rotate(-8 48 82)"/>
  <!-- Orelha direita -->
  <ellipse cx="154" cy="82" rx="32" ry="42" fill="#788898" stroke="#4A5A6A" stroke-width="2" transform="rotate(8 154 82)"/>
  <ellipse cx="152" cy="82" rx="22" ry="32" fill="#E0A0B0" opacity="0.4" transform="rotate(8 152 82)"/>

  <!-- Olhos -->
  <ellipse cx="80" cy="72" rx="10" ry="8" fill="white" stroke="#4A5A6A" stroke-width="1.5"/>
  <circle cx="81" cy="73" r="5" fill="#3E2723"/>
  <circle cx="82" cy="73" r="3" fill="#1A0800"/>
  <circle cx="83" cy="70" r="2.5" fill="white"/>
  <ellipse cx="120" cy="72" rx="10" ry="8" fill="white" stroke="#4A5A6A" stroke-width="1.5"/>
  <circle cx="119" cy="73" r="5" fill="#3E2723"/>
  <circle cx="118" cy="73" r="3" fill="#1A0800"/>
  <circle cx="117" cy="70" r="2.5" fill="white"/>

  <!-- Sobrancelhas -->
  <path d="M70,62 C75,58 82,58 88,62" stroke="#4A5A6A" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M112,62 C118,58 125,58 130,62" stroke="#4A5A6A" stroke-width="2.5" fill="none" stroke-linecap="round"/>

  <!-- Tromba -->
  <path d="M100,85 C100,95 95,108 88,118 C82,126 78,128 74,125 C70,122 72,118 76,118 C80,118 84,115 88,108 C92,100 95,92 98,86"
        fill="#8898A8" stroke="#4A5A6A" stroke-width="2.5"/>
  <path d="M90,100 L96,98" stroke="#4A5A6A" stroke-width="1" opacity="0.5"/>
  <path d="M86,108 L92,106" stroke="#4A5A6A" stroke-width="1" opacity="0.5"/>
  <path d="M82,116 L87,114" stroke="#4A5A6A" stroke-width="1" opacity="0.5"/>

  <!-- Bochechas -->
  <circle cx="60" cy="90" r="8" fill="#FFB6C1" opacity="0.35"/>
  <circle cx="140" cy="90" r="8" fill="#FFB6C1" opacity="0.35"/>
</svg>"""

# ── 9: Macaco / Monkey ──
ANIMALS["monkey"] = """<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Rabo -->
  <path d="M140,150 C160,145 170,125 160,110 C155,100 145,105 150,112 C155,120 148,138 140,145"
        fill="none" stroke="#6B4420" stroke-width="4" stroke-linecap="round"/>

  <!-- Corpo -->
  <ellipse cx="100" cy="150" rx="34" ry="28" fill="#8B5830" stroke="#4A2C10" stroke-width="2.5"/>
  <ellipse cx="100" cy="153" rx="20" ry="18" fill="#F0D8B0" opacity="0.7"/>

  <!-- Patas -->
  <ellipse cx="76" cy="178" rx="12" ry="12" fill="#7A4C28" stroke="#4A2C10" stroke-width="2"/>
  <ellipse cx="124" cy="178" rx="12" ry="12" fill="#7A4C28" stroke="#4A2C10" stroke-width="2"/>

  <!-- Cabeca -->
  <circle cx="100" cy="78" r="50" fill="#8B5830" stroke="#4A2C10" stroke-width="2.5"/>

  <!-- Orelhas -->
  <circle cx="50" cy="72" r="16" fill="#7A4C28" stroke="#4A2C10" stroke-width="2"/>
  <circle cx="50" cy="72" r="10" fill="#F0D8B0"/>
  <circle cx="150" cy="72" r="16" fill="#7A4C28" stroke="#4A2C10" stroke-width="2"/>
  <circle cx="150" cy="72" r="10" fill="#F0D8B0"/>

  <!-- Rosto claro -->
  <ellipse cx="100" cy="85" rx="35" ry="32" fill="#F0D8B0" stroke="#4A2C10" stroke-width="1.5"/>

  <!-- Olhos -->
  <ellipse cx="82" cy="74" rx="12" ry="13" fill="white" stroke="#4A2C10" stroke-width="1.5"/>
  <circle cx="84" cy="76" r="7" fill="#3E2723"/>
  <circle cx="85" cy="77" r="4" fill="#1A0800"/>
  <circle cx="87" cy="72" r="3" fill="white"/>
  <ellipse cx="118" cy="74" rx="12" ry="13" fill="white" stroke="#4A2C10" stroke-width="1.5"/>
  <circle cx="116" cy="76" r="7" fill="#3E2723"/>
  <circle cx="115" cy="77" r="4" fill="#1A0800"/>
  <circle cx="113" cy="72" r="3" fill="white"/>

  <!-- Nariz -->
  <ellipse cx="100" cy="90" rx="6" ry="4" fill="#6B4420"/>
  <!-- Boca -->
  <path d="M90,98 C95,104 105,104 110,98" stroke="#4A2C10" stroke-width="2" fill="none" stroke-linecap="round"/>

  <!-- Bochechas -->
  <circle cx="68" cy="92" r="7" fill="#FFB6C1" opacity="0.35"/>
  <circle cx="132" cy="92" r="7" fill="#FFB6C1" opacity="0.35"/>
</svg>"""


ANIMAL_ORDER = ["dog", "cat", "cow", "horse", "pig", "chicken", "duck", "lion", "elephant", "monkey"]


def render_svg_to_png(svg_str, output_path, size=SIZE):
    """Renderiza SVG string para PNG com transparencia."""
    import fitz
    svg_bytes = svg_str.strip().encode("utf-8")
    doc = fitz.open(stream=svg_bytes, filetype="svg")
    page = doc[0]
    scale_x = size / page.rect.width
    scale_y = size / page.rect.height
    mat = fitz.Matrix(scale_x, scale_y)
    pix = page.get_pixmap(matrix=mat, alpha=True)
    pix.save(str(output_path))
    doc.close()
    print(f"  OK {output_path.name} ({pix.width}x{pix.height})")


def generate_all(names=None):
    """Gera PNGs para os animais especificados (ou todos)."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    targets = names if names else ANIMAL_ORDER
    for name in targets:
        if name not in ANIMALS:
            print(f"  ERRO Animal desconhecido: {name}")
            continue
        render_svg_to_png(ANIMALS[name], OUT_DIR / f"{name}.png")


def print_inline(names=None):
    """Imprime SVGs formatados para uso inline no HTML."""
    targets = names if names else ANIMAL_ORDER
    print("const ANIMAL_SVGS = [")
    for i, name in enumerate(targets):
        inline = " ".join(ANIMALS[name].strip().split())
        comma = "," if i < len(targets) - 1 else ""
        print(f"  /* {i}: {name.capitalize()} */")
        print(f"  `{inline}`{comma}")
    print("];")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--inline" in args:
        args.remove("--inline")
        print_inline(args if args else None)
    elif "--help" in args or "-h" in args:
        print(__doc__)
    else:
        targets = args if args else None
        print(f"Gerando PNGs {SIZE}x{SIZE}px em {OUT_DIR}/")
        generate_all(targets)
        print("Pronto!")
