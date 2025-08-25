#!/usr/bin/env python3
"""
Vérification complète du portfolio - Toutes les cryptos
"""

import os
import sys
import ccxt
import json
from decimal import Decimal

# Configuration des clés CDP
CDP_API_KEY = "organizations/f8df9f96-f27a-4c5c-a096-0a1ee6c77c94/apiKeys/dd13e9b4-b84a-4026-8823-15f88bc5a7b6"
CDP_API_SECRET = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEILfixbR9+Y+WEPVQyaREeT5AzClpWxMBHpzbtIhfBSdeoAoGCCqGSM49\nAwEHoUQDQgAEgE7rYjuAX7hfA6S6rFAVIlvhQgLdh8mAGjCPXlY6HK6Nz7KLLZ3/\nD/7hLyqllJ2xoY2fj9HDEYd7Jz8D5I7W+w==\n-----END EC PRIVATE KEY-----\n"

def get_coinbase_exchange():
    """Initialise l'exchange Coinbase avec les clés CDP"""
    try:
        exchange = ccxt.coinbase({
            'apiKey': CDP_API_KEY,
            'secret': CDP_API_SECRET,
            'sandbox': False,
            'rateLimit': 1000,
            'enableRateLimit': True,
        })
        return exchange
    except Exception as e:
        print(f"❌ Erreur configuration Coinbase: {e}")
        return None

def check_full_portfolio():
    """Vérifie le portfolio complet avec toutes les cryptos"""
    print("🔍 VÉRIFICATION COMPLÈTE DU PORTFOLIO")
    print("=" * 50)
    
    exchange = get_coinbase_exchange()
    if not exchange:
        return
    
    try:
        # Récupération du portfolio complet
        balance = exchange.fetch_balance()
        
        total_usd = 0
        cryptos_found = []
        
        print("💰 PORTFOLIO DÉTAILLÉ:")
        print("-" * 40)
        
        for currency, amounts in balance.items():
            if currency == 'info':
                continue
                
            free = amounts.get('free', 0)
            used = amounts.get('used', 0)
            total = amounts.get('total', 0)
            
            if total > 0:
                # Récupération du prix
                try:
                    if currency == 'USD' or currency == 'USDC':
                        price = 1.0
                        usd_value = total
                    else:
                        ticker_symbol = f"{currency}/USD"
                        ticker = exchange.fetch_ticker(ticker_symbol)
                        price = ticker['last']
                        usd_value = total * price
                    
                    if usd_value > 0.001:  # Afficher même les petites positions
                        print(f"  {currency}: {total:.8f} (${usd_value:.2f}) - Prix: ${price:.4f}")
                        total_usd += usd_value
                        cryptos_found.append({
                            'currency': currency,
                            'amount': total,
                            'usd_value': usd_value,
                            'price': price
                        })
                        
                except Exception as e:
                    if total > 0.001:
                        print(f"  {currency}: {total:.8f} (Prix non disponible)")
        
        print("-" * 40)
        print(f"💰 TOTAL PORTFOLIO: ${total_usd:.2f}")
        print(f"📊 NOMBRE DE CRYPTOS: {len(cryptos_found)}")
        
        # Détails par crypto
        print("\n📋 DÉTAIL PAR CRYPTO:")
        print("-" * 40)
        for crypto in sorted(cryptos_found, key=lambda x: x['usd_value'], reverse=True):
            percentage = (crypto['usd_value'] / total_usd) * 100
            print(f"  {crypto['currency']:<6}: ${crypto['usd_value']:>7.2f} ({percentage:>5.1f}%)")
        
        # Sauvegarde des données
        portfolio_data = {
            'total_usd': total_usd,
            'cryptos': cryptos_found,
            'timestamp': str(exchange.milliseconds())
        }
        
        with open('portfolio_complet.json', 'w') as f:
            json.dump(portfolio_data, f, indent=2, default=str)
        
        print(f"\n✅ Portfolio sauvegardé dans portfolio_complet.json")
        
        # Vérification des cryptos manquantes
        if total_usd < 19:
            missing = 19 - total_usd
            print(f"\n⚠️  Il manque environ ${missing:.2f}")
            print("🔍 Vérifiez si vous avez des cryptos sur d'autres exchanges")
            print("🔍 Ou des tokens non supportés par l'API Coinbase")
        
        return total_usd, cryptos_found
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du portfolio: {e}")
        return None, []

if __name__ == "__main__":
    check_full_portfolio()
