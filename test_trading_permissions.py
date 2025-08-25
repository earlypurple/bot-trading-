#!/usr/bin/env python3
"""
Script pour tester les permissions de trading sur Coinbase Advanced Trade
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import ccxt
from config import COINBASE_API_KEY, COINBASE_API_SECRET, COINBASE_PASSPHRASE

def test_trading_permissions():
    """Test des permissions de trading"""
    print("🔍 TEST DES PERMISSIONS DE TRADING COINBASE ADVANCED")
    print("=" * 60)
    
    try:
        # Configuration Coinbase Advanced Trade
        exchange = ccxt.coinbaseadvanced({
            'apiKey': COINBASE_API_KEY,
            'secret': COINBASE_API_SECRET,
            'password': COINBASE_PASSPHRASE,
            'sandbox': False,
            'rateLimit': 1000,
            'enableRateLimit': True,
        })
        
        print("✅ Exchange configuré avec Coinbase Advanced Trade")
        
        # Test 1: Vérifier les comptes
        print("\n1. Test des comptes...")
        accounts = exchange.fetch_accounts()
        print(f"   Nombre de comptes: {len(accounts)}")
        
        # Trouver les comptes avec des balances
        accounts_with_balance = [acc for acc in accounts if float(acc.get('balance', 0)) > 0]
        print(f"   Comptes avec balance: {len(accounts_with_balance)}")
        
        for acc in accounts_with_balance[:5]:  # Top 5
            currency = acc.get('currency', 'N/A')
            balance = float(acc.get('balance', 0))
            available = float(acc.get('available', 0))
            print(f"   - {currency}: Balance={balance:.8f}, Disponible={available:.8f}")
        
        # Test 2: Vérifier les permissions de l'API
        print("\n2. Test des permissions API...")
        try:
            # Tester une requête qui nécessite des permissions de trading
            trading_fees = exchange.fetch_trading_fees()
            print("   ✅ Permissions de lecture OK")
        except Exception as e:
            print(f"   ❌ Erreur permissions: {e}")
        
        # Test 3: Vérifier si on peut créer un ordre test (très petit montant)
        print("\n3. Test d'ordre minimal...")
        
        # Trouver ETH account
        eth_account = None
        for acc in accounts:
            if acc.get('currency') == 'ETH' and float(acc.get('available', 0)) > 0:
                eth_account = acc
                break
        
        if eth_account:
            available_eth = float(eth_account.get('available', 0))
            print(f"   ETH disponible: {available_eth:.8f}")
            
            if available_eth > 0.0001:  # Si on a plus de 0.0001 ETH
                try:
                    # Essayer de créer un ordre de vente très petit
                    print("   Tentative d'ordre test...")
                    
                    # Récupérer le prix actuel
                    ticker = exchange.fetch_ticker('ETH/USD')
                    current_price = ticker['last']
                    
                    # Quantité minimale (très petit montant)
                    quantity = 0.00001  # 0.00001 ETH
                    
                    print(f"   Prix ETH: ${current_price:.2f}")
                    print(f"   Quantité test: {quantity} ETH")
                    
                    # Créer ordre de vente au prix du marché
                    order = exchange.create_market_sell_order('ETH/USD', quantity)
                    print(f"   ✅ ORDRE CRÉÉ AVEC SUCCÈS: {order.get('id')}")
                    print(f"   Status: {order.get('status')}")
                    
                    # Annuler immédiatement si possible
                    try:
                        exchange.cancel_order(order.get('id'), 'ETH/USD')
                        print("   Ordre annulé")
                    except:
                        print("   Ordre probablement exécuté (marché)")
                    
                except Exception as e:
                    print(f"   ❌ ERREUR TRADING: {e}")
                    if "account is not available" in str(e):
                        print("   🚨 PROBLÈME: Compte non autorisé pour le trading")
                        print("   💡 SOLUTION: Vérifier les permissions de l'API sur Coinbase")
                    elif "insufficient" in str(e).lower():
                        print("   ⚠️  Balance insuffisante")
                    else:
                        print(f"   Erreur inconnue: {e}")
            else:
                print("   ⚠️  Balance ETH insuffisante pour test")
        else:
            print("   ⚠️  Pas de compte ETH trouvé")
        
        # Test 4: Vérifier les markets supportés
        print("\n4. Test des marchés...")
        markets = exchange.load_markets()
        active_markets = [symbol for symbol, market in markets.items() if market.get('active', False)]
        print(f"   Marchés actifs: {len(active_markets)}")
        print(f"   Exemples: {', '.join(active_markets[:10])}")
        
        # Test 5: Informations sur les limites
        print("\n5. Informations sur les limites...")
        eth_market = markets.get('ETH/USD')
        if eth_market:
            limits = eth_market.get('limits', {})
            amount_limits = limits.get('amount', {})
            cost_limits = limits.get('cost', {})
            print(f"   ETH/USD - Montant min: {amount_limits.get('min', 'N/A')}")
            print(f"   ETH/USD - Coût min: ${cost_limits.get('min', 'N/A')}")
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_trading_permissions()
