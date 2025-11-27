# -*- coding: utf-8 -*-
import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configura tu usuario y tu token personal de GitHub aquí
USER = os.getenv("USER")
TOKEN = os.getenv("TOKEN")

if not USER or not TOKEN:
    raise ValueError("Las variables de entorno USER y TOKEN deben estar configuradas en el archivo .env")
headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_repos(user):
    """
    Obtiene todos los repositorios donde el usuario tiene permisos de colaborador.
    """
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/user/repos?affiliation=owner,collaborator,organization_member&per_page=100&page={page}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print("Error al obtener repositorios:", resp.text)
            break
        data = resp.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def get_commit_count(repo_full_name, user):
    """
    Cuenta los commits hechos por el usuario en un repositorio específico.
    """
    count = 0
    page = 1
    while True:
        url = f"https://api.github.com/repos/{repo_full_name}/commits?author={user}&per_page=100&page={page}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            break
        commits = resp.json()
        count += len(commits)
        if len(commits) < 100:
            break
        page += 1
    return count

def main():
    repos = get_repos(USER)
    total_commits = 0
    repos_with_commits = 0

    print(f"Repositorios encontrados: {len(repos)}")
    for repo in repos:
        repo_name = repo["full_name"]
        commits = get_commit_count(repo_name, USER)
        if commits > 0:
            repos_with_commits += 1
        total_commits += commits
        print(f"- {repo_name}: {commits} commits")

    print("\nResumen:")
    print(f"Total de commits: {total_commits}")
    print(f"Repositorios donde has colaborado (al menos 1 commit): {repos_with_commits}")

if __name__ == "__main__":
    main()