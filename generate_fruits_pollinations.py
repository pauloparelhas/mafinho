#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_fruits_pollinations.py — Gera imagens de frutas via Pollinations.ai
Completamente gratuito, sem conta, sem API key.

Uso:
  python generate_fruits_pollinations.py           # gera ausentes
  python generate_fruits_pollinations.py --force   # regera todas
  python generate_fruits_pollinations.py banana apple --force

Setup:
  pip install requests Pillow
"""

import sys
import os
import time
import requests
from urllib.parse import quote

STYLE = (
    "cute kawaii cartoon illustration, Disney Pixar toddler style, "
    "flat illustration, big expressive eyes, rounded shapes, "
    "vibrant saturated colors, clean dark outline, white background, "
    "centered, no text, no shadow, no extra characters, high quality"
)

FRUITS = [
    {
        "id": "banana",
        "desc": "single yellow banana, long curved crescent shape, elongated curved fruit with pointed tips, NOT round, kawaii face with big eyes and smile",
    },
    {
        "id": "apple",
        "desc": "whole round bright red apple with short green stem and tiny leaf, cute kawaii face, big round eyes, happy smile",
    },
    {
        "id": "pineapple",
        "desc": "whole pineapple with golden diamond-pattern skin and spiky green crown, cute kawaii face, big round eyes, tiny smile",
    },
    {
        "id": "strawberry",
        "desc": "whole heart-shaped bright red strawberry with tiny yellow seeds and green leafy crown, cute kawaii face, big round eyes",
    },
    {
        "id": "grape",
        "desc": "bunch of round juicy purple grapes with small green leaf at top, cute kawaii face on the bunch, big round eyes",
    },
    {
        "id": "pear",
        "desc": "whole green-yellow pear with short brown stem and tiny leaf, cute kawaii face, big round eyes, tiny smile",
    },
    {
        "id": "watermelon",
        "desc": "whole round watermelon with dark green skin and lighter green stripes, cute kawaii face, big round eyes, happy smile",
    },
    {
        "id": "melon",
        "desc": "yellow melon fruit, perfectly smooth round fruit, bright sunny yellow smooth skin, small brown stem on top, tropical melon, kawaii face with big round eyes and happy smile",
    },
    {
        "id": "avocado",
        "desc": "whole pear-shaped avocado with dark green bumpy skin, cute kawaii face, big round eyes, happy smile",
    },
    {
        "id": "guava",
        "desc": "whole round guava fruit with light green to yellow skin, cute kawaii face, big round eyes, tiny smile",
    },
    {
        "id": "mango",
        "desc": "whole mango fruit, kidney-shaped oval teardrop, yellow and red-orange skin, larger at bottom tapered at top with short stem, NOT round like an orange, kawaii face with big eyes",
    },
    {
        "id": "cherry",
        "desc": "two round bright red cherries connected by green stem with small leaves, cute kawaii faces, big round eyes",
    },
]


def generate_image(fruit_desc, output_path):
    prompt = f"{fruit_desc}, {STYLE}"
    encoded = quote(prompt)
    # seed fixo por fruta para reprodutibilidade
    seed = abs(hash(fruit_desc)) % 999999
    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width=1024&height=1024&seed={seed}&nologo=true&enhance=false"
    )

    try:
        resp = requests.get(url, timeout=120)

        if resp.status_code != 200:
            return False, f"HTTP {resp.status_code}"

        if len(resp.content) < 5000:
            return False, f"Resposta muito pequena ({len(resp.content)} bytes)"

        # verifica se é imagem válida
        if not resp.content[:4] in (b'\x89PNG', b'\xff\xd8\xff\xe0', b'\xff\xd8\xff\xe1'):
            if resp.content[:8] != b'\x89PNG\r\n\x1a\n' and resp.content[:2] != b'\xff\xd8':
                return False, "Resposta não é imagem"

        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(resp.content))
            img.save(output_path, "PNG")
        except Exception:
            with open(output_path, "wb") as f:
                f.write(resp.content)

        size_kb = os.path.getsize(output_path) // 1024
        return True, f"OK ({size_kb}KB)"

    except requests.exceptions.Timeout:
        return False, "Timeout (120s) — tente novamente"
    except Exception as e:
        return False, f"Erro: {str(e)[:150]}"


def main():
    force = "--force" in sys.argv
    requested = [a for a in sys.argv[1:] if not a.startswith("--")]

    if requested:
        valid = {f["id"] for f in FRUITS}
        for r in requested:
            if r not in valid:
                print(f"ERRO: '{r}' nao encontrado. Disponiveis: {', '.join(f['id'] for f in FRUITS)}")
                sys.exit(1)
        fruits = [f for f in FRUITS if f["id"] in requested]
    else:
        fruits = FRUITS

    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(base_dir, "img", "fruits")
    os.makedirs(out_dir, exist_ok=True)

    print("=" * 60)
    print("  Mafinho — Frutas via Pollinations.ai (FLUX, gratuito)")
    print("=" * 60)
    print(f"  Total: {len(fruits)} frutas | Forcar: {'Sim' if force else 'Nao'}")
    print("=" * 60)

    generated = skipped = failed = 0

    for i, fruit in enumerate(fruits, 1):
        out_path = os.path.join(out_dir, f"{fruit['id']}.png")

        if os.path.exists(out_path) and not force:
            print(f"  [{i:2}/{len(fruits)}] {fruit['id']:12s} — ja existe (use --force)")
            skipped += 1
            continue

        print(f"  [{i:2}/{len(fruits)}] {fruit['id']:12s} — gerando...", end=" ", flush=True)
        ok, msg = generate_image(fruit["desc"], out_path)

        if ok:
            print(f"[OK] {msg}")
            generated += 1
        else:
            print(f"[FALHA] {msg}")
            failed += 1

        if i < len(fruits):
            time.sleep(2)  # respeita rate limit do serviço

    print("\n" + "=" * 60)
    print(f"  Geradas: {generated}  |  Puladas: {skipped}  |  Falhas: {failed}")
    if failed:
        print("  Rode novamente para tentar as que falharam.")
        print("  Use --force para regerar todas.")
    print("=" * 60)


if __name__ == "__main__":
    main()
