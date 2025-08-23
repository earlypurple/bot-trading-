#!/usr/bin/env python3
"""
Script simple pour vérifier le portefeuille Coinbase
"""

import os
import sys
from dotenv import load_dotenv

def check_portfolio():
    """Vérifie le contenu du portefeuille"""
    print("💰 Vérification du Portefeuille Coinbase")
    print("=" * 40)
    
    # Charger les variables d'environnement
    load_dotenv()
    
    api_key = os.getenv('COINBASE_API_KEY')
    secret_key = os.getenv('COINBASE_SECRET_KEY')
    
    if not api_key or not secret_key:
        print("❌ Clés API non configurées")
        return
        
    print(f"🔑 API Key: {api_key[:8]}...")
    print(f"🔐 Secret: {'Configuré' if secret_key else 'Manquant'}")
    print()
    
    try:
        import ccxt
        print("📡 Connexion à Coinbase Advanced Trade...")
        
        exchange = ccxt.coinbaseadvanced({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
        })
        
        print("🔍 Récupération du solde...")
        balance = exchange.fetch_balance()
        
        print(f"✅ Connexion réussie !")
        print(f"📊 Nombre total d'actifs: {len(balance)}")
        print()
        
        # Compter les actifs avec solde
        actifs_avec_solde = 0
        actifs_details = []
        
        for asset, info in balance.items():
            if isinstance(info, dict):
                total = info.get('total', 0)
                if total > 0:
                    actifs_avec_solde += 1
                    actifs_details.append({
                        'asset': asset,
                        'total': total,
                        'free': info.get('free', 0),
                        'used': info.get('used', 0)
                    })
        
        print(f"💎 Actifs avec solde positif: {actifs_avec_solde}")
        
        if actifs_details:
            print("\n📈 Détails des actifs:")
            print("-" * 50)
            for actif in actifs_details[:10]:  # Top 10
                asset = actif['asset']
                total = actif['total']
                free = actif['free']
                
                if asset == 'EUR':
                    print(f"💶 {asset}: {total:.2f} (Disponible: {free:.2f})")
                elif asset == 'USD':
                    print(f"💵 {asset}: {total:.2f} (Disponible: {free:.2f})")
                else:
                    print(f"🪙 {asset}: {total:.8f} (Disponible: {free:.8f})")
        else:
            print("ℹ️  Aucun actif avec solde trouvé")
            
        # Test d'une requête simple pour les marchés
        print("\n🏪 Test des marchés disponibles...")
        try:
            markets = exchange.load_markets()
            print(f"✅ {len(markets)} marchés disponibles")
            
            # Afficher quelques marchés EUR
            eur_markets = [m for m in markets.keys() if '/EUR' in m][:5]
            if eur_markets:
                print("💶 Marchés EUR disponibles:")
                for market in eur_markets:
                    print(f"   - {market}")
                    
        except Exception as e:
            print(f"⚠️  Impossible de charger les marchés: {str(e)[:50]}")
            
    except ImportError:
        print("❌ Module ccxt non installé")
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        print("💡 Vérifiez vos clés API sur Coinbase")

if __name__ == "__main__":
    check_portfolio()
