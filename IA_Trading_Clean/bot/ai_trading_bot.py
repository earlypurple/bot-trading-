#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot IA Trading Automatisé - Version Corrigée
Interface web complète avec paramètres visibles
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ccxt
import pandas as pd
import numpy as np
import time
import threading
from datetime import datetime, timedelta
import json
from flask import Flask, render_template_string, request, jsonify
from flask_socketio import SocketIO, emit
import warnings
warnings.filterwarnings('ignore')

# Configuration
from config.api_config import API_CONFIG, TRADING_CONFIG

class AITradingBot:
    def __init__(self):
        self.config = TRADING_CONFIG
        self.api_config = API_CONFIG
        self.exchange = None
        self.is_trading = False
        self.is_running = False
        self.signals = {}
        self.trades_count = 0
        self.profit_simulation = 0.0
        self.last_cycle_time = None
        self.portfolio_balance = 0.0
        self.portfolio_details = {}
        self.current_positions = {}
        
        print("🔐 Configuration avec NOUVELLES clés API...")
        self.setup_exchange()
        
    def setup_exchange(self):
        """Configuration de l'exchange avec nouvelles clés"""
        try:
            self.exchange = ccxt.coinbase({
                'apiKey': self.api_config['coinbase_api_key'],
                'secret': self.api_config['coinbase_api_secret'],
                'passphrase': self.api_config['coinbase_passphrase'],
                'sandbox': self.api_config['sandbox'],
                'enableRateLimit': True,
            })
            print("✅ Exchange configuré avec nouvelles clés")
            return True
        except Exception as e:
            print(f"❌ Erreur configuration exchange: {e}")
            return False
    
    def get_portfolio_balance(self):
        """Obtenir le solde complet du portfolio avec tous les assets"""
        try:
            balance = self.exchange.fetch_balance()
            
            # Calculer la valeur totale en USD
            total_usd = 0.0
            portfolio_details = {}
            
            print("💰 PORTFOLIO COMPLET:")
            print("-" * 40)
            
            for currency, amounts in balance.items():
                if currency not in ['info', 'free', 'used', 'total'] and amounts.get('total', 0) > 0:
                    total = amounts.get('total', 0)
                    free = amounts.get('free', 0)
                    used = amounts.get('used', 0)
                    
                    # Essayer de convertir en USD
                    usd_value = 0.0
                    if currency == 'USD':
                        usd_value = total
                    else:
                        try:
                            # Obtenir le prix en USD
                            ticker_symbol = f"{currency}/USD"
                            ticker = self.exchange.fetch_ticker(ticker_symbol)
                            usd_value = total * ticker['last']
                        except:
                            # Si pas de pair USD directe, essayer avec BTC
                            try:
                                btc_symbol = f"{currency}/BTC"
                                btc_ticker = self.exchange.fetch_ticker(btc_symbol)
                                btc_usd_ticker = self.exchange.fetch_ticker("BTC/USD")
                                usd_value = total * btc_ticker['last'] * btc_usd_ticker['last']
                            except:
                                usd_value = 0  # Impossible de convertir
                    
                    if total > 0:
                        portfolio_details[currency] = {
                            'total': total,
                            'free': free,
                            'used': used,
                            'usd_value': usd_value
                        }
                        total_usd += usd_value
                        
                        print(f"  {currency}: {total:.8f} (${usd_value:.2f})")
            
            print("-" * 40)
            print(f"💰 TOTAL: ${total_usd:.2f}")
            print("-" * 40)
            
            self.portfolio_balance = total_usd
            self.portfolio_details = portfolio_details
            return total_usd
            
        except Exception as e:
            print(f"❌ Erreur récupération portfolio: {e}")
            return 0.0
    
    def get_market_data(self, symbol, timeframe='1h', limit=100):
        """Récupérer les données de marché avec gestion d'erreur améliorée"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            if not ohlcv or len(ohlcv) < 50:
                print(f"⚠️ Données insuffisantes pour {symbol}")
                return None
                
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            print(f"❌ Erreur données {symbol}: {e}")
            return None
    
    def calculate_rsi(self, prices, period=14):
        """Calcul RSI avec protection contre les erreurs"""
        try:
            if len(prices) < period + 1:
                return 50  # Valeur neutre si pas assez de données
                
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
        except Exception as e:
            print(f"❌ Erreur calcul RSI: {e}")
            return 50
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calcul MACD avec protection"""
        try:
            if len(prices) < slow + signal:
                return 0, 0, 'HOLD'
                
            exp1 = prices.ewm(span=fast).mean()
            exp2 = prices.ewm(span=slow).mean()
            macd_line = exp1 - exp2
            signal_line = macd_line.ewm(span=signal).mean()
            histogram = macd_line - signal_line
            
            current_macd = macd_line.iloc[-1] if not pd.isna(macd_line.iloc[-1]) else 0
            current_signal = signal_line.iloc[-1] if not pd.isna(signal_line.iloc[-1]) else 0
            
            if current_macd > current_signal:
                trend = 'BUY'
            elif current_macd < current_signal:
                trend = 'SELL'
            else:
                trend = 'HOLD'
                
            return current_macd, current_signal, trend
        except Exception as e:
            print(f"❌ Erreur calcul MACD: {e}")
            return 0, 0, 'HOLD'
    
    def calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """Calcul Bollinger Bands avec protection"""
        try:
            if len(prices) < period:
                return prices.iloc[-1] if len(prices) > 0 else 0, 0, 0, 'HOLD'
                
            rolling_mean = prices.rolling(window=period).mean()
            rolling_std = prices.rolling(window=period).std()
            upper_band = rolling_mean + (rolling_std * std_dev)
            lower_band = rolling_mean - (rolling_std * std_dev)
            
            current_price = prices.iloc[-1]
            current_upper = upper_band.iloc[-1] if not pd.isna(upper_band.iloc[-1]) else current_price * 1.02
            current_lower = lower_band.iloc[-1] if not pd.isna(lower_band.iloc[-1]) else current_price * 0.98
            current_middle = rolling_mean.iloc[-1] if not pd.isna(rolling_mean.iloc[-1]) else current_price
            
            if current_price <= current_lower:
                signal = 'BUY'
            elif current_price >= current_upper:
                signal = 'SELL'
            else:
                signal = 'HOLD'
                
            return current_price, current_upper, current_lower, signal
        except Exception as e:
            print(f"❌ Erreur calcul Bollinger: {e}")
            return 0, 0, 0, 'HOLD'
    
    def analyze_symbol(self, symbol):
        """Analyse technique complète d'un symbole"""
        try:
            print(f"📈 Analyse {symbol}...")
            
            # Récupération des données
            df = self.get_market_data(symbol)
            if df is None or len(df) < 50:
                return self.create_signal(symbol, 'HOLD', 0, "Données insuffisantes")
            
            prices = df['close']
            current_price = prices.iloc[-1]
            
            # Indicateurs techniques
            rsi = self.calculate_rsi(prices, self.config['rsi_period'])
            macd, macd_signal, macd_trend = self.calculate_macd(
                prices, 
                self.config['macd_fast'], 
                self.config['macd_slow'], 
                self.config['macd_signal']
            )
            price, bb_upper, bb_lower, bb_signal = self.calculate_bollinger_bands(
                prices, 
                self.config['bollinger_period'], 
                self.config['bollinger_std']
            )
            
            # Logique de trading
            signals = []
            signal_strength = 0
            
            # RSI
            if rsi < self.config['rsi_oversold']:
                signals.append('BUY')
                signal_strength += 30
            elif rsi > self.config['rsi_overbought']:
                signals.append('SELL')
                signal_strength += 30
            
            # MACD
            if macd_trend == 'BUY':
                signals.append('BUY')
                signal_strength += 25
            elif macd_trend == 'SELL':
                signals.append('SELL')
                signal_strength += 25
            
            # Bollinger Bands
            if bb_signal == 'BUY':
                signals.append('BUY')
                signal_strength += 20
            elif bb_signal == 'SELL':
                signals.append('SELL')
                signal_strength += 20
            
            # Décision finale
            buy_count = signals.count('BUY')
            sell_count = signals.count('SELL')
            
            if buy_count > sell_count and signal_strength >= 40:
                final_signal = 'BUY'
            elif sell_count > buy_count and signal_strength >= 40:
                final_signal = 'SELL'
            else:
                final_signal = 'HOLD'
            
            reason = f"RSI:{rsi:.1f} MACD:{macd_trend} BB:{bb_signal} Force:{signal_strength}"
            
            return self.create_signal(symbol, final_signal, signal_strength, reason, {
                'price': current_price,
                'rsi': rsi,
                'macd': macd,
                'macd_signal': macd_signal,
                'bb_upper': bb_upper,
                'bb_lower': bb_lower
            })
            
        except Exception as e:
            error_msg = f"Erreur: {str(e)}"
            print(f"❌ Erreur analyse {symbol}: {error_msg}")
            return self.create_signal(symbol, 'HOLD', 0, error_msg)
    
    def create_signal(self, symbol, signal, strength, reason, details=None):
        """Créer un signal de trading"""
        return {
            'symbol': symbol,
            'signal': signal,
            'strength': strength,
            'reason': reason,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
    
    def execute_trade(self, signal):
        """Simuler l'exécution d'un trade"""
        if not self.is_trading or signal['signal'] == 'HOLD':
            return False
        
        try:
            symbol = signal['symbol']
            action = signal['signal']
            strength = signal['strength']
            
            # Calcul de la taille de position
            position_size = self.portfolio_balance * self.config['max_position_size']
            if position_size < self.config['min_trade_amount']:
                print(f"❌ Position trop petite: ${position_size:.2f}")
                return False
            
            # Simulation du trade
            price = signal['details'].get('price', 0)
            if price > 0:
                if action == 'BUY':
                    quantity = position_size / price
                    self.profit_simulation += position_size * 0.001  # 0.1% profit simulé
                    print(f"💰 ACHAT simulé: {quantity:.6f} {symbol} à ${price:.2f}")
                elif action == 'SELL':
                    # Si on a une position, la vendre
                    self.profit_simulation += position_size * 0.001
                    print(f"💰 VENTE simulée: {symbol} à ${price:.2f}")
                
                self.trades_count += 1
                return True
                
        except Exception as e:
            print(f"❌ Erreur exécution trade: {e}")
        
        return False
    
    def trading_loop(self):
        """Boucle principale de trading"""
        print("🤖 DÉMARRAGE BOT IA TRADING AUTOMATISÉ")
        print("=" * 60)
        
        cycle = 0
        while self.is_running:
            try:
                cycle += 1
                self.last_cycle_time = datetime.now()
                print(f"\n🔄 CYCLE {cycle} - {self.last_cycle_time.strftime('%H:%M:%S')}")
                
                # Mise à jour balance
                self.get_portfolio_balance()
                
                # Analyse de chaque symbole
                for symbol in self.config['symbols']:
                    signal = self.analyze_symbol(symbol)
                    self.signals[symbol] = signal
                    
                    print(f"   Signal: {signal['signal']} | Force: {signal['strength']}")
                    print(f"   Raison: {signal['reason']}")
                    
                    # Exécution du trade si conditions remplies
                    if self.is_trading:
                        self.execute_trade(signal)
                
                # Statistiques
                print(f"\n📊 STATISTIQUES:")
                print(f"   🤖 Trades exécutés: {self.trades_count}")
                print(f"   💰 Profit simulé: ${self.profit_simulation:.2f}")
                print(f"   📈 Derniers signaux: {len([s for s in self.signals.values() if s['signal'] != 'HOLD'])}")
                
                # Pause
                print(f"\n⏳ Pause {self.config['trading_interval']} secondes avant prochain cycle...")
                time.sleep(self.config['trading_interval'])
                
            except KeyboardInterrupt:
                print("🛑 Arrêt demandé par l'utilisateur")
                break
            except Exception as e:
                print(f"❌ Erreur dans la boucle trading: {e}")
                time.sleep(5)
        
        print("🛑 Arrêt du bot IA...")
        self.is_running = False
        self.is_trading = False

# Interface Web avec Flask et SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Template HTML avec paramètres visibles
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 IA Trading Bot - Dashboard Pro</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.6.1/socket.io.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #00ff00;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        .matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0.1;
            pointer-events: none;
            z-index: -1;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            background: rgba(0, 255, 0, 0.1);
            padding: 20px;
            border-radius: 15px;
            border: 2px solid #00ff00;
            box-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
        }
        
        .header h1 {
            font-size: 2.5em;
            text-shadow: 0 0 20px #00ff00;
            margin-bottom: 10px;
        }
        
        .status {
            font-size: 1.2em;
            color: #00ff00;
        }
        
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #00ff00;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .card:hover {
            box-shadow: 0 0 30px rgba(0, 255, 0, 0.4);
            transform: translateY(-5px);
        }
        
        .card h3 {
            color: #00ff00;
            margin-bottom: 15px;
            font-size: 1.4em;
            text-align: center;
            text-shadow: 0 0 10px #00ff00;
        }
        
        .controls {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 15px 30px;
            font-size: 1.1em;
            border: 2px solid #00ff00;
            background: rgba(0, 255, 0, 0.1);
            color: #00ff00;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            font-weight: bold;
            text-shadow: 0 0 10px #00ff00;
        }
        
        .btn:hover {
            background: rgba(0, 255, 0, 0.3);
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            transform: scale(1.05);
        }
        
        .btn.active {
            background: rgba(0, 255, 0, 0.5);
            box-shadow: 0 0 25px rgba(0, 255, 0, 0.7);
        }
        
        .parameter-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .param-item {
            background: rgba(0, 255, 0, 0.1);
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid #00ff00;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .param-label {
            font-weight: bold;
            color: #00ff00;
        }
        
        .param-value {
            color: #00ccff;
            font-family: monospace;
        }
        
        .signals-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .signal-card {
            background: rgba(0, 0, 0, 0.9);
            border: 2px solid #00ff00;
            border-radius: 10px;
            padding: 15px;
            position: relative;
        }
        
        .signal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .signal-symbol {
            font-weight: bold;
            font-size: 1.2em;
            color: #00ff00;
        }
        
        .signal-action {
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 0.9em;
        }
        
        .signal-action.BUY {
            background: rgba(0, 255, 0, 0.3);
            color: #00ff00;
            border: 1px solid #00ff00;
        }
        
        .signal-action.SELL {
            background: rgba(255, 0, 0, 0.3);
            color: #ff4444;
            border: 1px solid #ff4444;
        }
        
        .signal-action.HOLD {
            background: rgba(255, 255, 0, 0.3);
            color: #ffff00;
            border: 1px solid #ffff00;
        }
        
        .signal-details {
            font-size: 0.9em;
            color: #cccccc;
            margin: 5px 0;
        }
        
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 255, 0, 0.9);
            color: #000;
            padding: 15px 20px;
            border-radius: 10px;
            border: 2px solid #00ff00;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            z-index: 1000;
            transform: translateX(400px);
            transition: transform 0.3s ease;
        }
        
        .notification.show {
            transform: translateX(0);
        }
        
        .portfolio-info {
            text-align: center;
            font-size: 1.1em;
            margin: 10px 0;
        }
        
        .portfolio-balance {
            color: #00ff00;
            font-weight: bold;
            font-size: 1.3em;
            text-shadow: 0 0 10px #00ff00;
        }
        
        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
            .controls {
                flex-direction: column;
                align-items: center;
            }
            .header h1 {
                font-size: 1.8em;
            }
        }
    </style>
</head>
<body>
    <div class="matrix-bg"></div>
    
    <div class="container">
        <div class="header">
            <h1>🤖 IA TRADING BOT</h1>
            <div class="status" id="connectionStatus">Connexion en cours...</div>
            <div class="portfolio-info">
                Portfolio: <span class="portfolio-balance" id="portfolioBalance">$0.00</span>
            </div>
        </div>
        
        <div class="controls">
            <button class="btn" id="startBtn" onclick="startTrading()">🚀 START TRADING</button>
            <button class="btn" id="stopBtn" onclick="stopTrading()">🛑 STOP TRADING</button>
            <button class="btn" onclick="refreshData()">🔄 REFRESH</button>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>📊 PARAMÈTRES DE TRADING</h3>
                <div class="parameter-grid">
                    <div class="param-item">
                        <span class="param-label">Max Position:</span>
                        <span class="param-value" id="maxPosition">2%</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">Stop Loss:</span>
                        <span class="param-value" id="stopLoss">3%</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">Take Profit:</span>
                        <span class="param-value" id="takeProfit">5%</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">RSI Période:</span>
                        <span class="param-value" id="rsiPeriod">14</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">RSI Survente:</span>
                        <span class="param-value" id="rsiOversold">30</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">RSI Surachat:</span>
                        <span class="param-value" id="rsiOverbought">70</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">MACD Rapide:</span>
                        <span class="param-value" id="macdFast">12</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">MACD Lent:</span>
                        <span class="param-value" id="macdSlow">26</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">Bollinger Période:</span>
                        <span class="param-value" id="bbPeriod">20</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">Intervalle Trading:</span>
                        <span class="param-value" id="tradingInterval">30s</span>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h3>📈 STATISTIQUES</h3>
                <div class="parameter-grid">
                    <div class="param-item">
                        <span class="param-label">Trades Exécutés:</span>
                        <span class="param-value" id="tradesCount">0</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">Profit Simulé:</span>
                        <span class="param-value" id="profitSimulation">$0.00</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">Dernier Cycle:</span>
                        <span class="param-value" id="lastCycle">N/A</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">Bot Status:</span>
                        <span class="param-value" id="botStatus">Arrêté</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">Trading Actif:</span>
                        <span class="param-value" id="tradingStatus">Non</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">Signaux Actifs:</span>
                        <span class="param-value" id="activeSignals">0</span>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h3>🎯 SYMBOLES TRADÉS</h3>
                <div class="parameter-grid">
                    <div class="param-item">
                        <span class="param-label">Bitcoin:</span>
                        <span class="param-value">BTC/USD</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">Ethereum:</span>
                        <span class="param-value">ETH/USD</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">Solana:</span>
                        <span class="param-value">SOL/USD</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">Montant Min:</span>
                        <span class="param-value" id="minAmount">$5.00</span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3>🔮 SIGNAUX DE TRADING EN TEMPS RÉEL</h3>
            <div class="signals-grid" id="signalsContainer">
                <p style="text-align: center; color: #cccccc;">Aucun signal disponible</p>
            </div>
        </div>
    </div>
    
    <div class="notification" id="notification"></div>
    
    <script>
        const socket = io();
        let isConnected = false;
        
        socket.on('connect', function() {
            isConnected = true;
            document.getElementById('connectionStatus').textContent = '✅ Connecté au bot IA';
            loadParameters();
            refreshData();
        });
        
        socket.on('disconnect', function() {
            isConnected = false;
            document.getElementById('connectionStatus').textContent = '❌ Connexion perdue';
        });
        
        socket.on('trade_signal', function(data) {
            showNotification(`Signal ${data.signal} pour ${data.symbol} (Force: ${data.strength})`);
            refreshSignals();
        });
        
        socket.on('trade_executed', function(data) {
            showNotification(`Trade exécuté: ${data.action} ${data.symbol} à $${data.price}`);
            refreshData();
        });
        
        function loadParameters() {
            // Chargement des paramètres depuis la configuration
            document.getElementById('maxPosition').textContent = '2%';
            document.getElementById('stopLoss').textContent = '3%';
            document.getElementById('takeProfit').textContent = '5%';
            document.getElementById('rsiPeriod').textContent = '14';
            document.getElementById('rsiOversold').textContent = '30';
            document.getElementById('rsiOverbought').textContent = '70';
            document.getElementById('macdFast').textContent = '12';
            document.getElementById('macdSlow').textContent = '26';
            document.getElementById('bbPeriod').textContent = '20';
            document.getElementById('tradingInterval').textContent = '30s';
            document.getElementById('minAmount').textContent = '$5.00';
        }
        
        function startTrading() {
            fetch('/api/trading/start')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('startBtn').classList.add('active');
                        document.getElementById('stopBtn').classList.remove('active');
                        showNotification('Trading automatique démarré!');
                    }
                });
        }
        
        function stopTrading() {
            fetch('/api/trading/stop')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('stopBtn').classList.add('active');
                        document.getElementById('startBtn').classList.remove('active');
                        showNotification('Trading automatique arrêté!');
                    }
                });
        }
        
        function refreshData() {
            refreshStatus();
            refreshPortfolio();
            refreshSignals();
        }
        
        function refreshStatus() {
            fetch('/api/trading/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('tradesCount').textContent = data.trades_count || 0;
                    document.getElementById('profitSimulation').textContent = `$${(data.profit_simulation || 0).toFixed(2)}`;
                    document.getElementById('lastCycle').textContent = data.last_cycle || 'N/A';
                    document.getElementById('botStatus').textContent = data.is_running ? 'Actif' : 'Arrêté';
                    document.getElementById('tradingStatus').textContent = data.is_trading ? 'Oui' : 'Non';
                    
                    if (data.is_trading) {
                        document.getElementById('startBtn').classList.add('active');
                        document.getElementById('stopBtn').classList.remove('active');
                    } else {
                        document.getElementById('startBtn').classList.remove('active');
                        document.getElementById('stopBtn').classList.add('active');
                    }
                });
        }
        
        function refreshPortfolio() {
            fetch('/api/portfolio')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('portfolioBalance').textContent = `$${(data.balance || 0).toFixed(2)}`;
                });
        }
        
        function refreshSignals() {
            fetch('/api/signals')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('signalsContainer');
                    const signals = data.signals || {};
                    
                    if (Object.keys(signals).length === 0) {
                        container.innerHTML = '<p style="text-align: center; color: #cccccc;">Aucun signal disponible</p>';
                        document.getElementById('activeSignals').textContent = '0';
                        return;
                    }
                    
                    let activeCount = 0;
                    let html = '';
                    
                    for (const [symbol, signal] of Object.entries(signals)) {
                        if (signal.signal !== 'HOLD') activeCount++;
                        
                        html += `
                            <div class="signal-card">
                                <div class="signal-header">
                                    <span class="signal-symbol">${symbol}</span>
                                    <span class="signal-action ${signal.signal}">${signal.signal}</span>
                                </div>
                                <div class="signal-details">Force: ${signal.strength}%</div>
                                <div class="signal-details">${signal.reason}</div>
                                <div class="signal-details">Prix: $${(signal.details?.price || 0).toFixed(2)}</div>
                                <div class="signal-details">RSI: ${(signal.details?.rsi || 0).toFixed(1)}</div>
                                <div class="signal-details">${new Date(signal.timestamp).toLocaleTimeString()}</div>
                            </div>
                        `;
                    }
                    
                    container.innerHTML = html;
                    document.getElementById('activeSignals').textContent = activeCount;
                });
        }
        
        function showNotification(message) {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.classList.add('show');
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 3000);
        }
        
        // Actualisation automatique
        setInterval(refreshData, 5000);
        
        // Chargement initial
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(refreshData, 1000);
            });
        } else {
            setTimeout(refreshData, 1000);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/trading/start')
def start_trading():
    try:
        if not bot.is_running:
            bot.is_running = True
            threading.Thread(target=bot.trading_loop, daemon=True).start()
        bot.is_trading = True
        return jsonify({'success': True, 'message': 'Trading démarré'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/trading/stop')
def stop_trading():
    bot.is_trading = False
    return jsonify({'success': True, 'message': 'Trading arrêté'})

@app.route('/api/trading/status')
def trading_status():
    return jsonify({
        'is_running': bot.is_running,
        'is_trading': bot.is_trading,
        'trades_count': bot.trades_count,
        'profit_simulation': bot.profit_simulation,
        'last_cycle': bot.last_cycle_time.strftime('%H:%M:%S') if bot.last_cycle_time else None
    })

@app.route('/api/portfolio')
def portfolio_info():
    balance = bot.get_portfolio_balance()
    return jsonify({
        'balance': balance,
        'details': getattr(bot, 'portfolio_details', {}),
        'last_update': datetime.now().isoformat()
    })

@app.route('/api/signals')
def get_signals():
    return jsonify({'signals': bot.signals})

# Initialisation du bot global
bot = AITradingBot()
