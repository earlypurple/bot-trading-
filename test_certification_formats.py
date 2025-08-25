#!/usr/bin/env python3
"""
Test approfondi de la certification avec différents formats
"""

import ccxt
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.api_config import API_CONFIG

def test_certification_formats():
    """Test différents formats de certification"""
    
    print("🔍 TEST APPROFONDI CERTIFICATION")
    print("=" * 60)
    
    # Format actuel
    current_passphrase = API_CONFIG['coinbase_passphrase']
    
    print(f"📋 Passphrase actuelle:")
    print(f"   Longueur: {len(current_passphrase)} caractères")
    print(f"   Format: {current_passphrase[:8]}...{current_passphrase[-8:]}")
    
    # Test différents formats
    test_configs = [
        {
            'name': 'Format 1: Passphrase comme password',
            'config': {
                'apiKey': API_CONFIG['coinbase_api_key'],
                'secret': API_CONFIG['coinbase_api_secret'],
                'password': current_passphrase,
                'sandbox': False,
            }
        },
        {
            'name': 'Format 2: Passphrase comme passphrase',
            'config': {
                'apiKey': API_CONFIG['coinbase_api_key'],
                'secret': API_CONFIG['coinbase_api_secret'],
                'passphrase': current_passphrase,
                'sandbox': False,
            }
        },
        {
            'name': 'Format 3: Headers personnalisés',
            'config': {
                'apiKey': API_CONFIG['coinbase_api_key'],
                'secret': API_CONFIG['coinbase_api_secret'],
                'password': current_passphrase,
                'headers': {
                    'CB-ACCESS-CERTIFICATION': 'TBPRO2025-1756037390'
                },
                'sandbox': False,
            }
        }
    ]
    
    for i, test in enumerate(test_configs, 1):
        print(f"\n{i}️⃣ {test['name']}")
        print("-" * 40)
        
        try:
            exchange = ccxt.coinbase(test['config'])
            balance = exchange.fetch_balance()
            print("   ✅ Connexion réussie")
            
            # Test mini-ordre
            markets = exchange.load_markets()
            if 'ETH/USD' in markets:
                min_amount = markets['ETH/USD']['limits']['amount']['min']
                test_amount = min_amount * 2
                
                print(f"   📊 Test ordre: {test_amount} ETH")
                
                try:
                    # Test création ordre (annulé immédiatement)
                    ticker = exchange.fetch_ticker('ETH/USD')
                    price = ticker['last']
                    
                    print(f"   💰 Prix ETH: ${price:,.2f}")
                    print("   🧪 Simulation ordre...")
                    
                    # Ici on testerait vraiment l'ordre mais on l'annule pour sécurité
                    # order = exchange.create_order('ETH/USD', 'market', 'sell', test_amount)
                    print("   ⚠️ Test annulé pour sécurité")
                    
                except Exception as e:
                    if "account is not available" in str(e).lower():
                        print("   ❌ ÉCHEC: account is not available")
                    elif "insufficient" in str(e).lower():
                        print("   ✅ SUCCÈS: API autorise trading (fonds insuffisants)")
                        return test['config']  # Configuration qui fonctionne
                    else:
                        print(f"   ⚠️ Autre erreur: {e}")
            
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    print("\n" + "=" * 60)
    print("❌ AUCUNE CONFIGURATION N'A FONCTIONNÉ")
    print("=" * 60)
    print("💡 SOLUTIONS POSSIBLES:")
    print("1. La certification n'est pas encore active côté Coinbase")
    print("2. Il faut activer manuellement le trading API sur coinbase.com")
    print("3. Votre compte nécessite une validation supplémentaire")
    print("4. Le format de certification est différent")
    
    return None

def suggest_manual_activation():
    """Suggestions pour activation manuelle"""
    
    print("\n🔧 ACTIVATION MANUELLE REQUISE")
    print("=" * 50)
    print("📋 Actions à effectuer sur coinbase.com:")
    print("1. Connectez-vous à votre compte")
    print("2. Paramètres → API")
    print("3. Vérifiez que vos clés API ont les permissions 'Trade'")
    print("4. Activez le 'Advanced Trading' si disponible")
    print("5. Confirmez votre certification TBPRO2025-1756037390")
    print("6. Attendez quelques minutes pour activation")
    
    print("\n🎯 Test simple:")
    print("Essayez de faire un trade manuel sur coinbase.com")
    print("Si ça fonctionne manuellement, l'API devrait suivre")

if __name__ == "__main__":
    working_config = test_certification_formats()
    
    if not working_config:
        suggest_manual_activation()
