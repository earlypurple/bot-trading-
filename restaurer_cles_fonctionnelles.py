#!/usr/bin/env python3
"""
🔄 RESTAURATEUR DES CLÉS COINBASE FONCTIONNELLES
Ce script restaure les clés API Coinbase fonctionnelles dans le dashboard
"""

import os
import shutil
import sys
import time
from datetime import datetime

# Chemins importants
PROJECT_DIR = "/Users/johan/ia_env/bot-trading-"
TRADING_BOT_DIR = os.path.join(PROJECT_DIR, "TradingBot_Pro_2025")
DASHBOARD_PATH = os.path.join(TRADING_BOT_DIR, "dashboard_trading_pro.py")
WORKING_DASHBOARD_PATH = os.path.join(TRADING_BOT_DIR, "dashboard_trading_fonctionnel.py")

# Clés API fonctionnelles (originales)
API_KEY_FONCTIONNELLE = "08d4759c-8572-4224-a3c8-6a63cf877fd6"
PRIVATE_KEY_FONCTIONNELLE = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIDdqwLclidk5lL0hF0rev6nDBBZFQYBjbs4r+ZdqqdZPoAoGCCqGSM49
AwEHoUQDQgAEFpDQesMVJlwz1CA5dgfDDfvigRXUimALaJE7bn6Hn8WNDMkGasds
Wqk/bwMFJGkLuyeXWMIUyMZFbuwVpptwNg==
-----END EC PRIVATE KEY-----"""

def create_backup(file_path):
    """Crée une sauvegarde du fichier"""
    backup_path = f"{file_path}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
    shutil.copy2(file_path, backup_path)
    print(f"✅ Sauvegarde créée: {backup_path}")
    return backup_path

def create_working_dashboard():
    """Crée une version du dashboard avec les clés fonctionnelles"""
    print("\n📊 Création du dashboard avec les clés fonctionnelles...")
    
    # Lire le contenu du dashboard original
    with open(DASHBOARD_PATH, 'r') as f:
        content = f.read()
    
    # Modifier la méthode setup_exchange pour utiliser les clés fonctionnelles
    import re
    exchange_pattern = r'def setup_exchange\(self\):(.*?)try:(.*?)private_key = """.*?"""(.*?)\'apiKey\': \'.*?\''
    
    # Créer le remplacement
    replacement = f"""def setup_exchange(self):\\1try:\\2private_key = \"\"\"-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIDdqwLclidk5lL0hF0rev6nDBBZFQYBjbs4r+ZdqqdZPoAoGCCqGSM49
AwEHoUQDQgAEFpDQesMVJlwz1CA5dgfDDfvigRXUimALaJE7bn6Hn8WNDMkGasds
Wqk/bwMFJGkLuyeXWMIUyMZFbuwVpptwNg==
-----END EC PRIVATE KEY-----\"\"\"\\3'apiKey': '08d4759c-8572-4224-a3c8-6a63cf877fd6'"""
    
    # Effectuer le remplacement
    modified_content = re.sub(exchange_pattern, replacement, content, flags=re.DOTALL)
    
    # Vérifier si le remplacement a été effectué
    if modified_content == content:
        print("❌ Échec de la modification des clés API dans le dashboard")
        return False
    
    # Ajouter un commentaire pour indiquer la modification
    header_comment = """#!/usr/bin/env python3
\"\"\"
🚀 TRADING BOT PRO DASHBOARD - Version Professionnelle avec clés fonctionnelles
Multiple stratégies, gestion des risques, interface avancée avec IA avancée
Version restaurée automatiquement le {}
\"\"\"
""".format(datetime.now().strftime('%d/%m/%Y à %H:%M'))
    
    modified_content = re.sub(r'#!/usr/bin/env python3.*?""".*?"""', header_comment, modified_content, flags=re.DOTALL)
    
    # Écrire le contenu modifié
    with open(WORKING_DASHBOARD_PATH, 'w') as f:
        f.write(modified_content)
    
    # Rendre le fichier exécutable
    os.chmod(WORKING_DASHBOARD_PATH, 0o755)
    
    print("✅ Dashboard avec clés fonctionnelles créé avec succès!")
    return True

def create_launcher_script():
    """Crée un script de lancement pour le dashboard avec clés fonctionnelles"""
    print("\n📜 Création du script de lancement...")
    
    launcher_path = os.path.join(PROJECT_DIR, "LANCER_PORTFOLIO_FONCTIONNEL.command")
    
    launcher_content = """#!/bin/bash

# LANCEUR DU PORTFOLIO COINBASE FONCTIONNEL
# Créé automatiquement le {}

# Chemins
PROJET_DIR="/Users/johan/ia_env/bot-trading-"
TRADING_BOT_DIR="$PROJET_DIR/TradingBot_Pro_2025"
ENV_PATH="/Users/johan/ia_env/bin/activate"
DASHBOARD="$TRADING_BOT_DIR/dashboard_trading_fonctionnel.py"

# Nettoyer les processus existants
pkill -f "python.*dashboard.*\.py" >/dev/null 2>&1 || true
lsof -ti:8088 | xargs kill -9 >/dev/null 2>&1 || true
sleep 1

clear
echo "🚀 LANCEUR DE DASHBOARD AVEC CLÉS COINBASE FONCTIONNELLES"
echo "======================================================"
echo ""
echo "⏳ Préparation de l'environnement..."

# Activation environnement
cd "$TRADING_BOT_DIR"
source "$ENV_PATH" || {{
  osascript -e 'display dialog "Erreur: Environnement Python non trouvé" buttons {{"OK"}} default button "OK" with icon stop'
  exit 1
}}

# Afficher notification
osascript -e 'display notification "Démarrage du dashboard avec clés fonctionnelles" with title "TradingBot Pro" sound name "Submarine"'

# Lancer navigateur dans 4 secondes
(sleep 4 && open "http://localhost:8088") &

echo "✅ Environnement activé"
echo "📊 Lancement du dashboard avec les clés fonctionnelles..."
echo "🌐 URL: http://localhost:8088 (s'ouvrira automatiquement)"
echo ""
echo "⚠️ IMPORTANT: Cette version utilise les anciennes clés API qui"
echo "   fonctionnaient correctement, sauvegardées dans:"
echo "   $PROJET_DIR/cles_coinbase_fonctionnelles.txt"
echo ""

# Lancer le dashboard fonctionnel
python "$DASHBOARD" --full-features --portfolio-live --enable-api --debug
""".format(datetime.now().strftime('%d/%m/%Y à %H:%M'))
    
    # Écrire le contenu
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    
    # Rendre le script exécutable
    os.chmod(launcher_path, 0o755)
    
    # Copier sur le bureau
    desktop_path = os.path.expanduser("~/Desktop/LANCER_PORTFOLIO_FONCTIONNEL.command")
    shutil.copy2(launcher_path, desktop_path)
    os.chmod(desktop_path, 0o755)
    
    print(f"✅ Script de lancement créé: {launcher_path}")
    print(f"✅ Script copié sur le bureau: {desktop_path}")
    return True

def main():
    """Fonction principale"""
    print("\n🔄 RESTAURATION DES CLÉS API COINBASE FONCTIONNELLES")
    print("===================================================\n")
    
    # Vérifier si le fichier dashboard existe
    if not os.path.exists(DASHBOARD_PATH):
        print(f"❌ Erreur: Le fichier {DASHBOARD_PATH} n'existe pas!")
        return False
    
    # Créer une sauvegarde du fichier dashboard original
    create_backup(DASHBOARD_PATH)
    
    # Créer le dashboard avec les clés fonctionnelles
    if not create_working_dashboard():
        print("❌ Échec de la création du dashboard fonctionnel!")
        return False
    
    # Créer le script de lancement
    if not create_launcher_script():
        print("❌ Échec de la création du script de lancement!")
        return False
    
    print("\n✨ RESTAURATION TERMINÉE AVEC SUCCÈS ✨")
    print("Utilisez le script LANCER_PORTFOLIO_FONCTIONNEL.command")
    print("sur votre bureau pour démarrer le dashboard.")
    print("Les clés API fonctionnelles ont été sauvegardées dans:")
    print(f"{PROJECT_DIR}/cles_coinbase_fonctionnelles.txt")
    print("===================================================\n")
    return True

if __name__ == "__main__":
    main()
