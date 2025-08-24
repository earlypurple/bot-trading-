"""
Multi-Timeframe Predictor - Prédictions IA sur plusieurs timeframes
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Tuple
import asyncio

class MultiTimeframePredictor:
    def __init__(self):
        self.timeframes = ['1m', '5m', '15m', '1h', '4h', '1d']
        self.ensemble_models = {}
        self.weights = {
            '1m': 0.05,    # Court terme
            '5m': 0.10,    # Scalping
            '15m': 0.15,   # Trading rapide
            '1h': 0.25,    # Trading moyen terme
            '4h': 0.30,    # Swing trading
            '1d': 0.15     # Tendance long terme
        }
        self.predictions_cache = {}
        self.last_update = {}
        
    def calculate_technical_indicators(self, prices: List[float], timeframe: str) -> Dict:
        """Calcule indicateurs techniques adaptés au timeframe"""
        if len(prices) < 20:
            return {}
            
        df = pd.DataFrame({'price': prices})
        
        # Périodes adaptées au timeframe
        periods = self.get_adaptive_periods(timeframe)
        
        indicators = {}
        
        # RSI adaptatif
        delta = df['price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=periods['rsi']).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods['rsi']).mean()
        rs = gain / loss
        indicators['rsi'] = 100 - (100 / (1 + rs)).iloc[-1]
        
        # MACD adaptatif
        ema_fast = df['price'].ewm(span=periods['macd_fast']).mean()
        ema_slow = df['price'].ewm(span=periods['macd_slow']).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=periods['macd_signal']).mean()
        indicators['macd'] = macd_line.iloc[-1]
        indicators['macd_signal'] = signal_line.iloc[-1]
        indicators['macd_histogram'] = (macd_line - signal_line).iloc[-1]
        
        # Bollinger Bands adaptatifs
        sma = df['price'].rolling(window=periods['bb']).mean()
        std = df['price'].rolling(window=periods['bb']).std()
        indicators['bb_upper'] = (sma + 2 * std).iloc[-1]
        indicators['bb_lower'] = (sma - 2 * std).iloc[-1]
        indicators['bb_position'] = (prices[-1] - indicators['bb_lower']) / (indicators['bb_upper'] - indicators['bb_lower'])
        
        # Momentum adaptatif
        indicators['momentum'] = (prices[-1] / prices[-periods['momentum']] - 1) * 100
        
        # Volume momentum (simulé basé sur volatilité)
        volatility = df['price'].pct_change().rolling(window=periods['volume']).std()
        indicators['volume_momentum'] = volatility.iloc[-1] * 100
        
        return indicators
    
    def get_adaptive_periods(self, timeframe: str) -> Dict[str, int]:
        """Retourne périodes adaptées au timeframe"""
        base_periods = {
            '1m': {'rsi': 14, 'macd_fast': 12, 'macd_slow': 26, 'macd_signal': 9, 'bb': 20, 'momentum': 10, 'volume': 14},
            '5m': {'rsi': 14, 'macd_fast': 12, 'macd_slow': 26, 'macd_signal': 9, 'bb': 20, 'momentum': 14, 'volume': 20},
            '15m': {'rsi': 14, 'macd_fast': 12, 'macd_slow': 26, 'macd_signal': 9, 'bb': 20, 'momentum': 20, 'volume': 30},
            '1h': {'rsi': 14, 'macd_fast': 12, 'macd_slow': 26, 'macd_signal': 9, 'bb': 20, 'momentum': 24, 'volume': 50},
            '4h': {'rsi': 14, 'macd_fast': 12, 'macd_slow': 26, 'macd_signal': 9, 'bb': 20, 'momentum': 50, 'volume': 100},
            '1d': {'rsi': 14, 'macd_fast': 12, 'macd_slow': 26, 'macd_signal': 9, 'bb': 20, 'momentum': 100, 'volume': 200}
        }
        return base_periods.get(timeframe, base_periods['1h'])
    
    def predict_timeframe(self, symbol: str, timeframe: str, prices: List[float]) -> Dict:
        """Prédiction pour un timeframe spécifique"""
        try:
            indicators = self.calculate_technical_indicators(prices, timeframe)
            if not indicators:
                return {'signal': 'HOLD', 'confidence': 0.0, 'strength': 0.0}
            
            # Calcul du signal basé sur les indicateurs
            signals = []
            weights = []
            
            # Signal RSI
            if indicators.get('rsi'):
                if indicators['rsi'] > 70:
                    signals.append(-1)  # SELL
                elif indicators['rsi'] < 30:
                    signals.append(1)   # BUY
                else:
                    signals.append(0)   # HOLD
                weights.append(0.25)
            
            # Signal MACD
            if indicators.get('macd') and indicators.get('macd_signal'):
                if indicators['macd'] > indicators['macd_signal']:
                    signals.append(1)   # BUY
                else:
                    signals.append(-1)  # SELL
                weights.append(0.30)
            
            # Signal Bollinger Bands
            if indicators.get('bb_position'):
                if indicators['bb_position'] > 0.8:
                    signals.append(-1)  # SELL
                elif indicators['bb_position'] < 0.2:
                    signals.append(1)   # BUY
                else:
                    signals.append(0)   # HOLD
                weights.append(0.20)
            
            # Signal Momentum
            if indicators.get('momentum'):
                if indicators['momentum'] > 5:
                    signals.append(1)   # BUY
                elif indicators['momentum'] < -5:
                    signals.append(-1)  # SELL
                else:
                    signals.append(0)   # HOLD
                weights.append(0.25)
            
            # Calcul signal final pondéré
            if signals and weights:
                weighted_signal = sum(s * w for s, w in zip(signals, weights)) / sum(weights)
                
                # Conversion en signal et force
                if weighted_signal > 0.3:
                    signal = 'BUY'
                    strength = min(abs(weighted_signal) * 100, 100)
                elif weighted_signal < -0.3:
                    signal = 'SELL'
                    strength = min(abs(weighted_signal) * 100, 100)
                else:
                    signal = 'HOLD'
                    strength = 0
                
                # Confiance basée sur convergence des signaux
                confidence = 1.0 - (np.std(signals) / 2.0) if len(signals) > 1 else 0.5
                
                return {
                    'signal': signal,
                    'confidence': confidence,
                    'strength': strength,
                    'timeframe': timeframe,
                    'indicators': indicators
                }
            
            return {'signal': 'HOLD', 'confidence': 0.0, 'strength': 0.0}
            
        except Exception as e:
            logging.error(f"Erreur prédiction {timeframe}: {e}")
            return {'signal': 'HOLD', 'confidence': 0.0, 'strength': 0.0}
    
    def predict_ensemble(self, symbol: str, price_data: Dict[str, List[float]]) -> Dict:
        """Combine prédictions de plusieurs timeframes"""
        try:
            predictions = {}
            
            # Prédictions pour chaque timeframe
            for timeframe in self.timeframes:
                if timeframe in price_data and price_data[timeframe]:
                    pred = self.predict_timeframe(symbol, timeframe, price_data[timeframe])
                    predictions[timeframe] = pred
            
            if not predictions:
                return {'signal': 'HOLD', 'confidence': 0.0, 'strength': 0.0}
            
            # Combinaison pondérée des signaux
            weighted_signals = []
            total_weight = 0
            confidence_sum = 0
            
            for timeframe, pred in predictions.items():
                if pred['confidence'] > 0.3:  # Seuil minimum de confiance
                    weight = self.weights[timeframe] * pred['confidence']
                    
                    if pred['signal'] == 'BUY':
                        weighted_signals.append(pred['strength'] * weight)
                    elif pred['signal'] == 'SELL':
                        weighted_signals.append(-pred['strength'] * weight)
                    else:
                        weighted_signals.append(0)
                    
                    total_weight += weight
                    confidence_sum += pred['confidence']
            
            if not weighted_signals or total_weight == 0:
                return {'signal': 'HOLD', 'confidence': 0.0, 'strength': 0.0}
            
            # Signal final
            final_signal_strength = sum(weighted_signals) / total_weight
            final_confidence = confidence_sum / len(predictions)
            
            if final_signal_strength > 20:
                final_signal = 'BUY'
            elif final_signal_strength < -20:
                final_signal = 'SELL'
            else:
                final_signal = 'HOLD'
            
            result = {
                'signal': final_signal,
                'confidence': final_confidence,
                'strength': abs(final_signal_strength),
                'timeframe_predictions': predictions,
                'ensemble_strength': final_signal_strength
            }
            
            # Cache du résultat
            self.predictions_cache[symbol] = result
            self.last_update[symbol] = datetime.now()
            
            return result
            
        except Exception as e:
            logging.error(f"Erreur ensemble prediction: {e}")
            return {'signal': 'HOLD', 'confidence': 0.0, 'strength': 0.0}
    
    def get_cached_prediction(self, symbol: str, max_age_minutes: int = 2) -> Dict:
        """Récupère prédiction en cache si récente"""
        if symbol in self.predictions_cache and symbol in self.last_update:
            age = datetime.now() - self.last_update[symbol]
            if age.total_seconds() < max_age_minutes * 60:
                return self.predictions_cache[symbol]
        return None
    
    def is_trend_alignment(self, predictions: Dict) -> bool:
        """Vérifie alignement des tendances entre timeframes"""
        signals = []
        for timeframe in ['15m', '1h', '4h']:
            if timeframe in predictions:
                pred = predictions[timeframe]
                if pred['signal'] == 'BUY':
                    signals.append(1)
                elif pred['signal'] == 'SELL':
                    signals.append(-1)
                else:
                    signals.append(0)
        
        if len(signals) >= 2:
            # Vérifier si au moins 2 timeframes sont alignés
            return len(set(signals)) <= 2 and 0 not in set(signals)
        return False
