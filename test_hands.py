import os
from dotenv import load_dotenv
from github_cliente import get_github_client

# Cargar variables
load_dotenv()

# --- CONFIGURA ESTO ---
REPO_NAME = "Atraides8/sandbox-pr-testing" # <--- CÁMBIALO (Usuario/Repo)
PR_NUMBER = 1                               # <--- Número de tu Pull Request abierto
# ----------------------

def test_comment():
    print(f"🤖 Intentando conectar con {REPO_NAME}...")
    
    try:
        # 1. Usar nuestra función helper para obtener el cliente autenticado
        gh = get_github_client(REPO_NAME)
        
        # 2. Obtener el repositorio
        repo = gh.get_repo(REPO_NAME)
        
        # 3. Obtener el Pull Request específico
        pr = repo.get_pull(PR_NUMBER)
        
        # 4. Escribir un comentario
        print("✍️  Escribiendo comentario...")
        pr.create_issue_comment("¡Hola humano! Soy el bot y tengo 'Manos' 🙌. Esta es una prueba de escritura automática.")
        
        print("✅ ¡Éxito! Revisa tu PR en GitHub.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_comment()