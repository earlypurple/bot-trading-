#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démo Portfolio Manager - Early-Bot-Trading
Version de démonstration avec données simulées
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_portfolio_manager import EnhancedPortfolioManager
import json
from datetime import datetime

class DemoPortfolioManager(EnhancedPortfolioManager):
    def __init__(self):
        # Initialisation sans exchange pour demo
        self.exchange = None
        self.db_path = "enhanced_portfolio.db"
        self.setup_database()
        self.performance_cache = {}
        print("✅ Demo Portfolio Manager initialisé")
    
    def get_demo_portfolio(self):
        """Portfolio de démonstration avec vos vraies données"""
        portfolio = {
            'BCH': {
                'balance': 0.01234,
                'price_usd': 470.85,
                'usd_value': 5.80,
                'percentage': 36.5,
                'change_24h': -2.3,
                'volatility': 45.2,
                'risk_score': 52,
                'performance_score': 65,
                'recommendation': 'CONSERVER',
                'volume_24h': 125000000,
                'market_cap': 9300000000
            },
            'ETH': {
                'balance': 0.00213,
                'price_usd': 2485.25,
                'usd_value': 5.29,
                'percentage': 33.3,
                'change_24h': 1.8,
                'volatility': 38.1,
                'risk_score': 35,
                'performance_score': 78,
                'recommendation': 'ACHETER',
                'volume_24h': 890000000,
                'market_cap': 299000000000
            },
            'SOL': {
                'balance': 0.0891,
                'price_usd': 152.67,
                'usd_value': 1.36,
                'percentage': 8.6,
                'change_24h': 5.2,
                'volatility': 62.3,
                'risk_score': 58,
                'performance_score': 82,
                'recommendation': 'CONSERVER',
                'volume_24h': 245000000,
                'market_cap': 71000000000
            },
            'FLR': {
                'balance': 15.234,
                'price_usd': 0.088,
                'usd_value': 1.34,
                'percentage': 8.4,
                'change_24h': -1.2,
                'volatility': 78.5,
                'risk_score': 75,
                'performance_score': 45,
                'recommendation': 'OBSERVER',
                'volume_24h': 12000000,
                'market_cap': 2100000000
            },
            'SHIB': {
                'balance': 45678.91,
                'price_usd': 0.00002,
                'usd_value': 0.91,
                'percentage': 5.7,
                'change_24h': 8.5,
                'volatility': 95.2,
                'risk_score': 85,
                'performance_score': 90,
                'recommendation': 'VENDRE',
                'volume_24h': 156000000,
                'market_cap': 15200000000
            },
            'ETC': {
                'balance': 0.0234,
                'price_usd': 27.78,
                'usd_value': 0.65,
                'percentage': 4.1,
                'change_24h': -0.8,
                'volatility': 52.1,
                'risk_score': 62,
                'performance_score': 55,
                'recommendation': 'OBSERVER',
                'volume_24h': 34000000,
                'market_cap': 4100000000
            },
            'API3': {
                'balance': 0.456,
                'price_usd': 1.75,
                'usd_value': 0.08,
                'percentage': 0.5,
                'change_24h': 12.3,
                'volatility': 125.8,
                'risk_score': 88,
                'performance_score': 95,
                'recommendation': 'RÉDUIRE',
                'volume_24h': 8500000,
                'market_cap': 175000000
            }
        }
        
        total_value = sum(asset['usd_value'] for asset in portfolio.values())
        
        # Recalcul des pourcentages
        for asset in portfolio.values():
            asset['percentage'] = (asset['usd_value'] / total_value) * 100
        
        # Métriques globales
        metrics = {
            'daily_change': 1.2,
            'portfolio_volatility': 58.3,
            'diversification_score': 72,
            'concentration_risk': 36.5,
            'num_assets': len(portfolio),
            'risk_adjusted_return': 0.89,
            'balance_quality': 'MODÉRÉMENT ÉQUILIBRÉ'
        }
        
        # Alertes
        alerts = []
        for currency, data in portfolio.items():
            if data['change_24h'] < -15:
                alerts.append({
                    'type': 'FORTE_BAISSE',
                    'currency': currency,
                    'message': f'{currency} a baissé de {data["change_24h"]:.1f}% en 24h',
                    'severity': 'HIGH',
                    'action': 'Considérer une vente de protection'
                })
            elif data['risk_score'] > 80 and data['percentage'] > 5:
                alerts.append({
                    'type': 'RISQUE_ÉLEVÉ',
                    'currency': currency,
                    'message': f'{currency} présente un risque élevé ({data["risk_score"]:.0f}/100)',
                    'severity': 'MEDIUM',
                    'action': 'Surveiller ou réduire la position'
                })
        
        # Recommandations
        recommendations = [
            {
                'type': 'DIVERSIFICATION',
                'priority': 'MEDIUM',
                'message': 'Ajouter USDC pour plus de stabilité',
                'action': 'Convertir 20% des altcoins vers USDC',
                'benefit': 'Réduction du risque global de 15%'
            },
            {
                'type': 'REBALANCING',
                'priority': 'LOW',
                'message': 'BCH et ETH dominent le portfolio',
                'action': 'Diversifier vers d\'autres cryptos de qualité',
                'benefit': 'Meilleure répartition des risques'
            }
        ]
        
        # Suggestion de rebalancing
        rebalancing = {
            'needed': True,
            'suggestions': [
                {
                    'risk_level': 'high_risk',
                    'action': 'Réduire',
                    'current': 19.7,
                    'target': 15.0,
                    'diff': 4.7
                }
            ],
            'estimated_benefit': 'Réduction du risque de 12%'
        }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_value': total_value,
            'portfolio': portfolio,
            'metrics': metrics,
            'alerts': alerts,
            'recommendations': recommendations,
            'diversification_score': 72,
            'rebalancing_suggestion': rebalancing
        }

def demo_analysis():
    """Analyse de démonstration complète"""
    print("🚀 ANALYSE PORTFOLIO - EARLY-BOT-TRADING")
    print("="*60)
    
    manager = DemoPortfolioManager()
    data = manager.get_demo_portfolio()
    
    # Affichage détaillé
    print(f"\n💰 PORTFOLIO ACTUEL - Valeur Totale: ${data['total_value']:.2f}")
    print(f"🎯 Score de Diversification: {data['diversification_score']}/100")
    print(f"📊 Qualité d'Équilibrage: {data['metrics']['balance_quality']}")
    print(f"📈 Performance 24h: +{data['metrics']['daily_change']:.1f}%")
    print(f"⚡ Volatilité Portfolio: {data['metrics']['portfolio_volatility']:.1f}%")
    
    print("\n" + "="*60)
    print("📋 DÉTAIL DES POSITIONS:")
    print("="*60)
    
    for currency, asset in sorted(data['portfolio'].items(), key=lambda x: x[1]['usd_value'], reverse=True):
        risk_icon = "🔴" if asset['risk_score'] > 70 else "🟡" if asset['risk_score'] > 40 else "🟢"
        change_icon = "📈" if asset['change_24h'] > 0 else "📉"
        
        print(f"{risk_icon} {currency:>6} | ${asset['usd_value']:>6.2f} ({asset['percentage']:>5.1f}%) | "
              f"{change_icon} {asset['change_24h']:>+5.1f}% | Risk: {asset['risk_score']:>2.0f}/100 | {asset['recommendation']}")
    
    # Alertes
    if data['alerts']:
        print(f"\n🔔 ALERTES ACTIVES ({len(data['alerts'])}):")
        print("-" * 50)
        for alert in data['alerts']:
            severity_icon = "🚨" if alert['severity'] == 'HIGH' else "⚠️"
            print(f"{severity_icon} {alert['message']}")
            print(f"   Action recommandée: {alert['action']}")
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS ({len(data['recommendations'])}):")
    print("-" * 50)
    for rec in data['recommendations']:
        priority_icon = "🔥" if rec['priority'] == 'HIGH' else "📋"
        print(f"{priority_icon} {rec['type']}: {rec['message']}")
        print(f"   Action: {rec['action']}")
        print(f"   Bénéfice: {rec['benefit']}")
        print()
    
    # Rebalancing
    if data['rebalancing_suggestion']['needed']:
        print("🎯 SUGGESTION DE REBALANCING:")
        print("-" * 50)
        for suggestion in data['rebalancing_suggestion']['suggestions']:
            print(f"• {suggestion['action']} allocation {suggestion['risk_level']}")
            print(f"  Actuel: {suggestion['current']:.1f}% → Cible: {suggestion['target']:.1f}%")
        print(f"💎 Bénéfice estimé: {data['rebalancing_suggestion']['estimated_benefit']}")
    
    print("\n" + "="*60)
    print("📊 RÉSUMÉ STRATÉGIQUE:")
    print("="*60)
    print(f"• Portfolio de ${data['total_value']:.2f} bien diversifié sur {len(data['portfolio'])} cryptos")
    print(f"• Volatilité modérée ({data['metrics']['portfolio_volatility']:.1f}%)")
    print(f"• Performance positive sur 24h (+{data['metrics']['daily_change']:.1f}%)")
    print(f"• {len(data['alerts'])} alertes à surveiller")
    print(f"• Recommandations pour optimiser le risque/rendement")
    
    print(f"\n💎 NEXT STEPS:")
    print(f"1. Surveiller les alertes {len(data['alerts'])} actives")
    print(f"2. Considérer le rebalancing suggéré")
    print(f"3. Ajouter USDC pour plus de stabilité")
    print(f"4. Activer le trading automatique avec IA")
    
    # Sauvegarde rapport
    filename = f"portfolio_demo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Rapport détaillé sauvegardé: {filename}")

if __name__ == "__main__":
    demo_analysis()
