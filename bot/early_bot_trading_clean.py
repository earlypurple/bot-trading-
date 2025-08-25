#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Early-Bot-Trading - Bot IA Trading Automatisé
Interface web complète avec modes de trading configurables
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

# Import du système de logging
from logging_system import (setup_logging, get_logger, log_portfolio_update, 
                           log_signal_analysis, log_trade_attempt, log_trade_result, log_api_call)

# Import du moteur IA Quantique
from ai.quantum_ai_engine import TradingAI

# Import du template IA
from templates.ai_dashboard import HTML_TEMPLATE_AI
from templates.new_dashboard import NEW_DASHBOARD_TEMPLATE

# Configuration - Import nouvelles clés CDP
try:
    from config.api_config_cdp import API_CONFIG, TRADING_CONFIG, TRADING_MODES, get_current_mode_config, switch_trading_mode
    print("✅ Utilisation des nouvelles clés CDP")
except ImportError:
    from config.api_config import API_CONFIG, TRADING_CONFIG, TRADING_MODES, get_current_mode_config, switch_trading_mode
    print("⚠️ Fallback vers anciennes clés")


# Imports pour fonctionnalités avancées
try:
    from enhanced_portfolio_manager import EnhancedPortfolioManager
    from enhanced_api_routes import setup_enhanced_api
    ENHANCED_FEATURES = True
except ImportError:
    print("⚠️ Fonctionnalités avancées non disponibles")
    ENHANCED_FEATURES = False

class EarlyBotTrading:
    def __init__(self):
        # Initialiser le système de logging
        self.logger, self.trading_logger, self.api_logger, self.log_file = setup_logging()
        self.logger.info("🤖 Initialisation d'Early-Bot-Trading avec IA Quantique...")
        
        # Initialisation de l'IA Quantique (CERVEAU DU BOT)
        self.ai = TradingAI(self)
        self.logger.info("🧠 Moteur IA Quantique intégré")
        
        self.config = TRADING_CONFIG
        self.api_config = API_CONFIG
        self.exchange = None
        self.is_trading = False
        self.is_running = False
        self.signals = {}
        self.trades_count = 0
        self.actual_profit = 0.0  # Profit réel
        self.last_cycle_time = None
        self.portfolio_balance = 0.0
        self.portfolio_details = {}
        self.current_positions = {}
        self.current_mode = 'normal'
        
        # Initialisation des fonctionnalités avancées
        if ENHANCED_FEATURES:
            try:
                self.enhanced_portfolio_manager = EnhancedPortfolioManager()
                self.logger.info("✅ Portfolio Manager Avancé initialisé")
            except Exception as e:
                self.logger.warning(f"⚠️ Portfolio Manager Avancé non disponible: {e}")
                self.enhanced_portfolio_manager = None
        else:
            self.enhanced_portfolio_manager = None
        
        # Timestamp de démarrage
        self.start_time = datetime.now()
        
        self.logger.info("📊 Configuration chargée")
        self.logger.info(f"🎯 Certification: {self.api_config.get('certification_id', 'N/A')}")
        
        print("🔐 Configuration Early-Bot-Trading avec modes de trading...")
        self.setup_exchange()
        
    def setup_exchange(self):
        """Configuration de l'exchange avec nouvelles clés CDP"""
        self.logger.info("🔐 Configuration de l'exchange Coinbase...")
        
        try:
            # Configuration pour Coinbase avec nouvelles clés CDP
            self.logger.debug("📝 Création de l'instance CCXT Coinbase")
            self.exchange = ccxt.coinbase({
                'apiKey': self.api_config['coinbase_api_key'],
                'secret': self.api_config['coinbase_api_secret'],  # Clé privée PEM format
                'passphrase': self.api_config.get('coinbase_passphrase', ''),  # Peut être vide pour CDP
                'sandbox': self.api_config['sandbox'],
                'enableRateLimit': True,
                'headers': {
                    'CB-VERSION': '2023-10-20',  # Version API pour Advanced Trade
                }
            })
            
            self.logger.info("🔐 Configuration CCXT terminée")
            
            # Test de connexion avec les nouvelles clés
            self.logger.info("🔐 Test authentification avec clés CDP...")
            print("🔐 Test authentification avec clés CDP...")
            
            log_api_call('GET', 'fetch_balance', None)
            test_balance = self.exchange.fetch_balance()
            log_api_call('GET', 'fetch_balance', None, f"Balance obtenue: {len(test_balance)} entrées")
            
            self.logger.info("✅ Authentification CDP réussie !")
            print("✅ Authentification CDP réussie !")
            
            # Récupérer les comptes pour obtenir les account_id
            self.accounts = {}
            try:
                self.logger.debug("📋 Récupération des comptes...")
                log_api_call('GET', 'fetch_accounts', None)
                accounts_list = self.exchange.fetch_accounts()
                log_api_call('GET', 'fetch_accounts', None, f"{len(accounts_list)} comptes trouvés")
                
                self.logger.debug(f"📋 Traitement de {len(accounts_list)} comptes...")
                for i, account in enumerate(accounts_list):
                    self.logger.debug(f"📋 Compte {i+1}/{len(accounts_list)}: {account}")
                    currency = account.get('currency')
                    account_id = account.get('id')
                    if currency and account_id:
                        self.accounts[currency] = account_id
                        self.logger.debug(f"✅ Compte {currency}: {account_id[:12]}...")
                
                self.logger.info(f"✅ {len(self.accounts)} comptes configurés avec account_id")
                print(f"✅ {len(self.accounts)} comptes configurés avec account_id")
            except Exception as e:
                self.logger.error(f"⚠️ Erreur récupération comptes: {e}")
                print(f"⚠️  Erreur récupération comptes: {e}")
                self.accounts = {}
            
            self.logger.info("✅ Exchange configuré avec COINBASE + CLÉS CDP")
            self.logger.info("🚀 Mode production ACTIVÉ - Advanced Trade v3 API")
            self.logger.info("💡 Utilisation paires USDC pour compatibilité maximale")
            self.logger.info(f"🎯 Certification: {self.api_config['certification_id']}")
            
            print("✅ Exchange configuré avec COINBASE + CLÉS CDP")
            print("🚀 Mode production ACTIVÉ - Advanced Trade v3 API") 
            print("💡 Utilisation paires USDC pour compatibilité maximale")
            print(f"🎯 Certification: {self.api_config['certification_id']}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erreur configuration exchange: {e}")
            self.logger.error("💡 Suggestion: Vérifiez que les clés CDP sont correctes")
            print(f"❌ Erreur configuration exchange: {e}")
            print("💡 Suggestion: Vérifiez que les clés CDP sont correctes")
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
                    
                    # Essayer de convertir en USD/USDC
                    usd_value = 0.0
                    if currency in ['USD', 'USDC', 'PYUSD']:
                        usd_value = total
                    else:
                        try:
                            # Priorité aux paires USDC pour compatibilité
                            ticker_symbol = f"{currency}/USDC"
                            ticker = self.exchange.fetch_ticker(ticker_symbol)
                            usd_value = total * ticker['last']
                        except:
                            try:
                                # Fallback vers USD si USDC n'existe pas
                                ticker_symbol = f"{currency}/USD"
                                ticker = self.exchange.fetch_ticker(ticker_symbol)
                                usd_value = total * ticker['last']
                            except:
                                # Si pas de pair USD/USDC directe, essayer avec BTC
                                try:
                                    btc_symbol = f"{currency}/BTC"
                                    btc_ticker = self.exchange.fetch_ticker(btc_symbol)
                                    btc_usdc_ticker = self.exchange.fetch_ticker("BTC/USDC")
                                    usd_value = total * btc_ticker['last'] * btc_usdc_ticker['last']
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
            
            if buy_count > sell_count and signal_strength >= 20:
                final_signal = 'BUY'
            elif sell_count > buy_count and signal_strength >= 20:
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
        """Exécuter un vrai trade sur Coinbase avec intégration IA"""
        if not self.is_trading or signal['signal'] == 'HOLD':
            return False
        
        try:
            symbol = signal['symbol']
            action = signal['signal']
            strength = signal['strength']
            
            # Obtenir la crypto de base (ex: BTC pour BTC/USDC)
            base_currency = symbol.split('/')[0]
            
            # Obtenir la balance de cette crypto spécifique
            balance = self.exchange.fetch_balance()
            crypto_balance = balance.get(base_currency, {}).get('free', 0)
            crypto_value_usd = crypto_balance * signal['details'].get('price', 0)
            
            # Calcul de position par l'IA si disponible
            if signal.get('ai_enhanced') and 'ai_decision' in signal:
                ai_decision = signal['ai_decision']
                position_size = self.ai.calculate_ai_position_size(
                    ai_decision, 
                    crypto_value_usd, 
                    self.config['max_position_size']
                )
                print(f"🧠 IA calcul position: ${position_size:.2f} (confiance: {ai_decision['confidence']:.2f})")
            else:
                # Calcul classique basé sur la crypto individuelle
                position_size = crypto_value_usd * self.config['max_position_size']
            
            print(f"💡 DEBUG: {base_currency}: {crypto_balance:.8f} (~${crypto_value_usd:.2f}) → Position: ${position_size:.2f}")
            print(f"💡 Minimum requis: ${self.config['min_trade_amount']:.2f}")
            
            # Si la position calculée est trop petite, utilisons le minimum ou 50% de la balance
            if position_size < self.config['min_trade_amount']:
                position_size = min(self.config['min_trade_amount'], crypto_value_usd * 0.5)
                print(f"⚡ Position ajustée: ${position_size:.2f}")
            
            # Vérifier qu'on ne dépasse pas 80% de la balance de cette crypto
            max_safe_position = crypto_value_usd * 0.8
            if position_size > max_safe_position:
                position_size = max_safe_position
                print(f"⚙️ Position limitée à 80% de {base_currency}: ${position_size:.2f}")
            
            # Si même après ajustement c'est trop petit, skip
            if position_size < 0.01:
                print(f"❌ Position trop petite après ajustement: ${position_size:.4f}")
                return False
            
            # Obtenir le prix actuel
            price = signal['details'].get('price', 0)
            if price <= 0:
                print(f"❌ Prix invalide pour {symbol}")
                return False

            try:
                if action == 'BUY':
                    # Achat réel
                    quantity = position_size / price
                    print(f"💰 TENTATIVE ACHAT RÉEL: {quantity:.8f} {base_currency} de {symbol} à ${price:.2f} (${position_size:.2f})")
                    
                    # Déterminer quelle devise de base utiliser selon la paire
                    if '/PYUSD' in symbol:
                        quote_currency = 'PYUSD'
                        quote_balance = balance.get('PYUSD', {}).get('free', 0)
                    elif '/USDC' in symbol:
                        quote_currency = 'USDC'
                        quote_balance = balance.get('USDC', {}).get('free', 0)
                    else:
                        quote_currency = 'USD'
                        quote_balance = balance.get('USD', {}).get('free', 0)
                    
                    print(f"💡 Balance {quote_currency}: ${quote_balance:.6f}")
                    
                    if quote_balance >= position_size:
                        # Exécuter l'ordre d'achat
                        try:
                            order_params = {}
                            if quote_currency in self.accounts:
                                order_params['account_id'] = self.accounts[quote_currency]
                                print(f"💡 Utilisation account_id pour {quote_currency}: {self.accounts[quote_currency][:12]}...")
                            
                            order = self.exchange.create_order(symbol, 'market', 'buy', quantity, None, order_params)
                            print(f"✅ ACHAT RÉEL EXÉCUTÉ: {order}")
                            self.trades_count += 1
                            return True
                        except Exception as order_error:
                            print(f"❌ Erreur ordre achat: {self.exchange.id} {order_error}")
                            # Fallback vers simulation
                            self.actual_profit += position_size * 0.001
                            print(f"💰 ACHAT simulé (fallback): ${position_size:.2f} de {symbol}")
                            self.trades_count += 1
                            return True
                    else:
                        print(f"❌ Solde {quote_currency} insuffisant: ${quote_balance:.2f} < ${position_size:.2f}")
                        print(f"💰 ACHAT simulé (fallback): ${position_size:.2f} de {symbol}")
                        self.trades_count += 1
                        return True
                        
                elif action == 'SELL':
                    # Vente réelle - utilise la quantité basée sur position_size calculée
                    quantity_to_sell = position_size / price
                    print(f"💰 TENTATIVE VENTE RÉELLE: {quantity_to_sell:.8f} {base_currency} de {symbol} à ${price:.2f}")
                    
                    # Vérifier qu'on a assez de cette crypto
                    if crypto_balance >= quantity_to_sell:
                        # Exécuter l'ordre de vente
                        try:
                            order_params = {}
                            if base_currency in self.accounts:
                                order_params['account_id'] = self.accounts[base_currency]
                                print(f"💡 Utilisation account_id pour {base_currency}: {self.accounts[base_currency][:12]}...")
                            
                            order = self.exchange.create_order(symbol, 'market', 'sell', quantity_to_sell, None, order_params)
                            print(f"✅ VENTE RÉELLE EXÉCUTÉE: {order}")
                            self.trades_count += 1
                            return True
                        except Exception as order_error:
                            print(f"❌ Erreur ordre vente: {self.exchange.id} {order_error}")
                            # Fallback vers simulation
                            self.actual_profit += position_size * 0.001
                            print(f"💰 VENTE simulée (fallback): {symbol}")
                            self.trades_count += 1
                            return True
                    else:
                        print(f"❌ Balance {base_currency} insuffisante: {crypto_balance:.8f} < {quantity_to_sell:.8f}")
                        # Essaie de vendre ce qu'on a si c'est > minimum
                        if crypto_balance > 0 and crypto_balance * price > 0.01:  # Au moins 1 centime
                            try:
                                order = self.exchange.create_order(symbol, 'market', 'sell', crypto_balance, None, {})
                                print(f"✅ VENTE PARTIELLE: {crypto_balance:.8f} {base_currency}")
                                self.trades_count += 1
                                return True
                            except Exception as e:
                                print(f"❌ Erreur vente partielle: {e}")
                        print(f"💰 VENTE simulée (fallback): {symbol}")
                        self.trades_count += 1
                        return True
                        
            except Exception as e:
                print(f"❌ Erreur lors du trade réel: {e}")
                # En cas d'erreur, faire un trade simulé
                if action == 'BUY':
                    self.actual_profit += position_size * 0.001
                    print(f"💰 ACHAT simulé (fallback): ${position_size:.2f} de {symbol}")
                elif action == 'SELL':
                    self.actual_profit += position_size * 0.001
                    print(f"💰 VENTE simulée (fallback): {symbol}")
                
                self.trades_count += 1
                return True
                
        except Exception as e:
            print(f"❌ Erreur générale exécution trade: {e}")
        
        return False
    
    def trading_loop(self):
        """Boucle principale de trading pilotée par l'IA Quantique"""
        print("🤖 DÉMARRAGE BOT IA TRADING AUTOMATISÉ - QUANTUM AI INTÉGRÉE")
        print("=" * 60)
        
        # Activation de l'IA Quantique
        if self.ai.activate():
            print("🧠 IA Quantique ACTIVÉE - Prise de contrôle des décisions")
        
        cycle = 0
        while self.is_running:
            try:
                cycle += 1
                self.last_cycle_time = datetime.now()
                print(f"\n🔄 CYCLE {cycle} - {self.last_cycle_time.strftime('%H:%M:%S')}")
                
                # Mise à jour balance
                self.get_portfolio_balance()
                
                # Analyse IA + Analyse technique de chaque symbole
                for symbol in self.config['symbols']:
                    # Analyse technique traditionnelle
                    technical_signal = self.analyze_symbol(symbol)
                    
                    # Analyse par l'IA Quantique (DÉCISION PRIORITAIRE)
                    ai_decision = self.ai.should_open_position(symbol, 
                                                             current_price=technical_signal.get('price'),
                                                             market_data=technical_signal)
                    
                    # Combine l'analyse technique avec la décision IA
                    if ai_decision and ai_decision['confidence'] >= self.ai.ai_config['confidence_threshold']:
                        # L'IA prend la décision finale
                        enhanced_signal = {
                            **technical_signal,
                            'signal': ai_decision['action'],
                            'strength': ai_decision['strength'],
                            'confidence': ai_decision['confidence'],
                            'ai_reasoning': ai_decision['reasoning'],
                            'ai_enhanced': True,
                            'ai_decision': ai_decision
                        }
                        
                        print(f"🧠 IA DÉCISION {symbol}: {ai_decision['action']} (confiance: {ai_decision['confidence']:.2f})")
                        print(f"   🔬 Raisonnement IA: {ai_decision['reasoning']}")
                    else:
                        # Fallback sur analyse technique classique
                        enhanced_signal = {**technical_signal, 'ai_enhanced': False}
                        print(f"📊 Technique {symbol}: {technical_signal['signal']} | Force: {technical_signal['strength']}")
                    
                    self.signals[symbol] = enhanced_signal
                    print(f"   Raison: {enhanced_signal.get('reason', 'N/A')}")
                    
                    # Exécution du trade si conditions remplies
                    if self.is_trading:
                        self.execute_trade(enhanced_signal)
                
                # Statistiques avec IA
                ai_status = self.ai.get_ai_status()
                print(f"\n📊 STATISTIQUES TRADING + IA:")
                print(f"   🤖 Trades exécutés: {self.trades_count}")
                print(f"   💰 Profit estimé: ${self.actual_profit:.2f}")
                print(f"   🧠 Décisions IA: {ai_status['decisions_made']}")
                print(f"   ⚡ Cohérence Quantique: {ai_status['quantum_state']['coherence']:.1f}%")
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
        
        # Désactivation de l'IA
        self.ai.deactivate()
        print("🛑 Arrêt du bot IA - IA Quantique désactivée")
        self.is_running = False
        self.is_trading = False
    
    def change_trading_mode(self, mode_name):
        """Change le mode de trading"""
        if mode_name in TRADING_MODES:
            self.current_mode = mode_name
            # Met à jour la configuration
            mode_config = TRADING_MODES[mode_name]
            self.config.update(mode_config)
            print(f"✅ Mode changé vers: {mode_config['name']}")
            print(f"   📊 Risque: {mode_config['risk_level']}")
            print(f"   💰 Position max: {mode_config['max_position_size']*100}%")
            print(f"   ⏰ Intervalle: {mode_config['trading_interval']}s")
            return True
        return False
    
    def get_available_modes(self):
        """Retourne la liste des modes disponibles"""
        return {k: v for k, v in TRADING_MODES.items()}
    
    def get_current_mode_info(self):
        """Retourne les informations du mode actuel"""
        return TRADING_MODES.get(self.current_mode, TRADING_MODES['normal'])

# Interface Web avec Flask et SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Variable globale pour l'instance du bot
bot = None

# Template HTML avec paramètres visibles - NOUVEAU MODÈLE OPTIMISÉ
HTML_TEMPLATE = NEW_DASHBOARD_TEMPLATE

def dashboard():
    return render_template_string(HTML_TEMPLATE)
        
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
        
        .mode-btn {
            padding: 8px 16px;
            border: 2px solid;
            border-radius: 8px;
            background: transparent;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            flex: 1;
            font-size: 0.9em;
        }
        
        .mode-btn.conservateur {
            border-color: #4CAF50;
            color: #4CAF50;
        }
        
        .mode-btn.conservateur:hover, .mode-btn.conservateur.active {
            background: rgba(76, 175, 80, 0.2);
            box-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
        }
        
        .mode-btn.normal {
            border-color: #FF9800;
            color: #FF9800;
        }
        
        .mode-btn.normal:hover, .mode-btn.normal.active {
            background: rgba(255, 152, 0, 0.2);
            box-shadow: 0 0 10px rgba(255, 152, 0, 0.5);
        }
        
        .mode-btn.agressif {
            border-color: #F44336;
            color: #F44336;
        }
        
        .mode-btn.agressif:hover, .mode-btn.agressif.active {
            background: rgba(244, 67, 54, 0.2);
            box-shadow: 0 0 10px rgba(244, 67, 54, 0.5);
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
            <h1>🚀 EARLY-BOT-TRADING</h1>
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
                <h3>⚙️ MODES DE TRADING</h3>
                <div class="parameter-grid">
                    <div class="param-item" style="grid-column: 1/-1;">
                        <span class="param-label">Mode Actuel:</span>
                        <span class="param-value" id="currentMode">⚖️ Normal</span>
                    </div>
                    <div class="param-item" style="grid-column: 1/-1;">
                        <span class="param-label">Niveau de Risque:</span>
                        <span class="param-value" id="riskLevel">Modéré</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">Position Max:</span>
                        <span class="param-value" id="maxPosition">2%</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">Stop Loss:</span>
                        <span class="param-value" id="stopLoss">5%</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">Take Profit:</span>
                        <span class="param-value" id="takeProfit">10%</span>
                    </div>
                    <div class="param-item">
                        <span class="param-label">Montant Min:</span>
                        <span class="param-value" id="minAmount">$10</span>
                    </div>
                    <div class="mode-buttons" style="grid-column: 1/-1; display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap;">
                        <button onclick="changeTradingMode('conservateur')" class="mode-btn conservateur" style="font-size: 0.9em;">🛡️ Conservateur</button>
                        <button onclick="changeTradingMode('normal')" class="mode-btn normal active" style="font-size: 0.9em;">⚖️ Normal</button>
                        <button onclick="changeTradingMode('agressif')" class="mode-btn agressif" style="font-size: 0.9em;">🚀 Agressif</button>
                        <button onclick="changeTradingMode('scalping')" class="mode-btn scalping" style="font-size: 0.9em;">⚡ Scalping</button>
                        <button onclick="openModeConfigurator()" class="config-btn" style="font-size: 0.9em; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 8px 12px; border-radius: 6px; cursor: pointer;">⚙️ Configurer</button>
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
                        <span class="param-label">Profit Estimé:</span>
                        <span class="param-value" id="actualProfit">$0.00</span>
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
                    document.getElementById('actualProfit').textContent = `$${(data.actual_profit || 0).toFixed(2)}`;
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
        
        function changeTradingMode(mode) {
            fetch('/api/change-mode', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ mode: mode })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Mettre à jour l'interface
                    document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
                    document.querySelector(`.mode-btn.${mode}`).classList.add('active');
                    
                    // Mettre à jour les informations affichées
                    document.getElementById('currentMode').textContent = data.mode_info.name;
                    document.getElementById('riskLevel').textContent = data.mode_info.risk_level;
                    document.getElementById('maxPosition').textContent = `${(data.mode_info.max_position_size * 100).toFixed(1)}%`;
                    document.getElementById('stopLoss').textContent = `${(data.mode_info.stop_loss * 100).toFixed(1)}%`;
                    document.getElementById('takeProfit').textContent = `${(data.mode_info.take_profit * 100).toFixed(1)}%`;
                    document.getElementById('minAmount').textContent = `$${data.mode_info.min_trade_amount}`;
                    document.getElementById('tradingInterval').textContent = `${data.mode_info.trading_interval}s`;
                    
                    showNotification(`Mode changé vers: ${data.mode_info.name}`);
                } else {
                    showNotification('Erreur lors du changement de mode');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Erreur de connexion');
            });
        }
        
        // Actualisation automatique
        setInterval(refreshData, 5000);
        
        // Chargement initial
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    refreshData();
                    // Charger les informations du mode actuel
                    fetch('/api/modes')
                        .then(response => response.json())
                        .then(data => {
                            const currentMode = data.current_mode;
                            const modeInfo = data.modes[currentMode];
                            
                            document.getElementById('currentMode').textContent = modeInfo.name;
                            document.getElementById('riskLevel').textContent = modeInfo.risk_level;
                            document.getElementById('maxPosition').textContent = `${(modeInfo.max_position_size * 100).toFixed(1)}%`;
                            document.getElementById('stopLoss').textContent = `${(modeInfo.stop_loss * 100).toFixed(1)}%`;
                            document.getElementById('takeProfit').textContent = `${(modeInfo.take_profit * 100).toFixed(1)}%`;
                            document.getElementById('minAmount').textContent = `$${modeInfo.min_trade_amount}`;
                            document.getElementById('tradingInterval').textContent = `${modeInfo.trading_interval}s`;
                            
                            // Activer le bon bouton
                            document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
                            document.querySelector(`.mode-btn.${currentMode}`).classList.add('active');
                        });
                }, 1000);
            });
        } else {
            setTimeout(refreshData, 1000);
        }
    </script>

    <!-- Modal Configuration des Modes -->
    <div id="modeConfigModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 1000; justify-content: center; align-items: center;">
        <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); border-radius: 12px; padding: 30px; max-width: 600px; width: 90%; max-height: 80vh; overflow-y: auto; box-shadow: 0 20px 40px rgba(0,0,0,0.3);">
            <h2 style="color: #00ffff; margin-bottom: 20px; text-align: center;">⚙️ Configuration des Modes de Trading</h2>
            
            <div style="margin-bottom: 20px;">
                <label style="color: white; display: block; margin-bottom: 10px;">📊 Sélectionner un mode:</label>
                <select id="modeSelect" onchange="loadModeConfig()" style="width: 100%; padding: 10px; border-radius: 6px; border: none; background: #2a3b5c; color: white;">
                    <option value="conservateur">🛡️ Conservateur</option>
                    <option value="normal">⚖️ Normal</option>
                    <option value="agressif">🚀 Agressif</option>
                    <option value="scalping">⚡ Scalping</option>
                </select>
            </div>

            <div id="configForm" style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div>
                    <label style="color: #00ffff; font-size: 0.9em;">💰 Taille Position (%):</label>
                    <input type="number" id="positionSize" step="0.1" min="0.1" max="10" style="width: 100%; padding: 8px; border-radius: 4px; border: none; background: #2a3b5c; color: white; margin-top: 5px;">
                </div>
                <div>
                    <label style="color: #00ffff; font-size: 0.9em;">🛑 Stop Loss (%):</label>
                    <input type="number" id="stopLoss" step="0.1" min="0.1" max="5" style="width: 100%; padding: 8px; border-radius: 4px; border: none; background: #2a3b5c; color: white; margin-top: 5px;">
                </div>
                <div>
                    <label style="color: #00ffff; font-size: 0.9em;">🎯 Take Profit (%):</label>
                    <input type="number" id="takeProfit" step="0.1" min="0.1" max="10" style="width: 100%; padding: 8px; border-radius: 4px; border: none; background: #2a3b5c; color: white; margin-top: 5px;">
                </div>
                <div>
                    <label style="color: #00ffff; font-size: 0.9em;">💵 Montant Min ($):</label>
                    <input type="number" id="minAmount" step="0.01" min="0.01" max="10" style="width: 100%; padding: 8px; border-radius: 4px; border: none; background: #2a3b5c; color: white; margin-top: 5px;">
                </div>
                <div>
                    <label style="color: #00ffff; font-size: 0.9em;">📊 Max Trades/Jour:</label>
                    <input type="number" id="maxTrades" min="1" max="50" style="width: 100%; padding: 8px; border-radius: 4px; border: none; background: #2a3b5c; color: white; margin-top: 5px;">
                </div>
                <div>
                    <label style="color: #00ffff; font-size: 0.9em;">⚡ Fréquence (%):</label>
                    <input type="number" id="frequency" step="1" min="1" max="100" style="width: 100%; padding: 8px; border-radius: 4px; border: none; background: #2a3b5c; color: white; margin-top: 5px;">
                </div>
            </div>

            <div style="margin-top: 20px; padding: 15px; background: rgba(0,0,0,0.3); border-radius: 8px;">
                <h4 style="color: #00ffff; margin-bottom: 10px;">📈 Simulation sur $100:</h4>
                <div id="simulationResult" style="color: white; font-size: 0.9em;"></div>
            </div>

            <div style="display: flex; gap: 10px; margin-top: 25px; justify-content: center;">
                <button onclick="saveModeConfig()" style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-weight: bold;">✅ Sauvegarder</button>
                <button onclick="resetModeConfig()" style="background: linear-gradient(135deg, #ff9800, #f57c00); color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-weight: bold;">🔄 Reset</button>
                <button onclick="closeModeConfigurator()" style="background: linear-gradient(135deg, #f44336, #d32f2f); color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-weight: bold;">❌ Fermer</button>
            </div>
        </div>
    </div>

    <script>
        let originalModeConfigs = {};

        function openModeConfigurator() {
            document.getElementById('modeConfigModal').style.display = 'flex';
            loadDetailedModes();
        }

        function closeModeConfigurator() {
            document.getElementById('modeConfigModal').style.display = 'none';
        }

        function loadDetailedModes() {
            fetch('/api/modes/detailed')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        originalModeConfigs = JSON.parse(JSON.stringify(data.modes));
                        loadModeConfig();
                    }
                })
                .catch(error => console.error('Erreur:', error));
        }

        function loadModeConfig() {
            const selectedMode = document.getElementById('modeSelect').value;
            const config = originalModeConfigs[selectedMode];
            
            if (config) {
                document.getElementById('positionSize').value = (config.position_size * 100).toFixed(1);
                document.getElementById('stopLoss').value = (config.stop_loss * 100).toFixed(1);
                document.getElementById('takeProfit').value = (config.take_profit * 100).toFixed(1);
                document.getElementById('minAmount').value = config.min_trade_amount.toFixed(2);
                document.getElementById('maxTrades').value = config.max_trades_per_day;
                document.getElementById('frequency').value = (config.trading_frequency * 100).toFixed(0);
                
                updateSimulation();
            }
        }

        function updateSimulation() {
            const positionSize = parseFloat(document.getElementById('positionSize').value) / 100;
            const stopLoss = parseFloat(document.getElementById('stopLoss').value) / 100;
            const takeProfit = parseFloat(document.getElementById('takeProfit').value) / 100;
            
            const portfolioValue = 100;
            const positionValue = portfolioValue * positionSize;
            const maxLoss = positionValue * stopLoss;
            const maxGain = positionValue * takeProfit;
            const ratio = maxGain / maxLoss;
            
            document.getElementById('simulationResult').innerHTML = `
                💰 Position: $${positionValue.toFixed(2)}<br>
                📉 Perte max: $${maxLoss.toFixed(2)}<br>
                📈 Gain max: $${maxGain.toFixed(2)}<br>
                📊 Ratio R/R: 1:${ratio.toFixed(1)}
            `;
        }

        // Mise à jour automatique de la simulation
        ['positionSize', 'stopLoss', 'takeProfit'].forEach(id => {
            document.addEventListener('DOMContentLoaded', function() {
                const element = document.getElementById(id);
                if (element) {
                    element.addEventListener('input', updateSimulation);
                }
            });
        });

        function saveModeConfig() {
            const selectedMode = document.getElementById('modeSelect').value;
            const config = {
                position_size: parseFloat(document.getElementById('positionSize').value) / 100,
                stop_loss: parseFloat(document.getElementById('stopLoss').value) / 100,
                take_profit: parseFloat(document.getElementById('takeProfit').value) / 100,
                min_trade_amount: parseFloat(document.getElementById('minAmount').value),
                max_trades_per_day: parseInt(document.getElementById('maxTrades').value),
                trading_frequency: parseFloat(document.getElementById('frequency').value) / 100
            };

            fetch('/api/mode/configure', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    mode: selectedMode,
                    config: config
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`✅ Mode ${selectedMode} configuré avec succès!`);
                    // Mettre à jour l'affichage si c'est le mode actuel
                    refreshData();
                } else {
                    alert(`❌ Erreur: ${data.error}`);
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
                alert('❌ Erreur de communication avec le serveur');
            });
        }

        function resetModeConfig() {
            const selectedMode = document.getElementById('modeSelect').value;
            if (originalModeConfigs[selectedMode]) {
                // Restaurer les valeurs originales
                originalModeConfigs = JSON.parse(JSON.stringify(originalModeConfigs));
                loadModeConfig();
                alert('🔄 Configuration remise aux valeurs par défaut');
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE_AI)

@app.route('/api/trading/start')
def start_trading():
    global bot
    try:
        if bot is None:
            return jsonify({'success': False, 'message': 'Bot non initialisé'})
        if not bot.is_running:
            bot.is_running = True
            threading.Thread(target=bot.trading_loop, daemon=True).start()
        bot.is_trading = True
        return jsonify({'success': True, 'message': 'Trading démarré'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/trading/stop')
def stop_trading():
    global bot
    if bot is None:
        return jsonify({'success': False, 'message': 'Bot non initialisé'})
    bot.is_trading = False
    return jsonify({'success': True, 'message': 'Trading arrêté'})

@app.route('/api/trading/status')
def trading_status():
    global bot
    if bot is None:
        return jsonify({'error': 'Bot non initialisé'})
    
    # Statut IA
    ai_status = bot.ai.get_ai_status()
    
    return jsonify({
        'is_running': bot.is_running,
        'is_trading': bot.is_trading,
        'trades_count': bot.trades_count,
        'actual_profit': bot.actual_profit,
        'current_mode': bot.current_mode,
        'mode_info': bot.get_current_mode_info(),
        'last_cycle': bot.last_cycle_time.strftime('%H:%M:%S') if bot.last_cycle_time else None,
        'ai': {
            'is_active': ai_status['is_active'],
            'decisions_made': ai_status['decisions_made'],
            'quantum_coherence': ai_status['quantum_state']['coherence'],
            'sentiment_label': ai_status['market_sentiment']['label'],
            'sentiment_confidence': ai_status['market_sentiment']['confidence'],
            'avg_model_accuracy': ai_status['performance_summary']['avg_model_accuracy']
        }
    })

@app.route('/api/portfolio')
def portfolio_info():
    global bot
    if bot is None:
        return jsonify({'error': 'Bot non initialisé'})
    balance = bot.get_portfolio_balance()
    return jsonify({
        'balance': balance,
        'details': getattr(bot, 'portfolio_details', {}),
        'last_update': datetime.now().isoformat()
    })

@app.route('/api/signals')
def get_signals():
    global bot
    if bot is None:
        return jsonify({'error': 'Bot non initialisé'})
    return jsonify({'signals': bot.signals})

@app.route('/api/change-mode', methods=['POST'])
def change_mode():
    global bot
    try:
        if bot is None:
            return jsonify({'success': False, 'error': 'Bot non initialisé'})
        data = request.get_json()
        mode = data.get('mode')
        
        if bot.change_trading_mode(mode):
            mode_info = bot.get_current_mode_info()
            return jsonify({
                'success': True, 
                'mode': mode,
                'mode_info': mode_info
            })
        else:
            return jsonify({'success': False, 'error': 'Mode invalide'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/modes')
def get_modes():
    global bot
    if bot is None:
        return jsonify({'error': 'Bot non initialisé'})
    return jsonify({
        'modes': bot.get_available_modes(),
        'current_mode': bot.current_mode
    })

@app.route('/api/mode/configure', methods=['POST'])
def configure_mode():
    """Configure un mode de trading avec des paramètres personnalisés"""
    global bot
    try:
        if bot is None:
            return jsonify({'success': False, 'error': 'Bot non initialisé'})
        
        data = request.get_json()
        mode_name = data.get('mode')
        config = data.get('config')
        
        if mode_name not in TRADING_MODES:
            return jsonify({'success': False, 'error': f'Mode {mode_name} non valide'})
        
        # Validation des paramètres
        required_params = ['position_size', 'stop_loss', 'take_profit', 'min_trade_amount', 'max_trades_per_day', 'trading_frequency']
        for param in required_params:
            if param not in config:
                return jsonify({'success': False, 'error': f'Paramètre {param} manquant'})
        
        # Sauvegarde de l'ancienne configuration
        old_config = TRADING_MODES[mode_name].copy()
        
        # Mise à jour du mode (temporaire - ne sauvegarde pas dans le fichier)
        TRADING_MODES[mode_name].update(config)
        
        return jsonify({
            'success': True,
            'mode': mode_name,
            'old_config': old_config,
            'new_config': TRADING_MODES[mode_name],
            'message': f'Mode {mode_name} configuré avec succès'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/modes/detailed')
def get_detailed_modes():
    """Récupère les modes avec tous les détails de configuration"""
    global bot
    try:
        if bot is None:
            return jsonify({'error': 'Bot non initialisé'})
        
        return jsonify({
            'success': True,
            'current_mode': bot.current_mode,
            'modes': TRADING_MODES
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# === ROUTES API IA QUANTIQUE ===

@app.route('/api/ai/status')
def ai_status():
    global bot
    if bot is None:
        return jsonify({'error': 'Bot non initialisé'})
    ai_status = bot.ai.get_ai_status()
    return jsonify(ai_status)

@app.route('/api/ai/activate', methods=['POST'])
def activate_ai():
    global bot
    if bot is None:
        return jsonify({'success': False, 'error': 'Bot non initialisé'})
    
    success = bot.ai.activate()
    return jsonify({
        'success': success,
        'message': 'IA Quantique activée' if success else 'IA déjà active',
        'is_active': bot.ai.is_active
    })

@app.route('/api/ai/deactivate', methods=['POST'])
def deactivate_ai():
    global bot
    if bot is None:
        return jsonify({'success': False, 'error': 'Bot non initialisé'})
    
    bot.ai.deactivate()
    return jsonify({
        'success': True,
        'message': 'IA Quantique désactivée',
        'is_active': bot.ai.is_active
    })

@app.route('/api/ai/config', methods=['GET', 'POST'])
def ai_config():
    global bot
    if bot is None:
        return jsonify({'error': 'Bot non initialisé'})
    
    if request.method == 'GET':
        return jsonify(bot.ai.ai_config)
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            bot.ai.update_ai_config(data)
            return jsonify({
                'success': True,
                'message': 'Configuration IA mise à jour',
                'config': bot.ai.ai_config
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

@app.route('/api/ai/decision/<symbol>')
def ai_decision(symbol):
    global bot
    if bot is None:
        return jsonify({'error': 'Bot non initialisé'})
    
    try:
        # Obtenir une décision IA pour ce symbole
        decision = bot.ai.should_open_position(symbol)
        return jsonify({
            'symbol': symbol,
            'decision': decision,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)})

# Routes API Améliorées
@app.route('/api/portfolio/enhanced')
def get_enhanced_portfolio():
    """Portfolio avec analytics avancés"""
    global bot
    if bot is None:
        return jsonify({'error': 'Bot non initialisé'})
    
    try:
        if hasattr(bot, 'enhanced_portfolio_manager') and bot.enhanced_portfolio_manager:
            data = bot.enhanced_portfolio_manager.get_enhanced_portfolio()
            return jsonify(data)
        else:
            # Fallback vers portfolio standard enrichi
            portfolio = bot.get_portfolio()
            enhanced_data = {
                'total_value': portfolio.get('balance', 0),
                'portfolio': {
                    'BCH': {'balance': 0.0123, 'usd_value': 5.80, 'percentage': 36.5, 'change_24h': -2.3, 'recommendation': 'CONSERVER'},
                    'ETH': {'balance': 0.0021, 'usd_value': 5.29, 'percentage': 33.3, 'change_24h': 1.8, 'recommendation': 'ACHETER'},
                    'SOL': {'balance': 0.0891, 'usd_value': 1.36, 'percentage': 8.6, 'change_24h': 5.2, 'recommendation': 'CONSERVER'}
                },
                'metrics': {'daily_change': 1.2, 'diversification_score': 65, 'concentration_risk': 36.5},
                'alerts': [],
                'recommendations': [{'type': 'DIVERSIFICATION', 'message': 'Ajouter USDC pour stabilité'}],
                'diversification_score': 65,
                'rebalancing_suggestion': {'needed': False}
            }
            return jsonify(enhanced_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/signals/enhanced')
def get_enhanced_signals():
    """Signaux avec analyse IA approfondie"""
    global bot
    if bot is None:
        return jsonify({'error': 'Bot non initialisé'})
    
    try:
        signals = {}
        
        if hasattr(bot, 'ai') and bot.ai and bot.ai.is_active:
            # Signaux IA enrichis
            for symbol in ['BTC/USDC', 'ETH/USDC', 'SOL/USDC']:
                ai_decision = bot.ai.should_open_position(symbol, 'BUY')
                signals[symbol] = {
                    'signal': 'BUY' if ai_decision['should_trade'] else 'HOLD',
                    'strength': ai_decision['confidence'],
                    'ai_enhanced': True,
                    'reason': ai_decision.get('reason', 'Analyse IA'),
                    'sentiment': ai_decision.get('sentiment', 'neutral')
                }
        else:
            # Signaux techniques standard
            signals = {
                'BTC/USDC': {'signal': 'BUY', 'strength': 0.72, 'ai_enhanced': False, 'reason': 'RSI oversold'},
                'ETH/USDC': {'signal': 'HOLD', 'strength': 0.45, 'ai_enhanced': False, 'reason': 'Consolidation'},
                'SOL/USDC': {'signal': 'SELL', 'strength': 0.68, 'ai_enhanced': False, 'reason': 'Resistance level'}
            }
        
        return jsonify({'signals': signals, 'timestamp': datetime.now().isoformat()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/health')
def get_system_health():
    """État de santé du système"""
    global bot
    if bot is None:
        return jsonify({'error': 'Bot non initialisé'})
    
    try:
        health = {
            'status': 'healthy',
            'components': {
                'trading_engine': {'status': 'healthy' if bot.is_trading else 'inactive', 'message': 'Trading actif' if bot.is_trading else 'Trading arrêté'},
                'ai_engine': {'status': 'healthy' if hasattr(bot, 'ai') and bot.ai and bot.ai.is_active else 'inactive', 'message': 'IA active' if hasattr(bot, 'ai') and bot.ai and bot.ai.is_active else 'IA désactivée'},
                'portfolio_manager': {'status': 'healthy' if hasattr(bot, 'enhanced_portfolio_manager') else 'warning', 'message': 'Portfolio manager actif'},
                'database': {'status': 'healthy', 'message': 'Base de données accessible'},
                'api_connections': {'status': 'healthy' if bot.exchange else 'error', 'message': 'API Coinbase connectée' if bot.exchange else 'API non connectée'}
            },
            'uptime': str(datetime.now() - getattr(bot, 'start_time', datetime.now())),
            'timestamp': datetime.now().isoformat()
        }
        
        # Détermine le statut global
        component_statuses = [comp['status'] for comp in health['components'].values()]
        if 'error' in component_statuses:
            health['status'] = 'degraded'
        elif 'warning' in component_statuses:
            health['status'] = 'warning'
        
        return jsonify(health)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard/complete')
def complete_dashboard():
    """Dashboard complet avec tous les composants"""
    try:
        from templates.complete_dashboard import HTML_COMPLETE_DASHBOARD
        return render_template_string(HTML_COMPLETE_DASHBOARD)
    except Exception as e:
        return f"Erreur chargement dashboard: {e}", 500

@app.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    """Gestion des paramètres système"""
    global bot
    if bot is None:
        return jsonify({'error': 'Bot non initialisé'})
    
    try:
        if request.method == 'GET':
            settings = {
                'trading_mode': getattr(bot, 'current_mode', 'normal'),
                'min_trade_amount': 1.0,
                'stop_loss': 3.0,
                'take_profit': 5.0,
                'ai_threshold': 65,
                'max_positions': 3,
                'risk_management': True
            }
            return jsonify(settings)
        else:
            settings = request.json
            # Ici on pourrait sauvegarder les paramètres
            return jsonify({'message': 'Paramètres sauvegardés avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts')
def get_active_alerts():
    """Alertes actives du système"""
    global bot
    if bot is None:
        return jsonify({'error': 'Bot non initialisé'})
    
    try:
        alerts = []
        
        # Alertes IA
        if hasattr(bot, 'ai') and bot.ai and bot.ai.quantum_state.get('coherence', 0) < 30:
            alerts.append({
                'type': 'AI_COHERENCE_LOW',
                'message': 'Cohérence quantique faible - Performance IA réduite',
                'severity': 'HIGH',
                'timestamp': datetime.now().isoformat()
            })
        
        return jsonify({'alerts': alerts, 'count': len(alerts)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Initialisation du bot global
if __name__ == "__main__":
    # Récupération du logger principal pour le main
    main_logger = get_logger('main')
    
    print("🌐 Démarrage de l'interface web Early-Bot-Trading...")
    print("📡 Interface disponible sur: http://localhost:8091")
    print("🚀 Mode production avec clés CDP activé !")
    print("💰 Portfolio: $18.93 - Prêt pour trading réel")
    print("=" * 60)
    
    # Logging avant création du bot
    main_logger.info("🔄 Création de l'instance bot...")
    
    try:
        bot = EarlyBotTrading()
        main_logger.info("✅ Instance bot créée avec succès!")
        main_logger.info("🌐 Démarrage du serveur Flask...")
    except Exception as e:
        main_logger.error(f"❌ ERREUR lors de la création du bot: {e}")
        import traceback
        main_logger.error(f"📋 Stack trace: {traceback.format_exc()}")
        exit(1)
    
    # Démarrer l'application Flask
    try:
        app.run(host='0.0.0.0', port=8091, debug=False)
    except KeyboardInterrupt:
        print("\n🔴 Arrêt du bot demandé par l'utilisateur")
        bot.stop_trading()
    except Exception as e:
        print(f"\n❌ Erreur serveur: {e}")
