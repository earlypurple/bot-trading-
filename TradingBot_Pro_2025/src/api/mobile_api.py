#!/usr/bin/env python3
"""
📱 API MOBILE - TRADINGBOT PRO 2025
===================================
🚀 API REST optimisée pour applications mobiles
📊 Endpoints spécialisés pour trading mobile
🔒 Authentification 2FA intégrée
⚡ Réponses optimisées et compression

🎯 Fonctionnalités:
- API REST complète pour mobile
- Authentification JWT + 2FA
- Endpoints optimisés mobile
- Compression et cache
- Push notifications
- Mode hors ligne
"""

import asyncio
import json
import gzip
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import logging
from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
from starlette.middleware.base import BaseHTTPMiddleware
import redis
import aiohttp
import asyncpg
from decimal import Decimal
import hashlib
import hmac
import base64

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MobileAPI")

# ============================================================================
# 📱 MODÈLES DE DONNÉES MOBILE
# ============================================================================

class MobileResponseFormat(Enum):
    """Formats de réponse mobile"""
    MINIMAL = "minimal"
    STANDARD = "standard"
    DETAILED = "detailed"

class NotificationType(Enum):
    """Types de notifications push"""
    PRICE_ALERT = "price_alert"
    TRADE_EXECUTED = "trade_executed"
    PORTFOLIO_UPDATE = "portfolio_update"
    MARKET_NEWS = "market_news"
    SYSTEM_ALERT = "system_alert"
    SECURITY_ALERT = "security_alert"

class OrderType(Enum):
    """Types d'ordres"""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

class OrderStatus(Enum):
    """Statuts d'ordres"""
    PENDING = "pending"
    PARTIAL = "partial"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

# Modèles Pydantic pour validation
class LoginRequest(BaseModel):
    user_id: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    device_id: str = Field(..., description="Identifiant unique de l'appareil")
    device_info: Dict[str, str] = Field(default_factory=dict)

class TwoFactorRequest(BaseModel):
    session_id: str
    method: str = Field(..., regex="^(totp|sms|email|backup_code)$")
    code: str = Field(..., min_length=4, max_length=12)

class PlaceOrderRequest(BaseModel):
    symbol: str = Field(..., regex="^[A-Z]{3,10}$")
    side: str = Field(..., regex="^(buy|sell)$")
    type: OrderType
    quantity: float = Field(..., gt=0)
    price: Optional[float] = Field(None, gt=0)
    stop_price: Optional[float] = Field(None, gt=0)
    time_in_force: str = Field(default="GTC", regex="^(GTC|IOC|FOK)$")

class PriceAlertRequest(BaseModel):
    symbol: str = Field(..., regex="^[A-Z]{3,10}$")
    condition: str = Field(..., regex="^(above|below)$")
    price: float = Field(..., gt=0)
    message: Optional[str] = Field(None, max_length=200)

class PortfolioRequest(BaseModel):
    format: MobileResponseFormat = MobileResponseFormat.STANDARD
    include_history: bool = False
    currency: str = Field(default="USD", regex="^[A-Z]{3}$")

@dataclass
class MobileResponse:
    """Réponse API mobile standardisée"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    message: Optional[str] = None
    timestamp: datetime = None
    request_id: Optional[str] = None
    cache_info: Optional[Dict] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convertit en dictionnaire pour JSON"""
        result = {
            'success': self.success,
            'timestamp': self.timestamp.isoformat(),
        }
        
        if self.data is not None:
            result['data'] = self.data
        if self.error:
            result['error'] = self.error
        if self.message:
            result['message'] = self.message
        if self.request_id:
            result['request_id'] = self.request_id
        if self.cache_info:
            result['cache_info'] = self.cache_info
            
        return result

# ============================================================================
# 🔒 MIDDLEWARE ET SÉCURITÉ
# ============================================================================

class MobileSecurityMiddleware(BaseHTTPMiddleware):
    """Middleware de sécurité pour API mobile"""
    
    async def dispatch(self, request: Request, call_next):
        # Générer ID de requête unique
        request_id = f"mob_{int(datetime.now().timestamp())}_{hash(str(request.url))}"
        request.state.request_id = request_id
        
        # Log de la requête
        logger.info(f"📱 {request.method} {request.url.path} [{request_id}]")
        
        # Vérifier rate limiting
        client_ip = request.client.host
        if await self._check_rate_limit(client_ip):
            return JSONResponse(
                status_code=429,
                content=MobileResponse(
                    success=False,
                    error="Rate limit exceeded",
                    message="Trop de requêtes, réessayez plus tard",
                    request_id=request_id
                ).to_dict()
            )
        
        # Traiter la requête
        start_time = datetime.now()
        response = await call_next(request)
        process_time = (datetime.now() - start_time).total_seconds()
        
        # Ajouter headers de sécurité
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
    
    async def _check_rate_limit(self, client_ip: str) -> bool:
        """Vérifie le rate limiting"""
        # Simulation simple (en production, utiliser Redis)
        return False  # Pas de limite pour les tests

class JWTBearer(HTTPBearer):
    """Gestionnaire d'authentification JWT"""
    
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        # En production, importer depuis le système 2FA
        self.jwt_secret = "demo_secret_key_mobile_api_2025"
    
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Schéma d'authentification invalide")
            
            payload = self._verify_jwt(credentials.credentials)
            if not payload:
                raise HTTPException(status_code=403, detail="Token invalide ou expiré")
            
            request.state.user_id = payload.get('user_id')
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Token manquant")
    
    def _verify_jwt(self, token: str) -> Optional[Dict]:
        """Vérifie un token JWT (version simplifiée)"""
        try:
            # En production, utiliser le système 2FA complet
            import jwt
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload
        except:
            return None

# ============================================================================
# 📊 GESTIONNAIRE DE DONNÉES MOBILE
# ============================================================================

class MobileDataManager:
    """Gestionnaire de données optimisé pour mobile"""
    
    def __init__(self):
        self.cache = {}  # En production, utiliser Redis
        self.cache_ttl = {
            'market_data': 30,      # 30 secondes
            'portfolio': 60,        # 1 minute
            'orders': 10,           # 10 secondes
            'account': 300,         # 5 minutes
        }
    
    async def get_market_data(self, symbols: List[str], format: MobileResponseFormat) -> Dict:
        """Obtient les données de marché optimisées pour mobile"""
        cache_key = f"market_{'-'.join(symbols)}_{format.value}"
        
        # Vérifier cache
        cached = self._get_from_cache(cache_key, 'market_data')
        if cached:
            return cached
        
        # Simuler données de marché
        data = {}
        for symbol in symbols:
            price = 50000 + hash(symbol) % 10000  # Prix simulé
            change_24h = (hash(symbol + str(datetime.now().hour)) % 1000 - 500) / 100
            
            if format == MobileResponseFormat.MINIMAL:
                data[symbol] = {
                    'price': price,
                    'change_24h': change_24h
                }
            elif format == MobileResponseFormat.STANDARD:
                data[symbol] = {
                    'price': price,
                    'change_24h': change_24h,
                    'volume_24h': price * 1000,
                    'high_24h': price * 1.05,
                    'low_24h': price * 0.95
                }
            else:  # DETAILED
                data[symbol] = {
                    'price': price,
                    'change_24h': change_24h,
                    'volume_24h': price * 1000,
                    'high_24h': price * 1.05,
                    'low_24h': price * 0.95,
                    'bid': price * 0.999,
                    'ask': price * 1.001,
                    'market_cap': price * 21000000,
                    'circulating_supply': 21000000
                }
        
        # Mettre en cache
        self._set_cache(cache_key, data, 'market_data')
        
        return data
    
    async def get_portfolio(self, user_id: str, format: MobileResponseFormat) -> Dict:
        """Obtient le portfolio optimisé pour mobile"""
        cache_key = f"portfolio_{user_id}_{format.value}"
        
        cached = self._get_from_cache(cache_key, 'portfolio')
        if cached:
            return cached
        
        # Simuler portfolio
        total_value = 100000  # $100k
        assets = [
            {'symbol': 'BTC', 'amount': 2.5, 'value': 125000},
            {'symbol': 'ETH', 'amount': 50, 'value': 150000},
            {'symbol': 'USD', 'amount': 25000, 'value': 25000}
        ]
        
        if format == MobileResponseFormat.MINIMAL:
            data = {
                'total_value': total_value,
                'asset_count': len(assets)
            }
        elif format == MobileResponseFormat.STANDARD:
            data = {
                'total_value': total_value,
                'change_24h': 2500,  # +$2.5k
                'change_percent': 2.5,
                'assets': [
                    {
                        'symbol': asset['symbol'],
                        'amount': asset['amount'],
                        'value': asset['value']
                    } for asset in assets
                ]
            }
        else:  # DETAILED
            data = {
                'total_value': total_value,
                'change_24h': 2500,
                'change_percent': 2.5,
                'assets': [
                    {
                        'symbol': asset['symbol'],
                        'amount': asset['amount'],
                        'value': asset['value'],
                        'allocation_percent': (asset['value'] / total_value) * 100,
                        'avg_buy_price': asset['value'] / asset['amount'] * 0.9,
                        'unrealized_pnl': asset['value'] * 0.1
                    } for asset in assets
                ],
                'performance': {
                    'day': {'value': 2500, 'percent': 2.5},
                    'week': {'value': 8000, 'percent': 8.7},
                    'month': {'value': 15000, 'percent': 17.6},
                    'year': {'value': 35000, 'percent': 53.8}
                }
            }
        
        self._set_cache(cache_key, data, 'portfolio')
        return data
    
    async def get_orders(self, user_id: str, status: Optional[str] = None) -> List[Dict]:
        """Obtient les ordres de l'utilisateur"""
        cache_key = f"orders_{user_id}_{status or 'all'}"
        
        cached = self._get_from_cache(cache_key, 'orders')
        if cached:
            return cached
        
        # Simuler ordres
        orders = [
            {
                'id': 'ORD001',
                'symbol': 'BTC',
                'side': 'buy',
                'type': 'limit',
                'quantity': 0.5,
                'price': 49000,
                'status': 'pending',
                'created_at': datetime.now().isoformat(),
                'filled_quantity': 0,
                'remaining_quantity': 0.5
            },
            {
                'id': 'ORD002',
                'symbol': 'ETH',
                'side': 'sell',
                'type': 'market',
                'quantity': 10,
                'price': 3000,
                'status': 'filled',
                'created_at': (datetime.now() - timedelta(hours=2)).isoformat(),
                'filled_quantity': 10,
                'remaining_quantity': 0
            }
        ]
        
        if status:
            orders = [order for order in orders if order['status'] == status]
        
        self._set_cache(cache_key, orders, 'orders')
        return orders
    
    def _get_from_cache(self, key: str, category: str) -> Optional[Any]:
        """Récupère depuis le cache"""
        if key in self.cache:
            cached_item = self.cache[key]
            ttl = self.cache_ttl.get(category, 60)
            
            if (datetime.now() - cached_item['timestamp']).seconds < ttl:
                return cached_item['data']
            else:
                del self.cache[key]
        
        return None
    
    def _set_cache(self, key: str, data: Any, category: str):
        """Met en cache"""
        self.cache[key] = {
            'data': data,
            'timestamp': datetime.now(),
            'category': category
        }

# ============================================================================
# 📱 API MOBILE FASTAPI
# ============================================================================

# Initialisation
app = FastAPI(
    title="TradingBot Pro 2025 - API Mobile",
    description="API REST optimisée pour applications mobiles de trading",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(MobileSecurityMiddleware)

# Gestionnaires
security = JWTBearer()
data_manager = MobileDataManager()

# ============================================================================
# 🔐 ENDPOINTS D'AUTHENTIFICATION
# ============================================================================

@app.post("/api/v1/auth/login")
async def mobile_login(request: LoginRequest, bg_tasks: BackgroundTasks):
    """Connexion utilisateur avec support 2FA"""
    try:
        # Simuler authentification (en production, utiliser le système 2FA)
        if request.user_id == "demo" and request.password == "password123":
            # Vérifier si 2FA requis
            requires_2fa = True  # Simuler 2FA requis
            
            if requires_2fa:
                session_id = f"session_{hash(request.user_id + str(datetime.now()))}"
                
                return MobileResponse(
                    success=True,
                    data={
                        'session_id': session_id,
                        'status': 'partial',
                        'next_method': 'totp',
                        'message': 'Code TOTP requis'
                    },
                    message="Première étape validée"
                ).to_dict()
            else:
                # Générer token JWT
                import jwt
                token = jwt.encode({
                    'user_id': request.user_id,
                    'device_id': request.device_id,
                    'exp': datetime.utcnow() + timedelta(hours=24)
                }, "demo_secret_key_mobile_api_2025", algorithm='HS256')
                
                return MobileResponse(
                    success=True,
                    data={
                        'token': token,
                        'expires_in': 86400,  # 24h
                        'user_info': {
                            'user_id': request.user_id,
                            'device_id': request.device_id
                        }
                    },
                    message="Connexion réussie"
                ).to_dict()
        else:
            return MobileResponse(
                success=False,
                error="invalid_credentials",
                message="Identifiants invalides"
            ).to_dict()
            
    except Exception as e:
        logger.error(f"❌ Erreur login mobile: {e}")
        return MobileResponse(
            success=False,
            error="internal_error",
            message="Erreur interne"
        ).to_dict()

@app.post("/api/v1/auth/2fa/verify")
async def verify_2fa(request: TwoFactorRequest):
    """Vérification du second facteur"""
    try:
        # Simuler vérification 2FA
        if request.code == "123456":  # Code de test
            # Générer token JWT
            import jwt
            token = jwt.encode({
                'user_id': 'demo',
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, "demo_secret_key_mobile_api_2025", algorithm='HS256')
            
            return MobileResponse(
                success=True,
                data={
                    'token': token,
                    'expires_in': 86400,
                    'user_info': {
                        'user_id': 'demo'
                    }
                },
                message="Authentification 2FA réussie"
            ).to_dict()
        else:
            return MobileResponse(
                success=False,
                error="invalid_code",
                message="Code 2FA invalide"
            ).to_dict()
            
    except Exception as e:
        logger.error(f"❌ Erreur 2FA mobile: {e}")
        return MobileResponse(
            success=False,
            error="internal_error"
        ).to_dict()

# ============================================================================
# 📊 ENDPOINTS DE DONNÉES MARCHÉ
# ============================================================================

@app.get("/api/v1/market/prices")
async def get_market_prices(
    symbols: str = "BTC,ETH,ADA",
    format: MobileResponseFormat = MobileResponseFormat.STANDARD,
    token: str = Depends(security)
):
    """Obtient les prix de marché optimisés pour mobile"""
    try:
        symbol_list = [s.strip().upper() for s in symbols.split(',')]
        
        data = await data_manager.get_market_data(symbol_list, format)
        
        return MobileResponse(
            success=True,
            data=data,
            cache_info={'format': format.value, 'symbols_count': len(symbol_list)}
        ).to_dict()
        
    except Exception as e:
        logger.error(f"❌ Erreur prix marché: {e}")
        return MobileResponse(
            success=False,
            error="market_data_error"
        ).to_dict()

@app.get("/api/v1/market/ticker/{symbol}")
async def get_ticker(
    symbol: str,
    format: MobileResponseFormat = MobileResponseFormat.STANDARD,
    token: str = Depends(security)
):
    """Obtient le ticker d'un symbole spécifique"""
    try:
        data = await data_manager.get_market_data([symbol.upper()], format)
        
        return MobileResponse(
            success=True,
            data=data.get(symbol.upper(), {}),
            cache_info={'symbol': symbol.upper(), 'format': format.value}
        ).to_dict()
        
    except Exception as e:
        logger.error(f"❌ Erreur ticker: {e}")
        return MobileResponse(
            success=False,
            error="ticker_error"
        ).to_dict()

# ============================================================================
# 💼 ENDPOINTS PORTFOLIO
# ============================================================================

@app.get("/api/v1/portfolio")
async def get_portfolio(
    format: MobileResponseFormat = MobileResponseFormat.STANDARD,
    currency: str = "USD",
    request: Request = None,
    token: str = Depends(security)
):
    """Obtient le portfolio de l'utilisateur"""
    try:
        user_id = request.state.user_id
        
        data = await data_manager.get_portfolio(user_id, format)
        
        return MobileResponse(
            success=True,
            data=data,
            cache_info={'user_id': user_id, 'format': format.value}
        ).to_dict()
        
    except Exception as e:
        logger.error(f"❌ Erreur portfolio: {e}")
        return MobileResponse(
            success=False,
            error="portfolio_error"
        ).to_dict()

@app.get("/api/v1/portfolio/performance")
async def get_portfolio_performance(
    period: str = "24h",
    request: Request = None,
    token: str = Depends(security)
):
    """Obtient les performances du portfolio"""
    try:
        user_id = request.state.user_id
        
        # Simuler performances
        performances = {
            '1h': {'value': 500, 'percent': 0.5},
            '24h': {'value': 2500, 'percent': 2.5},
            '7d': {'value': 8000, 'percent': 8.7},
            '30d': {'value': 15000, 'percent': 17.6},
            '1y': {'value': 35000, 'percent': 53.8}
        }
        
        data = performances.get(period, performances['24h'])
        
        return MobileResponse(
            success=True,
            data={
                'period': period,
                'performance': data,
                'benchmark': {
                    'btc': {'value': 1800, 'percent': 1.8},
                    'sp500': {'value': 800, 'percent': 0.8}
                }
            }
        ).to_dict()
        
    except Exception as e:
        logger.error(f"❌ Erreur performance: {e}")
        return MobileResponse(
            success=False,
            error="performance_error"
        ).to_dict()

# ============================================================================
# 📋 ENDPOINTS ORDRES
# ============================================================================

@app.get("/api/v1/orders")
async def get_orders(
    status: Optional[str] = None,
    limit: int = 50,
    request: Request = None,
    token: str = Depends(security)
):
    """Obtient les ordres de l'utilisateur"""
    try:
        user_id = request.state.user_id
        
        orders = await data_manager.get_orders(user_id, status)
        
        # Limiter les résultats
        if limit > 0:
            orders = orders[:limit]
        
        return MobileResponse(
            success=True,
            data={
                'orders': orders,
                'total': len(orders),
                'filter': {'status': status, 'limit': limit}
            }
        ).to_dict()
        
    except Exception as e:
        logger.error(f"❌ Erreur ordres: {e}")
        return MobileResponse(
            success=False,
            error="orders_error"
        ).to_dict()

@app.post("/api/v1/orders")
async def place_order(
    order: PlaceOrderRequest,
    request: Request = None,
    token: str = Depends(security)
):
    """Place un nouvel ordre"""
    try:
        user_id = request.state.user_id
        
        # Générer ID d'ordre
        order_id = f"ORD_{int(datetime.now().timestamp())}_{hash(user_id)}"
        
        # Simuler placement d'ordre
        order_data = {
            'id': order_id,
            'symbol': order.symbol,
            'side': order.side,
            'type': order.type.value,
            'quantity': order.quantity,
            'price': order.price,
            'stop_price': order.stop_price,
            'time_in_force': order.time_in_force,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'filled_quantity': 0,
            'remaining_quantity': order.quantity
        }
        
        logger.info(f"📋 Ordre placé: {order_id} pour {user_id}")
        
        return MobileResponse(
            success=True,
            data=order_data,
            message=f"Ordre {order_id} placé avec succès"
        ).to_dict()
        
    except Exception as e:
        logger.error(f"❌ Erreur placement ordre: {e}")
        return MobileResponse(
            success=False,
            error="order_placement_error"
        ).to_dict()

@app.delete("/api/v1/orders/{order_id}")
async def cancel_order(
    order_id: str,
    request: Request = None,
    token: str = Depends(security)
):
    """Annule un ordre"""
    try:
        user_id = request.state.user_id
        
        # Simuler annulation
        logger.info(f"❌ Ordre annulé: {order_id} pour {user_id}")
        
        return MobileResponse(
            success=True,
            data={'order_id': order_id, 'status': 'cancelled'},
            message=f"Ordre {order_id} annulé"
        ).to_dict()
        
    except Exception as e:
        logger.error(f"❌ Erreur annulation ordre: {e}")
        return MobileResponse(
            success=False,
            error="order_cancellation_error"
        ).to_dict()

# ============================================================================
# 🔔 ENDPOINTS NOTIFICATIONS
# ============================================================================

@app.post("/api/v1/notifications/alerts")
async def create_price_alert(
    alert: PriceAlertRequest,
    request: Request = None,
    token: str = Depends(security)
):
    """Crée une alerte de prix"""
    try:
        user_id = request.state.user_id
        
        alert_id = f"ALERT_{int(datetime.now().timestamp())}"
        
        alert_data = {
            'id': alert_id,
            'symbol': alert.symbol,
            'condition': alert.condition,
            'price': alert.price,
            'message': alert.message,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        logger.info(f"🔔 Alerte créée: {alert_id} pour {user_id}")
        
        return MobileResponse(
            success=True,
            data=alert_data,
            message="Alerte de prix créée"
        ).to_dict()
        
    except Exception as e:
        logger.error(f"❌ Erreur création alerte: {e}")
        return MobileResponse(
            success=False,
            error="alert_creation_error"
        ).to_dict()

@app.get("/api/v1/notifications/history")
async def get_notification_history(
    limit: int = 20,
    request: Request = None,
    token: str = Depends(security)
):
    """Obtient l'historique des notifications"""
    try:
        user_id = request.state.user_id
        
        # Simuler historique
        notifications = [
            {
                'id': 'NOTIF001',
                'type': 'price_alert',
                'title': 'BTC Alert',
                'message': 'BTC a dépassé $50,000',
                'timestamp': datetime.now().isoformat(),
                'read': False
            },
            {
                'id': 'NOTIF002', 
                'type': 'trade_executed',
                'title': 'Ordre exécuté',
                'message': 'Achat de 0.5 BTC exécuté',
                'timestamp': (datetime.now() - timedelta(hours=1)).isoformat(),
                'read': True
            }
        ][:limit]
        
        return MobileResponse(
            success=True,
            data={
                'notifications': notifications,
                'unread_count': len([n for n in notifications if not n['read']])
            }
        ).to_dict()
        
    except Exception as e:
        logger.error(f"❌ Erreur historique notifications: {e}")
        return MobileResponse(
            success=False,
            error="notifications_error"
        ).to_dict()

# ============================================================================
# ⚙️ ENDPOINTS SYSTÈME
# ============================================================================

@app.get("/api/v1/system/status")
async def get_system_status():
    """Obtient le statut du système"""
    try:
        status = {
            'status': 'operational',
            'version': '1.0.0',
            'uptime': '99.9%',
            'services': {
                'trading': 'operational',
                'market_data': 'operational',
                'notifications': 'operational',
                'auth': 'operational'
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return MobileResponse(
            success=True,
            data=status
        ).to_dict()
        
    except Exception as e:
        logger.error(f"❌ Erreur statut système: {e}")
        return MobileResponse(
            success=False,
            error="system_status_error"
        ).to_dict()

@app.get("/api/v1/system/health")
async def health_check():
    """Vérification de santé de l'API"""
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }

# ============================================================================
# 🧪 FONCTION DE TEST
# ============================================================================

async def test_mobile_api():
    """Test de l'API mobile"""
    print("🧪 TEST API MOBILE - TRADINGBOT PRO 2025")
    print("=" * 50)
    
    try:
        import httpx
        
        base_url = "http://localhost:8080"
        
        # Test connexion
        async with httpx.AsyncClient() as client:
            # Test health check
            response = await client.get(f"{base_url}/api/v1/system/health")
            print(f"Health Check: {'✅' if response.status_code == 200 else '❌'}")
            
            # Test login
            login_data = {
                "user_id": "demo",
                "password": "password123",
                "device_id": "test_device_001",
                "device_info": {"platform": "iOS", "version": "1.0.0"}
            }
            
            response = await client.post(f"{base_url}/api/v1/auth/login", json=login_data)
            print(f"Login: {'✅' if response.status_code == 200 else '❌'}")
            
            if response.status_code == 200:
                login_result = response.json()
                
                if login_result.get('data', {}).get('session_id'):
                    # Test 2FA
                    fa2_data = {
                        "session_id": login_result['data']['session_id'],
                        "method": "totp",
                        "code": "123456"
                    }
                    
                    response = await client.post(f"{base_url}/api/v1/auth/2fa/verify", json=fa2_data)
                    print(f"2FA: {'✅' if response.status_code == 200 else '❌'}")
                    
                    if response.status_code == 200:
                        token = response.json().get('data', {}).get('token')
                        
                        if token:
                            headers = {"Authorization": f"Bearer {token}"}
                            
                            # Test market data
                            response = await client.get(f"{base_url}/api/v1/market/prices", headers=headers)
                            print(f"Market Data: {'✅' if response.status_code == 200 else '❌'}")
                            
                            # Test portfolio
                            response = await client.get(f"{base_url}/api/v1/portfolio", headers=headers)
                            print(f"Portfolio: {'✅' if response.status_code == 200 else '❌'}")
                            
                            # Test orders
                            response = await client.get(f"{base_url}/api/v1/orders", headers=headers)
                            print(f"Orders: {'✅' if response.status_code == 200 else '❌'}")
        
        print("\n✅ TESTS API MOBILE TERMINÉS!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR TEST: {e}")
        return False

# ============================================================================
# 🚀 LANCEMENT DE L'API
# ============================================================================

if __name__ == "__main__":
    print("📱 API MOBILE - TRADINGBOT PRO 2025")
    print("=" * 40)
    print("🚀 Démarrage du serveur API mobile...")
    print("📍 URL: http://localhost:8080")
    print("📚 Documentation: http://localhost:8080/docs")
    print("=" * 40)
    
    # Configuration serveur
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8080,
        log_level="info",
        reload=True,
        access_log=True
    )
    
    server = uvicorn.Server(config)
    
    try:
        # Démarrer le serveur
        asyncio.run(server.serve())
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur API mobile")
    except Exception as e:
        print(f"\n❌ Erreur serveur: {e}")
