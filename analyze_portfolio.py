#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyseur de Portefeuille - Early-Bot-Trading
Conseils personnalisés pour votre portefeuille de $15.87
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.api_config import TRADING_MODES
import ccxt

def analyze_portfolio():
    print("📊 ANALYSE PERSONNALISÉE DE VOTRE PORTEFEUILLE")
    print("=" * 60)
    
    # Données de votre portefeuille
    portfolio = {
        'BCH': 5.80,
        'ETH': 5.29,
        'SOL': 1.36,
        'FLR': 1.34,
        'SHIB': 0.91,
        'ETC': 0.65,
        'AST': 0.44,
        'API3': 0.08,
        'ATOM': 0.01,
        'autres': 0.00
    }
    
    total = sum(portfolio.values())
    print(f"💰 TOTAL PORTEFEUILLE: ${total:.2f}")
    print()
    
    print("🎯 RÉPARTITION ACTUELLE:")
    for crypto, value in sorted(portfolio.items(), key=lambda x: x[1], reverse=True):
        percentage = (value / total) * 100
        if value > 0:
            print(f"   {crypto:>6}: ${value:>5.2f} ({percentage:>5.1f}%)")
    print()
    
    print("📈 MES RECOMMANDATIONS POUR VOTRE PORTEFEUILLE:")
    print()
    
    print("🎯 STRATÉGIE RECOMMANDÉE:")
    print("   1️⃣ COMMENCEZ avec le mode 'Conservateur'")
    print("      • Montant minimum: $0.50 seulement")
    print("      • Risque ultra-faible: 0.5% par trade")
    print("      • Stop-loss sécurisé: 2%")
    print()
    
    print("   2️⃣ CRYPTOS À PRIVILÉGIER pour débuter:")
    print("      🥇 ETH - Plus stable, bonnes analyses techniques")
    print("      🥈 SOL - Bon momentum, volatilité intéressante") 
    print("      🥉 BCH - Votre plus gros holding, bon pour scalping")
    print()
    
    print("   3️⃣ ÉVITEZ temporairement:")
    print("      ⚠️ SHIB - Trop volatil pour débuter")
    print("      ⚠️ Petites positions (<$1) - Frais trop élevés")
    print()
    
    print("⚡ PROGRESSION RECOMMANDÉE:")
    print("   ÉTAPE 1: Mode Conservateur (1-2 semaines)")
    print("           → Apprenez les signaux sans risque")
    print("           → Montants: $0.50 - $0.75")
    print()
    print("   ÉTAPE 2: Mode Normal (après gains de confiance)")
    print("           → Montants: $0.75 - $1.50")
    print("           → Plus de trades, RSI + MACD")
    print()
    print("   ÉTAPE 3: Mode Scalping (quand maîtrisé)")
    print("           → Montants: $0.25 - $2.00")
    print("           → Trading rapide, petits profits fréquents")
    print()
    
    print("💡 CONSEILS SPÉCIAUX POUR VOTRE SITUATION:")
    print("   • Votre portefeuille est PARFAIT pour apprendre")
    print("   • Diversifié mais pas trop dispersé")
    print("   • ETH + SOL = bonnes paires pour débuter")
    print("   • Avec $15.87, vous pouvez faire 30-60 micro-trades")
    print("   • Objectif réaliste: +10-20% en 1 mois")
    print()
    
    print("🚀 MODES OPTIMISÉS POUR VOUS:")
    for mode_name, config in TRADING_MODES.items():
        trades_possibles = int(total / config['min_trade_amount'])
        print(f"   {config['name']} - Min: ${config['min_trade_amount']:.2f}")
        print(f"      → Vous pouvez faire {trades_possibles} trades")
        print(f"      → Risque: {config['risk_level']}")
        print(f"      → Position max: {config['max_position_size']*100:.1f}% (${total * config['max_position_size']:.2f})")
        print()
    
    print("🎯 PLAN D'ACTION IMMÉDIAT:")
    print("   1. Lancez le bot en mode Conservateur")
    print("   2. Activez le trading sur ETH/USD uniquement")
    print("   3. Laissez tourner 1-2 heures en observation")
    print("   4. Commencez avec 1-2 trades de $0.50")
    print("   5. Analysez les résultats avant d'augmenter")
    print()
    
    print("💎 POTENTIEL DE VOTRE PORTEFEUILLE:")
    print(f"   • Avec trading conservateur: +${total * 0.1:.2f} par mois")
    print(f"   • Avec trading normal: +${total * 0.2:.2f} par mois") 
    print(f"   • Avec scalping maîtrisé: +${total * 0.4:.2f} par mois")
    print()
    print("⚠️ ATTENTION: Commencez doucement et apprenez d'abord !")

if __name__ == "__main__":
    analyze_portfolio()
