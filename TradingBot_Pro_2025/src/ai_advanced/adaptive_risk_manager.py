"""
Adaptive Risk Manager - Gestion adaptative des risques
"""
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import logging
import json

class AdaptiveRiskManager:
    def __init__(self):
        self.risk_levels = {
            'very_low': {'max_position': 0.05, 'stop_loss': 0.02, 'take_profit': 0.04},
            'low': {'max_position': 0.10, 'stop_loss': 0.03, 'take_profit': 0.06},
            'moderate': {'max_position': 0.15, 'stop_loss': 0.05, 'take_profit': 0.10},
            'high': {'max_position': 0.20, 'stop_loss': 0.08, 'take_profit': 0.15},
            'very_high': {'max_position': 0.30, 'stop_loss': 0.12, 'take_profit': 0.25}
        }
        
        self.market_conditions = {
            'bull_market': {'risk_multiplier': 1.2, 'position_multiplier': 1.3},
            'bear_market': {'risk_multiplier': 0.7, 'position_multiplier': 0.6},
            'sideways': {'risk_multiplier': 1.0, 'position_multiplier': 1.0},
            'high_volatility': {'risk_multiplier': 0.8, 'position_multiplier': 0.7},
            'low_volatility': {'risk_multiplier': 1.1, 'position_multiplier': 1.2}
        }
        
        self.portfolio_metrics = {
            'current_drawdown': 0,
            'max_drawdown': 0,
            'win_rate': 0.5,
            'profit_factor': 1.0,
            'volatility': 0.2
        }
        
        self.trade_history = []
        self.risk_adjustments_log = []
        
    def analyze_market_conditions(self, price_data: Dict[str, List[float]], 
                                volatility_data: Dict[str, float]) -> str:
        """Analyse les conditions du marché"""
        try:
            # Calcul tendance générale
            trends = []
            volatilities = []
            
            for symbol, prices in price_data.items():
                if len(prices) >= 20:
                    # Tendance (SMA court vs SMA long)
                    sma_short = np.mean(prices[-5:])
                    sma_long = np.mean(prices[-20:])
                    trend = (sma_short / sma_long - 1) * 100
                    trends.append(trend)
                    
                    # Volatilité
                    returns = np.diff(prices) / prices[:-1]
                    vol = np.std(returns) * np.sqrt(252) * 100  # Annualisée
                    volatilities.append(vol)
            
            if not trends or not volatilities:
                return 'sideways'
            
            avg_trend = np.mean(trends)
            avg_volatility = np.mean(volatilities)
            
            # Classification des conditions
            if avg_volatility > 60:  # Volatilité élevée
                return 'high_volatility'
            elif avg_volatility < 30:  # Volatilité faible
                return 'low_volatility'
            elif avg_trend > 5:  # Tendance haussière
                return 'bull_market'
            elif avg_trend < -5:  # Tendance baissière
                return 'bear_market'
            else:
                return 'sideways'
                
        except Exception as e:
            logging.error(f"Erreur analyse conditions marché: {e}")
            return 'sideways'
    
    def calculate_portfolio_drawdown(self, portfolio_values: List[float]) -> Tuple[float, float]:
        """Calcule drawdown actuel et maximum"""
        if len(portfolio_values) < 2:
            return 0, 0
        
        # Pic historique
        peak = max(portfolio_values)
        current_value = portfolio_values[-1]
        
        # Drawdown actuel
        current_drawdown = (peak - current_value) / peak if peak > 0 else 0
        
        # Drawdown maximum
        max_drawdown = 0
        running_peak = portfolio_values[0]
        
        for value in portfolio_values:
            if value > running_peak:
                running_peak = value
            drawdown = (running_peak - value) / running_peak if running_peak > 0 else 0
            max_drawdown = max(max_drawdown, drawdown)
        
        return current_drawdown, max_drawdown
    
    def update_portfolio_metrics(self, portfolio_values: List[float], 
                               recent_trades: List[Dict]) -> None:
        """Met à jour les métriques du portfolio"""
        try:
            # Calcul drawdown
            current_dd, max_dd = self.calculate_portfolio_drawdown(portfolio_values)
            self.portfolio_metrics['current_drawdown'] = current_dd
            self.portfolio_metrics['max_drawdown'] = max_dd
            
            # Analyse des trades récents
            if recent_trades:
                winning_trades = [t for t in recent_trades if t.get('profit', 0) > 0]
                total_trades = len(recent_trades)
                
                if total_trades > 0:
                    self.portfolio_metrics['win_rate'] = len(winning_trades) / total_trades
                    
                    # Profit factor
                    total_wins = sum(t.get('profit', 0) for t in winning_trades)
                    total_losses = abs(sum(t.get('profit', 0) for t in recent_trades if t.get('profit', 0) < 0))
                    
                    if total_losses > 0:
                        self.portfolio_metrics['profit_factor'] = total_wins / total_losses
                    else:
                        self.portfolio_metrics['profit_factor'] = float('inf') if total_wins > 0 else 1.0
            
            # Volatilité du portfolio
            if len(portfolio_values) > 1:
                returns = np.diff(portfolio_values) / portfolio_values[:-1]
                self.portfolio_metrics['volatility'] = np.std(returns) * np.sqrt(252)
                
        except Exception as e:
            logging.error(f"Erreur mise à jour métriques: {e}")
    
    def adjust_position_sizing(self, base_position_size: float, 
                             market_condition: str, 
                             portfolio_drawdown: float,
                             signal_confidence: float) -> float:
        """Ajuste la taille de position selon les conditions"""
        try:
            adjusted_size = base_position_size
            
            # Ajustement selon conditions marché
            market_params = self.market_conditions.get(market_condition, 
                                                     self.market_conditions['sideways'])
            adjusted_size *= market_params['position_multiplier']
            
            # Réduction si drawdown élevé
            if portfolio_drawdown > 0.10:  # 10% drawdown
                drawdown_penalty = 1 - (portfolio_drawdown * 2)  # Réduction proportionnelle
                adjusted_size *= max(drawdown_penalty, 0.3)  # Minimum 30% de la taille
            
            # Ajustement selon confiance du signal
            confidence_multiplier = 0.5 + (signal_confidence * 0.5)  # 0.5 à 1.0
            adjusted_size *= confidence_multiplier
            
            # Ajustement selon win rate
            if self.portfolio_metrics['win_rate'] < 0.4:  # Win rate faible
                adjusted_size *= 0.7
            elif self.portfolio_metrics['win_rate'] > 0.6:  # Win rate élevé
                adjusted_size *= 1.2
            
            # Limites absolues
            max_position = 0.25  # Maximum 25% du portfolio
            min_position = 0.01  # Minimum 1% du portfolio
            
            adjusted_size = max(min_position, min(adjusted_size, max_position))
            
            # Log de l'ajustement
            adjustment_log = {
                'timestamp': datetime.now(),
                'original_size': base_position_size,
                'adjusted_size': adjusted_size,
                'market_condition': market_condition,
                'portfolio_drawdown': portfolio_drawdown,
                'signal_confidence': signal_confidence,
                'win_rate': self.portfolio_metrics['win_rate']
            }
            self.risk_adjustments_log.append(adjustment_log)
            
            return adjusted_size
            
        except Exception as e:
            logging.error(f"Erreur ajustement position: {e}")
            return min(base_position_size, 0.05)  # Fallback conservateur
    
    def calculate_stop_loss(self, entry_price: float, 
                          market_condition: str, 
                          position_type: str,
                          volatility: float) -> float:
        """Calcule stop loss adaptatif"""
        try:
            # Stop loss de base selon volatilité
            base_stop_pct = min(max(volatility * 0.5, 0.02), 0.15)  # 2% à 15%
            
            # Ajustement selon conditions marché
            market_params = self.market_conditions.get(market_condition,
                                                     self.market_conditions['sideways'])
            stop_pct = base_stop_pct * market_params['risk_multiplier']
            
            # Ajustement selon drawdown
            if self.portfolio_metrics['current_drawdown'] > 0.05:
                stop_pct *= 0.8  # Stop plus serré si drawdown
            
            # Calcul prix stop
            if position_type.upper() == 'BUY':
                stop_price = entry_price * (1 - stop_pct)
            else:  # SELL
                stop_price = entry_price * (1 + stop_pct)
            
            return stop_price
            
        except Exception as e:
            logging.error(f"Erreur calcul stop loss: {e}")
            # Stop loss par défaut conservateur
            if position_type.upper() == 'BUY':
                return entry_price * 0.95  # -5%
            else:
                return entry_price * 1.05  # +5%
    
    def calculate_take_profit(self, entry_price: float,
                            market_condition: str,
                            position_type: str,
                            signal_strength: float) -> float:
        """Calcule take profit adaptatif"""
        try:
            # Take profit de base selon force du signal
            base_tp_pct = 0.05 + (signal_strength / 100 * 0.10)  # 5% à 15%
            
            # Ajustement selon conditions marché
            market_params = self.market_conditions.get(market_condition,
                                                     self.market_conditions['sideways'])
            tp_pct = base_tp_pct * market_params['position_multiplier']
            
            # Ajustement selon profit factor
            if self.portfolio_metrics['profit_factor'] > 1.5:
                tp_pct *= 1.2  # Take profit plus ambitieux
            elif self.portfolio_metrics['profit_factor'] < 0.8:
                tp_pct *= 0.8  # Take profit plus conservateur
            
            # Calcul prix take profit
            if position_type.upper() == 'BUY':
                tp_price = entry_price * (1 + tp_pct)
            else:  # SELL
                tp_price = entry_price * (1 - tp_pct)
            
            return tp_price
            
        except Exception as e:
            logging.error(f"Erreur calcul take profit: {e}")
            # Take profit par défaut
            if position_type.upper() == 'BUY':
                return entry_price * 1.08  # +8%
            else:
                return entry_price * 0.92  # -8%
    
    def should_reduce_exposure(self, portfolio_metrics: Dict) -> bool:
        """Détermine s'il faut réduire l'exposition"""
        # Critères de réduction d'exposition
        if portfolio_metrics.get('current_drawdown', 0) > 0.15:  # 15% drawdown
            return True
        
        if portfolio_metrics.get('win_rate', 0.5) < 0.3:  # Win rate < 30%
            return True
        
        if portfolio_metrics.get('profit_factor', 1.0) < 0.5:  # Profit factor < 0.5
            return True
        
        return False
    
    def get_risk_assessment(self, symbol: str, signal_data: Dict,
                          market_data: Dict) -> Dict:
        """Évaluation complète des risques"""
        try:
            # Analyse conditions marché
            market_condition = self.analyze_market_conditions(
                market_data.get('price_data', {}),
                market_data.get('volatility_data', {})
            )
            
            # Calcul risque position
            base_position = 0.10  # 10% de base
            adjusted_position = self.adjust_position_sizing(
                base_position,
                market_condition,
                self.portfolio_metrics['current_drawdown'],
                signal_data.get('confidence', 0.5)
            )
            
            # Prix d'entrée estimé
            entry_price = market_data.get('current_prices', {}).get(symbol, 100)
            volatility = market_data.get('volatility_data', {}).get(symbol, 0.2)
            
            # Stop loss et take profit
            stop_loss = self.calculate_stop_loss(
                entry_price, market_condition, 
                signal_data.get('action', 'BUY'), volatility
            )
            
            take_profit = self.calculate_take_profit(
                entry_price, market_condition,
                signal_data.get('action', 'BUY'),
                signal_data.get('strength', 50)
            )
            
            # Score de risque global
            risk_factors = {
                'market_condition_risk': self.get_market_risk_score(market_condition),
                'portfolio_drawdown_risk': min(self.portfolio_metrics['current_drawdown'] * 10, 10),
                'volatility_risk': min(volatility * 5, 10),
                'signal_confidence_risk': (1 - signal_data.get('confidence', 0.5)) * 10
            }
            
            overall_risk_score = sum(risk_factors.values()) / len(risk_factors)
            
            return {
                'symbol': symbol,
                'risk_assessment': {
                    'overall_risk_score': overall_risk_score,
                    'risk_level': self.score_to_risk_level(overall_risk_score),
                    'risk_factors': risk_factors
                },
                'position_sizing': {
                    'recommended_position': adjusted_position,
                    'max_position_value': adjusted_position * market_data.get('portfolio_value', 1000),
                    'market_condition': market_condition
                },
                'risk_management': {
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'risk_reward_ratio': abs(take_profit - entry_price) / abs(entry_price - stop_loss)
                },
                'recommendations': {
                    'reduce_exposure': self.should_reduce_exposure(self.portfolio_metrics),
                    'wait_for_better_setup': overall_risk_score > 7,
                    'increase_monitoring': overall_risk_score > 5
                },
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logging.error(f"Erreur évaluation risque: {e}")
            return self.get_conservative_risk_assessment(symbol)
    
    def get_market_risk_score(self, market_condition: str) -> float:
        """Score de risque selon conditions marché"""
        risk_scores = {
            'bull_market': 3,
            'bear_market': 8,
            'sideways': 5,
            'high_volatility': 9,
            'low_volatility': 2
        }
        return risk_scores.get(market_condition, 5)
    
    def score_to_risk_level(self, score: float) -> str:
        """Convertit score en niveau de risque"""
        if score <= 3:
            return 'LOW'
        elif score <= 6:
            return 'MODERATE'
        elif score <= 8:
            return 'HIGH'
        else:
            return 'VERY_HIGH'
    
    def get_conservative_risk_assessment(self, symbol: str) -> Dict:
        """Évaluation conservatrice par défaut"""
        return {
            'symbol': symbol,
            'risk_assessment': {
                'overall_risk_score': 7,
                'risk_level': 'HIGH',
                'risk_factors': {'default': 7}
            },
            'position_sizing': {
                'recommended_position': 0.02,  # 2% conservateur
                'max_position_value': 20,
                'market_condition': 'unknown'
            },
            'risk_management': {
                'stop_loss': 95,
                'take_profit': 105,
                'risk_reward_ratio': 2
            },
            'recommendations': {
                'reduce_exposure': True,
                'wait_for_better_setup': True,
                'increase_monitoring': True
            },
            'timestamp': datetime.now()
        }
