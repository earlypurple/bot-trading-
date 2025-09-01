#!/usr/bin/env python3
"""
🚀 Coinbase Public API Connector - TradingBot Pro 2025
Connecteur ultra-simple pour données publiques Coinbase
"""

import requests
import json
import time
import logging
from typing import Dict, List, Optional, Any

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CoinbasePublicConnector:
    """Connecteur pour l'API publique Coinbase (sans authentification)"""
    
    def __init__(self):
        self.base_url = "https://api.coinbase.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TradingBot-Pro-2025/1.0',
            'Accept': 'application/json'
        })
        
    def get_exchange_rates(self, currency: str = "USD") -> Dict[str, Any]:
        """Récupère les taux de change"""
        try:
            url = f"{self.base_url}/v2/exchange-rates"
            params = {"currency": currency}
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"❌ Erreur récupération taux: {e}")
            return {}
    
    def get_spot_prices(self, currencies: List[str] = None) -> Dict[str, float]:
        """Récupère les prix spot pour plusieurs cryptos"""
        if currencies is None:
            currencies = ["BTC", "ETH", "LTC", "BCH", "XRP"]
            
        prices = {}
        
        for currency in currencies:
            try:
                url = f"{self.base_url}/v2/prices/{currency}-USD/spot"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if "data" in data and "amount" in data["data"]:
                        prices[currency] = float(data["data"]["amount"])
                        logger.info(f"✅ {currency}: ${prices[currency]:,.2f}")
                else:
                    logger.warning(f"⚠️ Impossible de récupérer le prix de {currency}")
                    
                time.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                logger.error(f"❌ Erreur pour {currency}: {e}")
                
        return prices
    
    def get_currencies(self) -> List[Dict[str, Any]]:
        """Récupère la liste des cryptomonnaies"""
        try:
            url = f"{self.base_url}/v2/currencies"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get("data", [])
            
        except Exception as e:
            logger.error(f"❌ Erreur récupération currencies: {e}")
            return []
    
    def get_time(self) -> Dict[str, Any]:
        """Récupère l'heure du serveur Coinbase"""
        try:
            url = f"{self.base_url}/v2/time"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"❌ Erreur récupération time: {e}")
            return {}
    
    def test_connection(self) -> bool:
        """Test la connexion à l'API"""
        try:
            time_data = self.get_time()
            if time_data:
                logger.info("✅ Connexion API Coinbase réussie")
                return True
            else:
                logger.error("❌ Échec test connexion")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur test connexion: {e}")
            return False

def test_connector():
    """Test du connecteur"""
    print("🚀 Test Coinbase Public API Connector")
    print("=" * 50)
    
    # Initialisation
    connector = CoinbasePublicConnector()
    
    # Test connexion
    print("\n📡 Test de connexion...")
    if connector.test_connection():
        print("✅ Connexion OK")
    else:
        print("❌ Connexion KO")
        return
    
    # Test prix spot
    print("\n💰 Récupération des prix...")
    prices = connector.get_spot_prices()
    
    if prices:
        print("\n📊 Prix actuels:")
        for symbol, price in prices.items():
            print(f"  {symbol}/USD: ${price:,.2f}")
    else:
        print("❌ Aucun prix récupéré")
    
    # Test taux de change
    print("\n💱 Test taux de change...")
    rates = connector.get_exchange_rates()
    if rates and "data" in rates:
        btc_rate = rates["data"]["rates"].get("BTC", "N/A")
        print(f"  1 USD = {btc_rate} BTC")
    
    print("\n✅ Test terminé!")

if __name__ == "__main__":
    test_connector()
