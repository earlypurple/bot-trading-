#!/usr/bin/env python3
"""
🚀 Coinbase Cloud Trading API Connector - TradingBot Pro 2025
============================================================
Connecteur optimisé pour l'API Coinbase Cloud Trading (Advanced Trade)
avec authentification JWT Cloud Trading
"""

import requests
import json
import time
import jwt
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CoinbaseCloudConnector:
    """Connecteur pour l'API Coinbase Cloud Trading avec authentification JWT"""
    
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialise le connecteur Coinbase Cloud Trading
        
        Args:
            api_key: Clé API Coinbase Cloud Trading
            api_secret: Clé privée EC (format PEM)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.coinbase.com"
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TradingBot-Pro-2025/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
    def _create_jwt_token(self, request_method: str, request_path: str) -> str:
        """Crée un token JWT pour l'authentification Cloud Trading"""
        try:
            # URI complète pour le JWT
            uri = f"{request_method} {self.base_url}{request_path}"
            
            # Claims JWT
            claims = {
                'sub': self.api_key,
                'iss': "cdp",
                'nbf': int(time.time()),
                'exp': int(time.time()) + 120,  # 2 minutes d'expiration
                'uri': uri,
            }
            
            # Génération du token JWT avec ES256
            token = jwt.encode(claims, self.api_secret, algorithm='ES256')
            return token
            
        except Exception as e:
            logger.error(f"❌ Erreur génération JWT: {e}")
            raise
    
    def _make_request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict[str, Any]:
        """Effectue une requête authentifiée avec JWT"""
        try:
            path = f"/api/v3/{endpoint.lstrip('/')}"
            url = f"{self.base_url}{path}"
            
            # Génération du token JWT
            jwt_token = self._create_jwt_token(method.upper(), path)
            
            # Headers d'authentification
            headers = {
                'Authorization': f'Bearer {jwt_token}',
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
                    logger.error(f"Contenu: {e.response.text}")
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

def test_connector_with_keys(api_key: str, api_secret: str):
    """Test du connecteur avec les clés fournies"""
    print("🧪 Test Coinbase Cloud Trading Connector")
    print("=" * 50)
    
    try:
        # Création du connecteur
        connector = CoinbaseCloudConnector(api_key, api_secret)
        
        # Test de connexion
        print("\n📡 Test de connexion...")
        result = connector.test_connection()
        
        print(f"Status: {result['status']}")
        print(f"Message: {result['message']}")
        print(f"Authentifié: {result['authenticated']}")
        
        if result['status'] == 'success':
            print("\n💰 Résumé du portfolio...")
            portfolio = connector.get_portfolio_summary()
            if portfolio:
                print(f"Nombre de comptes: {portfolio.get('account_count', 0)}")
                for currency, balance in portfolio.get('balances', {}).items():
                    print(f"  {currency}: {balance['total']:.8f} (disponible: {balance['available']:.8f})")
        
        return result['status'] == 'success'
        
    except Exception as e:
        print(f"❌ Erreur test: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Module de test Coinbase Cloud Trading")
    print("Pour tester, utilisez: test_connector_with_keys(api_key, api_secret)")
