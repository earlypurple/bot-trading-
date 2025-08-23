from abc import ABC, abstractmethod
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class TradeSignal:
    """Represents a trading signal"""
    symbol: str
    side: str  # BUY or SELL
    quantity: float
    price: Optional[float] = None
    confidence: float = 0.0  # Signal confidence 0-1
    reason: str = ""
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

class BaseStrategy(ABC):
    """
    Enhanced abstract base class for all trading strategies.
    """

    def __init__(self, name: str, description: str, risk_level: str = "MEDIUM"):
        self.name = name
        self.description = description
        self.risk_level = risk_level  # LOW, MEDIUM, HIGH
        self.status = "STOPPED"
        self.logger = logging.getLogger(f"strategy.{name}")
        
        # Performance tracking
        self.trades_executed = 0
        self.successful_trades = 0
        self.failed_trades = 0
        self.total_pnl = 0.0
        self.last_execution = None
        
        # Strategy parameters
        self.parameters = {}
        self.stop_loss = 0.02  # 2% default stop loss
        self.take_profit = 0.05  # 5% default take profit
        
        # Position tracking
        self.current_positions = {}
        
    @abstractmethod
    def execute(self) -> Optional[TradeSignal]:
        """
        Execute the trading strategy and return a signal if any.
        Must be implemented by each strategy.
        """
        pass
    
    def validate_signal(self, signal: TradeSignal) -> bool:
        """
        Validate a trading signal before execution.
        Can be overridden by specific strategies for custom validation.
        """
        if not signal.symbol or not signal.side or signal.quantity <= 0:
            self.logger.warning(f"Invalid signal: {signal}")
            return False
            
        if signal.confidence < 0.5:  # Minimum confidence threshold
            self.logger.info(f"Signal confidence too low: {signal.confidence}")
            return False
            
        return True
    
    def calculate_position_size(self, capital: float, price: float, volatility: float = 0.02) -> float:
        """
        Calculate position size based on risk management rules.
        """
        # Kelly Criterion simplified implementation
        win_rate = self.successful_trades / max(self.trades_executed, 1)
        avg_win = self.total_pnl / max(self.successful_trades, 1) if self.successful_trades > 0 else 0
        avg_loss = abs(self.total_pnl) / max(self.failed_trades, 1) if self.failed_trades > 0 else volatility * price
        
        if avg_loss == 0:
            kelly_fraction = 0.01  # Conservative fallback
        else:
            kelly_fraction = (win_rate * avg_win - (1 - win_rate) * avg_loss) / avg_win
        
        # Conservative position sizing (max 10% of capital)
        kelly_fraction = min(max(kelly_fraction, 0.01), 0.10)
        
        return (capital * kelly_fraction) / price

    def start(self):
        """
        Start the trading strategy.
        """
        self.status = "RUNNING"
        self.last_execution = datetime.utcnow()
        self.logger.info(f"Strategy {self.name} started with risk level {self.risk_level}")

    def stop(self):
        """
        Stop the trading strategy.
        """
        self.status = "STOPPED"
        self.logger.info(f"Strategy {self.name} stopped")

    def pause(self):
        """
        Pause the trading strategy.
        """
        self.status = "PAUSED"
        self.logger.info(f"Strategy {self.name} paused")

    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive status of the trading strategy.
        """
        success_rate = (self.successful_trades / max(self.trades_executed, 1)) * 100
        
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "risk_level": self.risk_level,
            "trades_executed": self.trades_executed,
            "successful_trades": self.successful_trades,
            "failed_trades": self.failed_trades,
            "success_rate": round(success_rate, 2),
            "total_pnl": round(self.total_pnl, 2),
            "last_execution": self.last_execution.isoformat() if self.last_execution else None,
            "current_positions": len(self.current_positions),
            "parameters": self.parameters
        }
    
    def update_parameters(self, new_parameters: Dict[str, Any]):
        """
        Update strategy parameters.
        """
        self.parameters.update(new_parameters)
        self.logger.info(f"Parameters updated for {self.name}: {new_parameters}")
    
    def record_trade(self, signal: TradeSignal, success: bool, pnl: float):
        """
        Record trade execution results.
        """
        self.trades_executed += 1
        
        if success:
            self.successful_trades += 1
        else:
            self.failed_trades += 1
            
        self.total_pnl += pnl
        self.last_execution = datetime.utcnow()
        
        self.logger.info(f"Trade recorded: {signal.side} {signal.quantity} {signal.symbol} - "
                        f"Success: {success}, PnL: {pnl}")
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """
        Calculate and return performance metrics.
        """
        total_trades = max(self.trades_executed, 1)
        success_rate = self.successful_trades / total_trades
        
        # Calculate average profit per trade
        avg_profit_per_trade = self.total_pnl / total_trades
        
        # Calculate Sharpe ratio (simplified)
        returns = [avg_profit_per_trade] * total_trades  # Simplified for demo
        avg_return = sum(returns) / len(returns) if returns else 0
        return_std = (sum([(r - avg_return)**2 for r in returns]) / len(returns))**0.5 if returns else 1
        sharpe_ratio = avg_return / return_std if return_std > 0 else 0
        
        return {
            "success_rate": success_rate,
            "total_pnl": self.total_pnl,
            "avg_profit_per_trade": avg_profit_per_trade,
            "sharpe_ratio": sharpe_ratio,
            "total_trades": self.trades_executed
        }
