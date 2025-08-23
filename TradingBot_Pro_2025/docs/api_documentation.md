# TradingBot Pro 2025 - Documentation API

## Vue d'ensemble

L'API TradingBot Pro 2025 fournit une interface REST complète pour contrôler et surveiller le système de trading algorithmique. Cette API permet de gérer les stratégies, surveiller les risques, et recevoir des notifications en temps réel.

## URL de base

```
http://localhost:5000/api
```

## Authentification

Actuellement, l'API ne nécessite pas d'authentification. En production, il est recommandé d'implémenter l'authentification JWT.

## Endpoints

### 1. Santé du système

#### GET `/health`
Vérification de l'état de santé du système.

**Réponse :**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-23T10:30:00Z",
  "version": "0.2.0"
}
```

### 2. Statut du bot

#### GET `/status`
Récupère le statut général du bot de trading.

**Réponse :**
```json
{
  "bot_status": {
    "status": "ON|OFF",
    "active_strategies": []
  },
  "daily_capital": {
    "amount": 1000.0
  },
  "risk_metrics": {
    "daily_pnl": 0.0,
    "daily_trades": 0,
    "portfolio_value": 1000.0,
    "var_95": 0.0,
    "sharpe_ratio": 0.0,
    "position_count": 0,
    "max_position_value": 0.0
  },
  "emergency_stop": false,
  "timestamp": "2025-08-23T10:30:00Z"
}
```

## Exemples d'utilisation

### Python
```python
import requests

# Vérifier le statut
response = requests.get('http://localhost:5000/api/status')
status = response.json()
print(f"Bot status: {status['bot_status']['status']}")
```

## Sécurité

### Recommandations de production

1. **Authentification :** Implémenter JWT ou API keys
2. **HTTPS :** Utiliser uniquement HTTPS en production
3. **CORS :** Configurer CORS pour les domaines autorisés
