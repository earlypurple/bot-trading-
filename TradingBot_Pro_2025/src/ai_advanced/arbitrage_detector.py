"""
Arbitrage Detector - Détection d'opportunités d'arbitrage cross-exchange
"""
import asyncio
import aiohttp
import logging
from typing import Dict, List, Tuple
from datetime import datetime
import json

class ArbitrageDetector:
    def __init__(self):
        self.exchanges = {
            'coinbase': {
                'api_url': 'https://api.exchange.coinbase.com',
                'fee_maker': 0.005,  # 0.5%
                'fee_taker': 0.005   # 0.5%
            },
            'binance': {
                'api_url': 'https://api.binance.com',
                'fee_maker': 0.001,  # 0.1%
                'fee_taker': 0.001   # 0.1%
            },
            'kraken': {
                'api_url': 'https://api.kraken.com',
                'fee_maker': 0.0016, # 0.16%
                'fee_taker': 0.0026  # 0.26%
            }
        }
        self.symbols = ['BTC-USD', 'ETH-USD', 'ADA-USD', 'DOT-USD', 'LINK-USD']
        self.price_cache = {}
        self.last_update = {}
        self.min_profit_threshold = 0.5  # 0.5% minimum profit
        
    async def fetch_price_coinbase(self, session: aiohttp.ClientSession, symbol: str) -> float:
        """Récupère prix depuis Coinbase"""
        try:
            url = f"{self.exchanges['coinbase']['api_url']}/products/{symbol}/ticker"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return float(data.get('price', 0))
        except Exception as e:
            logging.error(f"Erreur Coinbase {symbol}: {e}")
        return 0
    
    async def fetch_price_binance(self, session: aiohttp.ClientSession, symbol: str) -> float:
        """Récupère prix depuis Binance (simulation)"""
        try:
            # Conversion symbole Coinbase vers Binance
            binance_symbol = symbol.replace('-', '').replace('USD', 'USDT')
            url = f"{self.exchanges['binance']['api_url']}/api/v3/ticker/price"
            params = {'symbol': binance_symbol}
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return float(data.get('price', 0))
        except Exception as e:
            logging.error(f"Erreur Binance {symbol}: {e}")
        return 0
    
    async def fetch_price_kraken(self, session: aiohttp.ClientSession, symbol: str) -> float:
        """Récupère prix depuis Kraken (simulation)"""
        try:
            # Conversion symbole pour Kraken
            kraken_symbol = symbol.replace('-', '').replace('USD', 'USD')
            if kraken_symbol == 'BTCUSD':
                kraken_symbol = 'XBTUSD'
            elif kraken_symbol == 'ETHUSD':
                kraken_symbol = 'ETHUSD'
            
            url = f"{self.exchanges['kraken']['api_url']}/0/public/Ticker"
            params = {'pair': kraken_symbol}
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'result' in data and kraken_symbol in data['result']:
                        return float(data['result'][kraken_symbol]['c'][0])
        except Exception as e:
            logging.error(f"Erreur Kraken {symbol}: {e}")
        return 0
    
    async def fetch_all_prices(self) -> Dict[str, Dict[str, float]]:
        """Récupère tous les prix de tous les exchanges"""
        prices = {exchange: {} for exchange in self.exchanges.keys()}
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            for symbol in self.symbols:
                # Coinbase (réel)
                tasks.append(self.fetch_price_coinbase(session, symbol))
                
                # Binance et Kraken (simulation avec variation)
                coinbase_price = await self.fetch_price_coinbase(session, symbol)
                if coinbase_price > 0:
                    # Simulation prix avec petites variations
                    import random
                    binance_variation = random.uniform(-0.01, 0.01)  # ±1%
                    kraken_variation = random.uniform(-0.015, 0.015)  # ±1.5%
                    
                    prices['binance'][symbol] = coinbase_price * (1 + binance_variation)
                    prices['kraken'][symbol] = coinbase_price * (1 + kraken_variation)
                    prices['coinbase'][symbol] = coinbase_price
        
        return prices
    
    def calculate_arbitrage_opportunity(self, symbol: str, prices: Dict[str, float]) -> List[Dict]:
        """Calcule opportunités d'arbitrage pour un symbole"""
        opportunities = []
        
        exchanges = list(prices.keys())
        
        for i, buy_exchange in enumerate(exchanges):
            for j, sell_exchange in enumerate(exchanges):
                if i >= j or prices[buy_exchange] == 0 or prices[sell_exchange] == 0:
                    continue
                
                buy_price = prices[buy_exchange]
                sell_price = prices[sell_exchange]
                
                # Calcul avec frais
                buy_fee = self.exchanges[buy_exchange]['fee_taker']
                sell_fee = self.exchanges[sell_exchange]['fee_taker']
                
                effective_buy_price = buy_price * (1 + buy_fee)
                effective_sell_price = sell_price * (1 - sell_fee)
                
                if effective_sell_price > effective_buy_price:
                    profit_absolute = effective_sell_price - effective_buy_price
                    profit_percentage = (profit_absolute / effective_buy_price) * 100
                    
                    if profit_percentage >= self.min_profit_threshold:
                        opportunity = {
                            'symbol': symbol,
                            'buy_exchange': buy_exchange,
                            'sell_exchange': sell_exchange,
                            'buy_price': buy_price,
                            'sell_price': sell_price,
                            'effective_buy_price': effective_buy_price,
                            'effective_sell_price': effective_sell_price,
                            'profit_absolute': profit_absolute,
                            'profit_percentage': profit_percentage,
                            'timestamp': datetime.now(),
                            'recommended_amount': min(1000, profit_percentage * 100)  # Taille position basée sur profit
                        }
                        opportunities.append(opportunity)
        
        return sorted(opportunities, key=lambda x: x['profit_percentage'], reverse=True)
    
    async def find_opportunities(self) -> List[Dict]:
        """Trouve toutes les opportunités d'arbitrage"""
        try:
            all_prices = await self.fetch_all_prices()
            all_opportunities = []
            
            for symbol in self.symbols:
                symbol_prices = {}
                for exchange in self.exchanges.keys():
                    if symbol in all_prices[exchange]:
                        symbol_prices[exchange] = all_prices[exchange][symbol]
                
                if len(symbol_prices) >= 2:
                    opportunities = self.calculate_arbitrage_opportunity(symbol, symbol_prices)
                    all_opportunities.extend(opportunities)
            
            # Cache des résultats
            self.price_cache = all_prices
            self.last_update = datetime.now()
            
            return sorted(all_opportunities, key=lambda x: x['profit_percentage'], reverse=True)
            
        except Exception as e:
            logging.error(f"Erreur recherche arbitrage: {e}")
            return []
    
    def get_top_opportunities(self, limit: int = 5) -> List[Dict]:
        """Retourne les meilleures opportunités"""
        return asyncio.run(self.find_opportunities())[:limit]
    
    def calculate_optimal_position_size(self, opportunity: Dict, portfolio_value: float, max_risk_percentage: float = 5.0) -> float:
        """Calcule taille optimale de position pour arbitrage"""
        max_position = portfolio_value * (max_risk_percentage / 100)
        
        # Limite basée sur le profit potentiel
        profit_based_limit = opportunity['profit_percentage'] * 50  # Plus le profit est élevé, plus on peut investir
        
        # Limite basée sur la liquidité (estimation)
        liquidity_limit = 1000  # $1000 max par trade d'arbitrage
        
        return min(max_position, profit_based_limit, liquidity_limit, opportunity['recommended_amount'])
    
    def is_opportunity_valid(self, opportunity: Dict, max_age_seconds: int = 30) -> bool:
        """Vérifie si l'opportunité est encore valide"""
        age = (datetime.now() - opportunity['timestamp']).total_seconds()
        return age <= max_age_seconds and opportunity['profit_percentage'] >= self.min_profit_threshold
    
    def get_arbitrage_analytics(self) -> Dict:
        """Retourne analytics des opportunités d'arbitrage"""
        return {
            'last_update': self.last_update,
            'exchanges_monitored': len(self.exchanges),
            'symbols_monitored': len(self.symbols),
            'min_profit_threshold': self.min_profit_threshold,
            'cache_size': len(self.price_cache)
        }
