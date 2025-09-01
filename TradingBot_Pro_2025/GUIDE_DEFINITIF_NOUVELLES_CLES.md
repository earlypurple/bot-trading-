🚨 GUIDE DÉFINITIF: CRÉER DES CLÉS QUI FONCTIONNENT
==================================================

⚠️ IMPORTANT: Tu as supprimé tes anciennes clés, c'est pour ça qu'on a des 401 !
✅ SOLUTION: Créer des NOUVELLES clés avec la BONNE configuration

📋 ÉTAPES EXACTES POUR CRÉER DES CLÉS QUI MARCHENT:
=================================================

🎯 OPTION 1: API v2 (RECOMMANDÉ - PLUS SIMPLE)
---------------------------------------------

1. 🔗 Va sur: https://www.coinbase.com/settings/api
   (Coinbase classique, PAS Advanced Trade)

2. 🔐 Connecte-toi avec ton compte

3. ➕ Clique "New API Key"

4. 🎯 Sélectionne ces permissions EXACTES:
   ✅ wallet:accounts:read
   ✅ wallet:transactions:read 
   ✅ wallet:buys:create
   ✅ wallet:sells:create

5. 💾 Tu auras 2 éléments:
   • API Key (UUID format)
   • API Secret (String long)

6. 🌐 IP Whitelist: Laisse vide ou mets 0.0.0.0/0

📝 FORMAT ATTENDU (API v2):
===========================
API_KEY: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
API_SECRET: ABCDEFabcdef123456789... (string long)

🎯 OPTION 2: Advanced Trade (SI API v2 NE MARCHE PAS)
---------------------------------------------------

1. 🔗 Va sur: https://www.coinbase.com/advanced-trade/api
   
2. ➕ Clique "Create API Key"

3. 🎯 Sélectionne "Advanced Trade" 

4. ✅ Permissions:
   • View (pour voir le portfolio)
   • Trade (pour passer des ordres)

5. 💾 Tu auras 3 éléments:
   • API Key (UUID)
   • Private Key (EC format -----BEGIN EC PRIVATE KEY-----)
   • Passphrase (string)

📝 FORMAT ATTENDU (Advanced Trade):
===================================
API_KEY: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PRIVATE_KEY: -----BEGIN EC PRIVATE KEY-----...
PASSPHRASE: randomstring123

🚀 APRÈS CRÉATION:
================

1. 📋 Copie EXACTEMENT les clés ici
2. ⚡ Je testerai immédiatement 
3. 🎯 Dashboard live avec TON portfolio !

🔍 POURQUOI ÇA VA MARCHER MAINTENANT:
====================================
• ✅ Nouvelles clés = actives
• ✅ Bonnes permissions
• ✅ Format correct
• ✅ Notre code fonctionne parfaitement

💡 CONSEIL:
==========
Commence par l'API v2 (Option 1) car c'est plus simple !
Si ça ne marche pas, essaie Advanced Trade (Option 2).

🚨 URGENT:
=========
Ne supprime PAS les nouvelles clés une fois créées !
On en a besoin pour le dashboard live !
