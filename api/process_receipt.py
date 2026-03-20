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
        Você é a AURU, uma IA especialista em finanças brasileiras. 
        Analise o cupom fiscal ou boleto e retorne APENAS um JSON:
        {
          "type": "compra" ou "boleto",
          "merchant": "Nome do Local",
          "amount": 0.00,
          "category": "Mercado", "Saúde", "Casa", etc,
          "card_info": "VISA 4590",
          "date": "YYYY-MM-DD"
        }
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
