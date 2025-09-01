#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import webbrowser
import time
import threading

class TradingBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot Trading Coinbase")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Définir le chemin du projet
        self.project_dir = "/Users/johan/ia_env/bot-trading-"
        
        # Configuration du style
        self.style = ttk.Style()
        self.style.theme_use("clam")  # ou "aqua" pour un look plus Mac
        self.style.configure("TButton", font=("SF Pro Display", 12, "bold"), padding=10)
        self.style.configure("TLabel", font=("SF Pro Display", 12))
        self.style.configure("Header.TLabel", font=("SF Pro Display", 16, "bold"))
        self.style.configure("Status.TLabel", font=("SF Pro Display", 12, "italic"))
        
        # Créer l'interface
        self.create_widgets()
        
        # Vérifier l'état initial
        self.check_bot_status()
        
        # Mise à jour périodique
        self.root.after(5000, self.update_status)
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Logo/Titre
        ttk.Label(main_frame, text="🤖 BOT TRADING COINBASE PRO", style="Header.TLabel").pack(pady=(0, 20))
        
        # Séparateur
        ttk.Separator(main_frame).pack(fill="x", pady=10)
        
        # Statut
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill="x", pady=10)
        
        ttk.Label(status_frame, text="État actuel:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.status_label = ttk.Label(status_frame, text="Vérification...", style="Status.TLabel")
        self.status_label.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Configuration
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding=10)
        config_frame.pack(fill="x", pady=10)
        
        # Mode de trading
        ttk.Label(config_frame, text="Mode de trading:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.mode_var = tk.StringVar(value="simulation")
        ttk.Radiobutton(config_frame, text="Simulation", variable=self.mode_var, value="simulation").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(config_frame, text="Trading réel (Coinbase)", variable=self.mode_var, value="real").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        
        # Montant maximum
        ttk.Label(config_frame, text="Montant max par trade (USD):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.amount_var = tk.StringVar(value="100")
        ttk.Spinbox(config_frame, from_=10, to=1000, increment=10, textvariable=self.amount_var, width=10).grid(row=1, column=1, columnspan=2, sticky="w", padx=5, pady=5)
        
        # Niveau de risque
        ttk.Label(config_frame, text="Niveau de risque:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.risk_var = tk.StringVar(value="MEDIUM")
        ttk.Combobox(config_frame, values=["LOW", "MEDIUM", "HIGH"], textvariable=self.risk_var, state="readonly", width=10).grid(row=2, column=1, columnspan=2, sticky="w", padx=5, pady=5)
        
        # Boutons d'action
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill="x", pady=20)
        
        # Bouton de lancement
        launch_btn = ttk.Button(action_frame, text="🚀 LANCER LE BOT", command=self.launch_bot)
        launch_btn.pack(fill="x", pady=5)
        
        # Bouton d'arrêt
        stop_btn = ttk.Button(action_frame, text="⛔️ ARRÊTER LE BOT", command=self.stop_bot)
        stop_btn.pack(fill="x", pady=5)
        
        # Bouton Dashboard
        dashboard_btn = ttk.Button(action_frame, text="📊 OUVRIR DASHBOARD", command=self.open_dashboard)
        dashboard_btn.pack(fill="x", pady=5)
        
        # Accès iPhone
        iphone_btn = ttk.Button(action_frame, text="📱 CONFIGURER ACCÈS IPHONE", command=self.setup_iphone)
        iphone_btn.pack(fill="x", pady=5)
        
        # Journal d'activité
        log_frame = ttk.LabelFrame(main_frame, text="Journal d'activité", padding=10)
        log_frame.pack(fill="both", expand=True, pady=10)
        
        self.log_text = tk.Text(log_frame, height=8, width=50, font=("Menlo", 10))
        self.log_text.pack(fill="both", expand=True)
        self.log_text.config(state="disabled")
        
        # Footer
        ttk.Label(main_frame, text="© 2025 Trading Bot Pro", font=("SF Pro Display", 10)).pack(pady=(10, 0))
    
    def launch_bot(self):
        """Lance le bot de trading avec la configuration spécifiée"""
        # Confirmation pour le trading réel
        if self.mode_var.get() == "real":
            if not messagebox.askyesno("Confirmation", "⚠️ ATTENTION ⚠️\n\nVous êtes sur le point de lancer le bot en mode TRADING RÉEL.\nDes transactions réelles seront effectuées avec votre argent.\n\nÊtes-vous sûr de vouloir continuer?"):
                return
        
        # Mise à jour du journal
        self.log("Lancement du bot en mode " + ("RÉEL" if self.mode_var.get() == "real" else "SIMULATION"))
        self.log(f"Montant max par trade: {self.amount_var.get()} USD")
        self.log(f"Niveau de risque: {self.risk_var.get()}")
        
        # Arrêter d'abord tout bot en cours
        self.stop_bot(silent=True)
        
        # Configurer l'environnement
        os.environ["TRADING_MODE"] = "LIVE" if self.mode_var.get() == "real" else "TEST"
        os.environ["MAX_TRADE_AMOUNT"] = self.amount_var.get()
        os.environ["RISK_LEVEL"] = self.risk_var.get()
        
        # Lancer dans un thread séparé pour ne pas bloquer l'interface
        def run_bot():
            try:
                cmd = ["/bin/bash", "-c"]
                
                if self.mode_var.get() == "real":
                    # Activer le trading réel d'abord
                    activate_cmd = f"cd {self.project_dir} && bash activer_trading_reel.sh > /dev/null 2>&1"
                    subprocess.run(activate_cmd, shell=True)
                    
                    # Puis lancer le bot
                    launch_cmd = f"cd {self.project_dir}/TradingBot_Pro_2025 && source /Users/johan/ia_env/bin/activate && python dashboard_trading_pro.py --live-trading"
                else:
                    launch_cmd = f"cd {self.project_dir}/TradingBot_Pro_2025 && source /Users/johan/ia_env/bin/activate && python dashboard_trading_pro.py --test-mode"
                
                cmd.append(launch_cmd)
                self.bot_process = subprocess.Popen(cmd)
                
                # Donner le temps au bot de démarrer
                time.sleep(3)
                
                # Ouvrir le dashboard
                self.open_dashboard()
                
                self.log("✅ Bot démarré avec succès!")
                self.root.after(0, self.update_status)
                
            except Exception as e:
                self.log(f"❌ Erreur lors du lancement: {str(e)}")
        
        # Démarrer le thread
        threading.Thread(target=run_bot, daemon=True).start()
    
    def stop_bot(self, silent=False):
        """Arrête le bot de trading"""
        try:
            # Essayer d'arrêter proprement
            subprocess.run(f"cd {self.project_dir} && ./arreter_dashboard.sh > /dev/null 2>&1", shell=True)
            
            # Forcer l'arrêt si nécessaire
            subprocess.run("pkill -f 'python.*dashboard_trading_pro.py' || true", shell=True)
            
            # Libérer le port
            subprocess.run("lsof -ti:8088 | xargs kill -9 > /dev/null 2>&1 || true", shell=True)
            
            if not silent:
                self.log("Bot arrêté.")
            
            # Mise à jour du statut
            self.root.after(1000, self.update_status)
            
        except Exception as e:
            if not silent:
                self.log(f"Erreur lors de l'arrêt: {str(e)}")
    
    def open_dashboard(self):
        """Ouvre le dashboard dans le navigateur"""
        try:
            webbrowser.open("http://localhost:8088")
            self.log("Dashboard ouvert dans le navigateur.")
        except Exception as e:
            self.log(f"Erreur lors de l'ouverture du dashboard: {str(e)}")
    
    def setup_iphone(self):
        """Configure l'accès depuis iPhone"""
        try:
            self.log("Configuration de l'accès iPhone...")
            
            # Exécuter le script dans un thread séparé
            def run_setup():
                cmd = f"cd {self.project_dir} && bash configurer_acces_iphone.sh"
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
                
                # Capturer et afficher la sortie
                for line in process.stdout:
                    self.log(line.strip())
            
            threading.Thread(target=run_setup, daemon=True).start()
            
        except Exception as e:
            self.log(f"Erreur: {str(e)}")
    
    def check_bot_status(self):
        """Vérifie si le bot est en cours d'exécution"""
        try:
            # Vérifier si le processus python du dashboard est en cours
            result = subprocess.run("pgrep -f 'python.*dashboard_trading_pro.py'", shell=True, stdout=subprocess.PIPE)
            
            if result.returncode == 0:
                # Le bot est en cours d'exécution
                self.status_label.config(text="✅ En cours d'exécution")
                
                # Vérifier s'il s'agit du mode réel ou simulation
                result = subprocess.run("ps aux | grep 'python.*dashboard_trading_pro.py.*--live-trading' | grep -v grep", shell=True, stdout=subprocess.PIPE)
                
                if result.returncode == 0:
                    self.status_label.config(text="🔴 Trading RÉEL en cours")
                else:
                    self.status_label.config(text="🔵 Simulation en cours")
            else:
                # Le bot n'est pas en cours d'exécution
                self.status_label.config(text="⚪ Arrêté")
            
        except Exception as e:
            self.status_label.config(text=f"❌ Erreur: {str(e)}")
    
    def update_status(self):
        """Met à jour périodiquement le statut du bot"""
        self.check_bot_status()
        self.root.after(5000, self.update_status)  # Vérifier toutes les 5 secondes
    
    def log(self, message):
        """Ajoute un message au journal"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)  # Défiler vers le bas
        self.log_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotApp(root)
    root.mainloop()
