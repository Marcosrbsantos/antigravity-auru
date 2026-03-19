import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SECRET")

def setup_storage():
    """
    Cria o bucket 'receipts' se ele não existir.
    """
    if not url or not key:
        print("Credenciais Supabase não encontradas.")
        return

    supabase: Client = create_client(url, key)
    
    try:
        # Tenta pegar as opções do bucket para ver se existe
        buckets = supabase.storage.list_buckets()
        exists = any(b.name == 'receipts' for b in buckets)
        
        if not exists:
            print("Criando bucket 'receipts'...")
            # Nota: a biblioteca python as vezes varia na criação, tentaremos normal
            supabase.storage.create_bucket('receipts', options={'public': False})
            print("Bucket 'receipts' criado com sucesso!")
        else:
            print("Bucket 'receipts' já existe.")
            
    except Exception as e:
        print(f"Erro ao gerenciar storage: {e}")

if __name__ == "__main__":
    setup_storage()
