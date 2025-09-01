#!/bin/bash
# 🎯 LANCEUR BOT TRADING AVANCÉ - BUREAU
# Double-cliquez pour lancer le bot avancé (version originale)

echo "🎯 LANCEMENT BOT TRADING AVANCÉ DEPUIS LE BUREAU"
echo "==============================================="

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}📁 Navigation vers le répertoire du bot...${NC}"

# Aller dans le répertoire du bot
cd "/Users/johan/ia_env/bot-trading-/TradingBot_Pro_2025"

if [ ! -d "/Users/johan/ia_env/bot-trading-/TradingBot_Pro_2025" ]; then
    echo -e "${RED}❌ ERREUR: Répertoire du bot introuvable${NC}"
    echo "Vérifiez que le projet est bien dans:"
    echo "/Users/johan/ia_env/bot-trading-/TradingBot_Pro_2025"
    read -p "Appuyez sur Entrée pour fermer..."
    exit 1
fi

echo -e "${GREEN}✅ Répertoire trouvé: $(pwd)${NC}"

echo -e "${PURPLE}🔍 Vérification des fichiers...${NC}"

# Vérifier les fichiers essentiels
if [ ! -f "BOT_TRADING_AVANCE.py" ]; then
    echo -e "${RED}❌ Bot avancé introuvable${NC}"
    exit 1
fi

if [ ! -f "cdp_api_key.json" ]; then
    echo -e "${RED}❌ Configuration API introuvable${NC}"
    echo "Vérifiez que le fichier cdp_api_key.json existe"
    read -p "Appuyez sur Entrée pour fermer..."
    exit 1
fi

if [ ! -d "final_env" ]; then
    echo -e "${RED}❌ Environnement Python introuvable${NC}"
    echo "L'environnement virtuel final_env n'existe pas"
    read -p "Appuyez sur Entrée pour fermer..."
    exit 1
fi

echo -e "${GREEN}✅ Tous les fichiers nécessaires sont présents${NC}"
echo ""

echo -e "${YELLOW}🚀 LANCEMENT DU BOT TRADING AVANCÉ...${NC}"
echo ""
echo -e "${PURPLE}📊 Dashboard accessible sur:${NC}"
echo -e "${GREEN}   🌐 http://localhost:8085${NC}"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANT:${NC}"
echo -e "${YELLOW}   Si vous voyez l'erreur 'account is not available':${NC}"
echo -e "${YELLOW}   → Connectez-vous sur Coinbase.com${NC}"
echo -e "${YELLOW}   → Allez dans Portfolio → Advanced Trade${NC}"
echo -e "${YELLOW}   → Transférez des USDC depuis votre portefeuille principal${NC}"
echo ""
echo -e "${PURPLE}🎯 MODES DE TRADING DISPONIBLES:${NC}"
echo -e "${GREEN}   • Micro Trading: \$1-3 (Ultra sécurisé)${NC}"
echo -e "${GREEN}   • Mode Conservateur: \$2-5 (Prudent)${NC}"
echo -e "${GREEN}   • Mode Équilibré: \$3-8 (Balance)${NC}"
echo -e "${GREEN}   • Mode Dynamique: \$5-12 (Actif)${NC}"
echo -e "${GREEN}   • Mode Agressif: \$8-20 (Maximum profit)${NC}"
echo ""
echo -e "${BLUE}✨ FONCTIONNALITÉS AVANCÉES:${NC}"
echo -e "${GREEN}   • Auto-trading intelligent${NC}"
echo -e "${GREEN}   • Logs système détaillés${NC}"
echo -e "${GREEN}   • Statistiques de performance${NC}"
echo -e "${GREEN}   • Interface moderne et responsive${NC}"
echo ""
echo -e "${RED}⏸️  Fermez cette fenêtre ou appuyez Ctrl+C pour arrêter le bot${NC}"
echo ""

# Lancer le bot avec PYTHONPATH
echo -e "${PURPLE}🔄 Démarrage en cours...${NC}"

# Ouvrir automatiquement le dashboard dans le navigateur après 3 secondes
(sleep 3 && open "http://localhost:8085") &

# Lancer le bot avancé
PYTHONPATH=./final_env/lib/python3.13/site-packages python3 BOT_TRADING_AVANCE.py

echo ""
echo -e "${YELLOW}👋 Bot avancé arrêté. Merci d'avoir utilisé le Bot Trading Avancé!${NC}"
read -p "Appuyez sur Entrée pour fermer cette fenêtre..."
