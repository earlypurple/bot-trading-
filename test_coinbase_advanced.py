#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test avec Coinbase Advanced Trade exchange
"""

import ccxt
import sys
import os

# Ajouter le répertoire parent pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.api_config import API_CONFIG

def test_coinbase_advanced():
    """Test avec l'exchange coinbaseadvanced"""
    print("🚀 TEST COINBASE ADVANCED TRADE")
    print("=" * 50)
    
    try:
        # Test avec coinbaseadvanced
        exchange = ccxt.coinbaseadvanced({
            'apiKey': API_CONFIG['coinbase_api_key'],
            'secret': API_CONFIG['coinbase_api_secret'],
            'passphrase': API_CONFIG['coinbase_passphrase'],
            'sandbox': False,
            'enableRateLimit': True,
        })
        
        print(f"🌐 Exchange: {exchange.id}")
        print(f"🌐 URLs par défaut:")
        for key, url in exchange.urls.items():
            if isinstance(url, dict):
                print(f"   {key}:")
                for subkey, suburl in url.items():
                    print(f"     {subkey}: {suburl}")
            else:
                print(f"   {key}: {url}")
        print()
        
        # Test de connexion
        print("🔌 Test de connexion...")
        balance = exchange.fetch_balance()
        print("✅ Connexion réussie à Coinbase Advanced Trade !")
        
        # Afficher les infos du compte
        usd_balance = balance.get('USD', {}).get('total', 0)
        print(f"💰 Solde USD: ${usd_balance:.2f}")
        
        # Test des marchés
        markets = exchange.load_markets()
        print(f"📈 Marchés disponibles: {len(markets)}")
        
        # Test ticker
        ticker = exchange.fetch_ticker('ETH/USD')
        print(f"💎 Prix ETH/USD: ${ticker['last']:.2f}")
        
        print("\n🎉 SUCCÈS: Coinbase Advanced Trade fonctionne !")
        
    except Exception as e:
        print(f"❌ Erreur Coinbase Advanced: {e}")
        
        # Fallback test avec coinbase normal
        print("\n🔄 Test fallback avec API Coinbase normale...")
        try:
            exchange_normal = ccxt.coinbase({
                'apiKey': API_CONFIG['coinbase_api_key'],
                'secret': API_CONFIG['coinbase_api_secret'],
                'passphrase': API_CONFIG['coinbase_passphrase'],
                'sandbox': False,
                'enableRateLimit': True,
            })
            
            balance = exchange_normal.fetch_balance()
            print("✅ API Coinbase normale fonctionne")
            
            # Test si les ordres sont supportés
            try:
                # Juste tester si l'échange supporte create_order
                if hasattr(exchange_normal, 'create_order'):
                    print("✅ create_order supporté")
                else:
                    print("❌ create_order non supporté")
                    
            except Exception as e2:
                print(f"⚠️ Test create_order: {e2}")
                
        except Exception as e2:
            print(f"❌ Erreur API normale aussi: {e2}")

if __name__ == "__main__":
    test_coinbase_advanced()
