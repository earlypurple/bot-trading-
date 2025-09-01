#!/bin/bash

# ULTRA SIMPLE - Lancement du bot de trading avec un seul clic
# Script créé le 24 août 2025 - Version corrigée

# ------- CONFIGURATION -------
PORTFOLIO_REEL=true           # true = trading réel, false = simulation
MONTANT_MAX_TRADE=200         # Montant maximum par trade (en USD)
NIVEAU_RISQUE="MEDIUM"        # LOW, MEDIUM, HIGH
# ----------------------------

# Afficher une interface graphique pour confirmer le lancement
osascript <<EOD
tell application "System Events"
  display dialog "🚨 LANCER LE BOT TRADING COINBASE 🚨\n\n💰 Mode: $([ "$PORTFOLIO_REEL" = true ] && echo "TRADING RÉEL" || echo "SIMULATION")\n💵 Montant max par trade: $MONTANT_MAX_TRADE USD\n⚠️ Niveau de risque: $NIVEAU_RISQUE\n\nÊtes-vous sûr de vouloir lancer le bot?" buttons {"Annuler", "Lancer!"} default button "Lancer!" with icon caution
end tell
EOD

# Vérifier la réponse
if [ $? -ne 0 ]; then
  osascript -e 'display notification "Lancement annulé" with title "Bot Trading" sound name "Basso"'
  exit 0
fi

# Préparer l'environnement
PROJET_DIR="/Users/johan/ia_env/bot-trading-"
cd "$PROJET_DIR"

# Nettoyer les processus existants
pkill -f "python.*dashboard_trading_pro.py" >/dev/null 2>&1 || true
lsof -ti:8088 | xargs kill -9 >/dev/null 2>&1 || true

# Notification de démarrage
osascript -e 'display notification "Bot de trading en cours de démarrage..." with title "Bot Trading" sound name "Submarine"'

# Appliquer la configuration trading réel
if [ "$PORTFOLIO_REEL" = true ]; then
  # Configurer le fichier d'environnement
  cat > "$PROJET_DIR/TradingBot_Pro_2025/trading_config.env" << EOL
TRADING_MODE=LIVE
MAX_TRADE_AMOUNT=$MONTANT_MAX_TRADE
RISK_LEVEL=$NIVEAU_RISQUE
EOL

  # Activer le trading réel
  if [ -f "$PROJET_DIR/activer_trading_reel.sh" ]; then
    bash "$PROJET_DIR/activer_trading_reel.sh" >/dev/null 2>&1
  fi

  # Lancer le bot en mode réel
  echo "🚀 Lancement du bot en MODE RÉEL avec Coinbase..."
  source /Users/johan/ia_env/bin/activate
  cd "$PROJET_DIR/TradingBot_Pro_2025"
  
  # Ouvrir le navigateur automatiquement
  sleep 2
  open "http://localhost:8088"
  
  # Lancer le bot
  python dashboard_trading_pro.py --live-trading
else
  # Lancer en mode simulation
  echo "🚀 Lancement du bot en MODE SIMULATION..."
  source /Users/johan/ia_env/bin/activate
  cd "$PROJET_DIR/TradingBot_Pro_2025"
  
  # Ouvrir le navigateur automatiquement
  sleep 2
  open "http://localhost:8088"
  
  # Lancer le bot
  python dashboard_trading_pro.py --test-mode
fi
