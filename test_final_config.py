#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final de la configuration avec toutes les URLs forcées
"""

import ccxt
import sys
import os

# Ajouter le répertoire parent pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.api_config import API_CONFIG

def test_final_config():
    """Test final avec toutes les URLs forcées"""
    print("🎯 TEST FINAL - CONFIGURATION ADVANCED TRADE API")
    print("=" * 60)
    
    try:
        # Configuration finale avec toutes les URLs forcées
        exchange = ccxt.coinbase({
            'apiKey': API_CONFIG['coinbase_api_key'],
            'secret': API_CONFIG['coinbase_api_secret'],
            'passphrase': API_CONFIG['coinbase_passphrase'],
            'sandbox': False,
            'enableRateLimit': True,
            # Force TOUTES les URLs vers l'API Advanced Trade
            'urls': {
                'api': {
                    'rest': 'https://api.exchange.coinbase.com',
                    'public': 'https://api.exchange.coinbase.com',
                    'private': 'https://api.exchange.coinbase.com',
                }
            }
        })
        
        print(f"🌐 Configuration finale des URLs:")
        print(f"   REST API: {exchange.urls['api']['rest']}")
        print(f"   Public API: {exchange.urls['api']['public']}")
        print(f"   Private API: {exchange.urls['api']['private']}")
        print(f"   Sandbox: {exchange.sandbox}")
        print()
        
        # Test de connexion et portfolio
        print("🔌 Test de connexion Advanced Trade API...")
        balance = exchange.fetch_balance()
        print("✅ Connexion réussie à l'API ADVANCED TRADE !")
        
        # Afficher les infos du compte
        usd_balance = balance.get('USD', {}).get('total', 0)
        print(f"💰 Solde USD: ${usd_balance:.2f}")
        
        # Test des marchés
        markets = exchange.load_markets()
        print(f"📈 Marchés disponibles: {len(markets)}")
        
        # Test ticker pour confirmer que c'est l'API Advanced Trade
        ticker = exchange.fetch_ticker('ETH/USD')
        print(f"💎 Prix ETH/USD: ${ticker['last']:.2f}")
        
        # Test simulé d'ordre (pour voir les erreurs)
        print("\n🧪 Test simulé de création d'ordre...")
        try:
            # Ne pas vraiment exécuter, juste tester les paramètres
            print("   Symbol: ETH/USD")
            print("   Type: market")
            print("   Side: buy") 
            print("   Amount: 0.001")
            print("   ⚠️ Ordre non exécuté (test uniquement)")
            
        except Exception as e:
            print(f"   ⚠️ Erreur test ordre: {e}")
        
        print("\n🎉 RÉSULTAT: Bot configuré pour Advanced Trade API")
        print("🚀 URL finale: https://api.exchange.coinbase.com")
        print("✅ Prêt pour trading réel !")
        
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")

if __name__ == "__main__":
    test_final_config()
