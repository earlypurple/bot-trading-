#!/usr/bin/env python3
"""
Nettoyage des fichiers obsolètes du projet
Supprime les anciens fichiers dashboard et garde le nouveau système
"""

import os
import shutil

def main():
    print("🧹 NETTOYAGE DES FICHIERS OBSOLÈTES")
    print("=" * 50)
    
    # Fichiers obsolètes à supprimer
    obsolete_files = [
        'dashboard_modes.html',
        'guide_configurateur.txt',
        'bot_trading_ia_v2.py',
        'launch_bot_clean.py',
        'launch_early_bot.py',
        'cleanup_workspace.py',
        'diagnostic_portfolio.py',
        'enhanced_portfolio_manager.py',
        'test_all_enhancements.py',
        'consolidate_portfolio.py',
        'validate_certification.py',
        'test_coinbase_configs.py',
        'test_auth_cdp.py',
        'test_bot_complet.py'
    ]
    
    # Dossiers obsolètes à supprimer
    obsolete_dirs = [
        'templates',
        'old_files',
        'backup'
    ]
    
    deleted_count = 0
    
    # Suppression des fichiers obsolètes
    for file in obsolete_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✅ Supprimé: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Erreur suppression {file}: {e}")
    
    # Suppression des dossiers obsolètes
    for dir in obsolete_dirs:
        if os.path.exists(dir):
            try:
                shutil.rmtree(dir)
                print(f"📁 Dossier supprimé: {dir}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Erreur suppression dossier {dir}: {e}")
    
    print()
    print(f"🎯 RÉSULTAT: {deleted_count} éléments supprimés")
    print()
    print("📋 FICHIERS CONSERVÉS (système optimisé):")
    print("  ✅ serveur_dashboard.py - Serveur principal")
    print("  ✅ dashboard_complet.html - Interface web moderne")
    print("  ✅ launch_dashboard_complet.py - Launcher")
    print("  ✅ configure_trading_modes.py - Configuration modes")
    print("  ✅ bot/early_bot_trading.py - Bot principal")
    print()
    print("🚀 Projet nettoyé et optimisé !")

if __name__ == "__main__":
    main()
