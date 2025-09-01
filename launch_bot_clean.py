#!/usr/bin/env python3
"""
🚀 LANCEMENT PROPRE DU BOT DE TRADING
Avec configurateur de modes intégré au dashboard
"""

import os
import sys
import subprocess
from pathlib import Path

def launch_bot():
    """Lance le bot depuis le bon répertoire"""
    
    # Répertoire de travail
    bot_dir = Path("/Users/johan/ia_env/bot-trading-/Early-Bot-Trading")
    bot_file = bot_dir / "bot" / "early_bot_trading.py"
    
    print("🚀 LANCEMENT DU BOT DE TRADING")
    print("=" * 40)
    print(f"📂 Répertoire: {bot_dir}")
    print(f"🤖 Bot: {bot_file}")
    
    # Vérification
    if not bot_file.exists():
        print(f"❌ Erreur: {bot_file} introuvable!")
        return False
    
    # Changement de répertoire
    os.chdir(bot_dir)
    print(f"✅ Répertoire changé vers: {os.getcwd()}")
    
    # Lancement
    try:
        print("\n🎯 Fonctionnalités disponibles:")
        print("   • Portfolio Manager Avancé")
        print("   • Dashboard avec configurateur de modes")
        print("   • Modes: Conservateur, Normal, Agressif, Scalping")
        print("   • Configuration temps réel depuis l'interface web")
        
        print("\n🌐 Une fois lancé, accédez à:")
        print("   http://localhost:8091")
        print("   Cliquez sur '⚙️ Configurer' pour les modes\n")
        
        print("🚀 Lancement en cours...")
        subprocess.run([sys.executable, str(bot_file)], check=True)
        
    except KeyboardInterrupt:
        print("\n⏹️  Arrêt demandé par l'utilisateur")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

if __name__ == "__main__":
    launch_bot()
