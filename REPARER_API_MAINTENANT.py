#!/usr/bin/env python3
"""
🔧 RÉPARATION IMMÉDIATE DES CLÉS API COINBASE
Solution rapide pour Johan - nettoyage des caractères spéciaux
"""

import os
import re

def main():
    print("🔧 RÉPARATION CLÉS API COINBASE")
    print("=" * 50)
    
    # VOS CLÉS DONNÉES PAR JOHAN
    api_key = "7bb7aaf0-8571-44ee-90cb-fa485597d0e8"
    
    # Nettoyage de la clé secrète - retrait des caractères spéciaux
    secret_raw = """-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEID8hv4KFza4u5TdKTJZ756KlN0JUqwBPViMFynUyNkhRoAoGCCqGSM49\nAwEHoUQDQgAEmGfueWxK4Ie/9T5o5HAgUqISxo5+ZgXHiE6/DRVk1F9mlDQT8kIh\n/kwtdZERNu52cX1WX0Est83oxc2O4ThTTQ==\n-----END EC PRIVATE KEY-----\n"""
    
    # Méthode 1: Nettoyage complet (retire tout sauf alphanumériques et +/=)
    secret_clean = re.sub(r'[^A-Za-z0-9+/=]', '', secret_raw)
    print(f"🧹 Clé nettoyée (méthode 1): {secret_clean[:50]}...")
    
    # Méthode 2: Garde juste la partie base64
    secret_base64 = re.search(r'-----BEGIN EC PRIVATE KEY-----\n(.*?)\n-----END EC PRIVATE KEY-----', secret_raw.replace('\\n', '\n'), re.DOTALL)
    if secret_base64:
        secret_content = secret_base64.group(1).replace('\n', '').replace('\\n', '')
        print(f"🎯 Clé base64 pure: {secret_content[:50]}...")
    else:
        secret_content = secret_clean
    
    # Méthode 3: Garde le format PEM mais nettoie
    secret_pem = secret_raw.replace('\\n', '\n')
    print(f"📝 Clé PEM formatée: {secret_pem[:80].replace(chr(10), ' ')}...")
    
    # Test avec les 3 versions
    print("\n🧪 TEST DES 3 VERSIONS DE CLÉS...")
    
    try:
        import ccxt
        
        # Version 1: Clé complètement nettoyée
        print("\n1️⃣ Test clé nettoyée complète...")
        try:
            exchange1 = ccxt.coinbase({
                'apiKey': api_key,
                'secret': secret_clean,
                'sandbox': False,
                'enableRateLimit': True,
            })
            balance1 = exchange1.fetch_balance()
            print("✅ VERSION 1 FONCTIONNE!")
            save_working_config(api_key, secret_clean, "nettoyée")
            return
        except Exception as e:
            print(f"❌ Version 1 échoue: {str(e)[:100]}")
        
        # Version 2: Base64 pur
        print("\n2️⃣ Test base64 pur...")
        try:
            exchange2 = ccxt.coinbase({
                'apiKey': api_key,
                'secret': secret_content,
                'sandbox': False,
                'enableRateLimit': True,
            })
            balance2 = exchange2.fetch_balance()
            print("✅ VERSION 2 FONCTIONNE!")
            save_working_config(api_key, secret_content, "base64")
            return
        except Exception as e:
            print(f"❌ Version 2 échoue: {str(e)[:100]}")
        
        # Version 3: PEM formaté
        print("\n3️⃣ Test PEM formaté...")
        try:
            exchange3 = ccxt.coinbase({
                'apiKey': api_key,
                'secret': secret_pem,
                'sandbox': False,
                'enableRateLimit': True,
            })
            balance3 = exchange3.fetch_balance()
            print("✅ VERSION 3 FONCTIONNE!")
            save_working_config(api_key, secret_pem, "PEM")
            return
        except Exception as e:
            print(f"❌ Version 3 échoue: {str(e)[:100]}")
        
        # Version 4: Clé brute sans modification
        print("\n4️⃣ Test clé brute...")
        try:
            exchange4 = ccxt.coinbase({
                'apiKey': api_key,
                'secret': secret_raw,
                'sandbox': False,
                'enableRateLimit': True,
            })
            balance4 = exchange4.fetch_balance()
            print("✅ VERSION 4 FONCTIONNE!")
            save_working_config(api_key, secret_raw, "brute")
            return
        except Exception as e:
            print(f"❌ Version 4 échoue: {str(e)[:100]}")
            
        print("\n💡 ESSAI AVEC COINBASEADVANCED...")
        # Test avec coinbaseadvanced
        try:
            exchange_adv = ccxt.coinbaseadvanced({
                'apiKey': api_key,
                'secret': secret_clean,
                'sandbox': False,
                'enableRateLimit': True,
            })
            balance_adv = exchange_adv.fetch_balance()
            print("✅ COINBASEADVANCED FONCTIONNE!")
            save_working_config(api_key, secret_clean, "advanced")
            return
        except Exception as e:
            print(f"❌ CoinbaseAdvanced échoue: {str(e)[:100]}")
        
    except ImportError:
        print("❌ Erreur: ccxt non installé")
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
    
    print("\n❌ AUCUNE VERSION NE FONCTIONNE")
    print("💡 Les clés peuvent être invalides ou inactives")

def save_working_config(api_key, secret, version):
    """Sauvegarde la configuration qui fonctionne"""
    config_content = f'''# Configuration API Coinbase FONCTIONNELLE
# Version qui marche: {version}

API_CONFIG = {{
    'coinbase_api_key': '{api_key}',
    'coinbase_api_secret': '{secret}',
}}

print("🎉 Configuration {version} chargée avec succès!")
'''
    
    # Sauvegarde dans plusieurs fichiers
    files = [
        'CONFIGURER_API_COINBASE.py',
        '/Users/johan/ia_env/bot-trading-/CONFIGURER_API_COINBASE.py',
        '/Users/johan/ia_env/bot-trading-/TradingBot_Pro_2025/CONFIGURER_API_COINBASE.py'
    ]
    
    for file_path in files:
        try:
            with open(file_path, 'w') as f:
                f.write(config_content)
            print(f"✅ Sauvegardé: {file_path}")
        except:
            pass
    
    print(f"\n🎯 CONFIGURATION {version.upper()} SAUVEGARDÉE!")
    print("🚀 Vous pouvez maintenant lancer le dashboard!")

if __name__ == "__main__":
    main()
