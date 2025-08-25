"""
Early-Bot-Trading - Bot IA Trading Automatisé avec nouveau dashboard optimisé
Version clean avec template moderne intégré
"""

import os
import sys
import json
import time
import asyncio
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
import threading
from typing import Dict, List, Optional, Tuple
import sqlite3

# Logging system
from logging_system import (setup_logging, get_logger, log_portfolio_update, 
                           log_trading_activity, log_error, log_ai_analysis)

# AI Trading Engine
from ai.quantum_ai_engine import TradingAI

# Import du nouveau template optimisé
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
    ENHANCED_FEATURES = True
except ImportError:
    print("⚠️ Fonctionnalités avancées non disponibles")
    ENHANCED_FEATURES = False

class EarlyBotTrading:
    """Bot de trading automatisé avec IA quantique et dashboard moderne"""
    
    def __init__(self):
        # Logging setup
        self.logger, self.trading_logger, self.api_logger, self.log_file = setup_logging()
        self.logger.info("🤖 Initialisation d'Early-Bot-Trading avec nouveau dashboard...")
        
        # Trading AI
        self.ai = TradingAI(self)
        
        # Configuration
        self.config = TRADING_CONFIG
        self.trading_modes = TRADING_MODES
        
        # État du bot
        self.is_trading = False
        self.current_mode = "normal"
        self.last_update = datetime.now()
        
        # Portfolio
        self.portfolio_balance = 0.0
        self.positions = []
        self.daily_pnl = 0.0
        
        # Enhanced Portfolio Manager
        if ENHANCED_FEATURES:
            try:
                self.portfolio_manager = EnhancedPortfolioManager()
                self.logger.info("✅ Enhanced Portfolio Manager activé")
            except Exception as e:
                self.logger.warning(f"⚠️ Enhanced Portfolio Manager non disponible: {e}")
                self.portfolio_manager = None
        else:
            self.portfolio_manager = None
        
        # Stats
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_profit = 0.0
        
        # Signaux IA
        self.signals = []
        
        self.logger.info("✅ Bot initialisé avec succès !")
    
    def start_trading(self) -> bool:
        """Démarre le trading automatisé"""
        try:
            if self.is_trading:
                return False
                
            self.is_trading = True
            self.logger.info("🚀 Trading démarré !")
            
            # Démarrer le thread de trading
            trading_thread = threading.Thread(target=self._trading_loop, daemon=True)
            trading_thread.start()
            
            return True
        except Exception as e:
            self.logger.error(f"❌ Erreur démarrage trading: {e}")
            return False
    
    def stop_trading(self) -> bool:
        """Arrête le trading automatisé"""
        try:
            self.is_trading = False
            self.logger.info("🛑 Trading arrêté")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erreur arrêt trading: {e}")
            return False
    
    def _trading_loop(self):
        """Boucle principale de trading"""
        while self.is_trading:
            try:
                # Analyser le marché avec l'IA
                analysis = self.ai.analyze_market()
                
                # Prendre des décisions de trading
                if analysis and analysis.get('signal'):
                    self._process_trading_signal(analysis)
                
                # Attendre avant la prochaine analyse
                time.sleep(self.config.get('analysis_interval', 60))
                
            except Exception as e:
                self.logger.error(f"❌ Erreur dans la boucle de trading: {e}")
                time.sleep(30)
    
    def _process_trading_signal(self, signal):
        """Traite un signal de trading"""
        try:
            # Logique de traitement des signaux
            self.logger.info(f"📊 Signal reçu: {signal}")
            
            # Ajouter le signal à la liste
            self.signals.append({
                'symbol': signal.get('symbol', 'BTC-USD'),
                'action': signal.get('action', 'HOLD'),
                'confidence': signal.get('confidence', 0.5),
                'timestamp': datetime.now().isoformat()
            })
            
            # Garder seulement les 10 derniers signaux
            self.signals = self.signals[-10:]
            
        except Exception as e:
            self.logger.error(f"❌ Erreur traitement signal: {e}")
    
    def change_trading_mode(self, mode: str) -> bool:
        """Change le mode de trading"""
        try:
            if mode in self.trading_modes:
                self.current_mode = mode
                self.config.update(self.trading_modes[mode])
                self.logger.info(f"⚙️ Mode changé vers: {mode}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Erreur changement mode: {e}")
            return False
    
    def get_portfolio_status(self) -> Dict:
        """Récupère le statut du portfolio"""
        try:
            if self.portfolio_manager:
                return self.portfolio_manager.get_comprehensive_analytics()
            else:
                return {
                    'balance': self.portfolio_balance,
                    'daily_pnl': self.daily_pnl,
                    'positions': len(self.positions),
                    'win_rate': self._calculate_win_rate()
                }
        except Exception as e:
            self.logger.error(f"❌ Erreur récupération portfolio: {e}")
            return {'balance': 0, 'daily_pnl': 0, 'positions': 0, 'win_rate': 0}
    
    def _calculate_win_rate(self) -> float:
        """Calcule le taux de réussite"""
        if self.total_trades == 0:
            return 0.0
        return (self.winning_trades / self.total_trades) * 100
    
    def get_ai_status(self) -> Dict:
        """Récupère le statut de l'IA"""
        try:
            return {
                'coherence': getattr(self.ai, 'quantum_coherence', 85),
                'precision': self._calculate_win_rate(),
                'active_signals': len(self.signals),
                'ml_models': 5
            }
        except Exception as e:
            self.logger.error(f"❌ Erreur récupération statut IA: {e}")
            return {'coherence': 0, 'precision': 0, 'active_signals': 0, 'ml_models': 0}

# Flask Application
app = Flask(__name__)
CORS(app)

# Variable globale pour l'instance du bot
bot = None

# Routes principales
@app.route('/')
def dashboard():
    """Page principale avec nouveau dashboard"""
    return render_template_string(NEW_DASHBOARD_TEMPLATE)

@app.route('/api/bot/start', methods=['POST'])
def api_start_trading():
    """API pour démarrer le trading"""
    global bot
    try:
        if bot is None:
            return jsonify({'success': False, 'error': 'Bot non initialisé'})
        
        success = bot.start_trading()
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/bot/stop', methods=['POST'])
def api_stop_trading():
    """API pour arrêter le trading"""
    global bot
    try:
        if bot is None:
            return jsonify({'success': False, 'error': 'Bot non initialisé'})
        
        success = bot.stop_trading()
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/bot/status')
def api_bot_status():
    """API pour récupérer le statut du bot"""
    global bot
    try:
        if bot is None:
            return jsonify({'error': 'Bot non initialisé'})
        
        return jsonify({
            'is_trading': bot.is_trading,
            'current_mode': bot.current_mode,
            'last_update': bot.last_update.isoformat(),
            'total_trades': bot.total_trades
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/portfolio/enhanced')
def api_portfolio_enhanced():
    """API pour récupérer le portfolio avec analytics"""
    global bot
    try:
        if bot is None:
            return jsonify({'error': 'Bot non initialisé'})
        
        portfolio = bot.get_portfolio_status()
        return jsonify(portfolio)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/positions')
def api_positions():
    """API pour récupérer les positions actives"""
    global bot
    try:
        if bot is None:
            return jsonify({'error': 'Bot non initialisé'})
        
        return jsonify(bot.positions)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/mode/set/<mode>', methods=['POST'])
def api_set_mode(mode):
    """API pour changer le mode de trading"""
    global bot
    try:
        if bot is None:
            return jsonify({'success': False, 'error': 'Bot non initialisé'})
        
        success = bot.change_trading_mode(mode)
        return jsonify({'success': success, 'current_mode': bot.current_mode})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/modes/detailed')
def api_modes_detailed():
    """API pour récupérer les modes avec détails"""
    global bot
    try:
        if bot is None:
            return jsonify({'error': 'Bot non initialisé'})
        
        return jsonify({
            'success': True,
            'current_mode': bot.current_mode,
            'modes': bot.trading_modes
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/mode/configure', methods=['POST'])
def api_configure_mode():
    """API pour configurer un mode de trading"""
    global bot
    try:
        if bot is None:
            return jsonify({'success': False, 'error': 'Bot non initialisé'})
        
        data = request.get_json()
        mode_name = data.get('mode')
        config = data.get('config')
        
        if mode_name not in bot.trading_modes:
            return jsonify({'success': False, 'error': f'Mode {mode_name} non valide'})
        
        # Validation des paramètres
        required_params = ['position_size', 'stop_loss', 'take_profit', 'min_trade_amount', 'max_trades_per_day', 'trading_frequency']
        for param in required_params:
            if param not in config:
                return jsonify({'success': False, 'error': f'Paramètre {param} manquant'})
        
        # Mise à jour du mode
        bot.trading_modes[mode_name].update(config)
        
        return jsonify({
            'success': True,
            'mode': mode_name,
            'new_config': bot.trading_modes[mode_name],
            'message': f'Mode {mode_name} configuré avec succès'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/ai/status')
def api_ai_status():
    """API pour récupérer le statut de l'IA"""
    global bot
    try:
        if bot is None:
            return jsonify({'error': 'Bot non initialisé'})
        
        ai_status = bot.get_ai_status()
        return jsonify(ai_status)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/signals')
def api_signals():
    """API pour récupérer les signaux IA"""
    global bot
    try:
        if bot is None:
            return jsonify({'error': 'Bot non initialisé'})
        
        return jsonify({'signals': bot.signals})
    except Exception as e:
        return jsonify({'error': str(e)})

# Initialisation et démarrage
if __name__ == "__main__":
    # Récupération du logger principal pour le main
    main_logger = get_logger('main')
    
    print("🌐 Démarrage du nouveau Bot Trading Quantique IA...")
    print("📡 Interface moderne disponible sur: http://localhost:8091")
    print("🚀 Dashboard optimisé avec template moderne activé !")
    print("💰 Portfolio: $18.93 - Prêt pour trading réel")
    print("=" * 60)
    
    # Logging avant création du bot
    main_logger.info("🔄 Création de l'instance bot avec nouveau dashboard...")
    
    try:
        bot = EarlyBotTrading()
        main_logger.info("✅ Instance bot créée avec succès!")
        main_logger.info("🌐 Démarrage du serveur Flask avec nouveau template...")
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
        if bot:
            bot.stop_trading()
    except Exception as e:
        print(f"\n❌ Erreur serveur: {e}")
