import os
import time
import threading
import logging
from flask import Flask, jsonify, send_from_directory, request, current_app

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

def setup_logging(app_instance):
    """Configures logging for the application."""
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend.log')
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add handler to the root logger to catch logs from other modules
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().setLevel(logging.INFO)

    # Add handler to the Flask app's logger
    app_instance.logger.addHandler(file_handler)
    app_instance.logger.setLevel(logging.INFO)

    # Also log to console for development
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logging.getLogger().addHandler(stream_handler)
    app_instance.logger.addHandler(stream_handler)


setup_logging(app)


# In-memory status for the bot and strategies
bot_status = {"status": "OFF", "active_strategies": []}
daily_capital = {"amount": 1000.0} # Default daily capital
strategies = {
    "scalping_quantique": ScalpingQuantique(),
    "grid_adaptive_ia": GridAdaptiveIA(),
    "cross_chain_arbitrage": CrossChainArbitrage(),
    "defi_yield_farming": DeFiYieldFarming(),
    "momentum_multi_asset": MomentumMultiAsset(),
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
    current_app.logger.info("Received request to toggle bot status.")
    if bot_status['status'] == 'OFF':
        bot_status['status'] = 'ON'
        current_app.logger.info("Bot has been turned ON.")
    else:
        bot_status['status'] = 'OFF'
        current_app.logger.info("Bot has been turned OFF.")
        # Also stop all strategies when turning the bot off
        for strategy in strategies.values():
            if strategy.status == 'RUNNING':
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
        current_app.logger.error(f"Attempted to start non-existent strategy: {strategy_name}")
        return jsonify({"error": "Strategy not found"}), 404

    if bot_status['status'] == 'OFF':
        current_app.logger.warning(f"Attempted to start strategy '{strategy_name}' while bot is OFF.")
        return jsonify({"error": "Bot is turned off. Cannot start strategy."}), 400

    strategy.start()
    current_app.logger.info(f"Strategy '{strategy_name}' started via API.")
    return jsonify(strategy.get_status())

@app.route('/api/strategies/<strategy_name>/stop', methods=['POST'])
def stop_strategy(strategy_name):
    """API endpoint to stop a strategy."""
    strategy = strategies.get(strategy_name)
    if strategy:
        strategy.stop()
        current_app.logger.info(f"Strategy '{strategy_name}' stopped via API.")
        return jsonify(strategy.get_status())
    current_app.logger.error(f"Attempted to stop non-existent strategy: {strategy_name}")
    return jsonify({"error": "Strategy not found"}), 404

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serves the frontend application."""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

def trading_loop():
    """
    The main trading loop that runs in a background thread.
    """
    logging.info("Trading loop started.")
    while True:
        # Check if the bot is ON
        if bot_status['status'] == 'ON':
            # logging.debug("Bot is ON, executing strategies...")
            for strategy_name, strategy_instance in strategies.items():
                if strategy_instance.status == 'RUNNING':
                    try:
                        strategy_instance.execute()
                    except Exception as e:
                        logging.error(f"Error executing strategy {strategy_name}: {e}")
        # else:
        #     logging.debug("Bot is OFF, sleeping.")

        time.sleep(5) # The loop runs every 5 seconds

if __name__ == '__main__':
    # Start the trading loop in a background thread
    trader_thread = threading.Thread(target=trading_loop, daemon=True)
    trader_thread.start()

    # Start the Flask app
    app.logger.info("Starting Flask app...")
    app.run(debug=True, port=5000, use_reloader=False) # use_reloader=False is important for threads
