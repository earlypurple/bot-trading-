#!/usr/bin/env python3
"""
Diagnostic complet pour résoudre l'erreur "account is not available" sur Coinbase Advanced Trade
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config'))

import ccxt
from config.api_config import API_CONFIG

# Récupérer les credentials depuis la config
COINBASE_API_KEY = API_CONFIG['coinbase_api_key']
COINBASE_API_SECRET = API_CONFIG['coinbase_api_secret']
COINBASE_PASSPHRASE = API_CONFIG['coinbase_passphrase']

def diagnostic_complet():
    """Diagnostic complet des comptes et permissions de trading"""
    print("🔍 DIAGNOSTIC COMPLET - COINBASE ADVANCED TRADE")
    print("=" * 70)
    
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
        
        # 1. ANALYSE DES COMPTES ET PORTEFEUILLES
        print("\n1️⃣  ANALYSE DES COMPTES")
        print("-" * 50)
        
        accounts = exchange.fetch_accounts()
        print(f"   Total comptes trouvés: {len(accounts)}")
        
        # Analyser chaque compte
        primary_accounts = []
        trading_accounts = []
        vault_accounts = []
        
        for i, acc in enumerate(accounts):
            currency = acc.get('currency', 'N/A')
            balance = float(acc.get('balance', 0))
            available = float(acc.get('available', 0))
            account_id = acc.get('id', 'N/A')
            account_type = acc.get('type', 'Unknown')
            
            # Identifier le type de compte
            if 'vault' in account_type.lower():
                vault_accounts.append(acc)
            elif balance > 0 or available > 0:
                if 'primary' in account_type.lower() or account_type == 'trading':
                    primary_accounts.append(acc)
                    trading_accounts.append(acc)
                else:
                    trading_accounts.append(acc)
            
            if i < 20:  # Afficher les 20 premiers
                print(f"   [{i+1:2}] {currency:8} | Balance: {balance:12.8f} | Dispo: {available:12.8f} | Type: {account_type:15} | ID: {account_id[:8]}...")
        
        print(f"\n   📊 Résumé:")
        print(f"      Comptes primaires: {len(primary_accounts)}")
        print(f"      Comptes trading: {len(trading_accounts)}")
        print(f"      Comptes vault: {len(vault_accounts)}")
        
        # 2. IDENTIFIER LE COMPTE PRINCIPAL POUR TRADING
        print("\n2️⃣  IDENTIFICATION DU COMPTE PRINCIPAL DE TRADING")
        print("-" * 50)
        
        # Chercher le compte USD principal
        usd_accounts = [acc for acc in accounts if acc.get('currency') == 'USD']
        usdc_accounts = [acc for acc in accounts if acc.get('currency') == 'USDC']
        
        print(f"   Comptes USD trouvés: {len(usd_accounts)}")
        print(f"   Comptes USDC trouvés: {len(usdc_accounts)}")
        
        # Analyser les comptes USD/USDC
        main_usd_account = None
        main_usdc_account = None
        
        for acc in usd_accounts:
            account_type = acc.get('type', '')
            balance = float(acc.get('balance', 0))
            if 'primary' in account_type.lower() or balance > 0:
                main_usd_account = acc
                print(f"   🎯 Compte USD principal trouvé: {acc.get('id', 'N/A')[:12]}... | Balance: ${balance:.2f}")
                break
        
        for acc in usdc_accounts:
            account_type = acc.get('type', '')
            balance = float(acc.get('balance', 0))
            if 'primary' in account_type.lower() or balance > 0:
                main_usdc_account = acc
                print(f"   🎯 Compte USDC principal trouvé: {acc.get('id', 'N/A')[:12]}... | Balance: {balance:.2f} USDC")
                break
        
        # 3. TESTER LES PAIRES DE TRADING SUPPORTÉES
        print("\n3️⃣  VÉRIFICATION DES PAIRES DE TRADING")
        print("-" * 50)
        
        markets = exchange.load_markets()
        
        # Paires importantes à tester
        test_pairs = ['BTC/USD', 'ETH/USD', 'SOL/USD', 'BTC/USDC', 'ETH/USDC', 'SOL/USDC']
        supported_pairs = []
        
        for pair in test_pairs:
            if pair in markets:
                market = markets[pair]
                active = market.get('active', False)
                supported_pairs.append(pair)
                print(f"   ✅ {pair:10} | Actif: {active} | Limites: {market.get('limits', {}).get('amount', {}).get('min', 'N/A')}")
            else:
                print(f"   ❌ {pair:10} | Non supporté")
        
        # 4. TEST DES PERMISSIONS DE TRADING
        print("\n4️⃣  TEST DES PERMISSIONS DE TRADING")
        print("-" * 50)
        
        # Chercher un compte avec ETH pour tester
        eth_account = None
        for acc in accounts:
            if acc.get('currency') == 'ETH' and float(acc.get('available', 0)) > 0.001:
                eth_account = acc
                break
        
        if eth_account:
            eth_balance = float(eth_account.get('available', 0))
            eth_account_id = eth_account.get('id')
            print(f"   💎 Compte ETH trouvé: {eth_balance:.6f} ETH disponible")
            print(f"   📝 Account ID: {eth_account_id}")
            
            # Test avec ETH/USD
            if 'ETH/USD' in supported_pairs:
                print(f"\n   🧪 Test d'ordre ETH/USD...")
                try:
                    ticker = exchange.fetch_ticker('ETH/USD')
                    current_price = ticker['last']
                    
                    # Quantité très petite pour test
                    test_quantity = 0.001  # 0.001 ETH
                    test_value = test_quantity * current_price
                    
                    print(f"      Prix ETH actuel: ${current_price:.2f}")
                    print(f"      Quantité test: {test_quantity} ETH (≈${test_value:.2f})")
                    
                    # Essayer de créer un ordre de vente au marché
                    order_params = {}
                    if eth_account_id:
                        order_params['account_id'] = eth_account_id
                    
                    print(f"      Paramètres: {order_params}")
                    
                    # IMPORTANT: Ne pas exécuter réellement, juste préparer
                    print(f"      ⚠️  Test en mode simulation (pas d'ordre réel)")
                    print(f"      💡 Commande qui serait exécutée:")
                    print(f"         exchange.create_market_sell_order('ETH/USD', {test_quantity}, None, None, {order_params})")
                    
                except Exception as e:
                    print(f"      ❌ Erreur lors du test: {e}")
            
            # Test avec ETH/USDC si USD ne marche pas
            if 'ETH/USDC' in supported_pairs:
                print(f"\n   🧪 Test d'ordre ETH/USDC...")
                try:
                    ticker = exchange.fetch_ticker('ETH/USDC')
                    current_price = ticker['last']
                    
                    test_quantity = 0.001  # 0.001 ETH
                    test_value = test_quantity * current_price
                    
                    print(f"      Prix ETH actuel: {current_price:.2f} USDC")
                    print(f"      Quantité test: {test_quantity} ETH (≈{test_value:.2f} USDC)")
                    print(f"      💡 ETH/USDC pourrait être plus compatible que ETH/USD")
                    
                except Exception as e:
                    print(f"      ❌ Erreur lors du test ETH/USDC: {e}")
        else:
            print("   ⚠️  Pas de compte ETH avec balance suffisante pour test")
        
        # 5. RECOMMANDATIONS
        print("\n5️⃣  RECOMMANDATIONS POUR RÉSOUDRE LE PROBLÈME")
        print("-" * 50)
        
        print("   🔧 Actions recommandées:")
        
        if main_usd_account:
            print(f"      1. ✅ Utiliser le compte USD principal: {main_usd_account.get('id', 'N/A')[:12]}...")
        elif main_usdc_account:
            print(f"      1. 💡 Utiliser USDC au lieu d'USD: {main_usdc_account.get('id', 'N/A')[:12]}...")
            print(f"         Remplacer BTC/USD par BTC/USDC, ETH/USD par ETH/USDC")
        else:
            print("      1. ⚠️  Aucun compte USD/USDC principal trouvé")
        
        if 'ETH/USDC' in supported_pairs and 'BTC/USDC' in supported_pairs:
            print("      2. ✅ Utiliser les paires USDC (ETH/USDC, BTC/USDC, SOL/USDC)")
        
        if eth_account:
            print(f"      3. ✅ Account ID à utiliser pour ETH: {eth_account.get('id')}")
        
        print("      4. 💡 Modifications du code bot:")
        print("         - Remplacer 'BTC/USD' par 'BTC/USDC'")
        print("         - Remplacer 'ETH/USD' par 'ETH/USDC'")
        print("         - Remplacer 'SOL/USD' par 'SOL/USDC'")
        print("         - Ajouter account_id dans les paramètres d'ordre")
        
        print("\n   📋 Code à modifier dans le bot:")
        print("      exchange.create_market_sell_order(")
        print("          'ETH/USDC',  # Au lieu de ETH/USD")
        print("          quantity,")
        print("          None,")
        print("          None,")
        print(f"          {{'account_id': '{eth_account.get('id') if eth_account else 'ACCOUNT_ID'}'}})")
        print("      )")
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnostic_complet()
