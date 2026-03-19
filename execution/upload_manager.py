import os
import json
import base64
from supabase import create_client, Client
from groq import Groq
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SECRET") # Usar service_role para bypass RLS
BUCKET_NAME = "receipts"

# Configuração Groq (Auru)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
MODEL_NAME = "llama-3.2-90b-vision-preview" 

def process_receipt(file_path: str, household_id: str = None):
    """
    Fluxo completo: Upload -> OCR/AI -> DB
    """
    print(f"🚀 [Auru] Iniciando processamento de: {file_path}")
    
    if not all([SUPABASE_URL, SUPABASE_KEY, GROQ_API_KEY]):
        return {"error": "Configurações de API ausentes no .env"}

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # 1. Upload para Supabase Storage
    file_name = os.path.basename(file_path)
    remote_path = f"uploads/{file_name}"
    
    try:
        with open(file_path, "rb") as f:
            supabase.storage.from_(BUCKET_NAME).upload(
                path=remote_path,
                file=f,
                file_options={"content-type": "image/jpeg", "x-upsert": "true"}
            )
        print("✅ [Storage] Upload concluído.")
    except Exception as e:
        # Se falhar porque o bucket não existe ou RLS, tentaremos prosseguir apenas com a IA se local
        print(f"⚠️ [Storage] Erro no upload: {e}")

    # 2. Processamento IA (Auru / Groq)
    # Como o Groq não suporta envio de imagem via URL pública nativamente de forma simples sem Vision,
    # vamos ler a imagem localmente e converter para Base64 se necessário, ou usar o texto se for OCR.
    # Para este MVP, vamos usar a técnica baseada no script de teste anterior que funcionou.
    
    client = Groq(api_key=GROQ_API_KEY)
    
    # Simulação de OCR + Extração (No futuro integraremos com Groq Vision diretamente se disponível)
    # Por enquanto, mantemos a lógica do prompt potente.
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    prompt = """
    Atue como Auru, o especialista financeiro visionário.
    Extraia do recibo abaixo: 
    1. Nome do Estabelecimento
    2. Data e Hora
    3. Valor Total (float)
    4. Itens (Nome, Preço Unitário, Quantidade)
    5. Categoria (Mercado, Lazer, Saúde, etc.)
    
    Retorne APENAS um JSON puro.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_string}",
                            },
                        },
                    ],
                }
            ],
            model=MODEL_NAME,
            response_format={"type": "json_object"}
        )
        data = json.loads(chat_completion.choices[0].message.content)
        print("💡 [Auru] Inteligência extraída com sucesso.")
    except Exception as e:
        return {"error": f"Falha na IA: {e}"}

    # 3. Persistência no Supabase DB
    try:
        # Formata para a tabela 'transactions'
        transaction_data = {
            "household_id": household_id, # Link com a familia
            "amount": data.get("total_spending") or data.get("Valor Total"),
            "category": data.get("Categoria") or "Geral",
            "description": data.get("Nome do Estabelecimento") or "Compra s/ nome",
            "transaction_date": data.get("Data") or "now()",
            "raw_data": data # Guarda o JSON completo
        }
        
        # Se não tivermos household_id, o RLS pode barrar se for anon.
        # Mas estamos usando service_role (SUPABASE_SECRET).
        res = supabase.table("transactions").insert(transaction_data).execute()
        print("🏦 [Database] Transação salva com sucesso.")
        return {"status": "success", "data": res.data}
    except Exception as e:
        print(f"❌ [Database] Erro ao salvar: {e}")
        return {"error": str(e), "extracted_data": data}

if __name__ == "__main__":
    test_file = "C:/Users/Admin/Desktop/Conta/.tmp/WhatsApp Image 2026-03-18 at 22.53.03.jpeg"
    if os.path.exists(test_file):
        result = process_receipt(test_file)
        print(json.dumps(result, indent=2))
    else:
        print(f"Aguardando imagem em: {test_file}")
