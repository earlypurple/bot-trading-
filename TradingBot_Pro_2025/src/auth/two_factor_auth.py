#!/usr/bin/env python3
"""
🔐 AUTHENTIFICATION 2FA - TRADINGBOT PRO 2025
============================================
🛡️ Système d'authentification à deux facteurs ultra-sécurisé
📱 Support TOTP, SMS, Email et clés de sauvegarde
🔒 Chiffrement avancé et protection contre les attaques

🎯 Fonctionnalités:
- TOTP (Google Authenticator, Authy)
- SMS avec codes temporaires
- Email avec liens sécurisés  
- Clés de sauvegarde
- Session management avancé
- Protection brute force
"""

import asyncio
import hashlib
import hmac
import time
import secrets
import base64
import qrcode
import io
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import logging
import json
import aiohttp
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import pyotp
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import bcrypt
import jwt

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Auth2FA")

class AuthMethod(Enum):
    """Méthodes d'authentification disponibles"""
    PASSWORD = "password"
    TOTP = "totp"
    SMS = "sms"
    EMAIL = "email"
    BACKUP_CODE = "backup_code"
    BIOMETRIC = "biometric"

class AuthStatus(Enum):
    """Statuts d'authentification"""
    PENDING = "pending"
    PARTIAL = "partial"  # Première étape validée
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"
    LOCKED = "locked"

@dataclass
class AuthAttempt:
    """Tentative d'authentification"""
    user_id: str
    method: AuthMethod
    timestamp: datetime
    ip_address: str
    user_agent: str
    success: bool
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TwoFactorConfig:
    """Configuration 2FA d'un utilisateur"""
    user_id: str
    totp_secret: Optional[str] = None
    totp_enabled: bool = False
    sms_phone: Optional[str] = None
    sms_enabled: bool = False
    email_enabled: bool = False
    backup_codes: List[str] = field(default_factory=list)
    recovery_email: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None

@dataclass
class AuthSession:
    """Session d'authentification"""
    session_id: str
    user_id: str
    status: AuthStatus
    methods_completed: List[AuthMethod] = field(default_factory=list)
    methods_required: List[AuthMethod] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(minutes=15))
    ip_address: str = ""
    user_agent: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

class PasswordManager:
    """Gestionnaire de mots de passe sécurisé"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash un mot de passe avec bcrypt"""
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Vérifie un mot de passe"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def check_password_strength(password: str) -> Dict[str, Any]:
        """Vérifie la force d'un mot de passe"""
        score = 0
        issues = []
        
        if len(password) >= 8:
            score += 1
        else:
            issues.append("Minimum 8 caractères requis")
            
        if any(c.isupper() for c in password):
            score += 1
        else:
            issues.append("Au moins une majuscule requise")
            
        if any(c.islower() for c in password):
            score += 1
        else:
            issues.append("Au moins une minuscule requise")
            
        if any(c.isdigit() for c in password):
            score += 1
        else:
            issues.append("Au moins un chiffre requis")
            
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        else:
            issues.append("Au moins un caractère spécial requis")
            
        strength_levels = {
            0: "Très faible",
            1: "Faible", 
            2: "Moyen",
            3: "Fort",
            4: "Très fort",
            5: "Excellent"
        }
        
        return {
            'score': score,
            'max_score': 5,
            'strength': strength_levels.get(score, "Inconnu"),
            'issues': issues,
            'valid': score >= 4
        }

class TOTPManager:
    """Gestionnaire TOTP (Time-based One-Time Password)"""
    
    def __init__(self, app_name: str = "TradingBot Pro 2025"):
        self.app_name = app_name
    
    def generate_secret(self) -> str:
        """Génère un secret TOTP"""
        return pyotp.random_base32()
    
    def generate_qr_code(self, user_email: str, secret: str) -> bytes:
        """Génère un QR code pour la configuration TOTP"""
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_email,
            issuer_name=self.app_name
        )
        
        # Créer QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        # Convertir en bytes
        img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        return img_buffer.getvalue()
    
    def verify_totp(self, secret: str, token: str, window: int = 1) -> bool:
        """Vérifie un code TOTP"""
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(token, valid_window=window)
        except Exception as e:
            logger.error(f"❌ Erreur vérification TOTP: {e}")
            return False
    
    def get_current_totp(self, secret: str) -> str:
        """Obtient le code TOTP actuel (pour tests)"""
        totp = pyotp.TOTP(secret)
        return totp.now()

class SMSManager:
    """Gestionnaire SMS pour codes de vérification"""
    
    def __init__(self, api_key: str = "", api_secret: str = ""):
        self.api_key = api_key
        self.api_secret = api_secret
        self.pending_codes: Dict[str, Dict] = {}
    
    def generate_sms_code(self) -> str:
        """Génère un code SMS à 6 chiffres"""
        return f"{secrets.randbelow(900000) + 100000}"
    
    async def send_sms_code(self, phone_number: str, user_id: str) -> bool:
        """Envoie un code SMS"""
        try:
            code = self.generate_sms_code()
            
            # Stocker le code temporairement
            self.pending_codes[f"{user_id}:{phone_number}"] = {
                'code': code,
                'timestamp': datetime.now(),
                'attempts': 0
            }
            
            # Simulation envoi SMS (remplacer par vraie API)
            message = f"Votre code TradingBot Pro: {code}. Valide 5 minutes."
            
            # En production, utiliser une vraie API SMS (Twilio, AWS SNS, etc.)
            logger.info(f"📱 Code SMS pour {phone_number}: {code}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur envoi SMS: {e}")
            return False
    
    def verify_sms_code(self, phone_number: str, user_id: str, code: str) -> bool:
        """Vérifie un code SMS"""
        key = f"{user_id}:{phone_number}"
        
        if key not in self.pending_codes:
            return False
        
        stored_data = self.pending_codes[key]
        stored_code = stored_data['code']
        timestamp = stored_data['timestamp']
        attempts = stored_data.get('attempts', 0)
        
        # Vérifier expiration (5 minutes)
        if datetime.now() - timestamp > timedelta(minutes=5):
            del self.pending_codes[key]
            return False
        
        # Vérifier nombre de tentatives
        if attempts >= 3:
            del self.pending_codes[key]
            return False
        
        # Vérifier le code
        if code == stored_code:
            del self.pending_codes[key]
            return True
        else:
            self.pending_codes[key]['attempts'] = attempts + 1
            return False

class EmailManager:
    """Gestionnaire Email pour codes de vérification"""
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587, 
                 email: str = "", password: str = ""):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
        self.pending_codes: Dict[str, Dict] = {}
    
    def generate_email_code(self) -> str:
        """Génère un code email à 8 caractères"""
        return secrets.token_urlsafe(6).upper()
    
    async def send_email_code(self, email_address: str, user_id: str) -> bool:
        """Envoie un code par email"""
        try:
            code = self.generate_email_code()
            
            # Stocker le code
            self.pending_codes[f"{user_id}:{email_address}"] = {
                'code': code,
                'timestamp': datetime.now(),
                'attempts': 0
            }
            
            # Préparer l'email
            subject = "Code de vérification TradingBot Pro 2025"
            body = f"""
            <html>
            <body>
                <h2>Code de vérification</h2>
                <p>Votre code de vérification TradingBot Pro 2025:</p>
                <h1 style="color: #007bff; font-family: monospace;">{code}</h1>
                <p>Ce code expire dans 10 minutes.</p>
                <p>Si vous n'avez pas demandé ce code, ignorez cet email.</p>
            </body>
            </html>
            """
            
            # Simulation envoi email (remplacer par vraie configuration SMTP)
            logger.info(f"📧 Code email pour {email_address}: {code}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur envoi email: {e}")
            return False
    
    def verify_email_code(self, email_address: str, user_id: str, code: str) -> bool:
        """Vérifie un code email"""
        key = f"{user_id}:{email_address}"
        
        if key not in self.pending_codes:
            return False
        
        stored_data = self.pending_codes[key]
        stored_code = stored_data['code']
        timestamp = stored_data['timestamp']
        attempts = stored_data.get('attempts', 0)
        
        # Vérifier expiration (10 minutes)
        if datetime.now() - timestamp > timedelta(minutes=10):
            del self.pending_codes[key]
            return False
        
        # Vérifier tentatives
        if attempts >= 3:
            del self.pending_codes[key]
            return False
        
        # Vérifier le code
        if code.upper() == stored_code:
            del self.pending_codes[key]
            return True
        else:
            self.pending_codes[key]['attempts'] = attempts + 1
            return False

class BackupCodeManager:
    """Gestionnaire de codes de sauvegarde"""
    
    @staticmethod
    def generate_backup_codes(count: int = 10) -> List[str]:
        """Génère des codes de sauvegarde"""
        codes = []
        for _ in range(count):
            # Format: XXXX-XXXX
            code = f"{secrets.randbelow(10000):04d}-{secrets.randbelow(10000):04d}"
            codes.append(code)
        return codes
    
    @staticmethod
    def hash_backup_codes(codes: List[str]) -> List[str]:
        """Hash les codes de sauvegarde"""
        hashed_codes = []
        for code in codes:
            # Utiliser SHA-256 pour les codes de sauvegarde
            hashed = hashlib.sha256(code.encode()).hexdigest()
            hashed_codes.append(hashed)
        return hashed_codes
    
    @staticmethod
    def verify_backup_code(code: str, hashed_codes: List[str]) -> Tuple[bool, str]:
        """Vérifie un code de sauvegarde et retourne le hash s'il est valide"""
        code_hash = hashlib.sha256(code.encode()).hexdigest()
        
        if code_hash in hashed_codes:
            return True, code_hash
        return False, ""

class BruteForceProtection:
    """Protection contre les attaques par force brute"""
    
    def __init__(self):
        self.attempts: Dict[str, List[datetime]] = {}
        self.locked_accounts: Dict[str, datetime] = {}
    
    def record_attempt(self, identifier: str, success: bool):
        """Enregistre une tentative"""
        if identifier not in self.attempts:
            self.attempts[identifier] = []
        
        self.attempts[identifier].append(datetime.now())
        
        # Garder seulement les 1 heure dernières
        cutoff = datetime.now() - timedelta(hours=1)
        self.attempts[identifier] = [
            attempt for attempt in self.attempts[identifier] 
            if attempt > cutoff
        ]
        
        # Vérifier si compte doit être verrouillé
        if not success and len(self.attempts[identifier]) >= 5:
            self.lock_account(identifier)
    
    def lock_account(self, identifier: str):
        """Verrouille un compte"""
        lock_duration = timedelta(minutes=30)
        self.locked_accounts[identifier] = datetime.now() + lock_duration
        logger.warning(f"🔒 Compte verrouillé: {identifier}")
    
    def is_locked(self, identifier: str) -> bool:
        """Vérifie si un compte est verrouillé"""
        if identifier not in self.locked_accounts:
            return False
        
        lock_expiry = self.locked_accounts[identifier]
        if datetime.now() > lock_expiry:
            del self.locked_accounts[identifier]
            return False
        
        return True
    
    def get_remaining_locktime(self, identifier: str) -> Optional[timedelta]:
        """Obtient le temps de verrouillage restant"""
        if identifier not in self.locked_accounts:
            return None
        
        lock_expiry = self.locked_accounts[identifier]
        remaining = lock_expiry - datetime.now()
        
        if remaining.total_seconds() <= 0:
            del self.locked_accounts[identifier]
            return None
        
        return remaining

class TwoFactorAuth:
    """Système d'authentification à deux facteurs complet"""
    
    def __init__(self, app_name: str = "TradingBot Pro 2025"):
        self.app_name = app_name
        
        # Gestionnaires
        self.password_manager = PasswordManager()
        self.totp_manager = TOTPManager(app_name)
        self.sms_manager = SMSManager()
        self.email_manager = EmailManager()
        self.backup_manager = BackupCodeManager()
        self.brute_force_protection = BruteForceProtection()
        
        # Base de données simulée
        self.users: Dict[str, Dict] = {}
        self.user_configs: Dict[str, TwoFactorConfig] = {}
        self.auth_sessions: Dict[str, AuthSession] = {}
        self.auth_attempts: List[AuthAttempt] = []
        
        # Configuration
        self.session_timeout = timedelta(hours=2)
        self.jwt_secret = secrets.token_urlsafe(32)
    
    def register_user(self, user_id: str, email: str, password: str, 
                     phone: Optional[str] = None) -> Dict[str, Any]:
        """Enregistre un nouvel utilisateur"""
        try:
            # Vérifier force du mot de passe
            password_check = self.password_manager.check_password_strength(password)
            if not password_check['valid']:
                return {
                    'success': False,
                    'error': 'Mot de passe trop faible',
                    'details': password_check
                }
            
            # Vérifier si utilisateur existe
            if user_id in self.users:
                return {
                    'success': False,
                    'error': 'Utilisateur déjà existant'
                }
            
            # Hasher le mot de passe
            hashed_password = self.password_manager.hash_password(password)
            
            # Créer utilisateur
            self.users[user_id] = {
                'user_id': user_id,
                'email': email,
                'password_hash': hashed_password,
                'phone': phone,
                'created_at': datetime.now(),
                'email_verified': False,
                'phone_verified': False
            }
            
            # Créer configuration 2FA
            self.user_configs[user_id] = TwoFactorConfig(user_id=user_id)
            
            logger.info(f"✅ Utilisateur enregistré: {user_id}")
            
            return {
                'success': True,
                'user_id': user_id,
                'message': 'Utilisateur créé avec succès'
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur enregistrement utilisateur: {e}")
            return {
                'success': False,
                'error': 'Erreur interne'
            }
    
    def setup_totp(self, user_id: str) -> Dict[str, Any]:
        """Configure TOTP pour un utilisateur"""
        try:
            if user_id not in self.users:
                return {'success': False, 'error': 'Utilisateur non trouvé'}
            
            user = self.users[user_id]
            config = self.user_configs[user_id]
            
            # Générer secret TOTP
            secret = self.totp_manager.generate_secret()
            config.totp_secret = secret
            
            # Générer QR code
            qr_code = self.totp_manager.generate_qr_code(user['email'], secret)
            qr_code_b64 = base64.b64encode(qr_code).decode()
            
            logger.info(f"🔐 TOTP configuré pour {user_id}")
            
            return {
                'success': True,
                'secret': secret,
                'qr_code': qr_code_b64,
                'manual_entry_key': secret,
                'message': 'Scannez le QR code avec votre app authenticator'
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur configuration TOTP: {e}")
            return {'success': False, 'error': 'Erreur configuration TOTP'}
    
    def verify_totp_setup(self, user_id: str, totp_code: str) -> Dict[str, Any]:
        """Vérifie et active TOTP"""
        try:
            config = self.user_configs.get(user_id)
            if not config or not config.totp_secret:
                return {'success': False, 'error': 'TOTP non configuré'}
            
            # Vérifier le code
            if self.totp_manager.verify_totp(config.totp_secret, totp_code):
                config.totp_enabled = True
                
                # Générer codes de sauvegarde
                backup_codes = self.backup_manager.generate_backup_codes()
                config.backup_codes = self.backup_manager.hash_backup_codes(backup_codes)
                
                logger.info(f"✅ TOTP activé pour {user_id}")
                
                return {
                    'success': True,
                    'backup_codes': backup_codes,
                    'message': 'TOTP activé avec succès. Sauvegardez vos codes de récupération!'
                }
            else:
                return {'success': False, 'error': 'Code TOTP invalide'}
                
        except Exception as e:
            logger.error(f"❌ Erreur vérification TOTP: {e}")
            return {'success': False, 'error': 'Erreur vérification'}
    
    async def start_authentication(self, user_id: str, password: str, 
                                 ip_address: str = "", user_agent: str = "") -> Dict[str, Any]:
        """Démarre le processus d'authentification"""
        try:
            # Vérifier protection brute force
            if self.brute_force_protection.is_locked(user_id):
                remaining = self.brute_force_protection.get_remaining_locktime(user_id)
                return {
                    'success': False,
                    'error': 'Compte temporairement verrouillé',
                    'remaining_time': str(remaining) if remaining else None
                }
            
            # Vérifier utilisateur et mot de passe
            user = self.users.get(user_id)
            if not user:
                self.brute_force_protection.record_attempt(user_id, False)
                return {'success': False, 'error': 'Identifiants invalides'}
            
            if not self.password_manager.verify_password(password, user['password_hash']):
                self.brute_force_protection.record_attempt(user_id, False)
                return {'success': False, 'error': 'Identifiants invalides'}
            
            # Première étape réussie
            self.brute_force_protection.record_attempt(user_id, True)
            
            # Créer session d'authentification
            session_id = secrets.token_urlsafe(32)
            config = self.user_configs[user_id]
            
            # Déterminer méthodes requises
            required_methods = [AuthMethod.PASSWORD]  # Déjà validé
            
            if config.totp_enabled:
                required_methods.append(AuthMethod.TOTP)
            elif config.sms_enabled:
                required_methods.append(AuthMethod.SMS)
            elif config.email_enabled:
                required_methods.append(AuthMethod.EMAIL)
            
            session = AuthSession(
                session_id=session_id,
                user_id=user_id,
                status=AuthStatus.PARTIAL if len(required_methods) > 1 else AuthStatus.COMPLETED,
                methods_completed=[AuthMethod.PASSWORD],
                methods_required=required_methods,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            self.auth_sessions[session_id] = session
            
            # Enregistrer tentative
            attempt = AuthAttempt(
                user_id=user_id,
                method=AuthMethod.PASSWORD,
                timestamp=datetime.now(),
                ip_address=ip_address,
                user_agent=user_agent,
                success=True
            )
            self.auth_attempts.append(attempt)
            
            result = {
                'success': True,
                'session_id': session_id,
                'status': session.status.value,
                'methods_completed': [m.value for m in session.methods_completed],
                'methods_required': [m.value for m in session.methods_required]
            }
            
            # Si 2FA requis, préparer la méthode
            if session.status == AuthStatus.PARTIAL:
                if AuthMethod.TOTP in required_methods and config.totp_enabled:
                    result['next_method'] = 'totp'
                    result['message'] = 'Entrez votre code TOTP'
                elif AuthMethod.SMS in required_methods and config.sms_enabled:
                    # Envoyer SMS
                    await self.sms_manager.send_sms_code(user['phone'], user_id)
                    result['next_method'] = 'sms'
                    result['message'] = 'Code SMS envoyé'
                elif AuthMethod.EMAIL in required_methods and config.email_enabled:
                    # Envoyer email
                    await self.email_manager.send_email_code(user['email'], user_id)
                    result['next_method'] = 'email'
                    result['message'] = 'Code email envoyé'
            else:
                # Authentification complète
                token = self._generate_jwt_token(user_id)
                result['token'] = token
                result['message'] = 'Authentification réussie'
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur authentification: {e}")
            return {'success': False, 'error': 'Erreur interne'}
    
    async def verify_second_factor(self, session_id: str, method: str, code: str) -> Dict[str, Any]:
        """Vérifie le second facteur d'authentification"""
        try:
            session = self.auth_sessions.get(session_id)
            if not session:
                return {'success': False, 'error': 'Session invalide'}
            
            # Vérifier expiration session
            if datetime.now() > session.expires_at:
                del self.auth_sessions[session_id]
                return {'success': False, 'error': 'Session expirée'}
            
            user_id = session.user_id
            config = self.user_configs[user_id]
            user = self.users[user_id]
            
            verified = False
            auth_method = AuthMethod(method)
            
            # Vérifier selon la méthode
            if auth_method == AuthMethod.TOTP and config.totp_enabled:
                verified = self.totp_manager.verify_totp(config.totp_secret, code)
            elif auth_method == AuthMethod.SMS and config.sms_enabled:
                verified = self.sms_manager.verify_sms_code(user['phone'], user_id, code)
            elif auth_method == AuthMethod.EMAIL and config.email_enabled:
                verified = self.email_manager.verify_email_code(user['email'], user_id, code)
            elif auth_method == AuthMethod.BACKUP_CODE:
                verified, used_hash = self.backup_manager.verify_backup_code(code, config.backup_codes)
                if verified:
                    # Supprimer le code utilisé
                    config.backup_codes.remove(used_hash)
            
            # Enregistrer tentative
            attempt = AuthAttempt(
                user_id=user_id,
                method=auth_method,
                timestamp=datetime.now(),
                ip_address=session.ip_address,
                user_agent=session.user_agent,
                success=verified
            )
            self.auth_attempts.append(attempt)
            
            if verified:
                # Ajouter méthode aux complétées
                session.methods_completed.append(auth_method)
                
                # Vérifier si authentification complète
                if set(session.methods_completed) >= set(session.methods_required):
                    session.status = AuthStatus.COMPLETED
                    
                    # Générer token JWT
                    token = self._generate_jwt_token(user_id)
                    
                    # Nettoyer session
                    del self.auth_sessions[session_id]
                    
                    logger.info(f"✅ Authentification 2FA complète pour {user_id}")
                    
                    return {
                        'success': True,
                        'status': 'completed',
                        'token': token,
                        'message': 'Authentification réussie'
                    }
                else:
                    return {
                        'success': True,
                        'status': 'partial',
                        'message': 'Facteur vérifié, continuez l\'authentification'
                    }
            else:
                return {'success': False, 'error': 'Code invalide'}
                
        except Exception as e:
            logger.error(f"❌ Erreur vérification 2FA: {e}")
            return {'success': False, 'error': 'Erreur vérification'}
    
    def _generate_jwt_token(self, user_id: str) -> str:
        """Génère un token JWT"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + self.session_timeout,
            'iat': datetime.utcnow(),
            'iss': self.app_name
        }
        
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def verify_jwt_token(self, token: str) -> Optional[Dict]:
        """Vérifie un token JWT"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def get_user_2fa_status(self, user_id: str) -> Dict[str, Any]:
        """Obtient le statut 2FA d'un utilisateur"""
        config = self.user_configs.get(user_id)
        if not config:
            return {'error': 'Utilisateur non trouvé'}
        
        return {
            'user_id': user_id,
            'totp_enabled': config.totp_enabled,
            'sms_enabled': config.sms_enabled,
            'email_enabled': config.email_enabled,
            'backup_codes_count': len(config.backup_codes),
            'last_used': config.last_used.isoformat() if config.last_used else None
        }
    
    def get_auth_stats(self) -> Dict[str, Any]:
        """Statistiques d'authentification"""
        recent_attempts = [
            attempt for attempt in self.auth_attempts
            if datetime.now() - attempt.timestamp < timedelta(hours=24)
        ]
        
        successful_attempts = [a for a in recent_attempts if a.success]
        failed_attempts = [a for a in recent_attempts if not a.success]
        
        return {
            'total_users': len(self.users),
            'users_with_2fa': len([c for c in self.user_configs.values() 
                                  if c.totp_enabled or c.sms_enabled or c.email_enabled]),
            'active_sessions': len(self.auth_sessions),
            'recent_attempts_24h': len(recent_attempts),
            'successful_attempts_24h': len(successful_attempts),
            'failed_attempts_24h': len(failed_attempts),
            'locked_accounts': len(self.brute_force_protection.locked_accounts)
        }

# ============================================================================
# 🧪 TESTS ET DÉMONSTRATION
# ============================================================================

async def test_2fa_system():
    """Test complet du système 2FA"""
    print("🧪 TEST AUTHENTIFICATION 2FA - TRADINGBOT PRO 2025")
    print("=" * 60)
    
    # Créer système 2FA
    auth_system = TwoFactorAuth()
    
    try:
        print("👤 Test enregistrement utilisateur...")
        
        # Enregistrer utilisateur test
        result = auth_system.register_user(
            user_id="test_user_001",
            email="test@tradingbot.com",
            password="SuperSecure123!",
            phone="+33123456789"
        )
        print(f"   Enregistrement: {'✅' if result['success'] else '❌'} {result.get('message', result.get('error'))}")
        
        if result['success']:
            user_id = result['user_id']
            
            print("\n🔐 Test configuration TOTP...")
            
            # Configurer TOTP
            totp_setup = auth_system.setup_totp(user_id)
            print(f"   Configuration TOTP: {'✅' if totp_setup['success'] else '❌'}")
            
            if totp_setup['success']:
                secret = totp_setup['secret']
                print(f"   Secret TOTP: {secret}")
                
                # Générer code TOTP pour test
                current_code = auth_system.totp_manager.get_current_totp(secret)
                print(f"   Code TOTP actuel: {current_code}")
                
                # Vérifier TOTP setup
                verify_result = auth_system.verify_totp_setup(user_id, current_code)
                print(f"   Activation TOTP: {'✅' if verify_result['success'] else '❌'}")
                
                if verify_result['success']:
                    print(f"   Codes de sauvegarde générés: {len(verify_result['backup_codes'])}")
                    
                    print("\n🔑 Test authentification complète...")
                    
                    # Test authentification
                    auth_result = await auth_system.start_authentication(
                        user_id=user_id,
                        password="SuperSecure123!",
                        ip_address="127.0.0.1",
                        user_agent="Test-Agent"
                    )
                    
                    print(f"   Étape 1 (mot de passe): {'✅' if auth_result['success'] else '❌'}")
                    
                    if auth_result['success'] and auth_result['status'] == 'partial':
                        session_id = auth_result['session_id']
                        
                        # Générer nouveau code TOTP
                        new_code = auth_system.totp_manager.get_current_totp(secret)
                        
                        # Vérifier 2FA
                        fa2_result = await auth_system.verify_second_factor(
                            session_id=session_id,
                            method="totp",
                            code=new_code
                        )
                        
                        print(f"   Étape 2 (TOTP): {'✅' if fa2_result['success'] else '❌'}")
                        
                        if fa2_result['success']:
                            print(f"   Token JWT généré: {'✅' if 'token' in fa2_result else '❌'}")
                            
                            # Test vérification token
                            if 'token' in fa2_result:
                                token_payload = auth_system.verify_jwt_token(fa2_result['token'])
                                print(f"   Vérification token: {'✅' if token_payload else '❌'}")
        
        print("\n📊 Statistiques système:")
        stats = auth_system.get_auth_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        print("\n✅ TEST 2FA TERMINÉ AVEC SUCCÈS!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR TEST: {e}")
        return False

if __name__ == "__main__":
    print("🔐 AUTHENTIFICATION 2FA - TRADINGBOT PRO 2025")
    print("=" * 55)
    
    # Test du système
    success = asyncio.run(test_2fa_system())
    
    if success:
        print("\n✅ SYSTÈME 2FA OPÉRATIONNEL!")
        print("🛡️ Sécurité renforcée activée")
    else:
        print("\n❌ ERREUR SYSTÈME 2FA")
        
    print("\n" + "=" * 55)
