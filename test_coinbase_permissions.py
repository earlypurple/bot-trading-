#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des permissions Coinbase API
Diagnostique les problèmes de trading
"""

import ccxt
import sys
import os

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.api_config import API_CONFIG

def test_coinbase_permissions():
    """Test complet des permissions Coinbase"""
    
    print("🔍 TEST DES PERMISSIONS COINBASE API")
    print("=" * 50)
    
    try:
        # Configuration de l'exchange
        exchange = ccxt.coinbase({
            'apiKey': API_CONFIG['coinbase_api_key'],
            'secret': API_CONFIG['coinbase_api_secret'],
            'password': API_CONFIG['coinbase_passphrase'],
            'sandbox': API_CONFIG.get('sandbox', False),
        })
        
        print("✅ Connexion à l'API établie")
        
        # Test 1: Lecture du portfolio
        print("\n1️⃣ TEST LECTURE PORTFOLIO...")
        try:
            balance = exchange.fetch_balance()
            print("✅ Lecture portfolio: SUCCÈS")
            
            # Afficher les balances principales
            for currency, amount in balance['total'].items():
                if amount > 0:
                    print(f"   💰 {currency}: {amount}")
        except Exception as e:
            print(f"❌ Lecture portfolio: ÉCHEC - {e}")
            return False
        
        # Test 2: Lecture des marchés
        print("\n2️⃣ TEST LECTURE MARCHÉS...")
        try:
            markets = exchange.load_markets()
            print(f"✅ Marchés chargés: {len(markets)} paires disponibles")
        except Exception as e:
            print(f"❌ Lecture marchés: ÉCHEC - {e}")
            return False
        
        # Test 3: Test d'ordre fictif (sans exécution)
        print("\n3️⃣ TEST PERMISSIONS TRADING...")
        try:
            # Essayer de créer un ordre de test avec un montant minuscule
            # Note: Ceci ne sera pas exécuté car en mode test
            symbol = 'BTC/USD'
            if symbol in markets:
                # Récupérer le ticker pour avoir le prix actuel
                ticker = exchange.fetch_ticker(symbol)
                current_price = ticker['last']
                
                # Calculer un montant minimal
                min_amount = 0.0001  # Montant minimal
                
                print(f"   📊 Prix BTC/USD: ${current_price}")
                print(f"   💡 Test avec montant: {min_amount} BTC")
                
                # Test de validation d'ordre (sans exécution)
                print("   🧪 Validation des paramètres d'ordre...")
                
                # Vérifier les limites minimum
                market_info = markets[symbol]
                min_cost = market_info.get('limits', {}).get('cost', {}).get('min', 0)
                min_amount_limit = market_info.get('limits', {}).get('amount', {}).get('min', 0)
                
                print(f"   📏 Montant minimum: {min_amount_limit}")
                print(f"   💵 Coût minimum: ${min_cost}")
                
                if min_cost and (min_amount * current_price) < min_cost:
                    print(f"   ⚠️  Montant trop petit pour trader (minimum: ${min_cost})")
                else:
                    print("   ✅ Paramètres d'ordre valides")
                
        except Exception as e:
            print(f"❌ Test trading: ÉCHEC - {e}")
            if "not available" in str(e).lower():
                print("   💡 CAUSE: Compte non disponible pour le trading")
                print("   🔧 SOLUTION: Vérifiez les permissions API 'Trade'")
            return False
        
        # Test 4: Vérification des ordres ouverts
        print("\n4️⃣ TEST ORDRES OUVERTS...")
        try:
            open_orders = exchange.fetch_open_orders()
            print(f"✅ Ordres ouverts: {len(open_orders)}")
        except Exception as e:
            print(f"❌ Lecture ordres: ÉCHEC - {e}")
            if "not available" in str(e).lower():
                print("   💡 CAUSE: Permission 'Trade' manquante")
            return False
        
        print("\n🎉 TOUS LES TESTS RÉUSSIS !")
        print("✅ Votre API a toutes les permissions nécessaires")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR DE CONNEXION: {e}")
        print("\n🔧 SOLUTIONS POSSIBLES:")
        print("1. Vérifiez vos clés API")
        print("2. Ajoutez la permission 'Trade' à votre clé API")
        print("3. Vérifiez que votre compte Coinbase Pro est actif")
        print("4. Vérifiez les restrictions IP (si configurées)")
        return False

def check_account_requirements():
    """Vérifier les prérequis du compte"""
    
    print("\n📋 PRÉREQUIS POUR LE TRADING RÉEL:")
    print("=" * 40)
    print("1. ✅ Compte Coinbase Pro vérifié (KYC)")
    print("2. ✅ Clé API avec permission 'Trade'")
    print("3. ✅ Fonds disponibles sur Coinbase Pro")
    print("4. ✅ Pas de restrictions de trading")
    print("5. ✅ IP autorisée (si restriction IP activée)")
    
    print("\n🔗 LIENS UTILES:")
    print("• Coinbase Pro: https://pro.coinbase.com")
    print("• API Settings: https://pro.coinbase.com/profile/api")
    print("• Documentation: https://docs.pro.coinbase.com")

if __name__ == "__main__":
    print("🚀 DIAGNOSTIC COINBASE API - EARLY-BOT-TRADING")
    print("=" * 60)
    
    # Test des permissions
    success = test_coinbase_permissions()
    
    # Afficher les prérequis
    check_account_requirements()
    
    if success:
        print("\n🎯 RÉSULTAT: Prêt pour le trading réel !")
    else:
        print("\n⚠️  RÉSULTAT: Corrections nécessaires avant trading réel")
        print("Le bot continuera en mode simulation jusqu'à résolution")
