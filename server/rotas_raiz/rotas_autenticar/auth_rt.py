# auth.py
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, jsonify, request, redirect, url_for, session, flash
from functools import wraps
from server.Database.modelo_base_dados import db, User



def generate_auth_token(user_id, role, expires_in=3600):
    """Gera um token JWT para o usuário."""
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'role': role
        }
        # Ensure the secret key is treated as bytes if encode expects it
        secret_key = current_app.config['SECRET_KEY']
        if isinstance(secret_key, str):
            secret_key = secret_key.encode('utf-8')

        token = jwt.encode(
            payload,
            secret_key, # Use the potentially bytes-encoded secret key
            algorithm='HS256'
        )
        return token.decode('utf-8') if isinstance(token, bytes) else token
    except Exception as e:
        return f"Error generating token: {str(e)}" # More descriptive error

def decode_auth_token(token):
    """Decodifica o token JWT."""
    try:
        secret_key = current_app.config['SECRET_KEY']
        if isinstance(secret_key, str):
            secret_key = secret_key.encode('utf-8')
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
    except Exception as e: # Catch other potential errors during decoding
        return f'Error decoding token: {str(e)}'

def login_required(f):
    """Decorator para proteger rotas que requerem login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verifica se há um token na sessão ou no cabeçalho Authorization
        token = None
        if 'logged_in' in session and session['logged_in']:
            token = session.get('jwt_token')
        else:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1] # Bearer <token>

        if not token:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('login.login')) # Redireciona para login se não houver token

        user_data = decode_auth_token(token)
        if isinstance(user_data, str): # Se for uma string, é um erro de token
            session.pop('logged_in', None)
            session.pop('jwt_token', None)
            flash(f'Sessão expirada ou inválida: {user_data}', 'danger')
            return redirect(url_for('login.login'))

        # Opcional: Verifique se o usuário ainda existe no banco de dados
        user = User.query.get(user_data['sub'])
        if not user or not user.is_active:
            session.pop('logged_in', None)
            session.pop('jwt_token', None)
            flash('Usuário desativado ou não encontrado. Faça login novamente.', 'danger')
            return redirect(url_for('login.login'))

        # Adiciona os dados do usuário ao objeto request para acesso na rota
        request.current_user = user
        request.user_role = user_data['role']
        return f(*args, **kwargs)
    return decorated_function

def is_authenticated():
    pass

def register_user(username, email, password, organization_id=None, role='user', first_name=None, last_name=None):
    """Registra um novo usuário no banco de dados."""
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return False, "Username or email already exists."

    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        organization_id=organization_id,
        role=role,
        first_name=first_name,
        last_name=last_name
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        return True, new_user
    except Exception as e:
        db.session.rollback()
        return False, f"Database error during registration: {str(e)}"

def verify_user(email, password):
    """Verifica as credenciais do usuário."""
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None