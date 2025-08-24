#!/usr/bin/env python3
"""
🔧 CONFIGURATEUR CLÉS API COINBASE - TRADINGBOT PRO 2025
========================================================
🔐 Assistant de configuration interactif
⚡ Configuration rapide et sécurisée

🎯 Fonctionnalités:
- 📝 Saisie interactive des clés API
- 🔒 Validation des clés
- 🧪 Test de connexion automatique
- 💾 Sauvegarde sécurisée
"""

import os
import sys
import json
import getpass
from pathlib import Path

# Ajouter le path pour importer nos modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from exchanges.coinbase_connector import CoinbaseConnector
    from config.coinbase_config import ConfigManager
except ImportError as e:
    print(f"❌ Erreur import: {e}")
    print("💡 Assurez-vous d'être dans le bon répertoire")
    sys.exit(1)

class CoinbaseSetup:
    """Assistant de configuration Coinbase"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.config_file = Path("coinbase_keys.json")
    
    def welcome(self):
        """Message de bienvenue"""
        print("🔧 CONFIGURATEUR COINBASE API")
        print("=" * 40)
        print("🎯 Configuration de vos clés API Coinbase")
        print("🔐 Données stockées en local de façon sécurisée")
        print()
        print("📋 Vous aurez besoin de:")
        print("   • Clé API (API Key)")
        print("   • Secret API (API Secret)")
        print("   • Passphrase")
        print()
        print("🌐 Obtenez vos clés sur: https://pro.coinbase.com/profile/api")
        print("=" * 40)
        print()
    
    def get_api_credentials(self, environment: str = "sandbox") -> dict:
        """
        Récupère les clés API de l'utilisateur
        
        Args:
            environment: 'sandbox' ou 'production'
            
        Returns:
            Dictionnaire avec les clés
        """
        env_name = "🧪 SANDBOX (Test)" if environment == "sandbox" else "🚀 PRODUCTION (Réel)"
        
        print(f"📝 Configuration {env_name}")
        print("-" * 30)
        
        if environment == "production":
            print("⚠️ ATTENTION: Mode production = ARGENT RÉEL !")
            print("💡 Recommandé: Commencez par le sandbox")
            confirm = input("Continuer en production? (y/N): ")
            if confirm.lower() != 'y':
                return None
        
        try:
            api_key = input("🔑 API Key: ").strip()
            if not api_key:
                print("❌ API Key requise")
                return None
            
            api_secret = getpass.getpass("🔐 API Secret: ").strip()
            if not api_secret:
                print("❌ API Secret requis")
                return None
            
            passphrase = getpass.getpass("🗝️ Passphrase: ").strip()
            if not passphrase:
                print("❌ Passphrase requise")
                return None
            
            return {
                "api_key": api_key,
                "api_secret": api_secret,
                "passphrase": passphrase,
                "sandbox": environment == "sandbox"
            }
        
        except KeyboardInterrupt:
            print("\n🛑 Configuration annulée")
            return None
        except Exception as e:
            print(f"❌ Erreur saisie: {e}")
            return None
    
    def test_connection(self, config: dict) -> bool:
        """
        Test la connexion avec les clés fournies
        
        Args:
            config: Configuration à tester
            
        Returns:
            True si connexion OK
        """
        print("\n🔍 Test de connexion...")
        
        try:
            connector = CoinbaseConnector(
                api_key=config["api_key"],
                api_secret=config["api_secret"],
                passphrase=config["passphrase"],
                sandbox=config["sandbox"]
            )
            
            result = connector.test_connection()
            
            if result["status"] == "success":
                print("✅ Connexion réussie !")
                print(f"🔐 Authentifié: {result['authenticated']}")
                print(f"📊 Produits disponibles: {result.get('products_count', 0)}")
                if result.get('accounts_count'):
                    print(f"💰 Comptes détectés: {result['accounts_count']}")
                return True
            
            elif result["status"] == "partial":
                print("⚠️ Connexion partielle")
                print(f"📝 Message: {result['message']}")
                return True
            
            else:
                print("❌ Échec de connexion")
                print(f"📝 Message: {result['message']}")
                return False
        
        except Exception as e:
            print(f"💥 Erreur test: {e}")
            return False
    
    def save_config(self, sandbox_config: dict = None, production_config: dict = None):
        """
        Sauvegarde la configuration
        
        Args:
            sandbox_config: Config sandbox
            production_config: Config production
        """
        print("\n💾 Sauvegarde de la configuration...")
        
        config_data = {
            "created_at": "2025-08-24",
            "version": "1.0"
        }
        
        if sandbox_config:
            config_data["sandbox"] = sandbox_config
        
        if production_config:
            config_data["production"] = production_config
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            # Sécuriser le fichier (lecture seule pour le propriétaire)
            os.chmod(self.config_file, 0o600)
            
            print(f"✅ Configuration sauvée: {self.config_file}")
            print("🔒 Permissions sécurisées appliquées")
            
            # Créer/mettre à jour .gitignore
            self.update_gitignore()
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
    
    def load_config(self) -> dict:
        """
        Charge la configuration existante
        
        Returns:
            Configuration chargée
        """
        if not self.config_file.exists():
            return {}
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Erreur lecture config: {e}")
            return {}
    
    def update_gitignore(self):
        """Met à jour .gitignore pour exclure les clés"""
        gitignore_file = Path(".gitignore")
        
        patterns_to_add = [
            "coinbase_keys.json",
            "*.key",
            "*.secret",
            ".env.local",
            "my_coinbase_keys.py"
        ]
        
        try:
            # Lire .gitignore existant
            existing_patterns = []
            if gitignore_file.exists():
                with open(gitignore_file, 'r') as f:
                    existing_patterns = f.read().splitlines()
            
            # Ajouter les nouveaux patterns
            new_patterns = []
            for pattern in patterns_to_add:
                if pattern not in existing_patterns:
                    new_patterns.append(pattern)
            
            if new_patterns:
                with open(gitignore_file, 'a') as f:
                    f.write("\n# TradingBot Pro 2025 - Clés API\n")
                    for pattern in new_patterns:
                        f.write(f"{pattern}\n")
                
                print(f"📝 .gitignore mis à jour avec {len(new_patterns)} nouveaux patterns")
        
        except Exception as e:
            print(f"⚠️ Impossible de mettre à jour .gitignore: {e}")
    
    def interactive_setup(self):
        """Configuration interactive complète"""
        
        self.welcome()
        
        # Charger config existante
        existing_config = self.load_config()
        
        if existing_config:
            print("🔍 Configuration existante détectée")
            if "sandbox" in existing_config:
                print("   ✅ Sandbox configuré")
            if "production" in existing_config:
                print("   ✅ Production configuré")
            
            response = input("\nÉcraser la configuration? (y/N): ")
            if response.lower() != 'y':
                print("📋 Configuration conservée")
                return
        
        # Configuration sandbox
        print("\n" + "="*50)
        print("🧪 ÉTAPE 1: Configuration Sandbox (Recommandé)")
        print("="*50)
        
        sandbox_config = None
        setup_sandbox = input("Configurer le sandbox? (Y/n): ")
        if setup_sandbox.lower() != 'n':
            sandbox_config = self.get_api_credentials("sandbox")
            
            if sandbox_config and self.test_connection(sandbox_config):
                print("✅ Sandbox configuré avec succès !")
            else:
                print("❌ Échec configuration sandbox")
                response = input("Continuer quand même? (y/N): ")
                if response.lower() != 'y':
                    return
        
        # Configuration production
        print("\n" + "="*50)
        print("🚀 ÉTAPE 2: Configuration Production (Optionnel)")
        print("="*50)
        
        production_config = None
        setup_production = input("Configurer la production? (y/N): ")
        if setup_production.lower() == 'y':
            production_config = self.get_api_credentials("production")
            
            if production_config and self.test_connection(production_config):
                print("✅ Production configuré avec succès !")
            else:
                print("❌ Échec configuration production")
        
        # Sauvegarde
        if sandbox_config or production_config:
            self.save_config(sandbox_config, production_config)
            
            print("\n" + "="*50)
            print("🎉 CONFIGURATION TERMINÉE !")
            print("="*50)
            print("✅ Clés API sauvegardées")
            print("🔒 Fichier sécurisé créé")
            print("🚀 Prêt pour le trading !")
            print()
            print("💡 Prochaines étapes:")
            print("   1. Lancez le dashboard: python dashboard_server.py")
            print("   2. Ouvrez http://localhost:8888")
            print("   3. Profitez du trading temps réel !")
        else:
            print("\n🛑 Aucune configuration sauvée")
    
    def quick_test(self):
        """Test rapide des clés existantes"""
        
        print("🔍 TEST RAPIDE DES CLÉS")
        print("=" * 30)
        
        config = self.load_config()
        
        if not config:
            print("❌ Aucune configuration trouvée")
            print("💡 Lancez d'abord la configuration: python setup_coinbase.py")
            return
        
        # Test sandbox
        if "sandbox" in config:
            print("\n🧪 Test Sandbox...")
            sandbox_result = self.test_connection(config["sandbox"])
            if not sandbox_result:
                print("❌ Sandbox: Échec")
        
        # Test production
        if "production" in config:
            print("\n🚀 Test Production...")
            prod_result = self.test_connection(config["production"])
            if not prod_result:
                print("❌ Production: Échec")
        
        if not config.get("sandbox") and not config.get("production"):
            print("⚠️ Aucune clé valide configurée")

def main():
    """Fonction principale"""
    
    setup = CoinbaseSetup()
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        setup.quick_test()
    else:
        setup.interactive_setup()

if __name__ == "__main__":
    main()
