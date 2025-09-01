#!/bin/bash

echo "🚨 LANCEMENT PORTFOLIO CORRIGÉ - SOLUTION FINALE"
echo "================================================"

# Tuer tous les processus Flask existants
echo "🔄 Arrêt des anciens processus..."
pkill -f "flask"
pkill -f "dashboard_trading_pro"
sleep 2

# Aller dans le répertoire
cd "/Users/johan/ia_env/bot-trading-/TradingBot_Pro_2025"

echo "✅ Démarrage du portfolio corrigé..."
echo "🌐 URL: http://localhost:8088"
echo ""
echo "⚠️ CORRECTION APPLIQUÉE:"
echo "   - Portfolio API réparée"
echo "   - Affichage forcé des vraies valeurs"
echo "   - Structure de données corrigée"
echo ""

# Lancer avec python3 directement
/usr/bin/python3 dashboard_trading_pro.py

echo ""
echo "Dashboard arrêté."
