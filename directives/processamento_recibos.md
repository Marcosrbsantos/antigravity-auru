# Diretriz: Processamento de Recibos com Llama 3 (Groq)

Esta diretriz define o fluxo de inteligência "fricção zero" para extração e análise de dados de compras.

## Fluxo de Trabalho

1. **Trigger de Entrada**:
   - O App faz o upload da imagem para o Supabase Storage.
   - A URL da imagem é passada para o pipeline de processamento.

2. **Extração com Llama 3 (via Groq)**:
   - **Prompt**: "Atue como um especialista em varejo brasileiro. Extraia: Nome do estabelecimento, Data, Valor Total, Itens (Nome, Preço, GTIN/Barcode). Identifique se é uma conta de consumo (Luz/Água) ou cupom fiscal."
   - **Formato**: JSON estrito.

3. **Enriquecimento e Comparação**:
   - Se houver GTIN/Barcode, realizar busca em APIs de preço (Menor Preço, Google Shopping).
   - Calcular `varedito`: 
     - "Barato" (abaixo da média).
     - "Mediano" (na média).
     - "Caro" (mais de 10% acima da média).

4. **Persistência**:
   - Salvar os dados na tabela `transactions`.
   - Salvar os itens na tabela `inventory_items`.

## Ferramentas Necessárias
- API do Groq configurada no `.env`.
- Script de execução `execution/process_receipt.py` (a ser desenvolvido).
