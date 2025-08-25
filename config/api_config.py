#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration API Early-Bot-Trading - Clés fonctionnelles
Dernière mise à jour: 24/08/2025
"""

# Configuration API Coinbase
API_CONFIG = {
    'exchange': 'coinbase',
    'coinbase_api_key': '7bb7aaf0-8571-44ee-90cb-fa485597d0e8',
    'coinbase_api_secret': '''-----BEGIN EC PRIVATE KEY-----
MHcCAQEEID8hv4KFza4u5TdKTJZ756KlN0JUqwBPViMFynUyNkhRoAoGCCqGSM49
AwEHoUQDQgAEmGfueWxK4Ie/9T5o5HAgUqISxo5+ZgXHiE6/DRVk1F9mlDQT8kIh
/kwtdZERNu52cX1WX0Est83oxc2O4ThTTQ==
-----END EC PRIVATE KEY-----''',
    'coinbase_passphrase': '2c94fd0aa6a13b2f7444a369282a09f51281c9b705e120c61a1a3ed58702e5a7',
    'certification_id': 'TBPRO2025-1756037390',
    'certification_validity': '12 mois',
    'production_ready': True,
    'sandbox': False  # Mode production avec certification
}

# Modes de trading disponibles
TRADING_MODES = {
    'conservateur': {
        'name': '🛡️ Conservateur',
        'description': 'Trading sécurisé avec faible risque',
        'max_position_size': 0.005,   # 0.5% du portfolio par trade (ultra safe)
        'stop_loss': 0.02,           # 2% stop loss
        'take_profit': 0.04,         # 4% take profit
        'rsi_oversold': 20,
        'rsi_overbought': 80,
        'signal_threshold': 75,
        'min_trade_amount': 0.50,    # 50 centimes minimum !
        'trading_interval': 90,      # 1.5 minute entre analyses
        'risk_level': 'Ultra Faible'
    },
    'normal': {
        'name': '⚖️ Normal',
        'description': 'Trading équilibré risque/rendement',
        'max_position_size': 0.01,   # 1% du portfolio par trade
        'stop_loss': 0.03,           # 3% stop loss
        'take_profit': 0.06,         # 6% take profit
        'rsi_oversold': 25,
        'rsi_overbought': 75,
        'signal_threshold': 65,
        'min_trade_amount': 0.75,    # 75 centimes minimum
        'trading_interval': 60,      # 1 minute entre analyses
        'risk_level': 'Faible'
    },
    'agressif': {
        'name': '🚀 Agressif',
        'description': 'Trading haute fréquence pour petit portefeuille',
        'max_position_size': 0.02,   # 2% du portfolio par trade
        'stop_loss': 0.05,           # 5% stop loss
        'take_profit': 0.10,         # 10% take profit
        'rsi_oversold': 30,
        'rsi_overbought': 70,
        'signal_threshold': 55,
        'min_trade_amount': 1.00,    # 1€ minimum
        'trading_interval': 30,      # 30 secondes entre analyses
        'risk_level': 'Modéré'
    },
    'scalping': {
        'name': '⚡ Scalping',
        'description': 'Micro-trading ultra rapide',
        'max_position_size': 0.025,  # 2.5% du portfolio par trade
        'stop_loss': 0.03,           # 3% stop loss rapide
        'take_profit': 0.05,         # 5% take profit rapide
        'rsi_oversold': 35,
        'rsi_overbought': 65,
        'signal_threshold': 50,
        'min_trade_amount': 0.25,    # 25 centimes pour scalping !
        'trading_interval': 15,      # 15 secondes ultra rapide
        'risk_level': 'Rapide'
    }
}

# Configuration Trading par défaut (mode normal)
TRADING_CONFIG = {
    'current_mode': 'normal',
    'symbols': ['BTC/USDC', 'ETH/USDC', 'SOL/USDC'],  # Utilisation USDC pour compatibilité
    'rsi_period': 14,
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9,
    'bollinger_period': 20,
    'bollinger_std': 2,
    **TRADING_MODES['normal']  # Utilise les paramètres du mode normal par défaut
}

def get_current_mode_config():
    """Retourne la configuration du mode actuel"""
    current_mode = TRADING_CONFIG.get('current_mode', 'normal')
    return TRADING_MODES.get(current_mode, TRADING_MODES['normal'])

def switch_trading_mode(mode_name):
    """Change le mode de trading"""
    if mode_name in TRADING_MODES:
        TRADING_CONFIG['current_mode'] = mode_name
        # Met à jour les paramètres avec le nouveau mode
        TRADING_CONFIG.update(TRADING_MODES[mode_name])
        return True
    return False

print("✅ Configuration Early-Bot-Trading chargée avec modes de trading")
