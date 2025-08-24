#!/usr/bin/env python3
"""
🔐 CONFIGURATION API COINBASE ADVANCED TRADE - TRADINGBOT PRO 2025
================================================================
Module interactif pour configurer tes clés API Coinbase Advanced Trade

🚀 Utilisation: python configure_coinbase.py
"""

import os
import sys
import json
from pathlib import Path

def print_header():
    """Affiche l'en-tête du configurateur"""
    print("🔐 CONFIGURATION COINBASE ADVANCED TRADE")
    print("=" * 60)
    print("🚀 TradingBot Pro 2025 - Configuration API")
    print("=" * 60)

def print_instructions():
    """Affiche les instructions pour obtenir les clés API"""
    print("\n📋 INSTRUCTIONS POUR OBTENIR TES CLÉS API:")
    print("-" * 50)
    print("1. 🌐 Va sur: https://cloud.coinbase.com/access/api")
    print("2. 🔑 Clique sur 'Create API Key'")
    print("3. 📱 Sélectionne 'Cloud Trading Keys' (pas Legacy)")
    print("4. ✅ Permissions REQUISES:")
    print("   ✓ wallet:accounts:read - Lire ton portfolio")
    print("   ✓ wallet:trades:read - Lire tes transactions")
    print("   ✓ wallet:orders:read - Lire tes ordres")
    print("   ✓ wallet:orders:create - Passer des ordres (optionnel)")
    print("5. 💾 Sauvegarde tes clés en lieu sûr")
    print("\n⚠️  IMPORTANT:")
    print("   - Utilise les Cloud Trading Keys (Advanced Trade)")
    print("   - PAS les Legacy Exchange Keys (Pro)")
    print("   - Garde tes clés secrètes!")

def get_api_keys():
    """Récupère les clés API de l'utilisateur"""
    print("\n🔑 SAISIE DES CLÉS API:")
    print("-" * 30)
    
    api_key = input("🔐 Entre ta clé API: ").strip()
    
    if not api_key:
        print("❌ Clé API vide!")
        return None, None
    
    api_secret = input("🔒 Entre ton secret API: ").strip()
    
    if not api_secret:
        print("❌ Secret API vide!")
        return None, None
    
    return api_key, api_secret

def validate_keys(api_key: str, api_secret: str):
    """Valide le format des clés"""
    print("\n🔍 VALIDATION DES CLÉS...")
    
    # Validation basique du format
    if len(api_key) < 10:
        print("❌ Clé API trop courte")
        return False
    
    if len(api_secret) < 10:
        print("❌ Secret API trop court")
        return False
    
    print("✅ Format des clés OK")
    return True

def test_connection(api_key: str, api_secret: str):
    """Test la connexion avec les clés fournies"""
    print("\n📡 TEST DE CONNEXION...")
    
    try:
        # Import du connecteur
        sys.path.insert(0, 'src')
        from exchanges.coinbase_advanced import CoinbaseAdvancedConnector
        
        # Création du connecteur
        connector = CoinbaseAdvancedConnector(api_key, api_secret, sandbox=False)
        
        # Test de connexion
        result = connector.test_connection()
        
        if result['status'] == 'success':
            print("✅ CONNEXION RÉUSSIE!")
            print(f"📊 {result['message']}")
            return True
        else:
            print("❌ ÉCHEC DE LA CONNEXION")
            print(f"🔍 Erreur: {result['message']}")
            return False
            
    except Exception as e:
        print(f"❌ ERREUR DE TEST: {e}")
        return False

def save_config(api_key: str, api_secret: str):
    """Sauvegarde la configuration"""
    print("\n💾 SAUVEGARDE DE LA CONFIGURATION...")
    
    # Choix du mode de sauvegarde
    print("📁 Options de sauvegarde:")
    print("1. Variables d'environnement (recommandé)")
    print("2. Fichier de configuration local")
    
    choice = input("🎯 Ton choix (1/2): ").strip()
    
    if choice == "1":
        # Variables d'environnement
        print("\n🌍 CONFIGURATION DES VARIABLES D'ENVIRONNEMENT:")
        print("Ajoute ces lignes à ton ~/.zshrc ou ~/.bashrc :")
        print()
        print(f"export COINBASE_API_KEY='{api_key}'")
        print(f"export COINBASE_API_SECRET='{api_secret}'")
        print("export COINBASE_SANDBOX='false'")
        print()
        print("Puis exécute: source ~/.zshrc")
        
        # Configuration temporaire pour cette session
        os.environ['COINBASE_API_KEY'] = api_key
        os.environ['COINBASE_API_SECRET'] = api_secret
        os.environ['COINBASE_SANDBOX'] = 'false'
        print("✅ Configuré temporairement pour cette session")
        
    elif choice == "2":
        # Fichier local
        config_data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "sandbox": False,
            "configured_at": str(os.times()),
            "note": "GARDEZ CE FICHIER SECRET - NE PAS COMMIT"
        }
        
        config_file = Path("coinbase_config_private.json")
        
        try:
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            print(f"✅ Configuration sauvée dans {config_file}")
            print("⚠️  ATTENTION: Gardez ce fichier secret!")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
    
    else:
        print("❌ Choix invalide")

def show_portfolio_preview(api_key: str, api_secret: str):
    """Affiche un aperçu du portfolio"""
    print("\n💰 APERÇU DE TON PORTFOLIO:")
    print("-" * 40)
    
    try:
        sys.path.insert(0, 'src')
        from exchanges.coinbase_advanced import CoinbaseAdvancedConnector
        
        connector = CoinbaseAdvancedConnector(api_key, api_secret)
        portfolio = connector.get_portfolio_summary()
        
        if portfolio:
            print(f"📊 Nombre de comptes: {portfolio.get('account_count', 0)}")
            
            balances = portfolio.get('balances', {})
            if balances:
                print("💳 Tes soldes:")
                for currency, balance in balances.items():
                    if balance['total'] > 0:
                        print(f"   {currency}: {balance['total']:.8f}")
                        print(f"     └─ Disponible: {balance['available']:.8f}")
            else:
                print("   Aucun solde significatif trouvé")
        else:
            print("❌ Impossible de récupérer le portfolio")
            
    except Exception as e:
        print(f"❌ Erreur portfolio: {e}")

def main():
    """Fonction principale"""
    print_header()
    print_instructions()
    
    # Vérifier si déjà configuré
    existing_key = os.getenv('COINBASE_API_KEY')
    if existing_key:
        print(f"\n✅ Configuration existante détectée")
        print(f"🔑 Clé API: {existing_key[:10]}...{existing_key[-4:]}")
        
        reconfigure = input("🔄 Reconfigurer? (y/N): ").strip().lower()
        if reconfigure not in ['y', 'yes', 'oui']:
            print("✅ Configuration conservée")
            return
    
    # Boucle de configuration
    while True:
        # Saisie des clés
        api_key, api_secret = get_api_keys()
        
        if not api_key or not api_secret:
            retry = input("\n🔄 Réessayer? (y/N): ").strip().lower()
            if retry not in ['y', 'yes', 'oui']:
                print("❌ Configuration annulée")
                return
            continue
        
        # Validation
        if not validate_keys(api_key, api_secret):
            retry = input("\n🔄 Réessayer? (y/N): ").strip().lower()
            if retry not in ['y', 'yes', 'oui']:
                print("❌ Configuration annulée")
                return
            continue
        
        # Test de connexion
        if test_connection(api_key, api_secret):
            # Succès!
            save_config(api_key, api_secret)
            show_portfolio_preview(api_key, api_secret)
            
            print("\n🎉 CONFIGURATION TERMINÉE AVEC SUCCÈS!")
            print("🚀 Ton TradingBot peut maintenant accéder à ton compte Coinbase")
            print("🎛️ Lance le dashboard pour voir tes données en temps réel:")
            print("   python dashboard_server.py")
            break
        else:
            print("\n🔍 VÉRIFICATIONS:")
            print("  - Clés API correctes?")
            print("  - Permissions configurées?")
            print("  - Type de clé: Cloud Trading (pas Legacy)?")
            
            retry = input("\n🔄 Réessayer? (y/N): ").strip().lower()
            if retry not in ['y', 'yes', 'oui']:
                print("❌ Configuration annulée")
                return

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Configuration interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
