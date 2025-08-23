"""
Module d'Intelligence Artificielle pour Trading Automatisé
=========================================================
IA qui analyse le marché et execute des trades automatiques selon les paramètres de l'utilisateur.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)

class TradingAI:
    """
    IA de trading automatisé avec gestion des risques.
    """
    
    def __init__(self):
        self.trading_modes = {
            'conservative': {
                'name': 'Conservateur',
                'description': 'Stratégie prudente, gains modérés, risques faibles',
                'max_risk_per_trade': 0.02,  # 2% max par trade
                'profit_target': 0.015,      # 1.5% profit target
                'stop_loss': 0.01,           # 1% stop loss
                'max_trades_per_day': 3,
                'preferred_assets': ['BTC', 'ETH', 'USDC']
            },
            'moderate': {
                'name': 'Modéré',
                'description': 'Équilibre entre risque et rendement',
                'max_risk_per_trade': 0.03,  # 3% max par trade
                'profit_target': 0.025,      # 2.5% profit target
                'stop_loss': 0.015,          # 1.5% stop loss
                'max_trades_per_day': 5,
                'preferred_assets': ['BTC', 'ETH', 'SOL', 'ATOM']
            },
            'aggressive': {
                'name': 'Agressif',
                'description': 'Gains élevés potentiels, risques plus importants',
                'max_risk_per_trade': 0.05,  # 5% max par trade
                'profit_target': 0.04,       # 4% profit target
                'stop_loss': 0.025,          # 2.5% stop loss
                'max_trades_per_day': 8,
                'preferred_assets': ['BTC', 'ETH', 'SOL', 'ATOM', 'SHIB', 'API3']
            }
        }
        
        self.daily_budget = 100.0  # Budget par défaut
        self.max_daily_loss = 50.0  # Perte maximale par défaut
        self.current_mode = 'moderate'
        self.daily_stats = {
            'trades_executed': 0,
            'total_profit_loss': 0.0,
            'successful_trades': 0,
            'failed_trades': 0,
            'last_reset': datetime.now().date()
        }
    
    def set_trading_parameters(self, mode: str, daily_budget: float, max_daily_loss: float):
        """Configure les paramètres de trading."""
        if mode in self.trading_modes:
            self.current_mode = mode
        self.daily_budget = daily_budget
        self.max_daily_loss = max_daily_loss
        
        logger.info(f"Paramètres configurés: Mode={mode}, Budget={daily_budget}$, Perte max={max_daily_loss}$")
    
    def reset_daily_stats_if_needed(self):
        """Remet à zéro les statistiques quotidiennes si nécessaire."""
        today = datetime.now().date()
        if self.daily_stats['last_reset'] != today:
            self.daily_stats = {
                'trades_executed': 0,
                'total_profit_loss': 0.0,
                'successful_trades': 0,
                'failed_trades': 0,
                'last_reset': today
            }
            logger.info("Statistiques quotidiennes remises à zéro")
    
    def analyze_market_sentiment(self, market_data: List[Dict]) -> Dict:
        """Analyse le sentiment du marché basé sur les données."""
        if not market_data:
            return {'sentiment': 'neutral', 'confidence': 0.5, 'reasoning': 'Données insuffisantes'}
        
        # Calcul du sentiment basé sur les variations 24h
        positive_changes = sum(1 for item in market_data if item.get('change_24h', 0) > 0)
        total_items = len(market_data)
        positive_ratio = positive_changes / total_items if total_items > 0 else 0.5
        
        # Calcul de la volatilité moyenne
        volatilities = []
        for item in market_data:
            high = item.get('high_24h', 0)
            low = item.get('low_24h', 0)
            price = item.get('price', 1)
            if price > 0:
                volatility = ((high - low) / price) * 100
                volatilities.append(volatility)
        
        avg_volatility = np.mean(volatilities) if volatilities else 5.0
        
        # Détermination du sentiment
        if positive_ratio > 0.7 and avg_volatility < 5:
            sentiment = 'bullish'
            confidence = 0.8
            reasoning = 'Marché haussier avec faible volatilité'
        elif positive_ratio < 0.3 and avg_volatility > 8:
            sentiment = 'bearish'
            confidence = 0.7
            reasoning = 'Marché baissier avec forte volatilité'
        elif avg_volatility > 10:
            sentiment = 'volatile'
            confidence = 0.6
            reasoning = 'Marché très volatil, prudence recommandée'
        else:
            sentiment = 'neutral'
            confidence = 0.5
            reasoning = 'Marché neutre, attente de signaux'
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'reasoning': reasoning,
            'positive_ratio': positive_ratio,
            'avg_volatility': round(avg_volatility, 2)
        }
    
    def calculate_technical_indicators(self, price_data: Dict) -> Dict:
        """Calcule des indicateurs techniques simples."""
        price = price_data.get('price', 0)
        high_24h = price_data.get('high_24h', price)
        low_24h = price_data.get('low_24h', price)
        change_24h = price_data.get('change_24h', 0)
        
        # Position dans la range 24h
        if high_24h != low_24h:
            position_in_range = (price - low_24h) / (high_24h - low_24h)
        else:
            position_in_range = 0.5
        
        # Signal basé sur la position et le momentum
        if position_in_range > 0.8 and change_24h > 2:
            signal = 'strong_buy'
            signal_strength = 0.9
        elif position_in_range > 0.6 and change_24h > 0:
            signal = 'buy'
            signal_strength = 0.7
        elif position_in_range < 0.2 and change_24h < -2:
            signal = 'strong_sell'
            signal_strength = 0.9
        elif position_in_range < 0.4 and change_24h < 0:
            signal = 'sell'
            signal_strength = 0.7
        else:
            signal = 'hold'
            signal_strength = 0.5
        
        return {
            'signal': signal,
            'signal_strength': signal_strength,
            'position_in_range': round(position_in_range, 3),
            'momentum': change_24h,
            'volatility': round(((high_24h - low_24h) / price) * 100, 2) if price > 0 else 0
        }
    
    def should_execute_trade(self) -> Tuple[bool, str]:
        """Vérifie si les conditions permettent d'exécuter un trade."""
        self.reset_daily_stats_if_needed()
        
        mode_config = self.trading_modes[self.current_mode]
        
        # Vérification du nombre de trades quotidiens
        if self.daily_stats['trades_executed'] >= mode_config['max_trades_per_day']:
            return False, f"Limite quotidienne de {mode_config['max_trades_per_day']} trades atteinte"
        
        # Vérification des pertes quotidiennes
        if abs(self.daily_stats['total_profit_loss']) >= self.max_daily_loss:
            return False, f"Perte quotidienne maximale de {self.max_daily_loss}$ atteinte"
        
        # Vérification du budget disponible
        trade_amount = self.daily_budget * mode_config['max_risk_per_trade']
        if trade_amount <= 0:
            return False, "Budget insuffisant pour trader"
        
        return True, "Conditions favorables au trading"
    
    def generate_trade_recommendation(self, symbol: str, market_data: List[Dict], portfolio_data: Dict) -> Dict:
        """Génère une recommandation de trade basée sur l'analyse IA."""
        try:
            # Analyse du sentiment général du marché
            market_sentiment = self.analyze_market_sentiment(market_data)
            
            # Recherche des données de l'actif spécifique
            asset_data = None
            for item in market_data:
                if item['symbol'] == symbol:
                    asset_data = item
                    break
            
            if not asset_data:
                return {
                    'action': 'hold',
                    'confidence': 0.0,
                    'reasoning': f'Données non disponibles pour {symbol}',
                    'recommended_amount': 0,
                    'risk_level': 'unknown'
                }
            
            # Analyse technique de l'actif
            technical_analysis = self.calculate_technical_indicators(asset_data)
            
            # Configuration du mode de trading
            mode_config = self.trading_modes[self.current_mode]
            
            # Vérification des conditions de trading
            can_trade, trade_status = self.should_execute_trade()
            
            if not can_trade:
                return {
                    'action': 'hold',
                    'confidence': 0.0,
                    'reasoning': trade_status,
                    'recommended_amount': 0,
                    'risk_level': 'blocked'
                }
            
            # Calcul du montant recommandé
            base_amount = self.daily_budget * mode_config['max_risk_per_trade']
            
            # Ajustement basé sur la confiance et le sentiment
            confidence_multiplier = (market_sentiment['confidence'] + technical_analysis['signal_strength']) / 2
            recommended_amount = base_amount * confidence_multiplier
            
            # Détermination de l'action
            if (technical_analysis['signal'] in ['strong_buy', 'buy'] and 
                market_sentiment['sentiment'] in ['bullish', 'neutral'] and
                technical_analysis['signal_strength'] > 0.6):
                action = 'buy'
                confidence = min(0.9, confidence_multiplier + 0.1)
            elif (technical_analysis['signal'] in ['strong_sell', 'sell'] and
                  market_sentiment['sentiment'] in ['bearish', 'volatile'] and
                  technical_analysis['signal_strength'] > 0.6):
                action = 'sell'
                confidence = min(0.9, confidence_multiplier + 0.1)
            else:
                action = 'hold'
                confidence = 0.5
            
            # Construction du raisonnement
            reasoning_parts = [
                f"Sentiment marché: {market_sentiment['sentiment']} ({market_sentiment['reasoning']})",
                f"Signal technique: {technical_analysis['signal']} (force: {technical_analysis['signal_strength']:.1f})",
                f"Volatilité: {technical_analysis['volatility']:.1f}%",
                f"Position dans range 24h: {technical_analysis['position_in_range']:.1%}"
            ]
            
            return {
                'action': action,
                'confidence': round(confidence, 2),
                'reasoning': ' | '.join(reasoning_parts),
                'recommended_amount': round(recommended_amount, 4),
                'risk_level': self.current_mode,
                'market_sentiment': market_sentiment,
                'technical_analysis': technical_analysis,
                'stop_loss_pct': mode_config['stop_loss'] * 100,
                'profit_target_pct': mode_config['profit_target'] * 100
            }
            
        except Exception as e:
            logger.error(f"Erreur dans la génération de recommandation: {str(e)}")
            return {
                'action': 'hold',
                'confidence': 0.0,
                'reasoning': f'Erreur d\'analyse: {str(e)[:100]}',
                'recommended_amount': 0,
                'risk_level': 'error'
            }
    
    def update_trade_result(self, profit_loss: float, success: bool):
        """Met à jour les statistiques après un trade."""
        self.reset_daily_stats_if_needed()
        
        self.daily_stats['trades_executed'] += 1
        self.daily_stats['total_profit_loss'] += profit_loss
        
        if success:
            self.daily_stats['successful_trades'] += 1
        else:
            self.daily_stats['failed_trades'] += 1
        
        logger.info(f"Trade résultat: {'Succès' if success else 'Échec'}, P&L: {profit_loss:.2f}$")
    
    def get_daily_summary(self) -> Dict:
        """Retourne un résumé des performances quotidiennes."""
        self.reset_daily_stats_if_needed()
        
        success_rate = 0
        if self.daily_stats['trades_executed'] > 0:
            success_rate = (self.daily_stats['successful_trades'] / self.daily_stats['trades_executed']) * 100
        
        mode_config = self.trading_modes[self.current_mode]
        
        return {
            'mode': self.current_mode,
            'mode_name': mode_config['name'],
            'daily_budget': self.daily_budget,
            'max_daily_loss': self.max_daily_loss,
            'trades_executed': self.daily_stats['trades_executed'],
            'max_trades_per_day': mode_config['max_trades_per_day'],
            'successful_trades': self.daily_stats['successful_trades'],
            'failed_trades': self.daily_stats['failed_trades'],
            'success_rate': round(success_rate, 1),
            'total_profit_loss': round(self.daily_stats['total_profit_loss'], 2),
            'remaining_budget': round(self.daily_budget - abs(self.daily_stats['total_profit_loss']), 2),
            'status': 'active' if abs(self.daily_stats['total_profit_loss']) < self.max_daily_loss else 'stopped'
        }

# Instance globale de l'IA
trading_ai = TradingAI()
