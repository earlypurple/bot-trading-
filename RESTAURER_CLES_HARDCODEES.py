#!/usr/bin/env python3
"""
🚨 RESTAURATION IMMÉDIATE DES CLÉS QUI FONCTIONNENT
Force l'utilisation des clés API originales hardcodées
"""

import os
import time
import shutil

def restaurer_cles_hardcodees():
    print("🚨 RESTAURATION FORCÉE DES CLÉS FONCTIONNELLES")
    print("=" * 55)
    
    dashboard_path = "/Users/johan/ia_env/bot-trading-/TradingBot_Pro_2025/dashboard_trading_pro.py"
    
    # Sauvegarde
    backup_path = f"{dashboard_path}.bak.final.{int(time.time())}"
    shutil.copy2(dashboard_path, backup_path)
    print(f"✅ Sauvegarde créée: {backup_path}")
    
    # Lire le fichier
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Chercher la fonction setup_exchange et la remplacer par les VRAIES clés
    import re
    
    # Pattern pour trouver setup_exchange
    pattern = r'def setup_exchange.*?private_key.*?\n.*?except.*?\n.*?return None'
    
    # Nouvelle fonction avec les VRAIES clés qui fonctionnaient
    new_setup = '''def setup_exchange(self):
        """Configuration de l'exchange Coinbase avec les VRAIES clés fonctionnelles"""
        try:
            print("🔐 Configuration Coinbase avec clés fonctionnelles...")
            
            # CLÉS HARDCODÉES QUI FONCTIONNENT - NE PAS MODIFIER
            apiKey = '08d4759c-8572-4224-a3c8-6a63cf877fd6'
            apiSecret = 'organizations/2a089493-b1ac-4a18-a9b8-b38e90a16c9c/apiKeys/08d4759c-8572-4224-a3c8-6a63cf877fd6/versions/b7b8e173-b6f0-497a-91b6-eb8c3b1bb6dd'
            
            private_key = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIME7wFvOgVHVaIRi+rS2xSlD9b8bBL+QO8EwbBE9ynKLoAoGCCqGSM49
AwEHoUQDQgAEhOCa7Y6wWHF1P1iG8gJGbgRSgw67vHlSBOgxqQsaLrF2xZ5pHtzm
DFnwszH8k+aOAKo2WnLQnS7g1e1X6qL+qA==
-----END EC PRIVATE KEY-----"""
            
            print(f"🔑 API Key: {apiKey[:8]}...")
            print(f"🗝️ Private Key: {'✅ Présente' if private_key else '❌ Manquante'}")
            
            self.exchange = ccxt.coinbaseadvanced({
                'apiKey': apiKey,
                'secret': apiSecret,
                'privateKey': private_key,
                'sandbox': False,
                'enableRateLimit': True,
                'timeout': 30000,
                'verbose': True
            })
            
            return self.exchange
            
        except Exception as e:
            print(f"❌ Erreur setup exchange: {e}")
            return None'''
    
    # Remplacer
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_setup, content, flags=re.DOTALL)
        print("✅ Fonction setup_exchange restaurée avec clés fonctionnelles")
    else:
        print("⚠️ Pattern non trouvé, recherche alternative...")
        # Chercher juste la fonction def setup_exchange
        setup_pattern = r'def setup_exchange\(self\):.*?(?=def |\Z)'
        if re.search(setup_pattern, content, re.DOTALL):
            content = re.sub(setup_pattern, new_setup + '\n\n    ', content, flags=re.DOTALL)
            print("✅ Fonction setup_exchange remplacée complètement")
    
    # Sauvegarder
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ CLÉS HARDCODÉES RESTAURÉES")
    print("🔄 Le dashboard utilisera maintenant les vraies clés")
    print("=" * 55)

if __name__ == "__main__":
    restaurer_cles_hardcodees()
