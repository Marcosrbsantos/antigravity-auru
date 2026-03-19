import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

try:
    models = client.models.list()
    print("Modelos disponíveis na Groq:")
    for model in models.data:
        print(f"- {model.id}")
except Exception as e:
    print(f"Erro ao listar modelos: {e}")
