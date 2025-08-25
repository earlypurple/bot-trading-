#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration API Early-Bot-Trading - Nouvelles clés CDP
Mise à jour: 25/08/2025 - Clés Coinbase Developer Platform
"""

# Configuration API Coinbase Developer Platform (CDP)
API_CONFIG = {
    'exchange': 'coinbase',
    # Nouvelles clés CDP - Compatible avec Advanced Trade v3
    'coinbase_api_key': '0b93dbfe-32e3-4a71-a983-41eb404c1139',  # Extrait du nom de l'API key
    'coinbase_api_secret': '''-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIL48eCgA+ocyaRny5AcpFoTlvWt1V8XC4ZTnC34WHyNfoAoGCCqGSM49
AwEHoUQDQgAEgeFclllAbAZ6iTmo4+snYZcBM+SN75MH8g76aHcSzwKxNSebW3Tv
EBvd42Q73R51QP1ji3cm+ReSErZEG610ag==
-----END EC PRIVATE KEY-----''',
    'coinbase_passphrase': '',  # Pas de passphrase pour les clés CDP
    'organization_id': 'e3660eee-4c95-4642-80a9-9b611f5e50eb',  # Extrait du nom
    'api_key_name': 'organizations/e3660eee-4c95-4642-80a9-9b611f5e50eb/apiKeys/0b93dbfe-32e3-4a71-a983-41eb404c1139',
    'certification_id': 'TBPRO2025-1756037390',
    'certification_validity': '12 mois',
    'production_ready': True,
    'sandbox': False  # Mode production avec nouvelles clés CDP
}

# Modes de trading disponibles - MICRO-TRADING OPTIMISÉ
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
        'min_trade_amount': 0.10,    # 10 centimes minimum ! Ultra micro
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
        'min_trade_amount': 0.15,    # 15 centimes minimum
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
        'min_trade_amount': 0.20,    # 20 centimes minimum
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
        'min_trade_amount': 0.05,    # 5 centimes pour scalping ! ULTRA MICRO
        'trading_interval': 15,      # 15 secondes ultra rapide
        'risk_level': 'Rapide'
    }
}

# Configuration Trading par défaut (mode normal)
TRADING_CONFIG = {
    'current_mode': 'normal',
    'symbols': ['BTC/USDC', 'ETH/USDC', 'SOL/USDC', 'BTC/PYUSD', 'ETH/PYUSD'],  # Ajout paires PYUSD
    'rsi_period': 14,
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9,
    'bollinger_period': 20,
    'bollinger_std': 2,
    
    # Configuration de consolidation automatique
    'auto_consolidate': True,        # Active la consolidation auto
    'consolidate_threshold': 2.0,    # Consolide positions < $2
    'consolidate_to': 'USDC',        # Crypto de destination
    'min_balance_keep': 0.10,        # Garde minimum 10 centimes par crypto
    
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

def should_consolidate_position(balance_usd, symbol):
    """Vérifie si une position doit être consolidée"""
    if not TRADING_CONFIG.get('auto_consolidate', False):
        return False
    
    threshold = TRADING_CONFIG.get('consolidate_threshold', 2.0)
    target_crypto = TRADING_CONFIG.get('consolidate_to', 'USDC')
    
    # Ne pas consolider la crypto cible ni USDC
    if symbol.replace('/USDC', '') == target_crypto or 'USDC' in symbol:
        return False
    
    # Consolide si balance < threshold
    return balance_usd < threshold and balance_usd > 0.01

def get_consolidation_config():
    """Retourne la configuration de consolidation"""
    return {
        'enabled': TRADING_CONFIG.get('auto_consolidate', False),
        'threshold': TRADING_CONFIG.get('consolidate_threshold', 2.0),
        'target': TRADING_CONFIG.get('consolidate_to', 'USDC'),
        'min_keep': TRADING_CONFIG.get('min_balance_keep', 0.10)
    }

print("✅ Configuration Early-Bot-Trading chargée avec nouvelles clés CDP")
print("🔐 Clés Coinbase Developer Platform configurées")
print("🚀 Compatible Advanced Trade API v3")
