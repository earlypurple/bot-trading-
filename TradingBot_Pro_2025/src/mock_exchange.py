"""
Module pour tester le dashboard avec des données simulées
"""
import random
import time
import json
import os
import threading

class MockExchange:
    """Échange simulé pour les tests"""
    
    def __init__(self):
        self.portfolio_data = self._generate_mock_portfolio()
        self.prices = {
            'BTC/USD': random.uniform(40000, 45000),
            'ETH/USD': random.uniform(2000, 2500),
            'ADA/USD': random.uniform(0.4, 0.6),
            'DOT/USD': random.uniform(5, 7),
            'LINK/USD': random.uniform(10, 15)
        }
        
        # Démarrer la simulation de variation des prix
        self.running = True
        self.price_thread = threading.Thread(target=self._price_simulator)
        self.price_thread.daemon = True
        self.price_thread.start()
    
    def _generate_mock_portfolio(self):
        """Génère un portfolio simulé"""
        return {
            'BTC': random.uniform(0.05, 0.15),
            'ETH': random.uniform(0.5, 1.5),
            'ADA': random.uniform(100, 500),
            'DOT': random.uniform(20, 50),
            'LINK': random.uniform(10, 30),
            'USD': random.uniform(500, 2000)
        }
    
    def _price_simulator(self):
        """Simule des variations de prix"""
        while self.running:
            for symbol in self.prices:
                # Simuler une variation de prix de ±2%
                current_price = self.prices[symbol]
                change = current_price * (random.uniform(-0.02, 0.02))
                self.prices[symbol] = max(0.01, current_price + change)
            
            # Mise à jour toutes les 10 secondes
            time.sleep(10)
    
    def fetch_balance(self):
        """Récupère un solde simulé"""
        balance = {
            'info': {},
            'free': {},
            'used': {},
            'total': {}
        }
        
        for currency, amount in self.portfolio_data.items():
            balance[currency] = {
                'free': amount * 0.9,  # 90% libre
                'used': amount * 0.1,  # 10% utilisé
                'total': amount        # Total
            }
        
        return balance
    
    def fetch_ticker(self, symbol):
        """Récupère un ticker simulé"""
        price = self.prices.get(symbol, 1.0)
        change = random.uniform(-5, 5)
        
        return {
            'symbol': symbol,
            'last': price,
            'bid': price * 0.999,
            'ask': price * 1.001,
            'high': price * 1.05,
            'low': price * 0.95,
            'percentage': change,
            'info': {}
        }

def get_mock_exchange():
    """Retourne une instance de MockExchange"""
    return MockExchange()

def save_portfolio_cache(portfolio_data):
    """Enregistre les données du portfolio dans un fichier cache"""
    cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    
    cache_file = os.path.join(cache_dir, 'portfolio_cache.json')
    with open(cache_file, 'w') as f:
        json.dump(portfolio_data, f)
    
    return True

def load_portfolio_cache():
    """Charge les données du portfolio depuis le cache"""
    cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cache')
    cache_file = os.path.join(cache_dir, 'portfolio_cache.json')
    
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except:
            pass
    
    return None
