#!/usr/bin/env python3
"""
Script de test des connexions API pour TradingBot Pro 2025
"""

import os
import sys
import asyncio
from dotenv import load_dotenv
import requests
import time

class APIConnectionTester:
    def __init__(self):
        load_dotenv()
        self.results = {}
        
    def test_binance_connection(self):
        """Test de connexion à Binance"""
        print("🔄 Test de connexion Binance...")
        
        api_key = os.getenv('BINANCE_API_KEY')
        secret_key = os.getenv('BINANCE_SECRET_KEY')
        
        if not api_key or api_key == 'your-binance-api-key':
            self.results['binance'] = "⚪ Non configuré"
            return False
            
        try:
            import ccxt
            exchange = ccxt.binance({
                'apiKey': api_key,
                'secret': secret_key,
                'sandbox': True,  # Mode test
                'enableRateLimit': True,
            })
            
            # Test de connexion
            balance = exchange.fetch_balance()
            markets = exchange.load_markets()
            
            self.results['binance'] = f"✅ Connecté ({len(markets)} marchés disponibles)"
            return True
            
        except Exception as e:
            self.results['binance'] = f"❌ Erreur: {str(e)[:50]}..."
            return False
            
    def test_coinbase_connection(self):
        """Test de connexion à Coinbase Advanced Trade"""
        print("🔄 Test de connexion Coinbase...")
        
        api_key = os.getenv('COINBASE_API_KEY')
        secret_key = os.getenv('COINBASE_SECRET_KEY')
        
        if not api_key or api_key == 'your-coinbase-api-key':
            self.results['coinbase'] = "⚪ Non configuré"
            return False
            
        try:
            import ccxt
            exchange = ccxt.coinbaseadvanced({
                'apiKey': api_key,
                'secret': secret_key,
                'enableRateLimit': True,
            })
            
            # Test de connexion simple
            balance = exchange.fetch_balance()
            
            self.results['coinbase'] = f"✅ Connecté ({len(balance)} actifs disponibles)"
            return True
            
        except Exception as e:
            self.results['coinbase'] = f"❌ Erreur: {str(e)[:50]}..."
            return False
            
    def test_telegram_bot(self):
        """Test du bot Telegram"""
        print("🔄 Test du bot Telegram...")
        
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not bot_token or bot_token == 'your-telegram-bot-token':
            self.results['telegram'] = "⚪ Non configuré"
            return False
            
        try:
            # Test de l'API Telegram
            url = f"https://api.telegram.org/bot{bot_token}/getMe"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                bot_info = response.json()
                if bot_info['ok']:
                    bot_name = bot_info['result']['username']
                    self.results['telegram'] = f"✅ Bot @{bot_name} connecté"
                    
                    # Test d'envoi de message si chat_id disponible
                    if chat_id and chat_id != 'your-telegram-chat-id':
                        message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                        data = {
                            'chat_id': chat_id,
                            'text': '🤖 Test de connexion TradingBot Pro 2025 - ✅ Succès!'
                        }
                        msg_response = requests.post(message_url, json=data, timeout=10)
                        if msg_response.status_code == 200:
                            self.results['telegram'] += " (message envoyé)"
                    
                    return True
                else:
                    self.results['telegram'] = "❌ Token invalide"
                    return False
            else:
                self.results['telegram'] = f"❌ Erreur HTTP {response.status_code}"
                return False
                
        except Exception as e:
            self.results['telegram'] = f"❌ Erreur: {str(e)[:50]}..."
            return False
            
    def test_discord_webhook(self):
        """Test du webhook Discord"""
        print("🔄 Test du webhook Discord...")
        
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        
        if not webhook_url or webhook_url == 'your-discord-webhook-url':
            self.results['discord'] = "⚪ Non configuré"
            return False
            
        try:
            # Test d'envoi de message Discord
            data = {
                'content': '🤖 Test de connexion TradingBot Pro 2025 - ✅ Succès!',
                'username': 'TradingBot Pro'
            }
            
            response = requests.post(webhook_url, json=data, timeout=10)
            
            if response.status_code in [200, 204]:
                self.results['discord'] = "✅ Webhook fonctionnel"
                return True
            else:
                self.results['discord'] = f"❌ Erreur HTTP {response.status_code}"
                return False
                
        except Exception as e:
            self.results['discord'] = f"❌ Erreur: {str(e)[:50]}..."
            return False
            
    def test_database_connection(self):
        """Test de connexion à la base de données"""
        print("🔄 Test de connexion base de données...")
        
        try:
            from sqlalchemy import create_engine
            from sqlalchemy.sql import text
            
            database_url = os.getenv('DATABASE_URL', 'sqlite:///trading_bot.db')
            engine = create_engine(database_url)
            
            # Test de connexion simple
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                row = result.fetchone()
                
            self.results['database'] = f"✅ Connecté ({database_url.split('://')[0]})"
            return True
            
        except Exception as e:
            self.results['database'] = f"❌ Erreur: {str(e)[:50]}..."
            return False
            
    def test_environment_variables(self):
        """Test des variables d'environnement"""
        print("🔄 Test des variables d'environnement...")
        
        required_vars = [
            'SECRET_KEY', 'JWT_SECRET_KEY', 'FLASK_ENV',
            'MAX_POSITION_SIZE', 'STOP_LOSS_PERCENTAGE', 'TAKE_PROFIT_PERCENTAGE'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
                
        if missing_vars:
            self.results['environment'] = f"❌ Variables manquantes: {', '.join(missing_vars)}"
            return False
        else:
            self.results['environment'] = f"✅ Toutes les variables configurées"
            return True
            
    def test_python_dependencies(self):
        """Test des dépendances Python"""
        print("🔄 Test des dépendances Python...")
        
        required_modules = [
            ('flask', 'flask'), 
            ('ccxt', 'ccxt'), 
            ('pandas', 'pandas'), 
            ('numpy', 'numpy'), 
            ('scikit-learn', 'sklearn'),
            ('sqlalchemy', 'sqlalchemy'), 
            ('requests', 'requests'), 
            ('python-dotenv', 'dotenv')
        ]
        
        missing_modules = []
        for display_name, import_name in required_modules:
            try:
                __import__(import_name)
            except ImportError:
                missing_modules.append(display_name)
                
        if missing_modules:
            self.results['dependencies'] = f"❌ Modules manquants: {', '.join(missing_modules)}"
            return False
        else:
            self.results['dependencies'] = f"✅ Tous les modules installés"
            return True
            
    def run_all_tests(self):
        """Lance tous les tests"""
        print("\n🧪 Test des Connexions API - TradingBot Pro 2025")
        print("=" * 55)
        
        tests = [
            ('Variables d\'environnement', self.test_environment_variables),
            ('Dépendances Python', self.test_python_dependencies),
            ('Base de données', self.test_database_connection),
            ('Binance API', self.test_binance_connection),
            ('Coinbase API', self.test_coinbase_connection),
            ('Telegram Bot', self.test_telegram_bot),
            ('Discord Webhook', self.test_discord_webhook),
        ]
        
        total_tests = len(tests)
        passed_tests = 0
        
        for test_name, test_func in tests:
            print(f"\n📋 {test_name}")
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                self.results[test_name.lower().replace(' ', '_')] = f"❌ Exception: {e}"
                
        # Affichage des résultats
        print("\n📊 Résultats des Tests")
        print("=" * 25)
        
        for test_name, result in self.results.items():
            print(f"  {test_name.replace('_', ' ').title()}: {result}")
            
        # Résumé
        print(f"\n🎯 Résumé: {passed_tests}/{total_tests} tests réussis")
        
        if passed_tests == total_tests:
            print("🎉 Tous les tests sont passés ! Le bot est prêt à fonctionner.")
            return True
        elif passed_tests >= total_tests * 0.7:
            print("⚠️  La plupart des tests sont passés. Vérifiez les erreurs ci-dessus.")
            return True
        else:
            print("❌ Plusieurs tests ont échoué. Veuillez corriger la configuration.")
            return False
            
    def generate_test_report(self):
        """Génère un rapport de test détaillé"""
        report_file = "api_test_report.txt"
        
        with open(report_file, 'w') as f:
            f.write("Rapport de Test API - TradingBot Pro 2025\n")
            f.write("=" * 45 + "\n")
            f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for test_name, result in self.results.items():
                f.write(f"{test_name.replace('_', ' ').title()}: {result}\n")
                
        print(f"\n📄 Rapport sauvegardé dans {report_file}")

def main():
    """Point d'entrée principal"""
    if not os.path.exists('.env'):
        print("❌ Fichier .env non trouvé!")
        print("Lancez d'abord: python setup_api_config.py")
        sys.exit(1)
        
    tester = APIConnectionTester()
    success = tester.run_all_tests()
    
    if '--report' in sys.argv:
        tester.generate_test_report()
        
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
