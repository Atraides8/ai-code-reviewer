import os
import hmac
import hashlib
import json
from fastapi import FastAPI, Request, HTTPException, Header, BackgroundTasks
from dotenv import load_dotenv

# Importamos nuestras piezas construidas en fases anteriores
from ai_agent import get_ai_review       # Fase 3: Cerebro
from github_cliente import get_github_client # Fase 4: Manos

load_dotenv()

app = FastAPI()

# --- LÓGICA DEL PROCESO (Lo que pasa tras bambalinas) ---
def process_pull_request(payload):
    """
    Esta función hace el trabajo pesado en segundo plano.
    """
    try:
        # 1. Extraer datos clave del Webhook
        action = payload.get("action")
        if action not in ["opened", "synchronize"]:
            # Solo nos interesa cuando abren PR o suben nuevo código (synchronize)
            return

        pr_number = payload["pull_request"]["number"]
        repo_full_name = payload["repository"]["full_name"] # Ej: "Atraides8/sandbox..."
        
        print(f"⚙️ Procesando PR #{pr_number} en {repo_full_name}...")

        # 2. Conectar con GitHub (Las Manos)
        gh_client = get_github_client(repo_full_name)
        repo = gh_client.get_repo(repo_full_name)
        pr = repo.get_pull(pr_number)

        # 3. Obtener el código a revisar (El Diff)
        # Iteramos los archivos y juntamos sus "patches" (los cambios)
        diff_text = ""
        for file in pr.get_files():
            if file.patch: # Solo si hay cambios de texto
                diff_text += f"Archivo: {file.filename}\n"
                diff_text += f"{file.patch}\n\n"

        if not diff_text:
            print("⚠️ El PR parece vacío o son archivos binarios.")
            return

        # 4. Consultar al Cerebro (Gemini)
        print("🤖 Enviando código a Gemini...")
        ai_comment = get_ai_review(diff_text)

        # 5. Publicar el comentario
        print("✍️ Publicando en GitHub...")
        pr.create_issue_comment(f"## 🤖 Revisión Automática de Código\n\n{ai_comment}")
        print(f"✅ ¡Listo! Comentario publicado en PR #{pr_number}")

    except Exception as e:
        print(f"❌ Error procesando el PR: {e}")


# --- ENDPOINT DEL WEBHOOK (El Oído) ---
@app.post("/webhook")
async def github_webhook(
    request: Request, 
    background_tasks: BackgroundTasks, # <--- Herramienta mágica de FastAPI
    x_hub_signature_256: str = Header(None)
):
    # 1. SEGURIDAD: Verificar Firma
    secret = os.getenv("WEBHOOK_SECRET")
    if not secret or not x_hub_signature_256:
        raise HTTPException(status_code=401, detail="Falta secreto o firma")

    payload_body = await request.body()
    hash_object = hmac.new(secret.encode("utf-8"), payload_body, hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    
    if not hmac.compare_digest(expected_signature, x_hub_signature_256):
        raise HTTPException(status_code=403, detail="Firma inválida")

    # 2. Procesar Payload
    payload = json.loads(payload_body)
    
    # 3. Delegar trabajo al Background (No hacemos esperar a GitHub)
    background_tasks.add_task(process_pull_request, payload)

    return {"status": "processing_in_background"}

@app.get("/")
def read_root():
    return {"bot_status": "Active 🟢"}