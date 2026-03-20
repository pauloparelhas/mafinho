# Aperfeicoamento de Governanca — Padroes Estruturantes
**Origem:** Projeto Mafinho Explora (jogos educativos, HTML/CSS/JS puro)
**Destino:** Projeto de estudo para provas (crianca de 7 anos)
**Objetivo:** Adotar os padroes que fazem sentido para melhorar navegacao, modularidade, reuso e escalabilidade

---

## 1. ARQUITETURA DE ARQUIVOS COMPARTILHADOS

### Problema que resolve
Cada pagina repete CSS e JS identicos, dificultando manutencao e gerando inconsistencia visual.

### Padrao recomendado
```
projeto/
  index.html          <- hub principal de navegacao
  base.css             <- design system compartilhado (cores, tipografia, navbar, componentes)
  base.js              <- sistema compartilhado (tema, som, navegacao, utilitarios)
  modulo_historia.html <- um arquivo por modulo/topico
  modulo_geografia.html
  ...
```

### Como funciona
- **`base.css`** define variaveis CSS (`:root`), reset, navbar, botoes, modais, animacoes
- **`base.js`** define objetos globais reutilizaveis (tema, navegacao entre telas, TTS)
- Cada pagina de modulo importa ambos e define apenas CSS/JS especifico do modulo

```html
<!-- Em cada modulo -->
<link rel="stylesheet" href="base.css"/>
<script src="base.js"></script>
<style>/* apenas CSS especifico deste modulo */</style>
<script>/* apenas logica especifica deste modulo */</script>
```

**Beneficio:** Mudar a navbar, o tema ou qualquer componente global = editar 1 arquivo = reflete em todos os modulos.

---

## 2. SISTEMA DE NAVEGACAO PADRONIZADO

### Navbar padrao (adaptar para o contexto de estudo)
```html
<nav class="navbar">
  <button id="btnHome" class="nav-btn btn-home" onclick="goHome()">icone_casa</button>
  <span class="nav-title" id="navTitle">Titulo do Modulo</span>
  <span style="flex:1"></span>
  <button id="btnTheme" class="nav-btn btn-theme" onclick="toggleTheme()">icone_tema</button>
</nav>
```

**Regras:**
- Todo botao com `id=` (facilita QA e automacao)
- Tamanho minimo de toque: 48px+ (adaptar para a idade — 7 anos precisa menos que 2 anos)
- Navbar sticky no topo, sempre visivel
- Botao Home abre menu de navegacao entre modulos (nao redireciona direto)

### Navegacao entre telas (SPA-like)
Em vez de multiplos arquivos HTML por sub-pagina, usar **telas show/hide** dentro do mesmo arquivo:

```javascript
const Nav = {
  _screens: [],
  boot(screens) {
    this._screens = screens;
    screens.forEach(id => document.getElementById(id).style.display = 'none');
    document.getElementById(screens[0]).style.display = 'flex';
  },
  show(id) {
    this._screens.forEach(s => {
      document.getElementById(s).style.display = (s === id) ? 'flex' : 'none';
    });
  }
};
```

**Beneficio:** Transicoes instantaneas, sem recarregar pagina, sem quebrar links, funciona offline com `file://`.

### Menu cross-modulo
Registrar todos os modulos num array central:

```javascript
const MODULES = [
  { id: 'historia', icon: 'icone', name: 'Historia', href: 'historia.html' },
  { id: 'geografia', icon: 'icone', name: 'Geografia', href: 'geografia.html' },
  // ...
];
```

O botao Home mostra um modal com grid de modulos, destacando o atual. Permite navegar entre modulos sem voltar ao index.

---

## 3. DESIGN SYSTEM COM VARIAVEIS CSS

```css
:root {
  /* Paleta — adaptar para o projeto */
  --primary: #1E88E5;
  --success: #43A047;
  --danger:  #E53935;
  --warning: #F9A825;

  /* Superficies */
  --bg: #F8F9FA;
  --surface: #FFFFFF;
  --text: #212121;
  --muted: #757575;
  --border: #DEE2E6;

  /* Tipografia escalavel */
  --fs: 1;
  --sm: calc(1rem * var(--fs));
  --md: calc(1.25rem * var(--fs));
  --lg: calc(1.75rem * var(--fs));
  --xl: calc(2.2rem * var(--fs));

  /* Componentes */
  --btn-h: 48px;
  --rad: 12px;
}

/* Tema escuro */
[data-theme="dark"] {
  --bg: #0F0F1A;
  --surface: #1A1A2E;
  --text: #F5F5F5;
  --muted: #9E9E9E;
  --border: #33335A;
}
```

**Beneficio:** Tema claro/escuro com um toggle. Fonte escalavel. Consistencia visual total.

---

## 4. PERSISTENCIA COM localStorage

Padroes do Mafinho que funcionam bem:

| Chave | Tipo | Uso |
|-------|------|-----|
| `app-theme` | `'light'` / `'dark'` | Tema persistente |
| `app-font` | `float` | Escala de fonte |
| `{modulo}_progresso` | `JSON` | Progresso por modulo |

**Regras:**
- Chave com prefixo unico por modulo (evita colisao)
- Salvar progresso ao completar cada etapa (nao apenas ao final)
- Leitura no `init()` de cada pagina

---

## 5. ESTRUTURA INTERNA DE UM MODULO

Cada modulo (ex: `historia.html`) segue este esqueleto:

```
Tela 1: Hub do modulo (lista de atividades disponiveis)
Tela 2: Conteudo/Estudo (material de leitura, video, resumo)
Tela 3: Exercicio/Quiz (perguntas interativas)
Tela 4: Resultado/Celebracao (feedback do desempenho)
```

Todas as telas sao `<div>` no mesmo HTML, controladas por `Nav.show()`.

---

## 6. PROTOCOLO DE QA

Antes de declarar qualquer modulo pronto:

- [ ] Navegacao: Home, voltar, avancar — todos funcionam
- [ ] Tema escuro funciona sem quebrar layout
- [ ] Progresso salva e restaura corretamente
- [ ] Funciona offline (file://) ou no GitHub Pages
- [ ] Responsivo: testado em 360px e 768px
- [ ] Sem scroll horizontal em nenhuma tela
- [ ] Todos os botoes sao clicaveis (sem sobreposicao)

---

## 7. INTEGRACAO COM NotebookLM — MODULO DE HISTORIA

### Estrategia: Usar NotebookLM como fabrica de conteudo, Claude como montador

O objetivo e gerar conteudo rico (resumos, videos, podcasts) no NotebookLM sem consumir tokens no Claude, e depois integrar esses assets no site.

### Fluxo de trabalho

```
1. Claude gera prompts/scripts otimizados para NotebookLM
2. Voce cola no NotebookLM e gera os subprodutos
3. Voce salva os assets (audio, texto, links) na pasta do projeto
4. Claude monta o modulo HTML integrando esses assets
```

### 7.1 — Geracao de resumos estruturados

**Prompt para colar no NotebookLM (adaptar por capitulo):**

```
Voce e um professor de historia para crianca de 7 anos no Brasil.
Resuma o seguinte conteudo em linguagem simples, com:
- Maximo 5 paragrafos curtos
- Palavras-chave em destaque
- 3 perguntas de revisao ao final (multipla escolha, 3 opcoes cada)
- Tom amigavel e encorajador

Conteudo:
[COLAR AQUI o texto do livro/apostila/capitulo]
```

**O que fazer com o resultado:**
- Salvar como `historia/cap1_resumo.json` ou `.txt`
- Claude monta a tela de estudo usando esse conteudo

### 7.2 — Geracao de podcasts/audio explicativo

**Prompt para NotebookLM Audio Overview:**

```
Crie uma conversa entre dois apresentadores explicando para uma crianca de 7 anos:
- Topico: [nome do capitulo]
- Pontos-chave: [lista de 3-5 pontos]
- Duracao desejada: 3-5 minutos
- Tom: divertido, com exemplos do dia-a-dia
- Incluir uma pergunta para a crianca pensar no final
```

**O que fazer com o resultado:**
- Baixar o audio gerado pelo NotebookLM
- Salvar como `historia/audio/cap1_podcast.mp3`
- Claude integra com player HTML5:

```html
<div class="audio-player">
  <audio id="podcastPlayer" src="historia/audio/cap1_podcast.mp3"></audio>
  <button onclick="document.getElementById('podcastPlayer').play()">
    Ouvir explicacao
  </button>
</div>
```

### 7.3 — Geracao de quizzes

**Prompt para colar no NotebookLM:**

```
Baseado neste conteudo, gere um quiz em formato JSON com:
- 5 perguntas de multipla escolha
- 3 opcoes por pergunta (a, b, c)
- Campo "correct" com a letra certa
- Campo "explanation" com explicacao curta da resposta
- Dificuldade: 2o ano do fundamental

Formato esperado:
[
  {
    "question": "Pergunta aqui?",
    "options": { "a": "Opcao A", "b": "Opcao B", "c": "Opcao C" },
    "correct": "b",
    "explanation": "Porque..."
  }
]

Conteudo:
[COLAR AQUI]
```

**O que fazer com o resultado:**
- Salvar como `historia/quizzes/cap1.json`
- Claude usa o JSON para montar o quiz interativo no HTML

### 7.4 — Geracao de linhas do tempo visuais

**Prompt para NotebookLM:**

```
Crie uma linha do tempo simplificada sobre [topico] com:
- Maximo 6 eventos
- Cada evento com: ano, titulo curto (5 palavras max), descricao (1 frase)
- Ordem cronologica
- Formato JSON:
[
  { "year": "1500", "title": "Chegada ao Brasil", "desc": "Os portugueses chegaram de navio" }
]
```

**O que fazer com o resultado:**
- Salvar como `historia/timelines/cap1.json`
- Claude renderiza como componente visual interativo (timeline horizontal scrollavel)

### 7.5 — Videos via NotebookLM

Se o NotebookLM gerar videos ou links de video:
- Salvar o link/embed
- Claude integra com iframe ou player nativo
- Fallback: thumbnail clicavel que abre em nova aba

---

## 8. ESTRUTURA DE PASTAS SUGERIDA PARA HISTORIA

```
projeto/
  index.html
  base.css
  base.js
  historia.html          <- modulo principal (hub + telas de estudo + quiz)
  historia/
    resumos/
      cap1.json          <- resumo gerado pelo NotebookLM
      cap2.json
    quizzes/
      cap1.json          <- quiz gerado pelo NotebookLM
      cap2.json
    audio/
      cap1_podcast.mp3   <- podcast gerado pelo NotebookLM
    timelines/
      cap1.json          <- linha do tempo gerada
    assets/
      imagens/           <- ilustracoes, mapas, etc.
```

---

## 9. FLUXO COMPLETO DE CRIACAO DE UM CAPITULO

```
Passo 1: Identificar conteudo-fonte (livro, apostila, anotacao)
Passo 2: Claude gera prompts otimizados para NotebookLM (resumo + quiz + audio)
Passo 3: Voce cola cada prompt no NotebookLM e salva os outputs
Passo 4: Voce coloca os arquivos nas pastas corretas
Passo 5: Claude monta/atualiza historia.html integrando os novos assets
Passo 6: QA rapido (navegacao, conteudo, responsivo)
Passo 7: Commit e deploy
```

**Economia de tokens:** Os passos 2 e 5 usam Claude. Os passos 3 e 4 sao manuais no NotebookLM (zero tokens). O conteudo pesado (resumos, quizzes, audios) e gerado fora do Claude.

---

## 10. REGRAS GERAIS DE GOVERNANCA

1. **Um arquivo HTML por modulo/materia** — contem hub + todas as atividades
2. **CSS e JS compartilhados em `base.css` e `base.js`** — nunca duplicar
3. **Dados separados do codigo** — quizzes, resumos e timelines em JSON
4. **Progresso persistente** — localStorage com chave unica por modulo
5. **Tema claro/escuro** — toggle global, persistente
6. **Navegacao padronizada** — navbar + menu de modulos + telas show/hide
7. **Mobile-first** — tudo funciona em 360px
8. **Offline-first** — funciona com `file://` e GitHub Pages
9. **QA antes de entregar** — checklist minimo sempre
10. **Commits granulares** — um commit por mudanca funcional, mensagem clara

---

*Documento gerado a partir dos padroes do Projeto Mafinho Explora.*
*Adaptar livremente ao contexto do projeto de estudo — nem tudo precisa ser adotado de uma vez.*
