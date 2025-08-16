import os
from flask import Flask, jsonify, send_from_directory, request

# Strategy imports
from strategies.scalping_quantique import ScalpingQuantique
from strategies.grid_adaptive_ia import GridAdaptiveIA
from strategies.cross_chain_arbitrage import CrossChainArbitrage
from strategies.defi_yield_farming import DeFiYieldFarming
from strategies.momentum_multi_asset import MomentumMultiAsset
from strategies.market_making import MarketMaking
from strategies.options import Options
from strategies.pairs_trading import PairsTrading
from strategies.statistical_arbitrage import StatisticalArbitrage

# Compliance import
from compliance.mica_sec_checker import MicaSecChecker

# Determine the correct static folder path
static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'public'))

app = Flask(__name__, static_folder=static_folder, static_url_path='')

# In-memory status for the bot and strategies
bot_status = {"status": "OFF", "active_strategies": []}
daily_capital = {"amount": 1000.0} # Default daily capital
strategies = {
    "scalping_quantique": ScalpingQuantique(),
    "grid_adaptive_ia": GridAdaptiveIA(),
    "cross_chain_arbitrage": CrossChainArbitrage(),
    "defi_yield_farming": DeFiYieldFarming(),
    "momentum_multi_asset": MomentumMultiAsset(asset_ticker='BTC-USD', model_path='btc_momentum_model.pkl'),
    "market_making": MarketMaking(),
    "options": Options(),
    "pairs_trading": PairsTrading(),
    "statistical_arbitrage": StatisticalArbitrage(),
}
compliance_checker = MicaSecChecker()

@app.route('/api/compliance/status', methods=['GET'])
def get_compliance_status():
    """API endpoint to get the compliance status."""
    return jsonify(compliance_checker.get_compliance_report())

@app.route('/api/status', methods=['GET'])
def get_bot_status():
    """API endpoint to get the main bot status."""
    active_strategies = [s.get_status() for s in strategies.values() if s.status == 'RUNNING']
    bot_status['active_strategies'] = active_strategies

    response_data = {
        "bot_status": bot_status,
        "daily_capital": daily_capital
    }
    return jsonify(response_data)

@app.route('/api/capital', methods=['POST'])
def set_daily_capital():
    """API endpoint to set the daily trading capital."""
    data = request.get_json()
    amount = data.get('amount')
    if amount is not None and isinstance(amount, (int, float)) and amount > 0:
        daily_capital['amount'] = amount
        return jsonify(daily_capital)
    return jsonify({"error": "Invalid amount"}), 400

@app.route('/api/toggle-bot', methods=['POST'])
def toggle_bot():
    """API endpoint to toggle the bot ON/OFF."""
    if bot_status['status'] == 'OFF':
        bot_status['status'] = 'ON'
    else:
        bot_status['status'] = 'OFF'
        # Also stop all strategies when turning the bot off
        for strategy in strategies.values():
            strategy.stop()
    return jsonify(bot_status)


@app.route('/api/strategies', methods=['GET'])
def get_strategies():
    """API endpoint to get the list of available strategies."""
    return jsonify([s.get_status() for s in strategies.values()])

@app.route('/api/strategies/<strategy_name>', methods=['GET'])
def get_strategy_status(strategy_name):
    """API endpoint to get the status of a specific strategy."""
    strategy = strategies.get(strategy_name)
    if strategy:
        return jsonify(strategy.get_status())
    return jsonify({"error": "Strategy not found"}), 404

@app.route('/api/strategies/<strategy_name>/start', methods=['POST'])
def start_strategy(strategy_name):
    """API endpoint to start a strategy."""
    strategy = strategies.get(strategy_name)
    if not strategy:
        return jsonify({"error": "Strategy not found"}), 404

    if bot_status['status'] == 'OFF':
        return jsonify({"error": "Bot is turned off. Cannot start strategy."}), 400

    strategy.start()
    return jsonify(strategy.get_status())

@app.route('/api/strategies/<strategy_name>/stop', methods=['POST'])
def stop_strategy(strategy_name):
    """API endpoint to stop a strategy."""
    strategy = strategies.get(strategy_name)
    if strategy:
        strategy.stop()
        return jsonify(strategy.get_status())
    return jsonify({"error": "Strategy not found"}), 404

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serves the frontend application."""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
