#!/usr/bin/env python3
"""
Configurateur avancé des modes de trading Early-Bot-Trading
Permet de personnaliser chaque mode : conservateur, normal, agressif, scalping
"""

import os
import json
import time
from decimal import Decimal

class TradingModeConfigurator:
    def __init__(self):
        self.config_file = "config/api_config.py"
        self.backup_file = "config/api_config_backup.py"
        self.modes = {
            'conservateur': {
                'name': '🛡️ Conservateur',
                'description': 'Trading prudent avec stop-loss stricts',
                'risk_level': 'Ultra Faible',
                'position_size': 0.02,  # 2% du portfolio
                'stop_loss': 0.015,     # 1.5%
                'take_profit': 0.025,   # 2.5%
                'min_trade_amount': 0.50,  # 50 centimes minimum
                'max_trades_per_day': 3,
                'trading_frequency': 0.1,  # 10% de chances par signal
                'require_confirmation': True
            },
            'normal': {
                'name': '⚖️ Normal',
                'description': 'Équilibre entre risque et profit',
                'risk_level': 'Faible',
                'position_size': 0.03,  # 3% du portfolio
                'stop_loss': 0.02,      # 2%
                'take_profit': 0.04,    # 4%
                'min_trade_amount': 0.30,  # 30 centimes minimum
                'max_trades_per_day': 5,
                'trading_frequency': 0.2,  # 20% de chances par signal
                'require_confirmation': False
            },
            'agressif': {
                'name': '🚀 Agressif',
                'description': 'Trading actif avec plus de risques',
                'risk_level': 'Modéré',
                'position_size': 0.05,  # 5% du portfolio
                'stop_loss': 0.03,      # 3%
                'take_profit': 0.06,    # 6%
                'min_trade_amount': 0.20,  # 20 centimes minimum
                'max_trades_per_day': 8,
                'trading_frequency': 0.3,  # 30% de chances par signal
                'require_confirmation': False
            },
            'scalping': {
                'name': '⚡ Scalping',
                'description': 'Trading très rapide petits profits',
                'risk_level': 'Rapide',
                'position_size': 0.01,  # 1% du portfolio
                'stop_loss': 0.005,     # 0.5%
                'take_profit': 0.01,    # 1%
                'min_trade_amount': 0.25,  # 25 centimes pour scalping
                'max_trades_per_day': 20,
                'trading_frequency': 0.5,  # 50% de chances par signal
                'require_confirmation': False
            }
        }
    
    def display_current_config(self):
        """Affiche la configuration actuelle"""
        print("🔧 CONFIGURATION ACTUELLE DES MODES DE TRADING")
        print("=" * 60)
        
        for mode, config in self.modes.items():
            print(f"\n{config['name']} ({mode.upper()})")
            print("-" * 40)
            print(f"  📝 Description: {config['description']}")
            print(f"  🎯 Risque: {config['risk_level']}")
            print(f"  💰 Taille position: {config['position_size']*100:.1f}% du portfolio")
            print(f"  🛑 Stop Loss: {config['stop_loss']*100:.1f}%")
            print(f"  🎯 Take Profit: {config['take_profit']*100:.1f}%")
            print(f"  💵 Montant min: ${config['min_trade_amount']:.2f}")
            print(f"  📊 Max trades/jour: {config['max_trades_per_day']}")
            print(f"  ⚡ Fréquence trading: {config['trading_frequency']*100:.0f}%")
            print(f"  ✅ Confirmation requise: {'Oui' if config['require_confirmation'] else 'Non'}")
    
    def configure_mode(self, mode_name):
        """Configure un mode spécifique"""
        if mode_name not in self.modes:
            print(f"❌ Mode '{mode_name}' non trouvé")
            return
        
        mode = self.modes[mode_name]
        print(f"\n🔧 CONFIGURATION DU MODE {mode['name']}")
        print("=" * 50)
        print("💡 Appuyez sur Entrée pour garder la valeur actuelle")
        
        # Configuration interactive
        try:
            # Position size
            new_position = input(f"💰 Taille position (actuel: {mode['position_size']*100:.1f}%): ")
            if new_position.strip():
                mode['position_size'] = float(new_position) / 100
            
            # Stop loss
            new_stop = input(f"🛑 Stop Loss (actuel: {mode['stop_loss']*100:.1f}%): ")
            if new_stop.strip():
                mode['stop_loss'] = float(new_stop) / 100
            
            # Take profit
            new_profit = input(f"🎯 Take Profit (actuel: {mode['take_profit']*100:.1f}%): ")
            if new_profit.strip():
                mode['take_profit'] = float(new_profit) / 100
            
            # Min trade amount
            new_min = input(f"💵 Montant minimum (actuel: ${mode['min_trade_amount']:.2f}): ")
            if new_min.strip():
                mode['min_trade_amount'] = float(new_min)
            
            # Max trades per day
            new_max = input(f"📊 Max trades/jour (actuel: {mode['max_trades_per_day']}): ")
            if new_max.strip():
                mode['max_trades_per_day'] = int(new_max)
            
            # Trading frequency
            new_freq = input(f"⚡ Fréquence trading (actuel: {mode['trading_frequency']*100:.0f}%): ")
            if new_freq.strip():
                mode['trading_frequency'] = float(new_freq) / 100
            
            print(f"✅ Mode {mode['name']} configuré avec succès!")
            
        except ValueError as e:
            print(f"❌ Erreur de saisie: {e}")
            return
    
    def save_config(self):
        """Sauvegarde la configuration dans le fichier"""
        try:
            # Créer une sauvegarde
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    content = f.read()
                with open(self.backup_file, 'w') as f:
                    f.write(content)
                print(f"💾 Sauvegarde créée: {self.backup_file}")
            
            # Générer le nouveau fichier de configuration
            config_content = self._generate_config_file()
            
            with open(self.config_file, 'w') as f:
                f.write(config_content)
            
            print(f"✅ Configuration sauvegardée dans {self.config_file}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
    
    def _generate_config_file(self):
        """Génère le contenu du fichier de configuration"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        content = f'''"""
Configuration Early-Bot-Trading - Modes de Trading
Générée automatiquement le {timestamp}
"""

# Configuration des clés Coinbase Developer Platform (CDP)
CDP_API_KEY = "organizations/f8df9f96-f27a-4c5c-a096-0a1ee6c77c94/apiKeys/dd13e9b4-b84a-4026-8823-15f88bc5a7b6"
CDP_API_SECRET = "-----BEGIN EC PRIVATE KEY-----\\nMHcCAQEEILfixbR9+Y+WEPVQyaREeT5AzClpWxMBHpzbtIhfBSdeoAoGCCqGSM49\\nAwEHoUQDQgAEgE7rYjuAX7hfA6S6rFAVIlvhQgLdh8mAGjCPXlY6HK6Nz7KLLZ3/\\nD/7hLyqllJ2xoY2fj9HDEYd7Jz8D5I7W+w==\\n-----END EC PRIVATE KEY-----\\n"
CDP_PASSPHRASE = "EarlyBotSecure2025!"

# Configuration Coinbase
COINBASE_CONFIG = {{
    'api_key': CDP_API_KEY,
    'api_secret': CDP_API_SECRET,
    'passphrase': CDP_PASSPHRASE,
    'sandbox': False,
    'compatibility_mode': True
}}

# Configuration des modes de trading
TRADING_MODES = {{
'''
        
        # Ajouter chaque mode
        for mode_name, config in self.modes.items():
            content += f'''    '{mode_name}': {{
        'name': '{config["name"]}',
        'description': '{config["description"]}',
        'risk_level': '{config["risk_level"]}',
        'position_size': {config["position_size"]:.4f},
        'stop_loss': {config["stop_loss"]:.4f},
        'take_profit': {config["take_profit"]:.4f},
        'min_trade_amount': {config["min_trade_amount"]:.2f},
        'max_trades_per_day': {config["max_trades_per_day"]},
        'trading_frequency': {config["trading_frequency"]:.2f},
        'require_confirmation': {config["require_confirmation"]}
    }},
'''
        
        content += '''}

# Configuration Trading par défaut (mode normal)
TRADING_CONFIG = {
    'current_mode': 'normal',
    'portfolio_protection': True,
    'risk_management': True,
    'auto_stop_loss': True,
    'log_all_trades': True,
    'enable_notifications': True,
    **TRADING_MODES['normal']  # Utilise les paramètres du mode normal par défaut
}

# Fonction pour récupérer la configuration actuelle
def get_current_trading_mode():
    current_mode = TRADING_CONFIG.get('current_mode', 'normal')
    return TRADING_MODES.get(current_mode, TRADING_MODES['normal'])

# Fonction pour changer de mode
def set_trading_mode(mode_name):
    if mode_name in TRADING_MODES:
        TRADING_CONFIG['current_mode'] = mode_name
        return True
    return False
'''
        
        return content
    
    def interactive_menu(self):
        """Menu interactif principal"""
        while True:
            print("\n" + "="*60)
            print("🎛️  CONFIGURATEUR MODES DE TRADING EARLY-BOT")
            print("="*60)
            print("1. 📋 Afficher configuration actuelle")
            print("2. 🛡️  Configurer mode Conservateur")
            print("3. ⚖️  Configurer mode Normal")
            print("4. 🚀 Configurer mode Agressif")
            print("5. ⚡ Configurer mode Scalping")
            print("6. 💾 Sauvegarder configuration")
            print("7. 🔄 Restaurer sauvegarde")
            print("8. 🧪 Tester configuration")
            print("9. ❌ Quitter")
            
            choice = input("\n👉 Votre choix (1-9): ").strip()
            
            if choice == '1':
                self.display_current_config()
            elif choice == '2':
                self.configure_mode('conservateur')
            elif choice == '3':
                self.configure_mode('normal')
            elif choice == '4':
                self.configure_mode('agressif')
            elif choice == '5':
                self.configure_mode('scalping')
            elif choice == '6':
                self.save_config()
            elif choice == '7':
                self.restore_backup()
            elif choice == '8':
                self.test_configuration()
            elif choice == '9':
                print("👋 Au revoir!")
                break
            else:
                print("❌ Choix invalide, essayez encore")
            
            input("\n⏸️  Appuyez sur Entrée pour continuer...")
    
    def restore_backup(self):
        """Restaure la sauvegarde"""
        try:
            if os.path.exists(self.backup_file):
                with open(self.backup_file, 'r') as f:
                    content = f.read()
                with open(self.config_file, 'w') as f:
                    f.write(content)
                print(f"✅ Configuration restaurée depuis {self.backup_file}")
            else:
                print("❌ Aucune sauvegarde trouvée")
        except Exception as e:
            print(f"❌ Erreur lors de la restauration: {e}")
    
    def test_configuration(self):
        """Teste la configuration actuelle"""
        print("\n🧪 TEST DE CONFIGURATION")
        print("=" * 40)
        
        for mode_name, config in self.modes.items():
            print(f"\n{config['name']} - Simulation sur $100:")
            
            portfolio_value = 100
            position_size = portfolio_value * config['position_size']
            stop_loss_amount = position_size * config['stop_loss']
            take_profit_amount = position_size * config['take_profit']
            
            print(f"  💰 Taille position: ${position_size:.2f}")
            print(f"  📉 Perte max (stop): ${stop_loss_amount:.2f}")
            print(f"  📈 Gain potentiel: ${take_profit_amount:.2f}")
            print(f"  📊 Ratio R/R: 1:{take_profit_amount/stop_loss_amount:.1f}")

def main():
    """Fonction principale"""
    print("🚀 CONFIGURATEUR MODES DE TRADING EARLY-BOT")
    print("Personnalisez vos modes: conservateur, normal, agressif, scalping")
    
    configurator = TradingModeConfigurator()
    configurator.interactive_menu()

if __name__ == "__main__":
    main()
