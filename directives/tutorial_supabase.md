# Tutorial Passo a Passo: Configuração do Supabase (Antigravity)

Este guia foi feito para quem está começando do zero. Siga cada passo para deixar seu ERP pessoal pronto.

## 1. Criar sua conta e projeto
1. Acesse [supabase.com](https://supabase.com) e crie uma conta (pode usar o GitHub).
2. Clique em **"New Project"**.
3. Escolha um nome (ex: `Antigravity`), uma senha para o banco de dados (guarde bem!) e a região mais próxima (ex: `Sao Paulo`).
4. Aguarde alguns minutos enquanto o Supabase prepara seu ambiente.

## 2. Criar as Tabelas e Segurança (SQL)
1. No menu lateral esquerdo, clique no ícone que parece um terminal: **"SQL Editor"**.
2. Clique em **"New Query"**.
3. Abra o arquivo `execution/schema.sql` no seu computador e copie todo o conteúdo.
4. Cole no editor do Supabase e clique no botão **"Run"** (ou aperte `Ctrl + Enter`).
5. Você verá a mensagem "Success. No rows returned". Suas tabelas e regras de segurança (RLS) estão criadas!

## 3. Configurar o Armazenamento de Fotos (Storage)
1. No menu lateral, clique no ícone de balde: **"Storage"**.
2. Clique em **"New Bucket"**.
3. Nomeie o bucket como `receipts` (exatamente assim).
4. Mantenha como **"Private"** (a segurança já está configurada via SQL).
5. Clique em **"Save"**.

## 4. Obter suas chaves de acesso
1. No menu lateral, clique na engrenagem: **"Project Settings"**.
2. Clique em **"API"**.
3. Você verá dois campos importantes:
   - **Project URL**: Copie este endereço.
   - **anon public**: Copie esta chave (clique em "Reveal" se necessário).

## 5. Configurar seu arquivo .env
1. Volte aqui para o seu editor de código.
2. Abra o arquivo `.env`.
3. Cole a URL no campo `SUPABASE_URL=`.
4. Cole a chave pública no campo `SUPABASE_KEY=`.

## O que foi feito?
- **Tabelas**: Agora você tem onde salvar transações e itens.
- **RLS**: Apenas você e sua esposa (profiles no mesmo household) podem ver seus dados.
- **Storage**: Espaço pronto para receber as fotos dos cupons fiscais.

---
**Dúvidas?** Basta me perguntar qualquer passo que não tenha ficado claro!
