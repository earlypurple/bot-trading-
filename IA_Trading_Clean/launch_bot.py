#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur du Bot IA Trading
"""

import os
import sys

# Ajouter le répertoire du bot au path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

if __name__ == '__main__':
    print("🚀 LANCEMENT DU BOT IA TRADING")
    print("=" * 50)
    print("📊 Interface web: http://localhost:8091")
    print("🔄 Ctrl+C pour arrêter")
    print("=" * 50)
    
    # Import et lancement du bot
    from bot.ai_trading_bot import app, socketio, bot
    
    print("🤖 LANCEMENT BOT IA TRADING AUTOMATISÉ")
    print("=" * 60)
    
    # Test de connexion
    print("📊 Test de connexion avec nouvelles clés...")
    balance = bot.get_portfolio_balance()
    if balance is not None:
        print(f"✅ Portfolio connecté: ${balance:.2f}")
    else:
        print("❌ Erreur connexion portfolio")
    
    print("\n🌐 Démarrage interface web...")
    print("📱 Dashboard IA disponible sur: http://localhost:8091")
    print("🤖 Interface de contrôle du bot de trading")
    print("🔄 Appuyez sur Ctrl+C pour arrêter")
    
    try:
        socketio.run(app, host='0.0.0.0', port=8091, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du bot IA...")
        bot.is_running = False
        bot.is_trading = False
    except Exception as e:
        print(f"❌ Erreur serveur: {e}")
