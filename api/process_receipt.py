import os
import json
from groq import Groq

# Configuração da Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def handler(request):
    # CORS Headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }

    if request.method == 'OPTIONS':
        return { 'statusCode': 200, 'headers': headers, 'body': '' }

    if request.method == 'POST':
        try:
            # Vercel request object has .json() or we read .body
            data = request.json
            image_base64 = data.get("image")
            
            if not image_base64:
                return { 'statusCode': 400, 'headers': headers, 'body': json.dumps({"error": "No image provided"}) }

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
                model="llama-3.2-11b-vision-preview", # Usei a 11B pq é mais rápida pra Vercel não dar timeout
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
            
            result = completion.choices[0].message.content
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': result
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({"error": str(e)})
            }

    return { 'statusCode': 405, 'headers': headers, 'body': 'Method Not Allowed' }
