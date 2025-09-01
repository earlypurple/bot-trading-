#!/usr/bin/env python3
"""Test simple du module bot final"""

try:
    print("🧪 TEST DÉMARRAGE BOT FINAL")
    print("1. Import des modules...")
    
    import os
    import sys
    import json
    print("✅ Modules standard OK")
    
    import ccxt
    print("✅ Module ccxt OK")
    
    print("2. Test configuration API...")
    
    config_path = 'cdp_api_key.json'
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        print(f"✅ Config API: {config['name'].split('/')[-1]}")
    else:
        print("❌ Fichier config API manquant")
        sys.exit(1)
    
    print("3. Test initialisation exchange...")
    
    exchange = ccxt.coinbaseadvanced({
        'apiKey': config['name'],
        'secret': config['privateKey'], 
        'passphrase': '',
        'sandbox': False,
        'enableRateLimit': True,
        'timeout': 30000,
        'options': {
            'createMarketBuyOrderRequiresPrice': False,
            'advanced': True,
            'fetchBalance': 'v2PrivateGetAccounts'
        }
    })
    
    print("✅ Exchange initialisé")
    
    print("4. Test connexion API...")
    
    balance = exchange.fetch_balance()
    print("✅ Balance récupérée")
    
    print("5. Test ticker...")
    
    ticker = exchange.fetch_ticker('SOL/USD')
    print(f"✅ SOL/USD: ${ticker['last']:.2f}")
    
    print("\\n🎯 TOUS LES TESTS RÉUSSIS !")
    print("Le problème ne vient pas de l'API")
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()
