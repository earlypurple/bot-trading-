#!/usr/bin/env python3
"""
Script pour mettre à jour la certification du bot
"""

def update_certification():
    print("🎫 MISE À JOUR CERTIFICATION BOT")
    print("=" * 50)
    
    print("Votre code de certification (valide 1 an) peut être:")
    print("1. Une nouvelle passphrase Coinbase")
    print("2. Un token d'authentification")
    print("3. Une clé API mise à jour")
    
    print("\n📝 Pour mettre à jour manuellement:")
    print("1. Ouvrez: config/api_config.py")
    print("2. Remplacez:")
    print("   'coinbase_passphrase': 'ma_passphrase_securisee'")
    print("   PAR:")
    print("   'coinbase_passphrase': 'VOTRE_VRAI_CODE_CERTIFICATION'")
    
    print("\n🔒 SÉCURITÉ:")
    print("• Ne partagez jamais votre code de certification")
    print("• Gardez-le secret et sécurisé")
    print("• Il est valide 1 an selon vos informations")
    
    print("\n✅ APRÈS MISE À JOUR:")
    print("• Redémarrez le bot")
    print("• Les trades réels fonctionneront")
    print("• Plus d'erreur 'account is not available'")

if __name__ == "__main__":
    update_certification()
