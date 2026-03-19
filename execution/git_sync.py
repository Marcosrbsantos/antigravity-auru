import subprocess
import os

cwd = r"c:\Users\Admin\Desktop\Conta"
remote_url = "https://github.com/Marcosrbsantos/antigravity-auru.git"

def run_git(args):
    print(f"Executando: git {' '.join(args)}")
    result = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erro: {result.stderr}")
    else:
        print(f"Sucesso: {result.stdout}")
    return result.returncode

if __name__ == "__main__":
    # Configurar Identidade
    run_git(["config", "user.email", "auru@antigravity.ia"])
    run_git(["config", "user.name", "Auru Agent"])
    
    # Init and Add
    run_git(["init"])
    run_git(["add", "."])
    
    # Commit
    run_git(["commit", "-m", "🚀 Antigravity | Auru: Deploy Inicial"])
    
    # Remote
    # Remove existing origin if any
    run_git(["remote", "remove", "origin"])
    run_git(["remote", "add", "origin", remote_url])
    
    # Branch and Push
    run_git(["branch", "-M", "main"])
    print("Tentando Push... (Pode pedir login se não houver credenciais)")
    run_git(["push", "-u", "origin", "main", "--force"])
