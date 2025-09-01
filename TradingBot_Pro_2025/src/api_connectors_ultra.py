"""
Système de Connecteurs d'APIs Gratuites Ultra-Optimisé
=====================================================
Connecteurs intelligents vers des APIs gratuites avec fallback automatique,
rate limiting, et optimisation pour maximiser les bénéfices.
"""

import asyncio
import aiohttp
import requests
import time
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import os
from abc import ABC, abstractmethod
import yfinance as yf
import ccxt

logger = logging.getLogger(__name__)

@dataclass
class APIResponse:
    """Réponse standardisée d'API"""
    success: bool
    data: Dict[str, Any]
    source: str
    timestamp: datetime
    rate_limit_remaining: Optional[int] = None
    error_message: Optional[str] = None

class BaseAPIConnector(ABC):
    """Connecteur d'API de base"""
    
    def __init__(self, name: str, base_url: str, rate_limit: int):
        self.name = name
        self.base_url = base_url
        self.rate_limit = rate_limit  # calls per minute
        self.call_history = []
        self.is_active = True
        self.last_error = None
    
    def can_make_call(self) -> bool:
        """Vérifie si on peut faire un appel API"""
        now = time.time()
        # Nettoyer l'historique (garder 1 minute)
        self.call_history = [t for t in self.call_history if now - t < 60]
        return len(self.call_history) < self.rate_limit and self.is_active
    
    def record_call(self):
        """Enregistre un appel API"""
        self.call_history.append(time.time())
    
    def disable_temporarily(self, duration_minutes: int = 5):
        """Désactive temporairement l'API"""
        self.is_active = False
        asyncio.create_task(self._reactivate_after(duration_minutes))
    
    async def _reactivate_after(self, minutes: int):
        """Réactive l'API après un délai"""
        await asyncio.sleep(minutes * 60)
        self.is_active = True
        logger.info(f"API {self.name} réactivée")
    
    @abstractmethod
    async def get_crypto_prices(self, symbols: List[str]) -> APIResponse:
        """Récupère les prix des cryptos"""
        pass
    
    @abstractmethod
    async def get_market_data(self, symbol: str) -> APIResponse:
        """Récupère les données de marché détaillées"""
        pass

class CoinGeckoConnector(BaseAPIConnector):
    """Connecteur CoinGecko - API gratuite très fiable"""
    
    def __init__(self):
        super().__init__("CoinGecko", "https://api.coingecko.com/api/v3", 50)
        self.coin_mapping = {
            'BTC/USD': 'bitcoin',
            'ETH/USD': 'ethereum',
            'SOL/USD': 'solana',
            'ATOM/USD': 'cosmos',
            'ADA/USD': 'cardano',
            'DOT/USD': 'polkadot',
            'LINK/USD': 'chainlink',
            'UNI/USD': 'uniswap',
            'AVAX/USD': 'avalanche-2',
            'MATIC/USD': 'matic-network'
        }
    
    async def get_crypto_prices(self, symbols: List[str]) -> APIResponse:
        """Récupère les prix des cryptos depuis CoinGecko"""
        if not self.can_make_call():
            return APIResponse(False, {}, self.name, datetime.now(), 
                             error_message="Rate limit atteint")
        
        try:
            coin_ids = []
            for symbol in symbols:
                if symbol in self.coin_mapping:
                    coin_ids.append(self.coin_mapping[symbol])
            
            if not coin_ids:
                return APIResponse(False, {}, self.name, datetime.now(),
                                 error_message="Aucun symbole supporté")
            
            url = f"{self.base_url}/simple/price"
            params = {
                'ids': ','.join(coin_ids),
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true',
                'include_market_cap': 'true',
                'include_last_updated_at': 'true'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        formatted_data = self._format_price_data(data, symbols)
                        self.record_call()
                        
                        return APIResponse(
                            True, formatted_data, self.name, datetime.now(),
                            rate_limit_remaining=self.rate_limit - len(self.call_history)
                        )
                    else:
                        error_msg = f"Erreur HTTP {response.status}"
                        self.last_error = error_msg
                        return APIResponse(False, {}, self.name, datetime.now(),
                                         error_message=error_msg)
        
        except Exception as e:
            error_msg = f"Erreur CoinGecko: {str(e)}"
            self.last_error = error_msg
            logger.error(error_msg)
            return APIResponse(False, {}, self.name, datetime.now(),
                             error_message=error_msg)
    
    async def get_market_data(self, symbol: str) -> APIResponse:
        """Récupère les données de marché détaillées"""
        if not self.can_make_call() or symbol not in self.coin_mapping:
            return APIResponse(False, {}, self.name, datetime.now(),
                             error_message="Rate limit ou symbole non supporté")
        
        try:
            coin_id = self.coin_mapping[symbol]
            url = f"{self.base_url}/coins/{coin_id}"
            params = {
                'localization': 'false',
                'tickers': 'false',
                'market_data': 'true',
                'community_data': 'false',
                'developer_data': 'false',
                'sparkline': 'false'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        formatted_data = self._format_market_data(data)
                        self.record_call()
                        
                        return APIResponse(
                            True, formatted_data, self.name, datetime.now(),
                            rate_limit_remaining=self.rate_limit - len(self.call_history)
                        )
                    else:
                        return APIResponse(False, {}, self.name, datetime.now(),
                                         error_message=f"Erreur HTTP {response.status}")
        
        except Exception as e:
            error_msg = f"Erreur market data: {str(e)}"
            logger.error(error_msg)
            return APIResponse(False, {}, self.name, datetime.now(),
                             error_message=error_msg)
    
    def _format_price_data(self, raw_data: Dict, symbols: List[str]) -> Dict:
        """Formate les données de prix"""
        formatted = {}
        
        for symbol in symbols:
            if symbol in self.coin_mapping:
                coin_id = self.coin_mapping[symbol]
                if coin_id in raw_data:
                    coin_data = raw_data[coin_id]
                    formatted[symbol] = {
                        'price': coin_data.get('usd', 0),
                        'change_24h': coin_data.get('usd_24h_change', 0),
                        'volume_24h': coin_data.get('usd_24h_vol', 0),
                        'market_cap': coin_data.get('usd_market_cap', 0),
                        'last_updated': coin_data.get('last_updated_at', int(time.time()))
                    }
        
        return formatted
    
    def _format_market_data(self, raw_data: Dict) -> Dict:
        """Formate les données de marché détaillées"""
        market_data = raw_data.get('market_data', {})
        
        return {
            'current_price': market_data.get('current_price', {}).get('usd', 0),
            'market_cap': market_data.get('market_cap', {}).get('usd', 0),
            'total_volume': market_data.get('total_volume', {}).get('usd', 0),
            'high_24h': market_data.get('high_24h', {}).get('usd', 0),
            'low_24h': market_data.get('low_24h', {}).get('usd', 0),
            'price_change_24h': market_data.get('price_change_24h', 0),
            'price_change_percentage_24h': market_data.get('price_change_percentage_24h', 0),
            'market_cap_rank': market_data.get('market_cap_rank', 0),
            'circulating_supply': market_data.get('circulating_supply', 0),
            'total_supply': market_data.get('total_supply', 0),
            'ath': market_data.get('ath', {}).get('usd', 0),
            'atl': market_data.get('atl', {}).get('usd', 0)
        }

class BinanceConnector(BaseAPIConnector):
    """Connecteur Binance - API gratuite avec haute fréquence"""
    
    def __init__(self):
        super().__init__("Binance", "https://api.binance.com/api/v3", 1200)
        self.symbol_mapping = {
            'BTC/USD': 'BTCUSDT',
            'ETH/USD': 'ETHUSDT',
            'SOL/USD': 'SOLUSDT',
            'ATOM/USD': 'ATOMUSDT',
            'ADA/USD': 'ADAUSDT',
            'DOT/USD': 'DOTUSDT',
            'LINK/USD': 'LINKUSDT',
            'UNI/USD': 'UNIUSDT',
            'AVAX/USD': 'AVAXUSDT',
            'MATIC/USD': 'MATICUSDT'
        }
    
    async def get_crypto_prices(self, symbols: List[str]) -> APIResponse:
        """Récupère les prix depuis Binance"""
        if not self.can_make_call():
            return APIResponse(False, {}, self.name, datetime.now(),
                             error_message="Rate limit atteint")
        
        try:
            binance_symbols = []
            for symbol in symbols:
                if symbol in self.symbol_mapping:
                    binance_symbols.append(self.symbol_mapping[symbol])
            
            if not binance_symbols:
                return APIResponse(False, {}, self.name, datetime.now(),
                                 error_message="Aucun symbole supporté")
            
            url = f"{self.base_url}/ticker/24hr"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        formatted_data = self._format_binance_data(data, symbols)
                        self.record_call()
                        
                        return APIResponse(
                            True, formatted_data, self.name, datetime.now(),
                            rate_limit_remaining=self.rate_limit - len(self.call_history)
                        )
                    else:
                        return APIResponse(False, {}, self.name, datetime.now(),
                                         error_message=f"Erreur HTTP {response.status}")
        
        except Exception as e:
            error_msg = f"Erreur Binance: {str(e)}"
            logger.error(error_msg)
            return APIResponse(False, {}, self.name, datetime.now(),
                             error_message=error_msg)
    
    async def get_market_data(self, symbol: str) -> APIResponse:
        """Récupère les données de marché depuis Binance"""
        if not self.can_make_call() or symbol not in self.symbol_mapping:
            return APIResponse(False, {}, self.name, datetime.now(),
                             error_message="Rate limit ou symbole non supporté")
        
        try:
            binance_symbol = self.symbol_mapping[symbol]
            url = f"{self.base_url}/ticker/24hr"
            params = {'symbol': binance_symbol}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        formatted_data = self._format_single_market_data(data)
                        self.record_call()
                        
                        return APIResponse(
                            True, formatted_data, self.name, datetime.now(),
                            rate_limit_remaining=self.rate_limit - len(self.call_history)
                        )
                    else:
                        return APIResponse(False, {}, self.name, datetime.now(),
                                         error_message=f"Erreur HTTP {response.status}")
        
        except Exception as e:
            error_msg = f"Erreur market data Binance: {str(e)}"
            logger.error(error_msg)
            return APIResponse(False, {}, self.name, datetime.now(),
                             error_message=error_msg)
    
    def _format_binance_data(self, raw_data: List[Dict], symbols: List[str]) -> Dict:
        """Formate les données Binance"""
        formatted = {}
        
        # Créer un mapping inverse
        reverse_mapping = {v: k for k, v in self.symbol_mapping.items()}
        
        for item in raw_data:
            binance_symbol = item['symbol']
            if binance_symbol in reverse_mapping:
                symbol = reverse_mapping[binance_symbol]
                if symbol in symbols:
                    formatted[symbol] = {
                        'price': float(item['lastPrice']),
                        'change_24h': float(item['priceChangePercent']),
                        'volume_24h': float(item['volume']),
                        'high_24h': float(item['highPrice']),
                        'low_24h': float(item['lowPrice']),
                        'open_price': float(item['openPrice']),
                        'close_price': float(item['lastPrice']),
                        'count': int(item['count'])
                    }
        
        return formatted
    
    def _format_single_market_data(self, raw_data: Dict) -> Dict:
        """Formate les données de marché pour un seul symbole"""
        return {
            'current_price': float(raw_data['lastPrice']),
            'high_24h': float(raw_data['highPrice']),
            'low_24h': float(raw_data['lowPrice']),
            'volume_24h': float(raw_data['volume']),
            'price_change_24h': float(raw_data['priceChange']),
            'price_change_percentage_24h': float(raw_data['priceChangePercent']),
            'weighted_avg_price': float(raw_data['weightedAvgPrice']),
            'open_price': float(raw_data['openPrice']),
            'trade_count': int(raw_data['count'])
        }

class YahooFinanceConnector(BaseAPIConnector):
    """Connecteur Yahoo Finance - Données stocks et crypto gratuites"""
    
    def __init__(self):
        super().__init__("Yahoo Finance", "https://query1.finance.yahoo.com", 100)
        self.symbol_mapping = {
            'BTC/USD': 'BTC-USD',
            'ETH/USD': 'ETH-USD',
            'SOL/USD': 'SOL-USD',
            'ATOM/USD': 'ATOM-USD',
            'ADA/USD': 'ADA-USD',
            'DOT/USD': 'DOT-USD',
            'LINK/USD': 'LINK-USD',
            'UNI/USD': 'UNI-USD',
            'AVAX/USD': 'AVAX-USD',
            'MATIC/USD': 'MATIC-USD'
        }
    
    async def get_crypto_prices(self, symbols: List[str]) -> APIResponse:
        """Récupère les prix via yfinance"""
        if not self.can_make_call():
            return APIResponse(False, {}, self.name, datetime.now(),
                             error_message="Rate limit atteint")
        
        try:
            formatted_data = {}
            
            for symbol in symbols:
                if symbol in self.symbol_mapping:
                    yf_symbol = self.symbol_mapping[symbol]
                    ticker = yf.Ticker(yf_symbol)
                    
                    # Récupérer les infos actuelles
                    info = ticker.info
                    hist = ticker.history(period="1d", interval="1m")
                    
                    if not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                        open_price = hist['Open'].iloc[0]
                        high_price = hist['High'].max()
                        low_price = hist['Low'].min()
                        volume = hist['Volume'].sum()
                        
                        change_24h = ((current_price - open_price) / open_price) * 100
                        
                        formatted_data[symbol] = {
                            'price': float(current_price),
                            'change_24h': float(change_24h),
                            'volume_24h': float(volume),
                            'high_24h': float(high_price),
                            'low_24h': float(low_price),
                            'open_price': float(open_price),
                            'market_cap': info.get('marketCap', 0)
                        }
            
            self.record_call()
            return APIResponse(
                True, formatted_data, self.name, datetime.now(),
                rate_limit_remaining=self.rate_limit - len(self.call_history)
            )
        
        except Exception as e:
            error_msg = f"Erreur Yahoo Finance: {str(e)}"
            logger.error(error_msg)
            return APIResponse(False, {}, self.name, datetime.now(),
                             error_message=error_msg)
    
    async def get_market_data(self, symbol: str) -> APIResponse:
        """Récupère les données de marché détaillées"""
        if not self.can_make_call() or symbol not in self.symbol_mapping:
            return APIResponse(False, {}, self.name, datetime.now(),
                             error_message="Rate limit ou symbole non supporté")
        
        try:
            yf_symbol = self.symbol_mapping[symbol]
            ticker = yf.Ticker(yf_symbol)
            
            info = ticker.info
            hist = ticker.history(period="5d", interval="1h")
            
            if not hist.empty:
                formatted_data = {
                    'current_price': float(hist['Close'].iloc[-1]),
                    'market_cap': info.get('marketCap', 0),
                    'volume_24h': float(hist['Volume'].iloc[-24:].sum()),
                    'high_24h': float(hist['High'].iloc[-24:].max()),
                    'low_24h': float(hist['Low'].iloc[-24:].min()),
                    'price_change_24h': float(hist['Close'].iloc[-1] - hist['Close'].iloc[-24]),
                    'price_change_percentage_24h': float(((hist['Close'].iloc[-1] / hist['Close'].iloc[-24]) - 1) * 100),
                    'circulating_supply': info.get('circulatingSupply', 0),
                    'total_supply': info.get('totalSupply', 0)
                }
                
                self.record_call()
                return APIResponse(
                    True, formatted_data, self.name, datetime.now(),
                    rate_limit_remaining=self.rate_limit - len(self.call_history)
                )
        
        except Exception as e:
            error_msg = f"Erreur market data Yahoo: {str(e)}"
            logger.error(error_msg)
            return APIResponse(False, {}, self.name, datetime.now(),
                             error_message=error_msg)

class FearGreedConnector(BaseAPIConnector):
    """Connecteur Fear & Greed Index - Sentiment gratuit"""
    
    def __init__(self):
        super().__init__("Fear & Greed", "https://api.alternative.me", 100)
    
    async def get_crypto_prices(self, symbols: List[str]) -> APIResponse:
        """Non applicable pour ce connecteur"""
        return APIResponse(False, {}, self.name, datetime.now(),
                         error_message="Méthode non supportée")
    
    async def get_market_data(self, symbol: str) -> APIResponse:
        """Non applicable pour ce connecteur"""
        return APIResponse(False, {}, self.name, datetime.now(),
                         error_message="Méthode non supportée")
    
    async def get_fear_greed_index(self) -> APIResponse:
        """Récupère l'index Fear & Greed"""
        if not self.can_make_call():
            return APIResponse(False, {}, self.name, datetime.now(),
                             error_message="Rate limit atteint")
        
        try:
            url = f"{self.base_url}/fng/"
            params = {'limit': 7, 'format': 'json'}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        formatted_data = self._format_fear_greed_data(data)
                        self.record_call()
                        
                        return APIResponse(
                            True, formatted_data, self.name, datetime.now(),
                            rate_limit_remaining=self.rate_limit - len(self.call_history)
                        )
                    else:
                        return APIResponse(False, {}, self.name, datetime.now(),
                                         error_message=f"Erreur HTTP {response.status}")
        
        except Exception as e:
            error_msg = f"Erreur Fear & Greed: {str(e)}"
            logger.error(error_msg)
            return APIResponse(False, {}, self.name, datetime.now(),
                             error_message=error_msg)
    
    def _format_fear_greed_data(self, raw_data: Dict) -> Dict:
        """Formate les données Fear & Greed"""
        if 'data' not in raw_data or not raw_data['data']:
            return {}
        
        current = raw_data['data'][0]
        historical = raw_data['data']
        
        # Calcul de la tendance
        if len(historical) > 1:
            trend = 'increasing' if int(current['value']) > int(historical[1]['value']) else 'decreasing'
        else:
            trend = 'stable'
        
        return {
            'current_value': int(current['value']),
            'current_classification': current['value_classification'],
            'timestamp': current['timestamp'],
            'trend': trend,
            'historical_data': [
                {
                    'value': int(item['value']),
                    'classification': item['value_classification'],
                    'timestamp': item['timestamp']
                } for item in historical
            ]
        }

class APIManager:
    """Gestionnaire d'APIs avec fallback intelligent et optimisation"""
    
    def __init__(self):
        self.connectors = {
            'coingecko': CoinGeckoConnector(),
            'binance': BinanceConnector(),
            'yahoo': YahooFinanceConnector(),
            'feargreed': FearGreedConnector()
        }
        
        # Priorités des APIs (plus élevé = priorité plus haute)
        self.priorities = {
            'coingecko': 100,  # Plus fiable et complète
            'binance': 90,     # Très rapide mais limité aux cryptos
            'yahoo': 80,       # Bon fallback
            'feargreed': 70    # Spécialisé sentiment
        }
        
        self.performance_stats = {name: {'success_rate': 1.0, 'avg_response_time': 1.0} 
                                 for name in self.connectors.keys()}
        
        # Cache pour éviter les appels répétitifs
        self.cache = {}
        self.cache_duration = 60  # secondes
    
    async def get_best_crypto_prices(self, symbols: List[str]) -> Dict[str, Any]:
        """Récupère les meilleurs prix en utilisant plusieurs APIs"""
        cache_key = f"prices_{','.join(sorted(symbols))}"
        
        # Vérifier le cache
        if self._is_cache_valid(cache_key):
            logger.info("Données récupérées du cache")
            return self.cache[cache_key]['data']
        
        # Trier les connecteurs par priorité et performance
        sorted_connectors = self._get_sorted_connectors()
        
        best_data = {}
        sources_used = []
        
        for connector_name in sorted_connectors:
            connector = self.connectors[connector_name]
            
            if not connector.can_make_call() or not connector.is_active:
                continue
            
            try:
                start_time = time.time()
                response = await connector.get_crypto_prices(symbols)
                response_time = time.time() - start_time
                
                if response.success:
                    # Mettre à jour les stats de performance
                    self._update_performance_stats(connector_name, True, response_time)
                    
                    # Fusionner les données
                    for symbol, data in response.data.items():
                        if symbol not in best_data:
                            best_data[symbol] = data
                            best_data[symbol]['source'] = response.source
                    
                    sources_used.append(response.source)
                    
                    # Si on a toutes les données nécessaires, arrêter
                    if len(best_data) >= len(symbols):
                        break
                else:
                    self._update_performance_stats(connector_name, False, response_time)
                    logger.warning(f"Échec {connector_name}: {response.error_message}")
            
            except Exception as e:
                logger.error(f"Erreur connecteur {connector_name}: {e}")
                self._update_performance_stats(connector_name, False, 5.0)
        
        # Ajouter des métadonnées
        result = {
            'data': best_data,
            'sources_used': sources_used,
            'timestamp': datetime.now().isoformat(),
            'coverage': len(best_data) / len(symbols) if symbols else 0
        }
        
        # Mettre en cache
        self._cache_data(cache_key, result)
        
        logger.info(f"Prix récupérés: {len(best_data)}/{len(symbols)} symboles, sources: {sources_used}")
        return result
    
    async def get_comprehensive_market_data(self, symbol: str) -> Dict[str, Any]:
        """Récupère des données de marché complètes en combinant plusieurs sources"""
        cache_key = f"market_{symbol}"
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']
        
        combined_data = {}
        sources_used = []
        
        # Essayer chaque connecteur
        for connector_name in self._get_sorted_connectors():
            connector = self.connectors[connector_name]
            
            if not connector.can_make_call() or not connector.is_active:
                continue
            
            try:
                response = await connector.get_market_data(symbol)
                
                if response.success:
                    # Fusionner les données
                    for key, value in response.data.items():
                        if key not in combined_data and value is not None:
                            combined_data[key] = value
                    
                    sources_used.append(response.source)
            
            except Exception as e:
                logger.error(f"Erreur market data {connector_name}: {e}")
        
        result = {
            'data': combined_data,
            'sources_used': sources_used,
            'symbol': symbol,
            'timestamp': datetime.now().isoformat()
        }
        
        self._cache_data(cache_key, result)
        return result
    
    async def get_market_sentiment(self) -> Dict[str, Any]:
        """Récupère le sentiment de marché"""
        cache_key = "market_sentiment"
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']
        
        sentiment_data = {}
        
        # Fear & Greed Index
        if self.connectors['feargreed'].can_make_call():
            try:
                response = await self.connectors['feargreed'].get_fear_greed_index()
                if response.success:
                    sentiment_data.update(response.data)
            except Exception as e:
                logger.error(f"Erreur sentiment: {e}")
        
        # Analyser les tendances générales des prix
        try:
            price_data = await self.get_best_crypto_prices(['BTC/USD', 'ETH/USD', 'SOL/USD'])
            if price_data['data']:
                positive_count = sum(1 for data in price_data['data'].values() 
                                   if data.get('change_24h', 0) > 0)
                total_count = len(price_data['data'])
                
                sentiment_data['market_momentum'] = {
                    'positive_ratio': positive_count / total_count if total_count > 0 else 0.5,
                    'total_coins_analyzed': total_count,
                    'positive_coins': positive_count
                }
        except Exception as e:
            logger.error(f"Erreur analyse momentum: {e}")
        
        result = {
            'data': sentiment_data,
            'timestamp': datetime.now().isoformat(),
            'sources_used': ['feargreed', 'price_analysis']
        }
        
        self._cache_data(cache_key, result)
        return result
    
    def _get_sorted_connectors(self) -> List[str]:
        """Trie les connecteurs par priorité et performance"""
        def sort_key(name):
            performance = self.performance_stats[name]
            priority = self.priorities[name]
            # Score composite: priorité + performance
            return priority * performance['success_rate'] / performance['avg_response_time']
        
        return sorted(self.connectors.keys(), key=sort_key, reverse=True)
    
    def _update_performance_stats(self, connector_name: str, success: bool, response_time: float):
        """Met à jour les statistiques de performance"""
        stats = self.performance_stats[connector_name]
        
        # Moyenne mobile pour le taux de succès
        current_rate = stats['success_rate']
        new_rate = 1.0 if success else 0.0
        stats['success_rate'] = (current_rate * 0.9) + (new_rate * 0.1)
        
        # Moyenne mobile pour le temps de réponse
        current_time = stats['avg_response_time']
        stats['avg_response_time'] = (current_time * 0.9) + (response_time * 0.1)
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Vérifie si les données en cache sont encore valides"""
        if cache_key not in self.cache:
            return False
        
        cache_age = time.time() - self.cache[cache_key]['timestamp']
        return cache_age < self.cache_duration
    
    def _cache_data(self, cache_key: str, data: Any):
        """Met en cache les données"""
        self.cache[cache_key] = {
            'data': data,
            'timestamp': time.time()
        }
        
        # Nettoyer le cache si trop gros
        if len(self.cache) > 100:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
    
    def get_api_status(self) -> Dict[str, Any]:
        """Retourne le statut de toutes les APIs"""
        status = {}
        
        for name, connector in self.connectors.items():
            stats = self.performance_stats[name]
            status[name] = {
                'is_active': connector.is_active,
                'rate_limit_remaining': connector.rate_limit - len(connector.call_history),
                'calls_made_last_minute': len(connector.call_history),
                'success_rate': f"{stats['success_rate']:.1%}",
                'avg_response_time': f"{stats['avg_response_time']:.2f}s",
                'last_error': connector.last_error,
                'priority': self.priorities[name]
            }
        
        return status
    
    async def health_check(self) -> Dict[str, Any]:
        """Effectue un check de santé de toutes les APIs"""
        health_results = {}
        
        for name, connector in self.connectors.items():
            try:
                # Test simple selon le type de connecteur
                if name == 'feargreed':
                    response = await connector.get_fear_greed_index()
                else:
                    response = await connector.get_crypto_prices(['BTC/USD'])
                
                health_results[name] = {
                    'status': 'healthy' if response.success else 'unhealthy',
                    'response_time': time.time(),  # Simplifié
                    'error': response.error_message if not response.success else None
                }
            
            except Exception as e:
                health_results[name] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return {
            'overall_health': 'healthy' if any(r['status'] == 'healthy' for r in health_results.values()) else 'unhealthy',
            'individual_status': health_results,
            'timestamp': datetime.now().isoformat()
        }

# Instance globale du gestionnaire d'APIs
api_manager = APIManager()

# Fonctions utilitaires pour faciliter l'utilisation
async def get_crypto_prices(symbols: List[str]) -> Dict[str, Any]:
    """Fonction utilitaire pour récupérer les prix"""
    return await api_manager.get_best_crypto_prices(symbols)

async def get_market_data(symbol: str) -> Dict[str, Any]:
    """Fonction utilitaire pour récupérer les données de marché"""
    return await api_manager.get_comprehensive_market_data(symbol)

async def get_market_sentiment() -> Dict[str, Any]:
    """Fonction utilitaire pour récupérer le sentiment"""
    return await api_manager.get_market_sentiment()

def get_api_status() -> Dict[str, Any]:
    """Fonction utilitaire pour le statut des APIs"""
    return api_manager.get_api_status()

async def health_check_apis() -> Dict[str, Any]:
    """Fonction utilitaire pour le check de santé"""
    return await api_manager.health_check()
