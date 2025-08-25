#!/bin/bash

# 🚀 EARLY-BOT-TRADING - Launcher Script
# Créé automatiquement pour Johan
# Double-cliquez pour lancer le bot de trading

clear
echo "🚀 ========================================"
echo "   EARLY-BOT-TRADING - LAUNCHER"
echo "======================================== 🚀"
echo ""
echo "💎 Bot optimisé pour micro-trading"
echo "🎯 Montants minimum : 0.25€ - 1€"
echo "⚡ Modes : Conservateur, Normal, Agressif, Scalping"
echo ""
echo "🔄 Démarrage en cours..."
echo ""

# Navigation vers le dossier du bot
cd "/Users/johan/ia_env/bot-trading-/Early-Bot-Trading"

# Vérification que le dossier existe
if [ ! -d "/Users/johan/ia_env/bot-trading-/Early-Bot-Trading" ]; then
    echo "❌ ERREUR: Dossier Early-Bot-Trading introuvable !"
    echo "   Chemin attendu: /Users/johan/ia_env/bot-trading-/Early-Bot-Trading"
    echo ""
    echo "Appuyez sur Entrée pour fermer..."
    read
    exit 1
fi

# Affichage du portfolio avant lancement
echo "💰 Chargement de votre portfolio..."
echo ""

# Lancement du bot
echo "🌐 Lancement du serveur..."
echo "📱 Dashboard disponible sur: http://localhost:8091"
echo ""
echo "⚠️  INSTRUCTIONS:"
echo "   1. Le dashboard va s'ouvrir automatiquement"
echo "   2. Choisissez votre mode de trading"
echo "   3. Cliquez sur START TRADING pour commencer"
echo "   4. Pour arrêter: fermez cette fenêtre ou Ctrl+C"
echo ""
echo "🎯 Modes recommandés pour votre portfolio ($15.86):"
echo "   🛡️  Conservateur: 0.50€ min (ultra sécurisé)"
echo "   ⚡ Scalping: 0.25€ min (micro-trading rapide)"
echo ""
echo "▶️  Démarrage dans 3 secondes..."
sleep 1
echo "▶️  Démarrage dans 2 secondes..."
sleep 1
echo "▶️  Démarrage dans 1 seconde..."
sleep 1

# Lancement du bot
echo ""
echo "🚀 LANCEMENT D'EARLY-BOT-TRADING..."
echo "================================================"

# Ouverture automatique du dashboard dans le navigateur (après 5 secondes)
(sleep 5 && open "http://localhost:8091") &

# Lancement du bot Python
/usr/bin/python3 /Users/johan/ia_env/bot-trading-/Early-Bot-Trading/launch_early_bot.py

# Message de fin
echo ""
echo "🛑 Early-Bot-Trading arrêté."
echo "💡 Pour relancer: double-cliquez à nouveau sur ce fichier"
echo ""
echo "Appuyez sur Entrée pour fermer..."
read
