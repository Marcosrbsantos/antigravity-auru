# Diretriz: Configuração do Supabase (Antigravity)

Esta diretriz define o processo de configuração do backend no Supabase.

## Objetivos
- Configurar a estrutura de dados relacional.
- Garantir a privacidade (RLS) entre diferentes núcleos familiares.
- Preparar o ambiente para o processamento de IA.

## Passos de Execução

1. **SQL Editor**:
   - Copie o conteúdo de `execution/schema.sql`.
   - Execute no painel SQL do Supabase.
   - Verifique se as extensões (uuid-ossp) foram habilitadas.

2. **Storage**:
   - Crie um bucket chamado `receipts`.
   - Configure a política de acesso:
     - `INSERT`: Apenas usuários autenticados.
     - `SELECT`: Apenas usuários do mesmo `household_id`.

3. **Authentication**:
   - Configure os provedores desejados.
   - Adicione o Trigger de perfil automático se necessário.

## Regras de Ouro
- Nunca desabilite o RLS em tabelas de produção.
- Todas as transações DEVEM estar vinculadas a um `household_id`.
