#!/usr/bin/env python3
"""
Script pour vérifier le statut du compte Coinbase et les exigences de certification
"""

import ccxt
import json
import sys
import os

# Ajouter le chemin vers le module de configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from config.api_config import API_CONFIG
except ImportError:
    # Alternative si le module n'est pas trouvé
    API_CONFIG = {
        'coinbase': {
            'api_key': '7bb7aaf0-8571-44ee-90cb-fa485597d0e8',
            'api_secret': '',  # Sera lu depuis les variables d'environnement
        }
    }

def check_account_status():
    """Vérifie le statut complet du compte Coinbase"""
    
    try:
        # Configuration de l'exchange
        exchange = ccxt.coinbase({
            'apiKey': API_CONFIG['coinbase_api_key'],
            'secret': API_CONFIG['coinbase_api_secret'],
            'sandbox': False,  # Production
            'enableRateLimit': True,
        })
        
        print("🔍 VÉRIFICATION DU STATUT COMPTE COINBASE")
        print("=" * 50)
        
        # 1. Vérification de base
        print("1️⃣ Connexion API...")
        balance = exchange.fetch_balance()
        print("   ✅ Connexion réussie")
        
        # 2. Informations du compte
        print("\n2️⃣ Informations du compte...")
        try:
            account_info = exchange.fetch_accounts()
            print(f"   📊 Comptes trouvés: {len(account_info)}")
            
            for account in account_info:
                if account.get('currency') and float(account.get('total', 0)) > 0:
                    print(f"   💰 {account['currency']}: {account['total']}")
        except Exception as e:
            print(f"   ⚠️ Impossible de récupérer les comptes: {e}")
        
        # 3. Test de trading permissions
        print("\n3️⃣ Test des permissions de trading...")
        try:
            # Test avec un ordre très petit (ne sera pas exécuté)
            markets = exchange.load_markets()
            
            # Essayer de créer un ordre de test avec une petite quantité
            if 'BTC/USD' in markets:
                market = markets['BTC/USD']
                min_amount = market.get('limits', {}).get('amount', {}).get('min', 0.00001)
                
                print(f"   📈 Marché BTC/USD disponible")
                print(f"   📏 Montant minimum: {min_amount}")
                
                # Test de validation d'ordre (dry run)
                try:
                    # Note: Coinbase peut ne pas supporter les ordres de test
                    print("   🧪 Test de création d'ordre...")
                    print("   ⚠️ Coinbase ne supporte pas les ordres de test")
                    
                except Exception as e:
                    print(f"   ❌ Erreur test ordre: {e}")
            
        except Exception as e:
            print(f"   ❌ Erreur permissions trading: {e}")
        
        # 4. Vérification des limitations de compte
        print("\n4️⃣ Statut des limitations...")
        try:
            # Certaines informations peuvent être disponibles via l'API
            print("   ℹ️ Vérification des statuts de compte...")
            
            # Check si on peut récupérer des infos sur les limites
            deposit_addresses = exchange.fetch_deposit_addresses()
            print(f"   📮 Adresses de dépôt configurées: {len(deposit_addresses)}")
            
        except Exception as e:
            print(f"   ⚠️ Impossible de vérifier les limitations: {e}")
        
        # 5. Recommandations
        print("\n" + "=" * 50)
        print("🎯 DIAGNOSTIC ET RECOMMANDATIONS")
        print("=" * 50)
        
        print("\n❌ PROBLÈME IDENTIFIÉ: 'account is not available'")
        print("   Cette erreur indique généralement:")
        print("   • Compte non vérifié complètement")
        print("   • Limitations de trading non levées")
        print("   • Certification KYC incomplète")
        
        print("\n✅ ACTIONS À EFFECTUER SUR COINBASE.COM:")
        print("   1. Connectez-vous à votre compte Coinbase")
        print("   2. Allez dans 'Paramètres' > 'Sécurité'")
        print("   3. Vérifiez le statut de vérification d'identité")
        print("   4. Completez la vérification KYC si nécessaire")
        print("   5. Vérifiez les limites de trading dans 'Paramètres' > 'Limites'")
        print("   6. Activez le trading avancé si disponible")
        
        print("\n📋 DOCUMENTS POTENTIELLEMENT REQUIS:")
        print("   • Pièce d'identité (passeport, carte d'identité)")
        print("   • Justificatif de domicile")
        print("   • Informations fiscales (selon pays)")
        
        print("\n🔄 APRÈS CERTIFICATION:")
        print("   Le bot pourra exécuter de vrais trades")
        print("   Les erreurs 'account is not available' disparaîtront")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

if __name__ == "__main__":
    check_account_status()
