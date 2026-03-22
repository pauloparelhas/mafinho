# CLAUDE.md — Mafinho Explora
## Jogos Educativos para Criança de 2 Anos
**Versão:** 2.1 | 22/03/2026 — Fase Profissional Estruturada

---

## PROTOCOLO DE TRABALHO — INVIOLÁVEL

**ANTES de implementar qualquer coisa: analisar → propor → aguardar aprovação → só então executar.**

O usuário decide. Claude propõe e executa quando autorizado. Nunca assumir aprovação implícita.

---

## CONTEXTO DO PROJETO

**Projeto:** Mafinho Explora — Jogos exploratórios para criança de 2 anos
**Público:** Criança de 2 anos (Mafinho), celular/tablet com supervisão do pai (Marcelo)
**Escola:** Maple Bear (bilíngue PT/EN — bandeira 🇨🇦 para inglês)
**Objetivo:** Alegria e prazer em aprender — NUNCA frustração.

**Princípios pedagógicos para 2 anos:**
- Informações grandes, claras, com muito espaço visual
- Uma única ação por tela (tap, arrastar, ou ouvir — nunca os três ao mesmo tempo)
- Feedback imediato, positivo e exagerado (animação, som, elogio)
- Sem texto de instrução — só imagens, sons e símbolos universais
- Sem timer — criança explora no próprio ritmo
- Errar não é ruim — animação de "tente de novo" SEM penalização
- Ciclo curto: não mais de 5 interações por rodada, então celebração

---

## MODO PLANEJAMENTO — ATIVAR AO INICIAR SESSÃO NOVA

Na primeira mensagem de cada sessão, Claude DEVE:
1. Invocar `Agent(subagent_type="gerente")` para retomar contexto
2. Apresentar: o que foi feito, o que está pendente, sugestão de próxima ação
3. Aguardar aprovação antes de implementar qualquer coisa

---

## AGENTES OBRIGATÓRIOS

Os agentes ficam em `.claude/agents/`. São invocados com `Agent(subagent_type="nome")`.

| Momento | Agente | O que faz |
|---|---|---|
| Início de sessão | `gerente` | Retoma contexto, lista tarefas, coordena |
| Antes de codar | `pedagogico` | Valida design para 2 anos, calibra dificuldade |
| Antes de declarar pronto | `ti` | DOM trace, mental render 360px, checklist completo |
| Após entregar | `arquivista` | Atualiza memory/, verifica estrutura |

**NUNCA declarar jogo como "pronto" sem rodar o agente `ti` antes.**
**NUNCA começar a codar sem rodar o agente `pedagogico` antes.**

---

## ARQUITETURA DO PROJETO

### Stack
- HTML5 + CSS3 + JavaScript puro (vanilla) — zero framework
- Compartilhados: `base.css` + `base.js` (importados por todos os jogos fase 2)
- Build: nenhum — abrir direto no navegador (file://)
- Fonte: Comic Sans MS (sistema) + Nunito (Google Fonts, assíncrono opcional)

### Estrutura de arquivos esperada
```
app_marcelo/
├── CLAUDE.md                    ← este arquivo
├── index.html                   ← hub de navegação principal
├── base.css                     ← design system compartilhado (fase 2)
├── base.js                      ← MF system: lock, theme, TTS, navbar, som
├── memory/
│   ├── MEMORY.md                ← índice de memórias
│   ├── project_status.md        ← status e backlog
│   └── PADRAO.md                ← padrões e anti-padrões descobertos
├── .claude/
│   └── agents/
│       ├── gerente.md
│       ├── pedagogico.md
│       ├── ti.md
│       └── arquivista.md
├── colors.html                  ← FASE 2 — padrão profissional (referência)
├── cores.html                   ← fase 1 (legado, mantido)
├── numeros.html, animais.html... ← hubs fase 1
└── _games/
    └── flashcard.html           ← template de referência
```

**Regra:** Novos jogos seguem `colors.html` como template, não `cores.html`.

---

## NAVBAR PADRÃO — FASE 2

```html
<nav class="navbar">
  <button id="navLogo"  onclick="goToIndex()">🏠</button>
  <button id="btnHome"  onclick="confirmHome()">↩</button>
  <button id="btnPrev"  onclick="prevPhase()">◀</button>
  <button id="btnNext"  onclick="nextPhase()">▶</button>
  <span style="flex:1"></span>
  <button id="themeBtn" onclick="MF.toggleTheme()">🌙</button>
  <button id="soundBtn" onclick="MF.toggleSound()">🔊</button>
  <button id="lockBtn"  onclick="MF.handleLock()">🔒</button>
</nav>
```

**Regras dos botões:**
- Todo botão com `id=` (facilita QA e automação)
- Tamanho mínimo: **80px × 80px** (fase 2 — era 54px na fase 1)
- Ícones grandes, sem texto
- `confirmHome()`: modal pergunta ao PAI se quer sair (criança não entende texto)
- `handleLock()`: 1º clique trava (fullscreen + bloqueia nav), 2º mostra overlay de desbloqueio
- `btnPrev` / `btnNext`: ocultos (`visibility:hidden`) quando fora do jogo

---

## PROTOCOLO QA OBRIGATÓRIO

### Passo 1 — INTENT
- QUEM vai usar? (criança sozinha? com pai?)
- O QUE deve acontecer em cada interação?
- POR QUE? A criança de 2 anos vai entender sem instrução verbal?

### Passo 2 — DOM TRACE
1. Ler HTML estático
2. Ler JS que gera/modifica o DOM
3. Identificar relação pai-filho REAL
4. SÓ ENTÃO definir CSS

**Regra:** NUNCA mexer em CSS sem verificar qual JS gera o DOM.

### Passo 3 — MENTAL RENDER em 360px
- Elemento X: posição, tamanho — alvo de toque ≥ 80px?
- Há sobreposição? Texto cortado?
- Tudo visível sem scroll?

### Passo 4 — USER FLOW do Toddler
- "Criança vê a tela → o que chama atenção primeiro? → ela vai querer tocar? → o que acontece?"
- "Criança erra → há animação de incentivo? → sem som de fracasso?"
- "Criança acerta → há celebração exagerada? → ela quer jogar de novo?"
- "Pai entrega o celular → tela está travada? → criança não sai do jogo por acidente?"

---

## CHECKLIST PRÉ-ENTREGA

- [ ] Uma única ação por tela
- [ ] Todo alvo de toque ≥ 80px (incluindo navbar)
- [ ] Sem texto de instrução — só imagens, sons e símbolos
- [ ] Feedback positivo imediato ao acerto (animação + TTS)
- [ ] Feedback neutro ao erro — SEM som de fracasso, SEM X vermelho agressivo
- [ ] Ciclo curto: máximo 5 interações por rodada, então celebração
- [ ] Sem timer
- [ ] Randomização: nova rodada = sequência diferente
- [ ] `confirmHome()` com modal para o pai (NÃO para a criança)
- [ ] Lock mode implementado (`handleLock()`)
- [ ] TTS fala no idioma ativo (mf-lang)
- [ ] Som toggle funcional (`toggleSound()`, persiste em localStorage)
- [ ] Tudo visível na tela em 360px — sem scroll durante o jogo
- [ ] `goToIndex()` aponta para `index.html`
- [ ] localStorage key única: `{topico}_progresso`
- [ ] btnPrev / btnNext visíveis durante o jogo, ocultos no hub
- [ ] Celebração após completar todas as fases
- [ ] Layout mobile-first testado mentalmente em 360px

---

## REGRA CRÍTICA — ARQUIVOS GRANDES E AGENTES

**NUNCA delegar a escrita de arquivo HTML/JS completo para um agente.**

Agentes têm limite de output. Arquivos de jogos têm 300–800 linhas. Um agente trunca silenciosamente.

**Regra inviolável:**
- Arquivos com mais de 300 linhas: escrever do contexto principal (Write tool), em partes
- Agentes só revisam/validam — nunca escrevem
- Salvar após cada parte completada
- Commit após cada mudança funcional

**Granularidade obrigatória:**
1. Estrutura HTML (cabeçalho, navbar, containers)
2. CSS (variáveis, layout, telas)
3. JS — dados e inicialização
4. JS — lógica do jogo
5. JS — feedback e animações
6. Teste mental QA
7. Commit

Perguntar ao usuário após cada parte antes de continuar.

---

## REGRA DE DOCUMENTAÇÃO — INVIOLÁVEL

**Documentação desatualizada é INACEITÁVEL.** Arquivos-chave (`CLAUDE.md`, `memory/MEMORY.md`, `memory/project_status.md`) DEVEM refletir o estado real do projeto a todo momento.

**Quando atualizar (ANTES de encerrar qualquer entrega):**
- Após cada commit que altera estado de módulos ou jogos
- Após corrigir bug causado por padrão errado
- Após implementar feature que vira padrão
- Antes de passar para o próximo jogo
- Ao final de TODA sessão, mesmo que só tenha havido limpeza/refactor

**O que atualizar:**
1. `memory/project_status.md` — tabela de módulos, jogos, status (fonte de verdade)
2. `memory/MEMORY.md` — índice de memórias + tabela resumo de módulos
3. Este `CLAUDE.md` — seção ESTADO ATUAL + checklist se houver novos padrões
4. `memory/PADRAO.md` — novo padrão ou anti-padrão (se aplicável)

**Regra para agentes:**
- O agente `arquivista` DEVE ser invocado após cada entrega para validar que toda documentação está atualizada
- O agente `gerente` DEVE ler `memory/project_status.md` como fonte de verdade ao retomar sessão
- Se qualquer agente detectar documentação desatualizada, deve ALERTAR imediatamente antes de prosseguir

---

## ESTADO ATUAL DO PROJETO (atualizar a cada commit)

**Última atualização:** 22/03/2026

| Módulo | Arquivo | Jogos implementados | Status |
|---|---|---|---|
| Colors | colors.html | Flashcard + Clicar + Arrastar | COMPLETO |
| Numbers | numbers.html | Contar + Flashcard + Clicar + Arrastar | COMPLETO |
| Animals | animals.html | Flashcard + Clicar + Arrastar (silhueta) | COMPLETO |
| Shapes | shapes.html | Flashcard + Clicar + Encontrar + Pintar | COMPLETO |
| Letters | letters.html | Flashcard + Pintar + Clicar | COMPLETO |
| Emotions | emotions.html | Flashcard + Clicar + Encontrar | 3 jogos |
| Objects | — | — | Não iniciado |
| Days | — | — | Não iniciado |

**Shared:** `base.css` + `base.js` (design system + MF/TTS/Nav/SFX)
**Hub:** `index.html` (navegação entre tópicos)

**Decisões técnicas ativas:**
- btnVoice (TTS mãe) removido de todos os módulos — feature não implementada
- base.js `voiceMode` default = `'sistema'`
- animals.html flashcards usam fundo pastel (SVGs kawaii sobre fundo forte ficam ilegíveis)
- emotions.html: 2 chars (boy/girl) × 4 emoções = 8 SVGs kawaii standalone

---

## SISTEMA DE DESIGN — REFERÊNCIA RÁPIDA

```css
/* Paleta (8 cores distintas, sem tons similares) */
--c-red: #E53935;  --c-blue: #1E88E5;  --c-yellow: #F9A825;
--c-green: #43A047; --c-orange: #FB8C00; --c-purple: #8E24AA;
--c-pink: #E91E63; --c-teal: #00897B;

/* Tipografia (escalada por --fs) */
--sm: calc(1.2rem * var(--fs));   --md: calc(1.55rem * var(--fs));
--lg: calc(2.1rem * var(--fs));   --xl: calc(2.7rem * var(--fs));
--2xl: calc(3.4rem * var(--fs));

/* Componentes — FASE 2: tudo ≥80px */
--btn-h: 80px;  --btn-hsm: 80px;  --rad: 18px;  --radlg: 26px;
```

**localStorage:**
| Chave | Valores | Descrição |
|-------|---------|-----------|
| mf-theme | 'light'/'dark' | Tema |
| mf-font | 0.7–1.5 | Escala de fonte |
| mf-lang | 'pt'/'en' | Idioma |
| mf-sound | 'on'/'off' | Som |
| {topico}_progresso | JSON | Progresso por jogo |

---

## O QUE NÃO FAZER

- NÃO entregar rápido e errado — melhor demorar e acertar
- NÃO tratar sintoma CSS sem investigar causa raiz no JS/DOM
- NÃO usar agente de revisão com prompt vago
- NÃO delegar escrita de arquivo >300 linhas para agente
- NÃO adicionar texto onde emoji/imagem resolve
- NÃO usar som de fracasso ou X vermelho agressivo para erro
- NÃO assumir que criança de 2 anos entende instrução de texto
- NÃO fazer tela com scroll — tudo deve caber em 360px
- NÃO reduzir botões abaixo de 80px (fase 2 aumentou o mínimo)
- NÃO começar a codar sem rodar agente `pedagogico`
- NÃO declarar pronto sem rodar agente `ti`
- NÃO encerrar sessão ou entrega com documentação desatualizada (CLAUDE.md, MEMORY.md, project_status.md)
- NÃO assumir que documentação de sessões anteriores está correta — verificar antes de usar

---

---

## BACKLOG FUTURO

### Jogos pendentes
- Emotions: jogos adicionais (Arrastar? a definir com usuário)
- Colors: Separar (4º jogo, completaria o tópico)
- Objects (🧸): tópico novo — vocabulário do dia-a-dia
- Dias da Semana (📅): tópico novo — conceito temporal básico

### Configurações customizáveis
- **Bandeira do idioma EN**: atualmente fixa 🇨🇦 (Maple Bear). Futuro: permitir configurar para 🇺🇸, 🇬🇧, etc. via `localStorage('mf-en-flag')` ou config JSON.
- **Registro de jogos**: centralizado em `MF.GAMES` (base.js). Novos jogos devem ser adicionados lá para aparecerem automaticamente no menu de navegação.

### Estrutura de assets escalável
```
app_marcelo/
├── img/
│   ├── animals/     ← PNGs 512x512 gerados por svg_animals.py
│   ├── shapes/      ← (futuro) PNGs de formas
│   └── objects/     ← (futuro) PNGs de objetos
├── svg_animals.py   ← pipeline SVG→PNG (PyMuPDF)
```
- SVGs inline nos HTMLs para carregamento rápido, PNGs como fallback/export
- PyMuPDF NÃO suporta `<radialGradient>` / `<linearGradient>` — usar shapes sólidas sobrepostas

---

*Baseado na sistematica do Projeto Serafina (Maple Bear Y2) e adaptado para criança de 2 anos.*
*Fase 2 iniciada em 16/03/2026 — padrão de referência: `colors.html`.*
