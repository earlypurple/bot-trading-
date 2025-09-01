# 🔑 Guide de Configuration API Coinbase Advanced

## Étapes pour créer/vérifier vos clés API

### 1. Connexion à Coinbase Advanced
- Allez sur : https://www.coinbase.com/settings/api
- Connectez-vous avec vos identifiants Coinbase

### 2. Création d'une nouvelle clé API
1. Cliquez sur "Create API Key" ou "Nouvelle clé API"
2. **Nom** : TradingBot_Pro_2025
3. **Permissions requises** :
   - ✅ **View** (Lecture des comptes et soldes)
   - ✅ **Trade** (Passage d'ordres)
   - ✅ **Transfer** (Transferts entre comptes)

### 3. Configuration IP (Optionnel mais recommandé)
- Laissez vide pour autoriser tous les IPs
- Ou ajoutez votre IP actuel pour plus de sécurité

### 4. Récupération des informations
Après création, vous obtiendrez :
- **API Key** (Key publique)
- **API Secret** (Clé secrète - TRÈS IMPORTANTE)
- **Passphrase** (Phrase de passe - parfois optionnelle)

### 5. Configuration dans le bot
Utilisez le script `setup_api_config.py` pour configurer vos nouvelles clés :

```bash
python3 setup_api_config.py
```

## ⚠️ Points importants
1. **Ne partagez JAMAIS votre API Secret**
2. **Conservez la passphrase en sécurité**
3. **Testez les clés avec de petits montants d'abord**
4. **Les clés peuvent prendre quelques minutes à être actives**

## 🔍 Vérification des permissions
Vos clés doivent avoir accès à :
- Lecture du portefeuille (balance)
- Historique des transactions
- Passage d'ordres d'achat/vente
- Consultation des prix du marché

## 📞 Support
Si les problèmes persistent :
1. Vérifiez que votre compte Coinbase est vérifié
2. Assurez-vous que vous avez des fonds sur Coinbase Advanced
3. Contactez le support Coinbase si nécessaire

## 🧪 Test de vos nouvelles clés
Après configuration, testez avec :
```bash
python3 test_api_connections.py
```
