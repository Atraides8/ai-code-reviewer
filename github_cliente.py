import os
from github import GithubIntegration
from github import Github

def get_github_client(repo_name):
    app_id = os.getenv("GITHUB_APP_ID")
    
    # --- LÓGICA HÍBRIDA (LOCAL vs NUBE) ---
    # 1. Intentamos leer el contenido de la llave desde una variable de entorno (NUBE)
    private_key_content = os.getenv("GITHUB_PRIVATE_KEY")
    
    # 2. Si no existe la variable, intentamos leer el archivo (LOCAL)
    if not private_key_content:
        pem_file_name = "tu-archivo-privado.2024-xx-xx.private-key.pem" # <--- ASEGÚRATE QUE ESTE NOMBRE SIGA SIENDO EL TUYO
        try:
            with open(pem_file_name, 'r') as f:
                private_key_content = f.read()
        except FileNotFoundError:
            raise Exception("No encontré la variable GITHUB_PRIVATE_KEY ni el archivo .pem")
    
    # ---------------------------------------

    git_integration = GithubIntegration(
        app_id,
        private_key_content,
    )

    owner, repo = repo_name.split("/")
    installation = git_integration.get_repo_installation(owner, repo)
    access_token = git_integration.get_access_token(installation.id).token
    
    return Github(auth=None, base_url="https://api.github.com", login_or_token=access_token)