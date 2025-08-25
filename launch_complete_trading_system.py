#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur Système Complet Bot Trading
Démarre le dashboard (port 8080) + API bot (port 8091)
"""

import subprocess
import time
import sys
import os
import signal

def cleanup_ports():
    """Nettoie les ports utilisés"""
    os.system("pkill -f 'serveur_dashboard' 2>/dev/null || true")
    os.system("pkill -f 'simple_trading_api' 2>/dev/null || true")
    os.system("lsof -ti :8080 | xargs kill -9 2>/dev/null || true")
    os.system("lsof -ti :8091 | xargs kill -9 2>/dev/null || true")
    time.sleep(2)

def start_dashboard():
    """Lance le serveur dashboard"""
    print("🌐 Démarrage du dashboard...")
    dashboard_process = subprocess.Popen(
        [sys.executable, "serveur_dashboard_stable.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3)  # Attendre que le dashboard démarre
    return dashboard_process

def start_bot_api():
    """Lance l'API du bot"""
    print("🤖 Démarrage de l'API du bot...")
    bot_process = subprocess.Popen(
        [sys.executable, "simple_trading_api.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2)  # Attendre que l'API démarre
    return bot_process

def main():
    print("🚀 LANCEMENT DU SYSTÈME COMPLET BOT TRADING")
    print("=" * 60)
    
    # Nettoyer les anciens processus
    cleanup_ports()
    
    # Démarrer les services
    dashboard_process = start_dashboard()
    bot_process = start_bot_api()
    
    # Vérifier que les services fonctionnent
    time.sleep(3)
    
    dashboard_ok = dashboard_process.poll() is None
    bot_ok = bot_process.poll() is None
    
    if dashboard_ok and bot_ok:
        print("✅ SYSTÈME COMPLET OPÉRATIONNEL!")
        print("🌐 Dashboard: http://localhost:8080")
        print("🤖 Bot API: http://localhost:8091")
        print("📱 Ouvrez le dashboard dans votre navigateur")
        print("\n🎯 FONCTIONNALITÉS DISPONIBLES:")
        print("  • Connexion portfolio réel Coinbase ✅")
        print("  • Changement de modes de trading ✅")
        print("  • Démarrage/arrêt du bot ✅")
        print("  • Interface française ✅")
        print("  • Protection contre les déconnexions ✅")
        print("\nAppuyez sur Ctrl+C pour arrêter le système")
        
        # Gestionnaire de signal pour arrêt propre
        def signal_handler(signum, frame):
            print("\n🛑 Arrêt du système...")
            dashboard_process.terminate()
            bot_process.terminate()
            print("✅ Système arrêté proprement")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Attendre indéfiniment
        try:
            dashboard_process.wait()
        except KeyboardInterrupt:
            signal_handler(None, None)
    
    else:
        print("❌ ERREUR LORS DU DÉMARRAGE")
        if not dashboard_ok:
            print("  • Dashboard: ÉCHEC")
        else:
            print("  • Dashboard: OK")
            
        if not bot_ok:
            print("  • Bot API: ÉCHEC")
        else:
            print("  • Bot API: OK")
        
        # Nettoyer les processus qui ont démarré
        if dashboard_process.poll() is None:
            dashboard_process.terminate()
        if bot_process.poll() is None:
            bot_process.terminate()

if __name__ == "__main__":
    main()
