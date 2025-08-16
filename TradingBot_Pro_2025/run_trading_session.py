from src.data.market_data import get_historical_data
from src.models.momentum_model import MomentumModel
from src.strategies.momentum_multi_asset import MomentumMultiAsset
import os

def run_session():
    """
    Orchestrates a full trading session:
    1. Trains the model if it doesn't exist.
    2. Runs a backtest on historical data.
    3. Simulates one live trade execution.
    """
    ASSET_TICKER = 'BTC-USD'
    MODEL_PATH = 'btc_momentum_model.pkl'

    TRAIN_START_DATE = '2020-01-01'
    TRAIN_END_DATE = '2022-12-31'

    BACKTEST_START_DATE = '2023-01-01'
    BACKTEST_END_DATE = '2023-12-31'

    print("--- Starting Trading Session ---")

    # 1. Train the model if it doesn't exist
    if not os.path.exists(MODEL_PATH):
        print(f"\nModel not found. Training a new model for {ASSET_TICKER}...")
        training_data = get_historical_data(ASSET_TICKER, TRAIN_START_DATE, TRAIN_END_DATE)
        if training_data is not None:
            model = MomentumModel(model_path=MODEL_PATH)
            model.train(training_data)
        else:
            print("Could not download training data. Aborting.")
            return
    else:
        print(f"\nFound existing model at {MODEL_PATH}.")

    # Initialize the strategy (which will load the model)
    strategy = MomentumMultiAsset(asset_ticker=ASSET_TICKER, model_path=MODEL_PATH)

    if not strategy.model:
        print("Failed to load model into strategy. Aborting.")
        return

    # 2. Run Backtest
    print(f"\nRunning backtest for {ASSET_TICKER} from {BACKTEST_START_DATE} to {BACKTEST_END_DATE}...")
    backtest_data = get_historical_data(ASSET_TICKER, BACKTEST_START_DATE, BACKTEST_END_DATE)
    if backtest_data is not None:
        strategy.backtest(backtest_data)
    else:
        print("Could not download backtesting data.")

    # 3. Simulate a single live execution
    print("\n--- Simulating a single live trade ---")
    strategy.start()
    strategy.execute()
    strategy.stop()

    print("\n--- Trading Session Finished ---")

if __name__ == '__main__':
    run_session()
