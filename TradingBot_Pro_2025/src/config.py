"""
Configuration management for TradingBot Pro 2025
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Database Configuration
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///trading_bot.db')
    
    # Trading APIs Configuration
    BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY')
    BINANCE_SECRET_KEY = os.environ.get('BINANCE_SECRET_KEY')
    COINBASE_API_KEY = os.environ.get('COINBASE_API_KEY')
    COINBASE_SECRET_KEY = os.environ.get('COINBASE_SECRET_KEY')
    
    # Quantum Computing Configuration
    IBM_QUANTUM_TOKEN = os.environ.get('IBM_QUANTUM_TOKEN')
    AWS_BRAKET_ACCESS_KEY = os.environ.get('AWS_BRAKET_ACCESS_KEY')
    AWS_BRAKET_SECRET_KEY = os.environ.get('AWS_BRAKET_SECRET_KEY')
    
    # Notification Configuration
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
    DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
    
    # Security Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    RATE_LIMIT_PER_MINUTE = int(os.environ.get('RATE_LIMIT_PER_MINUTE', 60))
    MAX_DAILY_TRADES = int(os.environ.get('MAX_DAILY_TRADES', 1000))
    
    # Risk Management Configuration
    MAX_POSITION_SIZE = float(os.environ.get('MAX_POSITION_SIZE', 0.1))
    STOP_LOSS_PERCENTAGE = float(os.environ.get('STOP_LOSS_PERCENTAGE', 0.02))
    TAKE_PROFIT_PERCENTAGE = float(os.environ.get('TAKE_PROFIT_PERCENTAGE', 0.05))
    
    # Redis Configuration for Celery
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'

# Configuration factory
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    return config[os.getenv('FLASK_ENV', 'default')]
