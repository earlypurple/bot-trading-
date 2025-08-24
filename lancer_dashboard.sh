#!/bin/bash

# Script de lancement du dashboard trading sans erreur de chemin
echo "🚀 Lancement du dashboard trading..."

# Chemin absolu du répertoire du projet
PROJET_DIR="/Users/johan/ia_env/bot-trading-/TradingBot_Pro_2025"

# Activation de l'environnement virtuel
source /Users/johan/ia_env/bin/activate

# Aller dans le bon répertoire
cd "$PROJET_DIR"
echo "📂 Répertoire actuel: $(pwd)"
echo "✅ Fichier dashboard présent: $(ls dashboard_trading_pro.py)"

# Vérification des ports
echo "🔍 Vérification des ports..."
if lsof -ti:8088 > /dev/null; then
  echo "⚠️  Le port 8088 est déjà utilisé, nettoyage..."
  lsof -ti:8088 | xargs kill -9
fi
if lsof -ti:8081 > /dev/null; then
  echo "⚠️  Le port 8081 est déjà utilisé, nettoyage..."
  lsof -ti:8081 | xargs kill -9
fi
if lsof -ti:8082 > /dev/null; then
  echo "⚠️  Le port 8082 est déjà utilisé, nettoyage..."
  lsof -ti:8082 | xargs kill -9
fi

echo "✨ Lancement du dashboard..."
echo "📊 URL du dashboard: http://localhost:8088"
echo ""

# Lancement du script Python
python "$PROJET_DIR/dashboard_trading_pro.py"
