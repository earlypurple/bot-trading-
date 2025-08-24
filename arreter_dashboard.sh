#!/bin/bash

# Script pour arrêter le dashboard trading
echo "🛑 Arrêt du dashboard trading..."

# Arrêter tous les processus python liés au dashboard
if pgrep -f "python.*dashboard_trading_pro.py" > /dev/null; then
  echo "⚠️ Arrêt des processus dashboard..."
  pkill -f "python.*dashboard_trading_pro.py"
  echo "✅ Processus arrêtés"
else
  echo "ℹ️ Aucun processus dashboard en cours d'exécution"
fi

# Vérification des ports utilisés
echo "🔍 Vérification des ports..."
if lsof -ti:8088 > /dev/null; then
  echo "⚠️ Le port 8088 est toujours utilisé, nettoyage..."
  lsof -ti:8088 | xargs kill -9
fi
if lsof -ti:8081 > /dev/null; then
  echo "⚠️ Le port 8081 est toujours utilisé, nettoyage..."
  lsof -ti:8081 | xargs kill -9
fi
if lsof -ti:8082 > /dev/null; then
  echo "⚠️ Le port 8082 est toujours utilisé, nettoyage..."
  lsof -ti:8082 | xargs kill -9
fi

echo "✅ Dashboard complètement arrêté"
