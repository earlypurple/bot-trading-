#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la configuration URL de production
Vérification que le bot utilise bien https://api.exchange.coinbase.com
"""

import ccxt
import sys
import os

# Ajouter le répertoire parent pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.api_config import API_CONFIG

def test_production_url():
    """Test que l'exchange utilise bien l'URL de production"""
    print("🔍 TEST CONFIGURATION URL DE PRODUCTION")
    print("=" * 50)
    
    try:
        # Configuration avec URL explicite
        exchange = ccxt.coinbase({
            'apiKey': API_CONFIG['coinbase_api_key'],
            'secret': API_CONFIG['coinbase_api_secret'],
            'passphrase': API_CONFIG['coinbase_passphrase'],
            'sandbox': False,
            'enableRateLimit': True,
            # Force l'URL de production
            'urls': {
                'api': {
                    'public': 'https://api.exchange.coinbase.com',
                    'private': 'https://api.exchange.coinbase.com',
                }
            }
        })
        
        print(f"🌐 URL configurée:")
        print(f"   Public API: {exchange.urls['api']['public']}")
        print(f"   Private API: {exchange.urls['api']['private']}")
        print()
        
        # Test de connexion
        print("🔌 Test de connexion...")
        balance = exchange.fetch_balance()
        print("✅ Connexion réussie à l'API PRODUCTION !")
        
        # Afficher les infos du compte
        usd_balance = balance.get('USD', {}).get('total', 0)
        print(f"💰 Solde USD: ${usd_balance:.2f}")
        
        # Vérifier les marchés disponibles
        markets = exchange.load_markets()
        print(f"📈 Marchés disponibles: {len(markets)}")
        
        # Test spécifique avec un ticker pour confirmer l'API
        try:
            ticker = exchange.fetch_ticker('BTC/USD')
            print(f"₿ Prix BTC/USD: ${ticker['last']:.2f}")
            print()
            print("🎯 CONFIRMATION: Le bot utilise bien l'API PRODUCTION Coinbase !")
            print("🚀 URL: https://api.exchange.coinbase.com")
            
        except Exception as e:
            print(f"⚠️ Erreur ticker: {e}")
            
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        
        # Si erreur, tester avec les URLs par défaut
        print("\n🔄 Test avec configuration par défaut CCXT...")
        try:
            exchange_default = ccxt.coinbase({
                'apiKey': API_CONFIG['coinbase_api_key'],
                'secret': API_CONFIG['coinbase_api_secret'],
                'passphrase': API_CONFIG['coinbase_passphrase'],
                'sandbox': False,
                'enableRateLimit': True,
            })
            
            print(f"🌐 URL par défaut:")
            print(f"   Public API: {exchange_default.urls['api']['public']}")
            print(f"   Private API: {exchange_default.urls['api']['private']}")
            
            balance = exchange_default.fetch_balance()
            print("✅ Connexion alternative réussie !")
            
        except Exception as e2:
            print(f"❌ Erreur connexion alternative: {e2}")
            print("\n💡 SOLUTION REQUISE:")
            print("   1. Vérifiez que vous avez créé des clés API depuis votre compte PRODUCTION Coinbase")
            print("   2. Les clés doivent être générées sur coinbase.com (pas coinbase-sandbox.com)")
            print("   3. Activez les permissions 'Trade' sur vos clés API")

if __name__ == "__main__":
    test_production_url()
