"""
🧠 ENTRAÎNEMENT MODÈLE IA ULTRA-AVANCÉ - TRADINGBOT PRO 2025 ULTRA
Système d'entraînement et d'amélioration continue des modèles d'IA
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import json
from datetime import datetime, timedelta
import logging
import warnings
warnings.filterwarnings('ignore')

# Imports conditionnels pour éviter les erreurs
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("XGBoost non disponible - utilisation de GradientBoosting à la place")

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    print("LightGBM non disponible - utilisation de RandomForest à la place")

try:
    from tensorflow import keras
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("TensorFlow non disponible - utilisation de modèles sklearn uniquement")

class UltraAdvancedModelTrainer:
    """Entraîneur de modèles d'IA ultra-avancé pour trading"""
    
    def __init__(self, data_path: str = None):
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        self.performance_metrics = {}
        self.data_path = data_path
        
        # Configuration du logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def generate_synthetic_data(self, n_samples: int = 10000) -> pd.DataFrame:
        """Générer des données synthétiques pour l'entraînement"""
        self.logger.info(f"Génération de {n_samples} échantillons de données synthétiques...")
        
        np.random.seed(42)
        
        # Générer des données de marché réalistes
        dates = pd.date_range(start='2020-01-01', periods=n_samples, freq='1H')
        
        # Prix de base avec tendance
        base_price = 100
        trend = np.cumsum(np.random.normal(0, 0.1, n_samples))
        noise = np.random.normal(0, 2, n_samples)
        
        prices = base_price + trend + noise
        prices = np.maximum(prices, 1)  # Prix minimum de 1
        
        # Générer les features
        data = pd.DataFrame({
            'timestamp': dates,
            'open': prices,
            'high': prices * (1 + np.abs(np.random.normal(0, 0.02, n_samples))),
            'low': prices * (1 - np.abs(np.random.normal(0, 0.02, n_samples))),
            'close': prices,
            'volume': np.random.lognormal(10, 1, n_samples),
        })
        
        # Calculer les features techniques
        data = self.calculate_technical_features(data)
        
        # Générer les targets (prix futurs)
        data['target_1h'] = data['close'].shift(-1)  # Prix dans 1h
        data['target_4h'] = data['close'].shift(-4)  # Prix dans 4h
        data['target_24h'] = data['close'].shift(-24)  # Prix dans 24h
        
        # Calculer les rendements
        data['return_1h'] = (data['target_1h'] / data['close'] - 1) * 100
        data['return_4h'] = (data['target_4h'] / data['close'] - 1) * 100
        data['return_24h'] = (data['target_24h'] / data['close'] - 1) * 100
        
        # Supprimer les NaN
        data = data.dropna()
        
        self.logger.info(f"Données générées: {len(data)} échantillons avec {len(data.columns)} features")
        return data
    
    def calculate_technical_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculer les indicateurs techniques avancés"""
        
        # Moyennes mobiles
        for period in [5, 10, 20, 50, 100]:
            data[f'sma_{period}'] = data['close'].rolling(window=period).mean()
            data[f'ema_{period}'] = data['close'].ewm(span=period).mean()
        
        # RSI
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = data['close'].ewm(span=12).mean()
        exp2 = data['close'].ewm(span=26).mean()
        data['macd'] = exp1 - exp2
        data['macd_signal'] = data['macd'].ewm(span=9).mean()
        data['macd_histogram'] = data['macd'] - data['macd_signal']
        
        # Bollinger Bands
        data['bb_middle'] = data['close'].rolling(window=20).mean()
        bb_std = data['close'].rolling(window=20).std()
        data['bb_upper'] = data['bb_middle'] + (bb_std * 2)
        data['bb_lower'] = data['bb_middle'] - (bb_std * 2)
        data['bb_width'] = data['bb_upper'] - data['bb_lower']
        data['bb_position'] = (data['close'] - data['bb_lower']) / data['bb_width']
        
        # Stochastic
        low_14 = data['low'].rolling(window=14).min()
        high_14 = data['high'].rolling(window=14).max()
        data['stoch_k'] = 100 * ((data['close'] - low_14) / (high_14 - low_14))
        data['stoch_d'] = data['stoch_k'].rolling(window=3).mean()
        
        # Volume indicators
        data['volume_sma'] = data['volume'].rolling(window=20).mean()
        data['volume_ratio'] = data['volume'] / data['volume_sma']
        
        # Price change features
        data['price_change'] = data['close'].pct_change()
        data['price_change_abs'] = data['price_change'].abs()
        data['volatility'] = data['price_change'].rolling(window=20).std()
        
        # Support and Resistance
        data['support'] = data['low'].rolling(window=20).min()
        data['resistance'] = data['high'].rolling(window=20).max()
        data['support_distance'] = (data['close'] - data['support']) / data['close']
        data['resistance_distance'] = (data['resistance'] - data['close']) / data['close']
        
        # Momentum indicators
        data['momentum'] = data['close'] / data['close'].shift(10) - 1
        data['roc'] = data['close'].pct_change(periods=10)
        
        # Williams %R
        data['williams_r'] = -100 * (high_14 - data['close']) / (high_14 - low_14)
        
        return data
    
    def prepare_features(self, data: pd.DataFrame) -> tuple:
        """Préparer les features pour l'entraînement"""
        
        # Sélectionner les features numériques
        feature_columns = [col for col in data.columns if col not in [
            'timestamp', 'target_1h', 'target_4h', 'target_24h',
            'return_1h', 'return_4h', 'return_24h'
        ]]
        
        # Supprimer les colonnes avec trop de NaN
        numeric_columns = data[feature_columns].select_dtypes(include=[np.number]).columns
        valid_columns = []
        
        for col in numeric_columns:
            if data[col].notna().sum() > len(data) * 0.7:  # Au moins 70% de données valides
                valid_columns.append(col)
        
        X = data[valid_columns].fillna(method='ffill').fillna(method='bfill')
        
        # Targets multiples
        y_1h = data['return_1h'].fillna(0)
        y_4h = data['return_4h'].fillna(0)
        y_24h = data['return_24h'].fillna(0)
        
        self.logger.info(f"Features préparées: {X.shape[1]} features, {len(X)} échantillons")
        return X, y_1h, y_4h, y_24h, valid_columns
    
    def train_ensemble_models(self, X, y, horizon: str = "1h") -> dict:
        """Entraîner un ensemble de modèles pour un horizon donné"""
        self.logger.info(f"Entraînement des modèles pour horizon {horizon}...")
        
        # Split des données
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, shuffle=False
        )
        
        # Normalisation
        scaler = RobustScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        models = {}
        
        # 1. Random Forest
        self.logger.info("Entraînement Random Forest...")
        rf_params = {
            'n_estimators': 200,
            'max_depth': 15,
            'min_samples_split': 5,
            'min_samples_leaf': 2,
            'random_state': 42,
            'n_jobs': -1
        }
        rf_model = RandomForestRegressor(**rf_params)
        rf_model.fit(X_train, y_train)
        models['random_forest'] = rf_model
        
        # 2. Gradient Boosting
        self.logger.info("Entraînement Gradient Boosting...")
        gb_params = {
            'n_estimators': 200,
            'learning_rate': 0.1,
            'max_depth': 8,
            'random_state': 42
        }
        gb_model = GradientBoostingRegressor(**gb_params)
        gb_model.fit(X_train, y_train)
        models['gradient_boosting'] = gb_model
        
        # 3. XGBoost (si disponible)
        if XGBOOST_AVAILABLE:
            self.logger.info("Entraînement XGBoost...")
            xgb_params = {
                'n_estimators': 200,
                'learning_rate': 0.1,
                'max_depth': 8,
                'random_state': 42
            }
            xgb_model = xgb.XGBRegressor(**xgb_params)
            xgb_model.fit(X_train, y_train)
            models['xgboost'] = xgb_model
        
        # 4. LightGBM (si disponible)
        if LIGHTGBM_AVAILABLE:
            self.logger.info("Entraînement LightGBM...")
            lgb_params = {
                'n_estimators': 200,
                'learning_rate': 0.1,
                'max_depth': 8,
                'random_state': 42,
                'verbosity': -1
            }
            lgb_model = lgb.LGBMRegressor(**lgb_params)
            lgb_model.fit(X_train, y_train)
            models['lightgbm'] = lgb_model
        
        # 5. Neural Network (si TensorFlow disponible)
        if TENSORFLOW_AVAILABLE:
            self.logger.info("Entraînement Neural Network...")
            nn_model = self.create_neural_network(X_train_scaled.shape[1])
            nn_model.fit(X_train_scaled, y_train, 
                        epochs=50, batch_size=32, verbose=0,
                        validation_split=0.2)
            models['neural_network'] = nn_model
        
        # Évaluer les modèles
        performance = {}
        for name, model in models.items():
            if name == 'neural_network':
                y_pred = model.predict(X_test_scaled).flatten()
            else:
                y_pred = model.predict(X_test)
            
            performance[name] = {
                'mse': mean_squared_error(y_test, y_pred),
                'mae': mean_absolute_error(y_test, y_pred),
                'r2': r2_score(y_test, y_pred)
            }
        
        # Sauvegarder le meilleur modèle
        best_model_name = min(performance.keys(), key=lambda k: performance[k]['mse'])
        best_model = models[best_model_name]
        
        model_info = {
            'models': models,
            'scaler': scaler,
            'performance': performance,
            'best_model': best_model_name,
            'feature_names': list(X.columns),
            'trained_at': datetime.now().isoformat()
        }
        
        # Sauvegarder
        joblib.dump(model_info, f'models/ensemble_model_{horizon}.pkl')
        
        self.logger.info(f"Meilleur modèle pour {horizon}: {best_model_name} (R²: {performance[best_model_name]['r2']:.4f})")
        
        return model_info
    
    def create_neural_network(self, input_dim: int):
        """Créer un réseau de neurones optimisé"""
        if not TENSORFLOW_AVAILABLE:
            return None
        
        model = keras.Sequential([
            keras.layers.Dense(128, activation='relu', input_shape=(input_dim,)),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(1, activation='linear')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def optimize_hyperparameters(self, X, y, model_type: str = 'random_forest'):
        """Optimiser les hyperparamètres avec GridSearch"""
        self.logger.info(f"Optimisation des hyperparamètres pour {model_type}...")
        
        if model_type == 'random_forest':
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 15, 20],
                'min_samples_split': [2, 5, 10]
            }
            model = RandomForestRegressor(random_state=42)
        
        elif model_type == 'xgboost' and XGBOOST_AVAILABLE:
            param_grid = {
                'n_estimators': [100, 200],
                'learning_rate': [0.05, 0.1, 0.2],
                'max_depth': [6, 8, 10]
            }
            model = xgb.XGBRegressor(random_state=42)
        
        else:
            self.logger.warning(f"Type de modèle non supporté: {model_type}")
            return None
        
        grid_search = GridSearchCV(
            model, param_grid, cv=5, 
            scoring='neg_mean_squared_error', 
            n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X, y)
        
        self.logger.info(f"Meilleurs paramètres: {grid_search.best_params_}")
        self.logger.info(f"Meilleur score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_estimator_
    
    def train_complete_system(self):
        """Entraîner le système complet"""
        self.logger.info("🧠 DÉBUT DE L'ENTRAÎNEMENT DU SYSTÈME IA COMPLET")
        print("=" * 60)
        
        # Créer le dossier models s'il n'existe pas
        import os
        os.makedirs('models', exist_ok=True)
        
        # 1. Générer ou charger les données
        if self.data_path and os.path.exists(self.data_path):
            data = pd.read_csv(self.data_path)
        else:
            data = self.generate_synthetic_data(10000)
        
        # 2. Préparer les features
        X, y_1h, y_4h, y_24h, feature_names = self.prepare_features(data)
        
        # 3. Entraîner les modèles pour chaque horizon
        horizons = {
            '1h': y_1h,
            '4h': y_4h,
            '24h': y_24h
        }
        
        results = {}
        
        for horizon, y in horizons.items():
            print(f"\n🎯 Entraînement pour horizon {horizon}")
            print("-" * 40)
            
            model_info = self.train_ensemble_models(X, y, horizon)
            results[horizon] = model_info
        
        # 4. Sauvegarder le résumé global
        summary = {
            'training_completed_at': datetime.now().isoformat(),
            'total_features': len(feature_names),
            'total_samples': len(X),
            'horizons_trained': list(horizons.keys()),
            'feature_names': feature_names,
            'models_performance': {
                horizon: info['performance'] 
                for horizon, info in results.items()
            }
        }
        
        with open('models/training_summary.json', 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print("\n" + "="*60)
        print("✅ ENTRAÎNEMENT TERMINÉ AVEC SUCCÈS !")
        print("="*60)
        
        # Afficher le résumé des performances
        for horizon, info in results.items():
            best_model = info['best_model']
            best_perf = info['performance'][best_model]
            print(f"🎯 {horizon}: {best_model} (R²: {best_perf['r2']:.4f}, MAE: {best_perf['mae']:.4f})")
        
        print(f"\n📁 Modèles sauvegardés dans: models/")
        print(f"📊 Résumé disponible: models/training_summary.json")
        
        return results
    
    def predict_with_ensemble(self, X, horizon: str = "1h"):
        """Prédiction avec l'ensemble de modèles"""
        try:
            model_info = joblib.load(f'models/ensemble_model_{horizon}.pkl')
            models = model_info['models']
            scaler = model_info['scaler']
            
            predictions = []
            
            for name, model in models.items():
                if name == 'neural_network':
                    X_scaled = scaler.transform(X)
                    pred = model.predict(X_scaled).flatten()
                else:
                    pred = model.predict(X)
                predictions.append(pred)
            
            # Moyenne pondérée des prédictions
            ensemble_pred = np.mean(predictions, axis=0)
            
            return ensemble_pred
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la prédiction: {e}")
            return None

def main():
    """Fonction principale pour l'entraînement"""
    trainer = UltraAdvancedModelTrainer()
    results = trainer.train_complete_system()
    return results

if __name__ == "__main__":
    main()
