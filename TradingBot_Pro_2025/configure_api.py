#!/usr/bin/env python3
"""
Guide de Configuration Interactive des API - TradingBot Pro 2025
"""

import os
import sys
from pathlib import Path

def display_main_menu():
    """Affiche le menu principal de configuration"""
    print("\n🔑 Configuration API - TradingBot Pro 2025")
    print("=" * 45)
    print("Que souhaitez-vous configurer ?")
    print()
    print("1. 🟢 Configuration complète interactive")
    print("2. 📈 Seulement les API de trading (Binance/Coinbase)")
    print("3. 📱 Seulement les notifications (Telegram/Discord)")
    print("4. ⚡ Configuration rapide (mode demo)")
    print("5. 🧪 Tester les connexions existantes")
    print("6. 📋 Voir la configuration actuelle")
    print("7. ❌ Quitter")
    print()
    
def show_current_config():
    """Affiche la configuration actuelle"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Aucun fichier .env trouvé")
        return
        
    print("\n📋 Configuration Actuelle")
    print("=" * 25)
    
    # Variables importantes à vérifier
    important_vars = {
        'FLASK_ENV': 'Environnement',
        'BINANCE_API_KEY': 'Binance API',
        'COINBASE_API_KEY': 'Coinbase API', 
        'TELEGRAM_BOT_TOKEN': 'Telegram Bot',
        'DISCORD_WEBHOOK_URL': 'Discord Webhook',
        'DATABASE_URL': 'Base de données',
        'MAX_POSITION_SIZE': 'Taille max position',
        'STOP_LOSS_PERCENTAGE': 'Stop Loss'
    }
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        for var, desc in important_vars.items():
            value = os.getenv(var, 'NON DÉFINI')
            if 'your-' in str(value):
                status = "⚪ Non configuré"
            elif value == 'NON DÉFINI':
                status = "❌ Manquant"
            else:
                # Masquer les clés sensibles
                if 'key' in var.lower() or 'token' in var.lower() or 'secret' in var.lower():
                    display_value = f"{value[:8]}..." if len(value) > 8 else "***"
                else:
                    display_value = value
                status = f"✅ {display_value}"
            
            print(f"  {desc:18}: {status}")
            
    except ImportError:
        print("❌ Impossible de charger la configuration (python-dotenv manquant)")

def quick_demo_setup():
    """Configuration rapide pour démo"""
    print("\n⚡ Configuration Rapide - Mode Démo")
    print("=" * 35)
    print("Cette configuration crée un environnement de test sécurisé.")
    print("Aucune vraie clé API n'est requise.")
    print()
    
    confirm = input("Continuer avec la configuration démo ? (o/N): ").lower().strip()
    if confirm != 'o':
        return
        
    # Configuration démo
    demo_config = """# Configuration DEMO - TradingBot Pro 2025
# ⚠️  NE PAS UTILISER EN PRODUCTION

# Configuration de l'application
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=demo-secret-key-for-testing-only
JWT_SECRET_KEY=demo-jwt-key-for-testing-only

# Configuration de la base de données
DATABASE_URL=sqlite:///demo_trading_bot.db

# Configuration des APIs de trading (DEMO - Pas de vraies clés)
BINANCE_API_KEY=demo-binance-key
BINANCE_SECRET_KEY=demo-binance-secret
COINBASE_API_KEY=demo-coinbase-key
COINBASE_SECRET_KEY=demo-coinbase-secret

# Configuration des alertes (DEMO)
TELEGRAM_BOT_TOKEN=demo-telegram-token
TELEGRAM_CHAT_ID=demo-chat-id
DISCORD_WEBHOOK_URL=demo-discord-webhook

# Configuration de sécurité
RATE_LIMIT_PER_MINUTE=60
MAX_DAILY_TRADES=10

# Configuration de risque (Paramètres sécurisés pour démo)
MAX_POSITION_SIZE=0.001
STOP_LOSS_PERCENTAGE=0.01
TAKE_PROFIT_PERCENTAGE=0.02

# Mode démo activé
DEMO_MODE=true
PAPER_TRADING=true
"""
    
    with open('.env', 'w') as f:
        f.write(demo_config)
        
    os.chmod('.env', 0o600)
    
    print("✅ Configuration démo créée")
    print("📁 Fichier .env créé avec des paramètres de test sécurisés")
    print("🔒 Mode paper trading activé (aucun vrai trading)")
    print("\n📝 Prochaines étapes:")
    print("1. Testez l'application: python run_trading_session.py start")
    print("2. Accédez au dashboard: http://localhost:5000")
    print("3. Configurez de vraies clés API quand vous êtes prêt")

def show_api_guides():
    """Affiche les guides pour obtenir les clés API"""
    print("\n📖 Guides d'Obtention des Clés API")
    print("=" * 35)
    
    guides = {
        "Binance": {
            "url": "https://www.binance.com/",
            "steps": [
                "1. Créez un compte sur Binance",
                "2. Allez dans 'Profil' > 'Sécurité API'",
                "3. Cliquez 'Créer une API'",
                "4. Nommez votre API (ex: TradingBot)",
                "5. Activez 'Trading' et 'Lecture'",
                "6. ❌ N'activez JAMAIS 'Retrait'",
                "7. Ajoutez une restriction IP si possible",
                "8. Sauvegardez votre API Key et Secret Key"
            ]
        },
        "Telegram": {
            "url": "https://t.me/BotFather",
            "steps": [
                "1. Ouvrez Telegram et cherchez @BotFather",
                "2. Tapez /start puis /newbot",
                "3. Donnez un nom à votre bot (ex: MonTradingBot)",
                "4. Donnez un username (ex: mon_trading_bot)",
                "5. Copiez le token fourni",
                "6. Pour le Chat ID: Ajoutez votre bot à un groupe",
                "7. Ou utilisez @userinfobot pour obtenir votre ID"
            ]
        },
        "Discord": {
            "url": "Discord Server Settings",
            "steps": [
                "1. Allez sur votre serveur Discord",
                "2. Paramètres du serveur > Intégrations",
                "3. Créer un Webhook",
                "4. Choisissez le canal de destination", 
                "5. Copiez l'URL du webhook"
            ]
        }
    }
    
    for service, info in guides.items():
        print(f"\n🔸 {service}")
        print(f"   URL: {info['url']}")
        for step in info['steps']:
            print(f"   {step}")

def configure_trading_apis():
    """Configuration interactive des API de trading"""
    print("\n📈 Configuration des API de Trading")
    print("=" * 33)
    
    # Vérifier le fichier existant
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            current_config = f.read()
    else:
        current_config = ""
        
    # Configuration Binance
    print("\n🟡 Binance")
    print("Binance est l'exchange le plus populaire avec de bonnes API.")
    
    if input("Configurer Binance ? (o/N): ").lower().strip() == 'o':
        print("\n📋 Instructions Binance:")
        print("1. Allez sur https://www.binance.com/")
        print("2. Compte > Gestion API > Créer une API")
        print("3. Activez 'Trading' et 'Lecture' uniquement")
        print("4. ❌ N'activez JAMAIS 'Retrait' pour la sécurité")
        print()
        
        api_key = input("Binance API Key: ").strip()
        if api_key:
            secret_key = input("Binance Secret Key: ").strip()
            
            # Mise à jour de la config
            if "BINANCE_API_KEY=" in current_config:
                current_config = current_config.replace("BINANCE_API_KEY=your-binance-api-key", f"BINANCE_API_KEY={api_key}")
                current_config = current_config.replace("BINANCE_SECRET_KEY=your-binance-secret-key", f"BINANCE_SECRET_KEY={secret_key}")
            else:
                current_config += f"\nBINANCE_API_KEY={api_key}\nBINANCE_SECRET_KEY={secret_key}\n"
                
            print("✅ Binance configuré")
    
    # Configuration Coinbase
    print("\n🔵 Coinbase Advanced Trade")
    if input("Configurer Coinbase ? (o/N): ").lower().strip() == 'o':
        print("\n📋 Instructions Coinbase:")
        print("1. Allez sur https://advanced.coinbase.com/")
        print("2. Settings > API > New API Key")
        print("3. Permissions: View + Trade")
        print("4. ⚠️  Pas de passphrase nécessaire")
        print()
        
        api_key = input("Coinbase API Key: ").strip()
        if api_key:
            secret_key = input("Coinbase Secret Key: ").strip()
            
            # Mise à jour de la config
            if "COINBASE_API_KEY=" in current_config:
                current_config = current_config.replace("COINBASE_API_KEY=your-coinbase-api-key", f"COINBASE_API_KEY={api_key}")
                current_config = current_config.replace("COINBASE_SECRET_KEY=your-coinbase-secret-key", f"COINBASE_SECRET_KEY={secret_key}")
            else:
                current_config += f"\nCOINBASE_API_KEY={api_key}\nCOINBASE_SECRET_KEY={secret_key}\n"
                
            print("✅ Coinbase configuré")
    
    # Sauvegarder la configuration
    with open('.env', 'w') as f:
        f.write(current_config)
    os.chmod('.env', 0o600)
    
    print("\n💾 Configuration sauvegardée dans .env")

def configure_notifications():
    """Configuration des notifications"""
    print("\n📱 Configuration des Notifications")
    print("=" * 34)
    
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            current_config = f.read()
    else:
        current_config = ""
        
    # Telegram
    print("\n💬 Telegram Bot")
    if input("Configurer les notifications Telegram ? (o/N): ").lower().strip() == 'o':
        print("\n📋 Instructions Telegram:")
        print("1. Cherchez @BotFather sur Telegram")
        print("2. Tapez /newbot et suivez les instructions")
        print("3. Copiez le token fourni")
        print("4. Pour le Chat ID, ajoutez votre bot à un chat")
        print("5. Ou utilisez @userinfobot pour obtenir votre ID")
        print()
        
        bot_token = input("Telegram Bot Token: ").strip()
        if bot_token:
            chat_id = input("Telegram Chat ID: ").strip()
            
            # Test du bot
            try:
                import requests
                url = f"https://api.telegram.org/bot{bot_token}/getMe"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    bot_info = response.json()
                    if bot_info.get('ok'):
                        print(f"✅ Bot validé: @{bot_info['result']['username']}")
                    else:
                        print("⚠️  Token semble invalide")
                else:
                    print("⚠️  Impossible de valider le token")
            except:
                print("⚠️  Impossible de tester la connexion")
                
            # Mise à jour config
            if "TELEGRAM_BOT_TOKEN=" in current_config:
                current_config = current_config.replace("TELEGRAM_BOT_TOKEN=your-telegram-bot-token", f"TELEGRAM_BOT_TOKEN={bot_token}")
                current_config = current_config.replace("TELEGRAM_CHAT_ID=your-telegram-chat-id", f"TELEGRAM_CHAT_ID={chat_id}")
            else:
                current_config += f"\nTELEGRAM_BOT_TOKEN={bot_token}\nTELEGRAM_CHAT_ID={chat_id}\n"
                
            print("✅ Telegram configuré")
    
    # Discord
    print("\n🎮 Discord Webhook")
    if input("Configurer les notifications Discord ? (o/N): ").lower().strip() == 'o':
        print("\n📋 Instructions Discord:")
        print("1. Allez sur votre serveur Discord")
        print("2. Paramètres du serveur > Intégrations")
        print("3. Créer un Webhook")
        print("4. Choisissez le canal et copiez l'URL")
        print()
        
        webhook_url = input("Discord Webhook URL: ").strip()
        if webhook_url:
            # Test du webhook
            try:
                import requests
                test_data = {'content': '🤖 Test TradingBot Pro 2025'}
                response = requests.post(webhook_url, json=test_data, timeout=5)
                if response.status_code in [200, 204]:
                    print("✅ Webhook testé avec succès")
                else:
                    print("⚠️  Webhook semble invalide")
            except:
                print("⚠️  Impossible de tester le webhook")
                
            # Mise à jour config
            if "DISCORD_WEBHOOK_URL=" in current_config:
                current_config = current_config.replace("DISCORD_WEBHOOK_URL=your-discord-webhook-url", f"DISCORD_WEBHOOK_URL={webhook_url}")
            else:
                current_config += f"\nDISCORD_WEBHOOK_URL={webhook_url}\n"
                
            print("✅ Discord configuré")
    
    # Sauvegarder
    with open('.env', 'w') as f:
        f.write(current_config)
    os.chmod('.env', 0o600)
    
    print("\n💾 Configuration sauvegardée")

def main():
    """Menu principal"""
    while True:
        display_main_menu()
        choice = input("Votre choix (1-7): ").strip()
        
        if choice == '1':
            print("🚀 Lancement de la configuration complète...")
            os.system(f"{sys.executable} setup_api_config.py")
        elif choice == '2':
            configure_trading_apis()
        elif choice == '3':
            configure_notifications()
        elif choice == '4':
            quick_demo_setup()
        elif choice == '5':
            print("🧪 Test des connexions...")
            os.system(f"{sys.executable} test_api_connections.py")
        elif choice == '6':
            show_current_config()
        elif choice == '7':
            print("👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide")
            
        if choice in ['1', '2', '3', '4']:
            print("\n✨ Configuration terminée !")
            print("💡 Conseil: Testez maintenant avec l'option 5")
            
        input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Configuration interrompue")
        sys.exit(0)
