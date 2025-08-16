import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

class MomentumModel:
    """
    A machine learning model to predict stock price direction based on momentum indicators.
    """

    def __init__(self, model_path="momentum_model.pkl"):
        self.model_path = model_path
        self.model = None

    def _prepare_data(self, data):
        """
        Prepares the data by creating features and the target variable.
        """
        df = data.copy()

        # Feature Engineering
        df['returns'] = df['Close'].pct_change()
        df['ma_5'] = df['Close'].rolling(window=5).mean()
        df['ma_20'] = df['Close'].rolling(window=20).mean()

        # Target variable: 1 if the next day's price goes up, 0 otherwise
        df['target'] = (df['returns'].shift(-1) > 0).astype(int)

        # Drop rows with NaN values created by rolling means and pct_change
        df.dropna(inplace=True)

        return df

    def train(self, data):
        """
        Trains the logistic regression model.
        """
        df = self._prepare_data(data)

        features = ['returns', 'ma_5', 'ma_20']
        X = df[features]
        y = df['target']

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        self.model = LogisticRegression(random_state=42)
        self.model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model trained with accuracy: {accuracy:.4f}")

        self.save_model()

    def predict(self, data):
        """
        Makes a prediction on new data.
        """
        if self.model is None:
            raise ValueError("Model has not been trained or loaded yet.")

        df = self._prepare_data(data)
        if df.empty:
            return None # Not enough data to make a prediction

        # Use the most recent data point for prediction
        last_features = df[['returns', 'ma_5', 'ma_20']].iloc[-1:]

        return self.model.predict(last_features)[0]

    def save_model(self):
        """
        Saves the trained model to a file.
        """
        if self.model:
            joblib.dump(self.model, self.model_path)
            print(f"Model saved to {self.model_path}")

    def load_model(self):
        """
        Loads a model from a file.
        """
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            print(f"Model loaded from {self.model_path}")
        else:
            raise FileNotFoundError(f"Model file not found at {self.model_path}")

if __name__ == '__main__':
    # Example usage:
    from ..data.market_data import get_historical_data

    # 1. Get data
    ticker = 'BTC-USD'
    start_date = '2020-01-01'
    end_date = '2023-12-31'
    data = get_historical_data(ticker, start_date, end_date)

    if data is not None:
        # 2. Train model
        model = MomentumModel(model_path="btc_momentum_model.pkl")
        model.train(data)

        # 3. Make a prediction on the last 30 days of data
        prediction_data = data.tail(30)
        prediction = model.predict(prediction_data)
        print(f"Prediction for the next day's direction (1=UP, 0=DOWN): {prediction}")

        # 4. Load the model and make another prediction
        loaded_model = MomentumModel(model_path="btc_momentum_model.pkl")
        loaded_model.load_model()
        prediction = loaded_model.predict(prediction_data)
        print(f"Prediction from loaded model: {prediction}")
