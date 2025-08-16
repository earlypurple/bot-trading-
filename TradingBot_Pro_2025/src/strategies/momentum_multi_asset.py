from .base_strategy import BaseStrategy
import requests
import logging

class MomentumMultiAsset(BaseStrategy):
    """
    Multi-Asset Momentum Strategy based on real-time price data.
    This simplified version fetches the current price of an asset and makes a decision.
    """

    def __init__(self, asset_id='bitcoin', currency='usd', threshold=50000):
        super().__init__(
            name="Momentum Multi-Asset (Live)",
            description=f"Live momentum trading for {asset_id} in {currency}."
        )
        self.asset_id = asset_id
        self.currency = currency
        self.api_url = f"https://api.coingecko.com/api/v3/simple/price?ids={self.asset_id}&vs_currencies={self.currency}"
        self.threshold = threshold # Example threshold for trading logic

    def execute(self):
        """
        Execute the momentum strategy using live data from CoinGecko.
        """
        if self.status != "RUNNING":
            return

        logging.info(f"Executing {self.name} for {self.asset_id}...")

        # 1. Fetch live data
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            price = data[self.asset_id][self.currency]
            logging.info(f"Current price of {self.asset_id}: ${price:,.2f}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data from CoinGecko: {e}")
            return
        except (KeyError, TypeError) as e:
            logging.error(f"Error parsing CoinGecko response: {e}")
            return

        # 2. Execute simulated trade based on a simple threshold
        if price > self.threshold:
            logging.info(f"Price ${price:,.2f} is above threshold ${self.threshold:,.2f}. SIMULATE BUY.")
        else:
            logging.info(f"Price ${price:,.2f} is not above threshold ${self.threshold:,.2f}. SIMULATE SELL/HOLD.")
