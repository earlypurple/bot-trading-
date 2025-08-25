#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur Système Complet - Dashboard + Bot
Lance simultanément le dashboard et le bot de trading
"""

import subprocess
import time
import sys
import os
import signal
import threading

class CompleteSystemLauncher:
    def __init__(self):
        self.dashboard_process = None
        self.bot_process = None
        self.running = True
        
    def launch_dashboard(self):
        """Lance le serveur dashboard sur le port 8080"""
        try:
            print("🌐 Démarrage du serveur dashboard...")
            self.dashboard_process = subprocess.Popen(
                [sys.executable, "serveur_dashboard_stable.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("✅ Dashboard démarré sur http://localhost:8080")
            return True
        except Exception as e:
            print(f"❌ Erreur dashboard: {e}")
            return False
    
    def launch_bot(self):
        """Lance le bot de trading sur le port 8091"""
        try:
            print("🤖 Démarrage du bot de trading...")
            # Attendre un peu que le dashboard soit prêt
            time.sleep(3)
            
            self.bot_process = subprocess.Popen(
                [sys.executable, "bot/early_bot_trading.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("✅ Bot de trading démarré sur port 8091")
            return True
        except Exception as e:
            print(f"❌ Erreur bot: {e}")
            return False
    
    def monitor_processes(self):
        """Surveille les processus et les redémarre si nécessaire"""
        while self.running:
            try:
                # Vérifier le dashboard
                if self.dashboard_process and self.dashboard_process.poll() is not None:
                    print("⚠️ Dashboard arrêté, redémarrage...")
                    self.launch_dashboard()
                
                # Vérifier le bot
                if self.bot_process and self.bot_process.poll() is not None:
                    print("⚠️ Bot arrêté, redémarrage...")
                    self.launch_bot()
                
                time.sleep(5)
            except KeyboardInterrupt:
                break
    
    def stop_all(self):
        """Arrête tous les processus"""
        self.running = False
        print("\n🛑 Arrêt du système complet...")
        
        if self.dashboard_process:
            self.dashboard_process.terminate()
            self.dashboard_process.wait()
            print("✅ Dashboard arrêté")
        
        if self.bot_process:
            self.bot_process.terminate()
            self.bot_process.wait()
            print("✅ Bot arrêté")
    
    def start_system(self):
        """Démarre le système complet"""
        print("🚀 LANCEMENT DU SYSTÈME COMPLET")
        print("=" * 50)
        
        # Nettoyer les anciens processus
        os.system("pkill -f 'serveur_dashboard' 2>/dev/null || true")
        os.system("pkill -f 'early_bot_trading' 2>/dev/null || true")
        time.sleep(2)
        
        # Démarrer les services
        dashboard_ok = self.launch_dashboard()
        if not dashboard_ok:
            print("❌ Impossible de démarrer le dashboard")
            return False
        
        bot_ok = self.launch_bot()
        if not bot_ok:
            print("❌ Impossible de démarrer le bot")
            return False
        
        print("\n✅ SYSTÈME COMPLET OPÉRATIONNEL!")
        print("🌐 Dashboard: http://localhost:8080")
        print("🤖 Bot API: http://localhost:8091")
        print("🔄 Surveillance active des processus")
        print("\nAppuyez sur Ctrl+C pour arrêter")
        
        # Configurer l'arrêt propre
        def signal_handler(signum, frame):
            self.stop_all()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Surveiller les processus
        try:
            self.monitor_processes()
        except KeyboardInterrupt:
            self.stop_all()
        
        return True

def main():
    launcher = CompleteSystemLauncher()
    
    try:
        launcher.start_system()
    except KeyboardInterrupt:
        launcher.stop_all()
        print("\n👋 Système arrêté proprement")

if __name__ == "__main__":
    main()
