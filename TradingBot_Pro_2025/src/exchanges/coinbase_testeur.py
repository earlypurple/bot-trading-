"""
🔧 Testeur Multiple API Coinbase - TradingBot Pro 2025
====================================================
"""

import requests
import hmac
import hashlib
import time
import json
import jwt
from cryptography.hazmat.primitives import serialization

def test_api_v2_simple(api_key):
    """Test API v2 simple avec Bearer token"""
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Test user endpoint
        resp = requests.get("https://api.coinbase.com/v2/user", headers=headers, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            user_name = data.get('data', {}).get('name', 'Unknown')
            print(f"   ✅ API v2 SUCCESS! User: {user_name}")
            return True
        else:
            print(f"   ❌ API v2 Failed: {resp.status_code} - {resp.text[:100]}")
            return False
            
    except Exception as e:
        print(f"   ❌ API v2 Error: {e}")
        return False

def test_api_hmac(api_key, secret):
    """Test authentification HMAC"""
    try:
        timestamp = str(int(time.time()))
        method = 'GET'
        path = '/v2/accounts'
        body = ''
        
        message = f"{timestamp}{method}{path}{body}"
        
        signature = hmac.new(
            secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        headers = {
            'CB-ACCESS-KEY': api_key,
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-PASSPHRASE': secret,
            'Content-Type': 'application/json'
        }
        
        resp = requests.get("https://api.coinbase.com/v2/accounts", headers=headers, timeout=10)
        
        if resp.status_code == 200:
            print(f"   ✅ HMAC SUCCESS!")
            return True
        else:
            print(f"   ❌ HMAC Failed: {resp.status_code} - {resp.text[:100]}")
            return False
            
    except Exception as e:
        print(f"   ❌ HMAC Error: {e}")
        return False

def test_api_jwt(api_key, private_key_pem):
    """Test authentification JWT pour Advanced Trade API"""
    try:
        # Charger la clé privée
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode(),
            password=None,
        )
        
        # Créer JWT token
        now = int(time.time())
        payload = {
            'sub': api_key,
            'iss': 'coinbase-cloud',
            'aud': ['public_websocket_api'],
            'exp': now + 120,
            'iat': now,
            'nbf': now
        }
        
        token = jwt.encode(payload, private_key, algorithm='ES256')
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Test Advanced Trade API
        resp = requests.get(
            "https://api.coinbase.com/api/v3/brokerage/accounts",
            headers=headers,
            timeout=10
        )
        
        if resp.status_code == 200:
            print(f"   ✅ JWT SUCCESS!")
            return True
        else:
            print(f"   ❌ JWT Failed: {resp.status_code} - {resp.text[:150]}")
            return False
            
    except Exception as e:
        print(f"   ❌ JWT Error: {e}")
        return False

def test_connector_with_keys(key1, key2):
    """Test toutes les méthodes avec 2 clés"""
    success = False
    
    print(f"   🧪 Test Bearer avec clé 1...")
    if test_api_v2_simple(key1):
        success = True
    
    print(f"   🧪 Test Bearer avec clé 2...")
    if test_api_v2_simple(key2):
        success = True
    
    print(f"   🧪 Test HMAC: key1->key2...")
    if test_api_hmac(key1, key2):
        success = True
    
    print(f"   🧪 Test HMAC: key2->key1...")
    if test_api_hmac(key2, key1):
        success = True
    
    # Test JWT seulement si une clé ressemble à une private key
    if "BEGIN EC PRIVATE KEY" in key1:
        print(f"   🧪 Test JWT: key2 avec private key1...")
        if test_api_jwt(key2, key1):
            success = True
    
    if "BEGIN EC PRIVATE KEY" in key2:
        print(f"   🧪 Test JWT: key1 avec private key2...")
        if test_api_jwt(key1, key2):
            success = True
    
    return success
