# auth.py
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, jsonify, request, redirect, url_for, session
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
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    except Exception as e:
        return str(e)

def decode_auth_token(token):
    """Decodifica o token JWT."""
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

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
            if auth_header:
                token = auth_header.split(" ")[1] # Bearer <token>
        
        if not token:
            return redirect(url_for('login')) # Redireciona para login se não houver token
        
        user_data = decode_auth_token(token)
        if isinstance(user_data, str): # Se for uma string, é um erro de token
            session.pop('logged_in', None)
            session.pop('jwt_token', None)
            return redirect(url_for('login'))
        
        # Opcional: Verifique se o usuário ainda existe no banco de dados
        user = User.query.get(user_data['sub'])
        if not user or not user.is_active:
            session.pop('logged_in', None)
            session.pop('jwt_token', None)
            return redirect(url_for('login'))

        # Adiciona os dados do usuário ao objeto request para acesso na rota
        request.current_user = user
        request.user_role = user_data['role']
        return f(*args, **kwargs)
    return decorated_function

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
    db.session.add(new_user)
    db.session.commit()
    return True, new_user

def verify_user(email, password):
    
    """Verifica as credenciais do usuário."""
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None