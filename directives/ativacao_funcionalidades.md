# Estratégia de Ativação das Funcionalidades

Para o app funcionar na Vercel, precisamos de uma ponte entre o HTML e o Python.

## 1. Backend (Vercel Functions)
Criaremos uma pasta `api/` com scripts `.py`. A Vercel executará isso como APIs.
- `api/upload.py`: Recebe a imagem, sobe no Supabase e retorna os dados via Groq.

## 2. Frontend (App.js)
Substituiremos os `alert()` por chamadas `fetch()` para a nossa API.

## 3. Segurança & Env
Você precisará colocar suas chaves (GROQ, SUPABASE) no painel da Vercel.

## 4. Banco de Dados
Lerei as transações diretamente do Supabase para que Maria Izabel e Marcos vejam os mesmos dados.
