#!/usr/bin/env python3
"""
🔧 Script de diagnostic et correction avancée pour TradingBot Pro
Ce script analyse et corrige les problèmes d'authentification avec Coinbase
"""

import os
import sys
import shutil
import re
import json
import time
from datetime import datetime

# Chemins importants
PROJECT_DIR = "/Users/johan/ia_env/bot-trading-"
TRADING_BOT_DIR = os.path.join(PROJECT_DIR, "TradingBot_Pro_2025")
DASHBOARD_PATH = os.path.join(TRADING_BOT_DIR, "dashboard_trading_pro.py")
CREDENTIALS_PATH = os.path.join(TRADING_BOT_DIR, "coinbase_credentials.env")
FIXED_DASHBOARD_PATH = os.path.join(TRADING_BOT_DIR, "dashboard_trading_fixed.py")

def backup_file(file_path):
    """Crée une sauvegarde du fichier avant modification"""
    backup_path = f"{file_path}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
    shutil.copy2(file_path, backup_path)
    print(f"✅ Sauvegarde créée: {backup_path}")
    return backup_path

def extract_credentials():
    """Extrait les identifiants du fichier credentials.env"""
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"❌ Erreur: Fichier {CREDENTIALS_PATH} introuvable!")
        return None, None
        
    try:
        api_key = None
        private_key_lines = []
        in_private_key = False
        
        with open(CREDENTIALS_PATH, 'r') as f:
            for line in f:
                if line.startswith('COINBASE_API_KEY='):
                    api_key = line.strip().split('=', 1)[1]
                elif '-----BEGIN EC PRIVATE KEY-----' in line:
                    in_private_key = True
                    private_key_lines.append(line.strip())
                elif in_private_key and '-----END EC PRIVATE KEY-----' in line:
                    private_key_lines.append(line.strip())
                    in_private_key = False
                elif in_private_key:
                    private_key_lines.append(line.strip())
        
        private_key = "\n".join(private_key_lines) if private_key_lines else None
        
        if not api_key or not private_key:
            print("❌ Erreur: Identifiants incomplets dans le fichier credentials!")
            return None, None
            
        return api_key, private_key
    except Exception as e:
        print(f"❌ Erreur lors de la lecture des identifiants: {str(e)}")
        return None, None

def create_fixed_dashboard():
    """Crée un fichier dashboard corrigé"""
    api_key, private_key = extract_credentials()
    if not api_key or not private_key:
        print("❌ Impossible de récupérer les identifiants.")
        return False
    
    try:
        # Créer le fichier avec la correction de la méthode setup_exchange
        with open(FIXED_DASHBOARD_PATH, 'w') as f:
            f.write("""#!/usr/bin/env python3
\"\"\"
🚀 TRADING BOT PRO DASHBOARD - Version Professionnelle Corrigée
Multiple stratégies, gestion des risques, interface avancée avec IA avancée
\"\"\"

import os
import sys
import ccxt
import time
import threading
import json
import random
import asyncio
import logging
import traceback
import sqlite3
import numpy as np
import pandas as pd
import ta
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template_string, request
from flask_socketio import SocketIO, emit
import requests

# Import des modules AI avancés
try:
    from src.ai_advanced.multi_timeframe_predictor import MultiTimeframePredictor
    from src.ai_advanced.arbitrage_detector import ArbitrageDetector
    from src.ai_advanced.quantum_portfolio_optimizer import QuantumPortfolioOptimizer
    from src.ai_advanced.social_sentiment_analyzer import SocialSentimentAnalyzer
    from src.ai_advanced.adaptive_risk_manager import AdaptiveRiskManager
    AI_MODULES_AVAILABLE = True
    print("🤖 Modules IA avancés initialisés avec succès!")
except ImportError as e:
    print(f"⚠️ Modules IA avancés non disponibles: {e}")
    AI_MODULES_AVAILABLE = False

# Configuration Flask
app = Flask(__name__, static_folder=None)
app.config['SECRET_KEY'] = 'trading_bot_pro_2025_fixed'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

class TradingConfig:
    \"\"\"Configuration du trading bot\"\"\"
    
    def __init__(self):
        self.max_portfolio_risk = 0.02  # 2% max du portfolio par trade
        self.max_daily_trades = 10      # Max 10 trades par jour
        self.max_total_investment = 100 # $100 max total à trader
        self.stop_loss_percent = 0.05   # Stop loss à 5%
        self.take_profit_percent = 0.10 # Take profit à 10%
        self.min_signal_strength = 20   # Signal minimum pour trader (réduit à 20%)
        self.trading_symbols = ['BTC/USD', 'ETH/USD', 'ADA/USD', 'DOT/USD', 'LINK/USD']
        self.strategies = ['tendance', 'momentum', 'convergence', 'volatilite']
        self.active_strategy = 'tendance'

class TradingBot:
    \"\"\"Bot de trading professionnel multi-stratégies avec IA avancée\"\"\"
    
    def __init__(self):
        self.is_running = False
        self.exchange = None
        self.portfolio = {}
        self.signals = []
        self.trades = []
        self.daily_trades = 0
        self.total_invested = 0
        
        # Initialisation des modules IA avancés
        if AI_MODULES_AVAILABLE:
            try:
                self.multi_timeframe_predictor = MultiTimeframePredictor()
                self.arbitrage_detector = ArbitrageDetector()
                self.quantum_optimizer = QuantumPortfolioOptimizer()
                self.social_sentiment = SocialSentimentAnalyzer()
                self.adaptive_risk_manager = AdaptiveRiskManager()
                self.ai_enhanced = True
                print("🤖 Modules IA avancés initialisés avec succès!")
            except Exception as e:
                print(f"⚠️ Erreur initialisation IA: {e}")
                self.ai_enhanced = False
        else:
            self.ai_enhanced = False
        self.total_profit = 0
        self.config = TradingConfig()
        
        # Initialiser le système ML avancé
        self.initialize_ml_system()
                
        self.last_trade_check = datetime.now()
        self.setup_exchange()
        
    def setup_exchange(self):
        \"\"\"Configuration de l'exchange Coinbase\"\"\"
        try:
            # Utiliser les identifiants du fichier de configuration
            private_key = \"\"\"{}\"\"\"
            
            exchange_config = {{
                'apiKey': '{}',
                'secret': private_key,
                'sandbox': False,
                'enableRateLimit': True,
                'options': {{
                    'timeout': 30000,
                    'adjustForTimeDifference': True
                }}
            }}
            
            self.exchange = ccxt.coinbaseadvanced(exchange_config)
            print("✅ TradingBot Pro connecté à Coinbase!")
            return True
            
        except Exception as e:
            print(f"❌ Erreur connexion bot: {{e}}")
            return False
""".format(private_key, api_key))
            
            # Ajouter le reste du contenu du dashboard original
            with open(DASHBOARD_PATH, 'r') as original:
                lines = original.readlines()
                # Ignorer les premières lignes qui ont été remplacées
                start_copy = False
                for line in lines:
                    if 'def get_portfolio(self):' in line:
                        start_copy = True
                    if start_copy:
                        f.write(line)
        
        print(f"✅ Nouveau dashboard créé: {FIXED_DASHBOARD_PATH}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création du dashboard fixe: {str(e)}")
        return False

def create_launcher_script():
    """Crée un script de lancement pour le dashboard fixe"""
    launcher_path = os.path.join(PROJECT_DIR, "DASHBOARD_COINBASE_FIXED.command")
    
    try:
        with open(launcher_path, 'w') as f:
            f.write("""#!/bin/bash

# DASHBOARD COINBASE CORRIGÉ - VERSION DE SECOURS
# Créé le {}

# Chemins
PROJET_DIR="/Users/johan/ia_env/bot-trading-"
TRADING_BOT_DIR="$PROJET_DIR/TradingBot_Pro_2025"
ENV_PATH="/Users/johan/ia_env/bin/activate"

# Nettoyage des processus
pkill -f "python.*dashboard.*\.py" >/dev/null 2>&1 || true
lsof -ti:8088 | xargs kill -9 >/dev/null 2>&1 || true
sleep 1

# Notification
osascript -e 'display notification "Démarrage de la version de secours du dashboard" with title "TradingBot Pro" sound name "Submarine"'

# Préparation
cd "$TRADING_BOT_DIR" || {{
  osascript -e 'display dialog "Erreur: Répertoire non trouvé" buttons {{"OK"}} default button "OK" with icon stop'
  exit 1
}}

# Activation environnement
source "$ENV_PATH" || {{
  osascript -e 'display dialog "Erreur: Environnement Python non trouvé" buttons {{"OK"}} default button "OK" with icon stop'
  exit 1
}}

# Lancer navigateur dans 4 secondes
(sleep 4 && open "http://localhost:8088") &

echo "🚀 LANCEMENT TRADINGBOT PRO DASHBOARD - VERSION CORRIGÉE"
echo "============================================================"
echo "🔍 Démarrage de la version de secours..."
echo ""
echo "📊 Dashboard accessible à l'adresse: http://localhost:8088"
echo ""
echo "⏳ Démarrage en cours..."

# Lancer le dashboard fixe
python dashboard_trading_fixed.py --full-features --enable-api --portfolio-live --debug

# Message en cas d'arrêt
echo "⚠️ Le dashboard s'est arrêté!"
sleep 5
""".format(datetime.now().strftime('%d/%m/%Y à %H:%M')))
            
        os.chmod(launcher_path, 0o755)  # Rendre exécutable
        desktop_path = os.path.expanduser("~/Desktop/DASHBOARD_COINBASE_FIXED.command")
        shutil.copy2(launcher_path, desktop_path)
        os.chmod(desktop_path, 0o755)  # Rendre exécutable
        
        print(f"✅ Script de lancement créé: {launcher_path}")
        print(f"✅ Script de lancement copié sur le bureau: {desktop_path}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création du script de lancement: {str(e)}")
        return False

def main():
    print("\n🔧 DIAGNOSTIC ET CORRECTION AVANCÉE DU TRADING BOT 🔧")
    print("=====================================================\n")
    
    # Sauvegarde du fichier original
    backup_file(DASHBOARD_PATH)
    
    # Création du dashboard fixe
    print("\n📊 Création d'une version corrigée du dashboard...")
    if create_fixed_dashboard():
        print("✅ Version corrigée du dashboard créée avec succès!")
    else:
        print("❌ Échec de la création du dashboard corrigé.")
        return False
    
    # Création du script de lancement
    print("\n📜 Création du script de lancement...")
    if create_launcher_script():
        print("✅ Script de lancement créé avec succès!")
    else:
        print("❌ Échec de la création du script de lancement.")
        return False
    
    print("\n✨ CORRECTION AVANCÉE TERMINÉE ✨")
    print("Un nouveau dashboard fixé a été créé.")
    print("Un script de lancement a été placé sur votre bureau.")
    print("Double-cliquez sur DASHBOARD_COINBASE_FIXED.command sur votre bureau.")
    print("=====================================================\n")
    return True

if __name__ == "__main__":
    main()
