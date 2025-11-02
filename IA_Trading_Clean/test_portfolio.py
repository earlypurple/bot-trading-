#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide du portfolio Coinbase
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import ccxt
from config.api_config import API_CONFIG

def test_portfolio():
    """Test direct du portfolio"""
    print("🔍 TEST PORTFOLIO COINBASE")
    print("=" * 50)
    
    try:
        # Configuration exchange
        exchange = ccxt.coinbase({
            'apiKey': API_CONFIG['coinbase_api_key'],
            'secret': API_CONFIG['coinbase_private_key'],
            'sandbox': API_CONFIG['sandbox'],
            'enableRateLimit': True,
        })
        
        print("✅ Exchange configuré")
        
        # Test balance
        print("\n📊 Récupération du balance...")
        balance = exchange.fetch_balance()
        
        print("\n💰 PORTFOLIO DÉTAILLÉ:")
        print("-" * 60)
        
        total_usd = 0.0
        asset_count = 0
        
        for currency, amounts in balance.items():
            if currency not in ['info', 'free', 'used', 'total'] and amounts.get('total', 0) > 0:
                total = amounts.get('total', 0)
                free = amounts.get('free', 0)
                used = amounts.get('used', 0)
                
                asset_count += 1
                
                # Calcul valeur USD
                usd_value = 0.0
                if currency == 'USD':
                    usd_value = total
                    total_usd += usd_value
                    print(f"💵 {currency:>8}: {total:>15.8f} | Libre: {free:>12.8f} | ${usd_value:>10.2f}")
                else:
                    try:
                        ticker = exchange.fetch_ticker(f"{currency}/USD")
                        usd_value = total * ticker['last']
                        total_usd += usd_value
                        print(f"🪙 {currency:>8}: {total:>15.8f} | Libre: {free:>12.8f} | ${usd_value:>10.2f}")
                    except Exception as e:
                        print(f"❌ {currency:>8}: {total:>15.8f} | Libre: {free:>12.8f} | Prix indisponible")
        
        print("-" * 60)
        print(f"📊 TOTAL ASSETS: {asset_count}")
        print(f"💰 VALEUR TOTALE: ${total_usd:.2f}")
        print("-" * 60)
        
        if asset_count == 0:
            print("⚠️  AUCUN ASSET DÉTECTÉ")
            print("   Vérifiez:")
            print("   - Les permissions API")
            print("   - Que vous êtes sur le bon compte")
            print("   - Que les cryptos sont bien sur Coinbase Pro/Advanced")
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        print("\nVérifications à faire:")
        print("- Clés API correctes")
        print("- Permissions 'view' activées")
        print("- Compte Coinbase Pro/Advanced")

if __name__ == '__main__':
    test_portfolio()
