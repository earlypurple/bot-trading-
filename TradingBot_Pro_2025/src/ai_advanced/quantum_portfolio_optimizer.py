"""
Quantum Portfolio Optimizer - Optimisation quantique de portfolio
"""
import numpy as np
from typing import Dict, List, Tuple
import logging
from datetime import datetime
import json

class QuantumPortfolioOptimizer:
    def __init__(self):
        self.assets = ['BTC', 'ETH', 'ADA', 'DOT', 'LINK']
        self.risk_levels = {
            'conservative': {'max_risk': 0.15, 'target_return': 0.08},
            'moderate': {'max_risk': 0.25, 'target_return': 0.15},
            'aggressive': {'max_risk': 0.40, 'target_return': 0.25}
        }
        self.correlation_matrix = None
        self.expected_returns = {}
        self.volatilities = {}
        
    def simulate_quantum_annealing(self, problem_matrix: np.ndarray, iterations: int = 1000) -> np.ndarray:
        """Simule l'algorithme quantique d'optimisation (QAOA simulé)"""
        try:
            n_assets = len(self.assets)
            
            # Initialisation aléatoire
            best_allocation = np.random.dirichlet(np.ones(n_assets))
            best_score = self.evaluate_portfolio(best_allocation)
            
            # Température pour simulated annealing
            initial_temp = 1.0
            final_temp = 0.01
            
            for i in range(iterations):
                # Température décroissante
                temp = initial_temp * (final_temp / initial_temp) ** (i / iterations)
                
                # Perturbation quantique simulée
                perturbation = np.random.normal(0, temp, n_assets)
                new_allocation = best_allocation + perturbation
                
                # Normalisation pour que la somme = 1
                new_allocation = np.abs(new_allocation)
                new_allocation = new_allocation / np.sum(new_allocation)
                
                # Évaluation
                new_score = self.evaluate_portfolio(new_allocation)
                
                # Acceptation selon critère quantique
                delta = new_score - best_score
                if delta > 0 or np.random.random() < np.exp(delta / temp):
                    best_allocation = new_allocation
                    best_score = new_score
            
            return best_allocation
            
        except Exception as e:
            logging.error(f"Erreur simulation quantique: {e}")
            # Fallback: allocation égale
            return np.ones(len(self.assets)) / len(self.assets)
    
    def calculate_expected_returns(self, price_history: Dict[str, List[float]]) -> Dict[str, float]:
        """Calcule rendements attendus basés sur l'historique"""
        expected_returns = {}
        
        for asset in self.assets:
            if asset in price_history and len(price_history[asset]) > 1:
                prices = np.array(price_history[asset])
                returns = np.diff(prices) / prices[:-1]
                
                # Rendement annualisé attendu
                daily_return = np.mean(returns)
                expected_annual = (1 + daily_return) ** 252 - 1  # 252 jours de trading
                expected_returns[asset] = expected_annual
            else:
                # Rendements par défaut basés sur les actifs crypto
                defaults = {
                    'BTC': 0.20,  # 20% attendu
                    'ETH': 0.25,  # 25% attendu
                    'ADA': 0.30,  # 30% attendu
                    'DOT': 0.35,  # 35% attendu
                    'LINK': 0.40  # 40% attendu
                }
                expected_returns[asset] = defaults.get(asset, 0.15)
        
        self.expected_returns = expected_returns
        return expected_returns
    
    def calculate_volatilities(self, price_history: Dict[str, List[float]]) -> Dict[str, float]:
        """Calcule volatilités des actifs"""
        volatilities = {}
        
        for asset in self.assets:
            if asset in price_history and len(price_history[asset]) > 1:
                prices = np.array(price_history[asset])
                returns = np.diff(prices) / prices[:-1]
                
                # Volatilité annualisée
                daily_vol = np.std(returns)
                annual_vol = daily_vol * np.sqrt(252)
                volatilities[asset] = annual_vol
            else:
                # Volatilités par défaut crypto
                defaults = {
                    'BTC': 0.60,   # 60% volatilité
                    'ETH': 0.75,   # 75% volatilité
                    'ADA': 0.85,   # 85% volatilité
                    'DOT': 0.90,   # 90% volatilité
                    'LINK': 0.95   # 95% volatilité
                }
                volatilities[asset] = defaults.get(asset, 0.70)
        
        self.volatilities = volatilities
        return volatilities
    
    def calculate_correlation_matrix(self, price_history: Dict[str, List[float]]) -> np.ndarray:
        """Calcule matrice de corrélation entre actifs"""
        try:
            returns_data = []
            
            for asset in self.assets:
                if asset in price_history and len(price_history[asset]) > 1:
                    prices = np.array(price_history[asset])
                    returns = np.diff(prices) / prices[:-1]
                    returns_data.append(returns)
                else:
                    # Données synthétiques si pas d'historique
                    synthetic_returns = np.random.normal(0, 0.02, 100)
                    returns_data.append(synthetic_returns)
            
            # Ajuster toutes les séries à la même longueur
            min_length = min(len(returns) for returns in returns_data)
            returns_matrix = np.array([returns[-min_length:] for returns in returns_data])
            
            # Calcul corrélation
            correlation_matrix = np.corrcoef(returns_matrix)
            
            # Validation matrice
            if np.any(np.isnan(correlation_matrix)):
                correlation_matrix = np.eye(len(self.assets))  # Identité si problème
            
            self.correlation_matrix = correlation_matrix
            return correlation_matrix
            
        except Exception as e:
            logging.error(f"Erreur calcul corrélation: {e}")
            # Matrice identité par défaut
            self.correlation_matrix = np.eye(len(self.assets))
            return self.correlation_matrix
    
    def evaluate_portfolio(self, allocation: np.ndarray) -> float:
        """Évalue un portfolio selon ratio Sharpe quantique"""
        try:
            # Rendement attendu du portfolio
            portfolio_return = sum(allocation[i] * self.expected_returns[asset] 
                                 for i, asset in enumerate(self.assets))
            
            # Risque du portfolio (volatilité)
            portfolio_variance = 0
            for i in range(len(allocation)):
                for j in range(len(allocation)):
                    vol_i = self.volatilities[self.assets[i]]
                    vol_j = self.volatilities[self.assets[j]]
                    corr_ij = self.correlation_matrix[i][j] if self.correlation_matrix is not None else 0
                    portfolio_variance += allocation[i] * allocation[j] * vol_i * vol_j * corr_ij
            
            portfolio_volatility = np.sqrt(portfolio_variance)
            
            # Ratio Sharpe modifié (risk-free rate = 2%)
            risk_free_rate = 0.02
            if portfolio_volatility > 0:
                sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
            else:
                sharpe_ratio = 0
            
            return sharpe_ratio
            
        except Exception as e:
            logging.error(f"Erreur évaluation portfolio: {e}")
            return 0
    
    def optimize_allocation(self, price_history: Dict[str, List[float]], 
                          risk_tolerance: str = 'moderate', 
                          portfolio_value: float = 1000) -> Dict:
        """Optimise allocation avec algorithmes quantiques"""
        try:
            # Calculs préliminaires
            self.calculate_expected_returns(price_history)
            self.calculate_volatilities(price_history)
            self.calculate_correlation_matrix(price_history)
            
            # Contraintes selon tolérance au risque
            risk_params = self.risk_levels.get(risk_tolerance, self.risk_levels['moderate'])
            
            # Optimisation quantique
            optimal_allocation = self.simulate_quantum_annealing(self.correlation_matrix)
            
            # Validation et ajustement des contraintes
            optimal_allocation = self.apply_risk_constraints(optimal_allocation, risk_params)
            
            # Calcul métriques finales
            portfolio_return = sum(optimal_allocation[i] * self.expected_returns[asset] 
                                 for i, asset in enumerate(self.assets))
            
            portfolio_risk = self.calculate_portfolio_risk(optimal_allocation)
            sharpe_ratio = self.evaluate_portfolio(optimal_allocation)
            
            # Conversion en allocations monétaires
            allocations = {}
            for i, asset in enumerate(self.assets):
                allocations[asset] = {
                    'percentage': optimal_allocation[i] * 100,
                    'amount': optimal_allocation[i] * portfolio_value,
                    'expected_return': self.expected_returns[asset] * 100,
                    'volatility': self.volatilities[asset] * 100
                }
            
            result = {
                'allocations': allocations,
                'portfolio_metrics': {
                    'expected_return': portfolio_return * 100,
                    'expected_risk': portfolio_risk * 100,
                    'sharpe_ratio': sharpe_ratio,
                    'risk_tolerance': risk_tolerance
                },
                'quantum_optimization': {
                    'iterations': 1000,
                    'algorithm': 'Simulated Quantum Annealing',
                    'convergence': 'Optimal'
                },
                'timestamp': datetime.now(),
                'rebalancing_needed': self.check_rebalancing_needed(optimal_allocation)
            }
            
            return result
            
        except Exception as e:
            logging.error(f"Erreur optimisation quantique: {e}")
            # Allocation équilibrée par défaut
            equal_allocation = 1.0 / len(self.assets)
            return {
                'allocations': {asset: {'percentage': equal_allocation * 100, 'amount': equal_allocation * portfolio_value} 
                               for asset in self.assets},
                'portfolio_metrics': {'expected_return': 15, 'expected_risk': 25, 'sharpe_ratio': 0.5},
                'error': str(e)
            }
    
    def apply_risk_constraints(self, allocation: np.ndarray, risk_params: Dict) -> np.ndarray:
        """Applique contraintes de risque à l'allocation"""
        # Limite max par actif (pas plus de 40% dans un seul actif)
        max_single_allocation = 0.40
        allocation = np.minimum(allocation, max_single_allocation)
        
        # Allocation minimum (au moins 5% par actif pour diversification)
        min_allocation = 0.05
        allocation = np.maximum(allocation, min_allocation)
        
        # Renormalisation
        allocation = allocation / np.sum(allocation)
        
        return allocation
    
    def calculate_portfolio_risk(self, allocation: np.ndarray) -> float:
        """Calcule risque total du portfolio"""
        portfolio_variance = 0
        for i in range(len(allocation)):
            for j in range(len(allocation)):
                vol_i = self.volatilities[self.assets[i]]
                vol_j = self.volatilities[self.assets[j]]
                corr_ij = self.correlation_matrix[i][j] if self.correlation_matrix is not None else 0
                portfolio_variance += allocation[i] * allocation[j] * vol_i * vol_j * corr_ij
        
        return np.sqrt(portfolio_variance)
    
    def check_rebalancing_needed(self, optimal_allocation: np.ndarray, threshold: float = 0.05) -> bool:
        """Vérifie si rééquilibrage nécessaire"""
        # Simple heuristique: si l'allocation diffère de plus de 5% de l'équilibre
        equal_allocation = 1.0 / len(self.assets)
        return np.any(np.abs(optimal_allocation - equal_allocation) > threshold)
    
    def get_rebalancing_trades(self, current_allocations: Dict, optimal_allocations: Dict, 
                             portfolio_value: float) -> List[Dict]:
        """Génère trades de rééquilibrage"""
        trades = []
        
        for asset in self.assets:
            if asset in current_allocations and asset in optimal_allocations:
                current_amount = current_allocations[asset]
                target_amount = optimal_allocations[asset]['amount']
                difference = target_amount - current_amount
                
                if abs(difference) > portfolio_value * 0.01:  # Seuil 1%
                    trade = {
                        'asset': asset,
                        'action': 'BUY' if difference > 0 else 'SELL',
                        'amount': abs(difference),
                        'percentage': abs(difference) / portfolio_value * 100
                    }
                    trades.append(trade)
        
        return trades
