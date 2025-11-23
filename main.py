import os
import hmac
import hashlib
import json
from fastapi import FastAPI, Request, HTTPException, Header # <--- Actualizado
from dotenv import load_dotenv

# 1. Cargar variables de entorno
# Esta función busca el archivo .env y carga las variables en el sistema.
load_dotenv()

# 2. Inicializar la App
app = FastAPI()

# 3. Ruta de prueba (Health Check)
# Sirve para saber si tu servidor está "vivo".
@app.get("/")
def read_root():
    return {"status": "online", "bot": "AI Code Reviewer"}

# 4. Ruta de verificación de Configuración
# ESTO ES SOLO PARA DESARROLLO. Nos confirma si Python leyó tu .env
@app.get("/debug-config")
def check_config():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        # Devolvemos solo una parte para confirmar sin revelar la clave completa
        return {"gemini_api_key": f"Cargada correctamente: {api_key[:4]}..."}
    else:
        return {"gemini_api_key": "ERROR: No encontrada"}
    

# Endpoint para recibir Webhooks de GitHub
@app.post("/webhook")
async def github_webhook(request: Request, x_hub_signature_256: str = Header(None)): #Se trae la cabecera de github, lo cual nos da la firma del mensaje
    # 1. Obtener el secreto del .env
    secret = os.getenv("WEBHOOK_SECRET")
    
    # 2. Validar que tengamos el secreto y la firma
    if not secret or not x_hub_signature_256:
        raise HTTPException(status_code=401, detail="Configuración de seguridad incompleta")

    # 3. Leer el cuerpo "crudo" de la petición (bytes) para calcular la firma
    payload_body = await request.body()
    
    # 4. Verificar la firma (Criptografía HMAC)
    # Creamos una firma local usando nuestro secreto y el cuerpo del mensaje
    hash_object = hmac.new(secret.encode("utf-8"), payload_body, hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    
    # Comparamos nuestra firma con la que mandó GitHub
    if not hmac.compare_digest(expected_signature, x_hub_signature_256):
        # Si no coinciden, alguien está intentando hackearnos
        raise HTTPException(status_code=403, detail="Firma inválida. ¡Intruso detectado!")

    # 5. Si pasamos la seguridad, procesamos el JSON
    payload = json.loads(payload_body)
    
    print("✅ Firma verificada. Webhook auténtico.")
    
    if "action" in payload:
        print(f"Acción realizada: {payload['action']}")
        
    return {"status": "received_securely"}