#!/bin/bash

# Script de correction des problèmes de connexion
echo "🔍 Diagnostic des problèmes du dashboard et du bot..."

# Chemin absolu du répertoire du projet
PROJET_DIR="/Users/johan/ia_env/bot-trading-/TradingBot_Pro_2025"
ENV_PATH="/Users/johan/ia_env/bin/activate"

# Vérifier si l'environnement virtuel existe
if [ ! -f "$ENV_PATH" ]; then
    echo "❌ Environnement virtuel non trouvé: $ENV_PATH"
    exit 1
fi

echo "✅ Environnement virtuel trouvé"

# Activer l'environnement virtuel
source "$ENV_PATH"

# Installer les dépendances manquantes
echo "📦 Installation des dépendances supplémentaires..."
pip install ccxt flask-cors flask-limiter yfinance ta

# Se déplacer dans le dossier du projet
cd "$PROJET_DIR"

# Créer le fichier de configuration des clés API si nécessaire
if [ ! -f "$PROJET_DIR/api_keys.py" ]; then
    echo "🔑 Création d'un fichier de configuration API..."
    cat > "$PROJET_DIR/api_keys.py" << EOL
# Configuration des clés API pour le trading bot
# Remplacer avec vos clés réelles pour une utilisation en production

API_KEYS = {
    'binance': {
        'api_key': 'votre_api_key_binance',
        'api_secret': 'votre_api_secret_binance',
        'sandbox': True  # Mode test
    },
    'coinbase': {
        'api_key': 'votre_api_key_coinbase',
        'api_secret': 'votre_api_secret_coinbase',
        'sandbox': True  # Mode test
    },
    'kraken': {
        'api_key': 'votre_api_key_kraken',
        'api_secret': 'votre_api_secret_kraken',
        'sandbox': True  # Mode test
    }
}

DEFAULT_EXCHANGE = 'binance'  # Utilise Binance par défaut
EOL
    echo "✅ Fichier api_keys.py créé avec des clés de test"
fi

# Modifier le fichier de config.py pour s'assurer que le mode test est activé
if [ -f "$PROJET_DIR/src/config.py" ]; then
    echo "⚙️ Vérification du fichier de configuration..."
    grep -q "TEST_MODE = True" "$PROJET_DIR/src/config.py" || {
        cat > "$PROJET_DIR/src/config.py" << EOL
# Configuration du Trading Bot
import os

# Mode test (pas de transactions réelles)
TEST_MODE = True

# Configuration des API
API_TIMEOUT = 30  # secondes
MAX_RETRIES = 3

# Limites de trading
MAX_TRADES_PER_DAY = 10
MAX_PORTFOLIO_RISK = 0.02  # 2%
MAX_INVESTMENT = 100  # $100

# Paramètres des stratégies
DEFAULT_STRATEGY = 'momentum_multi_asset'
AVAILABLE_STRATEGIES = [
    'momentum_multi_asset',
    'grid_adaptive_ia',
    'scalping_quantique',
    'cross_chain_arbitrage',
    'defi_yield_farming'
]

# Configuration IA
PREDICTION_INTERVAL = '1h'
MIN_CONFIDENCE = 0.65

def get_config():
    """Retourne la configuration"""
    return {
        'test_mode': TEST_MODE,
        'api_timeout': API_TIMEOUT,
        'max_retries': MAX_RETRIES,
        'max_trades_per_day': MAX_TRADES_PER_DAY,
        'max_portfolio_risk': MAX_PORTFOLIO_RISK,
        'max_investment': MAX_INVESTMENT,
        'default_strategy': DEFAULT_STRATEGY,
        'available_strategies': AVAILABLE_STRATEGIES,
        'prediction_interval': PREDICTION_INTERVAL,
        'min_confidence': MIN_CONFIDENCE
    }
EOL
        echo "✅ Fichier config.py mis à jour avec le mode test activé"
    }
fi

# Tuer tous les processus Python en cours
echo "🧹 Nettoyage des processus Python en cours..."
pkill -f "python.*dashboard" || true
sleep 2

# Vérification des ports utilisés
echo "🔍 Vérification des ports..."
lsof -ti:8088 | xargs kill -9 2>/dev/null || true
lsof -ti:8081 | xargs kill -9 2>/dev/null || true

echo "✅ Nettoyage terminé. Le dashboard est prêt à être lancé."
echo "🚀 Pour lancer le dashboard, exécutez: ./lancer_dashboard.sh"
