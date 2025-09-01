#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de nettoyage - Supprime les fichiers inutiles
"""

import os
import shutil
import sys

def clean_workspace():
    """Nettoie l'espace de travail en gardant seulement l'essentiel"""
    
    base_path = "/Users/johan/ia_env/bot-trading-"
    
    # Fichiers/dossiers à conserver
    keep_items = {
        'IA_Trading_Clean',  # Notre nouvelle structure propre
        '.git',              # Git repository
        '.gitignore',        # Git ignore
        'LICENSE',           # Licence
        'README.md'          # README principal
    }
    
    # Fichiers à garder temporairement pour référence
    temp_keep = {
        'CONFIGURER_API_COINBASE.py',  # Configuration API de référence
        'cles_coinbase_fonctionnelles.txt'  # Backup des clés
    }
    
    try:
        print("🧹 NETTOYAGE DE L'ESPACE DE TRAVAIL")
        print("=" * 50)
        
        # Lister tous les éléments
        all_items = os.listdir(base_path)
        
        for item in all_items:
            item_path = os.path.join(base_path, item)
            
            if item in keep_items:
                print(f"✅ Gardé: {item}")
                continue
            elif item in temp_keep:
                print(f"📦 Gardé temporairement: {item}")
                continue
            else:
                try:
                    if os.path.isdir(item_path):
                        print(f"🗑️  Suppression dossier: {item}")
                        shutil.rmtree(item_path)
                    else:
                        print(f"🗑️  Suppression fichier: {item}")
                        os.remove(item_path)
                except Exception as e:
                    print(f"❌ Erreur suppression {item}: {e}")
        
        print("\n✅ NETTOYAGE TERMINÉ")
        print(f"📁 Structure propre dans: {base_path}/IA_Trading_Clean")
        
    except Exception as e:
        print(f"❌ Erreur nettoyage: {e}")

if __name__ == '__main__':
    print("⚠️  ATTENTION: Ce script va supprimer les fichiers inutiles")
    print("Voulez-vous continuer? (y/N): ", end="")
    
    response = input().strip().lower()
    if response in ['y', 'yes', 'oui']:
        clean_workspace()
    else:
        print("❌ Nettoyage annulé")
