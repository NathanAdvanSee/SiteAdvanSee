# app.py

from flask import Flask, render_template # Remove request, jsonify
# REMOVIDO: from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from src.routes.assets import assets_bp
from src.routes.agents import agents_bp
# REMOVIDO: from src.routes.auth import auth_bp # Não precisa mais do blueprint de autenticação
from src.models.database import db, Organization, User, AssetCategory, Vendor, Location, Asset, Software, AssetSoftware, Vulnerability, AssetVulnerability, Patch, AssetPatch, Agent, AssetHistory
from src.models.config import CONFIG
# REMOVIDO: import bcrypt # Não precisa mais de bcrypt aqui

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')

    # Configurações do Banco de Dados
    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CONFIG.SQLALCHEMY_TRACK_MODIFICATIONS

    # REMOVIDO: Configuração do JWT
    # app.config['JWT_SECRET_KEY'] = 'dIjDw9YncsLcT8ZpBPkL1bl6Yhm7uijnhrwUEg'

    # Inicializa o SQLAlchemy com a aplicação Flask
    db.init_app(app)

    # REMOVIDO: Inicializa o Flask-JWT-Extended
    # jwt = JWTManager(app)

    # Habilita CORS para todas as rotas (necessário para requisições do frontend)
    CORS(app)

    # Registra os Blueprints
    app.register_blueprint(assets_bp, url_prefix='/api/assets')
    app.register_blueprint(agents_bp, url_prefix='/api/agents')
    # REMOVIDO: app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Cria as tabelas do banco de dados se elas não existirem
    with app.app_context():
        db.create_all()

        # Opcional: Inserir dados iniciais para a organização, se não houver nenhuma
        # Como não há login, o agente e a dashboard usarão uma organização padrão.
        default_org = Organization.query.first() # Buscar a primeira organização
        if not default_org:
            print("Criando organização padrão (para uso público da dashboard)...")
            default_org = Organization(name='Default Public Organization', description='Organization for public dashboard access') # Nome diferente para clareza
            db.session.add(default_org)
            db.session.commit()
            print(f"Organização '{default_org.name}' criada com ID: {default_org.id}")
            
        # REMOVIDO: Lógica de criação de usuário 'admin', pois não há login na dashboard
        # if not User.query.filter_by(username='admin').first():
        #     # ... criar admin com bcrypt ...

    # Rota para servir a página principal da dashboard (index.html)
    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)