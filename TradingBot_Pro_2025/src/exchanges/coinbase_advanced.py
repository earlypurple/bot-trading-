#!/usr/bin/env python3
"""
🚀 Coinbase Advanced Trade API Connector - TradingBot Pro 2025
===============================================================
Connecteur authentifié pour l'API Coinbase Advanced Trade
Permet d'accéder au portfolio, de passer des ordres, etc.

📚 Documentation: https://docs.cloud.coinbase.com/advanced-trade-api/docs/
🔐 Authentification: API Key + Secret (Cloud Trading)
"""

import requests
import json
import time
import hmac
import hashlib
import base64
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CoinbaseAdvancedConnector:
    """Connecteur pour l'API Coinbase Advanced Trade avec authentification"""
    
    def __init__(self, api_key: str, api_secret: str, sandbox: bool = True):
        """
        Initialise le connecteur Coinbase Advanced Trade
        
        Args:
            api_key: Clé API Coinbase
            api_secret: Secret API Coinbase  
            sandbox: True pour sandbox, False pour production
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.sandbox = sandbox
        
        # URLs de base
        if sandbox:
            self.base_url = "https://api.coinbase.com"  # Pas de sandbox pour Advanced Trade
            logger.warning("⚠️ Advanced Trade API n'a pas de sandbox, utilisation de la production")
        else:
            self.base_url = "https://api.coinbase.com"
            
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TradingBot-Pro-2025/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
    def _generate_signature(self, timestamp: str, method: str, path: str, body: str = "") -> str:
        """Génère la signature HMAC pour l'authentification"""
        message = f"{timestamp}{method}{path}{body}"
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _make_request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict[str, Any]:
        """Effectue une requête authentifiée vers l'API"""
        try:
            timestamp = str(int(time.time()))
            path = f"/api/v3/{endpoint.lstrip('/')}"
            url = f"{self.base_url}{path}"
            
            # Préparation du body
            body = ""
            if data:
                body = json.dumps(data)
            
            # Génération de la signature
            signature = self._generate_signature(timestamp, method.upper(), path, body)
            
            # Headers d'authentification
            headers = {
                'CB-ACCESS-KEY': self.api_key,
                'CB-ACCESS-SIGN': signature,
                'CB-ACCESS-TIMESTAMP': timestamp,
            }
            
            # Mise à jour des headers
            self.session.headers.update(headers)
            
            # Requête
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=10)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=10)
            else:
                raise ValueError(f"Méthode HTTP non supportée: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur requête API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    logger.error(f"Détail erreur: {error_detail}")
                except:
                    logger.error(f"Statut HTTP: {e.response.status_code}")
            return {}
        except Exception as e:
            logger.error(f"❌ Erreur générale: {e}")
            return {}
    
    def get_accounts(self) -> List[Dict[str, Any]]:
        """Récupère les comptes/portefeuilles"""
        try:
            response = self._make_request('GET', 'brokerage/accounts')
            if 'accounts' in response:
                logger.info(f"✅ {len(response['accounts'])} comptes récupérés")
                return response['accounts']
            else:
                logger.warning("⚠️ Aucun compte trouvé")
                return []
                
        except Exception as e:
            logger.error(f"❌ Erreur récupération comptes: {e}")
            return []
    
    def get_account_balance(self, account_id: str) -> Dict[str, Any]:
        """Récupère le solde d'un compte spécifique"""
        try:
            response = self._make_request('GET', f'brokerage/accounts/{account_id}')
            if 'account' in response:
                account = response['account']
                logger.info(f"✅ Solde {account.get('currency', 'N/A')}: {account.get('available_balance', {}).get('value', '0')}")
                return account
            else:
                logger.warning(f"⚠️ Compte {account_id} non trouvé")
                return {}
                
        except Exception as e:
            logger.error(f"❌ Erreur solde compte {account_id}: {e}")
            return {}
    
    def get_products(self) -> List[Dict[str, Any]]:
        """Récupère la liste des produits/paires de trading"""
        try:
            response = self._make_request('GET', 'brokerage/products')
            if 'products' in response:
                logger.info(f"✅ {len(response['products'])} produits disponibles")
                return response['products']
            else:
                logger.warning("⚠️ Aucun produit trouvé")
                return []
                
        except Exception as e:
            logger.error(f"❌ Erreur récupération produits: {e}")
            return []
    
    def get_product_candles(self, product_id: str, start: str, end: str, granularity: str = "ONE_HOUR") -> List[Dict[str, Any]]:
        """Récupère les données de chandelier pour un produit"""
        try:
            params = {
                'start': start,
                'end': end,
                'granularity': granularity
            }
            response = self._make_request('GET', f'brokerage/products/{product_id}/candles', params=params)
            
            if 'candles' in response:
                logger.info(f"✅ {len(response['candles'])} bougies récupérées pour {product_id}")
                return response['candles']
            else:
                logger.warning(f"⚠️ Aucune bougie trouvée pour {product_id}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Erreur candles {product_id}: {e}")
            return []
    
    def place_order(self, product_id: str, side: str, size: str, price: str = None, order_type: str = "market") -> Dict[str, Any]:
        """Place un ordre de trading"""
        try:
            order_data = {
                "client_order_id": str(uuid.uuid4()),
                "product_id": product_id,
                "side": side.lower(),  # "buy" ou "sell"
                "order_configuration": {}
            }
            
            if order_type.lower() == "market":
                if side.lower() == "buy":
                    order_data["order_configuration"] = {
                        "market_market_ioc": {
                            "quote_size": size  # Montant en devise de quote
                        }
                    }
                else:
                    order_data["order_configuration"] = {
                        "market_market_ioc": {
                            "base_size": size  # Quantité en devise de base
                        }
                    }
            elif order_type.lower() == "limit":
                order_data["order_configuration"] = {
                    "limit_limit_gtc": {
                        "base_size": size,
                        "limit_price": price
                    }
                }
            
            response = self._make_request('POST', 'brokerage/orders', data=order_data)
            
            if 'success' in response and response['success']:
                logger.info(f"✅ Ordre placé: {response.get('order_id', 'ID inconnu')}")
                return response
            else:
                logger.error(f"❌ Échec placement ordre: {response}")
                return {}
                
        except Exception as e:
            logger.error(f"❌ Erreur placement ordre: {e}")
            return {}
    
    def get_orders(self, product_id: str = None, order_status: str = None) -> List[Dict[str, Any]]:
        """Récupère les ordres"""
        try:
            params = {}
            if product_id:
                params['product_id'] = product_id
            if order_status:
                params['order_status'] = order_status
                
            response = self._make_request('GET', 'brokerage/orders/historical/batch', params=params)
            
            if 'orders' in response:
                logger.info(f"✅ {len(response['orders'])} ordres récupérés")
                return response['orders']
            else:
                logger.warning("⚠️ Aucun ordre trouvé")
                return []
                
        except Exception as e:
            logger.error(f"❌ Erreur récupération ordres: {e}")
            return []
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Récupère un résumé du portfolio"""
        try:
            accounts = self.get_accounts()
            if not accounts:
                return {}
            
            portfolio = {
                'total_value_usd': 0,
                'balances': {},
                'account_count': len(accounts)
            }
            
            for account in accounts:
                currency = account.get('currency', 'UNKNOWN')
                available = float(account.get('available_balance', {}).get('value', '0'))
                hold = float(account.get('hold', {}).get('value', '0'))
                total = available + hold
                
                if total > 0:
                    portfolio['balances'][currency] = {
                        'available': available,
                        'hold': hold,
                        'total': total
                    }
            
            logger.info(f"✅ Portfolio: {len(portfolio['balances'])} devises avec solde")
            return portfolio
            
        except Exception as e:
            logger.error(f"❌ Erreur résumé portfolio: {e}")
            return {}
    
    def test_connection(self) -> Dict[str, Any]:
        """Test la connexion à l'API"""
        try:
            accounts = self.get_accounts()
            if accounts:
                return {
                    'status': 'success',
                    'message': f'Connexion réussie - {len(accounts)} comptes trouvés',
                    'authenticated': True
                }
            else:
                return {
                    'status': 'error', 
                    'message': 'Connexion échouée - Aucun compte trouvé',
                    'authenticated': False
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erreur de connexion: {e}',
                'authenticated': False
            }

def test_connector():
    """Test du connecteur avec des clés d'exemple"""
    print("🚀 Test Coinbase Advanced Trade Connector")
    print("=" * 60)
    
    # ATTENTION: Il faut remplacer par tes vraies clés API
    api_key = "your_api_key_here"
    api_secret = "your_api_secret_here"
    
    if api_key == "your_api_key_here":
        print("❌ Veuillez configurer vos vraies clés API Coinbase")
        print("🔗 Créez vos clés sur: https://cloud.coinbase.com/access/api")
        print("\n📋 Permissions requises:")
        print("  - wallet:accounts:read")
        print("  - wallet:trades:read") 
        print("  - wallet:orders:read")
        print("  - wallet:orders:create (pour le trading)")
        return
    
    # Test du connecteur
    connector = CoinbaseAdvancedConnector(api_key, api_secret)
    
    # Test de connexion
    print("\n📡 Test de connexion...")
    result = connector.test_connection()
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    
    if result['status'] == 'success':
        print("\n💰 Résumé du portfolio...")
        portfolio = connector.get_portfolio_summary()
        if portfolio:
            print(f"Nombre de comptes: {portfolio.get('account_count', 0)}")
            for currency, balance in portfolio.get('balances', {}).items():
                print(f"  {currency}: {balance['total']:.8f} (disponible: {balance['available']:.8f})")
        
        print("\n📊 Produits disponibles (top 5)...")
        products = connector.get_products()
        for product in products[:5]:
            print(f"  {product.get('product_id', 'N/A')} - Status: {product.get('status', 'N/A')}")

if __name__ == "__main__":
    test_connector()
