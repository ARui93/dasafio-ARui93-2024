-- ========================================================
-- MARMORIX — Schema do banco (Supabase / Postgres)
-- Cole este arquivo inteiro no SQL Editor do Supabase e rode.
-- ========================================================

-- Extensão pra gerar IDs únicos (geralmente já vem ativada no Supabase)
create extension if not exists "pgcrypto";

-- ---------- EMPRESAS (cada marmoraria cliente) ----------
create table empresas (
  id uuid primary key default gen_random_uuid(),
  nome text not null,
  codigo text not null unique, -- código curto usado no login do vendedor, ex: "stand-rj"
  status_assinatura text not null default 'ativo', -- ativo | atrasado | bloqueado
  criado_em timestamptz not null default now()
);

-- ---------- PERFIS (liga um login à empresa e ao papel) ----------
-- O id aqui é o MESMO id do usuário em auth.users (1 pra 1).
create table perfis (
  id uuid primary key references auth.users(id) on delete cascade,
  empresa_id uuid not null references empresas(id) on delete cascade,
  nome text not null,
  papel text not null default 'vendedor', -- gestor | vendedor
  criado_em timestamptz not null default now()
);

-- ---------- PEDIDOS ----------
create table pedidos (
  id uuid primary key default gen_random_uuid(),
  empresa_id uuid not null references empresas(id) on delete cascade,
  vendedor_id uuid not null references perfis(id),
  numero_pedido text,
  cliente text,
  endereco text,
  prazo text,
  vendedor_nome text,
  criado_em timestamptz not null default now(),
  atualizado_em timestamptz not null default now()
);

-- ---------- PEÇAS (cada retângulo dentro de um pedido) ----------
create table pecas (
  id uuid primary key default gen_random_uuid(),
  pedido_id uuid not null references pedidos(id) on delete cascade,
  posicao text,
  material text,
  quantidade int default 1,
  largura numeric,
  profundidade numeric,
  x numeric default 0,
  y numeric default 0,
  rotacao int default 0,
  lados jsonb,
  nao_desenhar boolean default false,
  tem_cuba boolean default false,
  cuba_tipo text,
  cuba_largura numeric,
  cuba_profundidade numeric,
  cuba_pos_x numeric,
  tem_cooktop boolean default false,
  cooktop_largura numeric,
  cooktop_profundidade numeric,
  cooktop_pos_x numeric,
  tem_rebaixo boolean default false,
  rebaixo_tipo text,
  rebaixo_largura numeric,
  rebaixo_profundidade numeric,
  rebaixo_pos_x numeric
);

-- ========================================================
-- FUNÇÕES AUXILIARES (pra usar dentro das regras de segurança)
-- ========================================================

create or replace function minha_empresa()
returns uuid
language sql security definer stable
as $$
  select empresa_id from perfis where id = auth.uid();
$$;

create or replace function meu_papel()
returns text
language sql security definer stable
as $$
  select papel from perfis where id = auth.uid();
$$;

-- ========================================================
-- REGRAS DE SEGURANÇA (Row Level Security)
-- Isso é o que garante que uma empresa nunca vê dado de outra,
-- e que um vendedor só vê os próprios pedidos.
-- ========================================================

alter table empresas enable row level security;
alter table perfis enable row level security;
alter table pedidos enable row level security;
alter table pecas enable row level security;

-- EMPRESAS: só vê a própria empresa
create policy "ver_propria_empresa" on empresas
  for select using (id = minha_empresa());

-- Qualquer pessoa recém-cadastrada pode criar UMA empresa (isso é o
-- "criar conta" do gestor). Depois disso ela já vira dona daquela empresa.
create policy "criar_empresa_no_cadastro" on empresas
  for insert with check (auth.uid() is not null);

-- PERFIS: vê o próprio perfil; gestor vê todos os perfis da empresa dele
create policy "ver_perfis" on perfis
  for select using (
    id = auth.uid()
    or (meu_papel() = 'gestor' and empresa_id = minha_empresa())
  );

-- Usuário recém-cadastrado cria o próprio perfil (bootstrap do gestor)
create policy "criar_proprio_perfil" on perfis
  for insert with check (id = auth.uid());

-- PEDIDOS: vendedor vê só os seus; gestor vê todos da empresa
create policy "ver_pedidos" on pedidos
  for select using (
    empresa_id = minha_empresa()
    and (meu_papel() = 'gestor' or vendedor_id = auth.uid())
  );

create policy "criar_pedidos" on pedidos
  for insert with check (
    empresa_id = minha_empresa() and vendedor_id = auth.uid()
  );

create policy "editar_pedidos" on pedidos
  for update using (
    empresa_id = minha_empresa()
    and (meu_papel() = 'gestor' or vendedor_id = auth.uid())
  );

create policy "apagar_pedidos" on pedidos
  for delete using (
    empresa_id = minha_empresa()
    and (meu_papel() = 'gestor' or vendedor_id = auth.uid())
  );

-- PEÇAS: seguem a visibilidade do pedido a que pertencem
create policy "ver_pecas" on pecas
  for select using (pedido_id in (select id from pedidos));

create policy "criar_pecas" on pecas
  for insert with check (pedido_id in (select id from pedidos));

create policy "editar_pecas" on pecas
  for update using (pedido_id in (select id from pedidos));

create policy "apagar_pecas" on pecas
  for delete using (pedido_id in (select id from pedidos));

-- ========================================================
-- MIGRAÇÃO (só rode isso se você já tinha rodado o schema
-- antes e criou as tabelas sem as colunas de rebaixo)
-- ========================================================
-- alter table pecas add column if not exists tem_rebaixo boolean default false;
-- alter table pecas add column if not exists rebaixo_tipo text;
-- alter table pecas add column if not exists rebaixo_largura numeric;
-- alter table pecas add column if not exists rebaixo_profundidade numeric;
-- alter table pecas add column if not exists rebaixo_pos_x numeric;
