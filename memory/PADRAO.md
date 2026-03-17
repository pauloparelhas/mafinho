---
name: PADRAO
description: Padrões e anti-padrões descobertos no desenvolvimento do Mafinho Explora
type: reference
---

# PADRÕES E ANTI-PADRÕES — MAFINHO EXPLORA
**Atualizado:** 16/03/2026

---

## Padrões Estabelecidos (FAZER)

### P01 — Sistema MF em base.js
**Padrão:** Funções de tema, fonte, idioma, som e lock centralizadas em `base.js` (objeto MF).
Todos os jogos fase 2 importam `base.js` e chamam `MF.init()` no carregamento.
**Why:** Mudança em uma função reflete em todos os jogos automaticamente.
**How to apply:** `<script src="base.js"></script>` antes do script de jogo. Chamar `MF.init()` no final.

### P02 — Uma tela por vez (showScreen)
**Padrão:** Cada arquivo tem múltiplas `<section id="sXxx">`. Apenas uma tem class `active` (display:flex). As outras têm display:none.
Função `showScreen('sNome')` gerencia visibilidade e estado do btnPrev/btnNext.
**How to apply:** Sempre usar `showScreen()` para transições — nunca modificar display diretamente em outro lugar.

### P03 — Botões ≥80px em toda a interface (Fase 2)
**Padrão:** `--btn-h: 80px` e `--btn-hsm: 80px` em base.css. Todo botão usa essas variáveis.
**Why:** Fase 1 usava 54px para navbar — insuficiente para dedo de toddler (fase 2 corrigiu).
**How to apply:** Nunca definir height de botão < 80px. Nunca usar valor absoluto — usar a variável.

### P04 — Shuffle em nova rodada
**Padrão:** `deck = shuffle([...DADOS])` no início de cada nova rodada.
**Why:** Criança não se entedia com sequência sempre igual.
**How to apply:** Implementar `function shuffle(arr)` em cada arquivo de jogo (ou exportar de base.js).

### P05 — TTS fala no idioma ativo
**Padrão:** `MF.speak(texto, lang)` usa Web Speech API. `lang` vem de `document.documentElement.dataset.lang`.
**Why:** TTS no idioma errado é confuso e deseducativo.
**How to apply:** Sempre passar o texto no idioma correto E o lang code. Ex: `MF.speak(c.pt, 'pt')` ou `MF.speak(c.en, 'en')`.

### P06 — Hook de idioma para re-render do jogo
**Padrão:** Sobrescrever `MF.applyLang` em cada arquivo de jogo para re-renderizar o card ativo ao trocar idioma.
**Why:** O `MF.applyLang()` do base.js atualiza apenas elementos com `data-pt`. Textos dinâmicos (nomes dos cards) precisam de re-render manual.
**How to apply:** Ver implementação em `colors.html` — padrão `_origApplyLang`.

### P07 — localStorage com prefixo único por jogo
**Padrão:** `{topico}_progresso` para progresso de jogo. Chaves globais usam prefixo `mf-`.
**Why:** Evita colisão entre jogos.
**How to apply:** `colors_progresso`, `numbers_progresso`, etc.

---

## Anti-Padrões (NUNCA FAZER)

### AP01 — Botões menores que 80px
**Problema:** Criança não consegue tocar; cria frustração imediata.
**Correção:** Usar `height: var(--btn-h)` e `min-width: var(--btn-h)` em todo botão.

### AP02 — Scroll durante o jogo
**Problema:** Criança de 2 anos não sabe scrollar; perde contexto.
**Correção:** Toda tela de jogo deve caber em 360px altura sem scroll. Medir mentalmente antes de entregar.

### AP03 — Feedback punitivo
**Problema:** Som de erro, X vermelho, flash vermelho → frustração e choro.
**Correção:** Erro = elemento volta ao neutro silenciosamente. Acerto = celebração exagerada.

### AP04 — Dois tons do mesmo matiz
**Problema:** Criança não diferencia verde-claro de verde-escuro — confusão cognitiva.
**Correção:** Uma única cor por matiz. Usar apenas a paleta de 8 cores definida em base.css.

### AP05 — Instrução sem emoji correspondente
**Problema:** Criança de 2 anos não lê texto de instrução verbal.
**Correção:** Cada instrução deve ter emoji/ícone universal. Ex: "Toque para ouvir 👆🔊".

### AP06 — Agente escrevendo arquivo >300 linhas
**Problema:** Agentes truncam output silenciosamente → arquivo incompleto/quebrado.
**Correção:** Arquivos grandes SEMPRE escritos do contexto principal com Write tool, em partes.

### AP07 — Review com prompt vago
**Problema:** "Verifique se o CSS está correto" não produz feedback útil.
**Correção:** "Trace o JS que gera o DOM. Simule render em 360px. Verifique alvos ≥80px e sobreposições."

### AP09 — Arquivos externos em jogos (base.css / base.js via link/script src)
**Problema:** `<link href="base.css">` e `<script src="base.js">` não carregam via `file://` no celular (browser bloqueia por segurança). Sem base.css o layout desaparece. Sem base.js o `MF` é undefined e o JS crasha — tela em branco.
**Correção:** Todo arquivo de jogo deve ser **autocontido** — CSS e JS inline no mesmo `.html`. Os arquivos `base.css` e `base.js` existem como referência de desenvolvimento, mas o conteúdo deve ser copiado/inlined no HTML de cada jogo.
**Aprendido em:** 16/03/2026 — colors.html não funcionou no celular do Marcelo.

### AP08 — Confirmar saída com a criança (não o pai)
**Problema:** Criança toca em qualquer coisa — modal de confirmação deve ser para o PAI ler.
**Correção:** `confirmHome()` exibe "Sair do jogo?" em texto claro para adulto, não para criança.
