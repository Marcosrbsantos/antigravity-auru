import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SECRET")

def check_db():
    supabase: Client = create_client(url, key)
    res = supabase.table("transactions").select("*").order("created_at", desc=True).limit(1).execute()
    print("Última transação salva no banco:")
    import json
    print(json.dumps(res.data, indent=2))

if __name__ == "__main__":
    check_db()
