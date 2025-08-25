#!/usr/bin/env python3
"""
Configuration pour les nouvelles clés API Coinbase Developer Platform (CDP)
Remplace les anciennes clés de coinbase.com/settings/api
"""

# ANCIENNES CLÉS (coinbase.com/settings/api) - NE MARCHENT PLUS AVEC v3
OLD_API_CONFIG = {
    'coinbase_api_key': '7bb7aaf0-8571-44ee-90cb-fa485597d0e8',
    'coinbase_api_secret': '''-----BEGIN EC PRIVATE KEY-----
MHcCAQEEID8hv4KFza4u5TdKTJZ756KlN0JUqwBPViMFynUyNkhRoAoGCCqGSM49
AwEHoUQDQgAEmGfueWxK4Ie/9T5o5HAgUqISxo5+ZgXHiE6/DRVk1F9mlDQT8kIh
/kwtdZERNu52cX1WX0Est83oxc2O4ThTTQ==
-----END EC PRIVATE KEY-----''',
    'coinbase_passphrase': '2c94fd0aa6a13b2f7444a369282a09f51281c9b705e120c61a1a3ed58702e5a7',
}

# NOUVELLES CLÉS CDP (portal.cdp.coinbase.com) - À COMPLÉTER
NEW_CDP_CONFIG = {
    # Format CDP 2025 pour Advanced Trade v3
    'name': 'EarlyBotTrading',  # Nom du projet/app sur CDP
    'private_key': '''-----BEGIN EC PRIVATE KEY-----
[VOTRE_NOUVELLE_CLE_PRIVEE_PEM_ICI]
-----END EC PRIVATE KEY-----''',
    'organization_id': '[VOTRE_ORGANIZATION_ID]',  # Depuis le portail CDP
    'project_id': '[VOTRE_PROJECT_ID]',            # Depuis le portail CDP
    
    # Alternative : si vous utilisez encore le format API Key
    'api_key': '[NOUVELLE_API_KEY_CDP]',
    'api_secret': '''-----BEGIN EC PRIVATE KEY-----
[NOUVELLE_CLE_SECRETE_PEM]
-----END EC PRIVATE KEY-----''',
    'passphrase': '[NOUVELLE_PASSPHRASE]'
}

def get_cdp_config():
    """
    Instructions pour obtenir les nouvelles clés CDP :
    
    1. Aller sur https://portal.cdp.coinbase.com
    2. Créer un nouveau projet (ex: "EarlyBotTrading") 
    3. Aller dans "API Keys"
    4. Cliquer "Create API Key"
    5. Sélectionner les permissions :
       ✅ wallet:addresses:read
       ✅ wallet:transactions:read  
       ✅ wallet:transactions:send
       ✅ wallet:user:read
       ✅ Advanced Trade (si disponible)
    6. Télécharger le fichier JSON
    7. Copier les valeurs ici
    """
    return NEW_CDP_CONFIG

def test_new_keys():
    """Test des nouvelles clés CDP une fois configurées"""
    import ccxt
    
    # Configuration selon le nouveau format CDP
    if NEW_CDP_CONFIG['private_key'] != '[VOTRE_NOUVELLE_CLE_PRIVEE_PEM_ICI]':
        try:
            # Test avec le nouveau format CDP
            exchange = ccxt.coinbase({
                'apiKey': NEW_CDP_CONFIG.get('api_key', ''),
                'secret': NEW_CDP_CONFIG.get('private_key', ''),
                'password': NEW_CDP_CONFIG.get('passphrase', ''),
                'sandbox': False,
                'enableRateLimit': True,
            })
            
            print("🔧 Test avec nouvelles clés CDP...")
            
            # Test de connexion
            balance = exchange.fetch_balance()
            print("✅ CONNEXION RÉUSSIE avec les nouvelles clés CDP !")
            print(f"✅ Portfolio détecté !")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur avec nouvelles clés: {e}")
            return False
    else:
        print("⚠️  Veuillez d'abord configurer les nouvelles clés CDP dans ce fichier")
        return False

if __name__ == "__main__":
    print("🔐 CONFIGURATION NOUVELLES CLÉS API COINBASE CDP")
    print("=" * 60)
    print()
    print("📋 ÉTAPES À SUIVRE :")
    print("1. Aller sur https://portal.cdp.coinbase.com")
    print("2. Créer un nouveau projet/app")
    print("3. Générer des clés API Advanced Trade")
    print("4. Télécharger le fichier JSON avec privateKey")
    print("5. Remplacer les valeurs dans NEW_CDP_CONFIG ci-dessus")
    print("6. Relancer ce script pour tester")
    print()
    print("💡 Les anciennes clés de coinbase.com/settings/api ne marchent plus !")
    print("💡 Seules les clés du Developer Platform (CDP) fonctionnent avec v3")
    print()
    
    test_new_keys()
