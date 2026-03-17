# MAFINHO EXPLORA — ÍNDICE DE MEMÓRIAS
**Criado:** 09/03/2026 | **Fase 2:** 16/03/2026

---

## CONTEXTO GERAL
- **Projeto:** Jogos exploratórios para criança de 2 anos (Mafinho)
- **Escola:** Maple Bear (bilíngue PT/EN — bandeira 🇨🇦 para inglês)
- **Filosofia:** Tudo mais simples — alvos grandes, cores óbvias, sem frustração
- **Fase 2:** Iniciada em 16/03/2026 com padrão consultoriagamer aplicado

---

## MEMÓRIAS

| Arquivo | Tipo | Descrição |
|---------|------|-----------|
| [project_status.md](project_status.md) | projeto | Backlog e status dos jogos |
| [PADRAO.md](PADRAO.md) | referência | Padrões e anti-padrões descobertos |

---

## TÓPICOS DO PROJETO

| Tópico | Fase 1 (legado) | Fase 2 (novo padrão) | Status |
|--------|-----------------|----------------------|--------|
| Cores | cores.html | colors.html ✅ | Flashcard pronto |
| Números | numeros.html | — | Hub fase 1 |
| Animais | animais.html | — | Hub fase 1 |
| Formas | formas.html | — | Hub fase 1 |
| Objetos | objetos.html | — | Hub fase 1 |
| Dias da Semana | dias_semana.html | — | Hub fase 1 |

---

## REGRAS FIXAS DE DESIGN (JAMAIS VIOLAR)

- Fonte mínima: 1.2rem (escalada pela var --fs)
- Botões navbar e jogo: mínimo **80px** (fase 2 — era 54px na fase 1)
- Alvos de toque: mínimo 80×80px para toda interação
- Cores: apenas tons distintos (um azul, um verde — nunca dois verdes)
- Navbar fase 2: 7 botões — 🏠 ↩ ◀ ▶ [espaço] 🌙 🔊 🔒
- Idioma: 🇧🇷 Português / 🇨🇦 Inglês (Maple Bear)
- localStorage: mf-theme, mf-font, mf-lang, mf-sound (prefixo "mf-")
- Progresso por jogo: chave "{topico}_progresso"
