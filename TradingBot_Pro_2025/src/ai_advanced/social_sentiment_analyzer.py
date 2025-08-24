"""
Social Sentiment Analyzer - Analyse sentiment réseaux sociaux
"""
import asyncio
import aiohttp
import logging
from typing import Dict, List
from datetime import datetime, timedelta
import re
import json

class SocialSentimentAnalyzer:
    def __init__(self):
        self.platforms = ['twitter', 'reddit', 'telegram']
        self.crypto_keywords = {
            'BTC': ['bitcoin', 'btc', '$btc'],
            'ETH': ['ethereum', 'eth', '$eth'],
            'ADA': ['cardano', 'ada', '$ada'],
            'DOT': ['polkadot', 'dot', '$dot'],
            'LINK': ['chainlink', 'link', '$link']
        }
        
        # Mots-clés sentiment
        self.bullish_keywords = [
            'bullish', 'moon', 'pump', 'rally', 'surge', 'breakout', 'buy', 'long',
            'hodl', 'diamond hands', 'to the moon', 'rocket', 'green', 'gains',
            'ath', 'new high', 'resistance broken', 'support', 'bounce'
        ]
        
        self.bearish_keywords = [
            'bearish', 'dump', 'crash', 'drop', 'fall', 'sell', 'short',
            'paper hands', 'red', 'losses', 'resistance', 'breakdown',
            'support broken', 'capitulation', 'fud', 'fear'
        ]
        
        self.sentiment_cache = {}
        self.last_update = {}
        
    def simulate_twitter_sentiment(self, symbol: str) -> Dict:
        """Simule analyse sentiment Twitter"""
        import random
        
        # Simulation basée sur volatilité récente
        base_sentiment = random.uniform(-1, 1)
        
        # Facteurs influençant le sentiment
        factors = {
            'volume_factor': random.uniform(0.8, 1.2),
            'price_momentum': random.uniform(-0.3, 0.3),
            'social_buzz': random.uniform(0.5, 2.0)
        }
        
        # Calcul sentiment final
        sentiment_score = base_sentiment * factors['volume_factor']
        sentiment_score += factors['price_momentum']
        sentiment_score = max(-1, min(1, sentiment_score))
        
        # Génération de métriques
        mention_count = int(factors['social_buzz'] * random.randint(100, 1000))
        engagement_rate = random.uniform(0.02, 0.15)
        
        return {
            'platform': 'twitter',
            'symbol': symbol,
            'sentiment_score': sentiment_score,
            'sentiment_label': self.score_to_label(sentiment_score),
            'mention_count': mention_count,
            'engagement_rate': engagement_rate,
            'trending_score': factors['social_buzz'],
            'confidence': random.uniform(0.6, 0.9),
            'timestamp': datetime.now()
        }
    
    def simulate_reddit_sentiment(self, symbol: str) -> Dict:
        """Simule analyse sentiment Reddit"""
        import random
        
        # Reddit tend à être plus analytique
        base_sentiment = random.uniform(-0.8, 0.8)
        
        # Simulation posts et commentaires
        post_count = random.randint(10, 100)
        comment_count = random.randint(50, 500)
        upvote_ratio = random.uniform(0.5, 0.95)
        
        # Ajustement sentiment basé sur ratio upvotes
        sentiment_adjustment = (upvote_ratio - 0.5) * 2  # Convert to -1 to 1
        final_sentiment = (base_sentiment + sentiment_adjustment) / 2
        final_sentiment = max(-1, min(1, final_sentiment))
        
        return {
            'platform': 'reddit',
            'symbol': symbol,
            'sentiment_score': final_sentiment,
            'sentiment_label': self.score_to_label(final_sentiment),
            'post_count': post_count,
            'comment_count': comment_count,
            'upvote_ratio': upvote_ratio,
            'avg_score': random.randint(5, 100),
            'confidence': random.uniform(0.7, 0.95),
            'timestamp': datetime.now()
        }
    
    def simulate_telegram_sentiment(self, symbol: str) -> Dict:
        """Simule analyse sentiment Telegram"""
        import random
        
        # Telegram plus volatil et influencé par les groupes
        base_sentiment = random.uniform(-1.2, 1.2)
        base_sentiment = max(-1, min(1, base_sentiment))
        
        # Simulation activité groupes
        group_count = random.randint(5, 50)
        message_count = random.randint(100, 2000)
        active_users = random.randint(20, 500)
        
        return {
            'platform': 'telegram',
            'symbol': symbol,
            'sentiment_score': base_sentiment,
            'sentiment_label': self.score_to_label(base_sentiment),
            'group_count': group_count,
            'message_count': message_count,
            'active_users': active_users,
            'influence_score': random.uniform(0.3, 0.8),
            'confidence': random.uniform(0.5, 0.8),
            'timestamp': datetime.now()
        }
    
    def score_to_label(self, score: float) -> str:
        """Convertit score en label"""
        if score > 0.3:
            return 'BULLISH'
        elif score < -0.3:
            return 'BEARISH'
        else:
            return 'NEUTRAL'
    
    def analyze_text_sentiment(self, text: str) -> float:
        """Analyse sentiment d'un texte"""
        text_lower = text.lower()
        
        bullish_count = sum(1 for keyword in self.bullish_keywords if keyword in text_lower)
        bearish_count = sum(1 for keyword in self.bearish_keywords if keyword in text_lower)
        
        total_keywords = bullish_count + bearish_count
        if total_keywords == 0:
            return 0
        
        sentiment = (bullish_count - bearish_count) / total_keywords
        return sentiment
    
    async def analyze_symbol_sentiment(self, symbol: str) -> Dict:
        """Analyse sentiment complet pour un symbole"""
        try:
            # Récupération sentiment de toutes les plateformes
            twitter_sentiment = self.simulate_twitter_sentiment(symbol)
            reddit_sentiment = self.simulate_reddit_sentiment(symbol)
            telegram_sentiment = self.simulate_telegram_sentiment(symbol)
            
            # Agrégation avec pondération
            weights = {
                'twitter': 0.4,   # Twitter plus influent
                'reddit': 0.35,   # Reddit analytique
                'telegram': 0.25  # Telegram moins fiable
            }
            
            sentiments = [twitter_sentiment, reddit_sentiment, telegram_sentiment]
            
            # Calcul sentiment agrégé
            weighted_sentiment = sum(
                s['sentiment_score'] * weights[s['platform']] * s['confidence']
                for s in sentiments
            ) / sum(weights[s['platform']] * s['confidence'] for s in sentiments)
            
            # Métriques d'activité agrégées
            total_mentions = (twitter_sentiment['mention_count'] + 
                            reddit_sentiment['post_count'] + reddit_sentiment['comment_count'] +
                            telegram_sentiment['message_count'])
            
            avg_confidence = sum(s['confidence'] for s in sentiments) / len(sentiments)
            
            # Classification du sentiment
            sentiment_strength = abs(weighted_sentiment)
            if sentiment_strength > 0.6:
                strength_label = 'STRONG'
            elif sentiment_strength > 0.3:
                strength_label = 'MODERATE'
            else:
                strength_label = 'WEAK'
            
            result = {
                'symbol': symbol,
                'aggregated_sentiment': {
                    'score': weighted_sentiment,
                    'label': self.score_to_label(weighted_sentiment),
                    'strength': strength_label,
                    'confidence': avg_confidence
                },
                'platform_breakdown': {
                    'twitter': twitter_sentiment,
                    'reddit': reddit_sentiment,
                    'telegram': telegram_sentiment
                },
                'activity_metrics': {
                    'total_mentions': total_mentions,
                    'trending_factor': sum(s.get('trending_score', 1) for s in sentiments) / len(sentiments),
                    'engagement_quality': reddit_sentiment['upvote_ratio']
                },
                'signals': self.generate_trading_signals(weighted_sentiment, avg_confidence),
                'timestamp': datetime.now()
            }
            
            # Cache du résultat
            self.sentiment_cache[symbol] = result
            self.last_update[symbol] = datetime.now()
            
            return result
            
        except Exception as e:
            logging.error(f"Erreur analyse sentiment {symbol}: {e}")
            return self.get_neutral_sentiment(symbol)
    
    def generate_trading_signals(self, sentiment_score: float, confidence: float) -> Dict:
        """Génère signaux de trading basés sur sentiment"""
        signals = {
            'action': 'HOLD',
            'strength': 0,
            'reasoning': 'Sentiment neutre'
        }
        
        # Seuils pour signaux
        if confidence > 0.7:  # Confiance élevée
            if sentiment_score > 0.6:
                signals = {
                    'action': 'BUY',
                    'strength': min(sentiment_score * 100, 90),
                    'reasoning': 'Sentiment très bullish avec haute confiance'
                }
            elif sentiment_score < -0.6:
                signals = {
                    'action': 'SELL',
                    'strength': min(abs(sentiment_score) * 100, 90),
                    'reasoning': 'Sentiment très bearish avec haute confiance'
                }
            elif sentiment_score > 0.3:
                signals = {
                    'action': 'BUY',
                    'strength': min(sentiment_score * 50, 60),
                    'reasoning': 'Sentiment bullish modéré'
                }
            elif sentiment_score < -0.3:
                signals = {
                    'action': 'SELL',
                    'strength': min(abs(sentiment_score) * 50, 60),
                    'reasoning': 'Sentiment bearish modéré'
                }
        
        return signals
    
    def get_neutral_sentiment(self, symbol: str) -> Dict:
        """Retourne sentiment neutre par défaut"""
        return {
            'symbol': symbol,
            'aggregated_sentiment': {
                'score': 0,
                'label': 'NEUTRAL',
                'strength': 'WEAK',
                'confidence': 0.5
            },
            'platform_breakdown': {},
            'activity_metrics': {'total_mentions': 0},
            'signals': {'action': 'HOLD', 'strength': 0, 'reasoning': 'Données insuffisantes'},
            'timestamp': datetime.now()
        }
    
    async def analyze_multiple_symbols(self, symbols: List[str]) -> Dict[str, Dict]:
        """Analyse sentiment pour plusieurs symboles"""
        results = {}
        
        tasks = [self.analyze_symbol_sentiment(symbol) for symbol in symbols]
        sentiment_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for symbol, result in zip(symbols, sentiment_results):
            if isinstance(result, Exception):
                logging.error(f"Erreur sentiment {symbol}: {result}")
                results[symbol] = self.get_neutral_sentiment(symbol)
            else:
                results[symbol] = result
        
        return results
    
    def get_sentiment_summary(self, symbols: List[str]) -> Dict:
        """Résumé sentiment du marché"""
        sentiments = []
        
        for symbol in symbols:
            if symbol in self.sentiment_cache:
                sentiment_data = self.sentiment_cache[symbol]
                sentiments.append(sentiment_data['aggregated_sentiment']['score'])
        
        if not sentiments:
            return {'market_sentiment': 'NEUTRAL', 'score': 0, 'symbols_analyzed': 0}
        
        avg_sentiment = sum(sentiments) / len(sentiments)
        
        return {
            'market_sentiment': self.score_to_label(avg_sentiment),
            'score': avg_sentiment,
            'symbols_analyzed': len(sentiments),
            'bullish_count': sum(1 for s in sentiments if s > 0.3),
            'bearish_count': sum(1 for s in sentiments if s < -0.3),
            'neutral_count': sum(1 for s in sentiments if -0.3 <= s <= 0.3)
        }
    
    def get_cached_sentiment(self, symbol: str, max_age_minutes: int = 5) -> Dict:
        """Récupère sentiment en cache"""
        if symbol in self.sentiment_cache and symbol in self.last_update:
            age = datetime.now() - self.last_update[symbol]
            if age.total_seconds() < max_age_minutes * 60:
                return self.sentiment_cache[symbol]
        return None
