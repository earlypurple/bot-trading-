#!/usr/bin/env python3
"""
Script simple pour vérifier le portefeuille Coinbase
"""
import os
import ccxt
from dotenv import load_dotenv

def main():
    print("💰 Portefeuille Coinbase")
    print("=" * 25)
    
    load_dotenv()
    
    api_key = os.getenv('COINBASE_API_KEY')
    secret_key = os.getenv('COINBASE_SECRET_KEY')
    
    if not api_key:
        print("❌ API Key manquante")
        return
        
    print(f"🔑 API: {api_key[:8]}...")
    
    try:
        exchange = ccxt.coinbaseadvanced({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
        })
        
        balance = exchange.fetch_balance()
        print(f"✅ Connecté - {len(balance)} actifs")
        
        count = 0
        for asset, info in balance.items():
            if isinstance(info, dict) and info.get('total', 0) > 0:
                total = info.get('total', 0)
                print(f"  {asset}: {total}")
                count += 1
                
        if count == 0:
            print("  Aucun actif avec solde")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)[:50]}")

if __name__ == "__main__":
    main()
