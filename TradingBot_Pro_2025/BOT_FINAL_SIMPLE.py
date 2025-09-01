#!/usr/bin/env python3
"""
🎯 BOT TRADING FINAL SIMPLIFIÉ 
Version allégée pour identifier les problèmes de lancement
"""
import os
import sys
import json
import time
import threading
import webbrowser
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

print("🎯 DÉMARRAGE BOT FINAL SIMPLIFIÉ...")

try:
    import ccxt
    print("✅ Module ccxt importé")
except ImportError as e:
    print(f"❌ ERREUR ccxt: {e}")
    sys.exit(1)

class SimpleFinalBot:
    """Version simplifiée du bot final"""
    
    def __init__(self):
        print("🔧 Initialisation bot simplifié...")
        self.exchange = None
        self.is_connected = False
        self.portfolio = {}
        self.prices = {}
        
        try:
            # Configuration API
            print("📡 Configuration API...")
            with open('cdp_api_key.json', 'r') as f:
                config = json.load(f)
            
            print(f"🔑 API: {config['name'].split('/')[-1]}")
            
            # Exchange
            print("🏦 Connexion exchange...")
            self.exchange = ccxt.coinbaseadvanced({
                'apiKey': config['name'],
                'secret': config['privateKey'],
                'passphrase': '',
                'sandbox': False,
                'enableRateLimit': True,
                'timeout': 30000,
                'options': {
                    'createMarketBuyOrderRequiresPrice': False,  # ✅ CLEF !
                    'advanced': True,
                }
            })
            
            print("✅ Exchange configuré")
            
            # Test de base
            print("🧪 Test connexion...")
            balance = self.exchange.fetch_balance()
            print("✅ API fonctionnelle")
            
            self.is_connected = True
            print("🎯 Bot simplifié initialisé avec succès !")
            
        except Exception as e:
            print(f"❌ Erreur init: {e}")
            import traceback
            traceback.print_exc()
    
    def get_portfolio(self):
        """Récupérer portfolio"""
        try:
            balance = self.exchange.fetch_balance()
            portfolio = {}
            total_value = 0
            
            for currency, amounts in balance.items():
                if isinstance(amounts, dict) and amounts.get('total', 0) > 0:
                    portfolio[currency] = amounts
                    if currency in ['USD', 'USDC', 'USDT']:
                        total_value += amounts['total']
            
            return {'balances': portfolio, 'total_value': total_value}
        except Exception as e:
            print(f"❌ Erreur portfolio: {e}")
            return {'balances': {}, 'total_value': 0}
    
    def execute_test_trade(self, symbol='SOL/USD', usd_amount=1.5):
        """Test trade avec syntaxe finale"""
        try:
            print(f"🎯 TEST TRADE: {symbol} ${usd_amount}")
            
            # Vérifications
            portfolio = self.get_portfolio()
            usdc_available = portfolio['balances'].get('USDC', {}).get('free', 0)
            
            if usdc_available < usd_amount:
                return {'error': f'USDC insuffisant: ${usdc_available:.2f}'}
            
            # Prix actuel
            ticker = self.exchange.fetch_ticker(symbol)
            current_price = ticker['last']
            
            print(f"💰 USDC: ${usdc_available:.2f}")
            print(f"💱 Prix {symbol}: ${current_price:.2f}")
            
            # ✅ TRADE FINAL avec syntaxe corrigée
            order = self.exchange.create_order(
                symbol=symbol,
                type='market',
                side='buy',
                amount=usd_amount,  # ✅ Cost USD directement !
                price=None
            )
            
            print(f"✅ TRADE RÉUSSI: {order.get('id', 'N/A')}")
            
            return {
                'success': True,
                'id': order.get('id', f'test_{int(time.time())}'),
                'symbol': symbol,
                'usd_amount': usd_amount,
                'price': current_price,
                'status': order.get('status', 'filled')
            }
            
        except Exception as e:
            print(f"❌ Erreur trade: {e}")
            return {'error': str(e)}

# Instance globale
simple_bot = SimpleFinalBot()

class SimpleDashboardHandler(BaseHTTPRequestHandler):
    """Dashboard simplifié"""
    
    def do_GET(self):
        if self.path == '/':
            self._serve_dashboard()
        elif self.path == '/api/status':
            self._send_json({'connected': simple_bot.is_connected})
        elif self.path == '/api/portfolio':
            portfolio = simple_bot.get_portfolio()
            self._send_json(portfolio)
        elif self.path == '/api/test-trade':
            result = simple_bot.execute_test_trade()
            self._send_json(result)
        else:
            self.send_error(404)
    
    def _send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def _serve_dashboard(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """<!DOCTYPE html>
<html>
<head>
    <title>🎯 Bot Final Simplifié</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #1a1a1a; color: #fff; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { background: linear-gradient(45deg, #ff6b6b, #ffd93d); padding: 20px; border-radius: 10px; color: #000; text-align: center; margin-bottom: 20px; }
        .section { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 2px solid #ff6b6b; }
        .btn { background: #ff6b6b; color: #fff; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .btn:hover { background: #ff5252; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .success { background: rgba(76, 205, 196, 0.3); border: 1px solid #4ecdc4; }
        .error { background: rgba(255, 107, 107, 0.3); border: 1px solid #ff6b6b; }
        .portfolio { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }
        .portfolio-item { background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Bot Trading Final</h1>
            <div>✅ SYNTAXE API CORRIGÉE</div>
            <div>🚀 VERSION SIMPLIFIÉE</div>
        </div>
        
        <div class="section">
            <h2>📊 Status</h2>
            <div id="status" class="status">Chargement...</div>
            <button class="btn" onclick="updateStatus()">🔄 Actualiser</button>
        </div>
        
        <div class="section">
            <h2>💰 Portfolio</h2>
            <div id="portfolio" class="portfolio">Chargement...</div>
            <button class="btn" onclick="updatePortfolio()">🔄 Actualiser Portfolio</button>
        </div>
        
        <div class="section">
            <h2>🎯 Test Trade Final</h2>
            <div id="trade-result" class="status">Prêt pour test</div>
            <button class="btn" onclick="testTrade()">🚀 Test Trade $1.50</button>
        </div>
    </div>
    
    <script>
        async function updateStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                document.getElementById('status').innerHTML = 
                    data.connected ? 
                    '<div class="success">✅ API CONNECTÉE - BOT FINAL OPÉRATIONNEL</div>' :
                    '<div class="error">❌ Déconnecté</div>';
            } catch (e) {
                document.getElementById('status').innerHTML = '<div class="error">❌ Erreur: ' + e + '</div>';
            }
        }
        
        async function updatePortfolio() {
            try {
                const response = await fetch('/api/portfolio');
                const data = await response.json();
                
                let html = '';
                if (data.balances && Object.keys(data.balances).length > 0) {
                    Object.entries(data.balances).forEach(([currency, amounts]) => {
                        html += `<div class="portfolio-item">
                            <div><strong>${currency}</strong></div>
                            <div>${amounts.total.toFixed(6)}</div>
                            <div style="font-size: 0.8em;">Libre: ${amounts.free.toFixed(6)}</div>
                        </div>`;
                    });
                    html += `<div class="portfolio-item" style="background: rgba(76, 205, 196, 0.3);">
                        <div><strong>TOTAL</strong></div>
                        <div>$${data.total_value.toFixed(2)}</div>
                    </div>`;
                } else {
                    html = '<div>Portfolio vide</div>';
                }
                
                document.getElementById('portfolio').innerHTML = html;
            } catch (e) {
                document.getElementById('portfolio').innerHTML = '<div class="error">❌ Erreur portfolio</div>';
            }
        }
        
        async function testTrade() {
            try {
                document.getElementById('trade-result').innerHTML = '<div class="status">🔄 Exécution test trade...</div>';
                
                const response = await fetch('/api/test-trade');
                const result = await response.json();
                
                if (result.error) {
                    document.getElementById('trade-result').innerHTML = 
                        `<div class="error">❌ ÉCHEC: ${result.error}</div>`;
                } else {
                    document.getElementById('trade-result').innerHTML = 
                        `<div class="success">✅ SUCCÈS FINAL !<br>
                        ID: ${result.id}<br>
                        ${result.symbol}: $${result.usd_amount}<br>
                        Prix: $${result.price.toFixed(2)}<br>
                        Status: ${result.status}</div>`;
                }
                
                // Actualiser portfolio après trade
                setTimeout(updatePortfolio, 2000);
                
            } catch (e) {
                document.getElementById('trade-result').innerHTML = '<div class="error">❌ Erreur test: ' + e + '</div>';
            }
        }
        
        // Auto-update
        setInterval(() => {
            updateStatus();
            updatePortfolio();
        }, 10000);
        
        // Load initial data
        updateStatus();
        updatePortfolio();
    </script>
</body>
</html>"""
        self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        pass

def start_simple_dashboard():
    """Démarrer dashboard simplifié"""
    port = 8084
    
    print("\n🎯 LANCEMENT DASHBOARD FINAL SIMPLIFIÉ")
    print("=" * 50)
    print("✅ API SYNTAX CORRIGÉE:")
    print("   • createMarketBuyOrderRequiresPrice = False") 
    print("   • Cost USD passé directement dans amount")
    print("   • Tests API validés")
    print("=" * 50)
    
    try:
        server = HTTPServer(('localhost', port), SimpleDashboardHandler)
        print(f"🌐 Dashboard: http://localhost:{port}")
        print("🚀 PRÊT POUR TESTS FINAUX !")
        
        # Ouvrir navigateur
        threading.Timer(2, lambda: webbrowser.open(f'http://localhost:{port}')).start()
        
        print("\n⏸️ Ctrl+C pour arrêter")
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n⏹️ Arrêt bot final...")
        print("✅ Bot fermé proprement")
    except Exception as e:
        print(f"❌ Erreur serveur: {e}")

if __name__ == "__main__":
    if simple_bot.is_connected:
        start_simple_dashboard()
    else:
        print("❌ Bot non connecté - vérifiez l'API")
        sys.exit(1)
