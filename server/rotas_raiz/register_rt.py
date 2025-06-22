# server/rotas_raiz/register_rt.py

# Only import what's directly used or needed for the context
from server.rotas_raiz.rotas_autenticar.auth_rt import register_user
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from server.Config.Config import Config # Not directly used in this snippet, but common to have if config values are needed.


register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    print("Entrou na rota de registro")  # Debugging
    if request.method == 'POST':

        print("Dados recebidos do formulário de registro:", request.form)  # Debugging
        print("Dados do request:", request)  # Debugging
        print("POST")

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # For simplicity, allowing registration without organization_id.
        # In a real scenario, you might have a field for this or assign to a default organization.
        success, message = register_user(username, email, password)
        if success:
            flash('Registro bem-sucedido! Faça login para continuar.', 'success')
            return redirect(url_for('login.login')) # Use blueprint.route_name
        else:
            flash(f'Erro no registro: {message}', 'danger')
    return render_template('register.html') # You need to create a register.html template