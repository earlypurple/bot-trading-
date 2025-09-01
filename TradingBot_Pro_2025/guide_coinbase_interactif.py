#!/usr/bin/env python3
"""
🎯 GUIDE INTERACTIF COINBASE - TradingBot Pro 2025
=================================================
Guide étape par étape pour configurer les bonnes clés
"""

import webbrowser
import time

def guide_interactif():
    print("🎯 GUIDE INTERACTIF COINBASE CONFIGURATION")
    print("=" * 60)
    
    print("\n🔍 DIAGNOSTIC DE TON PROBLÈME")
    print("-" * 30)
    print("❌ Tu es actuellement sur : Coinbase Wallet")
    print("❌ Tu vois : 'Afficher, échanger, transférer'")
    print("❌ Résultat : Clés incompatibles avec le trading")
    
    print("\n✅ IL FAUT ALLER SUR LE VRAI COINBASE")
    print("-" * 30)
    print("🌐 URL correcte : https://coinbase.com")
    print("📊 Interface : Coinbase Exchange (trading)")
    print("🔑 Type de clés : Cloud Trading Keys")
    
    response = input("\n📱 Veux-tu que j'ouvre coinbase.com maintenant ? (o/n): ")
    if response.lower() in ['o', 'oui', 'y', 'yes']:
        print("🚀 Ouverture de coinbase.com...")
        webbrowser.open("https://coinbase.com")
        time.sleep(2)
    
    print("\n📋 ÉTAPES À SUIVRE SUR COINBASE.COM")
    print("=" * 50)
    
    etapes = [
        ("1. 🔐 Se connecter", "Utilise tes identifiants Coinbase"),
        ("2. 🚀 Activer Advanced Trade", "Menu 'Trade' → Accepter les conditions"),
        ("3. ⚙️ Aller dans Settings", "Cliquer sur la roue crantée en haut à droite"),
        ("4. 🔑 Section API", "Cliquer sur 'API' dans le menu Settings"),
        ("5. ➕ Créer une clé", "Bouton 'Create API Key'"),
        ("6. 🔧 Type de clé", "Sélectionner 'Cloud Trading Keys'"),
        ("7. ✅ Permissions", "Cocher 'Read' et 'Trade'"),
        ("8. 🌍 IP Whitelist", "Ajouter '0.0.0.0/0' ou ton IP"),
        ("9. 💾 Sauvegarder", "Noter la clé privée EC et l'API Key"),
        ("10. ⏰ Attendre", "5-15 minutes pour l'activation")
    ]
    
    for etape, description in etapes:
        print(f"\n{etape}")
        print(f"   📝 {description}")
        
        if "Settings" in etape:
            response = input("   ⏸️  Es-tu dans Settings ? (appuie sur Entrée pour continuer)")
        elif "API" in etape and "Section" in etape:
            response = input("   ⏸️  Vois-tu la section API ? (appuie sur Entrée pour continuer)")
        elif "Cloud Trading" in etape:
            response = input("   ⏸️  Vois-tu 'Cloud Trading Keys' ? (appuie sur Entrée pour continuer)")
    
    print("\n🎯 VÉRIFICATION FINALE")
    print("=" * 30)
    print("Tu dois avoir reçu :")
    print("🔑 API Key : Format UUID (ex: 03c9938e-5795-4c66-93e4-6fdef834fdbd)")
    print("🔒 Private Key : Format PEM EC (commence par -----BEGIN EC PRIVATE KEY-----)")
    
    print("\n📞 SI TU NE TROUVES PAS CES OPTIONS")
    print("=" * 40)
    print("💡 Raisons possibles :")
    print("   • Tu n'as pas activé Advanced Trade")
    print("   • Ton compte n'est pas vérifié")
    print("   • Tu es dans la mauvaise région")
    print("   • Tu utilises encore Coinbase Wallet")
    
    print("\n🆘 Solutions :")
    print("   • Contacter le support Coinbase")
    print("   • Chercher 'Advanced Trade' dans l'aide")
    print("   • Vérifier l'état de ton compte")
    
    print("\n🔄 APRÈS CRÉATION DES CLÉS")
    print("=" * 30)
    print("1. 📋 Copier les deux clés")
    print("2. 🔄 Les coller dans le système")
    print("3. ⏱️ Attendre l'activation")
    print("4. 🎉 Le dashboard basculera automatiquement en LIVE")

def verifier_type_cles():
    """Vérifier le type de clés créées"""
    print("\n🔍 VÉRIFICATION DU TYPE DE CLÉS")
    print("=" * 40)
    
    api_key = input("🔑 Colle ton API Key : ").strip()
    private_key = input("🔒 Colle ta Private Key (première ligne) : ").strip()
    
    print(f"\n📊 ANALYSE...")
    
    # Vérifier API Key
    if len(api_key) == 36 and api_key.count('-') == 4:
        print("✅ API Key : Format UUID correct")
    elif len(api_key) == 64:
        print("⚠️  API Key : Format HEX (possible Legacy)")
    else:
        print("❌ API Key : Format non reconnu")
    
    # Vérifier Private Key
    if "BEGIN EC PRIVATE KEY" in private_key:
        print("✅ Private Key : Format EC correct (Advanced Trade)")
    elif len(private_key) == 64:
        print("⚠️  Private Key : Format HEX (possible Legacy)")
    else:
        print("❌ Private Key : Format non reconnu")
    
    if "✅" in f"{api_key} {private_key}":
        print("\n🎉 TES CLÉS SEMBLENT CORRECTES !")
        print("🔄 Lance le test : python3 test_nouvelles_cles.py")
    else:
        print("\n❌ PROBLÈME AVEC TES CLÉS")
        print("💡 Assure-toi de créer des 'Cloud Trading Keys'")

if __name__ == "__main__":
    guide_interactif()
    
    print("\n" + "="*60)
    response = input("🔍 Veux-tu vérifier tes clés maintenant ? (o/n): ")
    if response.lower() in ['o', 'oui', 'y', 'yes']:
        verifier_type_cles()
    
    print("\n🚀 Le dashboard DÉMO continue de tourner en attendant !")
    print("🔗 http://localhost:8888")
