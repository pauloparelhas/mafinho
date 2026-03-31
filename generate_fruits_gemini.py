#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_fruits_gemini.py — Gera imagens de frutas via Gemini Imagen 3 API

Uso:
  python generate_fruits_gemini.py           # gera todas as frutas ausentes
  python generate_fruits_gemini.py --force   # regera todas, mesmo as existentes
  python generate_fruits_gemini.py banana apple --force  # só essas duas

Setup (uma vez):
  1. pip install requests Pillow
  2. Obtenha chave em aistudio.google.com
  3. Adicione ao .env:  GEMINI_API_KEY=AIza...

Padrão visual (INVIOLÁVEL — garante consistência entre todas as frutas):
  - Fruta inteira, sem cortes
  - Centralizada em fundo branco puro
  - Rosto kawaii fixo: dois olhos grandes redondos + sorrisinho pequeno
  - Flat illustration: sem gradientes pesados, contorno preto limpo
  - Cores naturais vibrantes da fruta
  - Formato quadrado, sem sombra, sem texto extra
"""

import sys
import os
import json
import time
import base64
import requests

GEMINI_MODEL = "gemini-2.5-flash-image"
GEMINI_BASE_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)

# ── Sufixo de estilo comum a todas as frutas ────────────────────────────────
STYLE_SUFFIX = (
    "cute kawaii cartoon style, tiny cute face drawn on the fruit with "
    "big round sparkly eyes and a small happy smile, "
    "flat illustration, clean black outline, "
    "vibrant natural colors, pure white background, "
    "perfectly centered, no shadow, no text, no extra objects, "
    "square composition, high quality"
)

# ── Dados das frutas: id + descrição física precisa ─────────────────────────
# A descrição física garante que o modelo gere a fruta correta com fidelidade.
# O STYLE_SUFFIX garante o mesmo estilo em todas.
FRUITS = [
    {
        "id": "banana",
        "description": "a single yellow crescent-shaped banana, whole and unpeeled",
    },
    {
        "id": "apple",
        "description": (
            "a round bright red apple with a short brown stem "
            "and a small green leaf on top, whole and uncut"
        ),
    },
    {
        "id": "pineapple",
        "description": (
            "a pineapple with golden-brown diamond-pattern textured skin "
            "and a crown of spiky green leaves on top, whole"
        ),
    },
    {
        "id": "strawberry",
        "description": (
            "a heart-shaped bright red strawberry with tiny yellow seeds "
            "on the surface and a small green leafy crown on top, whole"
        ),
    },
    {
        "id": "grape",
        "description": (
            "a cluster of round juicy purple grapes hanging together "
            "in a bunch, with two small green leaves at the top, whole"
        ),
    },
    {
        "id": "pear",
        "description": (
            "a pear with green and yellow gradient skin, "
            "classic pear shape, short brown stem, small leaf, whole and uncut"
        ),
    },
    {
        "id": "watermelon",
        "description": (
            "a whole round watermelon with dark green skin "
            "and lighter green vertical stripes, uncut"
        ),
    },
    {
        "id": "melon",
        "description": (
            "a whole round cantaloupe melon with golden-orange rough netted skin, "
            "uncut"
        ),
    },
    {
        "id": "avocado",
        "description": (
            "a whole pear-shaped avocado with dark green bumpy skin, "
            "uncut, single fruit"
        ),
    },
    {
        "id": "guava",
        "description": (
            "a whole round guava fruit with light green to yellow skin, "
            "uncut, single fruit"
        ),
    },
    {
        "id": "mango",
        "description": (
            "a whole oval mango with smooth yellow-orange gradient skin, "
            "uncut, single fruit"
        ),
    },
    {
        "id": "cherry",
        "description": (
            "two round bright red cherries joined at the stem, "
            "with small green leaves at the top, whole"
        ),
    },
]


def load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_path):
        print("ERRO: Arquivo .env nao encontrado!")
        print("Crie o arquivo .env com:  GEMINI_API_KEY=AIza...")
        sys.exit(1)
    vals = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                vals[k.strip()] = v.strip()
    return vals


def build_prompt(fruit):
    return f"{fruit['description']}, {STYLE_SUFFIX}"


def generate_image(api_key, prompt, output_path):
    url = f"{GEMINI_BASE_URL}?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }

    try:
        resp = requests.post(url, json=payload, timeout=90)

        if resp.status_code == 429:
            return False, "Rate limit — aguarde 1 minuto e tente novamente"

        if resp.status_code in (400, 403):
            try:
                msg = resp.json().get("error", {}).get("message", resp.text[:200])
            except Exception:
                msg = resp.text[:200]
            return False, f"HTTP {resp.status_code}: {msg}"

        if resp.status_code != 200:
            try:
                msg = resp.json().get("error", {}).get("message", resp.text[:200])
            except Exception:
                msg = resp.text[:200]
            return False, f"HTTP {resp.status_code}: {msg}"

        data = resp.json()
        # Extrai a parte de imagem da resposta generateContent
        try:
            parts = data["candidates"][0]["content"]["parts"]
        except (KeyError, IndexError):
            return False, f"Resposta inesperada: {str(data)[:200]}"

        b64 = None
        for part in parts:
            inline = part.get("inlineData", {})
            if inline.get("mimeType", "").startswith("image/"):
                b64 = inline.get("data", "")
                break

        if not b64:
            return False, f"Sem imagem na resposta: {str(data)[:200]}"

        image_bytes = base64.b64decode(b64)
        if len(image_bytes) < 1000:
            return False, "Imagem muito pequena — provavelmente erro"

        try:
            from PIL import Image
            import io

            img = Image.open(io.BytesIO(image_bytes))
            img.save(output_path, "PNG")
        except Exception:
            with open(output_path, "wb") as fp:
                fp.write(image_bytes)

        file_size = os.path.getsize(output_path) // 1024
        return True, f"OK ({file_size}KB)"

    except requests.exceptions.Timeout:
        return False, "Timeout (90s) — tente novamente"
    except Exception as e:
        return False, f"Erro: {str(e)[:200]}"


def main():
    force = "--force" in sys.argv
    requested_ids = [a for a in sys.argv[1:] if not a.startswith("--")]

    env = load_env()
    api_key = env.get("GEMINI_API_KEY")
    if not api_key:
        print("ERRO: GEMINI_API_KEY nao encontrado no .env!")
        print("Obtenha sua chave em aistudio.google.com e adicione ao .env:")
        print("  GEMINI_API_KEY=AIza...")
        sys.exit(1)

    if requested_ids:
        valid_ids = {f["id"] for f in FRUITS}
        for rid in requested_ids:
            if rid not in valid_ids:
                print(f"ERRO: Fruta '{rid}' nao encontrada.")
                print(f"  Disponiveis: {', '.join(f['id'] for f in FRUITS)}")
                sys.exit(1)
        fruits = [f for f in FRUITS if f["id"] in requested_ids]
    else:
        fruits = FRUITS

    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(base_dir, "img", "fruits")
    os.makedirs(out_dir, exist_ok=True)

    print("=" * 60)
    print("  Mafinho Explora — Gerador de Frutas (Gemini Imagen 3)")
    print("=" * 60)
    print(f"  Total a processar: {len(fruits)} frutas")
    print(f"  Destino: img/fruits/")
    print(f"  Forcar regeracao: {'Sim' if force else 'Nao'}")
    print("=" * 60)

    generated = skipped = failed = 0

    for i, fruit in enumerate(fruits, 1):
        out_path = os.path.join(out_dir, f"{fruit['id']}.png")

        if os.path.exists(out_path) and not force:
            print(f"  [{i:2}/{len(fruits)}] {fruit['id']:12s} — ja existe (use --force para regerar)")
            skipped += 1
            continue

        prompt = build_prompt(fruit)
        print(f"  [{i:2}/{len(fruits)}] {fruit['id']:12s} — gerando...", end=" ", flush=True)

        success, msg = generate_image(api_key, prompt, out_path)

        if success:
            print(f"[OK] {msg}")
            generated += 1
        else:
            print(f"[FALHA] {msg}")
            failed += 1

        if i < len(fruits):
            time.sleep(1.5)

    print("\n" + "=" * 60)
    print("  RESUMO")
    print("=" * 60)
    print(f"  Geradas:  {generated}")
    print(f"  Puladas:  {skipped}")
    print(f"  Falhas:   {failed}")
    if failed > 0:
        print("\n  Rode novamente para tentar as que falharam.")
        print("  Use --force para regerar todas.")


if __name__ == "__main__":
    main()
