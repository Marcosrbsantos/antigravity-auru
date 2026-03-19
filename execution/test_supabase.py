import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

def test_connection():
    if not url or not key:
        print("ERRO: SUPABASE_URL ou SUPABASE_KEY não encontradas no .env")
        return

    try:
        supabase: Client = create_client(url, key)
        # Tenta listar as tabelas (via rpc ou apenas uma query simples)
        # Como não sabemos se há dados, vamos apenas testar a inicialização e uma query na tabela profiles
        response = supabase.table("profiles").select("*").limit(1).execute()
        print("Conexão com Supabase estabelecida com sucesso!")
        print(f"Status da consulta: {response}")
    except Exception as e:
        print(f"Erro ao conectar ao Supabase: {e}")

if __name__ == "__main__":
    test_connection()
