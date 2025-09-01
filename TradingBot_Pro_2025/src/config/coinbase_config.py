#!/usr/bin/env python3
"""
🔐 CONFIGURATION API COINBASE - TRADINGBOT PRO 2025
===================================================
⚠️ IMPORTANT: Gardez vos clés API secrètes !
🔒 Ne jamais commit ce fichier avec de vraies clés

📋 Instructions pour obtenir vos clés API Coinbase:

1. 🌐 Connectez-vous à https://pro.coinbase.com
2. ⚙️ Allez dans Settings → API
3. ➕ Créez une nouvelle clé API avec permissions:
   - View (lecture des données)
   - Trade (passage d'ordres) 
   - Transfer (optionnel)
4. 📋 Copiez vos clés dans ce fichier
5. 🔐 Activez 2FA pour plus de sécurité

🛡️ Sécurité:
- Limitez les permissions aux strict nécessaire
- Utilisez d'abord le mode sandbox pour tester
- Ne partagez jamais vos clés API
- Révoquezles clés en cas de compromission
"""

import os
from typing import Dict, Any

# ============================================================================
# 🔑 CONFIGURATION DES CLÉS API
# ============================================================================

# 🧪 SANDBOX (ENVIRONNEMENT DE TEST) - Sûr pour les tests
COINBASE_SANDBOX_CONFIG = {
    "api_key": "",  # ← Votre clé API sandbox ici
    "api_secret": "",  # ← Votre secret API sandbox ici
    "passphrase": "",  # ← Votre passphrase sandbox ici
    "sandbox": True,  # ← Mode test activé
    "description": "Environnement de test Coinbase"
}

# 🚀 PRODUCTION (ENVIRONNEMENT RÉEL) - ⚠️ ARGENT RÉEL !
COINBASE_PRODUCTION_CONFIG = {
    "api_key": "",  # ← Votre clé API production ici (⚠️ ARGENT RÉEL)
    "api_secret": "",  # ← Votre secret API production ici (⚠️ ARGENT RÉEL)
    "passphrase": "",  # ← Votre passphrase production ici (⚠️ ARGENT RÉEL)
    "sandbox": False,  # ← Mode production (ATTENTION !)
    "description": "Environnement de production Coinbase"
}

# ============================================================================
# 🛠️ CONFIGURATION AVANCÉE
# ============================================================================

# Paramètres généraux
TRADING_CONFIG = {
    # Limites de sécurité
    "max_order_size_usd": 1000,  # Montant max par ordre en USD
    "max_daily_trades": 50,      # Nombre max de trades par jour
    "min_balance_usd": 100,      # Solde minimum à conserver
    
    # Cryptos autorisées
    "allowed_symbols": [
        "BTC", "ETH", "ADA", "DOT", "LINK", 
        "SOL", "AVAX", "MATIC", "ATOM", "ALGO"
    ],
    
    # Paramètres de trading
    "default_slippage": 0.005,   # 0.5% de slippage par défaut
    "order_timeout": 300,        # Timeout des ordres en secondes
    "retry_attempts": 3,         # Nombre de tentatives en cas d'échec
    
    # Monitoring
    "update_interval": 5,        # Fréquence de mise à jour (secondes)
    "log_trades": True,          # Enregistrer tous les trades
    "notifications": True        # Activer les notifications
}

# ============================================================================
# 🎛️ GESTION DE CONFIGURATION
# ============================================================================

class ConfigManager:
    """Gestionnaire de configuration sécurisé"""
    
    def __init__(self):
        self.environment = "sandbox"  # Par défaut en mode test
        self._config_cache = {}
    
    def get_coinbase_config(self, environment: str = None) -> Dict[str, Any]:
        """
        Récupère la configuration Coinbase
        
        Args:
            environment: 'sandbox' ou 'production'
            
        Returns:
            Configuration Coinbase
        """
        env = environment or self.environment
        
        if env == "sandbox":
            config = COINBASE_SANDBOX_CONFIG.copy()
        elif env == "production":
            config = COINBASE_PRODUCTION_CONFIG.copy()
        else:
            raise ValueError(f"Environnement inconnu: {env}")
        
        # Vérifier si les variables d'environnement existent
        env_key = f"COINBASE_{env.upper()}_API_KEY"
        env_secret = f"COINBASE_{env.upper()}_API_SECRET"
        env_passphrase = f"COINBASE_{env.upper()}_PASSPHRASE"
        
        # Priorité aux variables d'environnement (plus sécurisé)
        if os.getenv(env_key):
            config["api_key"] = os.getenv(env_key)
        if os.getenv(env_secret):
            config["api_secret"] = os.getenv(env_secret)
        if os.getenv(env_passphrase):
            config["passphrase"] = os.getenv(env_passphrase)
        
        return config
    
    def set_environment(self, environment: str):
        """
        Change l'environnement par défaut
        
        Args:
            environment: 'sandbox' ou 'production'
        """
        if environment not in ["sandbox", "production"]:
            raise ValueError("Environnement doit être 'sandbox' ou 'production'")
        
        self.environment = environment
        print(f"🔄 Environnement changé vers: {environment}")
        
        if environment == "production":
            print("⚠️ ATTENTION: Mode production activé - Argent réel !")
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Valide une configuration
        
        Args:
            config: Configuration à valider
            
        Returns:
            True si valide
        """
        required_fields = ["api_key", "api_secret", "passphrase"]
        
        for field in required_fields:
            if not config.get(field):
                print(f"❌ Champ manquant: {field}")
                return False
        
        print("✅ Configuration valide")
        return True
    
    def get_trading_config(self) -> Dict[str, Any]:
        """
        Récupère la configuration de trading
        
        Returns:
            Configuration de trading
        """
        return TRADING_CONFIG.copy()
    
    def setup_environment_variables(self):
        """
        Guide pour configurer les variables d'environnement
        """
        print("🔐 CONFIGURATION DES VARIABLES D'ENVIRONNEMENT")
        print("=" * 50)
        print()
        print("Pour plus de sécurité, utilisez les variables d'environnement:")
        print()
        print("💻 Dans votre terminal (.bashrc/.zshrc):")
        print("export COINBASE_SANDBOX_API_KEY='votre_cle_sandbox'")
        print("export COINBASE_SANDBOX_API_SECRET='votre_secret_sandbox'")
        print("export COINBASE_SANDBOX_PASSPHRASE='votre_passphrase_sandbox'")
        print()
        print("🚀 Pour la production (⚠️ ARGENT RÉEL):")
        print("export COINBASE_PRODUCTION_API_KEY='votre_cle_prod'")
        print("export COINBASE_PRODUCTION_API_SECRET='votre_secret_prod'")
        print("export COINBASE_PRODUCTION_PASSPHRASE='votre_passphrase_prod'")
        print()
        print("🔄 Puis rechargez: source ~/.bashrc (ou ~/.zshrc)")

# ============================================================================
# 🧪 CONFIGURATION PAR DÉFAUT (MODE DÉMO)
# ============================================================================

def get_demo_config() -> Dict[str, Any]:
    """
    Configuration de démonstration (sans clés réelles)
    
    Returns:
        Configuration pour mode démo
    """
    return {
        "api_key": None,
        "api_secret": None,
        "passphrase": None,
        "sandbox": True,
        "demo_mode": True,
        "description": "Mode démonstration - Données simulées"
    }

# ============================================================================
# 🎯 FONCTIONS UTILITAIRES
# ============================================================================

def create_config_template():
    """Crée un template de configuration vide"""
    
    template = """
# ===================================================
# 🔐 MES CLÉS API COINBASE - PERSONNEL ET CONFIDENTIEL
# ===================================================

# 🧪 SANDBOX (Tests)
COINBASE_SANDBOX_API_KEY = "votre_cle_sandbox_ici"
COINBASE_SANDBOX_API_SECRET = "votre_secret_sandbox_ici"
COINBASE_SANDBOX_PASSPHRASE = "votre_passphrase_sandbox_ici"

# 🚀 PRODUCTION (⚠️ ARGENT RÉEL !)
# COINBASE_PRODUCTION_API_KEY = "votre_cle_production_ici"
# COINBASE_PRODUCTION_API_SECRET = "votre_secret_production_ici"
# COINBASE_PRODUCTION_PASSPHRASE = "votre_passphrase_production_ici"
"""
    
    with open("my_coinbase_keys.py", "w") as f:
        f.write(template)
    
    print("📝 Template créé: my_coinbase_keys.py")
    print("✏️ Éditez ce fichier avec vos vraies clés")
    print("🔒 N'oubliez pas de l'ajouter à .gitignore !")

def verify_api_setup():
    """Vérifie que les API sont correctement configurées"""
    
    print("🔍 VÉRIFICATION CONFIGURATION API")
    print("=" * 40)
    
    config_manager = ConfigManager()
    
    # Test sandbox
    sandbox_config = config_manager.get_coinbase_config("sandbox")
    print(f"🧪 Sandbox configuré: {config_manager.validate_config(sandbox_config)}")
    
    # Test production (optionnel)
    try:
        prod_config = config_manager.get_coinbase_config("production")
        print(f"🚀 Production configuré: {config_manager.validate_config(prod_config)}")
    except:
        print("🚀 Production: Non configuré (optionnel)")
    
    return True

# ============================================================================
# 🚀 FONCTION PRINCIPALE
# ============================================================================

def main():
    """Test de la configuration"""
    
    print("🔐 CONFIGURATION API COINBASE")
    print("=" * 40)
    
    config_manager = ConfigManager()
    
    # Affichage du guide
    config_manager.setup_environment_variables()
    
    print("\n" + "=" * 40)
    
    # Vérification de la configuration
    verify_api_setup()
    
    # Proposition de créer un template
    response = input("\n📝 Créer un template de clés? (y/n): ")
    if response.lower() == 'y':
        create_config_template()

if __name__ == "__main__":
    main()
