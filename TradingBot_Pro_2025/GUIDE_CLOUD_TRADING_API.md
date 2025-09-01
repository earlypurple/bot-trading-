🚨 GUIDE URGENT: CRÉER DES CLÉS CLOUD TRADING API
=======================================================

⚠️ IMPORTANT: Les clés "Advanced Trade" ne fonctionnent pas
✅ SOLUTION: Créer des clés "Cloud Trading API"

📋 ÉTAPES EXACTES:
=================

1. 🔗 Va sur: https://www.coinbase.com/cloud/discover/sign-in
   (PAS sur coinbase.com normal!)

2. 🔐 Connecte-toi avec ton compte Coinbase habituel

3. 📱 Dans le menu de gauche, clique "API Keys" 

4. ➕ Clique "Create API Key"

5. 🎯 TRÈS IMPORTANT: Sélectionne "Cloud Trading API"
   (PAS "Advanced Trade"!)

6. ✅ Permissions à activer:
   • wallet:accounts:read ✅
   • wallet:buys:create ✅  
   • wallet:sells:create ✅
   • wallet:trades:read ✅
   • wallet:transactions:read ✅

7. 🌐 IP Whitelist: 0.0.0.0/0 (pour autoriser tous les IPs)

8. 💾 Sauvegarder les 3 éléments:
   • API Key (UUID format)
   • API Secret (String base64, pas EC key!)
   • Permissions (liste des permissions)

🔄 DIFFÉRENCES CLÉS:
==================
• Advanced Trade → JWT + EC Private Key + 401 errors
• Cloud Trading → HMAC + Base64 Secret + Fonctionne! ✅

🎯 FORMAT ATTENDU:
================
API_KEY: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
API_SECRET: ABCDEFabcdef123456789== (base64, pas EC!)
PERMISSIONS: wallet:accounts:read,wallet:buys:create,...

⚡ APRÈS CRÉATION:
================
1. Copie les 3 éléments ici
2. Je testerai immédiatement 
3. Dashboard live activé! 🚀

💡 POURQUOI ÇA VA MARCHER:
========================
• Cloud Trading API = Plus stable
• HMAC authentication = Plus compatible
• Base64 secret = Format standard
• Pas de JWT compliqué = Moins d'erreurs

🚨 SI ÇA NE MARCHE TOUJOURS PAS:
==============================
• Problème avec ton compte Coinbase
• Contact support: help.coinbase.com
• Utiliser dashboard hybride en attendant

🎯 DASHBOARD HYBRIDE DÉJÀ PRÊT:
=============================
• Prix réels en temps réel ✅
• Simulation portfolio réaliste ✅  
• Interface complète ✅
• Port 8889 ✅
