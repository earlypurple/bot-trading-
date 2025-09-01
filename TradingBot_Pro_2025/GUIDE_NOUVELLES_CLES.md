# 🔑 GUIDE CRÉATION NOUVELLES CLÉS API COINBASE

## 🎯 ÉTAPES RECOMMANDÉES

### 1. 🌐 Sur coinbase.com
1. **Se connecter** à ton compte Coinbase
2. **Settings** → **API** 
3. **Supprimer les anciennes clés** (optionnel mais recommandé)
4. **Create New API Key**

### 2. 🎛️ CONFIGURATION RECOMMANDÉE

#### Type de clés à choisir :
- ✅ **Cloud Trading API** (recommandé)
- ❌ Éviter "Advanced Trade" (problèmes d'auth)
- ❌ Éviter "Legacy API"

#### Permissions à cocher :
- ✅ **View** - Lecture des données de compte
- ✅ **Trade** - Passage d'ordres de trading
- ❌ **Transfer** - Pas nécessaire (peut créer des complications)

#### Configuration réseau :
- 🌍 **IP Whitelist** : `0.0.0.0/0` (accès depuis n'importe où)
- 🔒 **Restrictions géographiques** : Aucune

#### Paramètres avancés :
- ⏰ **Expiration** : 1 an ou "Never" si disponible
- 🔐 **Two-Factor** : Activé pour la création mais pas pour l'usage

### 3. 📋 INFORMATIONS À RÉCUPÉRER

Tu vas obtenir **3 éléments** :
1. **API Key** (format UUID : `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)
2. **API Secret** (chaîne longue, souvent en base64)
3. **Passphrase** (phrase que tu choisis ou générée)

### 4. 🔍 POINTS D'ATTENTION

#### Format attendu :
```
API Key: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Secret: base64_encoded_string_very_long
Passphrase: your_chosen_passphrase
```

#### Types de clés à éviter :
- ❌ Clés "Advanced Trade" uniquement
- ❌ Clés avec restrictions IP trop strictes
- ❌ Clés sans permission "Trade"

### 5. ⚡ TEST IMMÉDIAT

Dès que tu as tes nouvelles clés, copie-colle les **3 éléments** et on les testera avec notre **testeur automatique** qui vérifiera :

- ✅ Format des clés
- ✅ Authentification
- ✅ Accès aux comptes
- ✅ Permissions de trading
- ✅ Calcul de la valeur du portfolio

### 6. 🚀 INTÉGRATION AUTOMATIQUE

Si les tests passent, l'intégration dans le dashboard sera **automatique** :
- 📊 Portfolio temps réel
- 💰 Vraies données de trading
- 🔄 Synchronisation live
- 📈 Historique des trades

---

## 🎯 OBJECTIF
Une fois les nouvelles clés créées et testées, tu auras un **dashboard live complet** avec tes vraies données Coinbase ! 🚀
