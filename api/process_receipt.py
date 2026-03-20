import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

# Inicializa Flask
app = Flask(__name__)
CORS(app) # Habilita CORS para todas as rotas

# Configuração da Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/api/process_receipt', methods=['POST', 'OPTIONS'])
def process_receipt():
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        image_base64 = data.get("image")
        
        if not image_base64:
            return jsonify({"error": "No image provided"}), 400

        prompt = """
        Você é a AURU, especialista em OCR de cupons fiscais brasileiros.
        Analise a imagem e retorne um JSON com esta estrutura:
        {
          "type": "compra",
          "merchant": "Nome do Mercado",
          "total": 0.00,
          "date": "2024-03-20",
          "items": [
            {"name": "Produto", "price": 0.00, "icon": "📦"}
          ]
        }
        Use emojis apropriados. Se for boleto, mude type para 'boleto'.
        """

        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"}
        )
        
        # A Groq retorna uma string JSON, precisamos converter para objeto real
        result_content = completion.choices[0].message.content
        return result_content, 200, {'Content-Type': 'application/json'}
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Necessário para o Vercel reconhecer o app
handler = app
