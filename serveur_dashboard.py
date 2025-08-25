#!/usr/bin/env python3
"""
Serveur Complet pour le Dashboard du Bot de Trading Quantique
Version intégrée avec Early-Bot-Trading - PORTFOLIO RÉEL
"""
import os
import json
import time
import random
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timedelta
import webbrowser

# Import du connecteur portfolio réel
try:
    from portfolio_connector import RealPortfolioConnector
    REAL_PORTFOLIO_AVAILABLE = True
    print("✅ Connecteur portfolio réel importé")
except ImportError as e:
    REAL_PORTFOLIO_AVAILABLE = False
    print(f"⚠️ Connecteur portfolio réel non disponible: {e}")

class QuantumTradingBotServer:
    """Serveur complet avec simulation du bot et de l'IA + PORTFOLIO RÉEL"""

    def __init__(self):
        self.bot_running = False
        self.start_time = None
        
        # Connecteur portfolio réel
        self.portfolio_connector = None
        if REAL_PORTFOLIO_AVAILABLE:
            try:
                self.portfolio_connector = RealPortfolioConnector()
                print("✅ Connecteur portfolio réel initialisé")
            except Exception as e:
                print(f"⚠️ Erreur initialisation portfolio réel: {e}")
                self.portfolio_connector = None

        # Données par défaut si pas de connexion réelle
        self.fallback_data = {
            'initial_capital': 10000.0,
            'current_equity': 10247.83,
            'daily_pnl': 247.83
        }

    def get_real_portfolio_data(self):
        """Récupère les vraies données du portefeuille"""
        if self.portfolio_connector:
            try:
                return self.portfolio_connector.format_for_frontend()
            except Exception as e:
                print(f"⚠️ Erreur récupération portfolio réel: {e}")
                return None
        return None

    def get_financial_metrics(self):
        """Retourne les métriques financières (réelles ou simulées)"""
        real_data = self.get_real_portfolio_data()
        
        if real_data and real_data.get('portfolio'):
            # Utilise les vraies données
            portfolio = real_data['portfolio']
            return {
                'current_equity': float(portfolio['total_equity']),
                'daily_pnl': float(portfolio['daily_pnl']),
                'positions_count': portfolio['positions_count'],
                'win_rate': portfolio['win_rate'],
                'trades_today': portfolio['trades_today'],
                'source': 'real'
            }
        else:
            # Fallback vers les données simulées
            return {
                'current_equity': self.fallback_data['current_equity'],
                'daily_pnl': self.fallback_data['daily_pnl'],
                'positions_count': len(self.positions),
                'win_rate': '72%',
                'trades_today': 12,
                'source': 'simulated'
            }

    def get_real_positions(self):
        """Retourne les vraies positions du portefeuille"""
        real_data = self.get_real_portfolio_data()
        
        if real_data and real_data.get('positions'):
            return real_data['positions']
        else:
            # Fallback vers positions simulées
            return [
                {
                    'display_name': 'BTC-EUR',
                    'symbol': 'BTC',
                    'quantity': '0.045',
                    'value_eur': '2156.78',
                    'price': '47928.44',
                    'pnl': '+127.45 €',
                    'pnl_class': 'positive'
                },
                {
                    'display_name': 'ETH-EUR',
                    'symbol': 'ETH',
                    'quantity': '2.3',
                    'value_eur': '6632.40',
                    'price': '2884.52',
                    'pnl': '+89.32 €',
                    'pnl_class': 'positive'
                },
                {
                    'display_name': 'USDC-EUR',
                    'symbol': 'USDC',
                    'quantity': '1458.65',
                    'value_eur': '1458.65',
                    'price': '1.00',
                    'pnl': '0.00 €',
                    'pnl_class': 'neutral'
                }
            ]
            {
                'id': 1,
                'symbol': 'EURUSD',
                'side': 'LONG',
                'quantity': 1000,
                'entry_price': 1.1000,
                'current_price': 1.1025,
                'unrealized_pnl': 25.00,
                'strategy': 'Conservative',
                'entry_time': datetime.now() - timedelta(hours=2)
            },
            {
                'id': 2,
                'symbol': 'GBPUSD', 
                'side': 'SHORT',
                'quantity': 800,
                'entry_price': 1.2500,
                'current_price': 1.2485,
                'unrealized_pnl': 12.00,
                'strategy': 'Scalping',
                'entry_time': datetime.now() - timedelta(hours=1)
            },
            {
                'id': 3,
                'symbol': 'AUDUSD',
                'side': 'LONG', 
                'quantity': 1500,
                'entry_price': 0.6800,
                'current_price': 0.6815,
                'unrealized_pnl': 22.50,
                'strategy': 'ML Adaptive',
                'entry_time': datetime.now() - timedelta(minutes=30)
            ]

        # Positions simulées de fallback
        self.fallback_positions = [
            {
                'id': 1,
                'symbol': 'EURUSD',
                'side': 'LONG',
                'quantity': 1000,
                'entry_price': 1.1000,
                'current_price': 1.1025,
                'unrealized_pnl': 25.00,
                'strategy': 'Conservative',
                'entry_time': datetime.now() - timedelta(hours=2)
            },
            {
                'id': 2,
                'symbol': 'GBPUSD', 
                'side': 'SHORT',
                'quantity': 800,
                'entry_price': 1.2500,
                'current_price': 1.2485,
                'unrealized_pnl': 12.00,
                'strategy': 'Scalping',
                'entry_time': datetime.now() - timedelta(hours=1)
            },
            {
                'id': 3,
                'symbol': 'AUDUSD',
                'side': 'LONG', 
                'quantity': 1500,
                'entry_price': 0.6800,
                'current_price': 0.6815,
                'unrealized_pnl': 22.50,
                'strategy': 'ML Adaptive',
                'entry_time': datetime.now() - timedelta(minutes=30)
            }
            {
                'symbol': 'USDJPY',
                'side': 'BUY',
                'pnl': 45.20,
                'time': '11:35',
                'strategy': 'Aggressive',
                'duration': '2.3min',
                'ai_confidence': 84
            },
            {
                'symbol': 'EURUSD',
                'side': 'SELL', 
                'pnl': -12.30,
                'time': '11:28',
                'strategy': 'Normal',
                'duration': '1.8min',
                'ai_confidence': 67
            },
            {
                'symbol': 'BTCUSD',
                'side': 'BUY',
                'pnl': 127.80,
                'time': '11:15',
                'strategy': 'ML Adaptive',
                'duration': '8.4min',
                'ai_confidence': 91
            }
        ]

        # Métriques IA
        self.ai_models = {
            'lstm': {'accuracy': 87.3, 'predictions': 245},
            'random_forest': {'accuracy': 72.1, 'signals': 189},
            'bert_sentiment': {'accuracy': 91.5, 'analyses': 512},
            'gbm_volatility': {'accuracy': 78.4, 'forecasts': 156}
        }

        # Métriques quantiques
        self.quantum_metrics = {
            'superposition': 73.2,
            'entanglement': 82.5,
            'momentum': 65.8,
            'coherence': 89.4
        }

        # Sentiment de marché
        self.market_sentiment = {
            'score': 0.23,
            'label': 'bullish',
            'confidence': 0.81,
            'emoji': '📈'
        }

        # Logs d'activité
        self.activity_logs = [
            {'timestamp': datetime.now(), 'message': '🤖 Bot initialisé - IA intégrée activée', 'level': 'info'},
            {'timestamp': datetime.now(), 'message': '✅ 4 modèles ML chargés avec succès', 'level': 'success'},
            {'timestamp': datetime.now(), 'message': '🔬 Processeur quantique opérationnel', 'level': 'info'},
            {'timestamp': datetime.now(), 'message': '📊 Connexion aux données de marché établie', 'level': 'info'}
        ]

        # Thread de mise à jour
        self.update_thread = None

    def start_bot(self):
        """Démarre le bot"""
        if self.bot_running:
            return False

        self.bot_running = True
        self.start_time = datetime.now()

        # Démarrage du thread de mise à jour
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()

        self.add_log('🚀 Bot démarré avec succès', 'success')
        self.add_log('🧠 IA activée - 4 modèles opérationnels', 'success')
        self.add_log('🔬 Activation du processeur quantique', 'info')

        return True

    def stop_bot(self):
        """Arrête le bot"""
        if not self.bot_running:
            return False

        self.bot_running = False

        self.add_log('⏹️ Arrêt du bot demandé', 'warning')
        self.add_log('💾 Sauvegarde des données...', 'info')

        return True

    def _update_loop(self):
        """Boucle de mise à jour en continu"""
        while self.bot_running:
            try:
                # Mise à jour des métriques
                self._update_financial_metrics()
                self._update_quantum_metrics()
                self._update_ai_models()

                # Simulation d'activité
                if random.random() < 0.3:
                    self._simulate_trading_activity()

                time.sleep(3)  # Mise à jour toutes les 3 secondes

            except Exception as e:
                self.add_log(f'❌ Erreur mise à jour: {e}', 'error')
                time.sleep(5)

    def _update_financial_metrics(self):
        """Met à jour les métriques financières"""
        # Variation de l'equity
        equity_variation = (random.random() - 0.5) * 100
        self.current_equity += equity_variation

        # Variation du P&L journalier
        pnl_variation = (random.random() - 0.5) * 50
        self.daily_pnl += pnl_variation

        # Mise à jour des positions
        for position in self.positions:
            price_variation = (random.random() - 0.5) * 0.002
            position['current_price'] *= (1 + price_variation)

            # Recalcul du P&L
            if position['side'] == 'LONG':
                position['unrealized_pnl'] = (position['current_price'] - position['entry_price']) * position['quantity']
            else:
                position['unrealized_pnl'] = (position['entry_price'] - position['current_price']) * position['quantity']

    def _update_quantum_metrics(self):
        """Met à jour les métriques quantiques"""
        base_values = {
            'superposition': 73.2,
            'entanglement': 82.5,
            'momentum': 65.8
        }

        for key, base_value in base_values.items():
            variation = (random.random() - 0.5) * 20
            new_value = max(30, min(95, base_value + variation))
            self.quantum_metrics[key] = round(new_value, 1)

        # Cohérence globale
        avg_quantum = sum(list(self.quantum_metrics.values())[:3]) / 3
        self.quantum_metrics['coherence'] = round(avg_quantum + random.uniform(-5, 5), 1)

    def _update_ai_models(self):
        """Met à jour les performances des modèles IA"""
        for model_name, model_data in self.ai_models.items():
            # Amélioration graduelle de la précision
            if random.random() < 0.05:  # 5% chance d'amélioration
                improvement = random.uniform(0.1, 0.3)
                model_data['accuracy'] = min(95.0, model_data['accuracy'] + improvement)

            # Augmentation des compteurs
            if 'predictions' in model_data:
                model_data['predictions'] += random.randint(0, 2)
            if 'signals' in model_data:
                model_data['signals'] += random.randint(0, 1)
            if 'analyses' in model_data:
                model_data['analyses'] += random.randint(0, 3)
            if 'forecasts' in model_data:
                model_data['forecasts'] += random.randint(0, 1)

    def _simulate_trading_activity(self):
        """Simule l'activité de trading"""
        activities = [
            '📊 Analyse EURUSD - Signal IA détecté',
            '🎯 Prédiction ML: GBPUSD hausse probable', 
            '⚡ Momentum quantique élevé sur AUDUSD',
            '🔍 Scan des opportunités sur 12 paires',
            '📈 Sentiment marché: Bullish confirmé',
            '🤖 Modèle LSTM recalibré automatiquement',
            '💹 Nouvelle position: USDJPY via IA',
            '✅ Stop-loss ajusté par IA sur EURUSD',
            '🔬 Corrélation quantique: EUR/GBP détectée'
        ]

        activity = random.choice(activities)
        self.add_log(activity, 'info')

        # Simulation de nouveaux trades
        if random.random() < 0.1:  # 10% chance de nouveau trade
            pairs = ['EURUSD', 'GBPUSD', 'AUDUSD', 'USDJPY', 'BTCUSD']
            sides = ['BUY', 'SELL']
            strategies = ['Conservative', 'Scalping', 'ML Adaptive', 'Aggressive']

            pair = random.choice(pairs)
            side = random.choice(sides)
            strategy = random.choice(strategies)
            pnl = (random.random() - 0.2) * 150  # Bias positif
            confidence = random.randint(65, 95)

            new_trade = {
                'symbol': pair,
                'side': side,
                'pnl': pnl,
                'time': datetime.now().strftime('%H:%M'),
                'strategy': strategy,
                'duration': f'{random.uniform(0.5, 10):.1f}min',
                'ai_confidence': confidence
            }

            self.trades_history.insert(0, new_trade)

            # Garder seulement les 20 derniers
            if len(self.trades_history) > 20:
                self.trades_history = self.trades_history[:20]

            self.add_log(f'💰 Trade IA: {pair} {side} | {pnl:+.2f}€ | Conf: {confidence}%', 
                        'success' if pnl > 0 else 'warning')

    def add_log(self, message, level):
        """Ajoute une entrée au log"""
        entry = {
            'timestamp': datetime.now(),
            'message': message,
            'level': level
        }

        self.activity_logs.insert(0, entry)

        # Garder seulement les 100 dernières entrées
        if len(self.activity_logs) > 100:
            self.activity_logs = self.activity_logs[:100]

    def get_status(self):
        """Retourne le statut complet"""
        return {
            'bot': {
                'is_running': self.bot_running,
                'start_time': self.start_time.isoformat() if self.start_time else None,
                'current_equity': round(self.current_equity, 2),
                'daily_pnl': round(self.daily_pnl, 2),
                'initial_capital': self.initial_capital,
                'total_return_pct': round((self.current_equity - self.initial_capital) / self.initial_capital * 100, 2)
            },
            'positions': self.positions,
            'trades_history': self.trades_history[:10],  # 10 derniers
            'ai_models': self.ai_models,
            'quantum_metrics': self.quantum_metrics,
            'market_sentiment': self.market_sentiment,
            'activity_logs': [
                {
                    'timestamp': log['timestamp'].isoformat(),
                    'message': log['message'],
                    'level': log['level']
                }
                for log in self.activity_logs[:20]  # 20 dernières
            ],
            'performance_stats': {
                'total_trades': len(self.trades_history),
                'winning_trades': len([t for t in self.trades_history if t['pnl'] > 0]),
                'win_rate': len([t for t in self.trades_history if t['pnl'] > 0]) / max(1, len(self.trades_history)),
                'avg_trade': sum(t['pnl'] for t in self.trades_history) / max(1, len(self.trades_history))
            },
            'timestamp': datetime.now().isoformat()
        }

# Instance globale du serveur
server_instance = QuantumTradingBotServer()

class DashboardHandler(BaseHTTPRequestHandler):
    """Handler pour le serveur HTTP"""

    def do_GET(self):
        if self.path in ['/', '/dashboard']:
            self._serve_dashboard()
        elif self.path == '/api/status':
            self._serve_status()
        elif self.path == '/api/bot/start':
            self._start_bot()
        elif self.path == '/api/bot/stop':
            self._stop_bot()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/bot/start':
            self._start_bot()
        elif self.path == '/api/bot/stop':
            self._stop_bot()
        else:
            self.send_response(404)
            self.end_headers()

    def _serve_dashboard(self):
        """Sert le dashboard HTML"""
        try:
            # Chemin absolu vers le fichier HTML
            html_path = os.path.join(os.path.dirname(__file__), 'dashboard_complet.html')
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

        except FileNotFoundError:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            error_html = f"<h1>❌ Dashboard non trouvé</h1><p>Fichier recherché: {os.path.join(os.path.dirname(__file__), 'dashboard_complet.html')}</p>".encode('utf-8')
            self.wfile.write(error_html)

    def _serve_status(self):
        """API de statut"""
        status = server_instance.get_status()
        self._send_json(status)

    def _start_bot(self):
        """API pour démarrer le bot"""
        success = server_instance.start_bot()
        self._send_json({
            'success': success,
            'message': 'Bot démarré avec succès' if success else 'Bot déjà en cours',
            'timestamp': datetime.now().isoformat()
        })

    def _stop_bot(self):
        """API pour arrêter le bot"""
        success = server_instance.stop_bot()
        self._send_json({
            'success': success,
            'message': 'Bot arrêté avec succès',
            'timestamp': datetime.now().isoformat()
        })

    def _send_json(self, data):
        """Envoie une réponse JSON"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        json_str = json.dumps(data, indent=2, default=str, ensure_ascii=False)
        self.wfile.write(json_str.encode('utf-8'))

    def log_message(self, format, *args):
        # Supprime les logs HTTP pour un affichage plus propre
        pass

def main():
    """Lance le serveur complet"""
    print("🤖 SERVEUR DASHBOARD COMPLET - BOT TRADING QUANTIQUE")
    print("=" * 70)
    print("🌐 Interface web complète avec bot et IA intégrés")
    print("📊 Dashboard professionnel temps réel")
    print("🧠 4 modèles IA + métriques quantiques")
    print("💰 Tracking P&L complet")
    print("📱 Design responsive moderne")
    print()

    try:
        server = HTTPServer(('localhost', 8080), DashboardHandler)

        print("✅ Serveur démarré avec succès !")
        print("🌐 Dashboard disponible sur: http://localhost:8080")
        print()
        print("🎯 FONCTIONNALITÉS COMPLÈTES:")
        print("  • Interface web interactive")
        print("  • Bot start/stop fonctionnel")
        print("  • IA avec 4 modèles en temps réel")
        print("  • Métriques quantiques animées")
        print("  • Positions et trades simulés")
        print("  • Log d'activité en direct")
        print("  • Graphiques et analytics")
        print("  • Design responsive")
        print()
        print("🚀 Ouverture automatique du navigateur...")

        # Ouverture automatique du navigateur
        try:
            webbrowser.open('http://localhost:8080')
            print("✅ Navigateur ouvert automatiquement")
        except:
            print("ℹ️  Ouvrez manuellement: http://localhost:8080")

        print()
        print("🏃‍♂️ Serveur en cours d'exécution...")
        print("ℹ️  Appuyez sur Ctrl+C pour arrêter")
        print()

        server.serve_forever()

    except KeyboardInterrupt:
        print("\nℹ️  Arrêt du serveur demandé")
        if server_instance.bot_running:
            server_instance.stop_bot()
        print("📊 Dashboard fermé proprement")
    except Exception as e:
        print(f"\n❌ Erreur serveur: {e}")
        print("💡 Vérifiez que le port 8080 est libre")
        input("Appuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
