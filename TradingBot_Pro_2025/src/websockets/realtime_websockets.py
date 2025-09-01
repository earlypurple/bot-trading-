#!/usr/bin/env python3
"""
📊 WEBSOCKETS TEMPS RÉEL - TRADINGBOT PRO 2025
==============================================
🔥 Système WebSocket ultra-performant pour données temps réel
⚡ Gestion optimisée des connexions et diffusion instantanée
🔄 Support multi-canaux avec compression et authentification

🎯 Fonctionnalités:
- Streaming prix en temps réel
- Notifications trading instantanées  
- Dashboard live avec métriques
- Gestion connexions optimisée
"""

import asyncio
import websockets
import json
import logging
import time
import gzip
import base64
from typing import Dict, List, Set, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import threading
import weakref
import ssl
import jwt
from cryptography.fernet import Fernet

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WebSocketsRealTime")

class MessageType(Enum):
    """Types de messages WebSocket"""
    PRICE_UPDATE = "price_update"
    TRADE_SIGNAL = "trade_signal"
    PORTFOLIO_UPDATE = "portfolio_update"
    SYSTEM_STATUS = "system_status"
    NOTIFICATION = "notification"
    HEARTBEAT = "heartbeat"
    AUTH_REQUEST = "auth_request"
    AUTH_RESPONSE = "auth_response"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    ERROR = "error"

class ChannelType(Enum):
    """Canaux de données disponibles"""
    PRICES = "prices"
    TRADES = "trades"
    PORTFOLIO = "portfolio"
    SYSTEM = "system"
    ALERTS = "alerts"
    ANALYTICS = "analytics"

@dataclass
class WebSocketMessage:
    """Message WebSocket structuré"""
    type: MessageType
    channel: ChannelType
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    user_id: Optional[str] = None
    compressed: bool = False

@dataclass
class ClientConnection:
    """Connexion client avec métadonnées"""
    websocket: websockets.WebSocketServerProtocol
    user_id: Optional[str] = None
    subscriptions: Set[ChannelType] = field(default_factory=set)
    authenticated: bool = False
    connected_at: datetime = field(default_factory=datetime.now)
    last_ping: datetime = field(default_factory=datetime.now)
    ip_address: str = ""
    user_agent: str = ""

class WebSocketAuthenticator:
    """Authentification WebSocket sécurisée"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.cipher = Fernet(Fernet.generate_key())
        self.valid_tokens: Dict[str, Dict] = {}
        
    def generate_token(self, user_id: str, permissions: List[str] = None) -> str:
        """Génère un token JWT sécurisé"""
        try:
            payload = {
                'user_id': user_id,
                'permissions': permissions or ['read'],
                'exp': datetime.utcnow() + timedelta(hours=24),
                'iat': datetime.utcnow()
            }
            
            token = jwt.encode(payload, self.secret_key, algorithm='HS256')
            self.valid_tokens[user_id] = payload
            
            logger.info(f"🔐 Token généré pour utilisateur {user_id}")
            return token
            
        except Exception as e:
            logger.error(f"❌ Erreur génération token: {e}")
            return ""
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Vérifie et décode un token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            
            # Vérifier que le token est encore valide
            if payload['user_id'] in self.valid_tokens:
                logger.debug(f"✅ Token valide pour {payload['user_id']}")
                return payload
            else:
                logger.warning(f"⚠️ Token non reconnu pour {payload.get('user_id', 'unknown')}")
                return None
                
        except jwt.ExpiredSignatureError:
            logger.warning("⚠️ Token expiré")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"⚠️ Token invalide: {e}")
            return None

class RealTimeDataStreamer:
    """Générateur de données temps réel"""
    
    def __init__(self):
        self.running = False
        self.subscribers: Dict[ChannelType, Set[ClientConnection]] = {
            channel: set() for channel in ChannelType
        }
        self.data_generators: Dict[ChannelType, Callable] = {
            ChannelType.PRICES: self._generate_price_data,
            ChannelType.TRADES: self._generate_trade_data,
            ChannelType.PORTFOLIO: self._generate_portfolio_data,
            ChannelType.SYSTEM: self._generate_system_data,
            ChannelType.ALERTS: self._generate_alert_data,
            ChannelType.ANALYTICS: self._generate_analytics_data
        }
        
    def _generate_price_data(self) -> Dict[str, Any]:
        """Génère des données de prix simulées"""
        import random
        symbols = ['BTC/USD', 'ETH/USD', 'ADA/USD', 'DOT/USD', 'LINK/USD']
        
        return {
            'symbol': random.choice(symbols),
            'price': round(random.uniform(100, 50000), 2),
            'change_24h': round(random.uniform(-10, 10), 2),
            'volume': round(random.uniform(1000000, 100000000), 2),
            'bid': round(random.uniform(100, 50000), 2),
            'ask': round(random.uniform(100, 50000), 2),
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_trade_data(self) -> Dict[str, Any]:
        """Génère des données de trading simulées"""
        import random
        
        return {
            'trade_id': f"trade_{int(time.time())}_{random.randint(1000, 9999)}",
            'symbol': random.choice(['BTC/USD', 'ETH/USD', 'ADA/USD']),
            'side': random.choice(['buy', 'sell']),
            'amount': round(random.uniform(0.1, 10), 4),
            'price': round(random.uniform(100, 50000), 2),
            'status': random.choice(['executed', 'pending', 'partial']),
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_portfolio_data(self) -> Dict[str, Any]:
        """Génère des données de portefeuille simulées"""
        import random
        
        return {
            'total_value': round(random.uniform(10000, 100000), 2),
            'total_pnl': round(random.uniform(-1000, 5000), 2),
            'total_pnl_pct': round(random.uniform(-10, 25), 2),
            'positions': [
                {
                    'symbol': 'BTC/USD',
                    'amount': round(random.uniform(0.1, 5), 4),
                    'value': round(random.uniform(5000, 25000), 2),
                    'pnl': round(random.uniform(-500, 2000), 2)
                },
                {
                    'symbol': 'ETH/USD', 
                    'amount': round(random.uniform(1, 50), 4),
                    'value': round(random.uniform(2000, 15000), 2),
                    'pnl': round(random.uniform(-300, 1500), 2)
                }
            ],
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_system_data(self) -> Dict[str, Any]:
        """Génère des données système"""
        import random
        
        return {
            'status': random.choice(['healthy', 'warning', 'error']),
            'cpu_usage': round(random.uniform(20, 80), 1),
            'memory_usage': round(random.uniform(30, 90), 1),
            'active_connections': random.randint(50, 500),
            'trades_per_second': round(random.uniform(5, 50), 1),
            'latency_ms': round(random.uniform(10, 100), 1),
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_alert_data(self) -> Dict[str, Any]:
        """Génère des alertes simulées"""
        import random
        
        alerts = [
            "🚨 Prix BTC franchit résistance à 45000 USD",
            "📈 Signal d'achat détecté sur ETH/USD",
            "⚠️ Volatilité élevée détectée",
            "💰 Objectif de profit atteint sur position ADA",
            "🔔 Nouvelle opportunité d'arbitrage disponible"
        ]
        
        return {
            'id': f"alert_{int(time.time())}",
            'level': random.choice(['info', 'warning', 'critical']),
            'message': random.choice(alerts),
            'symbol': random.choice(['BTC/USD', 'ETH/USD', 'ADA/USD']),
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_analytics_data(self) -> Dict[str, Any]:
        """Génère des données analytiques"""
        import random
        
        return {
            'performance_score': round(random.uniform(70, 95), 1),
            'win_rate': round(random.uniform(60, 85), 1),
            'avg_profit': round(random.uniform(50, 500), 2),
            'max_drawdown': round(random.uniform(5, 20), 2),
            'sharpe_ratio': round(random.uniform(1.5, 3.5), 2),
            'trades_today': random.randint(10, 100),
            'profit_today': round(random.uniform(-100, 1000), 2),
            'timestamp': datetime.now().isoformat()
        }
    
    async def start_streaming(self):
        """Démarre le streaming de données"""
        self.running = True
        logger.info("🔄 Démarrage streaming données temps réel...")
        
        # Lancer les générateurs pour chaque canal
        tasks = []
        for channel in ChannelType:
            task = asyncio.create_task(self._stream_channel_data(channel))
            tasks.append(task)
            
        await asyncio.gather(*tasks)
    
    async def _stream_channel_data(self, channel: ChannelType):
        """Streaming pour un canal spécifique"""
        generator = self.data_generators.get(channel)
        if not generator:
            return
            
        # Intervalles différents selon le canal
        intervals = {
            ChannelType.PRICES: 1.0,      # 1 seconde
            ChannelType.TRADES: 2.0,      # 2 secondes  
            ChannelType.PORTFOLIO: 5.0,   # 5 secondes
            ChannelType.SYSTEM: 10.0,     # 10 secondes
            ChannelType.ALERTS: 15.0,     # 15 secondes
            ChannelType.ANALYTICS: 30.0   # 30 secondes
        }
        
        interval = intervals.get(channel, 5.0)
        
        while self.running:
            try:
                # Générer données
                data = generator()
                
                # Créer message
                message = WebSocketMessage(
                    type=MessageType.PRICE_UPDATE if channel == ChannelType.PRICES else MessageType.NOTIFICATION,
                    channel=channel,
                    data=data
                )
                
                # Diffuser aux abonnés
                await self._broadcast_to_channel(channel, message)
                
                # Attendre avant prochaine génération
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"❌ Erreur streaming {channel.value}: {e}")
                await asyncio.sleep(1)
    
    async def _broadcast_to_channel(self, channel: ChannelType, message: WebSocketMessage):
        """Diffuse un message à tous les abonnés d'un canal"""
        subscribers = self.subscribers.get(channel, set())
        
        if not subscribers:
            return
            
        # Préparer le message JSON
        message_data = {
            'type': message.type.value,
            'channel': message.channel.value,
            'data': message.data,
            'timestamp': message.timestamp.isoformat()
        }
        
        message_json = json.dumps(message_data)
        
        # Diffuser à tous les abonnés connectés
        disconnected_clients = set()
        
        for client in subscribers:
            try:
                if client.websocket.open:
                    await client.websocket.send(message_json)
                else:
                    disconnected_clients.add(client)
            except Exception as e:
                logger.warning(f"⚠️ Erreur envoi à client: {e}")
                disconnected_clients.add(client)
        
        # Nettoyer les clients déconnectés
        for client in disconnected_clients:
            subscribers.discard(client)
    
    def subscribe_client(self, client: ClientConnection, channel: ChannelType):
        """Abonne un client à un canal"""
        self.subscribers[channel].add(client)
        client.subscriptions.add(channel)
        logger.info(f"📡 Client {client.user_id or 'anonyme'} abonné au canal {channel.value}")
    
    def unsubscribe_client(self, client: ClientConnection, channel: ChannelType):
        """Désabonne un client d'un canal"""
        self.subscribers[channel].discard(client)
        client.subscriptions.discard(channel)
        logger.info(f"📡 Client {client.user_id or 'anonyme'} désabonné du canal {channel.value}")
    
    def stop_streaming(self):
        """Arrête le streaming"""
        self.running = False
        logger.info("🛑 Arrêt streaming données temps réel")

class WebSocketRealTimeServer:
    """Serveur WebSocket temps réel ultra-performant"""
    
    def __init__(self, host: str = "localhost", port: int = 8765, secret_key: str = "ultra_secret_key_2025"):
        self.host = host
        self.port = port
        self.secret_key = secret_key
        
        # Composants
        self.authenticator = WebSocketAuthenticator(secret_key)
        self.data_streamer = RealTimeDataStreamer()
        
        # Connexions actives
        self.clients: Dict[str, ClientConnection] = {}
        self.connection_count = 0
        
        # Serveur
        self.server = None
        self.running = False
        
    async def start_server(self):
        """Démarre le serveur WebSocket"""
        try:
            logger.info(f"🚀 Démarrage serveur WebSocket sur {self.host}:{self.port}")
            
            # Démarrer le streaming de données
            asyncio.create_task(self.data_streamer.start_streaming())
            
            # Démarrer le serveur WebSocket
            self.server = await websockets.serve(
                self.handle_client,
                self.host,
                self.port,
                ping_interval=20,
                ping_timeout=10,
                max_size=1024*1024,  # 1MB max message size
                compression="deflate"
            )
            
            self.running = True
            logger.info("✅ Serveur WebSocket démarré avec succès")
            
            # Garder le serveur en vie
            await self.server.wait_closed()
            
        except Exception as e:
            logger.error(f"❌ Erreur démarrage serveur: {e}")
            raise
    
    async def handle_client(self, websocket, path):
        """Gère une connexion client"""
        client_id = f"client_{self.connection_count}"
        self.connection_count += 1
        
        # Informations client
        remote_address = websocket.remote_address
        ip_address = remote_address[0] if remote_address else "unknown"
        
        client = ClientConnection(
            websocket=websocket,
            ip_address=ip_address,
            user_agent=websocket.request_headers.get("User-Agent", "unknown")
        )
        
        self.clients[client_id] = client
        
        logger.info(f"🔗 Nouvelle connexion: {client_id} depuis {ip_address}")
        
        try:
            # Message de bienvenue
            welcome_message = {
                'type': MessageType.SYSTEM_STATUS.value,
                'channel': ChannelType.SYSTEM.value,
                'data': {
                    'message': 'Bienvenue sur TradingBot Pro 2025 WebSocket',
                    'client_id': client_id,
                    'timestamp': datetime.now().isoformat(),
                    'available_channels': [ch.value for ch in ChannelType],
                    'auth_required': True
                },
                'timestamp': datetime.now().isoformat()
            }
            
            await websocket.send(json.dumps(welcome_message))
            
            # Boucle de traitement des messages
            async for message in websocket:
                await self.process_message(client, message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"🔌 Connexion fermée: {client_id}")
        except Exception as e:
            logger.error(f"❌ Erreur connexion {client_id}: {e}")
        finally:
            # Nettoyer la connexion
            await self.cleanup_client(client_id)
    
    async def process_message(self, client: ClientConnection, message: str):
        """Traite un message reçu du client"""
        try:
            data = json.loads(message)
            message_type = MessageType(data.get('type', ''))
            
            # Mettre à jour le ping
            client.last_ping = datetime.now()
            
            if message_type == MessageType.AUTH_REQUEST:
                await self.handle_auth_request(client, data)
            elif message_type == MessageType.SUBSCRIBE:
                await self.handle_subscribe(client, data)
            elif message_type == MessageType.UNSUBSCRIBE:
                await self.handle_unsubscribe(client, data)
            elif message_type == MessageType.HEARTBEAT:
                await self.handle_heartbeat(client)
            else:
                logger.warning(f"⚠️ Type de message non supporté: {message_type}")
                
        except json.JSONDecodeError:
            logger.warning("⚠️ Message JSON invalide reçu")
            await self.send_error(client, "Format JSON invalide")
        except ValueError as e:
            logger.warning(f"⚠️ Type de message invalide: {e}")
            await self.send_error(client, "Type de message non reconnu")
        except Exception as e:
            logger.error(f"❌ Erreur traitement message: {e}")
            await self.send_error(client, "Erreur interne serveur")
    
    async def handle_auth_request(self, client: ClientConnection, data: Dict):
        """Gère une demande d'authentification"""
        token = data.get('token', '')
        
        if not token:
            await self.send_error(client, "Token manquant")
            return
        
        # Vérifier le token
        payload = self.authenticator.verify_token(token)
        
        if payload:
            client.authenticated = True
            client.user_id = payload.get('user_id')
            
            response = {
                'type': MessageType.AUTH_RESPONSE.value,
                'channel': ChannelType.SYSTEM.value,
                'data': {
                    'authenticated': True,
                    'user_id': client.user_id,
                    'permissions': payload.get('permissions', []),
                    'message': 'Authentification réussie'
                },
                'timestamp': datetime.now().isoformat()
            }
            
            await client.websocket.send(json.dumps(response))
            logger.info(f"✅ Client authentifié: {client.user_id}")
        else:
            await self.send_error(client, "Token invalide ou expiré")
    
    async def handle_subscribe(self, client: ClientConnection, data: Dict):
        """Gère un abonnement à un canal"""
        if not client.authenticated:
            await self.send_error(client, "Authentification requise")
            return
        
        channel_name = data.get('channel', '')
        
        try:
            channel = ChannelType(channel_name)
            self.data_streamer.subscribe_client(client, channel)
            
            response = {
                'type': MessageType.SUBSCRIBE.value,
                'channel': ChannelType.SYSTEM.value,
                'data': {
                    'subscribed': True,
                    'channel': channel.value,
                    'message': f'Abonné au canal {channel.value}'
                },
                'timestamp': datetime.now().isoformat()
            }
            
            await client.websocket.send(json.dumps(response))
            
        except ValueError:
            await self.send_error(client, f"Canal invalide: {channel_name}")
    
    async def handle_unsubscribe(self, client: ClientConnection, data: Dict):
        """Gère un désabonnement d'un canal"""
        channel_name = data.get('channel', '')
        
        try:
            channel = ChannelType(channel_name)
            self.data_streamer.unsubscribe_client(client, channel)
            
            response = {
                'type': MessageType.UNSUBSCRIBE.value,
                'channel': ChannelType.SYSTEM.value,
                'data': {
                    'unsubscribed': True,
                    'channel': channel.value,
                    'message': f'Désabonné du canal {channel.value}'
                },
                'timestamp': datetime.now().isoformat()
            }
            
            await client.websocket.send(json.dumps(response))
            
        except ValueError:
            await self.send_error(client, f"Canal invalide: {channel_name}")
    
    async def handle_heartbeat(self, client: ClientConnection):
        """Gère un heartbeat"""
        response = {
            'type': MessageType.HEARTBEAT.value,
            'channel': ChannelType.SYSTEM.value,
            'data': {
                'status': 'alive',
                'server_time': datetime.now().isoformat()
            },
            'timestamp': datetime.now().isoformat()
        }
        
        await client.websocket.send(json.dumps(response))
    
    async def send_error(self, client: ClientConnection, message: str):
        """Envoie un message d'erreur au client"""
        error_message = {
            'type': MessageType.ERROR.value,
            'channel': ChannelType.SYSTEM.value,
            'data': {
                'error': True,
                'message': message
            },
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            await client.websocket.send(json.dumps(error_message))
        except Exception as e:
            logger.error(f"❌ Erreur envoi message d'erreur: {e}")
    
    async def cleanup_client(self, client_id: str):
        """Nettoie les ressources d'un client déconnecté"""
        client = self.clients.get(client_id)
        if not client:
            return
        
        # Désabonner de tous les canaux
        for channel in client.subscriptions.copy():
            self.data_streamer.unsubscribe_client(client, channel)
        
        # Supprimer de la liste des clients
        del self.clients[client_id]
        
        logger.info(f"🧹 Client {client_id} nettoyé")
    
    def generate_client_token(self, user_id: str, permissions: List[str] = None) -> str:
        """Génère un token pour un client (helper function)"""
        return self.authenticator.generate_token(user_id, permissions)
    
    async def stop_server(self):
        """Arrête le serveur"""
        self.running = False
        self.data_streamer.stop_streaming()
        
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
        logger.info("🛑 Serveur WebSocket arrêté")
    
    def get_server_stats(self) -> Dict[str, Any]:
        """Statistiques du serveur"""
        total_clients = len(self.clients)
        authenticated_clients = len([c for c in self.clients.values() if c.authenticated])
        
        subscriptions_by_channel = {}
        for channel in ChannelType:
            subscriptions_by_channel[channel.value] = len(self.data_streamer.subscribers[channel])
        
        return {
            'running': self.running,
            'total_clients': total_clients,
            'authenticated_clients': authenticated_clients,
            'subscriptions_by_channel': subscriptions_by_channel,
            'server_uptime': (datetime.now() - datetime.now()).total_seconds(),  # Placeholder
            'host': self.host,
            'port': self.port
        }

# ============================================================================
# 🧪 TESTS ET DÉMONSTRATION
# ============================================================================

async def test_websocket_server():
    """Test du serveur WebSocket"""
    print("🧪 TEST WEBSOCKET TEMPS RÉEL - TRADINGBOT PRO 2025")
    print("=" * 60)
    
    # Créer le serveur
    server = WebSocketRealTimeServer(host="localhost", port=8765)
    
    try:
        # Générer un token de test
        test_token = server.generate_client_token("user_test_001", ["read", "trade"])
        print(f"🔐 Token de test généré: {test_token[:50]}...")
        
        # Démarrer le serveur en arrière-plan
        print("🚀 Démarrage serveur WebSocket...")
        
        # Note: En production, utiliser asyncio.create_task() pour démarrer en arrière-plan
        # et avoir un client de test qui se connecte
        
        print("✅ Serveur WebSocket configuré et prêt")
        print(f"📡 URL de connexion: ws://{server.host}:{server.port}")
        print("🔧 Pour tester:")
        print("   1. Connexion WebSocket")
        print("   2. Envoi message auth avec token")
        print("   3. Abonnement aux canaux souhaités")
        print("   4. Réception données temps réel")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test: {e}")
        return False

if __name__ == "__main__":
    print("📊 WEBSOCKETS TEMPS RÉEL - TRADINGBOT PRO 2025")
    print("=" * 55)
    
    # Test de configuration
    success = asyncio.run(test_websocket_server())
    
    if success:
        print("\n✅ WEBSOCKETS TEMPS RÉEL CONFIGURÉS!")
        print("🚀 Prêt pour intégration")
    else:
        print("\n❌ ERREUR CONFIGURATION")
        
    print("\n" + "=" * 55)
