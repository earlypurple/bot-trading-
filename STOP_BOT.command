#!/bin/bash

# 🛑 EARLY-BOT-TRADING - Stop Script
# Arrête tous les processus du bot de trading

clear
echo "🛑 ========================================"
echo "   ARRÊT D'EARLY-BOT-TRADING"
echo "======================================== 🛑"
echo ""

echo "🔍 Recherche des processus en cours..."

# Arrêt de tous les processus liés au bot
pkill -f "launch_early_bot"
pkill -f "early_bot_trading"
pkill -f "flask"
pkill -f "8091"

echo "✅ Processus arrêtés"
echo ""
echo "🌐 Vérification des ports..."

# Vérification que le port 8091 est libéré
if lsof -i :8091 >/dev/null 2>&1; then
    echo "⚠️  Port 8091 encore utilisé, forçage de l'arrêt..."
    sudo lsof -ti:8091 | xargs sudo kill -9 2>/dev/null
    echo "✅ Port 8091 libéré"
else
    echo "✅ Port 8091 libre"
fi

echo ""
echo "🛑 EARLY-BOT-TRADING complètement arrêté !"
echo "💡 Pour relancer: double-cliquez sur 🚀 EARLY-BOT-TRADING.command"
echo ""
echo "Fermeture dans 3 secondes..."
sleep 3
