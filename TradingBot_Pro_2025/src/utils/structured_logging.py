"""
🗂️ SYSTÈME DE LOGS STRUCTURÉS JSON - TRADINGBOT PRO 2025 ULTRA
Logs ultra-professionnels pour analyse avancée
"""

import json
import logging
import structlog
from datetime import datetime
import traceback
import uuid
from typing import Dict, Any, Optional
import os
from pathlib import Path

class JSONStructuredLogger:
    """Système de logs structurés en JSON ultra-avancé"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configuration structlog
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        
        # Configuration des handlers
        self.setup_loggers()
        
    def setup_loggers(self):
        """Configuration des loggers spécialisés"""
        
        # Logger principal
        self.main_logger = structlog.get_logger("tradingbot.main")
        
        # Logger trading spécialisé
        self.trading_logger = structlog.get_logger("tradingbot.trading")
        
        # Logger API
        self.api_logger = structlog.get_logger("tradingbot.api")
        
        # Logger IA
        self.ai_logger = structlog.get_logger("tradingbot.ai")
        
        # Logger sécurité
        self.security_logger = structlog.get_logger("tradingbot.security")
        
        # Logger performance
        self.performance_logger = structlog.get_logger("tradingbot.performance")
        
        # Configuration des fichiers de logs
        log_files = {
            'main': self.log_dir / 'main.json',
            'trading': self.log_dir / 'trading.json',
            'api': self.log_dir / 'api.json',
            'ai': self.log_dir / 'ai.json',
            'security': self.log_dir / 'security.json',
            'performance': self.log_dir / 'performance.json',
            'errors': self.log_dir / 'errors.json'
        }
        
        # Setup handlers pour chaque logger
        for log_name, log_file in log_files.items():
            handler = logging.FileHandler(log_file)
            handler.setFormatter(logging.Formatter('%(message)s'))
            
            logger = logging.getLogger(f"tradingbot.{log_name}")
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
    
    def log_trade(self, trade_data: Dict[str, Any]):
        """Méthode de compatibilité pour log_trade"""
        success = trade_data.get('success', True)
        pnl = trade_data.get('profit', 0.0)
        self.log_trade_execution(trade_data, success, pnl)
    
    def log_ai_decision(self, decision_data: Dict[str, Any]):
        """Méthode de compatibilité pour log_ai_decision"""
        symbol = decision_data.get('symbol', 'UNKNOWN')
        prediction = {
            'action': decision_data.get('prediction', 'hold'),
            'confidence': decision_data.get('confidence', 0)
        }
        model_version = decision_data.get('algorithm', 'v1.0')
        self.log_ai_prediction(symbol, prediction, model_version)
    
    def log_trade_execution(self, trade_data: Dict[str, Any], success: bool, pnl: float):
        """Log d'exécution de trade structuré"""
        self.trading_logger.info(
            "trade_executed",
            trade_id=str(uuid.uuid4()),
            symbol=trade_data.get('symbol'),
            side=trade_data.get('side'),
            amount=trade_data.get('amount'),
            price=trade_data.get('price'),
            success=success,
            pnl=pnl,
            timestamp=datetime.now().isoformat(),
            strategy=trade_data.get('strategy', 'ai'),
            confidence=trade_data.get('confidence', 0),
            execution_time_ms=trade_data.get('execution_time', 0)
        )
    
    def log_ai_prediction(self, symbol: str, prediction: Dict[str, Any], model_version: str):
        """Log de prédiction IA structuré"""
        self.ai_logger.info(
            "ai_prediction",
            prediction_id=str(uuid.uuid4()),
            symbol=symbol,
            prediction=prediction,
            model_version=model_version,
            timestamp=datetime.now().isoformat(),
            confidence_score=prediction.get('confidence', 0),
            recommendation=prediction.get('action', 'hold')
        )
    
    def log_api_call(self, endpoint: str, method: str, status_code: int, response_time_ms: float, data_size: int = 0):
        """Log d'appel API structuré"""
        self.api_logger.info(
            "api_call",
            call_id=str(uuid.uuid4()),
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            response_time_ms=response_time_ms,
            data_size_bytes=data_size,
            timestamp=datetime.now().isoformat(),
            success=status_code < 400
        )
    
    def log_security_event(self, event_type: str, severity: str, details: Dict[str, Any]):
        """Log d'événement de sécurité"""
        self.security_logger.warning(
            "security_event",
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            severity=severity,
            details=details,
            timestamp=datetime.now().isoformat(),
            ip_address=details.get('ip_address', 'unknown'),
            user_agent=details.get('user_agent', 'unknown')
        )
    
    def log_performance_metric(self, metric_name: str, value: float, unit: str, context: Dict[str, Any] = None):
        """Log de métrique de performance"""
        self.performance_logger.info(
            "performance_metric",
            metric_id=str(uuid.uuid4()),
            metric_name=metric_name,
            value=value,
            unit=unit,
            context=context or {},
            timestamp=datetime.now().isoformat()
        )
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log d'erreur structuré"""
        error_logger = structlog.get_logger("tradingbot.errors")
        error_logger.error(
            "error_occurred",
            error_id=str(uuid.uuid4()),
            error_type=type(error).__name__,
            error_message=str(error),
            traceback=traceback.format_exc(),
            context=context or {},
            timestamp=datetime.now().isoformat()
        )
    
    def get_log_analytics(self, log_type: str = "trading", hours: int = 24) -> Dict[str, Any]:
        """Analyse des logs pour insights"""
        log_file = self.log_dir / f"{log_type}.json"
        
        if not log_file.exists():
            return {"error": f"Log file {log_type}.json not found"}
        
        analytics = {
            "total_entries": 0,
            "success_rate": 0,
            "error_count": 0,
            "avg_response_time": 0,
            "top_symbols": {},
            "performance_summary": {}
        }
        
        try:
            with open(log_file, 'r') as f:
                entries = []
                for line in f:
                    try:
                        entry = json.loads(line)
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue
                
                analytics["total_entries"] = len(entries)
                
                if log_type == "trading":
                    successful_trades = sum(1 for e in entries if e.get('success', False))
                    analytics["success_rate"] = (successful_trades / len(entries) * 100) if entries else 0
                    
                    # Top symbols
                    symbols = {}
                    for entry in entries:
                        symbol = entry.get('symbol', 'unknown')
                        symbols[symbol] = symbols.get(symbol, 0) + 1
                    analytics["top_symbols"] = dict(sorted(symbols.items(), key=lambda x: x[1], reverse=True)[:5])
                
                elif log_type == "api":
                    response_times = [e.get('response_time_ms', 0) for e in entries if 'response_time_ms' in e]
                    analytics["avg_response_time"] = sum(response_times) / len(response_times) if response_times else 0
                    analytics["error_count"] = sum(1 for e in entries if e.get('status_code', 200) >= 400)
        
        except Exception as e:
            analytics["error"] = f"Analysis failed: {str(e)}"
        
        return analytics

# Instance globale
structured_logger = JSONStructuredLogger()

# Alias pour compatibilité
StructuredLogger = JSONStructuredLogger

# Fonctions utilitaires
def log_trade(trade_data: Dict[str, Any], success: bool, pnl: float):
    """Log de trade simplifié"""
    structured_logger.log_trade_execution(trade_data, success, pnl)

def log_ai_prediction(symbol: str, prediction: Dict[str, Any], model_version: str = "v1.0"):
    """Log de prédiction IA simplifié"""
    structured_logger.log_ai_prediction(symbol, prediction, model_version)

def log_api_call(endpoint: str, method: str, status_code: int, response_time_ms: float):
    """Log d'API simplifié"""
    structured_logger.log_api_call(endpoint, method, status_code, response_time_ms)

def log_error(error: Exception, context: Dict[str, Any] = None):
    """Log d'erreur simplifié"""
    structured_logger.log_error(error, context)

def get_trading_analytics(hours: int = 24) -> Dict[str, Any]:
    """Analytics de trading"""
    return structured_logger.get_log_analytics("trading", hours)

if __name__ == "__main__":
    # Test du système de logs
    print("🗂️ Test du système de logs structurés JSON")
    
    # Test trade log
    log_trade({
        'symbol': 'BTC/USD',
        'side': 'buy',
        'amount': 0.001,
        'price': 45000,
        'strategy': 'ai_prediction',
        'confidence': 0.85
    }, True, 15.50)
    
    # Test AI prediction
    log_ai_prediction('ETH/USD', {
        'action': 'buy',
        'confidence': 0.92,
        'price_target': 2600
    })
    
    # Test API call
    log_api_call('/api/market-data', 'GET', 200, 150.5)
    
    # Test error
    try:
        raise ValueError("Test error for logging")
    except Exception as e:
        log_error(e, {'test_context': 'structured_logging_test'})
    
    print("✅ Logs structurés créés avec succès !")
    print("📊 Analysez les fichiers dans le dossier /logs/")
