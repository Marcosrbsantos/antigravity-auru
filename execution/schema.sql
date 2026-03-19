-- Antigravity: Core Schema (Supabase) - Versão Simplificada e Robusta

-- 1. EXTENSÕES
create extension if not exists "uuid-ossp";

-- 2. TABELAS (Sem políticas ainda)
create table if not exists public.households (
  id uuid primary key default uuid_generate_v4(),
  created_at timestamp with time zone default now()
);

create table if not exists public.profiles (
  id uuid references auth.users not null primary key,
  household_id uuid references public.households(id),
  display_name text,
  avatar_url text,
  created_at timestamp with time zone default now()
);

create table if not exists public.transactions (
  id uuid primary key default uuid_generate_v4(),
  household_id uuid references public.households(id),
  user_id uuid references public.profiles(id),
  description text,
  amount decimal(12,2),
  category_type text check (category_type in ('fixa', 'variavel', 'online', 'mercado')),
  is_income boolean default false,
  purchase_date date default current_date,
  receipt_url text,
  ai_rating text check (ai_rating in ('Barato', 'Mediano', 'Caro', 'Pendente')),
  raw_ai_data jsonb,
  created_at timestamp with time zone default now()
);

create table if not exists public.inventory_items (
  id uuid primary key default uuid_generate_v4(),
  transaction_id uuid references public.transactions(id) on delete cascade,
  product_name text,
  barcode text,
  unit_price decimal(12,2),
  market_avg_price decimal(12,2),
  created_at timestamp with time zone default now()
);

-- 3. HABILITAR SEGURANÇA (RLS)
alter table public.households enable row level security;
alter table public.profiles enable row level security;
alter table public.transactions enable row level security;
alter table public.inventory_items enable row level security;

-- 4. POLÍTICAS DE ACESSO (Simples para funcionar de primeira)

-- Profiles: O usuário pode ver e editar o próprio perfil
create policy "Ver próprio perfil" on public.profiles for select using (auth.uid() = id);
create policy "Editar próprio perfil" on public.profiles for update using (auth.uid() = id);

-- Households: O usuário pode ver o household se estiver vinculado a ele no perfil
create policy "Ver próprio household" on public.households for select 
using ( id in (select household_id from public.profiles where id = auth.uid()) );

-- Transactions: Tudo baseado no household_id do usuário
create policy "Gerenciar transações do household" on public.transactions for all
using ( household_id in (select household_id from public.profiles where id = auth.uid()) );

-- Items: Baseado na transação
create policy "Ver itens do household" on public.inventory_items for select
using ( transaction_id in (select id from public.transactions where household_id in (select household_id from public.profiles where id = auth.uid())) );
