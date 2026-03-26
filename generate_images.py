#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
"""
Mafinho Explora -- Gerador Automatico de Imagens
Usa HuggingFace Inference API (FLUX.1-schnell) — gratuito, zero tokens Claude.

Uso:
  python generate_images.py animals          # gera so animais
  python generate_images.py body             # gera corpo humano
  python generate_images.py --all            # gera tudo
  python generate_images.py body --force     # regera mesmo se ja existir

Setup (uma vez):
  1. pip install requests Pillow
  2. Crie conta gratis em huggingface.co
  3. Settings -> Access Tokens -> New token (Read)
  4. Adicione ao .env:  HF_TOKEN=hf_...
"""

import sys
import os
import json
import time
import io
import requests

HF_MODEL = "black-forest-labs/FLUX.1-schnell"
HF_API_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"

PROMPT_TEMPLATE = (
    "cute kawaii cartoon illustration of {name}, "
    "Disney/Pixar toddler style, flat illustration, "
    "big expressive eyes, rounded shapes, vibrant saturated colors, "
    "clean dark outline, white background, centered, "
    "no text, no shadow, no extra characters, high quality"
)

# ── Carregar tokens do .env ──
def load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if not os.path.exists(env_path):
        print("ERRO: Arquivo .env nao encontrado!")
        print("Crie o arquivo .env com:  HF_TOKEN=hf_...")
        sys.exit(1)
    vals = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                vals[k.strip()] = v.strip()
    return vals

# ── Carregar manifest ──
def load_manifest():
    manifest_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image_manifest.json')
    if not os.path.exists(manifest_path):
        print("ERRO: image_manifest.json nao encontrado!")
        sys.exit(1)
    with open(manifest_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# ── Gerar uma imagem via HuggingFace ──
def generate_image(hf_token, item_name, output_path):
    prompt = PROMPT_TEMPLATE.format(name=item_name)
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {
        "inputs": prompt,
        "parameters": {"num_inference_steps": 4, "guidance_scale": 0.0}
    }

    try:
        resp = requests.post(HF_API_URL, headers=headers, json=payload, timeout=120)

        # Modelo carregando — aguardar e tentar de novo
        if resp.status_code == 503:
            wait = resp.json().get('estimated_time', 20)
            return False, f"Modelo carregando ({wait:.0f}s) — rode novamente em instantes"

        if resp.status_code == 429:
            return False, "Rate limit — aguarde 1 minuto e tente novamente"

        if resp.status_code != 200:
            try:
                msg = resp.json().get('error', resp.text[:120])
            except Exception:
                msg = resp.text[:120]
            return False, f"HTTP {resp.status_code}: {msg}"

        image_bytes = resp.content
        if len(image_bytes) < 1000:
            return False, "Resposta muito pequena — provavelmente nao e imagem"

        try:
            from PIL import Image
            img = Image.open(io.BytesIO(image_bytes))
            img.save(output_path, 'PNG')
        except Exception:
            with open(output_path, 'wb') as f:
                f.write(image_bytes)

        file_size = os.path.getsize(output_path)
        return True, f"OK ({file_size // 1024}KB)"

    except requests.exceptions.Timeout:
        return False, "Timeout (120s) — tente novamente"
    except Exception as e:
        return False, f"Erro: {str(e)[:150]}"

# ── Main ──
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    force = '--force' in sys.argv
    topics = []
    for arg in sys.argv[1:]:
        if arg == '--all':
            topics = None
            break
        elif not arg.startswith('--'):
            topics.append(arg)

    env = load_env()
    hf_token = env.get('HF_TOKEN')
    if not hf_token:
        print("ERRO: HF_TOKEN nao encontrado no .env!")
        print("Crie conta em huggingface.co, gere um token (Read) e adicione ao .env:")
        print("  HF_TOKEN=hf_...")
        sys.exit(1)

    manifest = load_manifest()
    if topics is None:
        topics = list(manifest.keys())

    for t in topics:
        if t not in manifest:
            print(f"ERRO: Topico '{t}' nao encontrado. Disponiveis: {', '.join(manifest.keys())}")
            sys.exit(1)

    print(f"Provedor: HuggingFace ({HF_MODEL})")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    total_generated = total_skipped = total_failed = 0

    for topic in topics:
        items = manifest[topic]
        img_dir = os.path.join(base_dir, 'img', topic)
        os.makedirs(img_dir, exist_ok=True)

        print(f"\n{'='*50}")
        print(f"  Topico: {topic} ({len(items)} imagens)")
        print(f"{'='*50}")

        for i, item in enumerate(items):
            item_id   = item['id']
            item_name = item['prompt_name']
            output_path = os.path.join(img_dir, f"{item_id}.png")

            if os.path.exists(output_path) and not force:
                print(f"  [{i+1}/{len(items)}] {item_id:12s} -- JA EXISTE (pulando)")
                total_skipped += 1
                continue

            print(f"  [{i+1}/{len(items)}] {item_id:12s} -- Gerando...", end=' ', flush=True)
            success, msg = generate_image(hf_token, item_name, output_path)

            if success:
                print(f"[OK] {msg}")
                total_generated += 1
            else:
                print(f"[FALHA] {msg}")
                total_failed += 1

            if i < len(items) - 1:
                time.sleep(2)

    print(f"\n{'='*50}")
    print(f"  RESUMO")
    print(f"{'='*50}")
    print(f"  Geradas:  {total_generated}")
    print(f"  Puladas:  {total_skipped}")
    print(f"  Falhas:   {total_failed}")
    print(f"  Imagens em: img/{topics[0] if len(topics)==1 else ''}")

    if total_failed > 0:
        print(f"\n  Rode novamente para tentar as que falharam.")
        print(f"  Use --force para regerar todas.")

if __name__ == '__main__':
    main()
