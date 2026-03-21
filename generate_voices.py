#!/usr/bin/env python3
"""
generate_voices.py — Mafinho Explora Voice Generator
Usa Coqui XTTS-v2 para gerar áudios com voice cloning da mãe.

Uso:
  python generate_voices.py --test          # Gera 5 frases de teste
  python generate_voices.py                 # Gera TODAS as frases
  python generate_voices.py --list          # Lista todas as frases sem gerar

Requisitos:
  pip install TTS pydub
  Amostra de voz: audio/sample_mae.wav (30seg-2min, português)
"""

import argparse
import glob as globmod
import json
import os
import re
import sys
import time

# Garante que ffmpeg do winget esteja no PATH (Windows)
if sys.platform == 'win32':
    _winget_ffmpeg = globmod.glob(
        os.path.expanduser("~/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg*/*/bin")
    )
    if _winget_ffmpeg and _winget_ffmpeg[0] not in os.environ.get("PATH", ""):
        os.environ["PATH"] = _winget_ffmpeg[0] + ";" + os.environ.get("PATH", "")

# ---- Todas as frases do Mafinho Explora ----

# Números (nomes)
NUM_PT = ['Um', 'Dois', 'Três', 'Quatro', 'Cinco', 'Seis', 'Sete', 'Oito', 'Nove', 'Dez']
NUM_EN = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']

# Cores
COLORS_PT = ['Vermelho', 'Azul', 'Amarelo', 'Verde', 'Laranja', 'Roxo', 'Rosa', 'Preto', 'Branco']
COLORS_EN = ['Red', 'Blue', 'Yellow', 'Green', 'Orange', 'Purple', 'Pink', 'Black', 'White']

# Animais
ANIMALS_PT = ['Cachorro', 'Gato', 'Vaca', 'Cavalo', 'Porco', 'Galinha', 'Pato', 'Leão', 'Elefante', 'Macaco']
ANIMALS_EN = ['Dog', 'Cat', 'Cow', 'Horse', 'Pig', 'Chicken', 'Duck', 'Lion', 'Elephant', 'Monkey']
# Gênero dos animais (para construir frases com artigo correto)
ANIMALS_GEN = ['o', 'o', 'a', 'o', 'o', 'a', 'o', 'o', 'o', 'o']

# Formas
SHAPES_PT = ['Círculo', 'Quadrado', 'Triângulo', 'Estrela', 'Coração', 'Losango', 'Retângulo', 'Oval']
SHAPES_EN = ['Circle', 'Square', 'Triangle', 'Star', 'Heart', 'Diamond', 'Rectangle', 'Oval']
SHAPES_GEN = ['o', 'o', 'o', 'a', 'o', 'o', 'o', 'o']

# Letras (A-Z maiúsculas)
LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
LETTERS_NAMES_PT = ['Á','Bê','Cê','Dê','É','Éfe','Gê','Agá','I','Jota','Cá','Éle','Éme','Éne','Ó','Pê','Quê','Érre','Ésse','Tê','U','Vê','Dáblio','Xis','Ípsilon','Zê']
LETTERS_NAMES_EN = ['Ei','Bi','Si','Di','I','Ef','Ji','Eitch','Ai','Jei','Kei','El','Em','En','Ou','Pi','Kiu','Ar','Es','Ti','Iu','Vi','Dabeliu','Ex','Uai','Zi']

# Cores usadas no jogo de pintar (5 cores)
PAINT_COLORS_PT = ['Vermelho', 'Azul', 'Verde', 'Amarelo', 'Roxo']
PAINT_COLORS_EN = ['Red', 'Blue', 'Green', 'Yellow', 'Purple']

# Encorajamentos (compartilhados por todos os jogos)
ENCOURAGE_PT = [
    'Isso! Muito bem!', 'Parabéns!', 'Uau! Que esperto!',
    'Eba! Acertou!', 'Que inteligente!', 'Muito bem!',
    'Boa! Boa! Boa!', 'Que criança boa!', 'Eba! Que legal!',
    'Que maravilha!', 'Arrasou!', 'Que lindo!',
    'Mandou bem!', 'Isso aí!', 'Perfeito!',
]
ENCOURAGE_EN = [
    'Yay! Great job!', 'Well done!', 'Wow! So smart!',
    'You got it!', 'So clever!', 'Very good!',
    'Awesome!', 'What a good kid!', 'Yay! So cool!',
    'Wonderful!', 'Amazing!', 'How beautiful!',
    'Nailed it!', 'That\'s it!', 'Perfect!',
]


def build_phrase_list():
    """Constrói a lista completa de frases para geração."""
    phrases = {'pt': {}, 'en': {}}

    def add(lang, category, text):
        """Adiciona frase ao dicionário, evitando duplicatas."""
        key = f"{category}/{_slugify(text)}"
        phrases[lang][text] = key

    # ─── NÚMEROS ───
    for i, (pt, en) in enumerate(zip(NUM_PT, NUM_EN)):
        add('pt', 'numeros', pt)
        add('en', 'numbers', en)
        # "Que número é esse?" / "What number is this?"
        add('pt', 'numeros', f'{pt}!')
        add('en', 'numbers', f'{en}!')

    add('pt', 'numeros', 'Que número é esse?')
    add('en', 'numbers', 'What number is this?')

    # Contagem
    for i in range(1, 11):
        add('pt', 'numeros', f'Conte {i}!')
        add('en', 'numbers', f'Count {i}!')

    # Pintar números — "Pinte o 3 de vermelho" etc
    for pt_c, en_c in zip(PAINT_COLORS_PT, PAINT_COLORS_EN):
        add('pt', 'numeros', f'Pinte de {pt_c.lower()}!')
        add('en', 'numbers', f'Paint it {en_c.lower()}!')

    # Celebrações de números
    num_cel_pt = [
        'Parabéns! Você pintou todos os números! Que artista!',
        'Parabéns! Você escreveu todos os números! Que caligrafia linda!',
        'Parabéns! Você conhece todos os números! Que criança esperta!',
        'Parabéns! Você acertou todos os números! Que esperto!',
        'Parabéns! Você arrastou todos os números! Que incrível!',
        'Parabéns! Você contou até dez! Que criança esperta!',
    ]
    num_cel_en = [
        'Congratulations! You painted all the numbers! What an artist!',
        'Congratulations! You wrote all the numbers! Beautiful handwriting!',
        'Congratulations! You know all the numbers! So smart!',
        'Congratulations! You got all the numbers right! So clever!',
        'Congratulations! You dragged all the numbers! Amazing!',
        'Congratulations! You counted to ten! So smart!',
    ]
    for pt, en in zip(num_cel_pt, num_cel_en):
        add('pt', 'numeros', pt)
        add('en', 'numbers', en)

    # ─── CORES ───
    for pt, en in zip(COLORS_PT, COLORS_EN):
        add('pt', 'cores', pt)
        add('en', 'colors', en)
        add('pt', 'cores', f'{pt}!')
        add('en', 'colors', f'{en}!')

    add('pt', 'cores', 'Qual cor é esta?')
    add('en', 'colors', 'What color is this?')
    add('pt', 'cores', 'Aperte na cor')
    add('en', 'colors', 'Tap the color')
    add('pt', 'cores', 'Arraste para a cor certa!')
    add('en', 'colors', 'Drag to the right color!')
    add('pt', 'cores', 'Toque nos objetos')
    add('en', 'colors', 'Tap the')

    # "Aperte na cor vermelho" etc
    for pt, en in zip(COLORS_PT, COLORS_EN):
        add('pt', 'cores', f'Aperte na cor {pt.lower()}')
        add('en', 'colors', f'Tap the color {en.lower()}')

    # Celebrações de cores
    cor_cel_pt = [
        'Parabéns! Você conhece todas as cores! Que inteligente!',
        'Parabéns! Você acertou todas as cores! Muito bem!',
        'Parabéns! Você arrastou todas as cores! Que incrível!',
        'Parabéns! Você separou todas as cores! Que observador!',
    ]
    cor_cel_en = [
        'Congratulations! You know all the colors! So smart!',
        'Congratulations! You got all the colors right! Great job!',
        'Congratulations! You dragged all the colors! Amazing!',
        'Congratulations! You sorted all the colors! So observant!',
    ]
    for pt, en in zip(cor_cel_pt, cor_cel_en):
        add('pt', 'cores', pt)
        add('en', 'colors', en)

    # ─── ANIMAIS ───
    for pt, en, gen in zip(ANIMALS_PT, ANIMALS_EN, ANIMALS_GEN):
        add('pt', 'animais', pt)
        add('en', 'animals', en)
        add('pt', 'animais', f'{pt}!')
        add('en', 'animals', f'{en}!')
        # "É o cachorro!" / "It's the dog!"
        add('pt', 'animais', f'É {gen} {pt}!')
        add('en', 'animals', f"It's the {en}!")

    add('pt', 'animais', 'Quem é esse animal?')
    add('en', 'animals', 'Who is this animal?')
    add('pt', 'animais', 'Quem é?')
    add('en', 'animals', 'Who is it?')

    # "Qual é o cachorro?" etc (jogo clicar)
    for pt, en, gen in zip(ANIMALS_PT, ANIMALS_EN, ANIMALS_GEN):
        add('pt', 'animais', f'Qual é {gen} {pt}?')
        add('en', 'animals', f'Where is the {en}?')

    # Arrastar animais (silhueta)
    add('pt', 'animais', 'Arraste para a sombra!')
    add('en', 'animals', 'Drag to the shadow!')

    anim_cel_pt = [
        'Parabéns! Você conhece todos os animais! Que esperto!',
        'Parabéns! Você acertou todos os animais! Muito bem!',
        'Parabéns! Você encontrou todas as sombras! Que esperto!',
    ]
    anim_cel_en = [
        'Congratulations! You know all the animals! So smart!',
        'Congratulations! You got all the animals right! Great job!',
        'Congratulations! You found all the shadows! Amazing!',
    ]
    for pt, en in zip(anim_cel_pt, anim_cel_en):
        add('pt', 'animais', pt)
        add('en', 'animals', en)

    # ─── FORMAS ───
    for pt, en, gen in zip(SHAPES_PT, SHAPES_EN, SHAPES_GEN):
        add('pt', 'formas', pt)
        add('en', 'shapes', en)
        add('pt', 'formas', f'{pt}!')
        add('en', 'shapes', f'{en}!')
        # "É o círculo!" / "It's the circle!"
        art = 'a' if gen == 'a' else 'o'
        add('pt', 'formas', f'É {art} {pt}!')
        add('en', 'shapes', f"It's the {en.lower()}!")

    add('pt', 'formas', 'Qual forma é essa?')
    add('en', 'shapes', 'What shape is this?')
    add('pt', 'formas', 'Qual forma?')
    add('en', 'shapes', 'What shape?')

    # "Qual é o círculo?" etc (jogo clicar)
    for pt, en, gen in zip(SHAPES_PT, SHAPES_EN, SHAPES_GEN):
        art = 'a' if gen == 'a' else 'o'
        add('pt', 'formas', f'Qual é {art} {pt}?')
        add('en', 'shapes', f'Where is the {en.lower()}?')

    # "Toque nos círculos" (jogo encontrar)
    for pt, en in zip(SHAPES_PT, SHAPES_EN):
        add('pt', 'formas', f'Toque nos {_plural_pt(pt)}!')
        add('en', 'shapes', f'Tap the {en.lower()}s!')

    # Pintar formas
    for pt_c, en_c in zip(PAINT_COLORS_PT, PAINT_COLORS_EN):
        add('pt', 'formas', f'Pinte de {pt_c.lower()}!')
        add('en', 'shapes', f'Paint it {en_c.lower()}!')

    form_cel_pt = [
        'Parabéns! Você conhece todas as formas! Que inteligente!',
        'Parabéns! Você acertou todas as formas! Muito bem!',
        'Parabéns! Você encontrou todas as formas! Que observador!',
        'Parabéns! Você pintou todas as formas! Que artista!',
    ]
    form_cel_en = [
        'Congratulations! You know all the shapes! So smart!',
        'Congratulations! You got all the shapes right! Great job!',
        'Congratulations! You found all the shapes! So observant!',
        'Congratulations! You painted all the shapes! What an artist!',
    ]
    for pt, en in zip(form_cel_pt, form_cel_en):
        add('pt', 'formas', pt)
        add('en', 'shapes', en)

    # ─── LETRAS ───
    # PT: usa nome por extenso (Á, Bê, Cê...) — TTS pt-BR fala corretamente
    # EN: usa a LETRA sozinha (A, B, C...) — TTS en lê a letra corretamente
    #     NÃO usar nomes por extenso (Ei, Bi, Si) pois o TTS lê como palavra
    for letter, pt_name in zip(LETTERS, LETTERS_NAMES_PT):
        add('pt', 'letras', pt_name)
        add('en', 'letters', letter)
        add('pt', 'letras', f'{pt_name}!')
        add('en', 'letters', f'{letter}!')
        # "Qual é o A?" / "Where is the A?"
        add('pt', 'letras', f'Qual é o {letter}?')
        add('en', 'letters', f'Where is the {letter}?')

    add('pt', 'letras', 'Qual letra é essa?')
    add('en', 'letters', 'What letter is this?')

    # Pintar letras
    for pt_c, en_c in zip(PAINT_COLORS_PT, PAINT_COLORS_EN):
        add('pt', 'letras', f'Pinte de {pt_c.lower()}!')
        add('en', 'letters', f'Paint it {en_c.lower()}!')

    let_cel_pt = [
        'Parabéns! Você conhece todas as letras! Que criança esperta!',
        'Parabéns! Você pintou todas as letras! Que artista!',
        'Parabéns! Você acertou todas as letras! Que esperto!',
    ]
    let_cel_en = [
        'Congratulations! You know all the letters! What a smart child!',
        'Congratulations! You painted all the letters! What an artist!',
        'Congratulations! You got all the letters right! So smart!',
    ]
    for pt, en in zip(let_cel_pt, let_cel_en):
        add('pt', 'letras', pt)
        add('en', 'letters', en)

    # ─── ENCORAJAMENTOS (compartilhados) ───
    for pt, en in zip(ENCOURAGE_PT, ENCOURAGE_EN):
        add('pt', 'geral', pt)
        add('en', 'general', en)

    return phrases


def _slugify(text):
    """Converte texto para slug de arquivo."""
    s = text.lower().strip()
    # Remove pontuação
    s = re.sub(r'[!?¿¡.,;:\'"""()…]', '', s)
    # Acentos comuns -> base
    replacements = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e', 'í': 'i', 'ó': 'o',
        'ô': 'o', 'õ': 'o', 'ú': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n',
    }
    for old, new in replacements.items():
        s = s.replace(old, new)
    # Espaços -> underscore
    s = re.sub(r'\s+', '_', s)
    # Remove caracteres restantes que não sejam alfanumericos ou _
    s = re.sub(r'[^a-z0-9_]', '', s)
    # Limita tamanho
    return s[:60]


def _plural_pt(word):
    """Pluralização simplificada para português."""
    if word.endswith('ão'):
        return word[:-2] + 'ões'
    if word.endswith('l'):
        return word[:-1] + 'is'
    return word + 's'


def _ensure_wav(path):
    """Converte arquivo de áudio para WAV 22050Hz mono se necessário."""
    if path.lower().endswith('.wav'):
        return path
    wav_path = os.path.splitext(path)[0] + '_converted.wav'
    if os.path.exists(wav_path):
        return wav_path
    try:
        from pydub import AudioSegment
        print(f"  Convertendo {os.path.basename(path)} -> WAV 22kHz mono...")
        audio = AudioSegment.from_file(path)
        audio = audio.set_frame_rate(22050).set_channels(1)
        audio.export(wav_path, format='wav')
        print(f"  Convertido: {wav_path}")
        return wav_path
    except Exception as e:
        print(f"  ERRO ao converter {path}: {e}")
        print(f"  Tente instalar ffmpeg: winget install Gyan.FFmpeg")
        sys.exit(1)


def generate_audio(phrases, sample_path, output_dir, test_mode=False):
    """Gera arquivos de áudio usando XTTS-v2.

    sample_path pode ser:
      - Um arquivo único (ex: audio/sample_mae.wav) -> usado para PT e EN
      - Caminho base sem extensão -> tenta sample_mae_pt.wav e sample_mae_en.wav
        Se só encontrar o PT, usa ele para ambos (cross-language cloning)
    """

    try:
        from TTS.api import TTS as CoquiTTS
    except ImportError:
        print("ERRO: Coqui TTS não instalado.")
        print("Execute: pip install TTS")
        sys.exit(1)

    try:
        from pydub import AudioSegment
    except ImportError:
        print("ERRO: pydub não instalado.")
        print("Execute: pip install pydub")
        sys.exit(1)

    # Resolve amostra(s) de voz — aceita 1 arquivo ou 2 separados por idioma
    samples = {}
    if os.path.exists(sample_path):
        # Arquivo único -> usa para ambos
        samples['pt'] = sample_path
        samples['en'] = sample_path
        print(f"Amostra unica: {sample_path} (usada para PT e EN)")
    else:
        # Tenta variantes por idioma em vários locais
        search_patterns = []
        base, ext = os.path.splitext(sample_path)
        for lang_code in ['pt', 'en']:
            lang_names = {
                'pt': ['portugues', 'pt', 'portuguese'],
                'en': ['ingles', 'en', 'english', 'eng'],
            }
            found = False
            # Padrão original: sample_mae_pt.wav etc
            for try_ext in [ext, '.wav', '.m4a', '.mp3', '.mp4', '.ogg']:
                candidate = f"{base}_{lang_code}{try_ext}"
                if os.path.exists(candidate):
                    samples[lang_code] = candidate
                    found = True
                    break
            if found:
                continue
            # Busca em audiosmae/ com nomes como audiomaeportugues.mp4
            for folder in ['audiosmae', 'audiomae']:
                if not os.path.isdir(folder):
                    continue
                for f in os.listdir(folder):
                    fl = f.lower()
                    if any(name in fl for name in lang_names[lang_code]):
                        samples[lang_code] = os.path.join(folder, f)
                        found = True
                        break
                if found:
                    break

        if 'pt' not in samples and 'en' not in samples:
            print(f"ERRO: Nenhuma amostra de voz encontrada.")
            print(f"  Tentei: {sample_path}")
            print(f"  Tentei: {base}_pt.wav, {base}_en.wav, etc.")
            print(f"  Tentei: audiosmae/audiomae*.mp4")
            print(f"\nColoque a amostra em uma dessas opcoes:")
            print(f"  audio/sample_mae.wav          (arquivo unico)")
            print(f"  audio/sample_mae_pt.wav       (so portugues)")
            print(f"  audiosmae/audiomaeportugues.mp4 + audiosmae/audiomaeingles.mp4")
            sys.exit(1)

        # Se só tem um idioma, usa para o outro (cross-language cloning)
        if 'pt' in samples and 'en' not in samples:
            samples['en'] = samples['pt']
            print(f"Amostra PT: {samples['pt']}")
            print(f"Amostra EN: usando PT (cross-language cloning)")
        elif 'en' in samples and 'pt' not in samples:
            samples['pt'] = samples['en']
            print(f"Amostra EN: {samples['en']}")
            print(f"Amostra PT: usando EN (cross-language cloning)")
        else:
            print(f"Amostra PT: {samples['pt']}")
            print(f"Amostra EN: {samples['en']}")

    # Converte amostras para WAV se necessário (MP4, M4A, etc.)
    for lang_key in list(samples.keys()):
        samples[lang_key] = _ensure_wav(samples[lang_key])

    print("\nCarregando modelo XTTS-v2 (primeira vez faz download de ~2GB)...")
    tts = CoquiTTS("tts_models/multilingual/multi-dataset/xtts_v2")

    # Cria diretórios
    os.makedirs(os.path.join(output_dir, 'pt'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'en'), exist_ok=True)

    manifest = {'pt': {}, 'en': {}}
    total = sum(len(v) for v in phrases.values())
    done = 0
    errors = []

    if test_mode:
        # Em modo teste, pega só 5 frases de cada idioma
        test_phrases = {'pt': {}, 'en': {}}
        for lang in ['pt', 'en']:
            items = list(phrases[lang].items())[:5]
            test_phrases[lang] = dict(items)
        phrases = test_phrases
        total = sum(len(v) for v in phrases.values())
        print(f"\n=== MODO TESTE: gerando {total} frases ===\n")

    lang_map = {'pt': 'pt', 'en': 'en'}

    for lang in ['pt', 'en']:
        for text, slug in phrases[lang].items():
            done += 1
            wav_path = os.path.join(output_dir, lang, f"{slug.split('/')[-1]}.wav")
            mp3_path = os.path.join(output_dir, lang, f"{slug.split('/')[-1]}.mp3")
            rel_path = f"audio/{lang}/{slug.split('/')[-1]}.mp3"

            # Pula se já existe
            if os.path.exists(mp3_path):
                print(f"  [{done}/{total}] SKIP (ja existe): {text[:40]}")
                manifest[lang][text] = rel_path
                continue

            print(f"  [{done}/{total}] {lang.upper()}: {text[:50]}...")

            try:
                tts.tts_to_file(
                    text=text,
                    speaker_wav=samples[lang],
                    language=lang_map[lang],
                    file_path=wav_path,
                )

                # Converte WAV -> MP3
                audio = AudioSegment.from_wav(wav_path)
                audio.export(mp3_path, format='mp3', bitrate='128k')
                os.remove(wav_path)  # Remove WAV para economizar espaço

                manifest[lang][text] = rel_path
            except Exception as e:
                errors.append((lang, text, str(e)))
                print(f"    ERRO: {e}")

    # Salva manifest
    manifest_path = os.path.join(output_dir, 'manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Geração concluída!")
    print(f"  Sucessos: {done - len(errors)}")
    print(f"  Erros:    {len(errors)}")
    print(f"  Manifest: {manifest_path}")

    if errors:
        print(f"\nFrases com erro:")
        for lang, text, err in errors:
            print(f"  [{lang}] {text}: {err}")

    return manifest


def main():
    parser = argparse.ArgumentParser(description='Mafinho Explora — Voice Generator')
    parser.add_argument('--test', action='store_true', help='Gera apenas 5 frases de teste por idioma')
    parser.add_argument('--list', action='store_true', help='Lista todas as frases sem gerar áudio')
    parser.add_argument('--sample', default='audio/sample_mae.wav', help='Caminho da amostra de voz (default: audio/sample_mae.wav). Aceita .wav, .mp4, .m4a, .mp3')
    parser.add_argument('--output', default='audio', help='Diretório de saída (default: audio/)')
    args = parser.parse_args()

    # Muda para o diretório do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    phrases = build_phrase_list()

    if args.list:
        for lang in ['pt', 'en']:
            print(f"\n{'='*50}")
            print(f"  {lang.upper()} — {len(phrases[lang])} frases")
            print(f"{'='*50}")
            for text, slug in sorted(phrases[lang].items()):
                print(f"  {slug:50s} = {text}")
        total = sum(len(v) for v in phrases.values())
        print(f"\nTotal: {total} frases ({len(phrases['pt'])} PT + {len(phrases['en'])} EN)")
        return

    generate_audio(phrases, args.sample, args.output, test_mode=args.test)


if __name__ == '__main__':
    main()
