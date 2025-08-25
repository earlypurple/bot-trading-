#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot Trading API Simple - Gestion des modes et ordres
Version simplifiée pour fonctionner avec le dashboard séparé
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time
import json
from datetime import datetime

# Configuration des modes de trading
TRADING_MODES = {
    'normal': {
        'name': 'Normal',
        'risk_level': 3,
        'trade_frequency': 'medium',
        'max_position_size': 0.1,
        'stop_loss': 0.02,
        'take_profit': 0.05
    },
    'aggressive': {
        'name': 'Agressif',
        'risk_level': 5,
        'trade_frequency': 'high',
        'max_position_size': 0.2,
        'stop_loss': 0.05,
        'take_profit': 0.15
    },
    'conservative': {
        'name': 'Conservateur',
        'risk_level': 1,
        'trade_frequency': 'low',
        'max_position_size': 0.05,
        'stop_loss': 0.01,
        'take_profit': 0.03
    },
    'scalping': {
        'name': 'Scalping',
        'risk_level': 4,
        'trade_frequency': 'very_high',
        'max_position_size': 0.3,
        'stop_loss': 0.005,
        'take_profit': 0.01
    }
}

class SimpleTradingBot:
    def __init__(self):
        self.is_running = False
        self.current_mode = 'normal'
        self.balance = 11.87  # Portfolio réel
        self.daily_pnl = 0.0
        self.trades_count = 0
        self.last_trade_time = None
        
    def start(self):
        """Démarre le bot de trading"""
        if not self.is_running:
            self.is_running = True
            print("✅ Bot de trading démarré")
            # Démarrer la boucle de trading en arrière-plan
            threading.Thread(target=self.trading_loop, daemon=True).start()
            return True
        return False
    
    def stop(self):
        """Arrête le bot de trading"""
        if self.is_running:
            self.is_running = False
            print("🛑 Bot de trading arrêté")
            return True
        return False
    
    def change_mode(self, new_mode):
        """Change le mode de trading"""
        if new_mode in TRADING_MODES:
            old_mode = self.current_mode
            self.current_mode = new_mode
            print(f"🔄 Mode changé: {old_mode} → {new_mode}")
            return True
        return False
    
    def trading_loop(self):
        """Boucle principale de trading"""
        while self.is_running:
            try:
                # Simuler l'activité de trading
                print(f"🤖 Trading en mode {self.current_mode}...")
                
                # Simuler un petit P&L
                if self.trades_count % 10 == 0:
                    self.daily_pnl += 0.05
                
                self.trades_count += 1
                self.last_trade_time = datetime.now()
                
                # Attendre selon la fréquence du mode
                mode_config = TRADING_MODES[self.current_mode]
                if mode_config['trade_frequency'] == 'very_high':
                    time.sleep(5)
                elif mode_config['trade_frequency'] == 'high':
                    time.sleep(10)
                elif mode_config['trade_frequency'] == 'medium':
                    time.sleep(20)
                else:  # low
                    time.sleep(30)
                    
            except Exception as e:
                print(f"❌ Erreur dans la boucle de trading: {e}")
                time.sleep(10)
    
    def get_status(self):
        """Retourne le statut actuel du bot"""
        return {
            'is_running': self.is_running,
            'current_mode': self.current_mode,
            'balance': self.balance,
            'daily_pnl': self.daily_pnl,
            'trades_count': self.trades_count,
            'last_trade_time': self.last_trade_time.isoformat() if self.last_trade_time else None
        }

# Créer l'application Flask
app = Flask(__name__)
CORS(app, origins="*")

# Instance du bot
bot = SimpleTradingBot()

# Routes API
@app.route('/api/status', methods=['GET'])
def get_status():
    """Retourne le statut du bot"""
    try:
        status = bot.get_status()
        return jsonify({
            'success': True,
            'data': status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/start', methods=['POST'])
def start_bot():
    """Démarre le bot"""
    try:
        success = bot.start()
        return jsonify({
            'success': success,
            'message': 'Bot démarré' if success else 'Bot déjà en cours'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    """Arrête le bot"""
    try:
        success = bot.stop()
        return jsonify({
            'success': success,
            'message': 'Bot arrêté' if success else 'Bot déjà arrêté'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/mode/<mode_name>', methods=['POST'])
def change_mode(mode_name):
    """Change le mode de trading"""
    try:
        success = bot.change_mode(mode_name)
        if success:
            return jsonify({
                'success': True,
                'message': f'Mode changé vers {mode_name}',
                'current_mode': bot.current_mode
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Mode {mode_name} invalide'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/modes', methods=['GET'])
def get_modes():
    """Retourne la liste des modes disponibles"""
    return jsonify({
        'success': True,
        'modes': TRADING_MODES
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Vérification de santé"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'bot_running': bot.is_running
    })

if __name__ == '__main__':
    print("🤖 DÉMARRAGE BOT TRADING API")
    print("=" * 40)
    print("🔧 Bot simplifié pour changements de mode")
    print("🌐 API disponible sur http://localhost:8091")
    print("🔄 Compatible avec dashboard sur port 8080")
    print("\n📋 ENDPOINTS DISPONIBLES:")
    print("  GET  /api/status       - Statut du bot")
    print("  POST /api/start        - Démarrer le bot")
    print("  POST /api/stop         - Arrêter le bot")
    print("  POST /api/mode/<mode>  - Changer de mode")
    print("  GET  /api/modes        - Liste des modes")
    print("  GET  /health           - Vérification santé")
    print("\n🎯 MODES DISPONIBLES:")
    for mode_key, mode_info in TRADING_MODES.items():
        print(f"  • {mode_key}: {mode_info['name']}")
    
    print(f"\n✅ Démarrage sur le port 8091...")
    
    try:
        app.run(
            host='0.0.0.0',
            port=8091,
            debug=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du bot")
    except Exception as e:
        print(f"❌ Erreur: {e}")
