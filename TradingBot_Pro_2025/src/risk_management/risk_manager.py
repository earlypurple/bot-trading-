"""
Risk Management System for TradingBot Pro 2025
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class RiskLimits:
    """Risk limits configuration"""
    max_position_size: float = 0.1  # Maximum position size as percentage of portfolio
    max_daily_loss: float = 0.05    # Maximum daily loss as percentage
    max_drawdown: float = 0.15      # Maximum drawdown allowed
    max_correlation: float = 0.7    # Maximum correlation between positions
    max_trades_per_day: int = 1000  # Maximum trades per day
    stop_loss_percentage: float = 0.02  # Default stop loss
    take_profit_percentage: float = 0.05  # Default take profit

class RiskManager:
    """Advanced risk management system"""
    
    def __init__(self, risk_limits: RiskLimits = None):
        self.risk_limits = risk_limits or RiskLimits()
        self.daily_trades = 0
        self.daily_pnl = 0.0
        self.portfolio_value = 100000.0  # Default portfolio value
        self.positions = {}
        self.trade_history = []
        self.logger = logging.getLogger(__name__)
        
    def check_position_size(self, symbol: str, quantity: float, price: float) -> bool:
        """Check if position size is within limits"""
        position_value = quantity * price
        max_position_value = self.portfolio_value * self.risk_limits.max_position_size
        
        if position_value > max_position_value:
            self.logger.warning(f"Position size too large for {symbol}: {position_value} > {max_position_value}")
            return False
        return True
    
    def check_daily_loss_limit(self, potential_loss: float) -> bool:
        """Check if potential loss exceeds daily limit"""
        total_potential_loss = self.daily_pnl + potential_loss
        max_daily_loss_value = self.portfolio_value * self.risk_limits.max_daily_loss
        
        if abs(total_potential_loss) > max_daily_loss_value:
            self.logger.warning(f"Daily loss limit exceeded: {total_potential_loss}")
            return False
        return True
    
    def check_trade_frequency(self) -> bool:
        """Check if daily trade limit is exceeded"""
        if self.daily_trades >= self.risk_limits.max_trades_per_day:
            self.logger.warning(f"Daily trade limit exceeded: {self.daily_trades}")
            return False
        return True
    
    def calculate_position_correlation(self, symbol1: str, symbol2: str) -> float:
        """Calculate correlation between two positions (simplified)"""
        # This is a simplified correlation calculation
        # In production, you would use actual price data
        return 0.0
    
    def check_correlation_limits(self, new_symbol: str) -> bool:
        """Check if adding new position would exceed correlation limits"""
        for existing_symbol in self.positions:
            correlation = self.calculate_position_correlation(new_symbol, existing_symbol)
            if correlation > self.risk_limits.max_correlation:
                self.logger.warning(f"High correlation between {new_symbol} and {existing_symbol}: {correlation}")
                return False
        return True
    
    def calculate_var(self, confidence_level: float = 0.95) -> float:
        """Calculate Value at Risk"""
        if not self.trade_history:
            return 0.0
        
        # Simplified VaR calculation using historical returns
        returns = [trade['pnl'] / self.portfolio_value for trade in self.trade_history[-30:]]  # Last 30 trades
        if not returns:
            return 0.0
        
        returns.sort()
        var_index = int((1 - confidence_level) * len(returns))
        return abs(returns[var_index]) * self.portfolio_value if returns else 0.0
    
    def calculate_sharpe_ratio(self, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio"""
        if not self.trade_history:
            return 0.0
        
        returns = [trade['pnl'] / self.portfolio_value for trade in self.trade_history[-252:]]  # Last year
        if not returns:
            return 0.0
        
        avg_return = sum(returns) / len(returns) * 252  # Annualized
        std_return = (sum([(r - avg_return/252)**2 for r in returns]) / len(returns))**0.5 * (252**0.5)
        
        return (avg_return - risk_free_rate) / std_return if std_return > 0 else 0.0
    
    def validate_trade(self, symbol: str, side: str, quantity: float, price: float) -> Dict[str, bool]:
        """Comprehensive trade validation"""
        checks = {
            'position_size': self.check_position_size(symbol, quantity, price),
            'daily_loss': self.check_daily_loss_limit(-quantity * price * 0.02),  # Assume 2% potential loss
            'trade_frequency': self.check_trade_frequency(),
            'correlation': self.check_correlation_limits(symbol)
        }
        
        return checks
    
    def record_trade(self, symbol: str, side: str, quantity: float, price: float, pnl: float):
        """Record trade for risk tracking"""
        trade = {
            'timestamp': datetime.now(),
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'price': price,
            'pnl': pnl
        }
        
        self.trade_history.append(trade)
        self.daily_trades += 1
        self.daily_pnl += pnl
        
        # Update positions
        if symbol in self.positions:
            if side == 'BUY':
                self.positions[symbol] += quantity
            else:
                self.positions[symbol] -= quantity
        else:
            self.positions[symbol] = quantity if side == 'BUY' else -quantity
    
    def get_risk_metrics(self) -> Dict[str, float]:
        """Get current risk metrics"""
        return {
            'daily_pnl': self.daily_pnl,
            'daily_trades': self.daily_trades,
            'portfolio_value': self.portfolio_value,
            'var_95': self.calculate_var(0.95),
            'sharpe_ratio': self.calculate_sharpe_ratio(),
            'position_count': len(self.positions),
            'max_position_value': max([abs(qty * 100) for qty in self.positions.values()]) if self.positions else 0
        }
    
    def reset_daily_metrics(self):
        """Reset daily tracking metrics"""
        self.daily_trades = 0
        self.daily_pnl = 0.0
        self.logger.info("Daily risk metrics reset")

# Emergency stop system
class EmergencyStop:
    """Emergency stop system for critical situations"""
    
    def __init__(self, risk_manager: RiskManager):
        self.risk_manager = risk_manager
        self.is_active = False
        self.logger = logging.getLogger(__name__)
        
    def check_emergency_conditions(self) -> bool:
        """Check if emergency stop should be triggered"""
        metrics = self.risk_manager.get_risk_metrics()
        
        # Trigger conditions
        conditions = [
            metrics['daily_pnl'] < -self.risk_manager.portfolio_value * 0.1,  # 10% daily loss
            metrics['var_95'] > self.risk_manager.portfolio_value * 0.2,     # High VaR
            metrics['daily_trades'] > self.risk_manager.risk_limits.max_trades_per_day * 1.5  # Excessive trading
        ]
        
        return any(conditions)
    
    def trigger_emergency_stop(self, reason: str = "Unknown"):
        """Trigger emergency stop"""
        self.is_active = True
        self.logger.critical(f"EMERGENCY STOP TRIGGERED: {reason}")
        # Here you would implement actual stop logic:
        # - Close all positions
        # - Cancel all pending orders
        # - Send alerts
        # - Pause all strategies
        
    def reset_emergency_stop(self):
        """Reset emergency stop"""
        self.is_active = False
        self.logger.info("Emergency stop reset")

if __name__ == '__main__':
    # Test the risk management system
    risk_limits = RiskLimits(max_position_size=0.05, max_daily_loss=0.03)
    risk_manager = RiskManager(risk_limits)
    
    # Test trade validation
    checks = risk_manager.validate_trade('BTC-USD', 'BUY', 0.1, 50000)
    print("Trade validation:", checks)
    
    # Test emergency stop
    emergency = EmergencyStop(risk_manager)
    if emergency.check_emergency_conditions():
        emergency.trigger_emergency_stop("Test condition")
