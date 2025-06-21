
from server.rotas_raiz.rotas_autenticar.auth_rt import login_required, verify_user, generate_auth_token
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from server.Config.Config import Config


login_bp = Blueprint('login', __name__)
@login_bp.route('/login', methods=['GET', 'POST'])
@jwt_required()
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = verify_user(email, password)
        if user:
            # Gerar token JWT
            token = generate_auth_token(user.id, user.role, expires_in=3600)
            if isinstance(token, str) and "Error" in token: # Checa se a string de erro foi retornada
                print(f"Erro na geração do token: {token}") # Novo print
                flash(f'Erro ao gerar token: {token}', 'danger')
                return render_template('login.html')
            
            session['logged_in'] = True
            session['user_id'] = user.id
            session['user_role'] = user.role
            session['jwt_token'] = token.decode('utf-8') if isinstance(token, bytes) else token # Certifica-se de que é uma string
            
            flash('Login bem-sucedido!', 'success')
            print(f"Usuário {user.username} logado com sucesso. ID: {user.id}, Role: {user.role}")
            print(f"Token JWT gerado: {session['jwt_token']}")
            print(f"Config JWT Secret Key: {Config.JWT_SECRET_KEY}")
            print(f"REDIRECT URL: {url_for('equipamentos_list')}")  # Verifica a URL de redirecionamento
            #return redirect(url_for('equipamentos_list'))  # Redireciona para a lista de equipamentos
            #return render_template('dashboard.html')
        else:
            flash('Email ou senha inválidos.', 'danger')
    return render_template('login.html')
