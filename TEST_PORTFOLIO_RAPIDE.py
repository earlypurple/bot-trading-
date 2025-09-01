#!/usr/bin/env python3
"""
🚀 TEST RAPIDE PORTFOLIO COINBASE
Version simplifiée pour vérifier que tout fonctionne
"""

import sys
import os

# Ajouter le chemin pour importer la config
sys.path.append('/Users/johan/ia_env/bot-trading-')

try:
    from CONFIGURER_API_COINBASE import API_CONFIG
    print("✅ Configuration chargée")
except ImportError:
    print("❌ Impossible de charger la configuration")
    sys.exit(1)

try:
    import ccxt
    print("✅ CCXT importé")
except ImportError:
    print("❌ CCXT non disponible")
    sys.exit(1)

def test_portfolio():
    print("\n🎯 TEST DU PORTFOLIO COINBASE")
    print("=" * 40)
    
    try:
        # Configuration de l'exchange
        exchange = ccxt.coinbase({
            'apiKey': API_CONFIG['coinbase_api_key'],
            'secret': API_CONFIG['coinbase_api_secret'],
            'sandbox': False,
            'enableRateLimit': True,
        })
        
        print("🔗 Connexion à Coinbase...")
        
        # Test du balance
        balance = exchange.fetch_balance()
        print("✅ Balance récupéré avec succès!")
        
        # Affichage des soldes
        print("\n💰 VOTRE PORTFOLIO:")
        print("-" * 30)
        
        total_usd = 0
        for currency, amount in balance['total'].items():
            if amount > 0:
                print(f"💵 {currency}: {amount}")
                if currency == 'USD':
                    total_usd += amount
        
        print(f"\n🎉 TOTAL USD: ${total_usd:.2f}")
        
        if total_usd > 0:
            print("\n✅ SUCCÈS! Votre portfolio est connecté!")
            print(f"💰 Vous avez ${total_usd:.2f} disponibles")
        else:
            print("\n⚠️  Portfolio connecté mais solde USD à 0")
            print("💡 Vérifiez vos fonds sur Coinbase Advanced")
        
        # Test d'un ticker pour confirmer la connexion
        ticker = exchange.fetch_ticker('BTC/USD')
        print(f"\n📈 Prix BTC actuel: ${ticker['last']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = test_portfolio()
    if success:
        print("\n🎉 CONFIGURATION PARFAITE!")
        print("🚀 Votre bot est prêt à fonctionner!")
    else:
        print("\n❌ Des problèmes persistent")
        print("💡 Vérifiez vos clés API sur Coinbase")
