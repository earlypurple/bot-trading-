#!/usr/bin/env python3
"""
TradingBot Pro 2025 - Script de démarrage et de session de trading
Ce script facilite le lancement, la configuration et l'exécution du bot de trading.
"""

import os
import sys
import argparse
import subprocess
import signal
import time
from pathlib import Path

# Import des modules de trading pour les sessions
try:
    from src.data.market_data import get_historical_data
    from src.models.momentum_model import MomentumModel
    from src.strategies.momentum_multi_asset import MomentumMultiAsset
except ImportError:
    print("⚠️  Modules de trading non disponibles, seuls les commandes de base sont disponibles")
    get_historical_data = None
    MomentumModel = None
    MomentumMultiAsset = None

def setup_environment():
    """Configure l'environnement Python et installe les dépendances"""
    print("🔧 Configuration de l'environnement...")
    
    # Vérifier si nous sommes dans un environnement virtuel
    if not hasattr(sys, 'base_prefix') or sys.base_prefix == sys.prefix:
        print("⚠️  Il est recommandé d'utiliser un environnement virtuel")
        response = input("Continuer quand même ? (y/N): ")
        if response.lower() != 'y':
            print("❌ Installation annulée")
            return False
    
    # Installer les dépendances
    try:
        print("📦 Installation des dépendances...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dépendances installées avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation des dépendances: {e}")
        return False

def create_env_file():
    """Crée le fichier .env à partir du template si nécessaire"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📋 Création du fichier de configuration...")
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Fichier .env créé à partir du template")
        print("⚠️  N'oubliez pas de configurer vos clés API dans le fichier .env")
        return True
    elif not env_file.exists():
        print("⚠️  Aucun fichier de configuration trouvé")
        return False
    
    return True

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    required_packages = [
        'flask', 'requests', 'pandas', 'numpy', 
        'scikit-learn', 'yfinance', 'python-dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Dépendances manquantes: {', '.join(missing)}")
        return False
    
    print("✅ Toutes les dépendances sont installées")
    return True

def run_tests():
    """Exécute les tests unitaires"""
    print("🧪 Exécution des tests...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Tous les tests sont passés")
            return True
        else:
            print("❌ Certains tests ont échoué")
            print(result.stdout)
            print(result.stderr)
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution des tests: {e}")
        return False

def start_bot(mode='development', port=5000, host='127.0.0.1'):
    """Démarre le bot de trading"""
    print(f"🚀 Démarrage du bot en mode {mode}...")
    
    # Configurer les variables d'environnement
    env = os.environ.copy()
    env['FLASK_ENV'] = mode
    env['FLASK_DEBUG'] = 'True' if mode == 'development' else 'False'
    
    try:
        if mode == 'production':
            # Utiliser Gunicorn en production
            cmd = [
                'gunicorn',
                '--bind', f'{host}:{port}',
                '--workers', '4',
                '--timeout', '120',
                '--access-logfile', '-',
                '--error-logfile', '-',
                'src.app:app'
            ]
        else:
            # Utiliser le serveur de développement Flask
            cmd = [sys.executable, 'src/app.py']
            env['FLASK_RUN_HOST'] = host
            env['FLASK_RUN_PORT'] = str(port)
        
        print(f"🌐 Bot disponible sur http://{host}:{port}")
        print(f"📊 Dashboard: http://{host}:{port}")
        print(f"📡 API: http://{host}:{port}/api")
        print("\n💡 Appuyez sur Ctrl+C pour arrêter le bot")
        
        # Démarrer le processus
        process = subprocess.Popen(cmd, env=env, cwd='.')
        
        # Gérer l'arrêt propre
        def signal_handler(sig, frame):
            print("\n🛑 Arrêt du bot...")
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                print("⚠️  Arrêt forcé du processus")
                process.kill()
            print("✅ Bot arrêté proprement")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Attendre la fin du processus
        process.wait()
        
    except FileNotFoundError as e:
        print(f"❌ Commande non trouvée: {e}")
        if 'gunicorn' in str(e) and mode == 'production':
            print("💡 Installez Gunicorn avec: pip install gunicorn")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")

def run_trading_session():
    """
    Orchestrates a full trading session:
    1. Trains the model if it doesn't exist.
    2. Runs a backtest on historical data.
    3. Simulates one live trade execution.
    """
    if not all([get_historical_data, MomentumModel, MomentumMultiAsset]):
        print("❌ Modules de trading non disponibles")
        return False
        
    ASSET_TICKER = 'BTC-USD'
    MODEL_PATH = 'btc_momentum_model.pkl'

    TRAIN_START_DATE = '2020-01-01'
    TRAIN_END_DATE = '2022-12-31'

    BACKTEST_START_DATE = '2023-01-01'
    BACKTEST_END_DATE = '2023-12-31'

    print("🤖 --- Démarrage de la session de trading ---")

    # 1. Train the model if it doesn't exist
    if not os.path.exists(MODEL_PATH):
        print(f"\n📊 Modèle non trouvé. Entraînement d'un nouveau modèle pour {ASSET_TICKER}...")
        training_data = get_historical_data(ASSET_TICKER, TRAIN_START_DATE, TRAIN_END_DATE)
        if training_data is not None:
            model = MomentumModel(model_path=MODEL_PATH)
            model.train(training_data)
        else:
            print("❌ Impossible de télécharger les données d'entraînement.")
            return False
    else:
        print(f"\n✅ Modèle existant trouvé: {MODEL_PATH}")

    # Initialize the strategy (which will load the model)
    strategy = MomentumMultiAsset(asset_ticker=ASSET_TICKER, model_path=MODEL_PATH)

    if not strategy.model:
        print("❌ Échec du chargement du modèle dans la stratégie.")
        return False

    # 2. Run Backtest
    print(f"\n📈 Exécution du backtest pour {ASSET_TICKER} de {BACKTEST_START_DATE} à {BACKTEST_END_DATE}...")
    backtest_data = get_historical_data(ASSET_TICKER, BACKTEST_START_DATE, BACKTEST_END_DATE)
    if backtest_data is not None:
        strategy.backtest(backtest_data)
    else:
        print("❌ Impossible de télécharger les données de backtest.")

    # 3. Simulate a single live execution
    print("\n🔄 --- Simulation d'un trade en temps réel ---")
    strategy.start()
    strategy.execute()
    strategy.stop()

    print("\n✅ --- Session de trading terminée ---")
    return True

def show_status():
    """Affiche le statut du système"""
    print("📊 Statut du système TradingBot Pro 2025")
    print("=" * 50)
    
    # Vérifier l'environnement
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 Répertoire: {os.getcwd()}")
    
    # Vérifier les fichiers de configuration
    if Path(".env").exists():
        print("✅ Fichier de configuration: Présent")
    else:
        print("❌ Fichier de configuration: Manquant")
    
    # Vérifier les dépendances
    if check_dependencies():
        print("✅ Dépendances: Installées")
    else:
        print("❌ Dépendances: Manquantes")
    
    # Vérifier la structure des répertoires
    required_dirs = ['src', 'tests', 'docs', 'frontend']
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✅ Répertoire {dir_name}: Présent")
        else:
            print(f"❌ Répertoire {dir_name}: Manquant")

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="TradingBot Pro 2025 - Script de démarrage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python run_trading_session.py setup          # Configure l'environnement
  python run_trading_session.py start          # Démarre en mode développement
  python run_trading_session.py start --prod   # Démarre en mode production
  python run_trading_session.py session        # Lance une session de trading
  python run_trading_session.py test           # Exécute les tests
  python run_trading_session.py status         # Affiche le statut du système
        """
    )
    
    parser.add_argument('command', choices=['setup', 'start', 'session', 'test', 'status'],
                       help='Commande à exécuter')
    parser.add_argument('--prod', action='store_true',
                       help='Démarrer en mode production')
    parser.add_argument('--port', type=int, default=5000,
                       help='Port d\'écoute (défaut: 5000)')
    parser.add_argument('--host', default='127.0.0.1',
                       help='Adresse d\'écoute (défaut: 127.0.0.1)')
    parser.add_argument('--skip-tests', action='store_true',
                       help='Ignorer les tests lors du setup')
    
    args = parser.parse_args()
    
    print("🤖 TradingBot Pro 2025")
    print("=" * 30)
    
    if args.command == 'setup':
        print("🔧 Configuration de l'environnement...")
        success = True
        
        # Créer le fichier .env
        if not create_env_file():
            success = False
        
        # Installer les dépendances
        if not setup_environment():
            success = False
        
        # Exécuter les tests (optionnel)
        if not args.skip_tests and success:
            if not run_tests():
                print("⚠️  Les tests ont échoué, mais l'installation continue")
        
        if success:
            print("\n✅ Configuration terminée avec succès!")
            print("💡 Vous pouvez maintenant démarrer le bot avec: python run_trading_session.py start")
        else:
            print("\n❌ Erreurs lors de la configuration")
            sys.exit(1)
    
    elif args.command == 'start':
        # Vérifications préalables
        if not Path(".env").exists():
            print("❌ Fichier .env manquant. Exécutez d'abord: python run_trading_session.py setup")
            sys.exit(1)
        
        if not check_dependencies():
            print("❌ Dépendances manquantes. Exécutez: python run_trading_session.py setup")
            sys.exit(1)
        
        mode = 'production' if args.prod else 'development'
        start_bot(mode, args.port, args.host)
    
    elif args.command == 'session':
        # Lancer une session de trading
        if not run_trading_session():
            sys.exit(1)
    
    elif args.command == 'test':
        if not run_tests():
            sys.exit(1)
    
    elif args.command == 'status':
        show_status()

if __name__ == '__main__':
    main()
