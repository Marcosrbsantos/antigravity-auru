import os
import json
from groq import Groq
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa cliente Groq
# Certifique-se de adicionar GROQ_API_KEY ao seu arquivo .env
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    print("ERRO: GROQ_API_KEY não encontrada nas variáveis de ambiente.")
else:
    api_key = api_key.strip()
    print(f"Chave carregada: {api_key[:10]}...")

client = Groq(api_key=api_key)

def extract_receipt_data(text_input):
    """
    Simula a extração de dados de um recibo (via OCR ou texto bruto)
    usando o Llama 3 70B no Groq.
    """
    
    prompt = f"""
    Atue como um especialista em varejo brasileiro. 
    Analise o texto abaixo de um cupom fiscal e extraia as informações em formato JSON estrito.
    
    Campos necessários:
    - estabelecimento (nome)
    - data (AAAA-MM-DD)
    - valor_total (decimal)
    - tipo_consumo ('luz_agua' ou 'cupom_fiscal')
    - itens [
        {{
            "nome": "string",
            "preco": decimal,
            "gtin": "string ou null"
        }}
    ]

    Texto do recibo:
    ---
    {text_input}
    ---
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Você é um assistente especializado em extração de dados estruturados de documentos fiscais brasileiros. Responda apenas com o JSON."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        response_format={"type": "json_object"}
    )

    return json.loads(chat_completion.choices[0].message.content)

if __name__ == "__main__":
    # Exemplo de texto extraído de um cupom (OCR mock)
    sample_text = """
    MERCADO SUPER BOM LTDA
    RUA DAS FLORES, 123 - SAO PAULO - SP
    CNPJ: 12.345.678/0001-90
    
    DATA: 18/03/2026 14:30:22
    
    1234567890123  ARROZ BALANCE 5KG  1  25,90
    7891020304050  FEIJAO PRETO 1KG   2   8,50
    
    TOTAL R$ 42,90
    """
    
    print("Iniciando extração de dados com Groq...")
    try:
        data = extract_receipt_data(sample_text)
        print("\nSucesso!")
        output_path = "c:/Users/Admin/Desktop/Conta/.tmp/test_output.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Resultado salvo em: {output_path}")
    except Exception as e:
        error_msg = f"Erro ao processar: {e}"
        print(error_msg)
        error_path = "c:/Users/Admin/Desktop/Conta/.tmp/error.txt"
        with open(error_path, "w", encoding="utf-8") as f:
            f.write(error_msg)
        print(f"Erro salvo em: {error_path}")
        print("Dica: Verifique se a GROQ_API_KEY está correta no arquivo .env")
