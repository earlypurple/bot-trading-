#!/bin/bash
# 🚀 SCRIPT DE LANCEMENT FINAL
# Lance le bot de trading corrigé

echo "🎯 LANCEMENT BOT TRADING FINAL"
echo "================================"

cd /Users/johan/ia_env/bot-trading-/TradingBot_Pro_2025

echo "📁 Répertoire: $(pwd)"
echo "🔍 Vérification des fichiers..."

if [ ! -f "BOT_TRADING_CORRECTED_FINAL.py" ]; then
    echo "❌ Bot corrigé introuvable"
    exit 1
fi

if [ ! -f "cdp_api_key.json" ]; then
    echo "❌ Configuration API introuvable"
    exit 1
fi

if [ ! -d "final_env" ]; then
    echo "❌ Environnement Python introuvable"
    exit 1
fi

echo "✅ Tous les fichiers présents"
echo ""
echo "🚀 Lancement du bot corrigé..."
echo "📡 Dashboard: http://localhost:8087"
echo ""
echo "⚠️  IMPORTANT:"
echo "   Si erreur 'account is not available':"
echo "   → Transférer des USDC vers Advanced Trade sur Coinbase.com"
echo ""
echo "⏸️  Ctrl+C pour arrêter"
echo ""

# Lancer le bot avec PYTHONPATH
PYTHONPATH=./final_env/lib/python3.13/site-packages python3 BOT_TRADING_CORRECTED_FINAL.py
