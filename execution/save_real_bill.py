import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SECRET")

def save_manual_transaction():
    supabase: Client = create_client(url, key)
    
    data = {
        "amount": 1252.93,
        "category": "Aluguel/Moradia",
        "description": "Boleto Aluguel - Imobiliária Jaú (Rua Princesa Isabel)",
        "transaction_date": "2026-02-18",
        "raw_data": {
            "beneficiario": "Abilio Laranjeira Rodrigues de Areia & Cia Ltda",
            "vencimento": "18/02/2026",
            "detalhes": "IPTU R$ 79,07 + Creditas R$ 123,86",
            "processado_por": "Auru Vision"
        }
    }
    
    try:
        res = supabase.table("transactions").insert(data).execute()
        print("✅ Transação do boleto salva com sucesso!")
        print(json.dumps(res.data, indent=2))
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    save_manual_transaction()
