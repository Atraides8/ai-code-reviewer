import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("--- BUSCANDO MODELOS DISPONIBLES ---")
try:
    for m in genai.list_models():
        # Filtramos solo los que sirven para generar texto (generateContent)
        if 'generateContent' in m.supported_generation_methods:
            print(f"Nombre: {m.name}")
except Exception as e:
    print(f"Error: {e}")