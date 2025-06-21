# config.py
class Config:
    DB_HOST = "127.0.0.1"
    DB_NAME = "ISAC_BD_ADVANSEE"
    DB_USER = "isac"
    EMAIL = "isac.admin@advansee.com.br"
    DB_PASSWORD = "kwa44fgjc8suf91kjsacaz"
    DB_PORT = "5432"
    JWT_SECRET_KEY  = '5wC2A3DRsZfkAc5HJqbvmoa73OEb4IyenFuxTj0cO0RJUkTUw9'
    SECRET_KEY      = 'LkTjm5au6gaE4kBVvG5jODJO2m8h6nsq4wJfAOH80wmcLJnemz'
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False