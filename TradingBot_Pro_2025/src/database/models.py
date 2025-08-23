"""
Database models for TradingBot Pro 2025
"""
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import get_config

Base = declarative_base()
config = get_config()

class Trade(Base):
    """Model for storing trade information"""
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    strategy_name = Column(String(50), nullable=False)
    symbol = Column(String(20), nullable=False)
    side = Column(String(10), nullable=False)  # BUY or SELL
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    profit_loss = Column(Float, default=0.0)
    fees = Column(Float, default=0.0)
    status = Column(String(20), default='PENDING')  # PENDING, EXECUTED, CANCELLED, FAILED

class Strategy(Base):
    """Model for storing strategy information"""
    __tablename__ = 'strategies'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    status = Column(String(20), default='STOPPED')  # RUNNING, STOPPED, PAUSED
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    parameters = Column(Text)  # JSON string of strategy parameters
    
    # Relationship with trades
    trades = relationship("Trade", backref="strategy")

class Portfolio(Base):
    """Model for storing portfolio information"""
    __tablename__ = 'portfolio'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), nullable=False)
    quantity = Column(Float, nullable=False)
    average_price = Column(Float, nullable=False)
    current_price = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RiskMetrics(Base):
    """Model for storing risk metrics"""
    __tablename__ = 'risk_metrics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.utcnow)
    total_portfolio_value = Column(Float, nullable=False)
    daily_pnl = Column(Float, default=0.0)
    max_drawdown = Column(Float, default=0.0)
    var_95 = Column(Float, default=0.0)  # Value at Risk 95%
    sharpe_ratio = Column(Float, default=0.0)
    sortino_ratio = Column(Float, default=0.0)

class AlertLog(Base):
    """Model for storing alerts and notifications"""
    __tablename__ = 'alert_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(20), nullable=False)  # INFO, WARNING, ERROR, CRITICAL
    message = Column(Text, nullable=False)
    strategy_name = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    acknowledged = Column(Boolean, default=False)

# Database engine and session
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == '__main__':
    create_tables()
    print("Database tables created successfully!")
