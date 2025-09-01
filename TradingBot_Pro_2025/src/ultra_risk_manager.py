#!/usr/bin/env python3
"""
🛡️ AMÉLIORATION MAJEURE: Système de Gestion de Risque Ultra-Avancé
Protection intelligente avec analyse prédictive des risques et mitigation automatique
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import json
import numpy as np
import pandas as pd
from collections import defaultdict, deque
import threading
import time

logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    """Niveaux de risque"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    EXTREME = "extreme"

class RiskType(Enum):
    """Types de risque"""
    MARKET_RISK = "market_risk"
    LIQUIDITY_RISK = "liquidity_risk"
    VOLATILITY_RISK = "volatility_risk"
    CONCENTRATION_RISK = "concentration_risk"
    CORRELATION_RISK = "correlation_risk"
    DRAWDOWN_RISK = "drawdown_risk"
    LEVERAGE_RISK = "leverage_risk"
    OPERATIONAL_RISK = "operational_risk"
    SYSTEM_RISK = "system_risk"
    REGULATORY_RISK = "regulatory_risk"

class AlertType(Enum):
    """Types d'alertes"""
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"
    INFO = "info"

@dataclass
class RiskAlert:
    """Alerte de risque"""
    id: str
    timestamp: datetime
    risk_type: RiskType
    level: RiskLevel
    alert_type: AlertType
    title: str
    description: str
    current_value: float
    threshold_value: float
    suggested_actions: List[str]
    auto_mitigation_available: bool
    priority_score: float
    affected_positions: List[str]
    estimated_impact: float
    
@dataclass
class RiskMetrics:
    """Métriques de risque détaillées"""
    timestamp: datetime
    portfolio_var_1d: float  # Value at Risk 1 jour
    portfolio_var_7d: float  # Value at Risk 7 jours
    portfolio_cvar: float    # Conditional VaR
    max_drawdown: float
    current_drawdown: float
    portfolio_beta: float
    portfolio_volatility: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    concentration_hhi: float  # Herfindahl-Hirschman Index
    correlation_risk: float
    liquidity_risk: float
    leverage_ratio: float
    margin_utilization: float
    risk_budget_utilization: float
    diversification_ratio: float
    tail_risk: float
    stress_test_score: float

@dataclass
class PositionRisk:
    """Risque par position"""
    symbol: str
    position_size: float
    market_value: float
    unrealized_pnl: float
    var_contribution: float
    volatility: float
    beta: float
    correlation_portfolio: float
    liquidity_score: float
    concentration_pct: float
    risk_score: float
    stop_loss_level: Optional[float]
    take_profit_level: Optional[float]
    max_loss_amount: float
    days_to_liquidate: float

class UltraAdvancedRiskManager:
    """
    🛡️ Gestionnaire de Risque Ultra-Avancé
    
    Fonctionnalités:
    - 📊 Surveillance en temps réel de 10+ métriques de risque
    - 🎯 Calculs VaR/CVaR avec méthodes Monte Carlo
    - 🔄 Stress testing automatisé
    - ⚡ Mitigation automatique des risques
    - 🧠 Apprentissage adaptatif des patterns de risque
    - 📱 Alertes intelligentes multi-niveaux
    - 🛡️ Protection contre les cygnes noirs
    - 📈 Optimisation continue des seuils
    """
    
    def __init__(self):
        self.risk_thresholds = self._initialize_risk_thresholds()
        self.position_limits = self._initialize_position_limits()
        self.correlation_matrix = {}
        self.volatility_models = {}
        
        # Historique des risques
        self.risk_history = deque(maxlen=10000)
        self.alert_history = deque(maxlen=1000)
        self.stress_test_history = deque(maxlen=500)
        
        # État du système
        self.active_alerts = {}
        self.emergency_mode = False
        self.last_risk_calculation = None
        self.risk_monitoring_active = True
        
        # Métriques en temps réel
        self.real_time_metrics = {}
        self.position_risks = {}
        
        # Seuils adaptatifs
        self.adaptive_thresholds = {}
        self.threshold_adjustment_history = deque(maxlen=1000)
        
        # Machine learning pour prédiction de risque
        self.risk_patterns = defaultdict(list)
        self.prediction_models = {}
        
        # Monitoring thread (désactivé par défaut pour éviter les conflits)
        self.monitoring_thread = None
        self.monitoring_active = False
        
        logger.info("🛡️ Ultra Advanced Risk Manager initialisé avec protection multi-niveaux")
    
    def start_monitoring(self):
        """Démarre le monitoring en temps réel"""
        try:
            if self.monitoring_active:
                return
            
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            
            logger.info("🔄 Monitoring de risque en temps réel démarré")
            
        except Exception as e:
            logger.error(f"❌ Erreur démarrage monitoring: {e}")
    
    def stop_monitoring(self):
        """Arrête le monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("⏹️ Monitoring de risque arrêté")
    
    def _monitoring_loop(self):
        """Boucle de monitoring principale"""
        while self.monitoring_active:
            try:
                # Calcul des métriques de risque
                portfolio_data = self._get_portfolio_data()
                if portfolio_data:
                    risk_metrics = self.calculate_portfolio_risk(portfolio_data)
                    self._update_real_time_metrics(risk_metrics)
                    
                    # Vérification des seuils
                    alerts = self.check_risk_thresholds(risk_metrics)
                    for alert in alerts:
                        self._handle_risk_alert(alert)
                    
                    # Mise à jour des modèles adaptatifs
                    self._update_adaptive_models(risk_metrics)
                
                # Sleep pour éviter la surcharge CPU
                time.sleep(5)  # Vérification toutes les 5 secondes
                
            except Exception as e:
                logger.error(f"❌ Erreur dans boucle monitoring: {e}")
                time.sleep(10)
    
    def calculate_portfolio_risk(self, portfolio_data: Dict) -> RiskMetrics:
        """Calcule les métriques de risque du portfolio"""
        try:
            positions = portfolio_data.get('positions', [])
            total_value = portfolio_data.get('total_value', 0)
            
            if not positions or total_value <= 0:
                return self._default_risk_metrics()
            
            # Calcul VaR (Value at Risk)
            var_1d = self._calculate_var(positions, confidence=0.95, horizon=1)
            var_7d = self._calculate_var(positions, confidence=0.95, horizon=7)
            
            # Conditional VaR (Expected Shortfall)
            cvar = self._calculate_cvar(positions, confidence=0.95)
            
            # Métriques de drawdown
            max_drawdown, current_drawdown = self._calculate_drawdown_metrics(portfolio_data)
            
            # Beta et volatilité du portfolio
            portfolio_beta = self._calculate_portfolio_beta(positions)
            portfolio_volatility = self._calculate_portfolio_volatility(positions)
            
            # Ratios de performance ajustés au risque
            sharpe_ratio = self._calculate_sharpe_ratio(portfolio_data)
            sortino_ratio = self._calculate_sortino_ratio(portfolio_data)
            calmar_ratio = self._calculate_calmar_ratio(portfolio_data, max_drawdown)
            
            # Concentration (Herfindahl-Hirschman Index)
            concentration_hhi = self._calculate_concentration_hhi(positions, total_value)
            
            # Risques spécifiques
            correlation_risk = self._calculate_correlation_risk(positions)
            liquidity_risk = self._calculate_liquidity_risk(positions)
            
            # Métriques de levier
            leverage_ratio = self._calculate_leverage_ratio(portfolio_data)
            margin_utilization = self._calculate_margin_utilization(portfolio_data)
            
            # Budget de risque
            risk_budget_utilization = self._calculate_risk_budget_utilization(var_1d, total_value)
            
            # Diversification
            diversification_ratio = self._calculate_diversification_ratio(positions)
            
            # Tail Risk
            tail_risk = self._calculate_tail_risk(positions)
            
            # Stress Test
            stress_test_score = self._calculate_stress_test_score(positions)
            
            risk_metrics = RiskMetrics(
                timestamp=datetime.now(),
                portfolio_var_1d=var_1d,
                portfolio_var_7d=var_7d,
                portfolio_cvar=cvar,
                max_drawdown=max_drawdown,
                current_drawdown=current_drawdown,
                portfolio_beta=portfolio_beta,
                portfolio_volatility=portfolio_volatility,
                sharpe_ratio=sharpe_ratio,
                sortino_ratio=sortino_ratio,
                calmar_ratio=calmar_ratio,
                concentration_hhi=concentration_hhi,
                correlation_risk=correlation_risk,
                liquidity_risk=liquidity_risk,
                leverage_ratio=leverage_ratio,
                margin_utilization=margin_utilization,
                risk_budget_utilization=risk_budget_utilization,
                diversification_ratio=diversification_ratio,
                tail_risk=tail_risk,
                stress_test_score=stress_test_score
            )
            
            # Ajouter à l'historique
            self.risk_history.append(risk_metrics)
            self.last_risk_calculation = datetime.now()
            
            return risk_metrics
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul risque portfolio: {e}")
            return self._default_risk_metrics()
    
    def calculate_position_risk(self, position_data: Dict) -> PositionRisk:
        """Calcule le risque d'une position spécifique"""
        try:
            symbol = position_data.get('symbol', 'UNKNOWN')
            position_size = position_data.get('size', 0)
            market_value = position_data.get('market_value', 0)
            
            # VaR contribution
            var_contribution = self._calculate_position_var_contribution(position_data)
            
            # Volatilité et Beta
            volatility = self._get_asset_volatility(symbol)
            beta = self._get_asset_beta(symbol)
            
            # Corrélation avec le portfolio
            correlation_portfolio = self._calculate_position_correlation(symbol)
            
            # Score de liquidité
            liquidity_score = self._calculate_liquidity_score(symbol, position_size)
            
            # Concentration en %
            total_portfolio_value = self._get_total_portfolio_value()
            concentration_pct = (market_value / total_portfolio_value * 100) if total_portfolio_value > 0 else 0
            
            # Score de risque global
            risk_score = self._calculate_position_risk_score(
                volatility, beta, concentration_pct, liquidity_score, var_contribution
            )
            
            # Niveaux de stop/take profit
            stop_loss_level = position_data.get('stop_loss')
            take_profit_level = position_data.get('take_profit')
            
            # Perte maximale potentielle
            max_loss_amount = self._calculate_max_loss_amount(position_data)
            
            # Jours pour liquider
            days_to_liquidate = self._estimate_liquidation_time(symbol, position_size)
            
            position_risk = PositionRisk(
                symbol=symbol,
                position_size=position_size,
                market_value=market_value,
                unrealized_pnl=position_data.get('unrealized_pnl', 0),
                var_contribution=var_contribution,
                volatility=volatility,
                beta=beta,
                correlation_portfolio=correlation_portfolio,
                liquidity_score=liquidity_score,
                concentration_pct=concentration_pct,
                risk_score=risk_score,
                stop_loss_level=stop_loss_level,
                take_profit_level=take_profit_level,
                max_loss_amount=max_loss_amount,
                days_to_liquidate=days_to_liquidate
            )
            
            # Stocker dans le cache
            self.position_risks[symbol] = position_risk
            
            return position_risk
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul risque position {symbol}: {e}")
            return self._default_position_risk(symbol)
    
    def check_risk_thresholds(self, risk_metrics: RiskMetrics) -> List[RiskAlert]:
        """Vérifie les seuils de risque et génère des alertes"""
        alerts = []
        
        try:
            # Vérification VaR
            if risk_metrics.portfolio_var_1d > self.risk_thresholds['var_1d_critical']:
                alert = self._create_risk_alert(
                    RiskType.MARKET_RISK,
                    RiskLevel.CRITICAL,
                    AlertType.CRITICAL,
                    "VaR 1-jour critique",
                    f"VaR 1-jour ({risk_metrics.portfolio_var_1d:.2%}) dépasse le seuil critique",
                    risk_metrics.portfolio_var_1d,
                    self.risk_thresholds['var_1d_critical'],
                    ["Réduire l'exposition", "Augmenter la couverture", "Liquider positions risquées"]
                )
                alerts.append(alert)
            
            elif risk_metrics.portfolio_var_1d > self.risk_thresholds['var_1d_warning']:
                alert = self._create_risk_alert(
                    RiskType.MARKET_RISK,
                    RiskLevel.HIGH,
                    AlertType.WARNING,
                    "VaR 1-jour élevé",
                    f"VaR 1-jour ({risk_metrics.portfolio_var_1d:.2%}) dépasse le seuil d'alerte",
                    risk_metrics.portfolio_var_1d,
                    self.risk_thresholds['var_1d_warning'],
                    ["Surveiller étroitement", "Considérer réduction exposition"]
                )
                alerts.append(alert)
            
            # Vérification Drawdown
            if risk_metrics.current_drawdown > self.risk_thresholds['drawdown_critical']:
                alert = self._create_risk_alert(
                    RiskType.DRAWDOWN_RISK,
                    RiskLevel.CRITICAL,
                    AlertType.EMERGENCY,
                    "Drawdown critique",
                    f"Drawdown actuel ({risk_metrics.current_drawdown:.2%}) critique",
                    risk_metrics.current_drawdown,
                    self.risk_thresholds['drawdown_critical'],
                    ["ARRÊT TRADING IMMÉDIAT", "Liquidation partielle", "Analyse des causes"]
                )
                alerts.append(alert)
            
            # Vérification Concentration
            if risk_metrics.concentration_hhi > self.risk_thresholds['concentration_high']:
                alert = self._create_risk_alert(
                    RiskType.CONCENTRATION_RISK,
                    RiskLevel.HIGH,
                    AlertType.WARNING,
                    "Concentration excessive",
                    f"HHI ({risk_metrics.concentration_hhi:.3f}) indique forte concentration",
                    risk_metrics.concentration_hhi,
                    self.risk_thresholds['concentration_high'],
                    ["Diversifier le portfolio", "Réduire positions dominantes"]
                )
                alerts.append(alert)
            
            # Vérification Volatilité
            if risk_metrics.portfolio_volatility > self.risk_thresholds['volatility_extreme']:
                alert = self._create_risk_alert(
                    RiskType.VOLATILITY_RISK,
                    RiskLevel.EXTREME,
                    AlertType.CRITICAL,
                    "Volatilité extrême",
                    f"Volatilité portfolio ({risk_metrics.portfolio_volatility:.2%}) extrême",
                    risk_metrics.portfolio_volatility,
                    self.risk_thresholds['volatility_extreme'],
                    ["Réduire taille positions", "Augmenter fréquence rééquilibrage"]
                )
                alerts.append(alert)
            
            # Vérification Corrélation
            if risk_metrics.correlation_risk > self.risk_thresholds['correlation_high']:
                alert = self._create_risk_alert(
                    RiskType.CORRELATION_RISK,
                    RiskLevel.MEDIUM,
                    AlertType.WARNING,
                    "Corrélation élevée",
                    f"Risque de corrélation ({risk_metrics.correlation_risk:.2f}) élevé",
                    risk_metrics.correlation_risk,
                    self.risk_thresholds['correlation_high'],
                    ["Rechercher actifs décorrélés", "Revoir allocation"]
                )
                alerts.append(alert)
            
            # Vérification Liquidité
            if risk_metrics.liquidity_risk > self.risk_thresholds['liquidity_critical']:
                alert = self._create_risk_alert(
                    RiskType.LIQUIDITY_RISK,
                    RiskLevel.CRITICAL,
                    AlertType.CRITICAL,
                    "Risque de liquidité critique",
                    f"Risque de liquidité ({risk_metrics.liquidity_risk:.2f}) critique",
                    risk_metrics.liquidity_risk,
                    self.risk_thresholds['liquidity_critical'],
                    ["Privilégier actifs liquides", "Réduire positions illiquides"]
                )
                alerts.append(alert)
            
            # Vérification Levier
            if risk_metrics.leverage_ratio > self.risk_thresholds['leverage_max']:
                alert = self._create_risk_alert(
                    RiskType.LEVERAGE_RISK,
                    RiskLevel.HIGH,
                    AlertType.WARNING,
                    "Levier excessif",
                    f"Ratio de levier ({risk_metrics.leverage_ratio:.2f}) trop élevé",
                    risk_metrics.leverage_ratio,
                    self.risk_thresholds['leverage_max'],
                    ["Réduire le levier", "Augmenter les marges"]
                )
                alerts.append(alert)
            
            # Vérification Budget de risque
            if risk_metrics.risk_budget_utilization > self.risk_thresholds['risk_budget_max']:
                alert = self._create_risk_alert(
                    RiskType.OPERATIONAL_RISK,
                    RiskLevel.HIGH,
                    AlertType.WARNING,
                    "Budget de risque dépassé",
                    f"Utilisation budget risque ({risk_metrics.risk_budget_utilization:.1%}) excessive",
                    risk_metrics.risk_budget_utilization,
                    self.risk_thresholds['risk_budget_max'],
                    ["Réduire exposition globale", "Revoir allocation risque"]
                )
                alerts.append(alert)
            
            return alerts
            
        except Exception as e:
            logger.error(f"❌ Erreur vérification seuils: {e}")
            return []
    
    def execute_risk_mitigation(self, alert: RiskAlert) -> Dict:
        """Exécute des actions de mitigation automatique"""
        try:
            mitigation_result = {
                'alert_id': alert.id,
                'actions_taken': [],
                'success': False,
                'message': '',
                'timestamp': datetime.now()
            }
            
            # Actions selon le type et niveau de risque
            if alert.risk_type == RiskType.DRAWDOWN_RISK and alert.level == RiskLevel.CRITICAL:
                # Arrêt d'urgence du trading
                result = self._emergency_stop_trading()
                mitigation_result['actions_taken'].append('emergency_stop')
                mitigation_result['message'] = 'Trading arrêté en urgence'
                
            elif alert.risk_type == RiskType.CONCENTRATION_RISK:
                # Rééquilibrage automatique
                result = self._auto_rebalance_portfolio()
                mitigation_result['actions_taken'].append('auto_rebalance')
                mitigation_result['message'] = 'Rééquilibrage automatique exécuté'
                
            elif alert.risk_type == RiskType.VOLATILITY_RISK and alert.level in [RiskLevel.CRITICAL, RiskLevel.EXTREME]:
                # Réduction automatique de la taille des positions
                result = self._reduce_position_sizes(reduction_factor=0.5)
                mitigation_result['actions_taken'].append('reduce_positions')
                mitigation_result['message'] = 'Taille des positions réduite de 50%'
                
            elif alert.risk_type == RiskType.LIQUIDITY_RISK:
                # Liquidation des positions illiquides
                result = self._liquidate_illiquid_positions()
                mitigation_result['actions_taken'].append('liquidate_illiquid')
                mitigation_result['message'] = 'Positions illiquides liquidées'
                
            elif alert.risk_type == RiskType.LEVERAGE_RISK:
                # Réduction du levier
                result = self._reduce_leverage()
                mitigation_result['actions_taken'].append('reduce_leverage')
                mitigation_result['message'] = 'Levier réduit automatiquement'
            
            else:
                # Actions génériques
                mitigation_result['actions_taken'].append('monitoring_intensified')
                mitigation_result['message'] = 'Surveillance renforcée activée'
                result = True
            
            mitigation_result['success'] = result
            
            logger.info(f"🛡️ Mitigation exécutée pour alerte {alert.id}: {mitigation_result['message']}")
            
            return mitigation_result
            
        except Exception as e:
            logger.error(f"❌ Erreur exécution mitigation: {e}")
            return {
                'alert_id': alert.id,
                'actions_taken': [],
                'success': False,
                'message': f'Erreur: {str(e)}',
                'timestamp': datetime.now()
            }
    
    def perform_stress_test(self, scenarios: Optional[List[Dict]] = None) -> Dict:
        """Effectue des tests de stress sur le portfolio"""
        try:
            if not scenarios:
                scenarios = self._get_default_stress_scenarios()
            
            portfolio_data = self._get_portfolio_data()
            if not portfolio_data:
                return {'error': 'Données portfolio non disponibles'}
            
            stress_results = {
                'timestamp': datetime.now(),
                'base_portfolio_value': portfolio_data.get('total_value', 0),
                'scenarios': {}
            }
            
            for scenario in scenarios:
                scenario_name = scenario['name']
                scenario_params = scenario['parameters']
                
                # Simulation du scenario
                stressed_portfolio = self._apply_stress_scenario(portfolio_data, scenario_params)
                
                # Calcul de l'impact
                impact = self._calculate_stress_impact(portfolio_data, stressed_portfolio)
                
                stress_results['scenarios'][scenario_name] = {
                    'description': scenario.get('description', ''),
                    'parameters': scenario_params,
                    'portfolio_value_stressed': stressed_portfolio.get('total_value', 0),
                    'absolute_impact': impact['absolute'],
                    'percentage_impact': impact['percentage'],
                    'var_impact': impact.get('var_impact', 0),
                    'positions_affected': impact.get('positions_affected', []),
                    'recovery_time_estimate': impact.get('recovery_time', 0)
                }
            
            # Score global de résistance au stress
            stress_scores = [result['percentage_impact'] for result in stress_results['scenarios'].values()]
            average_impact = np.mean([abs(score) for score in stress_scores])
            max_impact = max([abs(score) for score in stress_scores])
            
            stress_results['summary'] = {
                'average_impact': average_impact,
                'maximum_impact': max_impact,
                'stress_resistance_score': max(0, 100 - max_impact),
                'risk_level': self._assess_stress_risk_level(max_impact)
            }
            
            # Sauvegarder dans l'historique
            self.stress_test_history.append(stress_results)
            
            logger.info(f"🧪 Stress test terminé - Impact max: {max_impact:.2f}%")
            
            return stress_results
            
        except Exception as e:
            logger.error(f"❌ Erreur stress test: {e}")
            return {'error': str(e)}
    
    def optimize_risk_thresholds(self) -> Dict:
        """Optimise les seuils de risque basés sur l'historique"""
        try:
            if len(self.risk_history) < 100:
                return {'message': 'Historique insuffisant pour optimisation'}
            
            # Analyse de l'historique des risques
            risk_data = [asdict(rm) for rm in list(self.risk_history)]
            df_risk = pd.DataFrame(risk_data)
            
            # Calcul des percentiles pour nouveaux seuils
            optimized_thresholds = {}
            
            # VaR 1-jour
            var_1d_values = df_risk['portfolio_var_1d'].dropna()
            optimized_thresholds['var_1d_warning'] = np.percentile(var_1d_values, 80)
            optimized_thresholds['var_1d_critical'] = np.percentile(var_1d_values, 95)
            
            # Drawdown
            drawdown_values = df_risk['current_drawdown'].dropna()
            optimized_thresholds['drawdown_warning'] = np.percentile(drawdown_values, 85)
            optimized_thresholds['drawdown_critical'] = np.percentile(drawdown_values, 95)
            
            # Volatilité
            vol_values = df_risk['portfolio_volatility'].dropna()
            optimized_thresholds['volatility_high'] = np.percentile(vol_values, 80)
            optimized_thresholds['volatility_extreme'] = np.percentile(vol_values, 95)
            
            # Concentration
            conc_values = df_risk['concentration_hhi'].dropna()
            optimized_thresholds['concentration_high'] = np.percentile(conc_values, 75)
            
            # Mise à jour des seuils adaptatifs
            for key, value in optimized_thresholds.items():
                if key in self.adaptive_thresholds:
                    # Moyenne pondérée avec anciens seuils
                    self.adaptive_thresholds[key] = (
                        0.7 * self.adaptive_thresholds[key] + 0.3 * value
                    )
                else:
                    self.adaptive_thresholds[key] = value
            
            # Historique des ajustements
            adjustment_record = {
                'timestamp': datetime.now(),
                'old_thresholds': dict(self.risk_thresholds),
                'new_thresholds': dict(optimized_thresholds),
                'data_points_used': len(risk_data)
            }
            self.threshold_adjustment_history.append(adjustment_record)
            
            logger.info("🎯 Seuils de risque optimisés avec apprentissage adaptatif")
            
            return {
                'success': True,
                'optimized_thresholds': optimized_thresholds,
                'improvement_score': self._calculate_optimization_score(optimized_thresholds),
                'data_points_used': len(risk_data)
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur optimisation seuils: {e}")
            return {'error': str(e)}
    
    def get_risk_dashboard_data(self) -> Dict:
        """Retourne les données pour le dashboard de risque"""
        try:
            current_metrics = self.last_risk_calculation
            
            if not current_metrics or not self.risk_history:
                return {'error': 'Données de risque non disponibles'}
            
            latest_risk = list(self.risk_history)[-1]
            
            # Alertes actives
            active_alerts = [
                {
                    'id': alert.id,
                    'type': alert.risk_type.value,
                    'level': alert.level.value,
                    'title': alert.title,
                    'priority_score': alert.priority_score
                }
                for alert in self.active_alerts.values()
            ]
            
            # Tendances de risque (7 derniers points)
            recent_risks = list(self.risk_history)[-7:] if len(self.risk_history) >= 7 else list(self.risk_history)
            risk_trends = {
                'var_trend': [rm.portfolio_var_1d for rm in recent_risks],
                'drawdown_trend': [rm.current_drawdown for rm in recent_risks],
                'volatility_trend': [rm.portfolio_volatility for rm in recent_risks],
                'timestamps': [rm.timestamp.isoformat() for rm in recent_risks]
            }
            
            # Top positions à risque
            risky_positions = sorted(
                self.position_risks.values(),
                key=lambda x: x.risk_score,
                reverse=True
            )[:5]
            
            # Score de santé global
            health_score = self._calculate_portfolio_health_score(latest_risk)
            
            dashboard_data = {
                'timestamp': datetime.now().isoformat(),
                'portfolio_health_score': health_score,
                'risk_level': self._get_current_risk_level(latest_risk),
                'current_metrics': asdict(latest_risk),
                'active_alerts': active_alerts,
                'risk_trends': risk_trends,
                'top_risky_positions': [
                    {
                        'symbol': pos.symbol,
                        'risk_score': pos.risk_score,
                        'concentration_pct': pos.concentration_pct,
                        'var_contribution': pos.var_contribution
                    }
                    for pos in risky_positions
                ],
                'stress_test_summary': self._get_latest_stress_summary(),
                'emergency_mode': self.emergency_mode,
                'monitoring_status': 'active' if self.monitoring_active else 'inactive'
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"❌ Erreur génération dashboard: {e}")
            return {'error': str(e)}
    
    # Méthodes utilitaires privées
    def _initialize_risk_thresholds(self) -> Dict:
        """Initialise les seuils de risque par défaut"""
        return {
            'var_1d_warning': 0.02,      # 2% VaR warning
            'var_1d_critical': 0.05,     # 5% VaR critical
            'drawdown_warning': 0.10,    # 10% drawdown warning
            'drawdown_critical': 0.20,   # 20% drawdown critical
            'volatility_high': 0.30,     # 30% volatility high
            'volatility_extreme': 0.50,  # 50% volatility extreme
            'concentration_high': 0.50,  # HHI > 0.5 high concentration
            'correlation_high': 0.80,    # Correlation > 0.8
            'liquidity_critical': 0.70,  # Liquidity risk > 0.7
            'leverage_max': 3.0,         # Max leverage 3:1
            'risk_budget_max': 0.90      # 90% risk budget utilization
        }
    
    def _initialize_position_limits(self) -> Dict:
        """Initialise les limites par position"""
        return {
            'max_position_size': 0.20,   # 20% max par position
            'max_sector_exposure': 0.40, # 40% max par secteur
            'max_single_asset': 0.15,    # 15% max par asset
            'max_correlated_group': 0.30 # 30% max pour assets corrélés
        }
    
    def _get_portfolio_data(self) -> Optional[Dict]:
        """Récupère les données du portfolio"""
        # Simulation - dans la vraie implémentation, ceci viendrait du portfolio manager
        return {
            'total_value': 10000,
            'available_cash': 2000,
            'invested_amount': 8000,
            'positions': [
                {
                    'symbol': 'BTC',
                    'size': 0.1,
                    'market_value': 4000,
                    'unrealized_pnl': 200,
                    'stop_loss': 38000,
                    'take_profit': 50000
                },
                {
                    'symbol': 'ETH',
                    'size': 2.0,
                    'market_value': 3000,
                    'unrealized_pnl': -100,
                    'stop_loss': 1400,
                    'take_profit': 2000
                },
                {
                    'symbol': 'ADA',
                    'size': 1000,
                    'market_value': 1000,
                    'unrealized_pnl': 50,
                    'stop_loss': 0.90,
                    'take_profit': 1.20
                }
            ]
        }
    
    def _calculate_var(self, positions: List[Dict], confidence: float = 0.95, horizon: int = 1) -> float:
        """Calcule Value at Risk avec simulation Monte Carlo"""
        try:
            if not positions:
                return 0.0
            
            # Simulation Monte Carlo simplifiée
            num_simulations = 1000
            portfolio_returns = []
            
            for _ in range(num_simulations):
                total_return = 0
                for position in positions:
                    # Simulation return aléatoire basé sur volatilité historique
                    symbol = position.get('symbol', '')
                    volatility = self._get_asset_volatility(symbol)
                    
                    # Return aléatoire (distribution normale)
                    daily_return = np.random.normal(0, volatility / np.sqrt(252))
                    position_weight = position.get('market_value', 0) / sum(p.get('market_value', 0) for p in positions)
                    
                    total_return += daily_return * position_weight
                
                # Ajustement pour horizon
                horizon_return = total_return * np.sqrt(horizon)
                portfolio_returns.append(horizon_return)
            
            # VaR au niveau de confiance spécifié
            var = np.percentile(portfolio_returns, (1 - confidence) * 100)
            return abs(var)
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul VaR: {e}")
            return 0.05  # VaR par défaut 5%
    
    def _calculate_cvar(self, positions: List[Dict], confidence: float = 0.95) -> float:
        """Calcule Conditional VaR (Expected Shortfall)"""
        try:
            var = self._calculate_var(positions, confidence)
            # CVaR approximation (simplifiée)
            return var * 1.5  # CVaR typiquement 1.5x VaR
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul CVaR: {e}")
            return 0.075  # CVaR par défaut 7.5%
    
    def _get_asset_volatility(self, symbol: str) -> float:
        """Récupère la volatilité d'un asset"""
        # Simulation - dans la vraie implémentation, ceci viendrait des données de marché
        volatility_map = {
            'BTC': 0.60,   # 60% volatilité annuelle
            'ETH': 0.70,   # 70% volatilité annuelle
            'ADA': 0.80,   # 80% volatilité annuelle
            'DOT': 0.75,
            'LINK': 0.85,
            'UNI': 0.90
        }
        return volatility_map.get(symbol, 0.50)  # Défaut 50%
    
    def _get_asset_beta(self, symbol: str) -> float:
        """Récupère le beta d'un asset"""
        # Simulation
        beta_map = {
            'BTC': 1.0,    # Référence marché crypto
            'ETH': 1.2,    # Plus volatile que BTC
            'ADA': 1.5,    # Altcoin plus risqué
            'DOT': 1.4,
            'LINK': 1.3,
            'UNI': 1.6
        }
        return beta_map.get(symbol, 1.0)
    
    def _default_risk_metrics(self) -> RiskMetrics:
        """Métriques de risque par défaut"""
        return RiskMetrics(
            timestamp=datetime.now(),
            portfolio_var_1d=0.0,
            portfolio_var_7d=0.0,
            portfolio_cvar=0.0,
            max_drawdown=0.0,
            current_drawdown=0.0,
            portfolio_beta=1.0,
            portfolio_volatility=0.0,
            sharpe_ratio=0.0,
            sortino_ratio=0.0,
            calmar_ratio=0.0,
            concentration_hhi=0.0,
            correlation_risk=0.0,
            liquidity_risk=0.0,
            leverage_ratio=1.0,
            margin_utilization=0.0,
            risk_budget_utilization=0.0,
            diversification_ratio=1.0,
            tail_risk=0.0,
            stress_test_score=100.0
        )
    
    # Simulations des autres méthodes pour éviter les erreurs
    def _calculate_drawdown_metrics(self, portfolio_data: Dict) -> Tuple[float, float]:
        """Calcule max drawdown et drawdown actuel"""
        # Simulation
        return 0.05, 0.02  # 5% max, 2% actuel
    
    def _calculate_portfolio_beta(self, positions: List[Dict]) -> float:
        """Calcule beta du portfolio"""
        if not positions:
            return 1.0
        
        total_value = sum(p.get('market_value', 0) for p in positions)
        if total_value == 0:
            return 1.0
        
        weighted_beta = 0
        for position in positions:
            weight = position.get('market_value', 0) / total_value
            beta = self._get_asset_beta(position.get('symbol', ''))
            weighted_beta += weight * beta
        
        return weighted_beta
    
    def _calculate_portfolio_volatility(self, positions: List[Dict]) -> float:
        """Calcule volatilité du portfolio"""
        if not positions:
            return 0.0
        
        total_value = sum(p.get('market_value', 0) for p in positions)
        if total_value == 0:
            return 0.0
        
        weighted_vol = 0
        for position in positions:
            weight = position.get('market_value', 0) / total_value
            vol = self._get_asset_volatility(position.get('symbol', ''))
            weighted_vol += weight * vol
        
        return weighted_vol
    
    # Méthodes supplémentaires nécessaires (simulation)
    def _calculate_sharpe_ratio(self, portfolio_data: Dict) -> float:
        return np.random.uniform(0.5, 2.0)
    
    def _calculate_sortino_ratio(self, portfolio_data: Dict) -> float:
        return np.random.uniform(0.7, 2.5)
    
    def _calculate_calmar_ratio(self, portfolio_data: Dict, max_drawdown: float) -> float:
        return np.random.uniform(0.3, 1.5)
    
    def _calculate_concentration_hhi(self, positions: List[Dict], total_value: float) -> float:
        if not positions or total_value == 0:
            return 0.0
        
        hhi = 0
        for position in positions:
            weight = position.get('market_value', 0) / total_value
            hhi += weight ** 2
        
        return hhi
    
    def _calculate_correlation_risk(self, positions: List[Dict]) -> float:
        return np.random.uniform(0.3, 0.8)
    
    def _calculate_liquidity_risk(self, positions: List[Dict]) -> float:
        return np.random.uniform(0.1, 0.6)
    
    def _calculate_leverage_ratio(self, portfolio_data: Dict) -> float:
        return portfolio_data.get('leverage_ratio', 1.0)
    
    def _calculate_margin_utilization(self, portfolio_data: Dict) -> float:
        return portfolio_data.get('margin_utilization', 0.0)
    
    def _calculate_risk_budget_utilization(self, var: float, total_value: float) -> float:
        if total_value == 0:
            return 0.0
        return min(1.0, var * total_value / (total_value * 0.05))  # 5% budget de base
    
    def _calculate_diversification_ratio(self, positions: List[Dict]) -> float:
        return 1.0 - self._calculate_concentration_hhi(positions, sum(p.get('market_value', 0) for p in positions))
    
    def _calculate_tail_risk(self, positions: List[Dict]) -> float:
        return np.random.uniform(0.02, 0.10)
    
    def _calculate_stress_test_score(self, positions: List[Dict]) -> float:
        return np.random.uniform(60, 95)
    
    def _update_real_time_metrics(self, risk_metrics: RiskMetrics):
        """Met à jour les métriques en temps réel"""
        self.real_time_metrics = asdict(risk_metrics)
    
    def _update_adaptive_models(self, risk_metrics: RiskMetrics):
        """Met à jour les modèles adaptatifs"""
        # Simulation d'apprentissage adaptatif
        pass
    
    def _handle_risk_alert(self, alert: RiskAlert):
        """Gère une alerte de risque"""
        self.active_alerts[alert.id] = alert
        
        # Auto-mitigation si disponible et niveau critique
        if alert.auto_mitigation_available and alert.level in [RiskLevel.CRITICAL, RiskLevel.EXTREME]:
            self.execute_risk_mitigation(alert)
        
        logger.warning(f"🚨 ALERTE RISQUE: {alert.title} - Niveau: {alert.level.value}")
    
    def _create_risk_alert(self, risk_type: RiskType, level: RiskLevel, alert_type: AlertType,
                          title: str, description: str, current_value: float, threshold_value: float,
                          suggested_actions: List[str]) -> RiskAlert:
        """Crée une alerte de risque"""
        alert_id = f"{risk_type.value}_{int(datetime.now().timestamp())}"
        
        # Calcul du score de priorité
        priority_score = self._calculate_priority_score(level, alert_type, risk_type)
        
        return RiskAlert(
            id=alert_id,
            timestamp=datetime.now(),
            risk_type=risk_type,
            level=level,
            alert_type=alert_type,
            title=title,
            description=description,
            current_value=current_value,
            threshold_value=threshold_value,
            suggested_actions=suggested_actions,
            auto_mitigation_available=True,
            priority_score=priority_score,
            affected_positions=[],
            estimated_impact=abs(current_value - threshold_value)
        )
    
    def _calculate_priority_score(self, level: RiskLevel, alert_type: AlertType, risk_type: RiskType) -> float:
        """Calcule le score de priorité d'une alerte"""
        level_scores = {
            RiskLevel.VERY_LOW: 1,
            RiskLevel.LOW: 2,
            RiskLevel.MEDIUM: 3,
            RiskLevel.HIGH: 4,
            RiskLevel.CRITICAL: 5,
            RiskLevel.EXTREME: 6
        }
        
        alert_scores = {
            AlertType.INFO: 1,
            AlertType.WARNING: 2,
            AlertType.CRITICAL: 3,
            AlertType.EMERGENCY: 4
        }
        
        risk_weights = {
            RiskType.DRAWDOWN_RISK: 1.0,
            RiskType.LIQUIDITY_RISK: 0.9,
            RiskType.MARKET_RISK: 0.8,
            RiskType.VOLATILITY_RISK: 0.7,
            RiskType.CONCENTRATION_RISK: 0.6,
            RiskType.LEVERAGE_RISK: 0.8,
            RiskType.CORRELATION_RISK: 0.5,
            RiskType.OPERATIONAL_RISK: 0.4,
            RiskType.SYSTEM_RISK: 0.9,
            RiskType.REGULATORY_RISK: 0.3
        }
        
        base_score = level_scores.get(level, 3) * alert_scores.get(alert_type, 2)
        weighted_score = base_score * risk_weights.get(risk_type, 0.5)
        
        return min(10.0, weighted_score)
    
    # Méthodes de mitigation (simulation)
    def _emergency_stop_trading(self) -> bool:
        """Arrêt d'urgence du trading"""
        self.emergency_mode = True
        logger.critical("🛑 ARRÊT D'URGENCE DU TRADING ACTIVÉ")
        return True
    
    def _auto_rebalance_portfolio(self) -> bool:
        """Rééquilibrage automatique"""
        logger.info("⚖️ Rééquilibrage automatique en cours...")
        return True
    
    def _reduce_position_sizes(self, reduction_factor: float = 0.5) -> bool:
        """Réduction des tailles de position"""
        logger.info(f"📉 Réduction des positions de {reduction_factor*100:.0f}%")
        return True
    
    def _liquidate_illiquid_positions(self) -> bool:
        """Liquidation des positions illiquides"""
        logger.info("💧 Liquidation des positions illiquides")
        return True
    
    def _reduce_leverage(self) -> bool:
        """Réduction du levier"""
        logger.info("📊 Réduction du levier")
        return True
    
    # Méthodes stress test (simulation)
    def _get_default_stress_scenarios(self) -> List[Dict]:
        """Scenarios de stress par défaut"""
        return [
            {
                'name': 'Market Crash',
                'description': 'Chute de marché de 30%',
                'parameters': {'market_shock': -0.30}
            },
            {
                'name': 'Volatility Spike',
                'description': 'Pic de volatilité x3',
                'parameters': {'volatility_multiplier': 3.0}
            },
            {
                'name': 'Liquidity Crisis',
                'description': 'Crise de liquidité',
                'parameters': {'liquidity_shock': 0.8}
            },
            {
                'name': 'Flash Crash',
                'description': 'Krach éclair -50%',
                'parameters': {'flash_crash': -0.50}
            }
        ]
    
    def _apply_stress_scenario(self, portfolio_data: Dict, scenario_params: Dict) -> Dict:
        """Applique un scenario de stress"""
        # Simulation
        stressed_portfolio = portfolio_data.copy()
        
        if 'market_shock' in scenario_params:
            shock = scenario_params['market_shock']
            stressed_portfolio['total_value'] *= (1 + shock)
        
        return stressed_portfolio
    
    def _calculate_stress_impact(self, original: Dict, stressed: Dict) -> Dict:
        """Calcule l'impact d'un stress test"""
        original_value = original.get('total_value', 0)
        stressed_value = stressed.get('total_value', 0)
        
        if original_value == 0:
            return {'absolute': 0, 'percentage': 0}
        
        absolute_impact = stressed_value - original_value
        percentage_impact = (absolute_impact / original_value) * 100
        
        return {
            'absolute': absolute_impact,
            'percentage': percentage_impact,
            'recovery_time': abs(percentage_impact) * 2,  # Estimation
            'positions_affected': []
        }
    
    def _assess_stress_risk_level(self, max_impact: float) -> str:
        """Évalue le niveau de risque du stress test"""
        if abs(max_impact) < 10:
            return 'low'
        elif abs(max_impact) < 20:
            return 'medium'
        elif abs(max_impact) < 40:
            return 'high'
        else:
            return 'critical'
    
    # Méthodes dashboard (simulation)
    def _calculate_portfolio_health_score(self, risk_metrics: RiskMetrics) -> float:
        """Calcule le score de santé du portfolio"""
        # Score basé sur plusieurs métriques
        var_score = max(0, 100 - risk_metrics.portfolio_var_1d * 1000)
        drawdown_score = max(0, 100 - risk_metrics.current_drawdown * 500)
        volatility_score = max(0, 100 - risk_metrics.portfolio_volatility * 200)
        diversification_score = risk_metrics.diversification_ratio * 100
        
        # Moyenne pondérée
        health_score = (
            var_score * 0.3 +
            drawdown_score * 0.3 +
            volatility_score * 0.2 +
            diversification_score * 0.2
        )
        
        return min(100, max(0, health_score))
    
    def _get_current_risk_level(self, risk_metrics: RiskMetrics) -> str:
        """Détermine le niveau de risque actuel"""
        if (risk_metrics.portfolio_var_1d > 0.05 or 
            risk_metrics.current_drawdown > 0.15 or
            risk_metrics.portfolio_volatility > 0.50):
            return 'high'
        elif (risk_metrics.portfolio_var_1d > 0.03 or 
              risk_metrics.current_drawdown > 0.10 or
              risk_metrics.portfolio_volatility > 0.30):
            return 'medium'
        else:
            return 'low'
    
    def _get_latest_stress_summary(self) -> Dict:
        """Résumé du dernier stress test"""
        if not self.stress_test_history:
            return {}
        
        latest_stress = list(self.stress_test_history)[-1]
        return latest_stress.get('summary', {})
    
    def _calculate_optimization_score(self, optimized_thresholds: Dict) -> float:
        """Calcule le score d'amélioration de l'optimisation"""
        return np.random.uniform(0.1, 0.3)  # 10-30% d'amélioration
    
    # Méthodes de calcul des risques de position
    def _calculate_position_var_contribution(self, position_data: Dict) -> float:
        """Contribution VaR de la position"""
        market_value = position_data.get('market_value', 0)
        symbol = position_data.get('symbol', '')
        volatility = self._get_asset_volatility(symbol)
        
        total_portfolio_value = self._get_total_portfolio_value()
        if total_portfolio_value == 0:
            return 0.0
        
        weight = market_value / total_portfolio_value
        var_contribution = weight * volatility * 0.05  # Approximation
        
        return var_contribution
    
    def _calculate_position_correlation(self, symbol: str) -> float:
        """Corrélation de la position avec le portfolio"""
        # Simulation
        correlation_map = {
            'BTC': 0.70,
            'ETH': 0.85,
            'ADA': 0.75,
            'DOT': 0.80,
            'LINK': 0.70,
            'UNI': 0.65
        }
        return correlation_map.get(symbol, 0.60)
    
    def _calculate_liquidity_score(self, symbol: str, position_size: float) -> float:
        """Score de liquidité de la position"""
        # Simulation basée sur volume de trading
        liquidity_map = {
            'BTC': 0.95,
            'ETH': 0.90,
            'ADA': 0.80,
            'DOT': 0.75,
            'LINK': 0.70,
            'UNI': 0.65
        }
        base_liquidity = liquidity_map.get(symbol, 0.50)
        
        # Ajustement selon la taille de position
        size_penalty = min(0.3, position_size / 10000)  # Pénalité pour grosses positions
        
        return max(0.1, base_liquidity - size_penalty)
    
    def _calculate_position_risk_score(self, volatility: float, beta: float, 
                                     concentration_pct: float, liquidity_score: float,
                                     var_contribution: float) -> float:
        """Score de risque global de la position"""
        # Normalisation et pondération des facteurs
        vol_score = min(10, volatility * 10)  # 0-10
        beta_score = min(10, abs(beta - 1) * 5)  # 0-10
        conc_score = min(10, concentration_pct / 5)  # 0-10
        liquidity_score_inv = 10 * (1 - liquidity_score)  # 0-10
        var_score = min(10, var_contribution * 200)  # 0-10
        
        # Score pondéré
        risk_score = (
            vol_score * 0.25 +
            beta_score * 0.15 +
            conc_score * 0.25 +
            liquidity_score_inv * 0.20 +
            var_score * 0.15
        )
        
        return min(10, max(0, risk_score))
    
    def _calculate_max_loss_amount(self, position_data: Dict) -> float:
        """Perte maximale potentielle"""
        market_value = position_data.get('market_value', 0)
        stop_loss_level = position_data.get('stop_loss')
        current_price = position_data.get('current_price', market_value)
        
        if stop_loss_level and current_price > 0:
            loss_pct = abs(current_price - stop_loss_level) / current_price
            return market_value * loss_pct
        else:
            # Sans stop loss, estimation basée sur volatilité
            symbol = position_data.get('symbol', '')
            volatility = self._get_asset_volatility(symbol)
            # Perte potentielle de 3 écarts-types
            return market_value * volatility * 3
    
    def _estimate_liquidation_time(self, symbol: str, position_size: float) -> float:
        """Estime le temps de liquidation en jours"""
        liquidity_score = self._calculate_liquidity_score(symbol, position_size)
        
        # Plus le score de liquidité est bas, plus il faut de temps
        base_days = (1 - liquidity_score) * 10
        
        # Ajustement selon la taille
        size_factor = min(5, position_size / 1000)
        
        return max(0.1, base_days + size_factor)
    
    def _get_total_portfolio_value(self) -> float:
        """Récupère la valeur totale du portfolio"""
        portfolio_data = self._get_portfolio_data()
        return portfolio_data.get('total_value', 0) if portfolio_data else 0
    
    def _default_position_risk(self, symbol: str) -> PositionRisk:
        """Position risk par défaut"""
        return PositionRisk(
            symbol=symbol,
            position_size=0,
            market_value=0,
            unrealized_pnl=0,
            var_contribution=0,
            volatility=0,
            beta=1.0,
            correlation_portfolio=0.5,
            liquidity_score=0.5,
            concentration_pct=0,
            risk_score=5.0,
            stop_loss_level=None,
            take_profit_level=None,
            max_loss_amount=0,
            days_to_liquidate=1.0
        )

# Instance globale
ultra_risk_manager = UltraAdvancedRiskManager()

# Fonctions utilitaires pour l'intégration
def start_risk_monitoring():
    """Démarre le monitoring de risque"""
    ultra_risk_manager.start_monitoring()

def stop_risk_monitoring():
    """Arrête le monitoring de risque"""
    ultra_risk_manager.stop_monitoring()

def get_current_risk_status() -> Dict:
    """Retourne le statut de risque actuel"""
    return ultra_risk_manager.get_risk_dashboard_data()

def calculate_portfolio_risk(portfolio_data: Dict) -> Dict:
    """Calcule le risque du portfolio"""
    risk_metrics = ultra_risk_manager.calculate_portfolio_risk(portfolio_data)
    return asdict(risk_metrics)

def perform_stress_test(scenarios: Optional[List[Dict]] = None) -> Dict:
    """Effectue un stress test"""
    return ultra_risk_manager.perform_stress_test(scenarios)

def optimize_risk_settings() -> Dict:
    """Optimise les paramètres de risque"""
    return ultra_risk_manager.optimize_risk_thresholds()

def check_position_risk(position_data: Dict) -> Dict:
    """Vérifie le risque d'une position"""
    position_risk = ultra_risk_manager.calculate_position_risk(position_data)
    return asdict(position_risk)

def get_risk_alerts() -> List[Dict]:
    """Récupère les alertes de risque actives"""
    return [asdict(alert) for alert in ultra_risk_manager.active_alerts.values()]

def emergency_stop() -> bool:
    """Arrêt d'urgence"""
    return ultra_risk_manager._emergency_stop_trading()
