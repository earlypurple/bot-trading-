#!/bin/bash
# 🚀 LANCER PORTFOLIO TRADING - Script de bureau simple
# Johan - Version fonctionnelle

echo "🚀 Démarrage du Portfolio Trading..."
echo "======================================"

# Aller dans le bon dossier
cd /Users/johan/ia_env/bot-trading-/TradingBot_Pro_2025

# Vérifier que Python est disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non trouvé"
    exit 1
fi

echo "✅ Python3 trouvé"
echo "🔗 Connexion au portfolio..."

# Copier la config fonctionnelle
cp /Users/johan/ia_env/bot-trading-/CONFIGURER_API_COINBASE.py ./

# Lancer le dashboard
echo "🎯 Lancement du dashboard..."
python3 dashboard_trading_pro.py

echo "👋 Portfolio fermé"
