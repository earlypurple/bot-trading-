#!/bin/bash

# SUPER SIMPLE - Lance tout en un clic (dashboard, bot, réglages)
# Créé le 24 août 2025 par GitHub Copilot
# COPIER CE FICHIER SUR VOTRE BUREAU POUR UN ACCÈS RAPIDE

# Chemin du projet
PROJET_DIR="/Users/johan/ia_env/bot-trading-"
TRADING_BOT_DIR="$PROJET_DIR/TradingBot_Pro_2025"
ENV_PATH="/Users/johan/ia_env/bin/activate"

# Afficher un message de bienvenue
clear
echo ""
echo "🚀 DÉMARRAGE DU BOT TRADING COINBASE PRO 2025 🚀"
echo "================================================"
echo ""
echo "⏳ Préparation de l'environnement..."

# Nettoyer les processus existants
pkill -f "python.*dashboard_trading_pro.py" >/dev/null 2>&1 || true
sleep 1
lsof -ti:8088 | xargs kill -9 >/dev/null 2>&1 || true
lsof -ti:8081 | xargs kill -9 >/dev/null 2>&1 || true
sleep 1

# Aller dans le répertoire du projet
cd "$PROJET_DIR" || {
  osascript -e 'display dialog "Erreur: Impossible de trouver le dossier du projet. Vérifiez le chemin dans le script." buttons {"OK"} default button "OK" with icon stop'
  exit 1
}

# Activer l'environnement
source "$ENV_PATH" || {
  osascript -e 'display dialog "Erreur: Impossible d'activer l'environnement Python. Vérifiez que Python est bien installé." buttons {"OK"} default button "OK" with icon stop'
  exit 1
}

# Afficher une notification
osascript -e 'display notification "Démarrage du Bot Trading Coinbase Pro" with title "Trading Bot" subtitle "Préparation en cours..." sound name "Submarine"'

echo "✅ Environnement prêt"
echo "✅ Chargement du portfolio Coinbase"
echo ""

# Aller dans le répertoire du trading bot
cd "$TRADING_BOT_DIR" || exit 1

# Lancer le bot avec tous les arguments nécessaires
echo "🔄 Démarrage du dashboard et de l'API..."
echo "📊 URL du dashboard: http://localhost:8088"
echo ""
echo "💎 TOUS LES RÉGLAGES SERONT ACCESSIBLES DANS LE DASHBOARD"
echo "💰 TRADING RÉEL ACTIVÉ (vous pouvez le désactiver dans le dashboard)"
echo ""

# Ouvrir le navigateur automatiquement dans 3 secondes
(sleep 3 && open "http://localhost:8088") &

# Fonction pour créer un fichier d'environnement temporaire
cat > "$TRADING_BOT_DIR/.env.dashboard" << EOL
COINBASE_API_KEY=$(grep COINBASE_API_KEY "$TRADING_BOT_DIR/coinbase_credentials.env" 2>/dev/null | cut -d= -f2 || echo "")
TRADING_MODE=LIVE
RISK_LEVEL=MEDIUM
MAX_TRADE_AMOUNT=100
PORTFOLIO_ACCESS=ENABLED
BOT_AUTO_START=false
EOL

# Lancer le dashboard avec les options complètes
python dashboard_trading_pro.py --full-features --dashboard-config=.env.dashboard --enable-api --portfolio-live --allow-settings

# Ce code ne sera jamais atteint tant que le dashboard fonctionne
echo "⚠️ Le dashboard s'est arrêté!"
echo "Pour le relancer, double-cliquez à nouveau sur ce script."
sleep 5
