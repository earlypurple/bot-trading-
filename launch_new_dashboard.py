#!/usr/bin/env python3
"""
Launcher pour Early-Bot-Trading avec nouveau dashboard moderne
Version clean et optimisée
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def main():
    """Lance le bot avec le nouveau dashboard"""
    
    print("🚀 EARLY-BOT-TRADING - NOUVEAU DASHBOARD")
    print("=" * 50)
    print("🎨 Interface moderne avec template optimisé")
    print("📊 Dashboard responsive et performant") 
    print("⚡ Fonctionnalités avancées intégrées")
    print("🔗 Accès: http://localhost:8091")
    print("=" * 50)
    
    # Vérifier le répertoire
    current_dir = Path.cwd()
    if not (current_dir / "bot" / "early_bot_trading_new.py").exists():
        print("❌ Erreur: Veuillez exécuter depuis le répertoire Early-Bot-Trading")
        sys.exit(1)
    
    # Arrêter les processus existants
    try:
        print("🔄 Nettoyage des processus existants...")
        subprocess.run(["pkill", "-f", "early_bot_trading"], check=False)
        subprocess.run(["pkill", "-f", "launch_early_bot"], check=False)
        time.sleep(2)
    except:
        pass
    
    # Vérifier que le port est libre
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 8091))
        sock.close()
        
        if result == 0:
            print("⚠️ Port 8091 occupé, nettoyage...")
            subprocess.run(["lsof", "-ti", ":8091"], check=False, capture_output=True)
    except:
        pass
    
    # Lancer le nouveau bot
    try:
        print("🚀 Démarrage du bot avec nouveau dashboard...")
        print("📡 Interface disponible sur: http://localhost:8091")
        print("💡 Appuyez sur Ctrl+C pour arrêter")
        print("-" * 50)
        
        # Lancer le bot
        os.chdir(current_dir)
        subprocess.run([sys.executable, "bot/early_bot_trading_new.py"], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé par l'utilisateur")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return 1
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return 1
    finally:
        print("🔄 Nettoyage final...")
        try:
            subprocess.run(["pkill", "-f", "early_bot_trading_new"], check=False)
        except:
            pass
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
