import os
import json
import base64
from http.server import BaseHTTPRequestHandler
from groq import Groq

# Configuração da Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        image_base64 = data.get("image")
        
        prompt = """
        Você é a AURU, especialista em OCR de cupons fiscais brasileiros.
        Analise a imagem e retorne um JSON com esta estrutura:
        {
          "type": "compra",
          "merchant": "Nome do Mercado",
          "total": 0.00,
          "date": "YYYY-MM-DD",
          "items": [
            {"name": "Arroz 5kg", "price": 25.90, "icon": "🌾"},
            {"name": "Leite Integral", "price": 5.49, "icon": "🥛"}
          ]
        }
        Use emojis brasileiros apropriados no campo 'icon'.
        """

        try:
            completion = client.chat.completions.create(
                model="llama-3.2-90b-vision-preview",
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
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(result.encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
