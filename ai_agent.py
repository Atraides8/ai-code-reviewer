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

def get_ai_review(diff_content, file_structure):
    """
    Envía el diff y la estructura del proyecto a Gemini.
    """
    
    prompt = f"""
    Actúa como un Ingeniero de Software Senior y Arquitecto de Software.
    
    CONTEXTO DEL PROYECTO:
    Estás revisando un Pull Request en un repositorio que tiene la siguiente estructura de archivos (esto te ayudará a entender las importaciones y la arquitectura):
    
    ```text
    {file_structure}
    ```
    
    TU TAREA:
    Revisa el siguiente 'git diff'.
    
    CÓDIGO A REVISAR:
    ```diff
    {diff_content}
    ```
    
    REGLAS DE REVISIÓN:
    1. Prioridad ALTA: Busca vulnerabilidades de seguridad (inyecciones, secretos expuestos).
    2. Prioridad MEDIA: Busca bugs lógicos y errores de sintaxis.
    3. Prioridad BAJA: Sugiere mejoras de rendimiento o arquitectura basada en la estructura que ves.
    4. Sé conciso. Si ves un archivo 'utils.py' en la estructura y el código lo importa, asume que es correcto, no alucines errores de importación.
    5. Responde en Markdown. Si todo está bien, responde "LGTM 🚀".
    """
    
    print("🤖 Consultando a Gemini con contexto estructural...")
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