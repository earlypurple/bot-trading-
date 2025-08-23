"""
Advanced logging and monitoring system for TradingBot Pro 2025
"""
import logging
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import structlog

class TradingBotLogger:
    """Advanced logging system for trading bot"""
    
    def __init__(self, log_level: str = "INFO", log_file: str = "trading_bot.log"):
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.log_file = log_file
        self.setup_logging()
        
    def setup_logging(self):
        """Setup structured logging with multiple handlers"""
        
        # Configure structlog
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
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        
        json_formatter = logging.Formatter('%(message)s')
        
        # Root logger configuration
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(console_handler)
        
        # File handler with rotation
        file_handler = RotatingFileHandler(
            self.log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)
        
        # Error file handler
        error_handler = RotatingFileHandler(
            "trading_bot_errors.log",
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(error_handler)
        
        # Trading activity log (separate file)
        trading_handler = TimedRotatingFileHandler(
            "trading_activity.log",
            when='midnight',
            interval=1,
            backupCount=30
        )
        trading_handler.setLevel(logging.INFO)
        trading_handler.setFormatter(json_formatter)
        
        # Create trading logger
        trading_logger = logging.getLogger('trading')
        trading_logger.addHandler(trading_handler)
        trading_logger.setLevel(logging.INFO)
        trading_logger.propagate = False

class PerformanceMonitor:
    """Performance monitoring system"""
    
    def __init__(self):
        self.metrics = {}
        self.start_times = {}
        self.logger = structlog.get_logger("performance")
        
    def start_timer(self, operation: str):
        """Start timing an operation"""
        self.start_times[operation] = datetime.now()
        
    def end_timer(self, operation: str, additional_data: Optional[Dict] = None):
        """End timing and log performance"""
        if operation in self.start_times:
            duration = (datetime.now() - self.start_times[operation]).total_seconds()
            
            log_data = {
                "operation": operation,
                "duration_seconds": duration,
                "timestamp": datetime.now().isoformat()
            }
            
            if additional_data:
                log_data.update(additional_data)
                
            self.logger.info("Operation completed", **log_data)
            
            # Store metrics
            if operation not in self.metrics:
                self.metrics[operation] = []
            self.metrics[operation].append(duration)
            
            del self.start_times[operation]
            
    def get_average_time(self, operation: str) -> Optional[float]:
        """Get average execution time for an operation"""
        if operation in self.metrics:
            return sum(self.metrics[operation]) / len(self.metrics[operation])
        return None

class TradingMetrics:
    """Trading-specific metrics collection"""
    
    def __init__(self):
        self.trade_count = 0
        self.successful_trades = 0
        self.failed_trades = 0
        self.total_pnl = 0.0
        self.logger = structlog.get_logger("trading")
        
    def log_trade(self, trade_data: Dict[str, Any]):
        """Log a trade with all relevant data"""
        self.trade_count += 1
        
        if trade_data.get('status') == 'EXECUTED':
            self.successful_trades += 1
            pnl = trade_data.get('pnl', 0)
            self.total_pnl += pnl
        elif trade_data.get('status') == 'FAILED':
            self.failed_trades += 1
            
        # Enrich trade data with metrics
        enriched_data = {
            **trade_data,
            "trade_number": self.trade_count,
            "success_rate": self.successful_trades / self.trade_count if self.trade_count > 0 else 0,
            "total_pnl": self.total_pnl,
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.info("Trade executed", **enriched_data)
        
    def log_strategy_event(self, strategy_name: str, event: str, data: Dict[str, Any] = None):
        """Log strategy-related events"""
        log_data = {
            "strategy": strategy_name,
            "event": event,
            "timestamp": datetime.now().isoformat()
        }
        
        if data:
            log_data.update(data)
            
        self.logger.info("Strategy event", **log_data)
        
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of trading metrics"""
        return {
            "total_trades": self.trade_count,
            "successful_trades": self.successful_trades,
            "failed_trades": self.failed_trades,
            "success_rate": self.successful_trades / self.trade_count if self.trade_count > 0 else 0,
            "total_pnl": self.total_pnl,
            "average_pnl_per_trade": self.total_pnl / self.trade_count if self.trade_count > 0 else 0
        }

class AlertSystem:
    """Alert and notification system"""
    
    def __init__(self):
        self.logger = structlog.get_logger("alerts")
        
    def send_alert(self, level: str, message: str, data: Optional[Dict] = None):
        """Send alert with specified level"""
        alert_data = {
            "alert_level": level,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        if data:
            alert_data.update(data)
            
        # Log the alert
        if level == "CRITICAL":
            self.logger.critical("Critical alert", **alert_data)
        elif level == "ERROR":
            self.logger.error("Error alert", **alert_data)
        elif level == "WARNING":
            self.logger.warning("Warning alert", **alert_data)
        else:
            self.logger.info("Info alert", **alert_data)
            
        # Here you would implement actual notification sending:
        # - Email notifications
        # - Telegram/Discord messages
        # - SMS alerts
        # - Webhook calls
        
    def send_trade_alert(self, trade_data: Dict[str, Any]):
        """Send trade-specific alert"""
        if trade_data.get('pnl', 0) < -1000:  # Large loss
            self.send_alert("ERROR", "Large loss detected", trade_data)
        elif trade_data.get('pnl', 0) > 1000:  # Large gain
            self.send_alert("INFO", "Large gain achieved", trade_data)

# Global instances
logger_system = TradingBotLogger()
performance_monitor = PerformanceMonitor()
trading_metrics = TradingMetrics()
alert_system = AlertSystem()

# Convenience functions
def get_logger(name: str):
    """Get a logger instance"""
    return structlog.get_logger(name)

def log_trade(trade_data: Dict[str, Any]):
    """Log a trade"""
    trading_metrics.log_trade(trade_data)
    alert_system.send_trade_alert(trade_data)

def log_strategy_event(strategy_name: str, event: str, data: Dict[str, Any] = None):
    """Log strategy event"""
    trading_metrics.log_strategy_event(strategy_name, event, data)

if __name__ == '__main__':
    # Test the logging system
    logger = get_logger("test")
    logger.info("Testing structured logging", operation="test", value=123)
    
    # Test performance monitoring
    performance_monitor.start_timer("test_operation")
    import time
    time.sleep(0.1)
    performance_monitor.end_timer("test_operation", {"additional": "data"})
    
    # Test trade logging
    trade_data = {
        "symbol": "BTC-USD",
        "side": "BUY",
        "quantity": 0.1,
        "price": 50000,
        "status": "EXECUTED",
        "pnl": 100
    }
    log_trade(trade_data)
