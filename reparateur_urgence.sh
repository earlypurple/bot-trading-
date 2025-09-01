#!/bin/bash

# RÉPARATEUR DASHBOARD COINBASE - VERSION D'URGENCE
# Créé le 24 août 2025

# Afficher message de démarrage
echo "🚨 RÉPARATEUR D'URGENCE POUR DASHBOARD TRADING COINBASE 🚨"
echo "=========================================================="
echo ""

# Définir les variables
PROJET_DIR="/Users/johan/ia_env/bot-trading-"
TRADING_BOT_DIR="$PROJET_DIR/TradingBot_Pro_2025"
ENV_PATH="/Users/johan/ia_env/bin/activate"
ORIGINAL_DASHBOARD="$TRADING_BOT_DIR/dashboard_trading_pro.py"
FIXED_DASHBOARD="$TRADING_BOT_DIR/dashboard_trading_fixed.py"
API_KEY=$(grep COINBASE_API_KEY "$TRADING_BOT_DIR/coinbase_credentials.env" | cut -d= -f2)

# Vérification des fichiers nécessaires
if [ ! -f "$ORIGINAL_DASHBOARD" ]; then
    echo "❌ Erreur: Fichier dashboard_trading_pro.py introuvable!"
    exit 1
fi

if [ ! -f "$TRADING_BOT_DIR/coinbase_credentials.env" ]; then
    echo "❌ Erreur: Fichier coinbase_credentials.env introuvable!"
    exit 1
fi

# Sauvegarder le dashboard original
echo "📂 Sauvegarde du fichier original..."
cp "$ORIGINAL_DASHBOARD" "${ORIGINAL_DASHBOARD}.bak.$(date +%Y%m%d%H%M%S)"

# Extraire la clé privée du fichier d'environnement
echo "🔑 Extraction des clés API Coinbase..."
PRIVATE_KEY=$(awk '/-----BEGIN EC PRIVATE KEY-----/,/-----END EC PRIVATE KEY-----/' "$TRADING_BOT_DIR/coinbase_credentials.env")

# Vérification des clés extraites
if [ -z "$API_KEY" ] || [ -z "$PRIVATE_KEY" ]; then
    echo "❌ Erreur: Impossible d'extraire les clés Coinbase!"
    exit 1
fi

echo "✅ Clés API extraites avec succès"

# Créer le nouveau fichier dashboard avec les corrections
echo "🔧 Création du dashboard corrigé..."

cat > "$FIXED_DASHBOARD" << EOL
#!/usr/bin/env python3
"""
🚀 TRADING BOT PRO DASHBOARD - Version Professionnelle Corrigée
Multiple stratégies, gestion des risques, interface avancée avec IA avancée
"""

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

# Configuration Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'trading_bot_pro_2025_fixed'
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuration de base
class TradingConfig:
    """Configuration du trading bot"""
    
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
    """Bot de trading professionnel"""
    
    def __init__(self):
        self.is_running = False
        self.exchange = None
        self.portfolio = {}
        self.signals = []
        self.trades = []
        self.daily_trades = 0
        self.total_invested = 0
        self.ai_enhanced = True
        self.total_profit = 0
        self.config = TradingConfig()
        self.last_trade_check = datetime.now()
        self.setup_exchange()
        
    def setup_exchange(self):
        """Configuration de l'exchange Coinbase avec les bonnes clés"""
        try:
            # Identifiants provenant du fichier coinbase_credentials.env
            private_key = """$PRIVATE_KEY"""
            
            exchange_config = {
                'apiKey': '$API_KEY',
                'secret': private_key,
                'sandbox': False,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',
                    'adjustForTimeDifference': True
                }
            }
            
            self.exchange = ccxt.coinbaseadvanced(exchange_config)
            print("✅ TradingBot Pro connecté à Coinbase!")
            return True
            
        except Exception as e:
            print(f"❌ Erreur connexion bot: {e}")
            return False
    
    def get_portfolio(self):
        """Récupère le portfolio en temps réel"""
        try:
            balance = self.exchange.fetch_balance()
            portfolio = []
            total_usd = 0
            
            print("📊 Données balance brutes:", balance.keys())
            
            for currency, amounts in balance.items():
                if currency not in ['info', 'free', 'used', 'total'] and isinstance(amounts, dict):
                    total = amounts.get('total', 0) or 0
                    
                    if total > 0:
                        try:
                            if currency != 'USD':
                                ticker = self.exchange.fetch_ticker(f'{currency}/USD')
                                price_usd = ticker['last']
                                value_usd = total * price_usd
                                change_24h = ticker.get('percentage', 0)
                            else:
                                price_usd = 1
                                value_usd = total
                                change_24h = 0
                        except Exception as ticker_error:
                            print(f"❌ Erreur récupération prix {currency}: {ticker_error}")
                            price_usd = 0
                            value_usd = 0
                            change_24h = 0
                        
                        portfolio.append({
                            'currency': currency,
                            'amount': total,
                            'price_usd': price_usd,
                            'value_usd': value_usd,
                            'change_24h': change_24h
                        })
                        
                        total_usd += value_usd
            
            # Trier par valeur
            portfolio.sort(key=lambda x: x['value_usd'], reverse=True)
            
            self.portfolio = {
                'items': portfolio,
                'total_value_usd': total_usd,
                'timestamp': time.time()
            }
            
            print(f"💰 Portfolio récupéré: {len(portfolio)} actifs, total ${total_usd:.2f}")
            return self.portfolio
            
        except Exception as e:
            print(f"❌ Erreur portfolio: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Détails: {e.response.text}")
            return {'items': [], 'total_value_usd': 0, 'error': str(e)}

# Instance globale du bot
trading_bot = TradingBot()

@app.route('/')
def dashboard():
    """Page d'accueil simplifiée du dashboard"""
    html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>TradingBot Pro - Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            text-align: center;
            padding: 20px 0;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }
        .card {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            backdrop-filter: blur(10px);
        }
        .portfolio-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .crypto-card {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        }
        h1 {
            margin: 0;
        }
        .btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }
        .btn.danger {
            background: #f44336;
        }
        .status {
            font-size: 1.2em;
            margin: 10px 0;
        }
        .controls {
            display: flex;
            gap: 10px;
            margin: 20px 0;
        }
        .positive { color: #4CAF50; }
        .negative { color: #f44336; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 TradingBot Pro - Dashboard Coinbase</h1>
            <p class="status">Version de secours - Corrigée</p>
        </header>
        
        <div class="card">
            <h2>État du Bot</h2>
            <p id="connectionStatus">Statut de connexion: Vérification...</p>
            <div class="controls">
                <button id="refreshPortfolio" class="btn">Rafraîchir Portfolio</button>
                <button id="startBot" class="btn">Démarrer Bot</button>
                <button id="stopBot" class="btn danger">Arrêter Bot</button>
            </div>
        </div>
        
        <div class="card">
            <h2>Portfolio Coinbase</h2>
            <p>Total: <span id="portfolioTotal">$0.00</span></p>
            <div id="portfolioGrid" class="portfolio-grid">
                <!-- Le portfolio sera chargé ici -->
            </div>
        </div>
    </div>
    
    <script>
        // Fonction pour actualiser le portfolio
        function refreshPortfolio() {
            document.getElementById('connectionStatus').textContent = 'Connexion: Chargement...';
            document.getElementById('portfolioGrid').innerHTML = '<p>Chargement du portfolio...</p>';
            
            // Requête AJAX pour récupérer le portfolio
            fetch('/api/portfolio')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('connectionStatus').textContent = 'Connexion: Erreur - ' + data.error;
                        return;
                    }
                    
                    document.getElementById('connectionStatus').textContent = 'Connexion: OK ✅';
                    document.getElementById('portfolioTotal').textContent = '$' + data.total_value_usd.toFixed(2);
                    
                    // Afficher les actifs
                    const grid = document.getElementById('portfolioGrid');
                    grid.innerHTML = '';
                    
                    if (data.items && data.items.length > 0) {
                        data.items.forEach(item => {
                            const card = document.createElement('div');
                            card.className = 'crypto-card';
                            const changeClass = item.change_24h >= 0 ? 'positive' : 'negative';
                            const changePrefix = item.change_24h >= 0 ? '+' : '';
                            
                            card.innerHTML = `
                                <h3>${item.currency}</h3>
                                <p>${item.amount.toFixed(6)}</p>
                                <p>Prix: $${item.price_usd.toFixed(2)}</p>
                                <p>Valeur: $${item.value_usd.toFixed(2)}</p>
                                <p class="${changeClass}">${changePrefix}${item.change_24h.toFixed(2)}%</p>
                            `;
                            grid.appendChild(card);
                        });
                    } else {
                        grid.innerHTML = '<p>Aucun actif trouvé dans le portfolio.</p>';
                    }
                })
                .catch(error => {
                    console.error('Erreur:', error);
                    document.getElementById('connectionStatus').textContent = 'Connexion: Erreur de réseau';
                });
        }
        
        // Configurer les événements des boutons
        document.getElementById('refreshPortfolio').addEventListener('click', refreshPortfolio);
        document.getElementById('startBot').addEventListener('click', () => {
            fetch('/api/start_bot', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    alert(data.success ? 'Bot démarré !' : 'Erreur: ' + data.error);
                });
        });
        document.getElementById('stopBot').addEventListener('click', () => {
            fetch('/api/stop_bot', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    alert(data.success ? 'Bot arrêté !' : 'Erreur: ' + data.error);
                });
        });
        
        // Chargement initial
        document.addEventListener('DOMContentLoaded', refreshPortfolio);
    </script>
</body>
</html>
    """
    return render_template_string(html_template)

@app.route('/api/portfolio')
def get_portfolio():
    """API pour récupérer le portfolio"""
    try:
        portfolio = trading_bot.get_portfolio()
        return jsonify(portfolio)
    except Exception as e:
        print(f"❌ Erreur API portfolio: {e}")
        return jsonify({"error": str(e)})

@app.route('/api/start_bot', methods=['POST'])
def start_bot():
    """API pour démarrer le bot"""
    try:
        trading_bot.is_running = True
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/stop_bot', methods=['POST'])
def stop_bot():
    """API pour arrêter le bot"""
    try:
        trading_bot.is_running = False
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    print("🚀 LANCEMENT TRADINGBOT PRO DASHBOARD - VERSION CORRIGÉE")
    print("============================================================")
    
    try:
        # Test de connexion
        print("🧪 Test de connexion...")
        portfolio = trading_bot.get_portfolio()
        
        # Démarrage du serveur Flask
        print("🌐 Démarrage du serveur web sur port 8088...")
        socketio.run(app, host='0.0.0.0', port=8088, debug=False)
    except Exception as e:
        print(f"❌ Erreur: {e}")
EOL

# Remplacer les variables dans le fichier
sed -i '' "s|\$API_KEY|$API_KEY|g" "$FIXED_DASHBOARD"
sed -i '' "s|\$PRIVATE_KEY|$PRIVATE_KEY|g" "$FIXED_DASHBOARD"

# Rendre le nouveau fichier exécutable
chmod +x "$FIXED_DASHBOARD"
echo "✅ Dashboard corrigé créé avec succès"

# Créer le script de lancement
echo "📜 Création du script de lancement..."
cat > "$PROJET_DIR/LANCER_DASHBOARD_URGENCE.command" << EOL
#!/bin/bash

# SCRIPT DE LANCEMENT D'URGENCE POUR DASHBOARD TRADING
# Créé le $(date +"%d/%m/%Y")

# Chemins
PROJET_DIR="/Users/johan/ia_env/bot-trading-"
TRADING_BOT_DIR="\$PROJET_DIR/TradingBot_Pro_2025"
ENV_PATH="/Users/johan/ia_env/bin/activate"
FIXED_DASHBOARD="\$TRADING_BOT_DIR/dashboard_trading_fixed.py"

# Nettoyer les processus existants
pkill -f "python.*dashboard.*\.py" >/dev/null 2>&1 || true
lsof -ti:8088 | xargs kill -9 >/dev/null 2>&1 || true
sleep 1

clear
echo "🚨 LANCEUR D'URGENCE - DASHBOARD TRADING COINBASE 🚨"
echo "===================================================="
echo ""
echo "⏳ Démarrage du dashboard..."

# Activation environnement
cd "\$TRADING_BOT_DIR"
source "\$ENV_PATH"

# Lancer navigateur dans 3 secondes
(sleep 3 && open "http://localhost:8088") &

# Démarrer le dashboard corrigé
python "\$FIXED_DASHBOARD"
EOL

# Rendre le script de lancement exécutable et le copier sur le bureau
chmod +x "$PROJET_DIR/LANCER_DASHBOARD_URGENCE.command"
cp "$PROJET_DIR/LANCER_DASHBOARD_URGENCE.command" ~/Desktop/
chmod +x ~/Desktop/LANCER_DASHBOARD_URGENCE.command

echo "✅ Script de lancement créé et copié sur le bureau"
echo ""
echo "🎉 CORRECTION TERMINÉE 🎉"
echo "Double-cliquez sur le script LANCER_DASHBOARD_URGENCE.command"
echo "sur votre bureau pour démarrer le dashboard corrigé."
echo ""
