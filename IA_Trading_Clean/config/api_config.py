#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration API Coinbase - Clés fonctionnelles
Dernière mise à jour: 24/08/2025
"""

import os
from dotenv import load_dotenv

# Construire le chemin vers le fichier .env qui se trouve à la racine de IA_Trading_Clean
# __file__ -> IA_Trading_Clean/config/api_config.py
# os.path.dirname(__file__) -> IA_Trading_Clean/config
# os.path.dirname(os.path.dirname(__file__)) -> IA_Trading_Clean
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'coinbase_credentials.env')

# Vérifier si le fichier existe avant de charger
if not os.path.exists(dotenv_path):
    raise FileNotFoundError(f"Fichier de configuration '{dotenv_path}' introuvable. Assurez-vous qu'il existe.")

load_dotenv(dotenv_path=dotenv_path)

# Configuration API Coinbase
API_CONFIG = {
    'exchange': 'coinbase',
    'coinbase_api_key': os.getenv('COINBASE_API_KEY'),
    'coinbase_private_key': os.getenv('COINBASE_PRIVATE_KEY'),
    'sandbox': False  # Mettre True pour le mode test
}

# Vérification que les clés sont bien chargées depuis le .env
if not all([API_CONFIG['coinbase_api_key'], API_CONFIG['coinbase_private_key']]):
    raise ValueError("Clés API non chargées. Vérifiez votre fichier 'coinbase_credentials.env'.")

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
