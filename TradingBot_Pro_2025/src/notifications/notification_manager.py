"""
Advanced notification system for TradingBot Pro 2025
"""
import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import logging

class NotificationType(Enum):
    """Types of notifications"""
    TRADE_EXECUTED = "trade_executed"
    STRATEGY_STARTED = "strategy_started"
    STRATEGY_STOPPED = "strategy_stopped"
    RISK_ALERT = "risk_alert"
    EMERGENCY_STOP = "emergency_stop"
    PROFIT_TARGET = "profit_target"
    LOSS_ALERT = "loss_alert"
    SYSTEM_ERROR = "system_error"

class NotificationChannel(Enum):
    """Available notification channels"""
    TELEGRAM = "telegram"
    DISCORD = "discord"
    EMAIL = "email"
    WEBHOOK = "webhook"
    SMS = "sms"

class NotificationManager:
    """Centralized notification management system"""
    
    def __init__(self, config: Dict[str, str] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.enabled_channels = set()
        self.message_templates = self._load_templates()
        
        # Configure enabled channels based on available config
        if self.config.get('TELEGRAM_BOT_TOKEN'):
            self.enabled_channels.add(NotificationChannel.TELEGRAM)
        if self.config.get('DISCORD_WEBHOOK_URL'):
            self.enabled_channels.add(NotificationChannel.DISCORD)
        if self.config.get('EMAIL_SMTP_SERVER'):
            self.enabled_channels.add(NotificationChannel.EMAIL)
    
    def _load_templates(self) -> Dict[NotificationType, Dict[str, str]]:
        """Load message templates for different notification types"""
        return {
            NotificationType.TRADE_EXECUTED: {
                "title": "🔄 Trade Executed",
                "template": "Trade: {side} {quantity} {symbol} at {price}\nPnL: {pnl}\nStrategy: {strategy}"
            },
            NotificationType.STRATEGY_STARTED: {
                "title": "▶️ Strategy Started",
                "template": "Strategy '{strategy}' has been started\nRisk Level: {risk_level}"
            },
            NotificationType.STRATEGY_STOPPED: {
                "title": "⏹️ Strategy Stopped",
                "template": "Strategy '{strategy}' has been stopped\nTotal PnL: {total_pnl}"
            },
            NotificationType.RISK_ALERT: {
                "title": "⚠️ Risk Alert",
                "template": "Risk alert triggered!\nType: {alert_type}\nValue: {value}\nThreshold: {threshold}"
            },
            NotificationType.EMERGENCY_STOP: {
                "title": "🚨 EMERGENCY STOP",
                "template": "EMERGENCY STOP ACTIVATED!\nReason: {reason}\nTime: {timestamp}\nAll trading halted."
            },
            NotificationType.PROFIT_TARGET: {
                "title": "🎯 Profit Target Hit",
                "template": "Profit target achieved!\nProfit: {profit}\nTarget: {target}\nStrategy: {strategy}"
            },
            NotificationType.LOSS_ALERT: {
                "title": "📉 Loss Alert",
                "template": "Loss threshold exceeded!\nLoss: {loss}\nThreshold: {threshold}\nStrategy: {strategy}"
            },
            NotificationType.SYSTEM_ERROR: {
                "title": "❌ System Error",
                "template": "System error detected!\nError: {error}\nComponent: {component}\nTime: {timestamp}"
            }
        }
    
    def format_message(self, notification_type: NotificationType, data: Dict[str, Any]) -> Dict[str, str]:
        """Format message using template"""
        template_info = self.message_templates.get(notification_type, {
            "title": "Notification",
            "template": str(data)
        })
        
        try:
            formatted_message = template_info["template"].format(**data)
            return {
                "title": template_info["title"],
                "message": formatted_message
            }
        except KeyError as e:
            self.logger.warning(f"Missing template data: {e}")
            return {
                "title": template_info["title"],
                "message": f"Notification data: {data}"
            }
    
    def send_telegram(self, title: str, message: str) -> bool:
        """Send notification via Telegram"""
        try:
            bot_token = self.config.get('TELEGRAM_BOT_TOKEN')
            chat_id = self.config.get('TELEGRAM_CHAT_ID')
            
            if not bot_token or not chat_id:
                self.logger.warning("Telegram configuration missing")
                return False
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            
            full_message = f"*{title}*\n\n{message}"
            
            payload = {
                'chat_id': chat_id,
                'text': full_message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            self.logger.info("Telegram notification sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send Telegram notification: {e}")
            return False
    
    def send_discord(self, title: str, message: str) -> bool:
        """Send notification via Discord webhook"""
        try:
            webhook_url = self.config.get('DISCORD_WEBHOOK_URL')
            
            if not webhook_url:
                self.logger.warning("Discord webhook URL not configured")
                return False
            
            embed = {
                "title": title,
                "description": message,
                "timestamp": datetime.utcnow().isoformat(),
                "color": self._get_color_for_title(title)
            }
            
            payload = {
                "embeds": [embed]
            }
            
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            self.logger.info("Discord notification sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send Discord notification: {e}")
            return False
    
    def send_webhook(self, title: str, message: str, webhook_url: str = None) -> bool:
        """Send notification via custom webhook"""
        try:
            url = webhook_url or self.config.get('CUSTOM_WEBHOOK_URL')
            
            if not url:
                self.logger.warning("Webhook URL not provided")
                return False
            
            payload = {
                "title": title,
                "message": message,
                "timestamp": datetime.utcnow().isoformat(),
                "source": "TradingBot Pro 2025"
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            self.logger.info("Webhook notification sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send webhook notification: {e}")
            return False
    
    def _get_color_for_title(self, title: str) -> int:
        """Get color code based on notification type"""
        if "EMERGENCY" in title:
            return 0xFF0000  # Red
        elif "Risk Alert" in title or "Loss Alert" in title:
            return 0xFF4500  # Orange Red
        elif "Profit Target" in title:
            return 0x00FF00  # Green
        elif "Trade Executed" in title:
            return 0x1E90FF  # Dodger Blue
        elif "Started" in title:
            return 0x32CD32  # Lime Green
        elif "Stopped" in title:
            return 0xFFD700  # Gold
        else:
            return 0x808080  # Gray
    
    def send_notification(self, 
                         notification_type: NotificationType, 
                         data: Dict[str, Any],
                         channels: Optional[List[NotificationChannel]] = None,
                         priority: str = "normal") -> Dict[NotificationChannel, bool]:
        """
        Send notification through specified channels
        
        Args:
            notification_type: Type of notification
            data: Data to include in notification
            channels: Specific channels to use (if None, use all enabled)
            priority: Priority level (low, normal, high, critical)
        
        Returns:
            Dictionary with success status for each channel
        """
        if channels is None:
            channels = list(self.enabled_channels)
        
        # Add timestamp if not present
        if 'timestamp' not in data:
            data['timestamp'] = datetime.utcnow().isoformat()
        
        # Format message
        formatted = self.format_message(notification_type, data)
        title = formatted["title"]
        message = formatted["message"]
        
        # Add priority indicator
        if priority == "critical":
            title = f"🚨 CRITICAL: {title}"
        elif priority == "high":
            title = f"❗ {title}"
        
        results = {}
        
        for channel in channels:
            if channel not in self.enabled_channels:
                self.logger.warning(f"Channel {channel} not enabled")
                results[channel] = False
                continue
            
            try:
                if channel == NotificationChannel.TELEGRAM:
                    results[channel] = self.send_telegram(title, message)
                elif channel == NotificationChannel.DISCORD:
                    results[channel] = self.send_discord(title, message)
                elif channel == NotificationChannel.WEBHOOK:
                    results[channel] = self.send_webhook(title, message)
                else:
                    self.logger.warning(f"Channel {channel} not implemented")
                    results[channel] = False
                    
            except Exception as e:
                self.logger.error(f"Error sending to {channel}: {e}")
                results[channel] = False
        
        return results
    
    def send_trade_notification(self, trade_data: Dict[str, Any]):
        """Convenience method for trade notifications"""
        self.send_notification(NotificationType.TRADE_EXECUTED, trade_data)
    
    def send_risk_alert(self, alert_data: Dict[str, Any]):
        """Convenience method for risk alerts"""
        self.send_notification(
            NotificationType.RISK_ALERT, 
            alert_data, 
            priority="high"
        )
    
    def send_emergency_alert(self, reason: str):
        """Convenience method for emergency alerts"""
        self.send_notification(
            NotificationType.EMERGENCY_STOP, 
            {"reason": reason},
            priority="critical"
        )

# Global notification manager instance
notification_manager = None

def initialize_notifications(config: Dict[str, str]):
    """Initialize global notification manager"""
    global notification_manager
    notification_manager = NotificationManager(config)
    return notification_manager

def send_notification(notification_type: NotificationType, data: Dict[str, Any], **kwargs):
    """Send notification using global manager"""
    if notification_manager:
        return notification_manager.send_notification(notification_type, data, **kwargs)
    else:
        logging.warning("Notification manager not initialized")
        return {}

if __name__ == '__main__':
    # Test the notification system
    test_config = {
        'TELEGRAM_BOT_TOKEN': 'test_token',
        'TELEGRAM_CHAT_ID': 'test_chat_id',
        'DISCORD_WEBHOOK_URL': 'https://discord.com/api/webhooks/test'
    }
    
    manager = NotificationManager(test_config)
    
    # Test trade notification
    trade_data = {
        "side": "BUY",
        "quantity": 0.1,
        "symbol": "BTC-USD",
        "price": 50000,
        "pnl": 100,
        "strategy": "Scalping Quantique"
    }
    
    results = manager.send_notification(NotificationType.TRADE_EXECUTED, trade_data)
    print("Notification results:", results)
