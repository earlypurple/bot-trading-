"""
Module d'Intelligence Artificielle Avancée pour Trading Automatisé
=================================================================
IA améliorée avec apprentissage adaptatif, analyse technique avancée,
et gestion intelligente des risques.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Tuple, Optional
import random
import math

logger = logging.getLogger(__name__)

class EnhancedTradingAI:
    """
    IA de trading avancée avec apprentissage adaptatif et analyse technique poussée.
    """
    
    def __init__(self):
        # Configuration des modes de trading améliorés
        self.trading_modes = {
            'conservative': {
                'name': '🛡️ Conservateur Plus',
                'description': 'IA prudente avec analyse multi-timeframe',
                'max_risk_per_trade': 0.015,
                'profit_target': 0.02,
                'stop_loss': 0.008,
                'max_trades_per_day': 4,
                'confidence_threshold': 0.85,
                'preferred_indicators': ['RSI', 'MACD', 'Bollinger'],
                'market_cap_filter': 'large',  # Large cap uniquement
                'volatility_threshold': 0.05
            },
            'moderate': {
                'name': '⚖️ Modéré Intelligent',
                'description': 'Équilibre optimal avec apprentissage adaptatif',
                'max_risk_per_trade': 0.025,
                'profit_target': 0.03,
                'stop_loss': 0.012,
                'max_trades_per_day': 7,
                'confidence_threshold': 0.75,
                'preferred_indicators': ['RSI', 'MACD', 'Bollinger', 'Volume', 'Stochastic'],
                'market_cap_filter': 'medium',
                'volatility_threshold': 0.08
            },
            'aggressive': {
                'name': '🚀 Agressif Optimisé',
                'description': 'IA haute performance avec stratégies avancées',
                'max_risk_per_trade': 0.04,
                'profit_target': 0.055,
                'stop_loss': 0.02,
                'max_trades_per_day': 12,
                'confidence_threshold': 0.65,
                'preferred_indicators': ['RSI', 'MACD', 'Bollinger', 'Volume', 'Stochastic', 'Williams%R'],
                'market_cap_filter': 'all',
                'volatility_threshold': 0.15
            },
            'scalping': {
                'name': '⚡ Scalping IA',
                'description': 'Trades rapides à haute fréquence',
                'max_risk_per_trade': 0.008,
                'profit_target': 0.008,
                'stop_loss': 0.004,
                'max_trades_per_day': 25,
                'confidence_threshold': 0.6,
                'preferred_indicators': ['RSI', 'Bollinger', 'Volume'],
                'market_cap_filter': 'large',
                'volatility_threshold': 0.03,
                'trade_duration': 'short'  # < 1h
            }
        }
        
        # Paramètres par défaut
        self.daily_budget = 150.0
        self.max_daily_loss = 75.0
        self.current_mode = 'moderate'
        
        # Statistiques avancées
        self.daily_stats = {
            'trades_executed': 0,
            'total_profit_loss': 0.0,
            'successful_trades': 0,
            'failed_trades': 0,
            'win_rate': 0.0,
            'average_profit': 0.0,
            'average_loss': 0.0,
            'largest_win': 0.0,
            'largest_loss': 0.0,
            'consecutive_wins': 0,
            'consecutive_losses': 0,
            'last_reset': datetime.now().date(),
            'performance_score': 50.0  # Score sur 100
        }
        
        # Apprentissage adaptatif
        self.performance_history = []
        self.market_conditions = {
            'trend': 'sideways',  # bullish, bearish, sideways
            'volatility': 'normal',  # low, normal, high
            'volume': 'normal',  # low, normal, high
            'correlation': 0.5,  # Corrélation inter-marchés
            'fear_greed_index': 50  # 0-100
        }
        
        # Gestion intelligente des actifs
        self.asset_scores = {}
        self.preferred_assets = ['BTC/USD', 'ETH/USD', 'SOL/USD', 'ATOM/USD']
        self.blacklisted_assets = []
        self.watchlist = []
        
        # Paramètres d'optimisation
        self.auto_optimization = True
        self.learning_rate = 0.1
        self.confidence_decay = 0.95
        
    def analyze_enhanced_market_sentiment(self, market_data: List[Dict], portfolio_data: Dict = None) -> Dict:
        """Analyse avancée du sentiment de marché avec IA."""
        if not market_data:
            return self._default_sentiment()
        
        try:
            # Calculs de base
            prices = [item.get('price', 0) for item in market_data]
            changes_24h = [item.get('change_24h', 0) for item in market_data]
            volumes = [item.get('volume_24h', 0) for item in market_data if item.get('volume_24h')]
            
            # Analyse du momentum
            positive_momentum = sum(1 for change in changes_24h if change > 0)
            momentum_strength = np.mean([abs(change) for change in changes_24h])
            momentum_ratio = positive_momentum / len(changes_24h) if changes_24h else 0.5
            
            # Analyse de volatilité
            volatility = np.std(changes_24h) if changes_24h else 0
            
            # Analyse de volume (si disponible)
            volume_trend = 'normal'
            if volumes:
                avg_volume = np.mean(volumes)
                recent_volume = np.mean(volumes[-3:]) if len(volumes) >= 3 else avg_volume
                volume_ratio = recent_volume / avg_volume if avg_volume > 0 else 1
                
                if volume_ratio > 1.3:
                    volume_trend = 'increasing'
                elif volume_ratio < 0.7:
                    volume_trend = 'decreasing'
            
            # Score de sentiment composite
            sentiment_score = self._calculate_sentiment_score(
                momentum_ratio, momentum_strength, volatility, volume_trend
            )
            
            # Détermination du sentiment
            if sentiment_score > 0.7:
                sentiment = 'very_bullish'
            elif sentiment_score > 0.6:
                sentiment = 'bullish'
            elif sentiment_score > 0.4:
                sentiment = 'neutral'
            elif sentiment_score > 0.3:
                sentiment = 'bearish'
            else:
                sentiment = 'very_bearish'
            
            # Mise à jour des conditions de marché
            self.market_conditions.update({
                'trend': self._determine_trend(changes_24h),
                'volatility': 'high' if volatility > 5 else 'normal' if volatility > 2 else 'low',
                'volume': volume_trend,
                'fear_greed_index': int(sentiment_score * 100)
            })
            
            return {
                'sentiment': sentiment,
                'confidence': min(sentiment_score + 0.1, 1.0),
                'score': sentiment_score * 100,
                'momentum_strength': momentum_strength,
                'volatility': volatility,
                'volume_trend': volume_trend,
                'market_conditions': self.market_conditions,
                'reasoning': self._generate_sentiment_reasoning(sentiment, momentum_ratio, volatility, volume_trend)
            }
            
        except Exception as e:
            logger.error(f"Erreur analyse sentiment: {e}")
            return self._default_sentiment()
    
    def get_ai_recommendation_enhanced(self, symbol: str, market_data: List[Dict] = None) -> Dict:
        """Recommandation IA améliorée avec analyse technique multi-indicateurs."""
        try:
            self.reset_daily_stats_if_needed()
            
            # Vérifications préliminaires
            if not self._can_trade():
                return self._no_trade_recommendation("Limites quotidiennes atteintes")
            
            if symbol in self.blacklisted_assets:
                return self._no_trade_recommendation(f"{symbol} en liste noire")
            
            # Analyse du marché
            market_sentiment = self.analyze_enhanced_market_sentiment(market_data)
            
            # Récupération des données pour l'actif
            asset_data = self._get_asset_data(symbol, market_data)
            if not asset_data:
                return self._no_trade_recommendation("Données insuffisantes")
            
            # Analyse technique avancée
            technical_analysis = self._perform_technical_analysis(asset_data, symbol)
            
            # Score de l'actif
            asset_score = self._calculate_asset_score(symbol, asset_data, technical_analysis, market_sentiment)
            
            # Calcul de la confiance globale
            confidence = self._calculate_overall_confidence(technical_analysis, market_sentiment, asset_score)
            
            # Décision de trading
            mode_config = self.trading_modes[self.current_mode]
            threshold = mode_config['confidence_threshold']
            
            if confidence < threshold:
                return self._no_trade_recommendation(f"Confiance insuffisante ({confidence:.1%} < {threshold:.1%})")
            
            # Détermination de l'action
            action = self._determine_action(technical_analysis, market_sentiment, asset_score)
            
            # Calcul du montant
            amount = self._calculate_optimal_amount(confidence, asset_data.get('price', 100))
            
            # Calculs des niveaux de stop loss et take profit adaptatifs
            stop_loss_pct, take_profit_pct = self._calculate_adaptive_levels(
                technical_analysis, market_sentiment, confidence
            )
            
            recommendation = {
                'action': action,
                'confidence': confidence,
                'recommended_amount': amount,
                'stop_loss_pct': stop_loss_pct * 100,
                'profit_target_pct': take_profit_pct * 100,
                'asset_score': asset_score,
                'technical_signals': technical_analysis,
                'market_sentiment': market_sentiment['sentiment'],
                'reasoning': self._generate_detailed_reasoning(
                    action, confidence, technical_analysis, market_sentiment, asset_score
                ),
                'risk_level': self._assess_risk_level(confidence, market_sentiment, technical_analysis),
                'expected_duration': self._estimate_trade_duration(action, market_sentiment, technical_analysis)
            }
            
            # Apprentissage: enregistrer la recommandation
            self._record_recommendation(symbol, recommendation)
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Erreur recommandation IA: {e}")
            return self._no_trade_recommendation(f"Erreur système: {str(e)}")
    
    def _perform_technical_analysis(self, asset_data: Dict, symbol: str) -> Dict:
        """Analyse technique avancée multi-indicateurs."""
        price = asset_data.get('price', 100)
        change_24h = asset_data.get('change_24h', 0)
        
        # Simulation d'indicateurs techniques (en production, utiliser de vraies données OHLCV)
        analysis = {}
        
        # RSI simulé
        rsi = self._simulate_rsi(price, change_24h)
        analysis['rsi'] = {
            'value': rsi,
            'signal': 'oversold' if rsi < 30 else 'overbought' if rsi > 70 else 'neutral',
            'strength': abs(rsi - 50) / 50
        }
        
        # MACD simulé
        macd_signal = self._simulate_macd(price, change_24h)
        analysis['macd'] = {
            'signal': macd_signal,
            'strength': random.uniform(0.3, 0.9)
        }
        
        # Bollinger Bands simulés
        bb_signal = self._simulate_bollinger_bands(price, change_24h)
        analysis['bollinger'] = {
            'position': bb_signal,
            'squeeze': random.choice([True, False]),
            'strength': random.uniform(0.4, 0.8)
        }
        
        # Volume analysis
        analysis['volume'] = {
            'trend': random.choice(['increasing', 'decreasing', 'stable']),
            'anomaly': random.choice([True, False]),
            'strength': random.uniform(0.3, 0.7)
        }
        
        # Support/Resistance levels
        analysis['support_resistance'] = {
            'near_support': price * 0.98,
            'near_resistance': price * 1.02,
            'distance_to_support': 0.02,
            'distance_to_resistance': 0.02
        }
        
        return analysis
    
    def _calculate_asset_score(self, symbol: str, asset_data: Dict, technical_analysis: Dict, market_sentiment: Dict) -> float:
        """Calcule un score global pour l'actif (0-100)."""
        score = 50.0  # Score de base
        
        # Bonus/malus basé sur l'actif préféré
        if symbol in self.preferred_assets:
            score += 10
        
        # Score basé sur la performance 24h
        change_24h = asset_data.get('change_24h', 0)
        if -2 <= change_24h <= 5:  # Zone favorable
            score += 5
        elif change_24h > 10 or change_24h < -5:  # Zone de haute volatilité
            score -= 5
        
        # Score technique
        technical_score = 0
        for indicator, data in technical_analysis.items():
            if indicator == 'rsi':
                if data['signal'] == 'oversold':
                    technical_score += 8
                elif data['signal'] == 'overbought':
                    technical_score -= 6
            elif indicator == 'macd':
                if data['signal'] == 'bullish':
                    technical_score += 6
                elif data['signal'] == 'bearish':
                    technical_score -= 4
            elif indicator == 'bollinger':
                if data['position'] == 'below_lower':
                    technical_score += 5
                elif data['position'] == 'above_upper':
                    technical_score -= 3
        
        score += technical_score
        
        # Score sentiment de marché
        sentiment_multiplier = {
            'very_bullish': 1.2,
            'bullish': 1.1,
            'neutral': 1.0,
            'bearish': 0.9,
            'very_bearish': 0.8
        }
        score *= sentiment_multiplier.get(market_sentiment.get('sentiment', 'neutral'), 1.0)
        
        # Historique de performance de l'actif
        if symbol in self.asset_scores:
            historical_score = self.asset_scores[symbol]
            score = (score * 0.7) + (historical_score * 0.3)  # Pondération historique
        
        return max(0, min(100, score))
    
    def _calculate_overall_confidence(self, technical_analysis: Dict, market_sentiment: Dict, asset_score: float) -> float:
        """Calcule la confiance globale de la recommandation."""
        base_confidence = 0.5
        
        # Confiance basée sur les indicateurs techniques
        technical_confidence = 0
        indicator_count = 0
        
        for indicator, data in technical_analysis.items():
            if 'strength' in data:
                technical_confidence += data['strength']
                indicator_count += 1
        
        if indicator_count > 0:
            technical_confidence /= indicator_count
        
        # Confiance basée sur le sentiment de marché
        market_confidence = market_sentiment.get('confidence', 0.5)
        
        # Confiance basée sur le score de l'actif
        asset_confidence = asset_score / 100
        
        # Score de performance historique
        performance_confidence = min(self.daily_stats['performance_score'] / 100, 1.0)
        
        # Calcul pondéré de la confiance
        overall_confidence = (
            technical_confidence * 0.35 +
            market_confidence * 0.25 +
            asset_confidence * 0.25 +
            performance_confidence * 0.15
        )
        
        # Ajustement basé sur les conditions de marché
        if self.market_conditions['volatility'] == 'high':
            overall_confidence *= 0.85  # Réduction en haute volatilité
        
        return max(0.1, min(1.0, overall_confidence))
    
    def update_performance_metrics(self, trade_result: Dict):
        """Met à jour les métriques de performance après un trade."""
        try:
            self.reset_daily_stats_if_needed()
            
            profit_loss = trade_result.get('profit_loss', 0)
            success = trade_result.get('success', False)
            
            # Mise à jour des statistiques de base
            self.daily_stats['trades_executed'] += 1
            self.daily_stats['total_profit_loss'] += profit_loss
            
            if success:
                self.daily_stats['successful_trades'] += 1
                self.daily_stats['consecutive_wins'] += 1
                self.daily_stats['consecutive_losses'] = 0
                if profit_loss > self.daily_stats['largest_win']:
                    self.daily_stats['largest_win'] = profit_loss
                self.daily_stats['average_profit'] = (
                    (self.daily_stats['average_profit'] * (self.daily_stats['successful_trades'] - 1) + profit_loss) /
                    self.daily_stats['successful_trades']
                )
            else:
                self.daily_stats['failed_trades'] += 1
                self.daily_stats['consecutive_losses'] += 1
                self.daily_stats['consecutive_wins'] = 0
                if profit_loss < self.daily_stats['largest_loss']:
                    self.daily_stats['largest_loss'] = profit_loss
                self.daily_stats['average_loss'] = (
                    (self.daily_stats['average_loss'] * (self.daily_stats['failed_trades'] - 1) + profit_loss) /
                    self.daily_stats['failed_trades']
                )
            
            # Calcul du taux de réussite
            total_trades = self.daily_stats['trades_executed']
            if total_trades > 0:
                self.daily_stats['win_rate'] = (self.daily_stats['successful_trades'] / total_trades) * 100
            
            # Calcul du score de performance
            self._update_performance_score()
            
            # Enregistrement dans l'historique
            self.performance_history.append({
                'timestamp': datetime.now(),
                'profit_loss': profit_loss,
                'success': success,
                'performance_score': self.daily_stats['performance_score']
            })
            
            # Limitation de l'historique (garder 30 derniers jours)
            cutoff_date = datetime.now() - timedelta(days=30)
            self.performance_history = [
                entry for entry in self.performance_history 
                if entry['timestamp'] > cutoff_date
            ]
            
            # Auto-optimisation si activée
            if self.auto_optimization:
                self._auto_optimize_parameters()
                
        except Exception as e:
            logger.error(f"Erreur mise à jour performance: {e}")
    
    def _update_performance_score(self):
        """Met à jour le score de performance global (0-100)."""
        base_score = 50
        
        # Score basé sur le P&L
        if self.daily_stats['total_profit_loss'] > 0:
            base_score += min(25, self.daily_stats['total_profit_loss'])
        else:
            base_score += max(-25, self.daily_stats['total_profit_loss'])
        
        # Score basé sur le taux de réussite
        win_rate_bonus = (self.daily_stats['win_rate'] - 50) * 0.5
        base_score += win_rate_bonus
        
        # Score basé sur la consistance (éviter les grosses pertes)
        if self.daily_stats['largest_loss'] < -20:
            base_score -= 10
        
        # Score basé sur les trades consécutifs
        if self.daily_stats['consecutive_wins'] >= 3:
            base_score += 5
        elif self.daily_stats['consecutive_losses'] >= 3:
            base_score -= 5
        
        self.daily_stats['performance_score'] = max(0, min(100, base_score))
    
    # Méthodes utilitaires privées
    def _default_sentiment(self):
        return {'sentiment': 'neutral', 'confidence': 0.5, 'reasoning': 'Analyse par défaut'}
    
    def _can_trade(self) -> bool:
        mode_config = self.trading_modes[self.current_mode]
        return (self.daily_stats['trades_executed'] < mode_config['max_trades_per_day'] and
                abs(self.daily_stats['total_profit_loss']) < self.max_daily_loss)
    
    def _no_trade_recommendation(self, reason: str) -> Dict:
        return {
            'action': 'hold',
            'confidence': 0.0,
            'recommended_amount': 0.0,
            'reasoning': reason,
            'risk_level': 'none'
        }
    
    def _get_asset_data(self, symbol: str, market_data: List[Dict]) -> Optional[Dict]:
        if not market_data:
            return None
        for item in market_data:
            if item.get('symbol') == symbol:
                return item
        return None
    
    def _calculate_sentiment_score(self, momentum_ratio: float, momentum_strength: float, 
                                 volatility: float, volume_trend: str) -> float:
        score = momentum_ratio * 0.4
        score += min(momentum_strength / 10, 0.3)
        
        if volume_trend == 'increasing':
            score += 0.1
        elif volume_trend == 'decreasing':
            score -= 0.1
            
        # Ajustement pour volatilité
        if volatility > 5:
            score *= 0.8  # Réduction si trop volatile
            
        return max(0, min(1, score))
    
    def _determine_trend(self, changes_24h: List[float]) -> str:
        if not changes_24h:
            return 'sideways'
        avg_change = np.mean(changes_24h)
        if avg_change > 2:
            return 'bullish'
        elif avg_change < -2:
            return 'bearish'
        return 'sideways'
    
    def _generate_sentiment_reasoning(self, sentiment: str, momentum_ratio: float, 
                                    volatility: float, volume_trend: str) -> str:
        reasons = []
        reasons.append(f"Momentum: {momentum_ratio:.1%} positif")
        reasons.append(f"Volatilité: {volatility:.1f}%")
        reasons.append(f"Volume: {volume_trend}")
        return f"Sentiment {sentiment} - " + ", ".join(reasons)
    
    def _simulate_rsi(self, price: float, change_24h: float) -> float:
        # Simulation simple du RSI
        base_rsi = 50 + (change_24h * 2)
        noise = random.uniform(-5, 5)
        return max(0, min(100, base_rsi + noise))
    
    def _simulate_macd(self, price: float, change_24h: float) -> str:
        if change_24h > 1:
            return random.choice(['bullish', 'neutral'])
        elif change_24h < -1:
            return random.choice(['bearish', 'neutral'])
        return 'neutral'
    
    def _simulate_bollinger_bands(self, price: float, change_24h: float) -> str:
        if change_24h > 3:
            return 'above_upper'
        elif change_24h < -3:
            return 'below_lower'
        return 'middle'
    
    def _determine_action(self, technical_analysis: Dict, market_sentiment: Dict, asset_score: float) -> str:
        buy_signals = 0
        sell_signals = 0
        
        # Signaux techniques
        if technical_analysis.get('rsi', {}).get('signal') == 'oversold':
            buy_signals += 2
        elif technical_analysis.get('rsi', {}).get('signal') == 'overbought':
            sell_signals += 2
            
        if technical_analysis.get('macd', {}).get('signal') == 'bullish':
            buy_signals += 1
        elif technical_analysis.get('macd', {}).get('signal') == 'bearish':
            sell_signals += 1
            
        # Sentiment de marché
        sentiment = market_sentiment.get('sentiment', 'neutral')
        if sentiment in ['bullish', 'very_bullish']:
            buy_signals += 1
        elif sentiment in ['bearish', 'very_bearish']:
            sell_signals += 1
            
        # Score de l'actif
        if asset_score > 70:
            buy_signals += 1
        elif asset_score < 40:
            sell_signals += 1
            
        if buy_signals > sell_signals:
            return 'buy'
        elif sell_signals > buy_signals:
            return 'sell'
        return 'hold'
    
    def _calculate_optimal_amount(self, confidence: float, price: float) -> float:
        mode_config = self.trading_modes[self.current_mode]
        max_risk = mode_config['max_risk_per_trade']
        
        # Calcul basé sur la confiance et le budget disponible
        risk_adjusted_budget = self.daily_budget * max_risk * confidence
        amount = risk_adjusted_budget / price
        
        return round(amount, 6)
    
    def _calculate_adaptive_levels(self, technical_analysis: Dict, market_sentiment: Dict, 
                                 confidence: float) -> Tuple[float, float]:
        mode_config = self.trading_modes[self.current_mode]
        base_stop_loss = mode_config['stop_loss']
        base_take_profit = mode_config['profit_target']
        
        # Ajustement basé sur la volatilité
        volatility_factor = 1.0
        if self.market_conditions['volatility'] == 'high':
            volatility_factor = 1.3
        elif self.market_conditions['volatility'] == 'low':
            volatility_factor = 0.8
            
        # Ajustement basé sur la confiance
        confidence_factor = 0.8 + (confidence * 0.4)
        
        adjusted_stop_loss = base_stop_loss * volatility_factor
        adjusted_take_profit = base_take_profit * volatility_factor * confidence_factor
        
        return adjusted_stop_loss, adjusted_take_profit
    
    def _generate_detailed_reasoning(self, action: str, confidence: float, 
                                   technical_analysis: Dict, market_sentiment: Dict, 
                                   asset_score: float) -> str:
        reasons = []
        
        reasons.append(f"Action recommandée: {action.upper()}")
        reasons.append(f"Confiance: {confidence:.1%}")
        reasons.append(f"Score actif: {asset_score:.0f}/100")
        reasons.append(f"Sentiment marché: {market_sentiment.get('sentiment', 'neutral')}")
        
        # Signaux techniques
        rsi_signal = technical_analysis.get('rsi', {}).get('signal', 'neutral')
        if rsi_signal != 'neutral':
            reasons.append(f"RSI: {rsi_signal}")
            
        macd_signal = technical_analysis.get('macd', {}).get('signal', 'neutral')
        if macd_signal != 'neutral':
            reasons.append(f"MACD: {macd_signal}")
        
        return " | ".join(reasons)
    
    def _assess_risk_level(self, confidence: float, market_sentiment: Dict, 
                          technical_analysis: Dict) -> str:
        risk_score = 0
        
        if confidence > 0.8:
            risk_score += 1
        elif confidence < 0.6:
            risk_score -= 1
            
        if market_sentiment.get('sentiment') in ['very_bullish', 'very_bearish']:
            risk_score -= 1
            
        if self.market_conditions['volatility'] == 'high':
            risk_score -= 1
            
        if risk_score >= 1:
            return 'low'
        elif risk_score <= -1:
            return 'high'
        return 'medium'
    
    def _estimate_trade_duration(self, action: str, market_sentiment: Dict, 
                               technical_analysis: Dict) -> str:
        if self.current_mode == 'scalping':
            return 'court (< 1h)'
        elif self.market_conditions['volatility'] == 'high':
            return 'court (1-4h)'
        elif market_sentiment.get('confidence', 0) > 0.8:
            return 'moyen (4-24h)'
        return 'long (1-3 jours)'
    
    def _record_recommendation(self, symbol: str, recommendation: Dict):
        """Enregistre la recommandation pour l'apprentissage."""
        # Mise à jour du score de l'actif
        current_score = self.asset_scores.get(symbol, 50.0)
        new_score = recommendation['asset_score']
        self.asset_scores[symbol] = (current_score * 0.7) + (new_score * 0.3)
    
    def _auto_optimize_parameters(self):
        """Optimisation automatique des paramètres basée sur la performance."""
        if len(self.performance_history) < 5:
            return
            
        recent_performance = self.performance_history[-5:]
        avg_performance = np.mean([p['profit_loss'] for p in recent_performance])
        
        # Si performance négative, ajuster les seuils
        if avg_performance < -10:
            # Augmenter les seuils de confiance
            for mode in self.trading_modes:
                current_threshold = self.trading_modes[mode]['confidence_threshold']
                self.trading_modes[mode]['confidence_threshold'] = min(0.95, current_threshold + 0.05)
                
        elif avg_performance > 20:
            # Diminuer légèrement les seuils si très bonne performance
            for mode in self.trading_modes:
                current_threshold = self.trading_modes[mode]['confidence_threshold']
                self.trading_modes[mode]['confidence_threshold'] = max(0.5, current_threshold - 0.02)
    
    def reset_daily_stats_if_needed(self):
        """Remet à zéro les statistiques quotidiennes si nécessaire."""
        today = datetime.now().date()
        if self.daily_stats['last_reset'] != today:
            # Sauvegarde des performances pour apprentissage
            if self.daily_stats['trades_executed'] > 0:
                daily_summary = {
                    'date': self.daily_stats['last_reset'],
                    'trades': self.daily_stats['trades_executed'],
                    'profit_loss': self.daily_stats['total_profit_loss'],
                    'win_rate': self.daily_stats['win_rate'],
                    'performance_score': self.daily_stats['performance_score']
                }
                self.performance_history.append(daily_summary)
            
            # Reset des stats
            self.daily_stats = {
                'trades_executed': 0,
                'total_profit_loss': 0.0,
                'successful_trades': 0,
                'failed_trades': 0,
                'win_rate': 0.0,
                'average_profit': 0.0,
                'average_loss': 0.0,
                'largest_win': 0.0,
                'largest_loss': 0.0,
                'consecutive_wins': 0,
                'consecutive_losses': 0,
                'last_reset': today,
                'performance_score': 50.0
            }
            logger.info("Statistiques quotidiennes remises à zéro avec historique sauvegardé")
    
    def get_trading_summary(self) -> Dict:
        """Retourne un résumé complet de l'état de l'IA."""
        self.reset_daily_stats_if_needed()
        
        mode_config = self.trading_modes[self.current_mode]
        remaining_budget = max(0, self.daily_budget - abs(self.daily_stats['total_profit_loss']))
        
        return {
            'status': 'active' if self._can_trade() else 'paused',
            'mode': self.current_mode,
            'mode_name': mode_config['name'],
            'daily_budget': self.daily_budget,
            'max_daily_loss': self.max_daily_loss,
            'remaining_budget': remaining_budget,
            'trades_executed': self.daily_stats['trades_executed'],
            'max_trades_per_day': mode_config['max_trades_per_day'],
            'successful_trades': self.daily_stats['successful_trades'],
            'failed_trades': self.daily_stats['failed_trades'],
            'total_profit_loss': round(self.daily_stats['total_profit_loss'], 2),
            'win_rate': round(self.daily_stats['win_rate'], 1),
            'performance_score': round(self.daily_stats['performance_score'], 1),
            'market_conditions': self.market_conditions,
            'consecutive_wins': self.daily_stats['consecutive_wins'],
            'consecutive_losses': self.daily_stats['consecutive_losses'],
            'largest_win': self.daily_stats['largest_win'],
            'largest_loss': self.daily_stats['largest_loss'],
            'preferred_assets': self.preferred_assets,
            'confidence_threshold': mode_config['confidence_threshold']
        }
    
    def set_trading_parameters(self, mode: str, daily_budget: float, max_daily_loss: float):
        """Configure les paramètres de trading."""
        if mode in self.trading_modes:
            self.current_mode = mode
        self.daily_budget = max(10, daily_budget)
        self.max_daily_loss = max(5, max_daily_loss)
        
        logger.info(f"Paramètres IA configurés: Mode={mode}, Budget={daily_budget}$, Perte max={max_daily_loss}$")
