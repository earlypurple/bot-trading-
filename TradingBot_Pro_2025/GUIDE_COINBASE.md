📋 GUIDE CONFIGURATION COINBASE API
===================================

🔧 ÉTAPES POUR CORRIGER TES CLÉS API
====================================

1. 🌐 VA SUR COINBASE
   → Connecte-toi sur coinbase.com
   → Settings > API (ou Advanced Trade > API Keys)

2. 🔑 TYPE DE CLÉS À CRÉER
   ✅ "Cloud Trading Keys" (recommandé)
   ❌ PAS "Legacy API Keys"
   
3. 📋 PERMISSIONS REQUISES
   ✅ Read (lecture des données)
   ✅ Trade (passage d'ordres)
   ❌ Transfer (pas nécessaire pour le trading)

4. 🌍 IP WHITELIST
   → Autoriser TOUTES les IPs: 0.0.0.0/0
   → Ou ton IP actuelle: 31.34.180.33

5. 📱 FORMAT ATTENDU
   • API Key: Format UUID (ex: a199253a-1f20-4347-a42a-80480aa683d9)
   • Private Key: Format PEM EC (commence par -----BEGIN EC PRIVATE KEY-----)

🔍 VÉRIFICATION DE TES CLÉS ACTUELLES
====================================

Problèmes détectés:
❌ Toutes tes clés renvoient "401 Unauthorized"
❌ L'API Advanced Trade est inaccessible
❌ Permissions insuffisantes ou clés incorrectes

Solutions:
1. 🔄 Créer de nouvelles clés "Cloud Trading"
2. ✅ Vérifier les permissions (Read + Trade)
3. 🌍 Autoriser ton IP (31.34.180.33)
4. ⏰ Attendre quelques minutes après création

🚀 MODES DISPONIBLES MAINTENANT
===============================

Mode DÉMO (actuel):
• ✅ Prix réels Coinbase (API publique)
• ✅ Portfolio simulé réaliste
• ✅ Interface complète
• ✅ Aucune authentification requise

Mode LIVE (après correction):
• 🔐 Authentification avec tes vraies clés
• 💰 Ton vrai portfolio Coinbase
• 📊 Trading automatique possible
• 💹 Données de trading en temps réel

📞 SUPPORT COINBASE
==================

Si problème persiste:
• 💬 Support Coinbase: help.coinbase.com
• 📧 Ticket de support avec tes IDs de clés
• 🔍 Vérifier l'état des services: status.coinbase.com

🎯 PROCHAINES ÉTAPES
===================

1. 📺 Lance le dashboard démo:
   python3 dashboard_demo.py

2. 🔧 Configure tes nouvelles clés API

3. 🔄 Relance le diagnostic:
   python3 diagnostic_coinbase_detail.py

4. 🚀 Passe en mode LIVE!
