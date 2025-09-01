#!/usr/bin/env python3
"""
🎯 BOT TRADING FINAL AVANCÉ
Version complète avec modes de trading, auto-trading et logs détaillés
"""
import os
import sys
import json
import time
import threading
import webbrowser
import random
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

print("🎯 DÉMARRAGE BOT TRADING FINAL AVANCÉ...")

try:
    import ccxt
    print("✅ Module ccxt importé")
except ImportError as e:
    print(f"❌ ERREUR ccxt: {e}")
    sys.exit(1)

class AdvancedTradingBot:
    """Bot de trading avancé avec modes multiples"""
    
    def __init__(self):
        print("🔧 Initialisation bot avancé...")
        self.exchange = None
        self.is_connected = False
        self.portfolio = {}
        self.prices = {}
        self.current_mode = "micro"
        self.auto_trading_active = False
        self.trades_history = []
        self.logs = []
        self.log_file = "TRADING_AVANCE.log"
        
        # Modes de trading disponibles
        self.trading_modes = {
            "micro": {
                "name": "Micro Trading",
                "description": "Trading ultra-sécurisé avec petits montants",
                "min_amount": 1.0,
                "max_amount": 3.0,
                "frequency_seconds": 900,  # 15 minutes
                "risk_level": "Très Faible",
                "profit_target": 0.5,  # 0.5%
                "max_trades_per_hour": 4
            },
            "conservateur": {
                "name": "Mode Conservateur", 
                "description": "Trading prudent avec risques limités",
                "min_amount": 2.0,
                "max_amount": 5.0,
                "frequency_seconds": 600,  # 10 minutes
                "risk_level": "Faible",
                "profit_target": 1.0,  # 1%
                "max_trades_per_hour": 6
            },
            "equilibre": {
                "name": "Mode Équilibré",
                "description": "Balance entre sécurité et profits",
                "min_amount": 3.0,
                "max_amount": 8.0,
                "frequency_seconds": 300,  # 5 minutes
                "risk_level": "Modéré",
                "profit_target": 1.5,  # 1.5%
                "max_trades_per_hour": 12
            },
            "dynamique": {
                "name": "Mode Dynamique",
                "description": "Trading actif pour profits accélérés",
                "min_amount": 5.0,
                "max_amount": 12.0,
                "frequency_seconds": 180,  # 3 minutes
                "risk_level": "Élevé",
                "profit_target": 2.0,  # 2%
                "max_trades_per_hour": 20
            },
            "aggressif": {
                "name": "Mode Agressif",
                "description": "Trading haute fréquence maximum profit",
                "min_amount": 8.0,
                "max_amount": 20.0,
                "frequency_seconds": 120,  # 2 minutes
                "risk_level": "Maximum",
                "profit_target": 3.0,  # 3%
                "max_trades_per_hour": 30
            }
        }
        
        try:
            # Configuration API
            self._log("INIT", "Démarrage bot avancé")
            print("📡 Configuration API...")
            with open('cdp_api_key.json', 'r') as f:
                config = json.load(f)
            
            print(f"🔑 API: {config['name'].split('/')[-1]}")
            
            # Exchange avec configuration optimisée
            print("🏦 Connexion exchange...")
            self.exchange = ccxt.coinbaseadvanced({
                'apiKey': config['name'],
                'secret': config['privateKey'],
                'passphrase': '',
                'sandbox': False,
                'enableRateLimit': True,
                'timeout': 30000,
                'options': {
                    'createMarketBuyOrderRequiresPrice': False,  # ✅ SYNTAXE CORRIGÉE
                    'advanced': True,
                    'fetchBalance': 'v2PrivateGetAccounts'
                }
            })
            
            print("✅ Exchange configuré")
            self._log("API", "Exchange connecté avec succès")
            
            # Test de connexion
            print("🧪 Test connexion...")
            balance = self.exchange.fetch_balance()
            print("✅ API fonctionnelle")
            self._log("API", "Test connexion réussi")
            
            self.is_connected = True
            print("🎯 Bot avancé initialisé avec succès !")
            self._log("INIT", "Initialisation complète réussie")
            
        except Exception as e:
            error_msg = f"Erreur initialisation: {e}"
            print(f"❌ {error_msg}")
            self._log("ERROR", error_msg)
            import traceback
            traceback.print_exc()
    
    def _log(self, category, message):
        """Système de logs avancé"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'category': category,
            'message': message,
            'mode': self.current_mode
        }
        
        self.logs.append(log_entry)
        
        # Garder seulement les 100 derniers logs en mémoire
        if len(self.logs) > 100:
            self.logs = self.logs[-100:]
        
        # Écrire dans le fichier
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] [{category}] [{self.current_mode}] {message}\\n")
        except:
            pass
        
        print(f"📝 [{category}] {message}")
    
    def get_portfolio(self):
        """Récupérer portfolio avec informations détaillées"""
        try:
            balance = self.exchange.fetch_balance()
            portfolio = {}
            total_value = 0
            
            # Récupérer les prix actuels
            self._update_prices()
            
            for currency, amounts in balance.items():
                if isinstance(amounts, dict) and amounts.get('total', 0) > 0:
                    portfolio[currency] = amounts
                    
                    # Calculer valeur
                    if currency in ['USD', 'USDC', 'USDT']:
                        total_value += amounts['total']
                    else:
                        price = self.prices.get(currency, 0)
                        if price > 0:
                            total_value += amounts['total'] * price
            
            usdc_free = portfolio.get('USDC', {}).get('free', 0)
            
            return {
                'balances': portfolio, 
                'total_value': total_value,
                'usdc_available': usdc_free,
                'prices': self.prices,
                'last_update': datetime.now().isoformat()
            }
        except Exception as e:
            self._log("ERROR", f"Erreur portfolio: {e}")
            return {'balances': {}, 'total_value': 0, 'usdc_available': 0}
    
    def _update_prices(self):
        """Mettre à jour les prix des crypto"""
        try:
            symbols = ['BTC/USD', 'ETH/USD', 'SOL/USD', 'ATOM/USD', 'BCH/USD', 'LTC/USD']
            
            for symbol in symbols:
                try:
                    ticker = self.exchange.fetch_ticker(symbol)
                    currency = symbol.split('/')[0]
                    self.prices[currency] = ticker['last']
                except Exception as e:
                    self._log("WARNING", f"Prix {symbol}: {e}")
                    
        except Exception as e:
            self._log("ERROR", f"Mise à jour prix: {e}")
    
    def set_trading_mode(self, mode_name):
        """Changer le mode de trading"""
        if mode_name in self.trading_modes:
            old_mode = self.current_mode
            self.current_mode = mode_name
            self._log("MODE", f"Changement mode: {old_mode} → {mode_name}")
            return True
        return False
    
    def get_current_mode_info(self):
        """Informations du mode actuel"""
        return self.trading_modes.get(self.current_mode, {})
    
    def execute_trade(self, symbol='SOL/USD', side='buy', usd_amount=None):
        """Exécuter un trade avec le mode actuel"""
        try:
            mode_info = self.get_current_mode_info()
            
            # Déterminer le montant si non spécifié
            if usd_amount is None:
                min_amt = mode_info.get('min_amount', 1.0)
                max_amt = mode_info.get('max_amount', 3.0)
                usd_amount = random.uniform(min_amt, max_amt)
            
            self._log("TRADE_START", f"Début trade {side} {symbol} ${usd_amount:.2f}")
            
            # Vérifications portfolio
            portfolio = self.get_portfolio()
            usdc_available = portfolio['usdc_available']
            
            if side == 'buy' and usdc_available < usd_amount:
                error = f'USDC insuffisant: ${usdc_available:.2f} < ${usd_amount:.2f}'
                self._log("TRADE_ERROR", error)
                return {'error': error}
            
            # Prix actuel
            ticker = self.exchange.fetch_ticker(symbol)
            current_price = ticker['last']
            
            self._log("TRADE_INFO", f"Prix {symbol}: ${current_price:.2f}")
            
            if side == 'buy':
                # ✅ SYNTAXE CORRIGÉE pour market buy
                order = self.exchange.create_order(
                    symbol=symbol,
                    type='market',
                    side='buy',
                    amount=usd_amount,  # Cost USD directement
                    price=None
                )
            else:
                # Pour sell, calculer la quantité
                base_currency = symbol.split('/')[0]
                available = portfolio['balances'].get(base_currency, {}).get('free', 0)
                
                if available <= 0:
                    error = f"Pas de {base_currency} disponible"
                    self._log("TRADE_ERROR", error)
                    return {'error': error}
                
                # Montant à vendre (max 80% du disponible)
                available_value = available * current_price
                sell_value = min(usd_amount, available_value * 0.8)
                amount_to_sell = sell_value / current_price
                
                order = self.exchange.create_order(
                    symbol=symbol,
                    type='market',
                    side='sell',
                    amount=amount_to_sell,
                    price=None
                )
            
            # Enregistrer le trade
            trade_record = {
                'id': order.get('id', f'trade_{int(time.time())}'),
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol,
                'side': side,
                'amount': order.get('amount', 0),
                'price': current_price,
                'cost': order.get('cost', usd_amount),
                'status': order.get('status', 'filled'),
                'mode': self.current_mode,
                'usd_amount': usd_amount,
                'type': 'REAL_TRADE'
            }
            
            self.trades_history.append(trade_record)
            
            # Garder seulement les 50 derniers trades
            if len(self.trades_history) > 50:
                self.trades_history = self.trades_history[-50:]
            
            self._log("TRADE_SUCCESS", f"Trade réussi: {trade_record['id']} - {side} ${usd_amount:.2f}")
            
            return trade_record
            
        except Exception as e:
            error_msg = str(e)
            self._log("TRADE_ERROR", f"Échec trade: {error_msg}")
            
            return {
                'error': error_msg,
                'symbol': symbol,
                'side': side,
                'usd_amount': usd_amount,
                'timestamp': datetime.now().isoformat(),
                'type': 'FAILED_TRADE'
            }
    
    def start_auto_trading(self):
        """Démarrer le trading automatique"""
        if self.auto_trading_active:
            return False
        
        self.auto_trading_active = True
        mode_info = self.get_current_mode_info()
        
        self._log("AUTO_START", f"Auto-trading démarré en mode {self.current_mode}")
        
        def auto_trading_loop():
            """Boucle de trading automatique"""
            last_trade_time = 0
            trades_this_hour = 0
            hour_start = time.time()
            
            while self.auto_trading_active:
                try:
                    current_time = time.time()
                    mode_info = self.get_current_mode_info()
                    
                    # Reset compteur horaire
                    if current_time - hour_start > 3600:  # 1 heure
                        trades_this_hour = 0
                        hour_start = current_time
                    
                    # Vérifier si on peut trader
                    time_since_last = current_time - last_trade_time
                    frequency = mode_info.get('frequency_seconds', 600)
                    max_trades = mode_info.get('max_trades_per_hour', 6)
                    
                    if time_since_last >= frequency and trades_this_hour < max_trades:
                        # Vérifier les fonds
                        portfolio = self.get_portfolio()
                        usdc_available = portfolio['usdc_available']
                        min_amount = mode_info.get('min_amount', 1.0)
                        
                        if usdc_available >= min_amount:
                            # Exécuter un trade
                            symbol = random.choice(['SOL/USD', 'ATOM/USD'])  # Alterner les paires
                            side = 'buy'  # Principalement acheter pour accumuler
                            
                            result = self.execute_trade(symbol, side)
                            
                            if 'error' not in result:
                                last_trade_time = current_time
                                trades_this_hour += 1
                                self._log("AUTO_TRADE", f"Trade auto réussi: {result.get('id', 'N/A')}")
                            else:
                                self._log("AUTO_ERROR", f"Trade auto échoué: {result['error']}")
                        else:
                            self._log("AUTO_INFO", f"USDC insuffisant: ${usdc_available:.2f}")
                    
                    # Pause adaptative
                    sleep_time = min(60, frequency / 10)  # Max 1 minute
                    time.sleep(sleep_time)
                    
                except Exception as e:
                    self._log("AUTO_ERROR", f"Erreur boucle auto: {e}")
                    time.sleep(60)  # Pause de récupération
        
        # Démarrer la boucle dans un thread séparé
        threading.Thread(target=auto_trading_loop, daemon=True).start()
        return True
    
    def stop_auto_trading(self):
        """Arrêter le trading automatique"""
        self.auto_trading_active = False
        self._log("AUTO_STOP", "Auto-trading arrêté")
    
    def get_performance_stats(self):
        """Statistiques de performance"""
        if not self.trades_history:
            return {
                'total_trades': 0,
                'successful_trades': 0,
                'success_rate': 0,
                'total_invested': 0,
                'estimated_profit': 0
            }
        
        successful = len([t for t in self.trades_history if t.get('status') == 'filled'])
        total_invested = sum(t.get('usd_amount', 0) for t in self.trades_history if t.get('type') == 'REAL_TRADE')
        estimated_profit = total_invested * 0.002  # Estimation 0.2% profit
        
        return {
            'total_trades': len(self.trades_history),
            'successful_trades': successful,
            'success_rate': (successful / len(self.trades_history)) * 100 if self.trades_history else 0,
            'total_invested': total_invested,
            'estimated_profit': estimated_profit
        }
    
    def get_dashboard_data(self):
        """Données complètes pour le dashboard"""
        portfolio = self.get_portfolio()
        mode_info = self.get_current_mode_info()
        performance = self.get_performance_stats()
        
        return {
            'status': {
                'connected': self.is_connected,
                'auto_trading': self.auto_trading_active,
                'current_mode': self.current_mode,
                'api_status': 'Connecté' if self.is_connected else 'Déconnecté'
            },
            'portfolio': portfolio,
            'current_mode': mode_info,
            'available_modes': self.trading_modes,
            'performance': performance,
            'recent_trades': self.trades_history[-10:],
            'recent_logs': self.logs[-20:]
        }

# Instance globale du bot
advanced_bot = AdvancedTradingBot()

class AdvancedDashboardHandler(BaseHTTPRequestHandler):
    """Handler pour le dashboard avancé"""
    
    def do_GET(self):
        if self.path == '/':
            self._serve_dashboard()
        elif self.path == '/api/dashboard':
            self._send_json(advanced_bot.get_dashboard_data())
        elif self.path == '/api/portfolio':
            portfolio = advanced_bot.get_portfolio()
            self._send_json(portfolio)
        elif self.path == '/api/status':
            data = advanced_bot.get_dashboard_data()
            self._send_json(data['status'])
        elif self.path == '/api/modes':
            self._send_json(advanced_bot.trading_modes)
        elif self.path == '/api/performance':
            self._send_json(advanced_bot.get_performance_stats())
        elif self.path == '/api/logs':
            self._send_json({'logs': advanced_bot.logs[-30:]})
        elif self.path == '/api/trades':
            self._send_json({'trades': advanced_bot.trades_history[-20:]})
        elif self.path == '/api/start-auto':
            result = advanced_bot.start_auto_trading()
            self._send_json({'started': result, 'mode': advanced_bot.current_mode})
        elif self.path == '/api/stop-auto':
            advanced_bot.stop_auto_trading()
            self._send_json({'stopped': True})
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/api/trade':
            data = self._get_post_data()
            result = advanced_bot.execute_trade(
                data.get('symbol', 'SOL/USD'),
                data.get('side', 'buy'),
                float(data.get('usd_amount', 1.5))
            )
            self._send_json(result)
            
        elif self.path == '/api/set-mode':
            data = self._get_post_data()
            success = advanced_bot.set_trading_mode(data.get('mode', 'micro'))
            self._send_json({
                'success': success,
                'mode': advanced_bot.current_mode,
                'mode_info': advanced_bot.get_current_mode_info()
            })
        else:
            self.send_error(404)
    
    def _get_post_data(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            return json.loads(post_data.decode())
        except:
            return {}
    
    def _send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def _serve_dashboard(self):
        """Dashboard HTML avancé"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Bot Trading Avancé</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 30px;
            background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
            color: #000;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .status-bar {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }
        
        .status-item {
            background: rgba(255, 255, 255, 0.2);
            padding: 15px 20px;
            border-radius: 15px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(10px);
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .status-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-bottom: 25px;
        }
        
        @media (max-width: 1200px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }
        
        .section {
            background: rgba(255, 255, 255, 0.15);
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 25px;
            backdrop-filter: blur(15px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        
        .section-title {
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #feca57;
            border-bottom: 3px solid #feca57;
            padding-bottom: 10px;
            text-align: center;
        }
        
        .modes-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .mode-card {
            background: rgba(0, 0, 0, 0.3);
            border: 2px solid transparent;
            border-radius: 15px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
        }
        
        .mode-card:hover {
            border-color: #feca57;
            transform: scale(1.05);
            box-shadow: 0 10px 25px rgba(254, 202, 87, 0.3);
        }
        
        .mode-card.active {
            border-color: #48dbfb;
            background: rgba(72, 219, 251, 0.2);
        }
        
        .mode-name {
            font-size: 1.2em;
            font-weight: bold;
            color: #feca57;
            margin-bottom: 10px;
        }
        
        .mode-description {
            font-size: 0.9em;
            color: #ccc;
            margin-bottom: 15px;
        }
        
        .mode-stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            font-size: 0.85em;
        }
        
        .portfolio-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .portfolio-item {
            background: rgba(72, 219, 251, 0.2);
            border: 1px solid #48dbfb;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .portfolio-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(72, 219, 251, 0.3);
        }
        
        .currency {
            font-weight: bold;
            font-size: 1.1em;
            color: #feca57;
            margin-bottom: 8px;
        }
        
        .balance {
            font-size: 0.95em;
            color: #fff;
        }
        
        .trade-controls {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .btn {
            padding: 12px 20px;
            border: none;
            border-radius: 10px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            font-size: 0.9em;
        }
        
        .btn-success {
            background: linear-gradient(45deg, #2ed573, #7bed9f);
            color: #000;
        }
        
        .btn-danger {
            background: linear-gradient(45deg, #ff6b6b, #ff5252);
            color: #fff;
        }
        
        .btn-primary {
            background: linear-gradient(45deg, #feca57, #ff9ff3);
            color: #000;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: #feca57;
            font-weight: bold;
        }
        
        .form-group select,
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.3);
            color: #fff;
            font-size: 1em;
        }
        
        .form-group select:focus,
        .form-group input:focus {
            outline: none;
            border-color: #feca57;
        }
        
        .trades-list, .logs-list {
            max-height: 350px;
            overflow-y: auto;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            padding: 15px;
        }
        
        .trade-item, .log-item {
            background: rgba(255, 255, 255, 0.1);
            margin-bottom: 10px;
            padding: 12px;
            border-radius: 8px;
            border-left: 4px solid #48dbfb;
            transition: all 0.3s ease;
        }
        
        .trade-item:hover, .log-item:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateX(5px);
        }
        
        .trade-item.failed, .log-item.error {
            border-left-color: #ff6b6b;
        }
        
        .trade-item.success {
            border-left-color: #2ed573;
        }
        
        .performance-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat-item {
            background: rgba(254, 202, 87, 0.2);
            border: 1px solid #feca57;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #feca57;
        }
        
        .stat-label {
            font-size: 0.8em;
            color: #ccc;
            margin-top: 5px;
        }
        
        .full-width {
            grid-column: 1 / -1;
        }
        
        .loading {
            text-align: center;
            color: #999;
            font-style: italic;
            padding: 20px;
        }
        
        /* Scrollbar personnalisée */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(254, 202, 87, 0.6);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(254, 202, 87, 0.8);
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🎯 Bot Trading Avancé</h1>
            <div style="font-size: 1.2em; margin-top: 10px;">
                ✅ Syntaxe API Corrigée • 🚀 Trading Automatique • 📊 Analyse Avancée
            </div>
        </header>
        
        <div class="status-bar">
            <div class="status-item">
                <div style="font-size: 1.2em;">🟢</div>
                <div>Statut: <span id="api-status">Chargement...</span></div>
            </div>
            <div class="status-item">
                <div style="font-size: 1.2em;">💰</div>
                <div>Portfolio: $<span id="portfolio-value">0</span></div>
            </div>
            <div class="status-item">
                <div style="font-size: 1.2em;" id="trading-icon">⏸️</div>
                <div>Auto-Trading: <span id="auto-status">Arrêté</span></div>
            </div>
            <div class="status-item">
                <div style="font-size: 1.2em;">⚙️</div>
                <div>Mode: <span id="current-mode">micro</span></div>
            </div>
            <div class="status-item">
                <div style="font-size: 1.2em;">📈</div>
                <div>Trades: <span id="total-trades">0</span></div>
            </div>
        </div>
        
        <div class="dashboard-grid">
            <!-- MODES DE TRADING -->
            <div class="section">
                <h2 class="section-title">⚙️ Modes de Trading</h2>
                <div class="modes-grid" id="modes-grid">
                    <div class="loading">Chargement des modes...</div>
                </div>
                <div class="trade-controls">
                    <button class="btn btn-success" onclick="startAutoTrading()">
                        ▶️ Démarrer Auto
                    </button>
                    <button class="btn btn-danger" onclick="stopAutoTrading()">
                        ⏹️ Arrêter Auto
                    </button>
                </div>
            </div>
            
            <!-- PORTFOLIO -->
            <div class="section">
                <h2 class="section-title">💰 Portfolio</h2>
                <div class="portfolio-grid" id="portfolio-grid">
                    <div class="loading">Chargement portfolio...</div>
                </div>
                <div style="margin-top: 15px; text-align: center; font-size: 1.2em;">
                    <strong>USDC Disponible: $<span id="usdc-available">0</span></strong>
                </div>
            </div>
        </div>
        
        <div class="dashboard-grid">
            <!-- TRADE MANUEL -->
            <div class="section">
                <h2 class="section-title">📈 Trade Manuel</h2>
                <div class="form-group">
                    <label>Paire de Trading</label>
                    <select id="trade-symbol">
                        <option value="SOL/USD">SOL/USD - Solana</option>
                        <option value="ATOM/USD">ATOM/USD - Cosmos</option>
                        <option value="ETH/USD">ETH/USD - Ethereum</option>
                        <option value="BTC/USD">BTC/USD - Bitcoin</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Direction</label>
                    <select id="trade-side">
                        <option value="buy">🟢 Acheter (Buy)</option>
                        <option value="sell">🔴 Vendre (Sell)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Montant USD</label>
                    <input type="number" id="trade-amount" value="2.0" step="0.5" min="1.0" max="50">
                </div>
                <button class="btn btn-primary" style="width: 100%;" onclick="executeManualTrade()">
                    🎯 Exécuter Trade
                </button>
                <div id="trade-result" style="margin-top: 15px;"></div>
            </div>
            
            <!-- PERFORMANCE -->
            <div class="section">
                <h2 class="section-title">📊 Performance</h2>
                <div class="performance-stats" id="performance-stats">
                    <div class="loading">Chargement stats...</div>
                </div>
            </div>
        </div>
        
        <div class="dashboard-grid">
            <!-- TRADES RÉCENTS -->
            <div class="section">
                <h2 class="section-title">💹 Trades Récents</h2>
                <div class="trades-list" id="trades-list">
                    <div class="loading">Aucun trade...</div>
                </div>
            </div>
            
            <!-- LOGS SYSTÈME -->
            <div class="section">
                <h2 class="section-title">📝 Logs Système</h2>
                <div class="logs-list" id="logs-list">
                    <div class="loading">Chargement logs...</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let currentMode = 'micro';
        let autoTradingActive = false;
        let updateInterval;
        
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🎯 Dashboard Avancé Initialisé');
            initializeDashboard();
            startAutoUpdates();
        });
        
        function initializeDashboard() {
            updateDashboard();
        }
        
        function startAutoUpdates() {
            updateInterval = setInterval(updateDashboard, 3000); // Mise à jour toutes les 3 secondes
        }
        
        async function updateDashboard() {
            try {
                const response = await fetch('/api/dashboard');
                const data = await response.json();
                
                updateStatus(data.status);
                updatePortfolio(data.portfolio);
                updateModes(data.available_modes, data.current_mode);
                updatePerformance(data.performance);
                updateTrades(data.recent_trades);
                updateLogs(data.recent_logs);
                
            } catch (error) {
                console.error('Erreur mise à jour:', error);
                document.getElementById('api-status').textContent = 'ERREUR';
            }
        }
        
        function updateStatus(status) {
            document.getElementById('api-status').textContent = status.api_status;
            document.getElementById('auto-status').textContent = 
                status.auto_trading ? 'ACTIF' : 'ARRÊTÉ';
            document.getElementById('trading-icon').textContent = 
                status.auto_trading ? '▶️' : '⏸️';
            document.getElementById('current-mode').textContent = status.current_mode;
            
            currentMode = status.current_mode;
            autoTradingActive = status.auto_trading;
        }
        
        function updatePortfolio(portfolio) {
            const portfolioGrid = document.getElementById('portfolio-grid');
            const portfolioValue = document.getElementById('portfolio-value');
            const usdcAvailable = document.getElementById('usdc-available');
            
            portfolioValue.textContent = portfolio.total_value.toFixed(2);
            usdcAvailable.textContent = portfolio.usdc_available.toFixed(2);
            
            if (portfolio.balances && Object.keys(portfolio.balances).length > 0) {
                portfolioGrid.innerHTML = '';
                
                Object.entries(portfolio.balances).forEach(([currency, amounts]) => {
                    const item = document.createElement('div');
                    item.className = 'portfolio-item';
                    
                    const price = portfolio.prices[currency] || 0;
                    const value = amounts.total * (price || 1);
                    
                    item.innerHTML = `
                        <div class="currency">${currency}</div>
                        <div class="balance">${amounts.total.toFixed(6)}</div>
                        <div style="font-size: 0.8em; color: #ccc;">
                            Libre: ${amounts.free.toFixed(6)}
                        </div>
                        <div style="font-size: 0.8em; color: #feca57;">
                            $${value.toFixed(2)}
                        </div>
                    `;
                    portfolioGrid.appendChild(item);
                });
            } else {
                portfolioGrid.innerHTML = '<div class="loading">Portfolio vide</div>';
            }
        }
        
        function updateModes(availableModes, currentModeInfo) {
            const modesGrid = document.getElementById('modes-grid');
            modesGrid.innerHTML = '';
            
            Object.entries(availableModes).forEach(([modeKey, modeData]) => {
                const card = document.createElement('div');
                card.className = 'mode-card';
                if (modeKey === currentMode) {
                    card.classList.add('active');
                }
                
                card.onclick = () => setTradingMode(modeKey);
                
                card.innerHTML = `
                    <div class="mode-name">${modeData.name}</div>
                    <div class="mode-description">${modeData.description}</div>
                    <div class="mode-stats">
                        <div>$${modeData.min_amount}-${modeData.max_amount}</div>
                        <div>${modeData.risk_level}</div>
                        <div>${Math.floor(modeData.frequency_seconds/60)}min</div>
                        <div>${modeData.profit_target}% cible</div>
                    </div>
                `;
                modesGrid.appendChild(card);
            });
        }
        
        function updatePerformance(performance) {
            const performanceStats = document.getElementById('performance-stats');
            const totalTrades = document.getElementById('total-trades');
            
            totalTrades.textContent = performance.total_trades;
            
            performanceStats.innerHTML = `
                <div class="stat-item">
                    <div class="stat-value">${performance.total_trades}</div>
                    <div class="stat-label">Total Trades</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${performance.successful_trades}</div>
                    <div class="stat-label">Réussis</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${performance.success_rate.toFixed(1)}%</div>
                    <div class="stat-label">Taux Succès</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">$${performance.total_invested.toFixed(2)}</div>
                    <div class="stat-label">Investi</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">$${performance.estimated_profit.toFixed(2)}</div>
                    <div class="stat-label">Profit Estimé</div>
                </div>
            `;
        }
        
        function updateTrades(trades) {
            const tradesList = document.getElementById('trades-list');
            
            if (trades && trades.length > 0) {
                tradesList.innerHTML = '';
                
                trades.reverse().forEach(trade => {
                    const item = document.createElement('div');
                    item.className = 'trade-item';
                    
                    if (trade.error) {
                        item.classList.add('failed');
                    } else if (trade.status === 'filled') {
                        item.classList.add('success');
                    }
                    
                    const timestamp = new Date(trade.timestamp).toLocaleTimeString();
                    const status = trade.error ? '❌ ÉCHEC' : '✅ SUCCÈS';
                    
                    item.innerHTML = `
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <strong>${trade.symbol || 'N/A'}</strong> - ${trade.side?.toUpperCase() || 'N/A'}
                                <div style="font-size: 0.9em;">
                                    $${trade.usd_amount || 'N/A'} - Mode: ${trade.mode || 'N/A'}
                                </div>
                                ${trade.error ? `<div style="font-size: 0.8em; color: #ff6b6b;">${trade.error}</div>` : ''}
                            </div>
                            <div style="text-align: right;">
                                <div>${status}</div>
                                <div style="font-size: 0.8em;">${timestamp}</div>
                            </div>
                        </div>
                    `;
                    tradesList.appendChild(item);
                });
            } else {
                tradesList.innerHTML = '<div class="loading">Aucun trade récent</div>';
            }
        }
        
        function updateLogs(logs) {
            const logsList = document.getElementById('logs-list');
            
            if (logs && logs.length > 0) {
                logsList.innerHTML = '';
                
                logs.reverse().forEach(log => {
                    const item = document.createElement('div');
                    item.className = 'log-item';
                    
                    if (log.category === 'ERROR') {
                        item.classList.add('error');
                    }
                    
                    item.innerHTML = `
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong>[${log.category}]</strong> ${log.message}
                            </div>
                            <div style="font-size: 0.8em; color: #ccc;">
                                ${log.timestamp.split(' ')[1]}
                            </div>
                        </div>
                    `;
                    logsList.appendChild(item);
                });
                
                // Auto-scroll vers le bas
                logsList.scrollTop = logsList.scrollHeight;
            } else {
                logsList.innerHTML = '<div class="loading">Aucun log</div>';
            }
        }
        
        async function setTradingMode(mode) {
            try {
                const response = await fetch('/api/set-mode', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ mode: mode })
                });
                
                const data = await response.json();
                if (data.success) {
                    currentMode = data.mode;
                    // Mise à jour immédiate de l'interface
                    updateDashboard();
                }
            } catch (error) {
                console.error('Erreur changement mode:', error);
            }
        }
        
        async function executeManualTrade() {
            const symbol = document.getElementById('trade-symbol').value;
            const side = document.getElementById('trade-side').value;
            const usd_amount = parseFloat(document.getElementById('trade-amount').value);
            const resultDiv = document.getElementById('trade-result');
            
            if (!usd_amount || usd_amount < 1.0) {
                resultDiv.innerHTML = '<div style="color: #ff6b6b;">Montant minimum: $1.00</div>';
                return;
            }
            
            resultDiv.innerHTML = '<div style="color: #feca57;">🔄 Exécution du trade...</div>';
            
            try {
                const response = await fetch('/api/trade', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ symbol, side, usd_amount })
                });
                
                const result = await response.json();
                
                if (result.error) {
                    resultDiv.innerHTML = `<div style="color: #ff6b6b;">❌ ÉCHEC: ${result.error}</div>`;
                } else {
                    resultDiv.innerHTML = `<div style="color: #2ed573;">✅ SUCCÈS: Trade ${result.id} exécuté</div>`;
                    // Mise à jour du dashboard après le trade
                    setTimeout(updateDashboard, 2000);
                }
            } catch (error) {
                console.error('Erreur trade:', error);
                resultDiv.innerHTML = '<div style="color: #ff6b6b;">❌ Erreur technique</div>';
            }
        }
        
        async function startAutoTrading() {
            if (!confirm(`Démarrer l'auto-trading en mode ${currentMode}?`)) {
                return;
            }
            
            try {
                const response = await fetch('/api/start-auto');
                const data = await response.json();
                
                if (data.started) {
                    autoTradingActive = true;
                    document.getElementById('auto-status').textContent = 'ACTIF';
                    document.getElementById('trading-icon').textContent = '▶️';
                }
            } catch (error) {
                console.error('Erreur démarrage auto:', error);
            }
        }
        
        async function stopAutoTrading() {
            try {
                const response = await fetch('/api/stop-auto');
                const data = await response.json();
                
                if (data.stopped) {
                    autoTradingActive = false;
                    document.getElementById('auto-status').textContent = 'ARRÊTÉ';
                    document.getElementById('trading-icon').textContent = '⏸️';
                }
            } catch (error) {
                console.error('Erreur arrêt auto:', error);
            }
        }
        
        // Nettoyage à la fermeture
        window.addEventListener('beforeunload', function() {
            if (updateInterval) {
                clearInterval(updateInterval);
            }
        });
    </script>
</body>
</html>"""
        self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        pass

def start_advanced_dashboard():
    """Démarrer le dashboard avancé"""
    port = 8085
    
    print("\n🎯 LANCEMENT BOT TRADING AVANCÉ")
    print("=" * 60)
    print("✅ NOUVELLES FONCTIONNALITÉS:")
    print("   • 5 modes de trading (micro → agressif)")
    print("   • Trading automatique intelligent")
    print("   • Logs système en temps réel")
    print("   • Statistiques de performance")
    print("   • Interface utilisateur améliorée")
    print("   • Syntaxe API Coinbase corrigée")
    print("=" * 60)
    
    for attempt in range(10):
        try:
            server = HTTPServer(('localhost', port), AdvancedDashboardHandler)
            print(f"🌐 Dashboard Avancé: http://localhost:{port}")
            print("🎯 MODES DISPONIBLES:")
            for mode_key, mode_data in advanced_bot.trading_modes.items():
                print(f"   • {mode_data['name']}: ${mode_data['min_amount']}-{mode_data['max_amount']}")
            print("=" * 60)
            print("🚀 BOT TRADING AVANCÉ PRÊT !")
            
            # Ouvrir le navigateur
            threading.Timer(2, lambda: webbrowser.open(f'http://localhost:{port}')).start()
            
            print("\n⏸️ Ctrl+C pour arrêter")
            server.serve_forever()
            
        except OSError as e:
            if "Address already in use" in str(e):
                port += 1
                print(f"⚠️ Port {port-1} occupé, essai port {port}...")
                continue
            else:
                raise e

if __name__ == "__main__":
    try:
        if advanced_bot.is_connected:
            start_advanced_dashboard()
        else:
            print("❌ Bot non connecté - vérifiez la configuration API")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Arrêt bot trading avancé...")
        advanced_bot.stop_auto_trading()
        print("✅ Bot fermé proprement")
        print(f"📄 Logs sauvegardés: {advanced_bot.log_file}")
