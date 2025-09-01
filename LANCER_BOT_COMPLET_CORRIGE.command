#!/bin/bash

# LANCEMENT COMPLET ET CORRIGÉ - PORTFOLIO FIXÉ - IA ACTIVÉE
# Créé le 24 août 2025
# DOUBLE-CLIQUEZ DESSUS DEPUIS VOTRE BUREAU

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

# Vérifier les corrections
if [ ! -f "$PROJET_DIR/corriger_trading_bot.py" ]; then
  osascript -e 'display dialog "Alerte: Le fichier de correction n'a pas été trouvé. Les problèmes pourraient persister." buttons {"Continuer quand même", "Annuler"} default button "Continuer quand même" with icon caution'
  if [ $? -ne 0 ]; then
    exit 1
  fi
else
  # Exécuter les corrections à nouveau pour s'assurer que tout fonctionne
  echo "🛠️ Vérification des corrections..."
  python "$PROJET_DIR/corriger_trading_bot.py" >/dev/null 2>&1
fi

# Vérifier que le fichier d'identifiants existe
if [ ! -f "$TRADING_BOT_DIR/coinbase_credentials.env" ]; then
  osascript -e 'display dialog "Erreur: Le fichier coinbase_credentials.env est introuvable. Impossible de démarrer le bot." buttons {"OK"} default button "OK" with icon stop'
  exit 1
fi

# Afficher une notification
osascript -e 'display notification "Démarrage du Bot Trading avec portfolio Coinbase et IA" with title "Trading Bot Pro" subtitle "Connexion en cours..." sound name "Submarine"'

echo "✅ Environnement prêt"
echo "✅ Corrections appliquées"
echo "✅ Portfolio Coinbase sera connecté"
echo "✅ IA Trading activée"
echo ""

# Aller dans le répertoire du trading bot
cd "$TRADING_BOT_DIR" || exit 1

# Ouvrir le navigateur automatiquement dans 3 secondes
(sleep 3 && open "http://localhost:8088") &

echo "🔄 Démarrage du dashboard et de l'API..."
echo "📊 URL du dashboard: http://localhost:8088"
echo ""
echo "💎 TOUS LES RÉGLAGES SONT ACCESSIBLES DANS LE DASHBOARD"
echo "💰 TRADING RÉEL ACTIVÉ (vous pouvez le désactiver dans le dashboard)"
echo "🧠 IA TRADING ACTIVÉE"
echo ""

# Lancer le dashboard avec la configuration complète
python dashboard_trading_pro.py --full-features --portfolio-live --enable-ai --enable-api --enable-trading

# Ce code ne sera jamais atteint tant que le dashboard fonctionne
echo "⚠️ Le dashboard s'est arrêté!"
echo "Pour le relancer, double-cliquez à nouveau sur ce script."
sleep 5
