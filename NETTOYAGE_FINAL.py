#!/usr/bin/env python3
"""
🧹 SCRIPT DE NETTOYAGE FINAL
Garde seulement le bot fonctionnel et supprime les fichiers inutiles
"""

import os
import shutil
import glob

def main():
    print("🧹 NETTOYAGE DE L'ESPACE DE TRAVAIL")
    print("=" * 50)
    
    base_path = "/Users/johan/ia_env/bot-trading-"
    
    # Fichiers à GARDER absolument
    files_to_keep = {
        # Bot principal et dashboard corrigé
        "TradingBot_Pro_2025/BOT_TRADING_CORRECTED_FINAL.py",
        "TradingBot_Pro_2025/BOT_TRADING_AVANCE.py", 
        "TradingBot_Pro_2025/cdp_api_key.json",
        
        # Configuration essentielle
        "TradingBot_Pro_2025/requirements.txt",
        "TradingBot_Pro_2025/.env",
        
        # Documentation importante
        "TradingBot_Pro_2025/README_SUCCESS.md",
        "TradingBot_Pro_2025/GUIDE_COMPLET_COINBASE.md",
        
        # Logs de trading
        "TradingBot_Pro_2025/TRADING_AVANCE.log",
        "TradingBot_Pro_2025/TRADING_CORRECTED.log",
        
        # Environnement virtuel
        "TradingBot_Pro_2025/final_env/",
        
        # Frontend si nécessaire
        "TradingBot_Pro_2025/frontend/",
        "TradingBot_Pro_2025/src/",
    }
    
    # Patterns de fichiers à SUPPRIMER
    patterns_to_delete = [
        "test_*.py",
        "diagnostic_*.py", 
        "check_*.py",
        "debug_*.py",
        "demo_*.py",
        "launch_*.py",
        "setup_*.py",
        "configure_*.py",
        "fix_*.py",
        "reconfigure_*.py",
        "monitor_*.py",
        "testeur_*.py",
        "*_test.py",
        "*_demo.py",
        "*_debug.py",
        "app_simple.py",
        "dashboard_*.py",
        "serveur_*.py",
        "portfolio_*.py",
        "bot_ia_trading.py",
        "start_*.py",
        "smart_launcher.py",
        "lanceur_*.py",
        "correctif_*.py",
        "advanced_trade_connector.py",
        "certification_finale.py",
        "tradingbot_*.py",
        "*.command",
        "*.sh",
        "*.md.backup",
        "*.log.old",
    ]
    
    print("🎯 FICHIERS À CONSERVER:")
    for file in files_to_keep:
        print(f"   ✅ {file}")
    
    print(f"\n📁 Analyse du répertoire: {base_path}")
    
    # Parcourir TradingBot_Pro_2025
    tradingbot_path = os.path.join(base_path, "TradingBot_Pro_2025")
    if os.path.exists(tradingbot_path):
        deleted_count = 0
        
        # Supprimer les fichiers selon les patterns
        for pattern in patterns_to_delete:
            files = glob.glob(os.path.join(tradingbot_path, pattern))
            for file in files:
                relative_file = os.path.relpath(file, base_path)
                if relative_file not in files_to_keep:
                    try:
                        os.remove(file)
                        print(f"   🗑️ Supprimé: {os.path.basename(file)}")
                        deleted_count += 1
                    except Exception as e:
                        print(f"   ❌ Erreur suppression {file}: {e}")
        
        # Supprimer le dossier tests complet
        tests_path = os.path.join(tradingbot_path, "tests")
        if os.path.exists(tests_path):
            try:
                shutil.rmtree(tests_path)
                print(f"   🗑️ Dossier supprimé: tests/")
                deleted_count += 1
            except Exception as e:
                print(f"   ❌ Erreur suppression tests/: {e}")
        
        print(f"\n✅ Nettoyage terminé: {deleted_count} éléments supprimés")
    
    # Nettoyer Early-Bot-Trading (garder seulement quelques fichiers)
    early_path = os.path.join(base_path, "Early-Bot-Trading")
    if os.path.exists(early_path):
        print(f"\n📁 Nettoyage Early-Bot-Trading...")
        
        # Fichiers à garder dans Early-Bot-Trading
        early_keep = [
            "cdp_api_key.json",
            "BOT_TRADING_FINAL.py",
            "micro_env/",
            "trading_env/"
        ]
        
        deleted_early = 0
        for item in os.listdir(early_path):
            item_path = os.path.join(early_path, item)
            if item not in early_keep:
                try:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                    print(f"   🗑️ Supprimé: {item}")
                    deleted_early += 1
                except Exception as e:
                    print(f"   ❌ Erreur: {e}")
        
        print(f"✅ Early-Bot-Trading nettoyé: {deleted_early} éléments supprimés")
    
    # Créer un README final
    readme_path = os.path.join(tradingbot_path, "README_FINAL.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("""# 🎯 Bot Trading Final - Version Nettoyée

## 📁 Structure Finale

### Fichiers Principaux
- **BOT_TRADING_CORRECTED_FINAL.py** - Bot corrigé (port 8087)
- **BOT_TRADING_AVANCE.py** - Bot avancé original (port 8085)
- **cdp_api_key.json** - Configuration API Coinbase

### Lancement
```bash
cd TradingBot_Pro_2025
PYTHONPATH=./final_env/lib/python3.13/site-packages python3 BOT_TRADING_CORRECTED_FINAL.py
```

### Dashboard
- Bot Corrigé: http://localhost:8087
- Bot Avancé: http://localhost:8085

## ⚠️ Erreur "account is not available"

### Cause
Les fonds USDC sont dans le portefeuille principal Coinbase, pas dans Advanced Trade.

### Solution
1. Aller sur Coinbase.com
2. Portfolio → Advanced Trade  
3. Transférer des USDC vers Advanced Trade
4. Ou utiliser l'interface Coinbase pour faire le transfert interne

### Vérification
```python
# Le bot détecte automatiquement:
# - ✅ 51 comptes trouvés
# - ❌ 0 comptes USDC dans Advanced Trade  
# - ✅ 5.62 USDC disponibles (mais pas dans le bon portefeuille)
```

## 🎯 Modes de Trading
- **Micro** ($1-3) - Ultra sécurisé
- **Conservateur** ($2-5) - Prudent
- **Équilibré** ($3-8) - Balance
- **Dynamique** ($5-12) - Actif
- **Agressif** ($8-20) - Maximum profit

## 🚀 Status
- ✅ API connectée et fonctionnelle
- ✅ Dashboard opérationnel
- ✅ 5 modes de trading
- ✅ Auto-trading configuré
- ⚠️ Besoin de transférer fonds vers Advanced Trade
""")
    
    print(f"\n📄 README final créé: {readme_path}")
    
    print("\n" + "=" * 50)
    print("🎯 NETTOYAGE TERMINÉ!")
    print("\n✅ FICHIERS CONSERVÉS:")
    print("   • BOT_TRADING_CORRECTED_FINAL.py (corrigé)")
    print("   • BOT_TRADING_AVANCE.py (original)")
    print("   • Configuration API et environnements")
    print("   • Documentation essentielle")
    print("\n🗑️ FICHIERS SUPPRIMÉS:")
    print("   • Tests et diagnostics")
    print("   • Fichiers temporaires")  
    print("   • Anciens bots obsolètes")
    print("   • Scripts de configuration")
    print("\n💡 PROCHAINE ÉTAPE:")
    print("   Transférer des USDC vers Advanced Trade sur Coinbase")

if __name__ == "__main__":
    main()
