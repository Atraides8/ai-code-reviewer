import os
from github import GithubIntegration

def get_github_client(repo_name):
    """
    Autentica al bot como una App e inicializa un cliente 
    para un repositorio específico.
    """
    # 1. Cargar credenciales del entorno
    app_id = os.getenv("GITHUB_APP_ID")
    
    # --- CONFIGURACIÓN: PON EL NOMBRE DE TU ARCHIVO .PEM AQUÍ ---
    pem_file_name = "review-bot-atraides.2025-11-21.private-key.pem" 
    # ------------------------------------------------------------

    # 2. Leer la llave privada
    try:
        with open(pem_file_name, 'r') as f:
            private_key = f.read()
    except FileNotFoundError:
        raise Exception(f"Error: No encuentro el archivo {pem_file_name}. ¿Está en la raíz?")

    # 3. Autenticarse como la App (A nivel global)
    # Esto nos dice "Hola, soy la App X", pero aún no sabemos en qué repo trabajar.
    git_integration = GithubIntegration(
        app_id,
        private_key,
    )

    # 4. Obtener la instalación específica para ESTE repositorio
    # Las Apps se "instalan" en usuarios u organizaciones. Necesitamos el ID de esa instalación.
    owner, repo = repo_name.split("/") # Ej: "juanito/sandbox" -> "juanito", "sandbox"
    
    try:
        installation = git_integration.get_repo_installation(owner, repo)
    except Exception as e:
        raise Exception(f"El bot no está instalado en el repo '{repo_name}'. Ve a la config de la App e instálalo. Error: {e}")

    # 5. Generar un token temporal para actuar en esa instalación
    # Estas son las verdaderas "Manos".
    access_token = git_integration.get_access_token(installation.id).token
    
    # Retornamos un cliente de Github autenticado listo para usar
    from github import Github
    return Github(auth=None, base_url="https://api.github.com", login_or_token=access_token)