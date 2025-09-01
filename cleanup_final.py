#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NETTOYAGE FINAL - Supprime tout sauf IA_Trading_Clean
"""

import os
import shutil
import sys

def cleanup_final():
    """Supprime tout sauf le dossier IA_Trading_Clean"""
    
    base_path = "/Users/johan/ia_env/bot-trading-"
    
    # Éléments à garder ABSOLUMENT
    keep_items = {
        'IA_Trading_Clean',  # Notre bot propre
        '.git',              # Repository git
        '.gitignore',        # Git ignore
        'LICENSE'            # Licence du projet
    }
    
    try:
        print("🧹 NETTOYAGE FINAL DE L'ESPACE DE TRAVAIL")
        print("=" * 60)
        print("⚠️  SUPPRESSION DE TOUS LES FICHIERS INUTILES")
        print("✅ Conservation uniquement: IA_Trading_Clean + Git")
        print("=" * 60)
        
        # Lister tous les éléments
        all_items = os.listdir(base_path)
        
        deleted_count = 0
        kept_count = 0
        
        for item in all_items:
            item_path = os.path.join(base_path, item)
            
            if item in keep_items:
                print(f"✅ GARDÉ: {item}")
                kept_count += 1
                continue
            else:
                try:
                    if os.path.isdir(item_path):
                        print(f"🗑️  SUPPRIMÉ (dossier): {item}")
                        shutil.rmtree(item_path)
                    else:
                        print(f"🗑️  SUPPRIMÉ (fichier): {item}")
                        os.remove(item_path)
                    deleted_count += 1
                except Exception as e:
                    print(f"❌ Erreur suppression {item}: {e}")
        
        print("\n" + "=" * 60)
        print("✅ NETTOYAGE TERMINÉ AVEC SUCCÈS")
        print(f"📊 Statistiques:")
        print(f"   🗑️  Éléments supprimés: {deleted_count}")
        print(f"   ✅ Éléments conservés: {kept_count}")
        print(f"📁 Projet nettoyé dans: {base_path}/IA_Trading_Clean")
        print("=" * 60)
        
        # Créer un fichier README principal
        readme_content = """# 🤖 IA Trading Bot - Version Finale

## 📁 Structure Nettoyée

Le projet a été complètement nettoyé et reorganisé dans le dossier `IA_Trading_Clean/`

### 🚀 Lancement Rapide
```bash
cd IA_Trading_Clean
python3 launch_bot.py
```

### 📊 Interface Web
- URL: http://localhost:8090
- Paramètres de trading visibles
- Contrôles Start/Stop
- Monitoring temps réel

### ✅ Fonctionnalités
- ✅ API Coinbase configurée et fonctionnelle
- ✅ Bot IA avec analyse technique complète
- ✅ Interface web avec tous les paramètres visibles
- ✅ Gestion des risques intégrée
- ✅ Notifications temps réel
- ✅ Architecture propre et organisée

---
**Version finale nettoyée - Tous les fichiers inutiles supprimés**
"""
        
        readme_path = os.path.join(base_path, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("📝 README principal créé")
        
    except Exception as e:
        print(f"❌ Erreur nettoyage: {e}")

if __name__ == '__main__':
    print("🚨 ATTENTION: NETTOYAGE FINAL")
    print("Ce script va supprimer TOUS les fichiers sauf IA_Trading_Clean")
    print("Le bot IA continuera de fonctionner normalement")
    print("\nVoulez-vous continuer? (y/N): ", end="")
    
    response = input().strip().lower()
    if response in ['y', 'yes', 'oui']:
        cleanup_final()
    else:
        print("❌ Nettoyage annulé")
