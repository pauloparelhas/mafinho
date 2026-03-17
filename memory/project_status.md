---
name: project_status
description: Status atual e backlog dos jogos do Mafinho Explora — atualizar após cada entrega
type: project
---

# STATUS DO PROJETO — MAFINHO EXPLORA
**Atualizado:** 17/03/2026

---

## Fase 2 — Novo padrão profissional

### Concluído (Fase 2)
- [x] 16/03/2026 — `colors.html` — Cores: Flashcard + Arrastar + **Clicar** (3 jogos prontos)
- [x] 16/03/2026 — `numbers.html` — Números: **Contar** (contagem sincronizada TTS+animação, 1-5)
- [x] 16/03/2026 — `index.html` — Hub atualizado: Cores e Números ativos, demais "Em breve"
- [x] 16/03/2026 — GitHub Pages publicado: https://pauloparelhas.github.io/mafinho/
- [x] 16/03/2026 — `CLAUDE.md` v2.0 — Protocolo atualizado
- [x] 16/03/2026 — `.claude/agents/` — 4 agentes criados
- [x] 17/03/2026 — `base.css` v2.1 — Reescrito com todo CSS compartilhado extraído de colors+numbers
- [x] 17/03/2026 — `base.js` v2.1 — Reescrito: MF, TTS(+speakExcitedAndWait), SFX, Nav, shuffle/delay
- [x] 17/03/2026 — `colors.html` refatorado — importa base.css+base.js (-514 linhas)
- [x] 17/03/2026 — `numbers.html` refatorado + contar 1-10 — importa base.css+base.js (-488 linhas)
- [x] 17/03/2026 — Números: voz empolgada na resposta, answerPop animation, intervalo reduzido

### Backlog (ordenado por prioridade)
| # | Arquivo | Tipo | Tópico | Status |
|---|---------|------|--------|--------|
| 1 | numbers.html | Flashcard, Clicar, Arrastar | Números — jogos | pendente |
| 2 | colors.html | Separar | Cores — nível 4 | pendente |
| 3 | animals.html | hub + jogos | Animais | pendente |
| 4 | shapes.html | hub + jogos | Formas | pendente |
| 5 | objects.html | hub + jogos | Objetos | pendente |
| 6 | days.html | hub + jogos | Dias da Semana | pendente |

### Detalhes do design — Números
- **Contar (1-10):** contagem sincronizada (TTS fala + objeto destaca), 2 velocidades (🐢/🐇), shuffle, pergunta retórica "Que número é esse?" → resposta empolgada após 0.8s com answerPop
- **Resposta:** apenas o nome do número ("Três!") com voz empolgada (rate 0.72, pitch 1.35) + animação de ampliação no dígito
- **Objetos:** temática masculina (⚽🚀✈️🦖🚗🚁⛵🦸‍♂️🏀🚲🤖🦁🏎️🏍️)
- **Flashcard/Clicar/Arrastar:** serão mais memorização, sem contagem animada

### Detalhes do design — Cores (Clicar)
- Sem círculo de referência; enunciado textual "Aperte na cor [Nome]!" com destaque colorido
- TTS fala comando completo; X tremendo cômico no erro; 3.5s entre acertos
- Feedback: SFX erro (bwooop engraçado) + SFX acerto (Dó-Mi-Sol)

---

## GitHub
- **Repo:** https://github.com/pauloparelhas/mafinho
- **Site:** https://pauloparelhas.github.io/mafinho/
- **Branch:** master, push automático sem pedir senha
- **Proteção:** .gitignore exclui .claude/, credenciais, .env
