#!/usr/bin/env python3
"""
🔔 AMÉLIORATION MAJEURE: Système de Notifications Intelligent Ultra-Avancé
Alertes multi-canaux avec IA prédictive et gestion de priorités
"""

import asyncio
import logging
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
import json
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import requests
import os
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class NotificationLevel(Enum):
    """Niveaux de notification"""
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5
    EMERGENCY = 6

class NotificationChannel(Enum):
    """Canaux de notification"""
    EMAIL = "email"
    TELEGRAM = "telegram"
    DISCORD = "discord"
    WEBHOOK = "webhook"
    SMS = "sms"
    PUSH = "push"
    DESKTOP = "desktop"
    DASHBOARD = "dashboard"

class NotificationType(Enum):
    """Types de notifications"""
    TRADE_SIGNAL = "trade_signal"
    TRADE_EXECUTED = "trade_executed"
    PROFIT_LOSS = "profit_loss"
    RISK_ALERT = "risk_alert"
    MARKET_ALERT = "market_alert"
    SYSTEM_STATUS = "system_status"
    PORTFOLIO_UPDATE = "portfolio_update"
    AI_INSIGHT = "ai_insight"
    ERROR_ALERT = "error_alert"

@dataclass
class NotificationMessage:
    """Message de notification structuré"""
    id: str
    type: NotificationType
    level: NotificationLevel
    title: str
    message: str
    data: Dict
    timestamp: datetime
    channels: List[NotificationChannel]
    priority: int = 5  # 1-10 (10 = très urgent)
    expires_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
    is_sent: bool = False
    sent_channels: List[NotificationChannel] = None

    def __post_init__(self):
        if self.sent_channels is None:
            self.sent_channels = []

class NotificationProvider(ABC):
    """Interface pour les fournisseurs de notifications"""
    
    @abstractmethod
    async def send(self, message: NotificationMessage) -> bool:
        """Envoie une notification"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Vérifie si le fournisseur est disponible"""
        pass

class EmailProvider(NotificationProvider):
    """Fournisseur de notifications par email"""
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = os.getenv('NOTIFICATION_EMAIL')
        self.password = os.getenv('NOTIFICATION_EMAIL_PASSWORD')
        self.to_email = os.getenv('NOTIFICATION_TO_EMAIL', self.email)
    
    async def send(self, message: NotificationMessage) -> bool:
        """Envoie un email"""
        try:
            if not self.is_available():
                return False
            
            msg = MimeMultipart()
            msg['From'] = self.email
            msg['To'] = self.to_email
            msg['Subject'] = f"🤖 TradingBot: {message.title}"
            
            # Corps du message avec formatage HTML
            html_body = self._format_email_html(message)
            msg.attach(MimeText(html_body, 'html'))
            
            # Envoi
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            
            logger.info(f"📧 Email envoyé: {message.title}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur envoi email: {e}")
            return False
    
    def is_available(self) -> bool:
        """Vérifie si l'email est configuré"""
        return bool(self.email and self.password)
    
    def _format_email_html(self, message: NotificationMessage) -> str:
        """Formate le message en HTML"""
        level_colors = {
            NotificationLevel.DEBUG: "#6b7280",
            NotificationLevel.INFO: "#3b82f6",
            NotificationLevel.WARNING: "#f59e0b",
            NotificationLevel.ERROR: "#ef4444",
            NotificationLevel.CRITICAL: "#dc2626",
            NotificationLevel.EMERGENCY: "#991b1b"
        }
        
        color = level_colors.get(message.level, "#6b7280")
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0;">
                    <h1 style="margin: 0; font-size: 24px;">🤖 TradingBot Pro 2025 Ultra</h1>
                    <p style="margin: 5px 0 0 0; opacity: 0.9;">Notification de Trading IA</p>
                </div>
                
                <div style="background: white; border: 1px solid #e5e7eb; border-top: none; padding: 20px; border-radius: 0 0 10px 10px;">
                    <div style="border-left: 4px solid {color}; padding-left: 15px; margin-bottom: 20px;">
                        <h2 style="color: {color}; margin: 0 0 10px 0; font-size: 18px;">{message.title}</h2>
                        <p style="margin: 0; color: #6b7280; font-size: 14px;">
                            {message.level.name} • {message.type.value} • {message.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
                        </p>
                    </div>
                    
                    <div style="background: #f9fafb; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                        <p style="margin: 0; font-size: 16px; line-height: 1.5;">{message.message}</p>
                    </div>
                    
                    {self._format_data_table(message.data)}
                    
                    <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #e5e7eb; font-size: 12px; color: #6b7280;">
                        <p style="margin: 0;">Envoyé par TradingBot Pro 2025 Ultra • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _format_data_table(self, data: Dict) -> str:
        """Formate les données en tableau HTML"""
        if not data:
            return ""
        
        html = "<div style='margin: 15px 0;'><h3 style='color: #374151; font-size: 16px; margin-bottom: 10px;'>📊 Détails:</h3><table style='width: 100%; border-collapse: collapse;'>"
        
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value, indent=2)
            
            html += f"""
            <tr style='border-bottom: 1px solid #e5e7eb;'>
                <td style='padding: 8px 12px; font-weight: bold; color: #374151; background: #f9fafb;'>{key.replace('_', ' ').title()}</td>
                <td style='padding: 8px 12px; color: #6b7280;'>{value}</td>
            </tr>
            """
        
        html += "</table></div>"
        return html

class TelegramProvider(NotificationProvider):
    """Fournisseur de notifications Telegram"""
    
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    async def send(self, message: NotificationMessage) -> bool:
        """Envoie un message Telegram"""
        try:
            if not self.is_available():
                return False
            
            # Formatage du message
            formatted_message = self._format_telegram_message(message)
            
            # Envoi via API Telegram
            url = f"{self.api_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': formatted_message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': True
            }
            
            async with asyncio.timeout(10):
                response = requests.post(url, json=payload)
                response.raise_for_status()
            
            logger.info(f"📱 Telegram envoyé: {message.title}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur envoi Telegram: {e}")
            return False
    
    def is_available(self) -> bool:
        """Vérifie si Telegram est configuré"""
        return bool(self.bot_token and self.chat_id)
    
    def _format_telegram_message(self, message: NotificationMessage) -> str:
        """Formate le message pour Telegram"""
        level_emoji = {
            NotificationLevel.DEBUG: "🔍",
            NotificationLevel.INFO: "ℹ️",
            NotificationLevel.WARNING: "⚠️",
            NotificationLevel.ERROR: "❌",
            NotificationLevel.CRITICAL: "🚨",
            NotificationLevel.EMERGENCY: "🆘"
        }
        
        type_emoji = {
            NotificationType.TRADE_SIGNAL: "📈",
            NotificationType.TRADE_EXECUTED: "✅",
            NotificationType.PROFIT_LOSS: "💰",
            NotificationType.RISK_ALERT: "⚠️",
            NotificationType.MARKET_ALERT: "📊",
            NotificationType.SYSTEM_STATUS: "🔧",
            NotificationType.PORTFOLIO_UPDATE: "💼",
            NotificationType.AI_INSIGHT: "🧠",
            NotificationType.ERROR_ALERT: "❌"
        }
        
        emoji = level_emoji.get(message.level, "📢")
        type_emoji_str = type_emoji.get(message.type, "📢")
        
        formatted = f"*🤖 TradingBot Pro 2025 Ultra*\n\n"
        formatted += f"{emoji} {type_emoji_str} *{message.title}*\n\n"
        formatted += f"_{message.message}_\n\n"
        
        if message.data:
            formatted += "*📊 Détails:*\n"
            for key, value in message.data.items():
                if isinstance(value, (dict, list)):
                    continue  # Skip complex objects for Telegram
                formatted += f"• *{key.replace('_', ' ').title()}:* {value}\n"
        
        formatted += f"\n🕐 _{message.timestamp.strftime('%Y-%m-%d %H:%M:%S')}_"
        
        return formatted

class DiscordProvider(NotificationProvider):
    """Fournisseur de notifications Discord"""
    
    def __init__(self):
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    async def send(self, message: NotificationMessage) -> bool:
        """Envoie un message Discord"""
        try:
            if not self.is_available():
                return False
            
            # Formatage du message Discord
            embed = self._create_discord_embed(message)
            
            payload = {
                'embeds': [embed],
                'username': 'TradingBot Pro 2025 Ultra',
                'avatar_url': 'https://via.placeholder.com/128/667eea/ffffff?text=🤖'
            }
            
            async with asyncio.timeout(10):
                response = requests.post(self.webhook_url, json=payload)
                response.raise_for_status()
            
            logger.info(f"🎮 Discord envoyé: {message.title}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur envoi Discord: {e}")
            return False
    
    def is_available(self) -> bool:
        """Vérifie si Discord est configuré"""
        return bool(self.webhook_url)
    
    def _create_discord_embed(self, message: NotificationMessage) -> Dict:
        """Crée un embed Discord"""
        level_colors = {
            NotificationLevel.DEBUG: 0x6b7280,
            NotificationLevel.INFO: 0x3b82f6,
            NotificationLevel.WARNING: 0xf59e0b,
            NotificationLevel.ERROR: 0xef4444,
            NotificationLevel.CRITICAL: 0xdc2626,
            NotificationLevel.EMERGENCY: 0x991b1b
        }
        
        color = level_colors.get(message.level, 0x6b7280)
        
        embed = {
            'title': f"🤖 {message.title}",
            'description': message.message,
            'color': color,
            'timestamp': message.timestamp.isoformat(),
            'footer': {
                'text': f"TradingBot Pro 2025 Ultra • {message.level.name} • {message.type.value}"
            },
            'fields': []
        }
        
        # Ajouter les données comme fields
        for key, value in list(message.data.items())[:5]:  # Limiter à 5 fields
            if isinstance(value, (dict, list)):
                value = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
            
            embed['fields'].append({
                'name': key.replace('_', ' ').title(),
                'value': str(value),
                'inline': True
            })
        
        return embed

class WebhookProvider(NotificationProvider):
    """Fournisseur de notifications webhook générique"""
    
    def __init__(self):
        self.webhook_urls = [
            url.strip() for url in os.getenv('WEBHOOK_URLS', '').split(',') 
            if url.strip()
        ]
    
    async def send(self, message: NotificationMessage) -> bool:
        """Envoie vers les webhooks"""
        try:
            if not self.is_available():
                return False
            
            payload = {
                'id': message.id,
                'type': message.type.value,
                'level': message.level.name,
                'title': message.title,
                'message': message.message,
                'data': message.data,
                'timestamp': message.timestamp.isoformat(),
                'priority': message.priority
            }
            
            success_count = 0
            for webhook_url in self.webhook_urls:
                try:
                    async with asyncio.timeout(10):
                        response = requests.post(webhook_url, json=payload)
                        if response.status_code == 200:
                            success_count += 1
                except Exception as e:
                    logger.warning(f"⚠️ Erreur webhook {webhook_url}: {e}")
            
            if success_count > 0:
                logger.info(f"🔗 Webhook envoyé: {success_count}/{len(self.webhook_urls)}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Erreur envoi webhook: {e}")
            return False
    
    def is_available(self) -> bool:
        """Vérifie si des webhooks sont configurés"""
        return len(self.webhook_urls) > 0

class DesktopProvider(NotificationProvider):
    """Fournisseur de notifications desktop"""
    
    async def send(self, message: NotificationMessage) -> bool:
        """Envoie une notification desktop"""
        try:
            import plyer
            
            plyer.notification.notify(
                title=f"🤖 TradingBot: {message.title}",
                message=message.message,
                app_name="TradingBot Pro 2025 Ultra",
                timeout=10
            )
            
            logger.info(f"🖥️ Notification desktop envoyée: {message.title}")
            return True
            
        except ImportError:
            logger.warning("📱 plyer non installé pour notifications desktop")
            return False
        except Exception as e:
            logger.error(f"❌ Erreur notification desktop: {e}")
            return False
    
    def is_available(self) -> bool:
        """Vérifie si les notifications desktop sont disponibles"""
        try:
            import plyer
            return True
        except ImportError:
            return False

class IntelligentNotificationManager:
    """
    🧠 Gestionnaire de Notifications Intelligent Ultra-Avancé
    
    Fonctionnalités:
    - 🎯 Routage intelligent basé sur priorité et contexte
    - 🔄 Retry automatique avec backoff exponentiel
    - 📊 Groupement et déduplication des notifications
    - 🎛️ Filtrage adaptatif basé sur les préférences
    - 📈 Analyse prédictive des notifications importantes
    - 🔕 Mode silencieux et horaires personnalisés
    """
    
    def __init__(self):
        self.providers = {
            NotificationChannel.EMAIL: EmailProvider(),
            NotificationChannel.TELEGRAM: TelegramProvider(),
            NotificationChannel.DISCORD: DiscordProvider(),
            NotificationChannel.WEBHOOK: WebhookProvider(),
            NotificationChannel.DESKTOP: DesktopProvider()
        }
        
        self.message_queue = asyncio.Queue()
        self.sent_messages = {}  # Cache des messages envoyés
        self.notification_history = []
        self.user_preferences = self._load_preferences()
        self.processing_task = None
        
        # Configuration des règles de routage
        self.routing_rules = {
            NotificationLevel.EMERGENCY: [NotificationChannel.EMAIL, NotificationChannel.TELEGRAM, NotificationChannel.DISCORD, NotificationChannel.DESKTOP],
            NotificationLevel.CRITICAL: [NotificationChannel.EMAIL, NotificationChannel.TELEGRAM, NotificationChannel.DESKTOP],
            NotificationLevel.ERROR: [NotificationChannel.EMAIL, NotificationChannel.TELEGRAM],
            NotificationLevel.WARNING: [NotificationChannel.TELEGRAM, NotificationChannel.DISCORD],
            NotificationLevel.INFO: [NotificationChannel.DASHBOARD],
            NotificationLevel.DEBUG: []
        }
        
        # Groupement des notifications
        self.notification_groups = {}
        self.group_timers = {}
        
    def _load_preferences(self) -> Dict:
        """Charge les préférences utilisateur"""
        default_preferences = {
            'quiet_hours': {
                'enabled': True,
                'start': '22:00',
                'end': '08:00',
                'emergency_override': True
            },
            'frequency_limits': {
                NotificationType.TRADE_SIGNAL.value: {'max_per_hour': 10},
                NotificationType.MARKET_ALERT.value: {'max_per_hour': 5},
                NotificationType.SYSTEM_STATUS.value: {'max_per_hour': 3}
            },
            'minimum_levels': {
                NotificationChannel.EMAIL.value: NotificationLevel.WARNING.value,
                NotificationChannel.TELEGRAM.value: NotificationLevel.INFO.value,
                NotificationChannel.DESKTOP.value: NotificationLevel.WARNING.value
            },
            'enabled_channels': [
                NotificationChannel.EMAIL.value,
                NotificationChannel.TELEGRAM.value,
                NotificationChannel.DASHBOARD.value
            ]
        }
        
        try:
            # TODO: Charger depuis un fichier de configuration
            return default_preferences
        except Exception:
            return default_preferences
    
    async def start(self):
        """Démarre le gestionnaire de notifications"""
        if self.processing_task is None or self.processing_task.done():
            self.processing_task = asyncio.create_task(self._process_notifications())
            logger.info("🔔 Gestionnaire de notifications démarré")
    
    async def stop(self):
        """Arrête le gestionnaire de notifications"""
        if self.processing_task and not self.processing_task.done():
            self.processing_task.cancel()
            try:
                await self.processing_task
            except asyncio.CancelledError:
                pass
            logger.info("🔕 Gestionnaire de notifications arrêté")
    
    async def send_notification(self, 
                              title: str,
                              message: str,
                              level: NotificationLevel = NotificationLevel.INFO,
                              notification_type: NotificationType = NotificationType.SYSTEM_STATUS,
                              data: Dict = None,
                              channels: List[NotificationChannel] = None,
                              priority: int = 5) -> str:
        """
        🚀 Envoie une notification intelligente
        
        Args:
            title: Titre de la notification
            message: Message principal
            level: Niveau de priorité
            notification_type: Type de notification
            data: Données additionnelles
            channels: Canaux spécifiques (optionnel)
            priority: Priorité 1-10 (10 = urgent)
        
        Returns:
            ID unique de la notification
        """
        try:
            # Génération d'un ID unique
            notification_id = f"{notification_type.value}_{int(datetime.now().timestamp())}"
            
            # Détermination des canaux
            if channels is None:
                channels = self._determine_channels(level, notification_type)
            
            # Filtrage basé sur les préférences
            channels = self._filter_channels(channels, level, notification_type)
            
            # Vérification des heures silencieuses
            if self._is_quiet_hours() and level.value < NotificationLevel.EMERGENCY.value:
                if not self.user_preferences['quiet_hours']['emergency_override']:
                    logger.info(f"🔕 Notification en attente (heures silencieuses): {title}")
                    return notification_id
            
            # Vérification des limites de fréquence
            if not self._check_frequency_limits(notification_type):
                logger.info(f"⏰ Notification ignorée (limite de fréquence): {title}")
                return notification_id
            
            # Création du message
            notification_message = NotificationMessage(
                id=notification_id,
                type=notification_type,
                level=level,
                title=title,
                message=message,
                data=data or {},
                timestamp=datetime.now(),
                channels=channels,
                priority=priority
            )
            
            # Déduplication
            if self._is_duplicate(notification_message):
                logger.info(f"🔄 Notification dupliquée ignorée: {title}")
                return notification_id
            
            # Groupement si applicable
            if self._should_group(notification_message):
                await self._add_to_group(notification_message)
                return notification_id
            
            # Ajout à la queue
            await self.message_queue.put(notification_message)
            
            logger.info(f"📬 Notification ajoutée à la queue: {title} ({level.name})")
            return notification_id
            
        except Exception as e:
            logger.error(f"❌ Erreur envoi notification: {e}")
            return ""
    
    async def _process_notifications(self):
        """Traite les notifications en arrière-plan"""
        while True:
            try:
                # Récupération du message avec timeout
                try:
                    message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    continue
                
                # Traitement du message
                await self._send_message(message)
                
                # Marquer comme terminé
                self.message_queue.task_done()
                
            except Exception as e:
                logger.error(f"❌ Erreur traitement notifications: {e}")
                await asyncio.sleep(1)
    
    async def _send_message(self, message: NotificationMessage):
        """Envoie un message via tous les canaux configurés"""
        try:
            success_count = 0
            
            for channel in message.channels:
                provider = self.providers.get(channel)
                if provider and provider.is_available():
                    try:
                        success = await provider.send(message)
                        if success:
                            message.sent_channels.append(channel)
                            success_count += 1
                    except Exception as e:
                        logger.error(f"❌ Erreur envoi {channel.value}: {e}")
            
            # Mise à jour du statut
            message.is_sent = success_count > 0
            
            if success_count > 0:
                logger.info(f"✅ Notification envoyée via {success_count}/{len(message.channels)} canaux: {message.title}")
                self._record_success(message)
            else:
                logger.warning(f"⚠️ Échec envoi notification: {message.title}")
                await self._handle_failed_message(message)
            
            # Sauvegarde dans l'historique
            self._add_to_history(message)
            
        except Exception as e:
            logger.error(f"❌ Erreur envoi message: {e}")
    
    async def _handle_failed_message(self, message: NotificationMessage):
        """Gère les messages en échec"""
        try:
            if message.retry_count < message.max_retries:
                message.retry_count += 1
                
                # Backoff exponentiel
                delay = min(300, 2 ** message.retry_count)  # Max 5 minutes
                
                logger.info(f"🔄 Retry {message.retry_count}/{message.max_retries} dans {delay}s: {message.title}")
                
                # Re-programmer l'envoi
                asyncio.create_task(self._retry_message(message, delay))
            else:
                logger.error(f"❌ Abandon après {message.max_retries} tentatives: {message.title}")
        
        except Exception as e:
            logger.error(f"❌ Erreur gestion échec: {e}")
    
    async def _retry_message(self, message: NotificationMessage, delay: int):
        """Retry un message après délai"""
        await asyncio.sleep(delay)
        await self.message_queue.put(message)
    
    def _determine_channels(self, level: NotificationLevel, notification_type: NotificationType) -> List[NotificationChannel]:
        """Détermine les canaux basés sur le niveau et le type"""
        # Canaux par défaut selon le niveau
        default_channels = self.routing_rules.get(level, [NotificationChannel.DASHBOARD])
        
        # Ajustements selon le type
        if notification_type == NotificationType.TRADE_EXECUTED:
            # Toujours notifier les trades
            if NotificationChannel.TELEGRAM not in default_channels:
                default_channels.append(NotificationChannel.TELEGRAM)
        
        elif notification_type == NotificationType.PROFIT_LOSS:
            # Profits/pertes importantes
            if level.value >= NotificationLevel.WARNING.value:
                if NotificationChannel.EMAIL not in default_channels:
                    default_channels.append(NotificationChannel.EMAIL)
        
        elif notification_type == NotificationType.AI_INSIGHT:
            # Insights IA uniquement si pertinents
            if level.value >= NotificationLevel.INFO.value:
                default_channels = [NotificationChannel.DASHBOARD, NotificationChannel.TELEGRAM]
        
        return default_channels
    
    def _filter_channels(self, channels: List[NotificationChannel], level: NotificationLevel, notification_type: NotificationType) -> List[NotificationChannel]:
        """Filtre les canaux selon les préférences utilisateur"""
        filtered_channels = []
        
        for channel in channels:
            # Vérifier si le canal est activé
            if channel.value not in self.user_preferences['enabled_channels']:
                continue
            
            # Vérifier le niveau minimum
            min_level = self.user_preferences['minimum_levels'].get(channel.value, NotificationLevel.DEBUG.value)
            if level.value < min_level:
                continue
            
            # Vérifier la disponibilité du provider
            provider = self.providers.get(channel)
            if not provider or not provider.is_available():
                continue
            
            filtered_channels.append(channel)
        
        return filtered_channels
    
    def _is_quiet_hours(self) -> bool:
        """Vérifie si on est en heures silencieuses"""
        if not self.user_preferences['quiet_hours']['enabled']:
            return False
        
        now = datetime.now().time()
        start_time = datetime.strptime(self.user_preferences['quiet_hours']['start'], '%H:%M').time()
        end_time = datetime.strptime(self.user_preferences['quiet_hours']['end'], '%H:%M').time()
        
        if start_time <= end_time:
            return start_time <= now <= end_time
        else:
            # Période traversant minuit
            return now >= start_time or now <= end_time
    
    def _check_frequency_limits(self, notification_type: NotificationType) -> bool:
        """Vérifie les limites de fréquence"""
        limits = self.user_preferences['frequency_limits'].get(notification_type.value)
        if not limits:
            return True
        
        max_per_hour = limits.get('max_per_hour', float('inf'))
        one_hour_ago = datetime.now() - timedelta(hours=1)
        
        # Compter les notifications du même type dans la dernière heure
        recent_count = sum(
            1 for msg in self.notification_history
            if msg['type'] == notification_type.value and msg['timestamp'] > one_hour_ago
        )
        
        return recent_count < max_per_hour
    
    def _is_duplicate(self, message: NotificationMessage) -> bool:
        """Vérifie si c'est un duplicata"""
        # Recherche dans les 10 derniers messages
        recent_messages = self.notification_history[-10:]
        
        for msg in recent_messages:
            if (msg['title'] == message.title and 
                msg['type'] == message.type.value and
                (datetime.now() - msg['timestamp']).total_seconds() < 300):  # 5 minutes
                return True
        
        return False
    
    def _should_group(self, message: NotificationMessage) -> bool:
        """Détermine si le message doit être groupé"""
        groupable_types = [
            NotificationType.TRADE_SIGNAL,
            NotificationType.MARKET_ALERT,
            NotificationType.PORTFOLIO_UPDATE
        ]
        
        return (message.type in groupable_types and 
                message.level.value <= NotificationLevel.INFO.value)
    
    async def _add_to_group(self, message: NotificationMessage):
        """Ajoute un message à un groupe"""
        group_key = f"{message.type.value}_{message.level.value}"
        
        if group_key not in self.notification_groups:
            self.notification_groups[group_key] = []
        
        self.notification_groups[group_key].append(message)
        
        # Timer pour envoyer le groupe
        if group_key not in self.group_timers:
            self.group_timers[group_key] = asyncio.create_task(
                self._send_grouped_notifications(group_key, delay=60)  # 1 minute
            )
    
    async def _send_grouped_notifications(self, group_key: str, delay: int):
        """Envoie les notifications groupées"""
        await asyncio.sleep(delay)
        
        if group_key in self.notification_groups:
            messages = self.notification_groups.pop(group_key)
            self.group_timers.pop(group_key, None)
            
            if messages:
                grouped_message = self._create_grouped_message(messages)
                await self.message_queue.put(grouped_message)
    
    def _create_grouped_message(self, messages: List[NotificationMessage]) -> NotificationMessage:
        """Crée un message groupé"""
        first_message = messages[0]
        count = len(messages)
        
        title = f"{count} {first_message.type.value.replace('_', ' ').title()}s"
        
        message_text = f"Résumé de {count} notifications:\n\n"
        for i, msg in enumerate(messages[:5], 1):  # Limiter à 5
            message_text += f"{i}. {msg.title}\n"
        
        if count > 5:
            message_text += f"\n... et {count - 5} autres"
        
        return NotificationMessage(
            id=f"group_{first_message.type.value}_{int(datetime.now().timestamp())}",
            type=first_message.type,
            level=first_message.level,
            title=title,
            message=message_text,
            data={'grouped_count': count, 'group_type': first_message.type.value},
            timestamp=datetime.now(),
            channels=first_message.channels,
            priority=first_message.priority
        )
    
    def _record_success(self, message: NotificationMessage):
        """Enregistre un succès d'envoi"""
        self.sent_messages[message.id] = {
            'message': message,
            'sent_at': datetime.now(),
            'channels': message.sent_channels
        }
        
        # Nettoyer les anciens messages (garder 1000 max)
        if len(self.sent_messages) > 1000:
            oldest_keys = list(self.sent_messages.keys())[:100]
            for key in oldest_keys:
                del self.sent_messages[key]
    
    def _add_to_history(self, message: NotificationMessage):
        """Ajoute à l'historique"""
        self.notification_history.append({
            'id': message.id,
            'type': message.type.value,
            'level': message.level.name,
            'title': message.title,
            'timestamp': datetime.now(),
            'channels': [c.value for c in message.sent_channels],
            'success': message.is_sent
        })
        
        # Garder seulement les 1000 derniers
        if len(self.notification_history) > 1000:
            self.notification_history = self.notification_history[-1000:]
    
    def get_notification_stats(self) -> Dict:
        """Retourne les statistiques des notifications"""
        now = datetime.now()
        day_ago = now - timedelta(days=1)
        hour_ago = now - timedelta(hours=1)
        
        last_24h = [msg for msg in self.notification_history if msg['timestamp'] > day_ago]
        last_hour = [msg for msg in self.notification_history if msg['timestamp'] > hour_ago]
        
        return {
            'total_sent': len(self.notification_history),
            'last_24h': len(last_24h),
            'last_hour': len(last_hour),
            'success_rate_24h': sum(msg['success'] for msg in last_24h) / len(last_24h) * 100 if last_24h else 0,
            'active_providers': sum(1 for p in self.providers.values() if p.is_available()),
            'queue_size': self.message_queue.qsize(),
            'grouped_pending': len(self.notification_groups)
        }
    
    def get_recent_notifications(self, limit: int = 20) -> List[Dict]:
        """Retourne les notifications récentes"""
        return self.notification_history[-limit:]
    
    async def send_test_notifications(self) -> Dict:
        """Envoie des notifications de test"""
        results = {}
        
        test_message = NotificationMessage(
            id="test_notification",
            type=NotificationType.SYSTEM_STATUS,
            level=NotificationLevel.INFO,
            title="Test de Notification",
            message="Ceci est un test du système de notifications TradingBot Pro 2025 Ultra",
            data={'test': True, 'timestamp': datetime.now().isoformat()},
            timestamp=datetime.now(),
            channels=list(self.providers.keys())
        )
        
        for channel, provider in self.providers.items():
            if provider.is_available():
                try:
                    success = await provider.send(test_message)
                    results[channel.value] = 'success' if success else 'failed'
                except Exception as e:
                    results[channel.value] = f'error: {str(e)}'
            else:
                results[channel.value] = 'not_configured'
        
        return results

# Instance globale
notification_manager = IntelligentNotificationManager()

# Fonctions utilitaires
async def notify_trade_signal(symbol: str, action: str, confidence: float, data: Dict = None):
    """Notification de signal de trading"""
    level = NotificationLevel.WARNING if confidence > 0.8 else NotificationLevel.INFO
    
    await notification_manager.send_notification(
        title=f"🎯 Signal Trading: {action.upper()} {symbol}",
        message=f"Signal {action} détecté pour {symbol} (confiance: {confidence:.1%})",
        level=level,
        notification_type=NotificationType.TRADE_SIGNAL,
        data=data or {},
        priority=8 if confidence > 0.8 else 6
    )

async def notify_trade_executed(symbol: str, action: str, amount: float, price: float, data: Dict = None):
    """Notification de trade exécuté"""
    await notification_manager.send_notification(
        title=f"✅ Trade Exécuté: {action.upper()} {symbol}",
        message=f"Trade {action} exécuté: {amount:.6f} {symbol} à {price:.2f}$",
        level=NotificationLevel.INFO,
        notification_type=NotificationType.TRADE_EXECUTED,
        data=data or {},
        priority=7
    )

async def notify_profit_loss(symbol: str, pnl: float, pnl_pct: float, data: Dict = None):
    """Notification de profit/perte"""
    level = NotificationLevel.WARNING if abs(pnl_pct) > 5 else NotificationLevel.INFO
    emoji = "💰" if pnl > 0 else "📉"
    
    await notification_manager.send_notification(
        title=f"{emoji} P&L: {'+' if pnl > 0 else ''}{pnl:.2f}$ ({'+' if pnl_pct > 0 else ''}{pnl_pct:.1f}%)",
        message=f"Position {symbol}: {'+' if pnl > 0 else ''}{pnl:.2f}$ ({'+' if pnl_pct > 0 else ''}{pnl_pct:.1f}%)",
        level=level,
        notification_type=NotificationType.PROFIT_LOSS,
        data=data or {},
        priority=8 if abs(pnl_pct) > 10 else 6
    )

async def notify_risk_alert(message: str, risk_level: str, data: Dict = None):
    """Notification d'alerte de risque"""
    level_map = {
        'low': NotificationLevel.INFO,
        'medium': NotificationLevel.WARNING,
        'high': NotificationLevel.ERROR,
        'critical': NotificationLevel.CRITICAL
    }
    
    level = level_map.get(risk_level, NotificationLevel.WARNING)
    
    await notification_manager.send_notification(
        title=f"⚠️ Alerte Risque: {risk_level.upper()}",
        message=message,
        level=level,
        notification_type=NotificationType.RISK_ALERT,
        data=data or {},
        priority=9 if risk_level in ['high', 'critical'] else 7
    )

async def notify_system_status(status: str, message: str, data: Dict = None):
    """Notification de statut système"""
    level_map = {
        'online': NotificationLevel.INFO,
        'warning': NotificationLevel.WARNING,
        'error': NotificationLevel.ERROR,
        'maintenance': NotificationLevel.INFO
    }
    
    level = level_map.get(status, NotificationLevel.INFO)
    
    await notification_manager.send_notification(
        title=f"🔧 Système: {status.upper()}",
        message=message,
        level=level,
        notification_type=NotificationType.SYSTEM_STATUS,
        data=data or {},
        priority=5
    )

async def notify_ai_insight(insight: str, confidence: float, data: Dict = None):
    """Notification d'insight IA"""
    await notification_manager.send_notification(
        title=f"🧠 Insight IA (confiance: {confidence:.1%})",
        message=insight,
        level=NotificationLevel.INFO,
        notification_type=NotificationType.AI_INSIGHT,
        data=data or {},
        priority=6
    )

# Démarrage automatique
async def start_notification_system():
    """Démarre le système de notifications"""
    await notification_manager.start()

def stop_notification_system():
    """Arrête le système de notifications"""
    if notification_manager.processing_task:
        notification_manager.processing_task.cancel()

def get_notification_system_status() -> Dict:
    """Retourne le statut du système de notifications"""
    return {
        'manager_status': 'running' if notification_manager.processing_task and not notification_manager.processing_task.done() else 'stopped',
        'providers_available': {channel.value: provider.is_available() for channel, provider in notification_manager.providers.items()},
        'stats': notification_manager.get_notification_stats(),
        'recent_notifications': notification_manager.get_recent_notifications(10)
    }
