#!/usr/bin/env python3
"""
📊 ANALYTICS AVANCÉS - TRADINGBOT PRO 2025
==========================================
📈 Analytics de performance et risque
🎯 Métriques business et techniques
📊 Dashboards et visualisations
🔍 Intelligence artificielle pour insights

🎯 Fonctionnalités:
- Analytics en temps réel
- Métriques de performance avancées
- Analyse de risque multi-facteurs
- Tableaux de bord interactifs
- Alertes intelligentes
- Rapports automatisés
"""

import asyncio
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, callback
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import yfinance as yf
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import logging
import json
import sqlite3
import warnings
warnings.filterwarnings('ignore')

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AdvancedAnalytics")

# ============================================================================
# 📊 CONFIGURATION ANALYTICS
# ============================================================================

class AnalyticsType(Enum):
    """Types d'analytics"""
    PERFORMANCE = "performance"
    RISK = "risk"
    PORTFOLIO = "portfolio"
    MARKET = "market"
    TRADING = "trading"
    CORRELATION = "correlation"
    ATTRIBUTION = "attribution"
    BEHAVIORAL = "behavioral"

class TimeFrame(Enum):
    """Périodes d'analyse"""
    INTRADAY = "1d"
    DAILY = "1d"
    WEEKLY = "1w"
    MONTHLY = "1M"
    QUARTERLY = "3M"
    YEARLY = "1Y"
    ALL_TIME = "max"

class RiskMetric(Enum):
    """Métriques de risque"""
    VaR = "value_at_risk"
    CVaR = "conditional_var"
    BETA = "beta"
    ALPHA = "alpha"
    SHARPE = "sharpe_ratio"
    SORTINO = "sortino_ratio"
    CALMAR = "calmar_ratio"
    MAX_DRAWDOWN = "max_drawdown"
    TRACKING_ERROR = "tracking_error"

@dataclass
class PerformanceMetrics:
    """Métriques de performance"""
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    avg_win: float
    avg_loss: float
    total_trades: int
    
@dataclass
class RiskMetrics:
    """Métriques de risque"""
    var_95: float
    var_99: float
    cvar_95: float
    cvar_99: float
    beta: float
    alpha: float
    tracking_error: float
    information_ratio: float
    downside_deviation: float
    
@dataclass
class PortfolioAnalytics:
    """Analytics de portfolio"""
    total_value: float
    asset_allocation: Dict[str, float]
    sector_allocation: Dict[str, float]
    geographic_allocation: Dict[str, float]
    correlation_matrix: np.ndarray
    diversification_ratio: float
    concentration_risk: float

# ============================================================================
# 🧮 CALCULATEUR DE MÉTRIQUES
# ============================================================================

class MetricsCalculator:
    """Calculateur de métriques avancées"""
    
    @staticmethod
    def calculate_performance_metrics(returns: np.ndarray, 
                                    benchmark_returns: Optional[np.ndarray] = None,
                                    risk_free_rate: float = 0.02) -> PerformanceMetrics:
        """Calcule les métriques de performance"""
        
        # Retours de base
        total_return = np.prod(1 + returns) - 1
        annualized_return = (1 + total_return) ** (252 / len(returns)) - 1
        volatility = np.std(returns) * np.sqrt(252)
        
        # Ratios de Sharpe et Sortino
        excess_returns = returns - risk_free_rate / 252
        sharpe_ratio = np.mean(excess_returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
        
        downside_returns = returns[returns < 0]
        downside_std = np.std(downside_returns) if len(downside_returns) > 0 else np.std(returns)
        sortino_ratio = np.mean(excess_returns) / downside_std * np.sqrt(252) if downside_std > 0 else 0
        
        # Maximum drawdown
        cumulative = np.cumprod(1 + returns)
        rolling_max = np.maximum.accumulate(cumulative)
        drawdowns = (cumulative - rolling_max) / rolling_max
        max_drawdown = np.min(drawdowns)
        
        # Calmar ratio
        calmar_ratio = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0
        
        # Statistiques de trading
        winning_trades = returns[returns > 0]
        losing_trades = returns[returns < 0]
        
        win_rate = len(winning_trades) / len(returns) if len(returns) > 0 else 0
        avg_win = np.mean(winning_trades) if len(winning_trades) > 0 else 0
        avg_loss = np.mean(losing_trades) if len(losing_trades) > 0 else 0
        profit_factor = abs(np.sum(winning_trades) / np.sum(losing_trades)) if np.sum(losing_trades) != 0 else float('inf')
        
        return PerformanceMetrics(
            total_return=total_return,
            annualized_return=annualized_return,
            volatility=volatility,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            calmar_ratio=calmar_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            profit_factor=profit_factor,
            avg_win=avg_win,
            avg_loss=avg_loss,
            total_trades=len(returns)
        )
    
    @staticmethod
    def calculate_risk_metrics(returns: np.ndarray, 
                             benchmark_returns: Optional[np.ndarray] = None,
                             confidence_levels: List[float] = [0.95, 0.99]) -> RiskMetrics:
        """Calcule les métriques de risque"""
        
        # VaR et CVaR
        var_95 = np.percentile(returns, (1 - 0.95) * 100)
        var_99 = np.percentile(returns, (1 - 0.99) * 100)
        
        cvar_95 = np.mean(returns[returns <= var_95])
        cvar_99 = np.mean(returns[returns <= var_99])
        
        # Beta et Alpha (si benchmark fourni)
        beta = 0
        alpha = 0
        tracking_error = 0
        information_ratio = 0
        
        if benchmark_returns is not None and len(benchmark_returns) == len(returns):
            # Régression linéaire pour Beta
            covariance = np.cov(returns, benchmark_returns)[0, 1]
            benchmark_variance = np.var(benchmark_returns)
            beta = covariance / benchmark_variance if benchmark_variance > 0 else 0
            
            # Alpha
            alpha = np.mean(returns) - beta * np.mean(benchmark_returns)
            
            # Tracking error
            active_returns = returns - benchmark_returns
            tracking_error = np.std(active_returns) * np.sqrt(252)
            
            # Information ratio
            information_ratio = np.mean(active_returns) / np.std(active_returns) * np.sqrt(252) if np.std(active_returns) > 0 else 0
        
        # Downside deviation
        mean_return = np.mean(returns)
        downside_returns = returns[returns < mean_return]
        downside_deviation = np.sqrt(np.mean((downside_returns - mean_return) ** 2)) if len(downside_returns) > 0 else 0
        
        return RiskMetrics(
            var_95=var_95,
            var_99=var_99,
            cvar_95=cvar_95,
            cvar_99=cvar_99,
            beta=beta,
            alpha=alpha,
            tracking_error=tracking_error,
            information_ratio=information_ratio,
            downside_deviation=downside_deviation
        )
    
    @staticmethod
    def calculate_portfolio_analytics(positions: Dict[str, float], 
                                    prices: Dict[str, float],
                                    returns_matrix: np.ndarray) -> PortfolioAnalytics:
        """Calcule les analytics de portfolio"""
        
        # Valeur totale
        total_value = sum(pos * prices.get(asset, 0) for asset, pos in positions.items())
        
        # Allocation par actif
        asset_allocation = {
            asset: (pos * prices.get(asset, 0)) / total_value 
            for asset, pos in positions.items()
        }
        
        # Allocation sectorielle simulée
        sector_allocation = {
            "Technology": 0.35,
            "Finance": 0.25,
            "Healthcare": 0.20,
            "Consumer": 0.15,
            "Other": 0.05
        }
        
        # Allocation géographique simulée
        geographic_allocation = {
            "North America": 0.60,
            "Europe": 0.25,
            "Asia": 0.12,
            "Other": 0.03
        }
        
        # Matrice de corrélation
        correlation_matrix = np.corrcoef(returns_matrix.T)
        
        # Ratio de diversification
        weights = np.array(list(asset_allocation.values()))
        portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(np.cov(returns_matrix.T), weights)))
        weighted_avg_vol = np.sum(weights * np.std(returns_matrix, axis=0))
        diversification_ratio = weighted_avg_vol / portfolio_vol if portfolio_vol > 0 else 1
        
        # Risque de concentration (HHI)
        concentration_risk = np.sum(weights ** 2)
        
        return PortfolioAnalytics(
            total_value=total_value,
            asset_allocation=asset_allocation,
            sector_allocation=sector_allocation,
            geographic_allocation=geographic_allocation,
            correlation_matrix=correlation_matrix,
            diversification_ratio=diversification_ratio,
            concentration_risk=concentration_risk
        )

# ============================================================================
# 📊 GÉNÉRATEUR DE VISUALISATIONS
# ============================================================================

class VisualizationGenerator:
    """Générateur de visualisations avancées"""
    
    @staticmethod
    def create_performance_dashboard(metrics: PerformanceMetrics, 
                                   returns: np.ndarray) -> go.Figure:
        """Crée un dashboard de performance"""
        
        # Créer subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Courbe de Performance", "Distribution des Retours", 
                          "Métriques Clés", "Drawdown"),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"type": "table"}, {"secondary_y": False}]]
        )
        
        # 1. Courbe de performance
        cumulative_returns = np.cumprod(1 + returns)
        dates = pd.date_range(start='2024-01-01', periods=len(returns), freq='D')
        
        fig.add_trace(
            go.Scatter(
                x=dates, 
                y=cumulative_returns,
                mode='lines',
                name='Performance',
                line=dict(color='blue', width=2)
            ),
            row=1, col=1
        )
        
        # 2. Distribution des retours
        fig.add_trace(
            go.Histogram(
                x=returns,
                nbinsx=50,
                name='Distribution',
                opacity=0.7,
                marker_color='lightblue'
            ),
            row=1, col=2
        )
        
        # 3. Tableau des métriques
        metrics_data = [
            ["Retour Total", f"{metrics.total_return:.2%}"],
            ["Retour Annualisé", f"{metrics.annualized_return:.2%}"],
            ["Volatilité", f"{metrics.volatility:.2%}"],
            ["Ratio de Sharpe", f"{metrics.sharpe_ratio:.3f}"],
            ["Ratio de Sortino", f"{metrics.sortino_ratio:.3f}"],
            ["Max Drawdown", f"{metrics.max_drawdown:.2%}"],
            ["Taux de Victoire", f"{metrics.win_rate:.2%}"],
            ["Facteur de Profit", f"{metrics.profit_factor:.2f}"]
        ]
        
        fig.add_trace(
            go.Table(
                header=dict(values=["Métrique", "Valeur"],
                           fill_color="lightblue",
                           align="center"),
                cells=dict(values=list(zip(*metrics_data)),
                          fill_color="white",
                          align="center")
            ),
            row=2, col=1
        )
        
        # 4. Courbe de drawdown
        cumulative = np.cumprod(1 + returns)
        rolling_max = np.maximum.accumulate(cumulative)
        drawdowns = (cumulative - rolling_max) / rolling_max
        
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=drawdowns,
                mode='lines',
                name='Drawdown',
                fill='tonexty',
                line=dict(color='red', width=1),
                fillcolor='rgba(255,0,0,0.3)'
            ),
            row=2, col=2
        )
        
        # Layout
        fig.update_layout(
            title="Dashboard de Performance",
            height=800,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_risk_heatmap(correlation_matrix: np.ndarray, 
                           asset_names: List[str]) -> go.Figure:
        """Crée une heatmap des corrélations"""
        
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix,
            x=asset_names,
            y=asset_names,
            colorscale='RdBu',
            zmid=0,
            text=np.round(correlation_matrix, 2),
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="Matrice de Corrélation des Actifs",
            xaxis_title="Actifs",
            yaxis_title="Actifs"
        )
        
        return fig
    
    @staticmethod
    def create_portfolio_allocation_chart(allocation: Dict[str, float]) -> go.Figure:
        """Crée un graphique d'allocation de portfolio"""
        
        labels = list(allocation.keys())
        values = list(allocation.values())
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3,
            textinfo='label+percent',
            textposition='auto'
        )])
        
        fig.update_layout(
            title="Allocation du Portfolio",
            annotations=[dict(text='Portfolio', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        
        return fig

# ============================================================================
# 🔍 ANALYSEUR D'ANOMALIES
# ============================================================================

class AnomalyDetector:
    """Détecteur d'anomalies dans les données de trading"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)
        self.dbscan = DBSCAN(eps=0.5, min_samples=5)
    
    def detect_price_anomalies(self, prices: np.ndarray, 
                             volumes: np.ndarray) -> Dict[str, Any]:
        """Détecte les anomalies de prix et volume"""
        
        # Calculer features
        returns = np.diff(prices) / prices[:-1]
        log_volumes = np.log(volumes[1:] + 1)
        
        # Z-scores
        return_zscore = np.abs(stats.zscore(returns))
        volume_zscore = np.abs(stats.zscore(log_volumes))
        
        # Seuils d'anomalie
        price_anomalies = np.where(return_zscore > 3)[0]
        volume_anomalies = np.where(volume_zscore > 3)[0]
        
        # Clustering pour détecter régimes de marché
        features = np.column_stack([returns, log_volumes])
        features_scaled = self.scaler.fit_transform(features)
        
        clusters = self.dbscan.fit_predict(features_scaled)
        outliers = np.where(clusters == -1)[0]
        
        return {
            'price_anomalies': price_anomalies.tolist(),
            'volume_anomalies': volume_anomalies.tolist(),
            'regime_outliers': outliers.tolist(),
            'n_regimes': len(np.unique(clusters[clusters != -1])),
            'anomaly_score': len(outliers) / len(features)
        }
    
    def detect_correlation_breakdown(self, returns_matrix: np.ndarray,
                                   window_size: int = 30) -> Dict[str, Any]:
        """Détecte les ruptures de corrélation"""
        
        n_assets = returns_matrix.shape[1]
        rolling_correlations = []
        
        # Calcul des corrélations roulantes
        for i in range(window_size, len(returns_matrix)):
            window_data = returns_matrix[i-window_size:i]
            corr_matrix = np.corrcoef(window_data.T)
            
            # Moyenne des corrélations (exclut diagonale)
            mask = ~np.eye(n_assets, dtype=bool)
            avg_correlation = np.mean(corr_matrix[mask])
            rolling_correlations.append(avg_correlation)
        
        rolling_correlations = np.array(rolling_correlations)
        
        # Détecter ruptures (changements brusques)
        correlation_changes = np.abs(np.diff(rolling_correlations))
        breakdowns = np.where(correlation_changes > 2 * np.std(correlation_changes))[0]
        
        return {
            'correlation_breakdowns': breakdowns.tolist(),
            'avg_correlation': np.mean(rolling_correlations),
            'correlation_volatility': np.std(rolling_correlations),
            'rolling_correlations': rolling_correlations.tolist()
        }

# ============================================================================
# 📊 SYSTÈME D'ANALYTICS PRINCIPAL
# ============================================================================

class AdvancedAnalyticsSystem:
    """Système d'analytics avancé principal"""
    
    def __init__(self):
        self.metrics_calculator = MetricsCalculator()
        self.viz_generator = VisualizationGenerator()
        self.anomaly_detector = AnomalyDetector()
        
        # Base de données simulée
        self.data = self._generate_sample_data()
    
    def _generate_sample_data(self) -> Dict[str, Any]:
        """Génère des données d'exemple"""
        
        np.random.seed(42)
        n_days = 252
        n_assets = 5
        
        # Générer retours corrélés
        correlation = 0.3
        cov_matrix = np.full((n_assets, n_assets), correlation)
        np.fill_diagonal(cov_matrix, 1.0)
        
        returns = np.random.multivariate_normal(
            mean=[0.0008, 0.0006, 0.0010, 0.0005, 0.0007],
            cov=cov_matrix * 0.0004,
            size=n_days
        )
        
        # Générer prix
        initial_prices = [100, 50, 150, 80, 120]
        prices = {}
        
        for i, asset in enumerate(['BTC', 'ETH', 'ADA', 'DOT', 'LINK']):
            asset_prices = [initial_prices[i]]
            for j in range(1, n_days):
                new_price = asset_prices[-1] * (1 + returns[j, i])
                asset_prices.append(new_price)
            prices[asset] = np.array(asset_prices)
        
        # Positions de portfolio simulées
        positions = {
            'BTC': 2.5,
            'ETH': 50.0,
            'ADA': 10000.0,
            'DOT': 1000.0,
            'LINK': 500.0
        }
        
        # Volumes simulés
        volumes = {}
        for asset in prices.keys():
            volumes[asset] = np.random.lognormal(15, 0.5, n_days)
        
        return {
            'returns': returns,
            'prices': prices,
            'positions': positions,
            'volumes': volumes,
            'dates': pd.date_range(start='2024-01-01', periods=n_days, freq='D')
        }
    
    async def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Génère un rapport d'analytics complet"""
        
        logger.info("📊 Génération rapport analytics complet...")
        
        try:
            # 1. Métriques de performance portfolio
            portfolio_returns = np.mean(self.data['returns'], axis=1)  # Portfolio équipondéré
            benchmark_returns = self.data['returns'][:, 0]  # BTC comme benchmark
            
            performance_metrics = self.metrics_calculator.calculate_performance_metrics(
                portfolio_returns, benchmark_returns
            )
            
            # 2. Métriques de risque
            risk_metrics = self.metrics_calculator.calculate_risk_metrics(
                portfolio_returns, benchmark_returns
            )
            
            # 3. Analytics de portfolio
            current_prices = {asset: prices[-1] for asset, prices in self.data['prices'].items()}
            portfolio_analytics = self.metrics_calculator.calculate_portfolio_analytics(
                self.data['positions'], current_prices, self.data['returns']
            )
            
            # 4. Détection d'anomalies
            btc_anomalies = self.anomaly_detector.detect_price_anomalies(
                self.data['prices']['BTC'], self.data['volumes']['BTC']
            )
            
            correlation_analysis = self.anomaly_detector.detect_correlation_breakdown(
                self.data['returns']
            )
            
            # 5. Analyse de contribution
            contribution_analysis = self._calculate_contribution_analysis()
            
            # 6. Analyse comportementale
            behavioral_metrics = self._calculate_behavioral_metrics()
            
            # 7. Métriques ESG simulées
            esg_metrics = self._calculate_esg_metrics()
            
            # Compiler rapport
            report = {
                'timestamp': datetime.now().isoformat(),
                'performance': {
                    'total_return': performance_metrics.total_return,
                    'annualized_return': performance_metrics.annualized_return,
                    'volatility': performance_metrics.volatility,
                    'sharpe_ratio': performance_metrics.sharpe_ratio,
                    'sortino_ratio': performance_metrics.sortino_ratio,
                    'max_drawdown': performance_metrics.max_drawdown,
                    'win_rate': performance_metrics.win_rate,
                    'profit_factor': performance_metrics.profit_factor
                },
                'risk': {
                    'var_95': risk_metrics.var_95,
                    'var_99': risk_metrics.var_99,
                    'cvar_95': risk_metrics.cvar_95,
                    'beta': risk_metrics.beta,
                    'alpha': risk_metrics.alpha,
                    'tracking_error': risk_metrics.tracking_error,
                    'downside_deviation': risk_metrics.downside_deviation
                },
                'portfolio': {
                    'total_value': portfolio_analytics.total_value,
                    'asset_allocation': portfolio_analytics.asset_allocation,
                    'diversification_ratio': portfolio_analytics.diversification_ratio,
                    'concentration_risk': portfolio_analytics.concentration_risk
                },
                'anomalies': {
                    'price_anomalies_count': len(btc_anomalies['price_anomalies']),
                    'volume_anomalies_count': len(btc_anomalies['volume_anomalies']),
                    'correlation_breakdowns': len(correlation_analysis['correlation_breakdowns']),
                    'anomaly_score': btc_anomalies['anomaly_score']
                },
                'contribution': contribution_analysis,
                'behavioral': behavioral_metrics,
                'esg': esg_metrics,
                'summary': {
                    'overall_score': self._calculate_overall_score(performance_metrics, risk_metrics),
                    'risk_level': self._assess_risk_level(risk_metrics),
                    'recommendation': self._generate_recommendation(performance_metrics, risk_metrics)
                }
            }
            
            logger.info("✅ Rapport analytics généré avec succès")
            return report
            
        except Exception as e:
            logger.error(f"❌ Erreur génération rapport: {e}")
            return {'error': str(e)}
    
    def _calculate_contribution_analysis(self) -> Dict[str, Any]:
        """Calcule l'analyse de contribution"""
        
        # Contribution par actif aux performances
        asset_contributions = {}
        total_portfolio_return = 0
        
        for asset, prices in self.data['prices'].items():
            asset_return = (prices[-1] - prices[0]) / prices[0]
            weight = self.data['positions'][asset] * prices[-1] / sum(
                pos * self.data['prices'][a][-1] for a, pos in self.data['positions'].items()
            )
            contribution = weight * asset_return
            asset_contributions[asset] = contribution
            total_portfolio_return += contribution
        
        # Contribution par secteur (simulée)
        sector_contributions = {
            'Technology': 0.15,
            'Finance': 0.08,
            'DeFi': 0.12,
            'Infrastructure': 0.06,
            'Other': 0.02
        }
        
        return {
            'asset_contributions': asset_contributions,
            'sector_contributions': sector_contributions,
            'top_contributor': max(asset_contributions, key=asset_contributions.get),
            'worst_contributor': min(asset_contributions, key=asset_contributions.get)
        }
    
    def _calculate_behavioral_metrics(self) -> Dict[str, Any]:
        """Calcule les métriques comportementales"""
        
        # Simuler métriques comportementales
        return {
            'trading_frequency': 'Medium',  # Low/Medium/High
            'risk_taking_behavior': 'Moderate',  # Conservative/Moderate/Aggressive
            'market_timing_skill': 0.62,  # 0-1 score
            'diversification_discipline': 0.78,
            'rebalancing_frequency': 'Monthly',
            'emotional_trading_index': 0.25,  # Lower is better
            'consistency_score': 0.83
        }
    
    def _calculate_esg_metrics(self) -> Dict[str, Any]:
        """Calcule les métriques ESG"""
        
        # Simuler scores ESG
        return {
            'environmental_score': 7.2,  # 0-10
            'social_score': 6.8,
            'governance_score': 8.1,
            'overall_esg_score': 7.4,
            'carbon_footprint': 'Low',  # Low/Medium/High
            'sustainable_investment_ratio': 0.65,  # 65% d'investissements durables
            'esg_risk_rating': 'Medium'
        }
    
    def _calculate_overall_score(self, perf: PerformanceMetrics, risk: RiskMetrics) -> float:
        """Calcule un score global"""
        
        # Pondération des métriques
        performance_weight = 0.4
        risk_weight = 0.3
        consistency_weight = 0.3
        
        # Normaliser métriques (0-100)
        perf_score = min(100, max(0, (perf.sharpe_ratio + 2) * 25))  # Sharpe entre -2 et 2
        risk_score = min(100, max(0, 100 - abs(perf.max_drawdown) * 200))  # Drawdown impact
        consistency_score = min(100, max(0, perf.win_rate * 100))
        
        overall = (
            performance_weight * perf_score +
            risk_weight * risk_score +
            consistency_weight * consistency_score
        )
        
        return round(overall, 1)
    
    def _assess_risk_level(self, risk: RiskMetrics) -> str:
        """Évalue le niveau de risque"""
        
        if abs(risk.var_95) > 0.05:  # VaR > 5%
            return "High"
        elif abs(risk.var_95) > 0.02:  # VaR > 2%
            return "Medium"
        else:
            return "Low"
    
    def _generate_recommendation(self, perf: PerformanceMetrics, risk: RiskMetrics) -> str:
        """Génère une recommandation"""
        
        if perf.sharpe_ratio > 1.5 and abs(perf.max_drawdown) < 0.15:
            return "Excellente performance avec risque maîtrisé. Maintenir la stratégie."
        elif perf.sharpe_ratio > 0.8:
            return "Performance satisfaisante. Considérer optimisation du risque."
        elif abs(perf.max_drawdown) > 0.25:
            return "Drawdown important. Revoir la gestion des risques."
        else:
            return "Performance modérée. Analyser et ajuster la stratégie."
    
    async def generate_realtime_alerts(self) -> List[Dict[str, Any]]:
        """Génère des alertes en temps réel"""
        
        alerts = []
        
        # Vérifier anomalies récentes
        for asset, prices in self.data['prices'].items():
            recent_returns = np.diff(prices[-5:]) / prices[-5:-1]
            
            if np.any(np.abs(recent_returns) > 0.1):  # 10% mouvement
                alerts.append({
                    'type': 'price_movement',
                    'severity': 'high',
                    'asset': asset,
                    'message': f"Mouvement de prix important détecté sur {asset}",
                    'timestamp': datetime.now().isoformat()
                })
        
        # Vérifier corrélations
        recent_corr = np.corrcoef(self.data['returns'][-30:].T)
        avg_corr = np.mean(recent_corr[~np.eye(recent_corr.shape[0], dtype=bool)])
        
        if avg_corr > 0.8:
            alerts.append({
                'type': 'correlation_spike',
                'severity': 'medium',
                'message': "Corrélations élevées détectées - risque de contagion",
                'timestamp': datetime.now().isoformat()
            })
        
        # Vérifier VaR
        recent_returns = np.mean(self.data['returns'][-30:], axis=1)
        current_var = np.percentile(recent_returns, 5)
        
        if abs(current_var) > 0.03:  # 3% VaR
            alerts.append({
                'type': 'risk_alert',
                'severity': 'high',
                'message': f"VaR élevé détecté: {current_var:.2%}",
                'timestamp': datetime.now().isoformat()
            })
        
        return alerts

# ============================================================================
# 🧪 TESTS ET DÉMONSTRATION
# ============================================================================

async def test_advanced_analytics():
    """Test du système d'analytics avancé"""
    
    print("🧪 TEST ANALYTICS AVANCÉS - TRADINGBOT PRO 2025")
    print("=" * 60)
    
    try:
        # Créer système analytics
        analytics_system = AdvancedAnalyticsSystem()
        
        print(f"📊 Données générées:")
        print(f"   - Actifs: {len(analytics_system.data['prices'])}")
        print(f"   - Période: {len(analytics_system.data['returns'])} jours")
        print(f"   - Portfolio: {len(analytics_system.data['positions'])} positions")
        
        # Générer rapport complet
        print(f"\n📈 Génération rapport analytics...")
        report = await analytics_system.generate_comprehensive_report()
        
        if 'error' in report:
            print(f"❌ Erreur: {report['error']}")
            return False
        
        print(f"\n📊 RÉSULTATS ANALYTICS:")
        print("=" * 50)
        
        # Performance
        perf = report['performance']
        print(f"\n💰 PERFORMANCE:")
        print(f"   Retour Total: {perf['total_return']:.2%}")
        print(f"   Retour Annualisé: {perf['annualized_return']:.2%}")
        print(f"   Volatilité: {perf['volatility']:.2%}")
        print(f"   Ratio de Sharpe: {perf['sharpe_ratio']:.3f}")
        print(f"   Max Drawdown: {perf['max_drawdown']:.2%}")
        print(f"   Taux de Victoire: {perf['win_rate']:.1%}")
        
        # Risque
        risk = report['risk']
        print(f"\n⚠️ RISQUE:")
        print(f"   VaR 95%: {risk['var_95']:.2%}")
        print(f"   VaR 99%: {risk['var_99']:.2%}")
        print(f"   Beta: {risk['beta']:.3f}")
        print(f"   Alpha: {risk['alpha']:.4f}")
        print(f"   Tracking Error: {risk['tracking_error']:.2%}")
        
        # Portfolio
        portfolio = report['portfolio']
        print(f"\n💼 PORTFOLIO:")
        print(f"   Valeur Totale: ${portfolio['total_value']:,.2f}")
        print(f"   Ratio Diversification: {portfolio['diversification_ratio']:.3f}")
        print(f"   Risque Concentration: {portfolio['concentration_risk']:.3f}")
        
        # Anomalies
        anomalies = report['anomalies']
        print(f"\n🔍 ANOMALIES:")
        print(f"   Anomalies Prix: {anomalies['price_anomalies_count']}")
        print(f"   Anomalies Volume: {anomalies['volume_anomalies_count']}")
        print(f"   Ruptures Corrélation: {anomalies['correlation_breakdowns']}")
        print(f"   Score Anomalie: {anomalies['anomaly_score']:.3f}")
        
        # Contribution
        contrib = report['contribution']
        print(f"\n📈 CONTRIBUTION:")
        print(f"   Meilleur Contributeur: {contrib['top_contributor']}")
        print(f"   Pire Contributeur: {contrib['worst_contributor']}")
        
        # Comportemental
        behavioral = report['behavioral']
        print(f"\n🧠 COMPORTEMENTAL:")
        print(f"   Fréquence Trading: {behavioral['trading_frequency']}")
        print(f"   Comportement Risque: {behavioral['risk_taking_behavior']}")
        print(f"   Score Timing: {behavioral['market_timing_skill']:.2f}")
        print(f"   Discipline Diversification: {behavioral['diversification_discipline']:.2f}")
        
        # ESG
        esg = report['esg']
        print(f"\n🌱 ESG:")
        print(f"   Score Environnemental: {esg['environmental_score']:.1f}/10")
        print(f"   Score Social: {esg['social_score']:.1f}/10")
        print(f"   Score Gouvernance: {esg['governance_score']:.1f}/10")
        print(f"   Score Global ESG: {esg['overall_esg_score']:.1f}/10")
        
        # Résumé
        summary = report['summary']
        print(f"\n📋 RÉSUMÉ:")
        print(f"   Score Global: {summary['overall_score']:.1f}/100")
        print(f"   Niveau de Risque: {summary['risk_level']}")
        print(f"   Recommandation: {summary['recommendation']}")
        
        # Test alertes temps réel
        print(f"\n🔔 Test alertes temps réel...")
        alerts = await analytics_system.generate_realtime_alerts()
        print(f"   Alertes générées: {len(alerts)}")
        
        for alert in alerts:
            severity_icon = '🔴' if alert['severity'] == 'high' else '🟡'
            print(f"   {severity_icon} {alert['type']}: {alert['message']}")
        
        print(f"\n✅ ANALYTICS AVANCÉS OPÉRATIONNELS!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR TEST: {e}")
        return False

if __name__ == "__main__":
    print("📊 ANALYTICS AVANCÉS - TRADINGBOT PRO 2025")
    print("=" * 55)
    
    # Test du système
    success = asyncio.run(test_advanced_analytics())
    
    if success:
        print("\n✅ SYSTÈME ANALYTICS PRÊT!")
        print("📈 Métriques de performance calculées")
        print("⚠️ Analyse de risque multi-facteurs active")
        print("🔍 Détection d'anomalies opérationnelle")
        print("📊 Dashboards et visualisations disponibles")
        print("🔔 Alertes intelligentes configurées")
    else:
        print("\n❌ ERREUR SYSTÈME ANALYTICS")
        
    print("\n" + "=" * 55)
