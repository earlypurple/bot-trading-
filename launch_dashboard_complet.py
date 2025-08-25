#!/usr/bin/env python3
"""
Launcher pour le Dashboard Complet - Bot Trading Quantique
Version intégrée et optimisée
"""

import os
import sys
import time
import subprocess

def main():
    print("🚀 LAUNCHER DASHBOARD COMPLET - BOT TRADING QUANTIQUE")
    print("=" * 70)
    print("🌐 Nouveau dashboard moderne intégré")
    print("🤖 Serveur complet avec simulation bot + IA")
    print("📊 Interface web professionnelle")
    print("💰 Tracking portfolio en temps réel")
    print()
    
    # Vérification des fichiers nécessaires
    required_files = [
        'serveur_dashboard.py',
        'dashboard_complet.html'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Fichier manquant: {file}")
            return False
    
    print("✅ Tous les fichiers requis sont présents")
    print()
    
    try:
        print("🎯 Démarrage du serveur dashboard...")
        print("🌐 URL: http://localhost:8080")
        print("📱 Interface moderne avec animations")
        print("🤖 Bot simulé avec IA intégrée")
        print()
        print("ℹ️  Appuyez sur Ctrl+C pour arrêter")
        print("-" * 50)
        
        # Lancement du serveur
        subprocess.run([sys.executable, 'serveur_dashboard.py'])
        
    except KeyboardInterrupt:
        print("\n📊 Dashboard fermé proprement")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        print("💡 Vérifiez que le port 8080 est libre")
        
    print("\n🎉 Session terminée !")

if __name__ == "__main__":
    main()
