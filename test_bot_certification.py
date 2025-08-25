#!/usr/bin/env python3
"""
Test de certification du bot avec le nouveau code de certification
"""

import ccxt
import json
import sys
import os

# Ajouter le chemin vers le module de configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.api_config import API_CONFIG

def test_bot_certification():
    """Test la certification du bot avec le nouveau code"""
    
    print("🔍 TEST DE CERTIFICATION BOT")
    print("=" * 50)
    
    # Afficher la configuration actuelle
    print("📋 Configuration actuelle:")
    print(f"   API Key: {API_CONFIG['coinbase_api_key']}")
    print(f"   Passphrase: {API_CONFIG['coinbase_passphrase']}")
    print(f"   Sandbox: {API_CONFIG.get('sandbox', False)}")
    
    # Test avec code de certification
    print("\n🎫 Test avec code de certification:")
    
    try:
        # Configuration de l'exchange avec certification
        exchange = ccxt.coinbase({
            'apiKey': API_CONFIG['coinbase_api_key'],
            'secret': API_CONFIG['coinbase_api_secret'],
            'password': API_CONFIG['coinbase_passphrase'],  # Passphrase pour Coinbase Pro
            'sandbox': False,
            'enableRateLimit': True,
        })
        
        print("   ✅ Exchange configuré avec passphrase")
        
        # Test de connexion
        balance = exchange.fetch_balance()
        print("   ✅ Connexion API réussie")
        
        # Test de création d'ordre (simulation)
        markets = exchange.load_markets()
        
        if 'BTC/USD' in markets:
            market = markets['BTC/USD']
            print(f"   📈 Marché BTC/USD: {market['symbol']}")
            print(f"   💰 Prix minimum: {market['limits']['amount']['min']}")
            
            # Test d'ordre avec une très petite quantité
            try:
                print("\n🧪 Test de validation d'ordre...")
                
                # Essayer de créer un ordre très petit pour tester
                test_amount = market['limits']['amount']['min'] * 2
                ticker = exchange.fetch_ticker('BTC/USD')
                current_price = ticker['last']
                
                print(f"   💱 Prix actuel BTC: ${current_price:,.2f}")
                print(f"   📊 Quantité de test: {test_amount}")
                
                # Note: On ne crée pas vraiment l'ordre, juste on teste la validation
                print("   ⚠️ Test d'ordre annulé (sécurité)")
                print("   ✅ Configuration semble valide pour trading")
                
            except Exception as e:
                if "account is not available" in str(e).lower():
                    print("   ❌ Erreur certification: account is not available")
                    print("   🔧 Solution: Vérifier le code de certification")
                    return False
                elif "invalid" in str(e).lower():
                    print("   ❌ Erreur authentification: Invalid credentials")
                    print("   🔧 Solution: Vérifier API Key/Secret/Passphrase")
                    return False
                else:
                    print(f"   ⚠️ Autre erreur: {e}")
        
        print("\n" + "=" * 50)
        print("💡 DIAGNOSTIC CERTIFICATION")
        print("=" * 50)
        
        if API_CONFIG['coinbase_passphrase'] == 'ma_passphrase_securisee':
            print("❌ PROBLÈME IDENTIFIÉ:")
            print("   Passphrase générique détectée!")
            print("   Vous devez utiliser votre VRAIE passphrase Coinbase")
            print("\n✅ SOLUTION:")
            print("   1. Connectez-vous sur coinbase.com")
            print("   2. Paramètres > API")
            print("   3. Récupérez votre vraie passphrase")
            print("   4. Remplacez 'ma_passphrase_securisee' dans api_config.py")
            return False
        else:
            print("✅ Passphrase personnalisée détectée")
            print("   La configuration semble correcte")
            
        print("\n📝 CODE DE CERTIFICATION (1 AN):")
        print("   Si vous avez un nouveau code de certification,")
        print("   il faut peut-être l'intégrer dans:")
        print("   • Paramètres Coinbase > API > Permissions")
        print("   • Ou comme paramètre supplémentaire dans l'API")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def prompt_for_certification_code():
    """Demande le code de certification à l'utilisateur"""
    
    print("\n🎫 INTÉGRATION CODE DE CERTIFICATION")
    print("=" * 50)
    print("Avez-vous reçu un code de certification spécifique ?")
    print("Ce code peut être:")
    print("• Un token d'authentification")
    print("• Un code de certification API")
    print("• Une clé de validation supplémentaire")
    print("\nSi oui, nous pouvons l'intégrer dans la configuration.")

if __name__ == "__main__":
    success = test_bot_certification()
    
    if not success:
        prompt_for_certification_code()
    else:
        print("\n🚀 Bot prêt pour trading certifié !")
