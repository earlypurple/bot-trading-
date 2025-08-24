# 🔧 SOLUTION PROBLÈME API COINBASE

## 🎯 Problème Identifié
- Clés API actives mais permissions insuffisantes
- Endpoints publics ✅ / Endpoints privés ❌

## 📋 ÉTAPES DE RÉSOLUTION

### 1. Vérifier les Permissions Coinbase
Sur coinbase.com → Settings → API :
- ✅ **View** (Lecture des données)
- ✅ **Trade** (Passage d'ordres)
- 🌍 **IP Whitelist**: `0.0.0.0/0` ou ton IP spécifique

### 2. Créer de Nouvelles Clés
Si les permissions sont correctes :
- Supprimer les anciennes clés
- Créer de nouvelles clés avec permissions complètes
- Attendre 10-15 minutes avant test

### 3. Solutions de Continuité
En attendant la résolution :

#### 📊 Dashboard DÉMO (Fonctionnel)
```bash
python dashboard_demo.py
```
- Port 8888
- Prix réels Coinbase
- Portfolio simulé

#### 🔄 Smart Launcher (Auto-switch)
```bash
python smart_launcher.py
```
- Détecte automatiquement quand l'API fonctionne
- Bascule auto entre démo et live

## 🕐 Timeline Prévue
- **Immédiat** : Dashboard démo opérationnel
- **15 minutes** : Nouvelles clés testées
- **24h maximum** : Problème résolu

## 📞 Support
Si rien ne fonctionne après 24h :
- Contacter Coinbase Support
- Mentionner : "API keys work on website but return 401 via API"
