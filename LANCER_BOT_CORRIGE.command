#!/bin/bash

# BOT TRADING COINBASE - VERSION CORRIGÉE - CONNEXION PORTFOLIO FIXÉE
# Créé le 24 août 2025
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

# Vérifier que le fichier d'identifiants existe
if [ ! -f "$TRADING_BOT_DIR/coinbase_credentials.env" ]; then
  osascript -e 'display dialog "Erreur: Le fichier coinbase_credentials.env est introuvable. Impossible de démarrer le bot." buttons {"OK"} default button "OK" with icon stop'
  exit 1
fi

# Extraire les identifiants Coinbase
COINBASE_API_KEY=$(grep "COINBASE_API_KEY" "$TRADING_BOT_DIR/coinbase_credentials.env" | cut -d'=' -f2)
# On ne peut pas extraire la clé privée facilement car elle est sur plusieurs lignes

# Afficher une notification
osascript -e 'display notification "Démarrage du Bot Trading avec portfolio Coinbase" with title "Trading Bot Pro" subtitle "Connexion en cours..." sound name "Submarine"'

echo "✅ Environnement prêt"
echo "✅ Identifiants Coinbase trouvés"
echo "✅ Portfolio Coinbase sera connecté"
echo ""

# Aller dans le répertoire du trading bot
cd "$TRADING_BOT_DIR" || exit 1

# Création d'un script temporaire pour configurer le bot correctement
cat > "$TRADING_BOT_DIR/temp_setup.py" << EOL
#!/usr/bin/env python3
import os
import sys
import json

# Lire le fichier coinbase_credentials.env
with open('coinbase_credentials.env', 'r') as f:
    lines = f.readlines()

# Extraire les identifiants
api_key = None
private_key_lines = []
in_private_key = False

for line in lines:
    if line.strip().startswith('COINBASE_API_KEY='):
        api_key = line.strip().split('=', 1)[1]
    elif '-----BEGIN EC PRIVATE KEY-----' in line:
        in_private_key = True
        private_key_lines.append(line.strip())
    elif in_private_key and '-----END EC PRIVATE KEY-----' in line:
        private_key_lines.append(line.strip())
        in_private_key = False
    elif in_private_key:
        private_key_lines.append(line.strip())

# Créer un fichier de configuration temporaire pour le dashboard
private_key = '\\n'.join(private_key_lines) if private_key_lines else ''

# Créer un fichier de configuration JSON pour le dashboard
config = {
    'api_key': api_key,
    'private_key': private_key,
    'trading_mode': 'LIVE',
    'risk_level': 'MEDIUM',
    'max_trade_amount': 100,
    'portfolio_access': True,
    'auto_start': False
}

# Sauvegarder le fichier de configuration
with open('.dashboard_config.json', 'w') as f:
    json.dump(config, f)

print("Configuration prête pour le dashboard")
EOL

# Exécuter le script de configuration temporaire
python "$TRADING_BOT_DIR/temp_setup.py"

# Ouvrir le navigateur automatiquement dans 3 secondes
(sleep 3 && open "http://localhost:8088") &

echo "🔄 Démarrage du dashboard et de l'API..."
echo "📊 URL du dashboard: http://localhost:8088"
echo ""
echo "💎 TOUS LES RÉGLAGES SONT ACCESSIBLES DANS LE DASHBOARD"
echo "💰 TRADING RÉEL ACTIVÉ (vous pouvez le désactiver dans le dashboard)"
echo ""

# Lancer le dashboard avec la configuration correcte
python dashboard_trading_pro.py --config-file=.dashboard_config.json --enable-api --portfolio-live --enable-trading

# Ce code ne sera jamais atteint tant que le dashboard fonctionne
echo "⚠️ Le dashboard s'est arrêté!"
echo "Pour le relancer, double-cliquez à nouveau sur ce script."
sleep 5

# Nettoyer le fichier temporaire au démarrage
rm -f "$TRADING_BOT_DIR/temp_setup.py" "$TRADING_BOT_DIR/.dashboard_config.json"
