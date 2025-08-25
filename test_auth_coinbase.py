#!/usr/bin/env python3
"""
Test d'authentification Coinbase pour diagnostiquer l'erreur 401
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config'))

import ccxt
from config.api_config import API_CONFIG

def test_auth():
    """Test l'authentification Coinbase step by step"""
    print("🔐 TEST D'AUTHENTIFICATION COINBASE")
    print("=" * 50)
    
    credentials = {
        'apiKey': API_CONFIG['coinbase_api_key'],
        'secret': API_CONFIG['coinbase_api_secret'],
        'password': API_CONFIG['coinbase_passphrase'],
        'sandbox': False
    }
    
    print(f"🔑 API Key: {credentials['apiKey'][:20]}...")
    print(f"🔐 Passphrase: {credentials['password'][:20]}...")
    print(f"📝 Secret: {'*' * 20}")
    
    try:
        # Test 1: Création simple de l'exchange
        print("\n1️⃣  Test création exchange...")
        exchange = ccxt.coinbase(credentials)
        print("✅ Exchange créé")
        
        # Test 2: Test endpoint public
        print("\n2️⃣  Test endpoint public...")
        try:
            markets = exchange.load_markets()
            print(f"✅ Marchés chargés: {len(markets)} paires")
            
            # Vérifier les paires USDC
            usdc_pairs = [symbol for symbol in markets if '/USDC' in symbol]
            print(f"✅ Paires USDC disponibles: {len(usdc_pairs)}")
            if usdc_pairs:
                print(f"   Exemples: {', '.join(usdc_pairs[:5])}")
            
        except Exception as e:
            print(f"❌ Erreur marchés: {e}")
        
        # Test 3: Test endpoint privé simple
        print("\n3️⃣  Test endpoint privé (balance)...")
        try:
            balance = exchange.fetch_balance()
            print("✅ Balance récupérée avec succès")
            
            # Afficher les cryptos avec balance
            cryptos_with_balance = []
            for currency, amounts in balance.items():
                if currency not in ['info', 'free', 'used', 'total']:
                    total = amounts.get('total', 0)
                    if total > 0:
                        cryptos_with_balance.append(f"{currency}: {total}")
            
            print(f"💰 Cryptos avec balance: {len(cryptos_with_balance)}")
            for crypto in cryptos_with_balance[:10]:
                print(f"   {crypto}")
                
        except Exception as e:
            print(f"❌ Erreur balance: {e}")
            print(f"   Type d'erreur: {type(e).__name__}")
            
            # Analyser l'erreur spécifiquement
            error_str = str(e)
            if "401" in error_str:
                print("   🚨 PROBLÈME D'AUTHENTIFICATION DÉTECTÉ")
                if "Unauthorized" in error_str:
                    print("   💡 Les credentials ne sont pas acceptés par l'API")
                    print("   🔧 ACTIONS À VÉRIFIER:")
                    print("      1. Vérifier que l'API key est bien active sur Coinbase")
                    print("      2. Vérifier que les permissions 'view', 'trade', 'transfer' sont activées")
                    print("      3. Vérifier que l'API n'est pas en mode sandbox")
                    print("      4. Vérifier la date/heure système (authentification basée sur timestamp)")
            elif "403" in error_str:
                print("   🚨 PROBLÈME DE PERMISSIONS")
                print("   💡 L'API key est valide mais n'a pas les bonnes permissions")
            
        # Test 4: Test d'info système
        print("\n4️⃣  Info système...")
        import time
        print(f"   Timestamp actuel: {int(time.time())}")
        print(f"   Version CCXT: {ccxt.__version__}")
        
        # Test 5: Test simple avec autre méthode
        print("\n5️⃣  Test méthode alternative...")
        try:
            # Essayer fetch_trading_fees (plus léger)
            fees = exchange.fetch_trading_fees()
            print("✅ Trading fees récupérés")
        except Exception as e:
            print(f"❌ Erreur fees: {e}")
        
    except Exception as e:
        print(f"❌ ERREUR CRÉATION EXCHANGE: {e}")

if __name__ == "__main__":
    test_auth()
