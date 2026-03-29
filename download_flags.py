#!/usr/bin/env python3
"""
download_flags.py — baixa bandeiras do FlagCDN para img/flags/
Uso: python download_flags.py [--force]
"""

import os, sys, requests

OUT_DIR = os.path.join(os.path.dirname(__file__), 'img', 'flags')
FLAG_URL = 'https://flagcdn.com/w320/{code}.png'

FLAGS = [
    {'code': 'br', 'name': 'Brasil'},
    {'code': 'ca', 'name': 'Canadá'},
    {'code': 'us', 'name': 'Estados Unidos'},
    {'code': 'pt', 'name': 'Portugal'},
    {'code': 'ar', 'name': 'Argentina'},
    {'code': 'fr', 'name': 'França'},
    {'code': 'de', 'name': 'Alemanha'},
    {'code': 'jp', 'name': 'Japão'},
    {'code': 'mx', 'name': 'México'},
    {'code': 'gb', 'name': 'Reino Unido'},
    {'code': 'es', 'name': 'Espanha'},
    {'code': 'it', 'name': 'Itália'},
]

def main():
    force = '--force' in sys.argv
    os.makedirs(OUT_DIR, exist_ok=True)

    ok = skipped = errors = 0
    for f in FLAGS:
        path = os.path.join(OUT_DIR, f['code'] + '.png')
        if os.path.exists(path) and not force:
            print(f"  skip  {f['code']}.png ({f['name']})")
            skipped += 1
            continue
        try:
            url = FLAG_URL.format(code=f['code'])
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            with open(path, 'wb') as fp:
                fp.write(r.content)
            size = len(r.content) // 1024
            print(f"  OK    {f['code']}.png — {f['name']} ({size}KB)")
            ok += 1
        except Exception as e:
            print(f"  ERRO  {f['code']}.png — {f['name']}: {e}")
            errors += 1

    print(f"\n{'-'*40}")
    print(f"  Baixados: {ok}  |  Existentes: {skipped}  |  Erros: {errors}")
    if errors:
        print("  Rode novamente para tentar os erros.")

if __name__ == '__main__':
    main()
