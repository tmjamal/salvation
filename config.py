import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'srashtaavinte-maargadarshnam-2024-secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///islamic_site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False

class VercelConfig(Config):
    DEBUG = False
    # Vercel will provide DATABASE_URL for PostgreSQL
    # For SQLite, you might need to use a file-based database
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'vercel': VercelConfig,
    'default': ProductionConfig
}
