#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration API Coinbase - Clés fonctionnelles
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
    'coinbase_passphrase': 'ma_passphrase_securisee',
    'sandbox': False  # Mettre True pour le mode test
}

# Configuration Trading
TRADING_CONFIG = {
    'symbols': ['BTC/USD', 'ETH/USD', 'SOL/USD'],
    'max_position_size': 0.02,  # 2% du portfolio par trade
    'stop_loss': 0.03,          # 3% stop loss
    'take_profit': 0.05,        # 5% take profit
    'rsi_period': 14,
    'rsi_oversold': 30,
    'rsi_overbought': 70,
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9,
    'bollinger_period': 20,
    'bollinger_std': 2,
    'trading_interval': 30,     # Secondes entre analyses
    'min_trade_amount': 5.0     # Montant minimum par trade en USD
}

print("✅ Configuration API chargée avec nouvelles clés")
