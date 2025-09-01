# 🤖 IA Trading Bot - Version Propre

## 📁 Structure du Projet

```
IA_Trading_Clean/
├── launch_bot.py          # 🚀 Lanceur principal
├── config/
│   └── api_config.py      # 🔐 Configuration API & Trading
├── bot/
│   └── ai_trading_bot.py  # 🤖 Bot IA avec interface web
└── README.md              # 📖 Ce fichier
```

## ✅ Fonctionnalités

### 🔧 **Configuration Centralisée**
- Clés API Coinbase fonctionnelles
- Paramètres de trading configurables
- Stop Loss : 3% | Take Profit : 5%
- Position max : 2% du portfolio

### 🤖 **Intelligence Artificielle**
- Analyse RSI (14 périodes)
- MACD (12/26/9)
- Bollinger Bands (20 périodes)
- Signaux automatiques BUY/SELL/HOLD

### 📊 **Interface Web Complète**
- Dashboard temps réel
- Paramètres visibles
- Contrôles Start/Stop
- Notifications WebSocket
- Statistiques en direct

### 💰 **Trading Sécurisé**
- Mode simulation intégré
- Gestion des risques
- Historique des trades
- Portfolio tracking

## 🚀 Utilisation

### Lancement Simple
```bash
cd IA_Trading_Clean
python3 launch_bot.py
```

### Interface Web
- URL: http://localhost:8090
- Contrôles: START/STOP Trading
- Monitoring temps réel

## 📊 Paramètres de Trading

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| Max Position | 2% | % max du portfolio par trade |
| Stop Loss | 3% | Perte maximale acceptable |
| Take Profit | 5% | Objectif de profit |
| RSI Période | 14 | Période pour calcul RSI |
| RSI Survente | 30 | Seuil d'achat RSI |
| RSI Surachat | 70 | Seuil de vente RSI |
| MACD Rapide | 12 | EMA rapide MACD |
| MACD Lent | 26 | EMA lente MACD |
| Bollinger | 20 | Période Bollinger Bands |
| Intervalle | 30s | Temps entre analyses |

## 🎯 Symboles Tradés

- **BTC/USD** - Bitcoin
- **ETH/USD** - Ethereum  
- **SOL/USD** - Solana

## 🔒 Sécurité

- Clés API chiffrées
- Mode sandbox disponible
- Simulation avant trading réel
- Arrêt d'urgence intégré

## 📈 Monitoring

- Portfolio balance en temps réel
- Signaux de trading visuels
- Statistiques de performance
- Historique des trades

---

**✅ Version Nettoyée - Tous les fichiers inutiles supprimés**
**🤖 Bot IA Optimisé avec Interface Web Complète**
