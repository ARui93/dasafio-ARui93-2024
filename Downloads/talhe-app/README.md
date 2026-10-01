# Talhe — Gerador de desenho técnico

> **Login e banco de dados**: veja o [GUIA-IMPLEMENTACAO.md](./GUIA-IMPLEMENTACAO.md)
> pro passo a passo completo de configuração do Supabase (login, multi-empresa,
> bloqueio de acesso).

Protótipo em React + Vite. Fora do ambiente de teste do Claude, o botão de
**imprimir** funciona normalmente (sem as limitações do preview de artifact).

## 1. Rodar localmente (pra testar antes de publicar)

Pré-requisito: [Node.js](https://nodejs.org) instalado (versão 18 ou mais recente).

```bash
npm install
npm run dev
```

Abre em `http://localhost:5173`.

## 2. Subir pro GitHub

```bash
git init
git add .
git commit -m "primeira versão do Talhe"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/NOME-DO-REPO.git
git push -u origin main
```

## 3. Publicar na Vercel (recomendado)

### Opção A — pelo site da Vercel (mais simples, sem terminal)

1. Cria uma conta em [vercel.com](https://vercel.com) (dá pra entrar direto com o GitHub)
2. Clica em **Add New → Project**
3. Escolhe o repositório que você acabou de subir (passo 2)
4. A Vercel já detecta sozinha que é um projeto Vite — não precisa mudar nada nas configurações
5. Clica em **Deploy**

Em cerca de 1 minuto o site fica no ar num link tipo:

```
https://nome-do-repo.vercel.app
```

A partir daí, **todo `git push` pra branch `main` atualiza o site sozinho**,
sem precisar repetir nenhum passo.

### Opção B — pelo terminal (Vercel CLI)

```bash
npm install -g vercel
vercel login
vercel --prod
```

Na primeira vez ele faz algumas perguntas (nome do projeto, pasta, etc.) —
pode aceitar as respostas padrão.

### Domínio próprio

Depois de publicado, em **Project Settings → Domains** dá pra ligar um
domínio próprio da empresa (tipo `talhe.com.br`) em vez do link
`.vercel.app`.

## Alternativa: GitHub Pages

Se preferir usar o GitHub Pages em vez da Vercel:

1. Abra `vite.config.js` e troque `base: "/"` por `base: "/NOME-DO-REPO/"`
   (tem que bater com o nome do repositório do passo 2)
2. Rode:
   ```bash
   npm install
   npm run deploy
   ```
3. Em **Settings → Pages** no GitHub, escolha a branch `gh-pages` como fonte

O site fica em `https://SEU-USUARIO.github.io/NOME-DO-REPO/`. Diferente da
Vercel, aqui é preciso rodar `npm run deploy` manualmente a cada atualização
(a menos que configure uma GitHub Action pra isso).

## Estrutura do projeto

- `src/App.jsx` — todo o sistema (formulário, prancha, impressão)
- `src/main.jsx` — ponto de entrada que monta o App
- `index.html` — página HTML base
- `vite.config.js` — configuração de build
- `vercel.json` — configuração de build específica da Vercel

## Observação sobre dados

Este protótipo não tem banco de dados nem login — tudo fica só na memória
do navegador enquanto a página está aberta. Ao atualizar/fechar a página,
os dados preenchidos se perdem. Isso é esperado nesta fase de protótipo.
