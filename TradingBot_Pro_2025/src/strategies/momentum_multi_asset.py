from .base_strategy import BaseStrategy
from models.momentum_model import MomentumModel
from data.market_data import get_historical_data
import os
import datetime

class MomentumMultiAsset(BaseStrategy):
    """
    Multi-Asset Momentum Strategy: Trades assets (crypto, stocks, metals) based on strong momentum signals.
    This version uses a trained AI model to predict price direction.
    """

    def __init__(self, min_bet=1.0, asset_ticker='BTC-USD', model_path='btc_momentum_model.pkl'):
        super().__init__(
            name="Momentum Multi-Asset",
            description=f"AI-powered momentum trading for {asset_ticker}."
        )
        self.min_bet = min_bet
        self.asset_ticker = asset_ticker
        self.model_path = model_path
        self.model = self._load_model()

    def _load_model(self):
        """Loads the pre-trained model for the strategy."""
        if not os.path.exists(self.model_path):
            print(f"Model file not found at {self.model_path}. Please train the model first.")
            return None

        model = MomentumModel(model_path=self.model_path)
        model.load_model()
        return model

    def execute(self):
        """
        Execute the multi-asset momentum strategy for a single asset.
        """
        if self.status != "RUNNING" or self.model is None:
            if self.model is None:
                print("Cannot execute strategy: Model is not loaded.")
            return

        print(f"Executing {self.name} for {self.asset_ticker}...")

        # 1. Fetch recent data needed for prediction
        # We need at least 20 historical data points for the moving average features
        # and one more for the percentage change. Fetching data from the last 60 days.
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=60)

        try:
            prediction_data = get_historical_data(self.asset_ticker, start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'))
            if prediction_data is None or len(prediction_data) < 21:
                print("Not enough recent data to make a prediction.")
                return
        except Exception as e:
            print(f"Error fetching data for {self.asset_ticker}: {e}")
            return

        # 2. Get prediction from the model
        prediction = self.model.predict(prediction_data)

        # 3. Execute simulated trade
        if prediction == 1:
            print(f"SIMULATE TRADE: Model predicts UP. Placing BUY order for {self.asset_ticker} with min bet {self.min_bet}.")
        else:
            print(f"SIMULATE TRADE: Model predicts DOWN. Placing SELL order for {self.asset_ticker} with min bet {self.min_bet}.")

    def backtest(self, data):
        """
        Backtests the strategy on historical data.
        """
        if self.model is None:
            print("Cannot backtest: Model is not loaded.")
            return

        print(f"--- Starting Backtest for {self.name} on {self.asset_ticker} ---")

        # Prepare data with features
        # Note: In a real scenario, you'd avoid lookahead bias by calculating features iteratively.
        # For this baseline, we pre-calculate for simplicity.
        df = self.model._prepare_data(data)
        features = ['returns', 'ma_5', 'ma_20']

        capital = 10000  # Starting capital
        position = 0  # 0 for no position, 1 for long
        trades = 0

        for i in range(len(df) - 1):
            current_features = df[features].iloc[i:i+1]
            actual_return = df['returns'].iloc[i+1]

            prediction = self.model.model.predict(current_features)[0]

            # Trading logic
            if prediction == 1 and position == 0: # Buy signal and not in position
                position = 1
                trades += 1
                # print(f"Day {df.index[i].date()}: BUY")
            elif prediction == 0 and position == 1: # Sell signal and in position
                position = 0
                # print(f"Day {df.index[i].date()}: SELL")

            # Update capital
            if position == 1:
                capital *= (1 + actual_return)

        final_capital = capital
        total_return = (final_capital - 10000) / 10000 * 100

        print(f"--- Backtest Results ---")
        print(f"Initial Capital: $10,000")
        print(f"Final Capital: ${final_capital:,.2f}")
        print(f"Total Return: {total_return:.2f}%")
        print(f"Total Trades: {trades}")
        print(f"------------------------")

if __name__ == '__main__':
    # Example of how to run this strategy and backtest it

    # Ensure the model exists by running momentum_model.py first if needed
    if not os.path.exists('btc_momentum_model.pkl'):
        print("Training model first...")
        from TradingBot_Pro_2025.src.models.momentum_model import MomentumModel
        training_data = get_historical_data('BTC-USD', '2020-01-01', '2022-12-31')
        if training_data is not None:
            model = MomentumModel(model_path="btc_momentum_model.pkl")
            model.train(training_data)

    # --- Run Live Execution Example ---
    print("\n--- Running Live Execution Example ---")
    strategy = MomentumMultiAsset()
    if strategy.model:
        strategy.start()
        strategy.execute()
        strategy.stop()
    else:
        print("Strategy could not be initialized.")

    # --- Run Backtesting Example ---
    print("\n--- Running Backtesting Example ---")
    backtest_data = get_historical_data('BTC-USD', '2023-01-01', '2023-12-31')
    if backtest_data is not None and strategy.model:
        strategy.backtest(backtest_data)
