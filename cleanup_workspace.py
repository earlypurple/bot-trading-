#!/usr/bin/env python3
"""
🧹 NETTOYAGE D'URGENCE DE L'ESPACE DE TRAVAIL
Supprime les fichiers redondants et organise proprement
"""

import os
import shutil
import sys
from pathlib import Path

def cleanup_workspace():
    """Nettoie l'espace de travail chaotique"""
    
    root_dir = Path("/Users/johan/ia_env/bot-trading-")
    
    print("🧹 NETTOYAGE D'URGENCE DE L'ESPACE DE TRAVAIL")
    print("=" * 50)
    
    # 1. Fichiers à supprimer (redondants/obsolètes)
    files_to_delete = [
        "BOT_TRADING_APP.py",
        "CONFIGURER_API_COINBASE.py", 
        "CORRECTIF_DEFINITIF.py",
        "CORRIGER_PORTFOLIO_URGENT.py",
        "LANCER_APP_TRADING.command",
        "LANCER_BOT_COMPLET.command",
        "LANCER_BOT_COMPLET_CORRIGE.command",
        "LANCER_BOT_CORRIGE.command",
        "LANCER_BOT_TRADING.command",
        "LANCER_BOT_TRADING_FIX.command",
        "LANCER_PORTFOLIO_CORRIGE.command",
        "LANCER_PORTFOLIO_TRADING.command",
        "REPARER_API_MAINTENANT.py",
        "RESTAURER_CLES_HARDCODEES.py",
        "TEST_PORTFOLIO_RAPIDE.py",
        "activer_trading_reel.sh",
        "appliquer_correctifs.sh",
        "arreter_dashboard.sh",
        "cleanup_final.py",
        "cles_coinbase_fonctionnelles.txt",
        "configurer_acces_iphone.sh",
        "correction_avancee.py",
        "corriger_connexion.sh",
        "corriger_trading_bot.py",
        "lancer_dashboard.sh",
        "reparateur_urgence.sh",
        "restaurer_cles_fonctionnelles.py"
    ]
    
    print("🗑️  Suppression des fichiers redondants...")
    deleted_count = 0
    for filename in files_to_delete:
        file_path = root_dir / filename
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"   ✅ Supprimé: {filename}")
                deleted_count += 1
            except Exception as e:
                print(f"   ❌ Erreur: {filename} - {e}")
    
    print(f"\n📊 {deleted_count} fichiers supprimés")
    
    # 2. Dossiers à conserver
    keep_dirs = ["Early-Bot-Trading", "TradingBot_Pro_2025", ".git"]
    
    print("\n📁 Répertoires conservés:")
    for dir_name in keep_dirs:
        dir_path = root_dir / dir_name
        if dir_path.exists():
            print(f"   ✅ {dir_name}")
    
    # 3. Suppression du dossier IA_Trading_Clean s'il existe
    ia_clean_dir = root_dir / "IA_Trading_Clean"
    if ia_clean_dir.exists():
        try:
            shutil.rmtree(ia_clean_dir)
            print(f"   🗑️  Supprimé: IA_Trading_Clean (redondant)")
        except Exception as e:
            print(f"   ❌ Erreur suppression IA_Trading_Clean: {e}")
    
    print("\n🎯 STRUCTURE FINALE:")
    print("=" * 30)
    for item in sorted(root_dir.iterdir()):
        if item.is_dir():
            print(f"📁 {item.name}/")
        else:
            print(f"📄 {item.name}")
    
    print("\n✅ NETTOYAGE TERMINÉ!")
    print("📂 Répertoire principal de travail: Early-Bot-Trading/")
    print("🤖 Fichier bot principal: Early-Bot-Trading/bot/early_bot_trading.py")

if __name__ == "__main__":
    cleanup_workspace()
