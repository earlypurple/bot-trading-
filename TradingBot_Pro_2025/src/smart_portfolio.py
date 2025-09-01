"""
Gestionnaire de Portfolio Intelligent - Capital Minimal Optimisé
================================================================
Système ultra-performant pour gérer un portfolio avec un capital minimal (1€)
et maximiser les rendements avec une gestion de risque intelligente.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_DOWN, ROUND_UP
import json
import sqlite3
from abc import ABC, abstractmethod
import numpy as np
from enum import Enum

logger = logging.getLogger(__name__)

class PositionType(Enum):
    LONG = "long"
    SHORT = "short"

class TradeStatus(Enum):
    PENDING = "pending"
    EXECUTED = "executed"
    CANCELLED = "cancelled"
    FILLED = "filled"

@dataclass
class Position:
    """Représente une position dans le portfolio"""
    symbol: str
    position_type: PositionType
    quantity: Decimal
    entry_price: Decimal
    current_price: Decimal
    entry_time: datetime
    stop_loss: Optional[Decimal] = None
    take_profit: Optional[Decimal] = None
    fees_paid: Decimal = Decimal('0')
    unrealized_pnl: Decimal = Decimal('0')
    realized_pnl: Decimal = Decimal('0')
    
    def update_current_price(self, new_price: Decimal):
        """Met à jour le prix actuel et calcule le PnL"""
        self.current_price = new_price
        
        if self.position_type == PositionType.LONG:
            self.unrealized_pnl = (new_price - self.entry_price) * self.quantity
        else:  # SHORT
            self.unrealized_pnl = (self.entry_price - new_price) * self.quantity
        
        # Soustraire les frais
        self.unrealized_pnl -= self.fees_paid
    
    @property
    def market_value(self) -> Decimal:
        """Valeur de marché actuelle de la position"""
        return self.quantity * self.current_price
    
    @property
    def pnl_percentage(self) -> Decimal:
        """Pourcentage de gain/perte"""
        invested_amount = self.quantity * self.entry_price
        if invested_amount > 0:
            return (self.unrealized_pnl / invested_amount) * 100
        return Decimal('0')

@dataclass
class Trade:
    """Représente un trade exécuté"""
    id: str
    symbol: str
    side: str  # "buy" ou "sell"
    quantity: Decimal
    price: Decimal
    timestamp: datetime
    fees: Decimal
    status: TradeStatus
    portfolio_value_before: Decimal
    portfolio_value_after: Decimal
    pnl: Decimal = Decimal('0')
    strategy_used: str = ""
    confidence_score: float = 0.0

@dataclass
class PortfolioMetrics:
    """Métriques de performance du portfolio"""
    total_value: Decimal
    available_cash: Decimal
    invested_amount: Decimal
    total_pnl: Decimal
    total_pnl_percentage: Decimal
    daily_pnl: Decimal
    daily_pnl_percentage: Decimal
    total_fees_paid: Decimal
    number_of_trades: int
    win_rate: float
    profit_factor: float
    sharpe_ratio: float
    max_drawdown: float
    positions_count: int
    diversification_score: float

class RiskCalculator:
    """Calculateur de risque intelligent pour capital minimal"""
    
    def __init__(self, min_capital: Decimal = Decimal('1.0')):
        self.min_capital = min_capital
        self.max_position_size_ratio = Decimal('0.25')  # 25% max par position
        self.max_daily_loss_ratio = Decimal('0.05')     # 5% perte max par jour
        self.min_trade_amount = Decimal('0.10')         # Trade minimal 10 centimes
        
    def calculate_position_size(self, 
                              available_capital: Decimal,
                              entry_price: Decimal,
                              confidence_score: float,
                              volatility: float) -> Decimal:
        """Calcule la taille optimale d'une position"""
        
        # Ajuster selon la confiance (50% à 100% de la taille max)
        confidence_multiplier = Decimal(str(0.5 + (confidence_score * 0.5)))
        
        # Ajuster selon la volatilité (moins de volatilité = plus de taille)
        volatility_multiplier = Decimal(str(max(0.3, 1.0 - volatility)))
        
        # Taille de base (pourcentage du capital)
        base_size = available_capital * self.max_position_size_ratio
        
        # Appliquer les multiplicateurs
        adjusted_size = base_size * confidence_multiplier * volatility_multiplier
        
        # Calculer la quantité
        quantity = adjusted_size / entry_price
        
        # Arrondir vers le bas pour éviter de dépasser le capital
        return quantity.quantize(Decimal('0.00000001'), rounding=ROUND_DOWN)
    
    def calculate_stop_loss(self,
                          entry_price: Decimal,
                          position_type: PositionType,
                          volatility: float) -> Decimal:
        """Calcule le stop loss optimal"""
        
        # Stop loss basé sur la volatilité (2-5% selon la volatilité)
        stop_loss_percentage = Decimal(str(0.02 + (volatility * 0.03)))
        
        if position_type == PositionType.LONG:
            return entry_price * (Decimal('1') - stop_loss_percentage)
        else:  # SHORT
            return entry_price * (Decimal('1') + stop_loss_percentage)
    
    def calculate_take_profit(self,
                            entry_price: Decimal,
                            position_type: PositionType,
                            confidence_score: float) -> Decimal:
        """Calcule le take profit optimal"""
        
        # Take profit basé sur la confiance (3-8% selon la confiance)
        take_profit_percentage = Decimal(str(0.03 + (confidence_score * 0.05)))
        
        if position_type == PositionType.LONG:
            return entry_price * (Decimal('1') + take_profit_percentage)
        else:  # SHORT
            return entry_price * (Decimal('1') - take_profit_percentage)
    
    def validate_trade(self,
                      available_capital: Decimal,
                      trade_amount: Decimal,
                      current_daily_loss: Decimal) -> Tuple[bool, str]:
        """Valide si un trade peut être exécuté"""
        
        # Vérifier le capital minimum
        if available_capital < self.min_capital:
            return False, "Capital insuffisant"
        
        # Vérifier le montant minimum de trade
        if trade_amount < self.min_trade_amount:
            return False, f"Montant de trade trop faible (min: {self.min_trade_amount}€)"
        
        # Vérifier qu'on ne dépasse pas le capital
        if trade_amount > available_capital:
            return False, "Montant de trade supérieur au capital disponible"
        
        # Vérifier la perte journalière maximale
        max_daily_loss = available_capital * self.max_daily_loss_ratio
        if abs(current_daily_loss) > max_daily_loss:
            return False, "Limite de perte journalière atteinte"
        
        return True, "Trade validé"

class PortfolioDatabase:
    """Base de données pour le portfolio"""
    
    def __init__(self, db_path: str = "portfolio.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table des positions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                position_type TEXT NOT NULL,
                quantity REAL NOT NULL,
                entry_price REAL NOT NULL,
                current_price REAL NOT NULL,
                entry_time TEXT NOT NULL,
                stop_loss REAL,
                take_profit REAL,
                fees_paid REAL DEFAULT 0,
                unrealized_pnl REAL DEFAULT 0,
                realized_pnl REAL DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des trades
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id TEXT PRIMARY KEY,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                quantity REAL NOT NULL,
                price REAL NOT NULL,
                timestamp TEXT NOT NULL,
                fees REAL NOT NULL,
                status TEXT NOT NULL,
                portfolio_value_before REAL,
                portfolio_value_after REAL,
                pnl REAL DEFAULT 0,
                strategy_used TEXT,
                confidence_score REAL DEFAULT 0
            )
        ''')
        
        # Table des métriques de portfolio
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS portfolio_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                total_value REAL NOT NULL,
                available_cash REAL NOT NULL,
                invested_amount REAL NOT NULL,
                total_pnl REAL NOT NULL,
                daily_pnl REAL NOT NULL,
                total_fees_paid REAL NOT NULL,
                number_of_trades INTEGER NOT NULL,
                win_rate REAL NOT NULL,
                positions_count INTEGER NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_position(self, position: Position) -> int:
        """Sauvegarde une position"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO positions (
                symbol, position_type, quantity, entry_price, current_price,
                entry_time, stop_loss, take_profit, fees_paid, unrealized_pnl, realized_pnl
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            position.symbol,
            position.position_type.value,
            float(position.quantity),
            float(position.entry_price),
            float(position.current_price),
            position.entry_time.isoformat(),
            float(position.stop_loss) if position.stop_loss else None,
            float(position.take_profit) if position.take_profit else None,
            float(position.fees_paid),
            float(position.unrealized_pnl),
            float(position.realized_pnl)
        ))
        
        position_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return position_id
    
    def save_trade(self, trade: Trade):
        """Sauvegarde un trade"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO trades (
                id, symbol, side, quantity, price, timestamp, fees, status,
                portfolio_value_before, portfolio_value_after, pnl, strategy_used, confidence_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            trade.id,
            trade.symbol,
            trade.side,
            float(trade.quantity),
            float(trade.price),
            trade.timestamp.isoformat(),
            float(trade.fees),
            trade.status.value,
            float(trade.portfolio_value_before),
            float(trade.portfolio_value_after),
            float(trade.pnl),
            trade.strategy_used,
            trade.confidence_score
        ))
        
        conn.commit()
        conn.close()
    
    def load_active_positions(self) -> List[Position]:
        """Charge les positions actives"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT symbol, position_type, quantity, entry_price, current_price,
                   entry_time, stop_loss, take_profit, fees_paid, unrealized_pnl, realized_pnl
            FROM positions 
            WHERE is_active = 1
        ''')
        
        positions = []
        for row in cursor.fetchall():
            position = Position(
                symbol=row[0],
                position_type=PositionType(row[1]),
                quantity=Decimal(str(row[2])),
                entry_price=Decimal(str(row[3])),
                current_price=Decimal(str(row[4])),
                entry_time=datetime.fromisoformat(row[5]),
                stop_loss=Decimal(str(row[6])) if row[6] else None,
                take_profit=Decimal(str(row[7])) if row[7] else None,
                fees_paid=Decimal(str(row[8])),
                unrealized_pnl=Decimal(str(row[9])),
                realized_pnl=Decimal(str(row[10]))
            )
            positions.append(position)
        
        conn.close()
        return positions
    
    def get_trades_history(self, limit: int = 100) -> List[Trade]:
        """Récupère l'historique des trades"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, symbol, side, quantity, price, timestamp, fees, status,
                   portfolio_value_before, portfolio_value_after, pnl, strategy_used, confidence_score
            FROM trades 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        trades = []
        for row in cursor.fetchall():
            trade = Trade(
                id=row[0],
                symbol=row[1],
                side=row[2],
                quantity=Decimal(str(row[3])),
                price=Decimal(str(row[4])),
                timestamp=datetime.fromisoformat(row[5]),
                fees=Decimal(str(row[6])),
                status=TradeStatus(row[7]),
                portfolio_value_before=Decimal(str(row[8])),
                portfolio_value_after=Decimal(str(row[9])),
                pnl=Decimal(str(row[10])),
                strategy_used=row[11] or "",
                confidence_score=row[12] or 0.0
            )
            trades.append(trade)
        
        conn.close()
        return trades

class SmartPortfolioManager:
    """Gestionnaire de portfolio intelligent pour capital minimal"""
    
    def __init__(self, 
                 initial_capital: Decimal = Decimal('1.0'),
                 db_path: str = "smart_portfolio.db"):
        
        self.initial_capital = initial_capital
        self.available_cash = initial_capital
        self.positions: Dict[str, Position] = {}
        self.risk_calculator = RiskCalculator()
        self.database = PortfolioDatabase(db_path)
        
        # Charger les positions existantes
        self._load_existing_positions()
        
        # Métriques de performance
        self.total_fees_paid = Decimal('0')
        self.daily_pnl_start = self.get_total_portfolio_value()
        self.daily_pnl_timestamp = datetime.now().date()
        
        # Historique pour calculs de risque
        self.value_history = []
        self.max_value = initial_capital
        
        logger.info(f"Portfolio initialisé avec {initial_capital}€")
    
    def _load_existing_positions(self):
        """Charge les positions existantes depuis la base de données"""
        try:
            positions = self.database.load_active_positions()
            for position in positions:
                self.positions[position.symbol] = position
            
            # Recalculer le cash disponible
            invested_amount = sum(
                pos.quantity * pos.entry_price for pos in self.positions.values()
            )
            self.available_cash = self.initial_capital - invested_amount
            
            logger.info(f"Chargé {len(positions)} positions existantes")
        
        except Exception as e:
            logger.error(f"Erreur chargement positions: {e}")
    
    async def create_position(self,
                            symbol: str,
                            position_type: PositionType,
                            entry_price: Decimal,
                            confidence_score: float,
                            volatility: float,
                            strategy_name: str = "") -> Tuple[bool, str, Optional[Position]]:
        """Crée une nouvelle position"""
        
        try:
            # Calculer la taille de position optimale
            position_size = self.risk_calculator.calculate_position_size(
                self.available_cash, entry_price, confidence_score, volatility
            )
            
            if position_size <= 0:
                return False, "Taille de position calculée nulle", None
            
            # Calculer le montant du trade
            trade_amount = position_size * entry_price
            
            # Calculer les frais (0.1% par défaut)
            fees = trade_amount * Decimal('0.001')
            total_cost = trade_amount + fees
            
            # Vérifier si on a assez de capital
            if total_cost > self.available_cash:
                # Ajuster la taille pour correspondre au capital disponible
                available_for_trade = self.available_cash * Decimal('0.95')  # Garde 5% de marge
                position_size = available_for_trade / (entry_price * Decimal('1.001'))
                trade_amount = position_size * entry_price
                fees = trade_amount * Decimal('0.001')
                total_cost = trade_amount + fees
            
            # Validation finale
            daily_pnl = self.get_daily_pnl()
            is_valid, error_msg = self.risk_calculator.validate_trade(
                self.available_cash, total_cost, daily_pnl
            )
            
            if not is_valid:
                return False, error_msg, None
            
            # Calculer stop loss et take profit
            stop_loss = self.risk_calculator.calculate_stop_loss(
                entry_price, position_type, volatility
            )
            take_profit = self.risk_calculator.calculate_take_profit(
                entry_price, position_type, confidence_score
            )
            
            # Créer la position
            position = Position(
                symbol=symbol,
                position_type=position_type,
                quantity=position_size,
                entry_price=entry_price,
                current_price=entry_price,
                entry_time=datetime.now(),
                stop_loss=stop_loss,
                take_profit=take_profit,
                fees_paid=fees
            )
            
            # Mettre à jour le portfolio
            self.positions[symbol] = position
            self.available_cash -= total_cost
            self.total_fees_paid += fees
            
            # Sauvegarder en base
            self.database.save_position(position)
            
            # Créer l'enregistrement de trade
            trade = Trade(
                id=f"open_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                symbol=symbol,
                side="buy" if position_type == PositionType.LONG else "sell",
                quantity=position_size,
                price=entry_price,
                timestamp=datetime.now(),
                fees=fees,
                status=TradeStatus.EXECUTED,
                portfolio_value_before=self.get_total_portfolio_value() + total_cost,
                portfolio_value_after=self.get_total_portfolio_value(),
                strategy_used=strategy_name,
                confidence_score=confidence_score
            )
            
            self.database.save_trade(trade)
            
            logger.info(f"Position créée: {symbol} {position_type.value} "
                       f"{position_size} @ {entry_price}€ (frais: {fees}€)")
            
            return True, f"Position ouverte avec succès", position
        
        except Exception as e:
            error_msg = f"Erreur création position: {str(e)}"
            logger.error(error_msg)
            return False, error_msg, None
    
    async def close_position(self,
                           symbol: str,
                           exit_price: Decimal,
                           reason: str = "manual") -> Tuple[bool, str, Decimal]:
        """Ferme une position"""
        
        if symbol not in self.positions:
            return False, "Position introuvable", Decimal('0')
        
        try:
            position = self.positions[symbol]
            
            # Calculer la valeur de sortie
            exit_value = position.quantity * exit_price
            
            # Calculer les frais de sortie
            exit_fees = exit_value * Decimal('0.001')
            net_exit_value = exit_value - exit_fees
            
            # Calculer le PnL réalisé
            if position.position_type == PositionType.LONG:
                realized_pnl = net_exit_value - (position.quantity * position.entry_price)
            else:  # SHORT
                realized_pnl = (position.quantity * position.entry_price) - net_exit_value
            
            # Soustraire tous les frais
            realized_pnl -= (position.fees_paid + exit_fees)
            
            # Mettre à jour le portfolio
            self.available_cash += net_exit_value
            self.total_fees_paid += exit_fees
            
            # Supprimer la position
            del self.positions[symbol]
            
            # Créer l'enregistrement de trade de fermeture
            trade = Trade(
                id=f"close_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                symbol=symbol,
                side="sell" if position.position_type == PositionType.LONG else "buy",
                quantity=position.quantity,
                price=exit_price,
                timestamp=datetime.now(),
                fees=exit_fees,
                status=TradeStatus.EXECUTED,
                portfolio_value_before=self.get_total_portfolio_value() - net_exit_value,
                portfolio_value_after=self.get_total_portfolio_value(),
                pnl=realized_pnl
            )
            
            self.database.save_trade(trade)
            
            logger.info(f"Position fermée: {symbol} PnL: {realized_pnl}€ (raison: {reason})")
            
            return True, f"Position fermée - PnL: {realized_pnl:.4f}€", realized_pnl
        
        except Exception as e:
            error_msg = f"Erreur fermeture position: {str(e)}"
            logger.error(error_msg)
            return False, error_msg, Decimal('0')
    
    async def update_prices(self, price_data: Dict[str, Decimal]):
        """Met à jour les prix de toutes les positions"""
        
        for symbol, position in self.positions.items():
            if symbol in price_data:
                old_price = position.current_price
                new_price = price_data[symbol]
                position.update_current_price(new_price)
                
                # Vérifier les ordres stop loss / take profit
                await self._check_stop_orders(symbol, position, new_price)
        
        # Mettre à jour l'historique de valeur
        current_value = self.get_total_portfolio_value()
        self.value_history.append((datetime.now(), current_value))
        
        # Garder seulement les 1000 dernières valeurs
        if len(self.value_history) > 1000:
            self.value_history = self.value_history[-1000:]
        
        # Mettre à jour la valeur maximale
        if current_value > self.max_value:
            self.max_value = current_value
    
    async def _check_stop_orders(self, symbol: str, position: Position, current_price: Decimal):
        """Vérifie et exécute les ordres stop si nécessaire"""
        
        should_close = False
        close_reason = ""
        
        if position.position_type == PositionType.LONG:
            # Stop loss
            if position.stop_loss and current_price <= position.stop_loss:
                should_close = True
                close_reason = "stop_loss"
            # Take profit
            elif position.take_profit and current_price >= position.take_profit:
                should_close = True
                close_reason = "take_profit"
        
        else:  # SHORT
            # Stop loss
            if position.stop_loss and current_price >= position.stop_loss:
                should_close = True
                close_reason = "stop_loss"
            # Take profit
            elif position.take_profit and current_price <= position.take_profit:
                should_close = True
                close_reason = "take_profit"
        
        if should_close:
            success, message, pnl = await self.close_position(symbol, current_price, close_reason)
            if success:
                logger.info(f"Ordre automatique exécuté: {symbol} {close_reason} PnL: {pnl}€")
    
    def get_total_portfolio_value(self) -> Decimal:
        """Calcule la valeur totale du portfolio"""
        positions_value = sum(pos.market_value for pos in self.positions.values())
        return self.available_cash + positions_value
    
    def get_daily_pnl(self) -> Decimal:
        """Calcule le PnL journalier"""
        current_date = datetime.now().date()
        
        # Réinitialiser si nouveau jour
        if current_date != self.daily_pnl_timestamp:
            self.daily_pnl_start = self.get_total_portfolio_value()
            self.daily_pnl_timestamp = current_date
            return Decimal('0')
        
        return self.get_total_portfolio_value() - self.daily_pnl_start
    
    def get_portfolio_metrics(self) -> PortfolioMetrics:
        """Calcule toutes les métriques du portfolio"""
        
        total_value = self.get_total_portfolio_value()
        invested_amount = sum(
            pos.quantity * pos.entry_price for pos in self.positions.values()
        )
        total_unrealized_pnl = sum(pos.unrealized_pnl for pos in self.positions.values())
        
        # Calculer les métriques de trading
        trades = self.database.get_trades_history(1000)
        winning_trades = [t for t in trades if t.pnl > 0]
        win_rate = len(winning_trades) / len(trades) if trades else 0
        
        # Profit factor
        total_wins = sum(t.pnl for t in winning_trades)
        total_losses = abs(sum(t.pnl for t in trades if t.pnl < 0))
        profit_factor = float(total_wins / total_losses) if total_losses > 0 else float('inf')
        
        # Sharpe ratio (simplifié)
        if len(self.value_history) > 10:
            returns = [
                float((self.value_history[i][1] - self.value_history[i-1][1]) / self.value_history[i-1][1])
                for i in range(1, len(self.value_history))
            ]
            if returns and np.std(returns) > 0:
                sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252)  # Annualisé
            else:
                sharpe_ratio = 0.0
        else:
            sharpe_ratio = 0.0
        
        # Max drawdown
        max_drawdown = 0.0
        if self.max_value > 0:
            current_drawdown = float((self.max_value - total_value) / self.max_value)
            max_drawdown = max(0.0, current_drawdown)
        
        # Score de diversification
        diversification_score = min(1.0, len(self.positions) / 5.0) if self.positions else 0.0
        
        return PortfolioMetrics(
            total_value=total_value,
            available_cash=self.available_cash,
            invested_amount=invested_amount,
            total_pnl=total_value - self.initial_capital,
            total_pnl_percentage=(total_value - self.initial_capital) / self.initial_capital * 100,
            daily_pnl=self.get_daily_pnl(),
            daily_pnl_percentage=self.get_daily_pnl() / self.daily_pnl_start * 100 if self.daily_pnl_start > 0 else Decimal('0'),
            total_fees_paid=self.total_fees_paid,
            number_of_trades=len(trades),
            win_rate=win_rate,
            profit_factor=profit_factor,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            positions_count=len(self.positions),
            diversification_score=diversification_score
        )
    
    def get_position_summary(self) -> Dict[str, Any]:
        """Résumé de toutes les positions"""
        positions_data = {}
        
        for symbol, position in self.positions.items():
            positions_data[symbol] = {
                'type': position.position_type.value,
                'quantity': float(position.quantity),
                'entry_price': float(position.entry_price),
                'current_price': float(position.current_price),
                'market_value': float(position.market_value),
                'unrealized_pnl': float(position.unrealized_pnl),
                'pnl_percentage': float(position.pnl_percentage),
                'stop_loss': float(position.stop_loss) if position.stop_loss else None,
                'take_profit': float(position.take_profit) if position.take_profit else None,
                'entry_time': position.entry_time.isoformat(),
                'fees_paid': float(position.fees_paid)
            }
        
        return positions_data
    
    def can_open_new_position(self, required_amount: Decimal) -> Tuple[bool, str]:
        """Vérifie si on peut ouvrir une nouvelle position"""
        
        # Vérifier le capital disponible
        if required_amount > self.available_cash:
            return False, "Capital insuffisant"
        
        # Vérifier le nombre de positions (max 5 pour diversification)
        if len(self.positions) >= 5:
            return False, "Nombre maximum de positions atteint"
        
        # Vérifier que ce n'est pas trop petit
        if required_amount < self.risk_calculator.min_trade_amount:
            return False, f"Montant trop faible (min: {self.risk_calculator.min_trade_amount}€)"
        
        return True, "Position autorisée"
    
    def get_risk_metrics(self) -> Dict[str, Any]:
        """Calcule les métriques de risque"""
        
        total_value = self.get_total_portfolio_value()
        
        # Exposition par position
        position_exposures = {}
        for symbol, position in self.positions.items():
            exposure = float(position.market_value / total_value * 100) if total_value > 0 else 0
            position_exposures[symbol] = exposure
        
        # Risque maximum par position
        max_position_risk = max(position_exposures.values()) if position_exposures else 0
        
        # Capital restant en pourcentage
        cash_ratio = float(self.available_cash / total_value * 100) if total_value > 0 else 100
        
        return {
            'total_value': float(total_value),
            'available_cash_ratio': cash_ratio,
            'position_exposures': position_exposures,
            'max_position_risk': max_position_risk,
            'positions_count': len(self.positions),
            'daily_pnl': float(self.get_daily_pnl()),
            'max_drawdown': self.get_portfolio_metrics().max_drawdown,
            'can_trade': cash_ratio > 10  # Au moins 10% de cash pour trader
        }

# Instance globale du gestionnaire de portfolio
portfolio_manager = SmartPortfolioManager()

# Fonctions utilitaires
async def create_long_position(symbol: str, entry_price: float, confidence: float, volatility: float, strategy: str = ""):
    """Fonction utilitaire pour créer une position longue"""
    return await portfolio_manager.create_position(
        symbol, PositionType.LONG, Decimal(str(entry_price)), confidence, volatility, strategy
    )

async def create_short_position(symbol: str, entry_price: float, confidence: float, volatility: float, strategy: str = ""):
    """Fonction utilitaire pour créer une position courte"""
    return await portfolio_manager.create_position(
        symbol, PositionType.SHORT, Decimal(str(entry_price)), confidence, volatility, strategy
    )

async def close_position_by_symbol(symbol: str, exit_price: float, reason: str = "manual"):
    """Fonction utilitaire pour fermer une position"""
    return await portfolio_manager.close_position(symbol, Decimal(str(exit_price)), reason)

async def update_portfolio_prices(price_data: Dict[str, float]):
    """Fonction utilitaire pour mettre à jour les prix"""
    decimal_prices = {symbol: Decimal(str(price)) for symbol, price in price_data.items()}
    await portfolio_manager.update_prices(decimal_prices)

def get_portfolio_status():
    """Fonction utilitaire pour obtenir le statut du portfolio"""
    metrics = portfolio_manager.get_portfolio_metrics()
    positions = portfolio_manager.get_position_summary()
    risk_metrics = portfolio_manager.get_risk_metrics()
    
    return {
        'metrics': {
            'total_value': float(metrics.total_value),
            'available_cash': float(metrics.available_cash),
            'total_pnl': float(metrics.total_pnl),
            'total_pnl_percentage': float(metrics.total_pnl_percentage),
            'daily_pnl': float(metrics.daily_pnl),
            'win_rate': metrics.win_rate,
            'profit_factor': metrics.profit_factor,
            'positions_count': metrics.positions_count
        },
        'positions': positions,
        'risk_metrics': risk_metrics
    }
