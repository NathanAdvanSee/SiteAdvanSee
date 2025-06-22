# server/rotas_raiz/login_rt.py

from server.rotas_raiz.rotas_autenticar.auth_rt import verify_user, generate_auth_token
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity # jwt_required removed as per above
from server.Config.Config import Config # Imported for reference if needed, but current_app.config is generally preferred


login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = verify_user(email, password)
        if user:
            # Gerar token JWT
            token = generate_auth_token(user.id, user.role, expires_in=3600)
            # Ensure the token is a string (it should be from generate_auth_token)
            if isinstance(token, bytes):
                token = token.decode('utf-8')

            if "Error" in str(token): # Check for error message within the token string
                print(f"Erro na geração do token: {token}")
                flash(f'Erro ao gerar token: {token}', 'danger')
                return render_template('login.html')

            session['logged_in'] = True
            session['user_id'] = user.id
            session['user_role'] = user.role
            session['jwt_token'] = token

            flash('Login bem-sucedido!', 'success')
            print(f"Usuário {user.username} logado com sucesso. ID: {user.id}, Role: {user.role}")
            print(f"Token JWT gerado: {session['jwt_token']}")
            print(f"Config JWT Secret Key: {Config.JWT_SECRET_KEY}") # For debugging purposes
            print(f"REDIRECT URL: {url_for('main.dashboard')}") # Redirect to dashboard after successful login
            return redirect(url_for('main.dashboard')) # Redirect to the dashboard blueprint's dashboard route
        else:
            flash('Email ou senha inválidos.', 'danger')
    return render_template('login.html')