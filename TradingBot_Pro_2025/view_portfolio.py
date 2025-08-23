#!/usr/bin/env python3
"""
Script simple pour voir le portefeuille Coinbase
"""

import os
from dotenv import load_dotenv
import ccxt

def main():
    load_dotenv()
    
    print("💰 Vérification du Portefeuille Coinbase")
    print("=" * 40)
    
    try:
        # Connexion Coinbase
        exchange = ccxt.coinbaseadvanced({
            'apiKey': os.getenv('COINBASE_API_KEY'),
            'secret': os.getenv('COINBASE_SECRET_KEY'),
            'enableRateLimit': True,
        })
        
        # Récupérer le balance
        balance = exchange.fetch_balance()
        
        print(f"Nombre total d'actifs: {len(balance)}")
        print()
        
        # Trouver les actifs avec solde
        actifs_positifs = []
        for asset, info in balance.items():
            if isinstance(info, dict) and info.get('total', 0) > 0:
                actifs_positifs.append((asset, info['total']))
        
        if actifs_positifs:
            print(f"Actifs avec solde positif: {len(actifs_positifs)}")
            print()
            for asset, total in actifs_positifs:
                print(f"  {asset}: {total}")
        else:
            print("Aucun actif avec solde positif")
            
        print()
        print("✅ Connexion réussie!")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    main()
