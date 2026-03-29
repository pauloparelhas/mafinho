"""
download_placeholders.py
Baixa imagens gratuitas do OpenMoji e adiciona marcação de placeholder:
  1. X vermelho discreto no canto inferior direito (cheque sustado)
  2. Faixa "FREE" semi-transparente no rodapé
Quando as APIs voltarem, basta regerar as imagens sem este script.
"""

import requests, io, os
from PIL import Image, ImageDraw, ImageFont

BASE_URL = 'https://raw.githubusercontent.com/hfg-gmuend/openmoji/master/color/618x618/{code}.png'
ROOT = r'G:\Meu Drive\Dev_Paulo\mafinho\img'

# ── Frutas: id → código Unicode OpenMoji ─────────────────────────────────────
FRUITS = [
    ('banana',     '1F34C'),
    ('apple',      '1F34E'),
    ('pineapple',  '1F34D'),
    ('strawberry', '1F353'),
    ('grape',      '1F347'),
    ('pear',       '1F350'),
    ('watermelon', '1F349'),
    ('melon',      '1F348'),
    ('avocado',    '1F951'),
    ('guava',      '1F96D'),  # manga como substituto de goiaba (placeholder)
    ('mango',      '1F96D'),
    ('cherry',     '1F352'),
]

# ── Emoções com medo ──────────────────────────────────────────────────────────
# Rosto assustado + leve tint de cor para diferenciar menino/menina
EMOTIONS_SCARED = [
    ('boy_scared',  '1F631', (180, 210, 255, 35)),   # tint azul leve = menino
    ('girl_scared', '1F631', (255, 180, 210, 35)),   # tint rosa leve = menina
]


def fetch(code):
    url = BASE_URL.format(code=code)
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return Image.open(io.BytesIO(r.content)).convert('RGBA')


def add_placeholder_marks(img: Image.Image) -> Image.Image:
    """
    Adiciona ao PNG:
      - X vermelho discreto, 36px, canto inferior direito
      - Faixa 'FREE IMG' semi-transparente no rodapé
    """
    img = img.copy()
    w, h = img.size
    draw = ImageDraw.Draw(img)

    # 1. X vermelho (cheque sustado) ─ quase imperceptível
    pad = 10
    sz = 36
    x1, y1 = w - pad - sz, h - pad - sz
    x2, y2 = w - pad,      h - pad
    red = (210, 30, 30, 160)
    draw.line([(x1, y1), (x2, y2)], fill=red, width=3)
    draw.line([(x2, y1), (x1, y2)], fill=red, width=3)

    # 2. Faixa de rodapé "FREE IMG" ─ visível mas discreta
    band_h = 28
    band = Image.new('RGBA', (w, band_h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.rectangle([(0, 0), (w, band_h)], fill=(60, 60, 60, 110))
    try:
        font = ImageFont.truetype('arial.ttf', 14)
    except Exception:
        font = ImageFont.load_default()
    label = 'FREE IMG - substituir quando API disponivel'
    # Centralizar texto
    try:
        bbox = bd.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
    except Exception:
        tw = len(label) * 7
    tx = max(4, (w - tw) // 2)
    bd.text((tx, 6), label, fill=(255, 255, 255, 200), font=font)
    img.paste(band, (0, h - band_h), band)

    return img


def add_tint(img: Image.Image, tint_rgba: tuple) -> Image.Image:
    tint = Image.new('RGBA', img.size, tint_rgba)
    return Image.alpha_composite(img, tint)


def save(img: Image.Image, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img = img.resize((512, 512), Image.LANCZOS)
    img.save(path, 'PNG')
    print(f'  OK  {os.path.basename(path)}')


# ─── FRUTAS ──────────────────────────────────────────────────────────────────
print('\n== Frutas ==')
for fruit_id, code in FRUITS:
    out = os.path.join(ROOT, 'fruits', f'{fruit_id}.png')
    if os.path.exists(out):
        print(f'  skip {fruit_id}')
        continue
    try:
        img = fetch(code)
        img = add_placeholder_marks(img)
        save(img, out)
    except Exception as e:
        print(f'  ERRO {fruit_id}: {e}')

# ─── EMOÇÕES (scared) ────────────────────────────────────────────────────────
print('\n== Emocoes: medo ==')
for name, code, tint in EMOTIONS_SCARED:
    out = os.path.join(ROOT, 'emotions', f'{name}.png')
    if os.path.exists(out):
        print(f'  skip {name}')
        continue
    try:
        img = fetch(code)
        img = add_tint(img, tint)
        img = add_placeholder_marks(img)
        save(img, out)
    except Exception as e:
        print(f'  ERRO {name}: {e}')

print('\nConcluído.')
