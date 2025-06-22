# server/rotas_raiz/raiz_rt.py
import os
from flask import Blueprint, send_from_directory, render_template, current_app, redirect, url_for

# Cria um Blueprint para a raiz
raiz_bp = Blueprint('frontend', __name__)

# Rota raiz - agora redireciona para a SPA index.html
@raiz_bp.route('/')
def root():
    # current_app é usado dentro de Blueprints para acessar a instância do Flask app
    # Isso garante que app.template_folder e app.static_folder sejam acessados corretamente
    return render_template('index.html')

# Rota "catch-all" para servir arquivos estáticos ou o index.html da SPA
@raiz_bp.route('/<path:path>')
def servir(path):
    # Obtém os caminhos de forma segura dentro do contexto do Blueprint
    static_folder_path = os.path.join(current_app.root_path, current_app.static_folder)
    template_folder_path = os.path.join(current_app.root_path, current_app.template_folder)

    # 1. Tenta servir um arquivo estático da pasta 'static'
    # Esta parte é útil para arquivos diretos na raiz, ou para catch-all de JS frameworks.
    # Para CSS/JS/Imagens dentro de subpastas do seu static_folder, o Flask já faz isso por padrão.
    if os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)

    # If the path is for a known template that should be directly rendered by a blueprint,
    # we should let that blueprint's route handle it.
    # For a SPA, usually all unmatched routes fall back to index.html.
    # The login route is now handled by the login_bp, so this specific check is removed.

    # 2. Se não for nenhum dos anteriores, serve o index.html da SPA
    # Isso é essencial para o roteamento client-side (ex: /dashboard, /profile)
    index_path = os.path.join(template_folder_path, 'index.html')
    if os.path.exists(index_path):
        return render_template('index.html')
    else:
        return "index.html not found", 404