#!/usr/bin/env python3
"""
Script de test pour l'API portefeuille.
"""

import ccxt
import os
from dotenv import load_dotenv

def test_coinbase_connection():
    """Test direct de la connexion Coinbase."""
    print("=== Test de la connexion Coinbase ===")
    
    # Charger les variables d'environnement
    load_dotenv()
    
    api_key = os.getenv('COINBASE_API_KEY')
    secret_key = os.getenv('COINBASE_SECRET_KEY')
    
    print(f"API Key présente: {'Oui' if api_key else 'Non'}")
    print(f"Secret Key présente: {'Oui' if secret_key else 'Non'}")
    
    if not api_key or not secret_key:
        print("❌ Clés API manquantes")
        return False
    
    try:
        # Connexion à Coinbase
        exchange = ccxt.coinbaseadvanced({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
        })
        
        print("✅ Connexion Coinbase créée")
        
        # Test du balance
        print("🔄 Récupération du balance...")
        balance = exchange.fetch_balance()
        
        print(f"✅ Balance récupéré: {len(balance)} entrées")
        
        # Traiter les données
        assets = []
        total_value = 0
        
        for asset, info in balance.items():
            if isinstance(info, dict) and info.get('total', 0) > 0:
                total = info.get('total', 0)
                free = info.get('free', 0)
                used = info.get('used', 0)
                
                assets.append({
                    "symbol": asset,
                    "balance": total,
                    "available": free,
                    "locked": used,
                })
                
                print(f"  - {asset}: {total}")
                
                # Calculer la valeur totale (approximative)
                if asset in ['EUR', 'USD']:
                    total_value += total
        
        print(f"\n✅ Total des actifs trouvés: {len(assets)}")
        print(f"✅ Valeur totale (EUR/USD): {total_value:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

if __name__ == "__main__":
    test_coinbase_connection()
