#!/usr/bin/env python3
"""
🎯 CONNECTOR ADVANCED TRADE COINBASE
Authentification spécifique pour les clés Advanced Trade
"""

import jwt
import time
import requests
from cryptography.hazmat.primitives import serialization
import json

class CoinbaseAdvancedTradeConnector:
    """Connector spécialisé pour Coinbase Advanced Trade API"""
    
    def __init__(self, api_key, private_key_pem):
        self.api_key = api_key
        self.private_key = serialization.load_pem_private_key(
            private_key_pem.encode('utf-8'),
            password=None
        )
        self.base_url = "https://api.coinbase.com"
        
    def create_jwt_token(self, request_method="GET", request_path="/api/v3/brokerage/accounts"):
        """Créer un token JWT spécifique pour Advanced Trade"""
        
        # Header JWT pour Advanced Trade
        header = {
            "alg": "ES256",
            "kid": self.api_key,
            "typ": "JWT",
            "nonce": str(int(time.time() * 1000))  # Nonce requis pour Advanced Trade
        }
        
        # Payload JWT pour Advanced Trade
        current_time = int(time.time())
        payload = {
            "sub": self.api_key,
            "iss": "cdp",  # Coinbase Developer Platform
            "aud": ["public"],
            "iat": current_time,
            "exp": current_time + 120,
            "nbf": current_time,
            "uri": request_method + " " + self.base_url + request_path
        }
        
        return jwt.encode(payload, self.private_key, algorithm="ES256", headers=header)
    
    def make_authenticated_request(self, method="GET", endpoint="/api/v3/brokerage/accounts", data=None):
        """Faire une requête authentifiée Advanced Trade"""
        
        full_path = endpoint
        token = self.create_jwt_token(method, full_path)
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "TradingBot-Pro-AdvancedTrade/1.0"
        }
        
        url = self.base_url + endpoint
        
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=15)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=15)
        else:
            raise ValueError(f"Méthode non supportée: {method}")
            
        return response
    
    def test_connection(self):
        """Test de connexion Advanced Trade"""
        print("🎯 TEST CONNEXION ADVANCED TRADE")
        print("=" * 50)
        
        # Test des endpoints Advanced Trade
        tests = [
            ("👤 User Profile", "/api/v3/brokerage/user"),
            ("💰 Accounts", "/api/v3/brokerage/accounts"), 
            ("📊 Products", "/api/v3/brokerage/products"),
            ("💼 Portfolios", "/api/v3/brokerage/portfolios"),
        ]
        
        success_count = 0
        
        for name, endpoint in tests:
            print(f"\n🧪 {name}")
            print("-" * 30)
            
            try:
                response = self.make_authenticated_request("GET", endpoint)
                status = response.status_code
                
                print(f"📊 Status: {status}")
                
                if status == 200:
                    print("✅ SUCCÈS!")
                    success_count += 1
                    
                    try:
                        data = response.json()
                        if 'accounts' in data:
                            accounts = data['accounts']
                            print(f"💰 Comptes: {len(accounts)}")
                            
                            # Calculer valeur totale
                            total_value = 0
                            active_balances = []
                            
                            for account in accounts:
                                currency = account.get('currency', 'N/A')
                                available = float(account.get('available_balance', {}).get('value', '0'))
                                hold = float(account.get('hold', {}).get('value', '0'))
                                
                                if available > 0 or hold > 0:
                                    balance_total = available + hold
                                    active_balances.append(f"{currency}: {balance_total:.8f}")
                                    
                                    if currency in ['USD', 'EUR']:
                                        total_value += balance_total
                            
                            print(f"💵 Valeur fiat: ${total_value:.2f}")
                            print(f"🪙 Cryptos actives: {len([b for b in active_balances if not any(fiat in b for fiat in ['USD', 'EUR'])])}")
                            
                            # Afficher top 3 balances
                            if active_balances:
                                print("📈 Top balances:")
                                for balance in active_balances[:3]:
                                    print(f"   • {balance}")
                                    
                        elif 'products' in data:
                            products = data['products']
                            print(f"📊 Produits: {len(products)}")
                            
                            # Compter par type
                            spot_count = len([p for p in products if p.get('product_type') == 'SPOT'])
                            print(f"   • SPOT: {spot_count}")
                            
                        elif 'portfolios' in data:
                            portfolios = data['portfolios']
                            print(f"💼 Portfolios: {len(portfolios)}")
                            
                        elif 'user' in data:
                            user = data['user']
                            user_id = user.get('id', 'N/A')
                            print(f"👤 User ID: {user_id[:8]}...")
                            
                    except Exception as e:
                        print(f"⚠️ Erreur parsing: {e}")
                        print("✅ Mais la connexion fonctionne!")
                        
                elif status == 401:
                    print("❌ 401 Unauthorized")
                    try:
                        error_data = response.json()
                        error_msg = error_data.get('error', {}).get('message', 'No details')
                        print(f"💬 Détail: {error_msg}")
                    except:
                        print("💬 Pas de détails d'erreur")
                        
                elif status == 403:
                    print("❌ 403 Forbidden - Permissions insuffisantes")
                    
                else:
                    print(f"⚠️ Code inhabituel: {status}")
                    try:
                        print(f"📝 Réponse: {response.text[:100]}...")
                    except:
                        pass
                        
            except Exception as e:
                print(f"💥 Erreur: {str(e)}")
        
        # Résumé
        print(f"\n{'='*50}")
        print(f"🎯 RÉSULTAT: {success_count}/{len(tests)} endpoints fonctionnels")
        
        if success_count == len(tests):
            print("🎉 CONNEXION ADVANCED TRADE RÉUSSIE!")
            print("✅ Toutes les fonctionnalités disponibles")
            return True
        elif success_count > 0:
            print("⚠️ CONNEXION PARTIELLE")
            print("💡 Certains endpoints fonctionnent")
            return True
        else:
            print("❌ ÉCHEC TOTAL")
            print("🔧 Vérifier la configuration")
            return False

def test_advanced_trade():
    """Test avec les vraies clés Advanced Trade"""
    
    print("🚀 TEST COINBASE ADVANCED TRADE")
    print("=" * 60)
    print("🎯 Utilisation des endpoints et auth spécifiques Advanced Trade")
    print("=" * 60)
    
    # Tes clés Advanced Trade
    api_key = "03c9938e-5795-4c66-93e4-6fdef834fdbd"
    private_key_pem = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEICQbrYDGTcR56Mw4zCVSujiVx3aClJChDHUEvyEbFjWAoAoGCCqGSM49
AwEHoUQDQgAEUCeFPnFXlOfalPtq8nFKMpVVgeyh8f2sOBd2JpwBDAoGaT3UYFQD
Gsy2RbpPKuNbDtnFHHtvQpVNCYkqD/d7Tw==
-----END EC PRIVATE KEY-----"""
    
    try:
        # Créer le connector Advanced Trade
        connector = CoinbaseAdvancedTradeConnector(api_key, private_key_pem)
        
        # Tester la connexion
        success = connector.test_connection()
        
        if success:
            print(f"\n🚀 PROCHAINES ÉTAPES:")
            print("1. 📊 Dashboard LIVE avec vraies données")
            print("2. 🤖 Lancer session de trading")
            print("3. 💹 Analyse portfolio en temps réel")
            
            return connector
        else:
            print(f"\n🔧 DIAGNOSTIC NÉCESSAIRE:")
            print("1. Vérifier permissions sur coinbase.com")
            print("2. Confirmer type de clés (Advanced Trade)")
            print("3. Tester avec nouvelles clés si nécessaire")
            
            return None
            
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE: {str(e)}")
        return None

if __name__ == "__main__":
    connector = test_advanced_trade()
    
    if connector:
        print("\n✅ Connector Advanced Trade prêt!")
        print("🔄 Utilisable dans dashboard_live.py")
    else:
        print("\n❌ Problème avec Advanced Trade")
        print("📊 Dashboard démo disponible en attendant")
