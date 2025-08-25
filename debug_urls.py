#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vérification complète des URLs utilisées par CCXT Coinbase
"""

import ccxt
import sys
import os

# Ajouter le répertoire parent pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.api_config import API_CONFIG

def check_all_urls():
    """Vérifier toutes les URLs utilisées par l'exchange"""
    print("🔍 ANALYSE COMPLÈTE DES URLs COINBASE")
    print("=" * 50)
    
    # Test 1: Configuration actuelle
    print("📍 TEST 1: Configuration actuelle")
    try:
        exchange = ccxt.coinbase({
            'apiKey': API_CONFIG['coinbase_api_key'],
            'secret': API_CONFIG['coinbase_api_secret'],
            'passphrase': API_CONFIG['coinbase_passphrase'],
            'sandbox': False,
            'enableRateLimit': True,
        })
        
        print(f"🌐 URLs par défaut CCXT:")
        for key, url in exchange.urls.items():
            if isinstance(url, dict):
                print(f"   {key}:")
                for subkey, suburl in url.items():
                    print(f"     {subkey}: {suburl}")
            else:
                print(f"   {key}: {url}")
        print()
        
    except Exception as e:
        print(f"❌ Erreur test 1: {e}\n")
    
    # Test 2: Configuration avec URLs forcées
    print("📍 TEST 2: Configuration avec URLs forcées")
    try:
        exchange = ccxt.coinbase({
            'apiKey': API_CONFIG['coinbase_api_key'],
            'secret': API_CONFIG['coinbase_api_secret'],
            'passphrase': API_CONFIG['coinbase_passphrase'],
            'sandbox': False,
            'enableRateLimit': True,
            'urls': {
                'api': {
                    'public': 'https://api.exchange.coinbase.com',
                    'private': 'https://api.exchange.coinbase.com',
                }
            }
        })
        
        print(f"🌐 URLs après modification:")
        for key, url in exchange.urls.items():
            if isinstance(url, dict):
                print(f"   {key}:")
                for subkey, suburl in url.items():
                    print(f"     {subkey}: {suburl}")
            else:
                print(f"   {key}: {url}")
        print()
        
        # Test de connexion
        balance = exchange.fetch_balance()
        print("✅ Connexion réussie avec URLs forcées")
        
    except Exception as e:
        print(f"❌ Erreur test 2: {e}\n")
    
    # Test 3: Affichage de la configuration complète
    print("📍 TEST 3: Vérification sandbox flag")
    try:
        exchange = ccxt.coinbase({
            'apiKey': API_CONFIG['coinbase_api_key'],
            'secret': API_CONFIG['coinbase_api_secret'],
            'passphrase': API_CONFIG['coinbase_passphrase'],
            'sandbox': False,
            'enableRateLimit': True,
        })
        
        print(f"🔧 Sandbox mode: {exchange.sandbox}")
        print(f"🔧 ID Exchange: {exchange.id}")
        print(f"🔧 Version: {exchange.version if hasattr(exchange, 'version') else 'N/A'}")
        
        # Vérifier si la méthode describe existe
        if hasattr(exchange, 'describe'):
            description = exchange.describe()
            if 'urls' in description:
                print(f"🔧 URLs de base dans describe:")
                for key, url in description['urls'].items():
                    if isinstance(url, dict):
                        print(f"   {key}:")
                        for subkey, suburl in url.items():
                            print(f"     {subkey}: {suburl}")
                    else:
                        print(f"   {key}: {url}")
        
    except Exception as e:
        print(f"❌ Erreur test 3: {e}")

if __name__ == "__main__":
    check_all_urls()
