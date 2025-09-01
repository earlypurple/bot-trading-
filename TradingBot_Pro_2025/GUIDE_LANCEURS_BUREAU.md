# 🚀 GUIDE D'UTILISATION - LANCEURS BUREAU

## 📁 Fichiers Créés sur le Bureau

### 1. **LANCER_BOT_TRADING_BUREAU.command**
- 🎯 **Version :** Bot Corrigé (avec diagnostic d'erreur)
- 🌐 **Dashboard :** http://localhost:8087
- 🔧 **Fonction :** Version avec corrections pour l'erreur "account not available"

### 2. **LANCER_BOT_AVANCE_BUREAU.command**
- 🎯 **Version :** Bot Avancé Original
- 🌐 **Dashboard :** http://localhost:8085
- 🔧 **Fonction :** Version complète avec toutes les fonctionnalités

## 🎯 Comment Utiliser

### Étape 1: Double-Cliquer
1. Double-cliquez sur l'un des fichiers `.command` sur votre bureau
2. Le Terminal s'ouvrira automatiquement
3. Le bot se lancera et vérifiera tous les fichiers nécessaires

### Étape 2: Accès Dashboard
- Le navigateur s'ouvrira automatiquement après 3 secondes
- Vous accéderez directement au dashboard de trading
- Interface moderne avec tous les contrôles

### Étape 3: Trading
- Choisissez votre mode de trading (micro → agressif)
- Activez l'auto-trading si désiré
- Surveillez les logs en temps réel

## ⚠️ Résolution de l'Erreur "account is not available"

### Cause
Les fonds USDC sont dans votre portefeuille principal Coinbase, mais pas dans Advanced Trade.

### Solution Simple
1. **Connectez-vous sur Coinbase.com**
2. **Allez dans Portfolio → Advanced Trade**
3. **Transférez des USDC** depuis votre portefeuille principal vers Advanced Trade
4. **Relancez le bot** - le trading fonctionnera immédiatement

## 🎯 Modes de Trading Disponibles

| Mode | Montant | Fréquence | Risque | Objectif |
|------|---------|-----------|---------|----------|
| **Micro** | $1-3 | 15 min | Très Faible | Sécurité maximale |
| **Conservateur** | $2-5 | 10 min | Faible | Trading prudent |
| **Équilibré** | $3-8 | 5 min | Modéré | Balance profit/risque |
| **Dynamique** | $5-12 | 3 min | Élevé | Trading actif |
| **Agressif** | $8-20 | 2 min | Très Élevé | Profit maximum |

## 🔄 Arrêter le Bot

### Méthode 1: Terminal
- Appuyez `Ctrl+C` dans la fenêtre Terminal
- Le bot s'arrêtera proprement

### Méthode 2: Fermer la Fenêtre
- Fermez simplement la fenêtre Terminal
- Tous les logs seront sauvegardés

## 📊 Fonctionnalités Dashboard

### Interface Principale
- **Portfolio en temps réel** - Vos actifs actuels
- **Prix des cryptos** - Mise à jour automatique
- **Logs système** - Activité détaillée du bot
- **Statistiques** - Performance et profits

### Contrôles
- **Changement de mode** - Clic sur les boutons de mode
- **Trading manuel** - Ordres immédiats
- **Auto-trading** - Démarrage/arrêt automatique

### Surveillance
- **Trades en cours** - Suivi en temps réel
- **Historique** - Tous les trades effectués
- **Erreurs** - Diagnostic automatique

## 🔧 Dépannage

### Le bot ne démarre pas
1. Vérifiez que vous êtes dans le bon répertoire
2. Confirmez que tous les fichiers sont présents
3. Vérifiez l'environnement Python

### Dashboard inaccessible
1. Attendez quelques secondes après le lancement
2. Actualisez la page web
3. Vérifiez que le port n'est pas occupé

### Erreurs API
1. Vérifiez votre connexion internet
2. Confirmez les clés API Coinbase
3. Transférez des fonds vers Advanced Trade

## 🎯 Raccourcis Utiles

### Lancement Rapide
- **Bot Corrigé :** Double-clic → `LANCER_BOT_TRADING_BUREAU.command`
- **Bot Avancé :** Double-clic → `LANCER_BOT_AVANCE_BUREAU.command`

### Dashboards
- **Bot Corrigé :** http://localhost:8087
- **Bot Avancé :** http://localhost:8085

### Logs
- **Corrigé :** `TRADING_CORRECTED.log`
- **Avancé :** `TRADING_AVANCE.log`

---

## ✅ TOUT EST PRÊT !

Votre bot de trading est maintenant accessible depuis votre bureau. Double-cliquez et commencez à trader ! 🚀

**Note :** Pensez à transférer des USDC vers Advanced Trade pour activer le trading réel.
