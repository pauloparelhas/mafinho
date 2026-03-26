---
name: project_status
description: Status atual e backlog dos jogos do Mafinho Explora — atualizar após cada entrega
type: project
---

# STATUS DO PROJETO — MAFINHO EXPLORA
**Atualizado:** 24/03/2026

---

## Fase 2 — Estado atual dos módulos

| Módulo | Arquivo | Jogos implementados | Status |
|---|---|---|---|
| Colors | colors.html | Flashcard + Clicar + Arrastar | COMPLETO |
| Numbers | numbers.html | Contar + Flashcard + Clicar + Arrastar | COMPLETO |
| Animals | animals.html | Flashcard + Clicar + Arrastar (silhueta) | COMPLETO |
| Shapes | shapes.html | Flashcard + Clicar + Encontrar + Pintar | COMPLETO |
| Letters | letters.html | Flashcard + Pintar + Clicar | COMPLETO |
| Emotions | emotions.html | Flashcard + Clicar + Encontrar | COMPLETO |
| Body | body.html | — | EM ANDAMENTO |
| Objects | — | — | Não iniciado |
| Days | — | — | Não iniciado |

**Shared:** `base.css` + `base.js` (design system + MF/TTS/Nav/SFX)
**Hub:** `index.html`
**Site:** https://pauloparelhas.github.io/mafinho/

---

## Módulo em andamento: Corpo Humano (body.html)

**Plano:** 3 jogos
1. **Flashcard** — close-up de cada parte, TTS fala o nome
2. **Tocar** — figura completa + hotspots invisíveis, "onde está o nariz?"
3. **Montar** — assembly click-to-place, silhueta guia + chips de partes

**Partes do corpo (12):** cabeça, cabelo, olho, nariz, boca, orelha, pescoço, barriga, braço, mão, perna, pé

**Assets:** PNG via Gemini API (generate_images.py) — 13 imagens (1 full body + 12 partes)

**Progresso:**
- [x] Pré-trabalho: base.js atualizado (MF.GAMES com 'body')
- [ ] image_manifest.json — adicionar bloco "body"
- [ ] Rodar generate_images.py body
- [ ] HTML estático
- [ ] CSS
- [ ] JS dados (PARTS + LANG)
- [ ] JS FlashGame
- [ ] JS TocaGame
- [ ] JS AssemblyGame
- [ ] QA + commit

---

## Backlog futuro

| Tópico | Arquivo | Jogos previstos |
|--------|---------|----------------|
| Objects (🧸) | objects.html | Flashcard + Clicar + Arrastar |
| Days (📅) | days.html | Flashcard + Sequência |
| Body v2 | body.html | Músculos, ossos (futuro) |
| Colors | colors.html | Separar (4º jogo) |

---

## Decisões técnicas ativas

- btnVoice (TTS mãe) removido de todos os módulos — feature não implementada
- base.js voiceMode default = 'sistema'
- animals.html flashcards usam fundo pastel (SVGs kawaii ficavam ilegíveis em fundo forte)
- emotions.html: 2 chars (boy/girl) × 4 emoções = 8 SVGs kawaii standalone
- body.html: PNG via Gemini (sem SVG) — hotspots por coordenadas % sobre imagem full.png

---

## GitHub

- **Repo:** https://github.com/pauloparelhas/mafinho
- **Site:** https://pauloparelhas.github.io/mafinho/
- **Branch:** master
