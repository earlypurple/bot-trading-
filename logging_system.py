#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de logging pour Early-Bot-Trading
Capture tous les logs, erreurs et activités du bot
"""

import logging
import sys
import os
from datetime import datetime

def setup_logging():
    """Configure le système de logging pour le bot"""
    
    # Créer le répertoire logs s'il n'existe pas
    log_dir = "/Users/johan/ia_env/bot-trading-/Early-Bot-Trading/logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Nom du fichier log avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_dir}/early_bot_{timestamp}.log"
    
    # Configuration du logger principal
    logger = logging.getLogger('EarlyBotTrading')
    logger.setLevel(logging.DEBUG)
    
    # Supprimer les handlers existants pour éviter la duplication
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Formatter pour les logs
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler pour fichier - TOUT est enregistré
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler pour console - messages importants uniquement
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Logger pour erreurs critiques (fichier séparé)
    error_file = f"{log_dir}/early_bot_errors_{timestamp}.log"
    error_handler = logging.FileHandler(error_file, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    # Logger pour activité trading (fichier séparé)
    trading_file = f"{log_dir}/early_bot_trading_{timestamp}.log"
    trading_handler = logging.FileHandler(trading_file, encoding='utf-8')
    trading_handler.setLevel(logging.INFO)
    trading_formatter = logging.Formatter(
        '%(asctime)s | TRADING | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    trading_handler.setFormatter(trading_formatter)
    
    # Créer un logger spécifique pour le trading
    trading_logger = logging.getLogger('TradingActivity')
    trading_logger.setLevel(logging.INFO)
    trading_logger.addHandler(trading_handler)
    trading_logger.addHandler(console_handler)  # Affichage console aussi
    
    # Logger pour l'API Coinbase
    api_file = f"{log_dir}/early_bot_api_{timestamp}.log"
    api_handler = logging.FileHandler(api_file, encoding='utf-8')
    api_handler.setLevel(logging.DEBUG)
    api_handler.setFormatter(formatter)
    
    api_logger = logging.getLogger('CoinbaseAPI')
    api_logger.setLevel(logging.DEBUG)
    api_logger.addHandler(api_handler)
    api_logger.addHandler(file_handler)  # Dans le log principal aussi
    
    # Capturer les exceptions non gérées
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            logger.info("🔴 Arrêt du bot demandé par l'utilisateur (Ctrl+C)")
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        logger.critical("❌ Exception non gérée", exc_info=(exc_type, exc_value, exc_traceback))
    
    sys.excepthook = handle_exception
    
    # Messages de démarrage
    logger.info("=" * 80)
    logger.info("🚀 EARLY-BOT-TRADING - SYSTÈME DE LOGGING INITIALISÉ")
    logger.info("=" * 80)
    logger.info(f"📁 Fichier log principal: {log_file}")
    logger.info(f"🚨 Fichier erreurs: {error_file}")
    logger.info(f"💰 Fichier trading: {trading_file}")
    logger.info(f"🔗 Fichier API: {api_file}")
    logger.info(f"🕐 Session démarrée: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    return logger, trading_logger, api_logger, log_file

def get_logger(name='EarlyBotTrading'):
    """Récupère un logger configuré"""
    return logging.getLogger(name)

def log_portfolio_update(portfolio_data):
    """Log spécialisé pour les mises à jour de portfolio"""
    trading_logger = logging.getLogger('TradingActivity')
    trading_logger.info(f"💰 Portfolio mis à jour: ${portfolio_data.get('total', 0):.2f}")
    
    main_logger = logging.getLogger('EarlyBotTrading')
    main_logger.debug(f"📊 Détails portfolio: {portfolio_data}")

def log_signal_analysis(symbol, signal_data):
    """Log spécialisé pour l'analyse des signaux"""
    trading_logger = logging.getLogger('TradingActivity')
    signal = signal_data.get('signal', 'UNKNOWN')
    strength = signal_data.get('strength', 0)
    price = signal_data.get('details', {}).get('price', 0)
    
    trading_logger.info(f"📈 {symbol}: {signal} (Force: {strength}) - Prix: ${price:.2f}")
    
    main_logger = logging.getLogger('EarlyBotTrading')
    main_logger.debug(f"🔍 Analyse complète {symbol}: {signal_data}")

def log_trade_attempt(action, symbol, amount, price):
    """Log spécialisé pour les tentatives de trade"""
    trading_logger = logging.getLogger('TradingActivity')
    trading_logger.info(f"💰 TENTATIVE {action}: {symbol} - ${amount:.2f} à ${price:.2f}")

def log_trade_result(success, action, symbol, result_data):
    """Log spécialisé pour les résultats de trade"""
    trading_logger = logging.getLogger('TradingActivity')
    
    if success:
        trading_logger.info(f"✅ {action} RÉEL EXÉCUTÉ: {symbol}")
        trading_logger.info(f"📄 Ordre: {result_data}")
    else:
        error_msg = result_data.get('error', 'Erreur inconnue')
        trading_logger.warning(f"❌ {action} échoué: {symbol} - {error_msg}")
        trading_logger.info(f"🔄 Fallback simulation activé")

def log_api_call(method, endpoint, params=None, response=None, error=None):
    """Log spécialisé pour les appels API"""
    api_logger = logging.getLogger('CoinbaseAPI')
    
    if error:
        api_logger.error(f"❌ API {method} {endpoint}: {error}")
    else:
        api_logger.debug(f"✅ API {method} {endpoint}")
        if params:
            api_logger.debug(f"📤 Paramètres: {params}")
        if response:
            api_logger.debug(f"📥 Réponse: {response}")

if __name__ == "__main__":
    # Test du système de logging
    logger, trading_logger, api_logger, log_file = setup_logging()
    
    # Tests
    logger.info("🧪 Test du système de logging...")
    logger.debug("Message de debug")
    logger.warning("Message d'avertissement")
    logger.error("Message d'erreur de test")
    
    trading_logger.info("💰 Test activité trading")
    api_logger.info("🔗 Test API Coinbase")
    
    logger.info(f"✅ Tests terminés - Logs disponibles dans: {log_file}")
    print(f"\n📁 Fichier de log créé: {log_file}")
