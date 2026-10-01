# Guia de implementação — Talhe com login e banco de dados

Este guia parte do zero: você não precisa saber programar pra seguir os
passos, só ir copiando/colando o que está indicado. Reserve uns 30-40
minutos na primeira vez.

---

## Visão geral do que você vai montar

- **Supabase** guarda os dados (empresas, usuários, pedidos, peças) e cuida
  do login.
- **Vercel** hospeda o site (o que o vendedor/gestor acessa pelo navegador).
- Os dois são gratuitos pra começar.

Hierarquia de acesso: **Gestor** (cria vendedores, vê todos os pedidos da
empresa) → **Vendedor** (vê só os pedidos que ele mesmo criou).

---

## Passo 1 — Criar o projeto no Supabase

1. Vá em [supabase.com](https://supabase.com) e crie uma conta (dá pra
   entrar com GitHub).
2. Clique em **New Project**.
3. Escolha um nome (ex: `talhe`), uma senha de banco (guarde essa senha
   em algum lugar seguro — só é pedida em raras situações) e a região mais
   próxima (`South America (São Paulo)`).
4. Aguarde uns 2 minutos enquanto o Supabase prepara o projeto.

## Passo 2 — Rodar o SQL que cria as tabelas

1. No painel do Supabase, no menu à esquerda, clique em **SQL Editor**.
2. Clique em **New query**.
3. Abra o arquivo `supabase-schema.sql` (está na raiz deste projeto),
   copie **todo o conteúdo** e cole nessa tela.
4. Clique em **Run** (ou Ctrl+Enter).
5. Deve aparecer "Success. No rows returned" — isso significa que as
   tabelas `empresas`, `perfis`, `pedidos` e `pecas` foram criadas, junto
   com as regras de segurança que isolam os dados por empresa.

Se der algum erro, o mais comum é ter rodado o SQL duas vezes (as tabelas
já existem). Nesse caso, apague as tabelas pelo **Table Editor** e rode de
novo.

## Passo 3 — Pegar as chaves de API

1. No menu à esquerda, vá em **Project Settings → API**.
2. Você vai precisar de três valores nesta tela:
   - **Project URL** (ex: `https://abcdefgh.supabase.co`)
   - **anon public** (uma chave longa) — essa é pública, pode ficar no
     código do site
   - **service_role** (outra chave longa) — essa é **secreta**, nunca pode
     aparecer no código do site, só em configuração de servidor

## Passo 4 — Configurar as variáveis de ambiente

### Pra rodar no seu computador (opcional, só se for testar local)

1. Na raiz do projeto, copie o arquivo `.env.example` e renomeie a cópia
   pra `.env.local`.
2. Preencha:
   ```
   VITE_SUPABASE_URL=https://abcdefgh.supabase.co
   VITE_SUPABASE_ANON_KEY=a-chave-anon-que-você-copiou
   ```
3. Rode `npm install` e depois `npm run dev`.

### Na Vercel (pra funcionar no site publicado)

1. No painel da Vercel, entre no seu projeto → **Settings → Environment
   Variables**.
2. Adicione três variáveis:

   | Nome | Valor | Onde pegar |
   |---|---|---|
   | `VITE_SUPABASE_URL` | sua Project URL | Passo 3 |
   | `VITE_SUPABASE_ANON_KEY` | sua chave anon | Passo 3 |
   | `SUPABASE_SERVICE_ROLE_KEY` | sua chave service_role | Passo 3 |

3. Depois de salvar, vá em **Deployments**, clique nos "..." do último
   deploy e escolha **Redeploy** (as variáveis novas só valem a partir do
   próximo deploy).

⚠️ A `SUPABASE_SERVICE_ROLE_KEY` é a única realmente secreta das três —
ela é usada só dentro da função `api/criar-vendedor.js`, que roda no
servidor da Vercel, nunca no navegador da pessoa.

## Passo 5 — Subir o projeto pro GitHub e conectar na Vercel

Se ainda não fez isso:

```bash
git init
git add .
git commit -m "sistema com login e banco de dados"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/NOME-DO-REPO.git
git push -u origin main
```

Depois, em [vercel.com](https://vercel.com): **Add New → Project** →
escolha o repositório → **Deploy**. Depois do primeiro deploy, volte e
configure as variáveis de ambiente do Passo 4, e faça um **Redeploy**.

## Passo 6 — Testar o fluxo completo

1. Abra o site publicado.
2. Clique em **"criar empresa"**.
3. Preencha nome da empresa, um código curto (ex: `stand-rj`), seu nome,
   e-mail e senha. Clique em **criar empresa**.
4. Você cai direto na lista de pedidos, como gestor.
5. Clique em **vendedores** → crie um vendedor de teste (nome + senha).
6. Saia (**sair**) e entre de novo, agora na aba **vendedor**, usando o
   código da empresa + nome do vendedor + a senha que você definiu.
7. Crie um pedido de teste, adicione uma peça, clique em **salvar
   pedido**.
8. Saia e entre de novo como **gestor** — o pedido do vendedor deve
   aparecer na lista.

Se todos esses passos funcionarem, o sistema está de pé.

---

## Como bloquear/liberar uma empresa (controle de pagamento)

Por enquanto isso é manual, direto no Supabase — e está tudo bem ser assim
no início:

1. No Supabase, vá em **Table Editor → empresas**.
2. Encontre a empresa desejada.
3. Edite a coluna `status_assinatura` pra `bloqueado` (ou `atrasado`).
4. Da próxima vez que alguém daquela empresa tentar entrar, vai ver a tela
   de "acesso bloqueado".
5. Pra liberar de novo, volte o valor pra `ativo`.

Quando fizer sentido automatizar isso com uma plataforma de pagamento
(Asaas, Iugu, Stripe), é só essa mesma coluna que vai passar a ser
atualizada automaticamente por um webhook, em vez de você editar à mão.

---

## Confirmação de e-mail e recuperação de senha

Essas duas já estão implementadas:

- **Confirmação de e-mail**: ao criar a empresa, o gestor recebe um link de
  confirmação. Só depois de clicar nele é que a empresa é criada de
  verdade no banco (antes disso a pessoa ainda não está autenticada, então
  o sistema guarda os dados digitados temporariamente no navegador e
  termina de criar a empresa assim que o link é confirmado).
- **Recuperação de senha**: na tela de login, aba "gestor", tem o link
  "esqueci minha senha", que envia um e-mail com link de redefinição.

Isso já está pronto no código, mas o Supabase precisa de um ajuste de
configuração pra funcionar direito com o domínio do seu site publicado:

1. No Supabase, vá em **Authentication → URL Configuration**.
2. Em **Site URL**, coloque a URL do seu site na Vercel (ex:
   `https://talhe.vercel.app`).
3. Em **Redirect URLs**, adicione a mesma URL.

Sem isso, os links dos e-mails de confirmação/recuperação podem apontar
pra `localhost` em vez do seu site publicado.

⚠️ Login de **vendedor** usa um e-mail interno inventado (não é um e-mail
de verdade), então recuperação de senha por e-mail não se aplica a ele.
Se um vendedor esquecer a senha, por enquanto o jeito é o gestor recriar o
acesso dele (apagar e cadastrar de novo em **Vendedores**). Redefinir a
senha de um vendedor direto, sem recriar a conta, é uma melhoria que dá
pra fazer depois.


## Limitações restantes (pra você ter ciência)

Nenhuma dessas impede de testar o sistema agora — são pontos pra revisar
antes de vender pra outras marmorarias:

- **Papel do usuário no cadastro**: hoje, tecnicamente, alguém com
  conhecimento técnico poderia tentar se cadastrar direto como "gestor"
  sem passar pela tela de cadastro normal. Pra uma versão comercial, vale
  reforçar essa regra no banco. Posso ajudar nisso quando for a hora.
- **Redefinir senha de vendedor**: só dá pra recriar o acesso, não
  redefinir a senha existente (ver seção acima).
- **Painel do dono do SaaS**: hoje "o dono" (você) gerencia as empresas
  clientes direto pelo painel do Supabase (Table Editor). Uma tela própria
  pra isso é um passo natural mais pra frente.
- **Sem backups automáticos**: o plano gratuito do Supabase não faz backup
  sozinho. Antes de ter clientes pagantes de verdade, vale considerar o
  plano pago (que inclui backup) ou configurar um backup manual periódico.
