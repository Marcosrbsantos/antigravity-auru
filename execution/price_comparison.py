import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Usaremos a API do Google Search (via Serper ou similar) ou um buscador direto
# Para este MVP, vamos simular a busca ou usar uma URL de busca direta
# O usuário mencionou Serper API.

SERPER_API_KEY = os.environ.get("SERPER_API_KEY")

def get_market_price(product_name, gtin=None):
    """
    Busca o preço médio de mercado para um produto.
    Prioriza o GTIN se disponível.
    """
    query = gtin if gtin else product_name
    print(f"Buscando preço para: {query}...")
    
    # Mock de busca por enquanto (será integrado com Serper se houver chave)
    # Exemplo de lógica real:
    # url = "https://google.serper.dev/shopping"
    # payload = json.dumps({"q": query, "gl": "br", "hl": "pt-br"})
    # headers = {'X-API-KEY': SERPER_API_KEY, 'Content-Type': 'application/json'}
    # response = requests.request("POST", url, headers=headers, data=payload)
    
    # Preços mockados baseados em categorias comuns para teste
    mock_prices = {
        "1234567890123": 22.50, # Arroz deveria custar 22.50
        "7891020304050": 9.20   # Feijão deveria custar 9.20
    }
    
    return mock_prices.get(gtin, 10.00) # Retorna 10.00 como fallback

if __name__ == "__main__":
    # Teste
    p1 = get_market_price("Arroz 5kg", "1234567890123")
    print(f"Preço de mercado: R$ {p1:.2f}")
