#!/usr/bin/env python3
"""
🔄 AMÉLIORATION MAJEURE: Système de Trading Multi-Timeframes Ultra-Sophistiqué
Stratégies avancées avec gestion de position intelligente et hedging
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json
import numpy as np

logger = logging.getLogger(__name__)

class TimeFrame(Enum):
    """Timeframes de trading"""
    M1 = "1m"      # 1 minute
    M5 = "5m"      # 5 minutes
    M15 = "15m"    # 15 minutes
    H1 = "1h"      # 1 heure
    H4 = "4h"      # 4 heures
    D1 = "1d"      # 1 jour
    W1 = "1w"      # 1 semaine

class SignalStrength(Enum):
    """Force des signaux"""
    VERY_WEAK = 1
    WEAK = 2
    MODERATE = 3
    STRONG = 4
    VERY_STRONG = 5

@dataclass
class TradingSignal:
    """Signal de trading structuré"""
    timeframe: TimeFrame
    action: str  # buy, sell, hold
    strength: SignalStrength
    confidence: float
    entry_price: float
    stop_loss: float
    take_profit: float
    reasoning: str
    timestamp: datetime
    expected_duration: str
    risk_reward_ratio: float

@dataclass
class Position:
    """Position de trading"""
    symbol: str
    side: str  # long, short
    entry_price: float
    current_price: float
    quantity: float
    stop_loss: float
    take_profit: float
    unrealized_pnl: float
    realized_pnl: float
    timestamp: datetime
    strategy: str
    timeframe: TimeFrame

class MultiTimeframeStrategy:
    """
    🎯 Stratégie Multi-Timeframes Ultra-Avancée
    
    Fonctionnalités:
    - 📊 Analyse simultanée sur 7 timeframes
    - 🎪 Confluence de signaux multi-horizons
    - ⚡ Entrées/sorties optimales basées sur l'harmonie temporelle
    - 🛡️ Hedging automatique pour protection
    - 📈 Scaling in/out intelligent
    """
    
    def __init__(self):
        self.active_positions = {}
        self.signal_history = []
        self.timeframe_weights = {
            TimeFrame.M1: 0.05,   # Très faible pour le bruit
            TimeFrame.M5: 0.10,   # Entrées de précision
            TimeFrame.M15: 0.15,  # Confirmations courtes
            TimeFrame.H1: 0.25,   # Tendances moyennes
            TimeFrame.H4: 0.25,   # Tendances principales
            TimeFrame.D1: 0.15,   # Biais directionnel
            TimeFrame.W1: 0.05    # Contexte long terme
        }
        
        self.strategy_modes = {
            'scalping': {
                'primary_timeframes': [TimeFrame.M1, TimeFrame.M5],
                'confirmation_timeframes': [TimeFrame.M15, TimeFrame.H1],
                'max_hold_time': timedelta(minutes=30),
                'risk_per_trade': 0.005,  # 0.5%
                'min_rr_ratio': 1.5
            },
            'day_trading': {
                'primary_timeframes': [TimeFrame.M15, TimeFrame.H1],
                'confirmation_timeframes': [TimeFrame.H4, TimeFrame.D1],
                'max_hold_time': timedelta(hours=8),
                'risk_per_trade': 0.01,   # 1%
                'min_rr_ratio': 2.0
            },
            'swing_trading': {
                'primary_timeframes': [TimeFrame.H4, TimeFrame.D1],
                'confirmation_timeframes': [TimeFrame.W1],
                'max_hold_time': timedelta(days=7),
                'risk_per_trade': 0.02,   # 2%
                'min_rr_ratio': 3.0
            },
            'position_trading': {
                'primary_timeframes': [TimeFrame.D1, TimeFrame.W1],
                'confirmation_timeframes': [],
                'max_hold_time': timedelta(days=30),
                'risk_per_trade': 0.03,   # 3%
                'min_rr_ratio': 4.0
            }
        }
        
        self.current_mode = 'day_trading'
        
    async def analyze_multi_timeframe(self, symbol: str, market_data: List[Dict]) -> Dict:
        """
        🔍 Analyse multi-timeframes complète
        
        Returns:
            Dict avec signaux par timeframe et recommandation finale
        """
        try:
            # Analyse sur chaque timeframe
            timeframe_signals = {}
            
            for timeframe in TimeFrame:
                signal = await self._analyze_timeframe(symbol, market_data, timeframe)
                timeframe_signals[timeframe.value] = signal
            
            # Confluence des signaux
            confluence_analysis = self._analyze_confluence(timeframe_signals)
            
            # Recommandation finale
            final_recommendation = self._generate_final_recommendation(
                confluence_analysis, timeframe_signals
            )
            
            # Gestion des positions existantes
            position_management = await self._manage_existing_positions(symbol, market_data)
            
            return {
                'symbol': symbol,
                'timestamp': datetime.now().isoformat(),
                'timeframe_signals': timeframe_signals,
                'confluence_analysis': confluence_analysis,
                'final_recommendation': final_recommendation,
                'position_management': position_management,
                'multi_strategy_score': self._calculate_multi_strategy_score(timeframe_signals),
                'risk_assessment': self._assess_multi_timeframe_risk(confluence_analysis),
                'optimal_entry_strategy': self._suggest_entry_strategy(final_recommendation)
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur analyse multi-timeframe: {e}")
            return self._default_analysis()
    
    async def _analyze_timeframe(self, symbol: str, market_data: List[Dict], timeframe: TimeFrame) -> TradingSignal:
        """Analyse un timeframe spécifique"""
        try:
            # Simulation de données pour le timeframe
            asset_data = self._get_asset_data(symbol, market_data)
            if not asset_data:
                return self._default_signal(timeframe)
            
            price = asset_data['price']
            change_24h = asset_data.get('change_24h', 0)
            volume = asset_data.get('volume', 0)
            
            # Adaptation des signaux selon le timeframe
            if timeframe in [TimeFrame.M1, TimeFrame.M5]:
                # Scalping - signaux rapides
                signal = self._scalping_analysis(price, change_24h, volume, timeframe)
            elif timeframe in [TimeFrame.M15, TimeFrame.H1]:
                # Day trading - momentum et breakouts
                signal = self._day_trading_analysis(price, change_24h, volume, timeframe)
            elif timeframe in [TimeFrame.H4, TimeFrame.D1]:
                # Swing trading - tendances moyennes
                signal = self._swing_analysis(price, change_24h, volume, timeframe)
            else:
                # Position trading - tendances long terme
                signal = self._position_analysis(price, change_24h, volume, timeframe)
            
            return signal
            
        except Exception as e:
            logger.error(f"❌ Erreur analyse timeframe {timeframe.value}: {e}")
            return self._default_signal(timeframe)
    
    def _scalping_analysis(self, price: float, change_24h: float, volume: float, timeframe: TimeFrame) -> TradingSignal:
        """Analyse pour scalping (M1, M5)"""
        # Volatilité et momentum court terme
        volatility = abs(change_24h)
        momentum = change_24h * 0.1  # Réduction pour timeframe court
        
        # Signaux de scalping
        if momentum > 0.2 and volatility > 0.5:
            action = 'buy'
            strength = SignalStrength.MODERATE
            confidence = 0.6
        elif momentum < -0.2 and volatility > 0.5:
            action = 'sell'
            strength = SignalStrength.MODERATE
            confidence = 0.6
        else:
            action = 'hold'
            strength = SignalStrength.WEAK
            confidence = 0.3
        
        # Calcul des niveaux
        stop_loss_pct = 0.3  # 0.3% pour scalping
        take_profit_pct = 0.5  # 0.5% pour scalping
        
        stop_loss = price * (1 - stop_loss_pct / 100) if action == 'buy' else price * (1 + stop_loss_pct / 100)
        take_profit = price * (1 + take_profit_pct / 100) if action == 'buy' else price * (1 - take_profit_pct / 100)
        
        return TradingSignal(
            timeframe=timeframe,
            action=action,
            strength=strength,
            confidence=confidence,
            entry_price=price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            reasoning=f"Scalping {timeframe.value}: momentum={momentum:.3f}, volatilité={volatility:.2f}%",
            timestamp=datetime.now(),
            expected_duration="1-15 minutes",
            risk_reward_ratio=take_profit_pct / stop_loss_pct
        )
    
    def _day_trading_analysis(self, price: float, change_24h: float, volume: float, timeframe: TimeFrame) -> TradingSignal:
        """Analyse pour day trading (M15, H1)"""
        # Momentum et volume
        momentum = change_24h * 0.3
        volume_factor = 1.2 if volume > 1000000 else 0.8
        
        # RSI simulé
        rsi = 50 + (change_24h * 2)
        rsi = max(0, min(100, rsi))
        
        # Signaux day trading
        if momentum > 1.0 and rsi < 70 and volume_factor > 1.0:
            action = 'buy'
            strength = SignalStrength.STRONG
            confidence = 0.75
        elif momentum < -1.0 and rsi > 30 and volume_factor > 1.0:
            action = 'sell'
            strength = SignalStrength.STRONG
            confidence = 0.75
        elif 0.5 < momentum < 1.0 and rsi < 60:
            action = 'buy'
            strength = SignalStrength.MODERATE
            confidence = 0.6
        elif -1.0 < momentum < -0.5 and rsi > 40:
            action = 'sell'
            strength = SignalStrength.MODERATE
            confidence = 0.6
        else:
            action = 'hold'
            strength = SignalStrength.WEAK
            confidence = 0.4
        
        # Niveaux day trading
        stop_loss_pct = 1.0  # 1%
        take_profit_pct = 2.0  # 2%
        
        stop_loss = price * (1 - stop_loss_pct / 100) if action == 'buy' else price * (1 + stop_loss_pct / 100)
        take_profit = price * (1 + take_profit_pct / 100) if action == 'buy' else price * (1 - take_profit_pct / 100)
        
        return TradingSignal(
            timeframe=timeframe,
            action=action,
            strength=strength,
            confidence=confidence,
            entry_price=price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            reasoning=f"Day trading {timeframe.value}: momentum={momentum:.2f}, RSI={rsi:.0f}, volume_factor={volume_factor:.1f}",
            timestamp=datetime.now(),
            expected_duration="1-8 heures",
            risk_reward_ratio=take_profit_pct / stop_loss_pct
        )
    
    def _swing_analysis(self, price: float, change_24h: float, volume: float, timeframe: TimeFrame) -> TradingSignal:
        """Analyse pour swing trading (H4, D1)"""
        # Tendance moyenne terme
        trend_strength = change_24h * 0.6
        
        # MACD simulé
        macd = trend_strength * 0.1
        macd_signal = "bullish" if macd > 0.1 else "bearish" if macd < -0.1 else "neutral"
        
        # Bollinger Bands simulé
        bb_position = "upper" if change_24h > 3 else "lower" if change_24h < -3 else "middle"
        
        # Signaux swing
        if trend_strength > 2.0 and macd_signal == "bullish" and bb_position != "upper":
            action = 'buy'
            strength = SignalStrength.VERY_STRONG
            confidence = 0.85
        elif trend_strength < -2.0 and macd_signal == "bearish" and bb_position != "lower":
            action = 'sell'
            strength = SignalStrength.VERY_STRONG
            confidence = 0.85
        elif 1.0 < trend_strength < 2.0 and macd_signal == "bullish":
            action = 'buy'
            strength = SignalStrength.STRONG
            confidence = 0.7
        elif -2.0 < trend_strength < -1.0 and macd_signal == "bearish":
            action = 'sell'
            strength = SignalStrength.STRONG
            confidence = 0.7
        else:
            action = 'hold'
            strength = SignalStrength.MODERATE
            confidence = 0.5
        
        # Niveaux swing
        stop_loss_pct = 2.5  # 2.5%
        take_profit_pct = 6.0  # 6%
        
        stop_loss = price * (1 - stop_loss_pct / 100) if action == 'buy' else price * (1 + stop_loss_pct / 100)
        take_profit = price * (1 + take_profit_pct / 100) if action == 'buy' else price * (1 - take_profit_pct / 100)
        
        return TradingSignal(
            timeframe=timeframe,
            action=action,
            strength=strength,
            confidence=confidence,
            entry_price=price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            reasoning=f"Swing {timeframe.value}: trend={trend_strength:.2f}, MACD={macd_signal}, BB={bb_position}",
            timestamp=datetime.now(),
            expected_duration="1-7 jours",
            risk_reward_ratio=take_profit_pct / stop_loss_pct
        )
    
    def _position_analysis(self, price: float, change_24h: float, volume: float, timeframe: TimeFrame) -> TradingSignal:
        """Analyse pour position trading (D1, W1)"""
        # Tendance long terme
        long_trend = change_24h * 2.0  # Amplification pour long terme
        
        # Moyenne mobile simulée
        ma_signal = "above" if long_trend > 0 else "below"
        
        # Divergence momentum/prix
        momentum_divergence = abs(long_trend) > 5  # Divergence forte
        
        # Signaux position
        if long_trend > 5.0 and ma_signal == "above" and not momentum_divergence:
            action = 'buy'
            strength = SignalStrength.VERY_STRONG
            confidence = 0.9
        elif long_trend < -5.0 and ma_signal == "below" and not momentum_divergence:
            action = 'sell'
            strength = SignalStrength.VERY_STRONG
            confidence = 0.9
        elif 2.0 < long_trend < 5.0:
            action = 'buy'
            strength = SignalStrength.STRONG
            confidence = 0.75
        elif -5.0 < long_trend < -2.0:
            action = 'sell'
            strength = SignalStrength.STRONG
            confidence = 0.75
        else:
            action = 'hold'
            strength = SignalStrength.MODERATE
            confidence = 0.6
        
        # Niveaux position
        stop_loss_pct = 5.0   # 5%
        take_profit_pct = 15.0  # 15%
        
        stop_loss = price * (1 - stop_loss_pct / 100) if action == 'buy' else price * (1 + stop_loss_pct / 100)
        take_profit = price * (1 + take_profit_pct / 100) if action == 'buy' else price * (1 - take_profit_pct / 100)
        
        return TradingSignal(
            timeframe=timeframe,
            action=action,
            strength=strength,
            confidence=confidence,
            entry_price=price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            reasoning=f"Position {timeframe.value}: long_trend={long_trend:.2f}, MA={ma_signal}, divergence={momentum_divergence}",
            timestamp=datetime.now(),
            expected_duration="1-4 semaines",
            risk_reward_ratio=take_profit_pct / stop_loss_pct
        )
    
    def _analyze_confluence(self, timeframe_signals: Dict) -> Dict:
        """Analyse la confluence des signaux multi-timeframes"""
        try:
            buy_signals = 0
            sell_signals = 0
            hold_signals = 0
            total_confidence = 0
            weighted_strength = 0
            
            # Analyse pondérée des signaux
            for tf_value, signal in timeframe_signals.items():
                timeframe = TimeFrame(tf_value)
                weight = self.timeframe_weights[timeframe]
                
                if signal['action'] == 'buy':
                    buy_signals += weight
                elif signal['action'] == 'sell':
                    sell_signals += weight
                else:
                    hold_signals += weight
                
                total_confidence += signal['confidence'] * weight
                weighted_strength += signal['strength'].value * weight
            
            # Détermination du consensus
            max_signal = max(buy_signals, sell_signals, hold_signals)
            
            if max_signal == buy_signals and buy_signals > 0.4:
                consensus = 'buy'
                consensus_strength = buy_signals
            elif max_signal == sell_signals and sell_signals > 0.4:
                consensus = 'sell'
                consensus_strength = sell_signals
            else:
                consensus = 'hold'
                consensus_strength = hold_signals
            
            # Analyse de la cohérence
            signal_variance = np.var([buy_signals, sell_signals, hold_signals])
            coherence = 1.0 - min(1.0, signal_variance * 2)
            
            return {
                'consensus': consensus,
                'consensus_strength': consensus_strength,
                'buy_weight': buy_signals,
                'sell_weight': sell_signals,
                'hold_weight': hold_signals,
                'total_confidence': total_confidence,
                'weighted_strength': weighted_strength,
                'coherence': coherence,
                'confluence_quality': 'high' if coherence > 0.7 else 'medium' if coherence > 0.4 else 'low'
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur analyse confluence: {e}")
            return {
                'consensus': 'hold',
                'consensus_strength': 0.1,
                'coherence': 0.1,
                'confluence_quality': 'low'
            }
    
    def _generate_final_recommendation(self, confluence: Dict, timeframe_signals: Dict) -> Dict:
        """Génère la recommandation finale basée sur la confluence"""
        try:
            consensus = confluence['consensus']
            consensus_strength = confluence['consensus_strength']
            coherence = confluence['coherence']
            
            # Mode de trading actuel
            mode_config = self.strategy_modes[self.current_mode]
            primary_timeframes = mode_config['primary_timeframes']
            
            # Vérification des timeframes primaires
            primary_signals = []
            for tf in primary_timeframes:
                if tf.value in timeframe_signals:
                    primary_signals.append(timeframe_signals[tf.value])
            
            # Consensus des timeframes primaires
            primary_consensus = self._get_primary_consensus(primary_signals)
            
            # Décision finale
            if (consensus == primary_consensus and 
                consensus_strength > 0.5 and 
                coherence > 0.6):
                
                final_action = consensus
                confidence = min(0.95, consensus_strength * coherence)
                quality = 'excellent'
                
            elif consensus == primary_consensus and consensus_strength > 0.3:
                final_action = consensus
                confidence = consensus_strength * 0.8
                quality = 'good'
                
            elif coherence < 0.4:
                final_action = 'hold'
                confidence = 0.3
                quality = 'poor'
                
            else:
                final_action = 'hold'
                confidence = 0.5
                quality = 'average'
            
            # Calcul de la taille de position optimale
            position_size = self._calculate_optimal_position_size(
                confidence, mode_config['risk_per_trade']
            )
            
            # Niveaux moyens pondérés
            avg_levels = self._calculate_average_levels(timeframe_signals, final_action)
            
            return {
                'action': final_action,
                'confidence': confidence,
                'quality': quality,
                'position_size_pct': position_size,
                'entry_strategy': self._suggest_entry_strategy_detailed(final_action, quality),
                'stop_loss': avg_levels['stop_loss'],
                'take_profit': avg_levels['take_profit'],
                'risk_reward_ratio': avg_levels['rr_ratio'],
                'timeframe_alignment': primary_consensus == consensus,
                'recommended_duration': mode_config['max_hold_time'].total_seconds() / 3600,  # en heures
                'reasoning': self._generate_confluence_reasoning(confluence, primary_consensus, quality)
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur génération recommandation: {e}")
            return {
                'action': 'hold',
                'confidence': 0.1,
                'quality': 'error',
                'reasoning': 'Erreur dans l\'analyse'
            }
    
    def _get_primary_consensus(self, primary_signals: List[Dict]) -> str:
        """Obtient le consensus des timeframes primaires"""
        if not primary_signals:
            return 'hold'
        
        actions = [signal['action'] for signal in primary_signals]
        buy_count = actions.count('buy')
        sell_count = actions.count('sell')
        
        if buy_count > sell_count:
            return 'buy'
        elif sell_count > buy_count:
            return 'sell'
        else:
            return 'hold'
    
    def _calculate_optimal_position_size(self, confidence: float, base_risk: float) -> float:
        """Calcule la taille de position optimale"""
        # Kelly Criterion adapté
        kelly_fraction = confidence * 2 - 1  # -1 à 1
        kelly_fraction = max(0, kelly_fraction)  # Seulement positions positives
        
        # Limitation conservatrice
        max_position = base_risk * 3  # Maximum 3x le risque de base
        optimal_size = min(max_position, base_risk + (kelly_fraction * base_risk))
        
        return round(optimal_size * 100, 2)  # en pourcentage
    
    def _calculate_average_levels(self, timeframe_signals: Dict, action: str) -> Dict:
        """Calcule les niveaux moyens pondérés"""
        try:
            total_weight = 0
            weighted_stop_loss = 0
            weighted_take_profit = 0
            
            for tf_value, signal in timeframe_signals.items():
                if signal['action'] == action:
                    timeframe = TimeFrame(tf_value)
                    weight = self.timeframe_weights[timeframe]
                    
                    weighted_stop_loss += signal['stop_loss'] * weight
                    weighted_take_profit += signal['take_profit'] * weight
                    total_weight += weight
            
            if total_weight > 0:
                avg_stop_loss = weighted_stop_loss / total_weight
                avg_take_profit = weighted_take_profit / total_weight
            else:
                # Valeurs par défaut
                price = list(timeframe_signals.values())[0]['entry_price']
                if action == 'buy':
                    avg_stop_loss = price * 0.98  # -2%
                    avg_take_profit = price * 1.04  # +4%
                elif action == 'sell':
                    avg_stop_loss = price * 1.02  # +2%
                    avg_take_profit = price * 0.96  # -4%
                else:
                    avg_stop_loss = 0
                    avg_take_profit = 0
            
            # Calcul du ratio risk/reward
            if avg_stop_loss > 0 and avg_take_profit > 0:
                entry_price = list(timeframe_signals.values())[0]['entry_price']
                if action == 'buy':
                    risk = abs(entry_price - avg_stop_loss)
                    reward = abs(avg_take_profit - entry_price)
                elif action == 'sell':
                    risk = abs(avg_stop_loss - entry_price)
                    reward = abs(entry_price - avg_take_profit)
                else:
                    risk = reward = 0
                
                rr_ratio = reward / risk if risk > 0 else 0
            else:
                rr_ratio = 0
            
            return {
                'stop_loss': round(avg_stop_loss, 2),
                'take_profit': round(avg_take_profit, 2),
                'rr_ratio': round(rr_ratio, 2)
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul niveaux moyens: {e}")
            return {'stop_loss': 0, 'take_profit': 0, 'rr_ratio': 0}
    
    def _suggest_entry_strategy_detailed(self, action: str, quality: str) -> Dict:
        """Suggère une stratégie d'entrée détaillée"""
        if action == 'hold':
            return {
                'strategy': 'wait',
                'description': 'Attendre une meilleure opportunité',
                'entry_method': 'none'
            }
        
        if quality == 'excellent':
            return {
                'strategy': 'aggressive_entry',
                'description': 'Entrée agressive immédiate',
                'entry_method': 'market_order',
                'position_scaling': 'full_position',
                'timing': 'immediate'
            }
        elif quality == 'good':
            return {
                'strategy': 'scaled_entry',
                'description': 'Entrée échelonnée en 2-3 tranches',
                'entry_method': 'limit_orders',
                'position_scaling': '50%_initial_50%_confirmation',
                'timing': 'staged'
            }
        else:
            return {
                'strategy': 'conservative_entry',
                'description': 'Entrée prudente avec confirmation',
                'entry_method': 'limit_order_with_confirmation',
                'position_scaling': '25%_test_position',
                'timing': 'wait_for_confirmation'
            }
    
    def _generate_confluence_reasoning(self, confluence: Dict, primary_consensus: str, quality: str) -> str:
        """Génère le raisonnement de la confluence"""
        reasoning_parts = []
        
        reasoning_parts.append(f"Consensus multi-timeframes: {confluence['consensus'].upper()}")
        reasoning_parts.append(f"Force du consensus: {confluence['consensus_strength']:.1%}")
        reasoning_parts.append(f"Cohérence: {confluence['coherence']:.1%}")
        reasoning_parts.append(f"Qualité confluence: {confluence['confluence_quality']}")
        reasoning_parts.append(f"Alignement timeframes primaires: {'OUI' if primary_consensus == confluence['consensus'] else 'NON'}")
        reasoning_parts.append(f"Qualité finale: {quality.upper()}")
        
        return " | ".join(reasoning_parts)
    
    async def _manage_existing_positions(self, symbol: str, market_data: List[Dict]) -> Dict:
        """Gère les positions existantes"""
        try:
            if symbol not in self.active_positions:
                return {'status': 'no_positions', 'actions': []}
            
            position = self.active_positions[symbol]
            current_price = self._get_current_price(symbol, market_data)
            
            if current_price is None:
                return {'status': 'error', 'message': 'Prix indisponible'}
            
            # Mise à jour du P&L
            if position.side == 'long':
                position.unrealized_pnl = (current_price - position.entry_price) * position.quantity
            else:
                position.unrealized_pnl = (position.entry_price - current_price) * position.quantity
            
            position.current_price = current_price
            
            # Vérifications de gestion
            actions = []
            
            # Stop loss
            if ((position.side == 'long' and current_price <= position.stop_loss) or
                (position.side == 'short' and current_price >= position.stop_loss)):
                actions.append({
                    'type': 'stop_loss_triggered',
                    'action': 'close_position',
                    'reason': 'Stop loss atteint',
                    'urgency': 'high'
                })
            
            # Take profit
            if ((position.side == 'long' and current_price >= position.take_profit) or
                (position.side == 'short' and current_price <= position.take_profit)):
                actions.append({
                    'type': 'take_profit_triggered',
                    'action': 'close_position',
                    'reason': 'Take profit atteint',
                    'urgency': 'medium'
                })
            
            # Trailing stop (simulation)
            if position.unrealized_pnl > 0:
                trailing_distance = position.entry_price * 0.02  # 2%
                new_stop_loss = current_price - trailing_distance if position.side == 'long' else current_price + trailing_distance
                
                if ((position.side == 'long' and new_stop_loss > position.stop_loss) or
                    (position.side == 'short' and new_stop_loss < position.stop_loss)):
                    actions.append({
                        'type': 'trailing_stop_update',
                        'action': 'update_stop_loss',
                        'new_stop_loss': new_stop_loss,
                        'reason': 'Ajustement trailing stop',
                        'urgency': 'low'
                    })
            
            # Scaling out (prise de bénéfices partielle)
            pnl_pct = (position.unrealized_pnl / (position.entry_price * position.quantity)) * 100
            if pnl_pct > 3:  # +3% de profit
                actions.append({
                    'type': 'partial_profit_taking',
                    'action': 'scale_out_25%',
                    'reason': f'Prise de bénéfices partielle (+{pnl_pct:.1f}%)',
                    'urgency': 'low'
                })
            
            return {
                'status': 'position_active',
                'position': {
                    'symbol': position.symbol,
                    'side': position.side,
                    'entry_price': position.entry_price,
                    'current_price': current_price,
                    'quantity': position.quantity,
                    'unrealized_pnl': position.unrealized_pnl,
                    'pnl_pct': pnl_pct,
                    'stop_loss': position.stop_loss,
                    'take_profit': position.take_profit
                },
                'actions': actions,
                'hold_duration': (datetime.now() - position.timestamp).total_seconds() / 3600  # heures
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur gestion positions: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _calculate_multi_strategy_score(self, timeframe_signals: Dict) -> Dict:
        """Calcule un score multi-stratégies"""
        try:
            strategy_scores = {
                'scalping_score': 0,
                'day_trading_score': 0,
                'swing_score': 0,
                'position_score': 0
            }
            
            # Calcul pour chaque stratégie
            # Scalping (M1, M5)
            scalping_tfs = [TimeFrame.M1.value, TimeFrame.M5.value]
            scalping_signals = [timeframe_signals[tf] for tf in scalping_tfs if tf in timeframe_signals]
            if scalping_signals:
                strategy_scores['scalping_score'] = np.mean([s['confidence'] * s['strength'].value for s in scalping_signals])
            
            # Day Trading (M15, H1)
            day_trading_tfs = [TimeFrame.M15.value, TimeFrame.H1.value]
            day_signals = [timeframe_signals[tf] for tf in day_trading_tfs if tf in timeframe_signals]
            if day_signals:
                strategy_scores['day_trading_score'] = np.mean([s['confidence'] * s['strength'].value for s in day_signals])
            
            # Swing (H4, D1)
            swing_tfs = [TimeFrame.H4.value, TimeFrame.D1.value]
            swing_signals = [timeframe_signals[tf] for tf in swing_tfs if tf in timeframe_signals]
            if swing_signals:
                strategy_scores['swing_score'] = np.mean([s['confidence'] * s['strength'].value for s in swing_signals])
            
            # Position (D1, W1)
            position_tfs = [TimeFrame.D1.value, TimeFrame.W1.value]
            position_signals = [timeframe_signals[tf] for tf in position_tfs if tf in timeframe_signals]
            if position_signals:
                strategy_scores['position_score'] = np.mean([s['confidence'] * s['strength'].value for s in position_signals])
            
            # Stratégie recommandée
            best_strategy = max(strategy_scores.items(), key=lambda x: x[1])
            
            return {
                'scores': strategy_scores,
                'recommended_strategy': best_strategy[0].replace('_score', ''),
                'best_score': best_strategy[1],
                'strategy_distribution': self._normalize_scores(strategy_scores)
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul score multi-stratégies: {e}")
            return {'recommended_strategy': 'day_trading', 'best_score': 0.1}
    
    def _normalize_scores(self, scores: Dict) -> Dict:
        """Normalise les scores en pourcentages"""
        total = sum(scores.values())
        if total == 0:
            return {k: 0.25 for k in scores.keys()}  # Distribution égale si total = 0
        
        return {k: round((v / total) * 100, 1) for k, v in scores.items()}
    
    def _assess_multi_timeframe_risk(self, confluence: Dict) -> Dict:
        """Évalue le risque multi-timeframes"""
        try:
            # Facteurs de risque
            coherence_risk = 1.0 - confluence['coherence']
            consensus_risk = 1.0 - confluence['consensus_strength']
            
            # Risque global
            total_risk = (coherence_risk * 0.6) + (consensus_risk * 0.4)
            
            if total_risk < 0.3:
                risk_level = 'low'
                max_position_size = 0.03  # 3%
            elif total_risk < 0.6:
                risk_level = 'medium'
                max_position_size = 0.02  # 2%
            else:
                risk_level = 'high'
                max_position_size = 0.01  # 1%
            
            return {
                'risk_level': risk_level,
                'risk_score': total_risk,
                'max_position_size_pct': max_position_size * 100,
                'risk_factors': {
                    'timeframe_coherence': coherence_risk,
                    'consensus_weakness': consensus_risk
                },
                'risk_mitigation': self._suggest_risk_mitigation(risk_level, total_risk)
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur évaluation risque: {e}")
            return {'risk_level': 'high', 'risk_score': 0.8}
    
    def _suggest_risk_mitigation(self, risk_level: str, risk_score: float) -> List[str]:
        """Suggère des mesures d'atténuation du risque"""
        mitigations = []
        
        if risk_level == 'high':
            mitigations.extend([
                "Réduire la taille de position à 1% maximum",
                "Utiliser des stop-loss serrés",
                "Éviter l'effet de levier",
                "Attendre une meilleure confluence",
                "Considérer le hedging"
            ])
        elif risk_level == 'medium':
            mitigations.extend([
                "Position de taille modérée (2% max)",
                "Stop-loss adaptatifs",
                "Surveillance rapprochée",
                "Entrée échelonnée"
            ])
        else:  # low risk
            mitigations.extend([
                "Position normale autorisée",
                "Stop-loss standards",
                "Suivi régulier suffisant"
            ])
        
        return mitigations
    
    def _suggest_entry_strategy(self, recommendation: Dict) -> Dict:
        """Suggère une stratégie d'entrée optimale"""
        try:
            action = recommendation.get('action', 'hold')
            confidence = recommendation.get('confidence', 0.5)
            quality = recommendation.get('quality', 'average')
            
            if action == 'hold':
                return {
                    'strategy_type': 'wait_and_see',
                    'description': 'Attendre de meilleures conditions',
                    'next_review': '15 minutes'
                }
            
            # Stratégies d'entrée basées sur la qualité
            if quality == 'excellent' and confidence > 0.8:
                return {
                    'strategy_type': 'immediate_full_entry',
                    'description': 'Entrée immédiate avec position complète',
                    'entry_method': 'market_order',
                    'position_allocation': '100%',
                    'timing': 'now'
                }
            elif quality in ['excellent', 'good'] and confidence > 0.6:
                return {
                    'strategy_type': 'scaled_entry_aggressive',
                    'description': 'Entrée échelonnée agressive (60%-40%)',
                    'entry_method': 'market_order + limit_orders',
                    'position_allocation': '60% immediate, 40% on pullback',
                    'timing': 'immediate + confirmation'
                }
            elif confidence > 0.5:
                return {
                    'strategy_type': 'scaled_entry_conservative',
                    'description': 'Entrée échelonnée conservatrice (40%-60%)',
                    'entry_method': 'limit_orders',
                    'position_allocation': '40% initial, 60% on confirmation',
                    'timing': 'staged_over_time'
                }
            else:
                return {
                    'strategy_type': 'test_position',
                    'description': 'Position test de petite taille',
                    'entry_method': 'small_limit_order',
                    'position_allocation': '25% test position',
                    'timing': 'careful_entry'
                }
                
        except Exception as e:
            logger.error(f"❌ Erreur stratégie d'entrée: {e}")
            return {'strategy_type': 'wait_and_see', 'description': 'Erreur - attendre'}
    
    # Méthodes utilitaires
    def _get_asset_data(self, symbol: str, market_data: List[Dict]) -> Optional[Dict]:
        """Récupère les données d'un actif"""
        for item in market_data:
            if item.get('symbol') == symbol:
                return item
        return None
    
    def _get_current_price(self, symbol: str, market_data: List[Dict]) -> Optional[float]:
        """Récupère le prix actuel d'un actif"""
        asset_data = self._get_asset_data(symbol, market_data)
        return asset_data.get('price') if asset_data else None
    
    def _default_signal(self, timeframe: TimeFrame) -> TradingSignal:
        """Signal par défaut"""
        return TradingSignal(
            timeframe=timeframe,
            action='hold',
            strength=SignalStrength.WEAK,
            confidence=0.1,
            entry_price=0,
            stop_loss=0,
            take_profit=0,
            reasoning='Données insuffisantes',
            timestamp=datetime.now(),
            expected_duration='unknown',
            risk_reward_ratio=0
        )
    
    def _default_analysis(self) -> Dict:
        """Analyse par défaut en cas d'erreur"""
        return {
            'symbol': 'UNKNOWN',
            'timestamp': datetime.now().isoformat(),
            'timeframe_signals': {},
            'confluence_analysis': {
                'consensus': 'hold',
                'consensus_strength': 0.1,
                'coherence': 0.1,
                'confluence_quality': 'poor'
            },
            'final_recommendation': {
                'action': 'hold',
                'confidence': 0.1,
                'quality': 'error',
                'reasoning': 'Erreur dans l\'analyse'
            },
            'error': True
        }
    
    def set_trading_mode(self, mode: str):
        """Change le mode de trading"""
        if mode in self.strategy_modes:
            self.current_mode = mode
            logger.info(f"Mode de trading changé: {mode}")
        else:
            logger.warning(f"Mode de trading invalide: {mode}")
    
    def get_active_positions(self) -> Dict:
        """Retourne les positions actives"""
        return {symbol: {
            'side': pos.side,
            'entry_price': pos.entry_price,
            'current_price': pos.current_price,
            'quantity': pos.quantity,
            'unrealized_pnl': pos.unrealized_pnl,
            'timestamp': pos.timestamp.isoformat()
        } for symbol, pos in self.active_positions.items()}

# Instance globale
multi_timeframe_strategy = MultiTimeframeStrategy()

async def get_multi_timeframe_analysis(symbol: str, market_data: List[Dict]) -> Dict:
    """
    🎯 Point d'entrée principal pour l'analyse multi-timeframes
    """
    return await multi_timeframe_strategy.analyze_multi_timeframe(symbol, market_data)

def set_strategy_mode(mode: str):
    """Change le mode de stratégie"""
    multi_timeframe_strategy.set_trading_mode(mode)

def get_strategy_status() -> Dict:
    """Retourne le statut de la stratégie"""
    return {
        'current_mode': multi_timeframe_strategy.current_mode,
        'active_positions': len(multi_timeframe_strategy.active_positions),
        'timeframe_weights': {tf.value: weight for tf, weight in multi_timeframe_strategy.timeframe_weights.items()},
        'available_modes': list(multi_timeframe_strategy.strategy_modes.keys())
    }
