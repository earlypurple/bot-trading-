#!/usr/bin/env python3
"""
Script de configuration interactive des API pour TradingBot Pro 2025
"""

import os
import sys
import secrets
import getpass
from pathlib import Path

class APIConfigurationManager:
    def __init__(self):
        self.env_file = Path(".env")
        self.env_example = Path(".env.example")
        self.config = {}
        
    def display_welcome(self):
        print("\n🔑 Configuration des API - TradingBot Pro 2025")
        print("=" * 50)
        print("Ce script va vous guider pour configurer les clés API nécessaires.")
        print("Vos clés seront stockées de manière sécurisée dans le fichier .env")
        print()
        
    def generate_secure_keys(self):
        """Génère des clés sécurisées automatiquement"""
        print("🔐 Génération des clés de sécurité...")
        self.config['SECRET_KEY'] = secrets.token_urlsafe(32)
        self.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(32)
        print("✅ Clés de sécurité générées automatiquement")
        
    def configure_trading_apis(self):
        """Configure les API de trading"""
        print("\n📈 Configuration des API de Trading")
        print("-" * 35)
        
        # Configuration Binance
        print("\n🔸 Binance (Recommandé pour débuter)")
        print("Pour obtenir vos clés Binance:")
        print("1. Allez sur https://www.binance.com/")
        print("2. Compte > Gestion API > Créer une API")
        print("3. Activez uniquement 'Lecture' et 'Trading' (PAS 'Retrait')")
        print("4. Notez votre API Key et Secret Key")
        
        use_binance = input("\nVoulez-vous configurer Binance ? (o/N): ").lower().strip()
        if use_binance == 'o':
            self.config['BINANCE_API_KEY'] = input("Binance API Key: ").strip()
            self.config['BINANCE_SECRET_KEY'] = getpass.getpass("Binance Secret Key (masqué): ").strip()
            print("✅ Binance configuré")
        else:
            self.config['BINANCE_API_KEY'] = 'your-binance-api-key'
            self.config['BINANCE_SECRET_KEY'] = 'your-binance-secret-key'
            
        # Configuration Coinbase
        print("\n🔸 Coinbase Advanced Trade")
        print("Pour obtenir vos clés Coinbase:")
        print("1. Allez sur https://advanced.coinbase.com/")
        print("2. Settings > API > New API Key")
        print("3. Permissions: View + Trade")
        print("4. ⚠️  Pas de passphrase nécessaire pour Advanced Trade")
        
        use_coinbase = input("\nVoulez-vous configurer Coinbase ? (o/N): ").lower().strip()
        if use_coinbase == 'o':
            self.config['COINBASE_API_KEY'] = input("Coinbase API Key: ").strip()
            self.config['COINBASE_SECRET_KEY'] = getpass.getpass("Coinbase Secret Key (masqué): ").strip()
            print("✅ Coinbase configuré")
        else:
            self.config['COINBASE_API_KEY'] = 'your-coinbase-api-key'
            self.config['COINBASE_SECRET_KEY'] = 'your-coinbase-secret-key'
            
    def configure_notifications(self):
        """Configure les notifications"""
        print("\n📱 Configuration des Notifications")
        print("-" * 33)
        
        # Telegram
        print("\n🔸 Telegram Bot (Recommandé)")
        print("Pour créer un bot Telegram:")
        print("1. Parlez à @BotFather sur Telegram")
        print("2. Tapez /newbot et suivez les instructions")
        print("3. Récupérez votre token")
        print("4. Ajoutez votre bot à un chat et récupérez le chat ID")
        
        use_telegram = input("\nVoulez-vous configurer Telegram ? (o/N): ").lower().strip()
        if use_telegram == 'o':
            self.config['TELEGRAM_BOT_TOKEN'] = input("Telegram Bot Token: ").strip()
            self.config['TELEGRAM_CHAT_ID'] = input("Telegram Chat ID: ").strip()
            print("✅ Telegram configuré")
        else:
            self.config['TELEGRAM_BOT_TOKEN'] = 'your-telegram-bot-token'
            self.config['TELEGRAM_CHAT_ID'] = 'your-telegram-chat-id'
            
        # Discord
        print("\n🔸 Discord Webhook")
        use_discord = input("Voulez-vous configurer Discord ? (o/N): ").lower().strip()
        if use_discord == 'o':
            self.config['DISCORD_WEBHOOK_URL'] = input("Discord Webhook URL: ").strip()
            print("✅ Discord configuré")
        else:
            self.config['DISCORD_WEBHOOK_URL'] = 'your-discord-webhook-url'
            
    def configure_risk_parameters(self):
        """Configure les paramètres de risque"""
        print("\n⚖️ Configuration des Paramètres de Risque")
        print("-" * 40)
        
        print("Configuration des limites de sécurité:")
        
        # Taille maximum des positions
        max_position = input("Taille max des positions (0.01-0.1, défaut: 0.05): ").strip()
        self.config['MAX_POSITION_SIZE'] = max_position if max_position else '0.05'
        
        # Stop Loss
        stop_loss = input("Stop Loss en % (0.01-0.05, défaut: 0.02): ").strip()
        self.config['STOP_LOSS_PERCENTAGE'] = stop_loss if stop_loss else '0.02'
        
        # Take Profit
        take_profit = input("Take Profit en % (0.03-0.1, défaut: 0.05): ").strip()
        self.config['TAKE_PROFIT_PERCENTAGE'] = take_profit if take_profit else '0.05'
        
        # Limite de trades
        max_trades = input("Max trades par jour (défaut: 100): ").strip()
        self.config['MAX_DAILY_TRADES'] = max_trades if max_trades else '100'
        
        print("✅ Paramètres de risque configurés")
        
    def configure_environment(self):
        """Configure l'environnement"""
        print("\n🌍 Configuration de l'Environnement")
        print("-" * 35)
        
        env_choice = input("Environnement (development/production, défaut: development): ").strip()
        self.config['FLASK_ENV'] = env_choice if env_choice else 'development'
        self.config['FLASK_DEBUG'] = 'True' if self.config['FLASK_ENV'] == 'development' else 'False'
        
        # Base de données
        db_choice = input("Base de données (sqlite/postgresql, défaut: sqlite): ").strip()
        if db_choice == 'postgresql':
            db_url = input("URL PostgreSQL (ex: postgresql://user:pass@localhost/tradingbot): ").strip()
            self.config['DATABASE_URL'] = db_url
        else:
            self.config['DATABASE_URL'] = 'sqlite:///trading_bot.db'
            
        print("✅ Environnement configuré")
        
    def set_default_values(self):
        """Définit les valeurs par défaut pour les options non configurées"""
        defaults = {
            'RATE_LIMIT_PER_MINUTE': '60',
            'IBM_QUANTUM_TOKEN': 'your-ibm-quantum-token',
            'AWS_BRAKET_ACCESS_KEY': 'your-aws-braket-access-key',
            'AWS_BRAKET_SECRET_KEY': 'your-aws-braket-secret-key'
        }
        
        for key, value in defaults.items():
            if key not in self.config:
                self.config[key] = value
                
    def create_env_file(self):
        """Crée le fichier .env avec la configuration"""
        print("\n💾 Création du fichier .env...")
        
        env_content = f"""# Configuration générée automatiquement le {os.popen('date').read().strip()}
# TradingBot Pro 2025 - Configuration API

# Configuration de l'application
FLASK_ENV={self.config['FLASK_ENV']}
FLASK_DEBUG={self.config['FLASK_DEBUG']}
SECRET_KEY={self.config['SECRET_KEY']}

# Configuration de la base de données
DATABASE_URL={self.config['DATABASE_URL']}

# Configuration des APIs de trading
BINANCE_API_KEY={self.config['BINANCE_API_KEY']}
BINANCE_SECRET_KEY={self.config['BINANCE_SECRET_KEY']}
COINBASE_API_KEY={self.config['COINBASE_API_KEY']}
COINBASE_SECRET_KEY={self.config['COINBASE_SECRET_KEY']}

# Configuration des services quantiques (optionnel)
IBM_QUANTUM_TOKEN={self.config['IBM_QUANTUM_TOKEN']}
AWS_BRAKET_ACCESS_KEY={self.config['AWS_BRAKET_ACCESS_KEY']}
AWS_BRAKET_SECRET_KEY={self.config['AWS_BRAKET_SECRET_KEY']}

# Configuration des alertes
TELEGRAM_BOT_TOKEN={self.config['TELEGRAM_BOT_TOKEN']}
TELEGRAM_CHAT_ID={self.config['TELEGRAM_CHAT_ID']}
DISCORD_WEBHOOK_URL={self.config['DISCORD_WEBHOOK_URL']}

# Configuration de sécurité
JWT_SECRET_KEY={self.config['JWT_SECRET_KEY']}
RATE_LIMIT_PER_MINUTE={self.config['RATE_LIMIT_PER_MINUTE']}
MAX_DAILY_TRADES={self.config['MAX_DAILY_TRADES']}

# Configuration de risque
MAX_POSITION_SIZE={self.config['MAX_POSITION_SIZE']}
STOP_LOSS_PERCENTAGE={self.config['STOP_LOSS_PERCENTAGE']}
TAKE_PROFIT_PERCENTAGE={self.config['TAKE_PROFIT_PERCENTAGE']}
"""

        with open(self.env_file, 'w') as f:
            f.write(env_content)
            
        # Sécuriser le fichier
        os.chmod(self.env_file, 0o600)  # Lecture/écriture pour le propriétaire seulement
        
        print("✅ Fichier .env créé et sécurisé")
        
    def test_configuration(self):
        """Teste la configuration"""
        print("\n🧪 Test de la Configuration")
        print("-" * 27)
        
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            # Test des variables d'environnement
            secret_key = os.getenv('SECRET_KEY')
            if secret_key and secret_key != 'your-secret-key-here':
                print("✅ Variables d'environnement chargées")
            else:
                print("❌ Problème de chargement des variables")
                return False
                
            # Test de connexion CCXT (optionnel)
            try:
                import ccxt
                print("✅ Bibliothèque CCXT disponible")
                
                # Test Binance en mode sandbox si configuré
                if (self.config['BINANCE_API_KEY'] != 'your-binance-api-key' and 
                    self.config['BINANCE_SECRET_KEY'] != 'your-binance-secret-key'):
                    try:
                        exchange = ccxt.binance({
                            'apiKey': self.config['BINANCE_API_KEY'],
                            'secret': self.config['BINANCE_SECRET_KEY'],
                            'sandbox': True,  # Mode test
                            'enableRateLimit': True,
                        })
                        # Test simple de connexion
                        exchange.load_markets()
                        print("✅ Connexion Binance (sandbox) réussie")
                    except Exception as e:
                        print(f"⚠️  Attention: Problème de connexion Binance: {str(e)[:50]}...")
                        
            except ImportError:
                print("⚠️  CCXT non installé - les connexions aux exchanges ne peuvent pas être testées")
                
            return True
            
        except Exception as e:
            print(f"❌ Erreur de test: {e}")
            return False
            
    def display_summary(self):
        """Affiche un résumé de la configuration"""
        print("\n📋 Résumé de la Configuration")
        print("=" * 30)
        
        configured_apis = []
        if self.config['BINANCE_API_KEY'] != 'your-binance-api-key':
            configured_apis.append("✅ Binance")
        else:
            configured_apis.append("⚪ Binance (non configuré)")
            
        if self.config['COINBASE_API_KEY'] != 'your-coinbase-api-key':
            configured_apis.append("✅ Coinbase")
        else:
            configured_apis.append("⚪ Coinbase (non configuré)")
            
        if self.config['TELEGRAM_BOT_TOKEN'] != 'your-telegram-bot-token':
            configured_apis.append("✅ Telegram")
        else:
            configured_apis.append("⚪ Telegram (non configuré)")
            
        if self.config['DISCORD_WEBHOOK_URL'] != 'your-discord-webhook-url':
            configured_apis.append("✅ Discord")
        else:
            configured_apis.append("⚪ Discord (non configuré)")
            
        for api in configured_apis:
            print(f"  {api}")
            
        print(f"\n🌍 Environnement: {self.config['FLASK_ENV']}")
        print(f"🗄️  Base de données: {self.config['DATABASE_URL'].split('://')[0]}")
        print(f"⚖️  Risque max position: {self.config['MAX_POSITION_SIZE']}")
        print(f"🛑 Stop Loss: {self.config['STOP_LOSS_PERCENTAGE']}")
        print(f"🎯 Take Profit: {self.config['TAKE_PROFIT_PERCENTAGE']}")
        
    def run_configuration(self):
        """Lance le processus de configuration complet"""
        self.display_welcome()
        
        # Vérification du fichier existant
        if self.env_file.exists():
            overwrite = input("Un fichier .env existe déjà. Le remplacer ? (o/N): ").lower().strip()
            if overwrite != 'o':
                print("❌ Configuration annulée")
                return False
                
        try:
            self.generate_secure_keys()
            self.configure_environment()
            self.configure_trading_apis()
            self.configure_notifications()
            self.configure_risk_parameters()
            self.set_default_values()
            self.create_env_file()
            
            if self.test_configuration():
                self.display_summary()
                print("\n🎉 Configuration terminée avec succès !")
                print("\n📝 Prochaines étapes:")
                print("1. Vérifiez le fichier .env créé")
                print("2. Testez la connexion aux exchanges")
                print("3. Lancez l'application avec: python run_trading_session.py start")
                return True
            else:
                print("\n⚠️  Configuration créée avec des avertissements")
                return False
                
        except KeyboardInterrupt:
            print("\n❌ Configuration interrompue par l'utilisateur")
            return False
        except Exception as e:
            print(f"\n❌ Erreur lors de la configuration: {e}")
            return False

def main():
    """Point d'entrée principal"""
    if len(sys.argv) > 1 and sys.argv[1] == '--auto':
        # Mode automatique avec valeurs par défaut
        manager = APIConfigurationManager()
        manager.generate_secure_keys()
        manager.config.update({
            'FLASK_ENV': 'development',
            'FLASK_DEBUG': 'True',
            'DATABASE_URL': 'sqlite:///trading_bot.db',
            'BINANCE_API_KEY': 'your-binance-api-key',
            'BINANCE_SECRET_KEY': 'your-binance-secret-key',
            'COINBASE_API_KEY': 'your-coinbase-api-key',
            'COINBASE_SECRET_KEY': 'your-coinbase-secret-key',
            'TELEGRAM_BOT_TOKEN': 'your-telegram-bot-token',
            'TELEGRAM_CHAT_ID': 'your-telegram-chat-id',
            'DISCORD_WEBHOOK_URL': 'your-discord-webhook-url',
            'MAX_POSITION_SIZE': '0.05',
            'STOP_LOSS_PERCENTAGE': '0.02',
            'TAKE_PROFIT_PERCENTAGE': '0.05',
            'MAX_DAILY_TRADES': '100',
            'RATE_LIMIT_PER_MINUTE': '60'
        })
        manager.set_default_values()
        manager.create_env_file()
        print("✅ Configuration automatique terminée")
    else:
        # Mode interactif
        manager = APIConfigurationManager()
        manager.run_configuration()

if __name__ == "__main__":
    main()
