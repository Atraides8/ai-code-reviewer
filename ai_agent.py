import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Configuración Inicial
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("No se encontró la GEMINI_API_KEY en el archivo .env")

genai.configure(api_key=API_KEY)

# Usamos el modelo Flash porque es rápido y barato (ideal para bots)
model = genai.GenerativeModel('gemini-2.0-flash')

def get_ai_review(diff_content):
    """
    Envía el diff a Gemini y retorna la revisión.
    """
    
    # --- PROMPT ENGINEERING ---
    # Aquí definimos la personalidad y las reglas del bot.
    prompt = f"""
    Actúa como un Ingeniero de Software Senior experto en seguridad y buenas prácticas (Python).
    
    Tu tarea es revisar el siguiente 'git diff' de un Pull Request.
    
    Reglas:
    1. Busca bugs potenciales, problemas de seguridad (claves expuestas, inyecciones) y mala optimización.
    2. Sé constructivo pero directo.
    3. Ignora temas triviales como espacios en blanco o falta de comentarios obvios.
    4. Si el código parece seguro, responde "LGTM" (Looks Good To Me).
    5. Usa formato Markdown para tu respuesta.
    
    Código a revisar:
    ```diff
    {diff_content}
    ```
    """
    
    print("🤖 Consultando a Gemini...")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error consultando a la IA: {str(e)}"

# --- BLOQUE DE PRUEBA (Solo se ejecuta si corres este archivo directamente) ---
if __name__ == "__main__":
    # Leemos el archivo falso que creamos
    try:
        with open("dummy_diff.txt", "r", encoding="utf-8") as f:
            diff_falso = f.read()
            
        # Probamos la función
        review = get_ai_review(diff_falso)
        
        print("\n--- 📝 REVISIÓN GENERADA POR IA ---\n")
        print(review)
        print("\n-----------------------------------")
        
    except FileNotFoundError:
        print("Error: No encontré el archivo dummy_diff.txt para probar.")