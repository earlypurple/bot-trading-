#!/bin/bash

# Script d'activation du trading réel avec Coinbase
echo "🚀 Activation du trading RÉEL avec Coinbase..."

# Chemin absolu du répertoire du projet
PROJET_DIR="/Users/johan/ia_env/bot-trading-/TradingBot_Pro_2025"
ENV_PATH="/Users/johan/ia_env/bin/activate"
CREDENTIALS_FILE="$PROJET_DIR/coinbase_credentials.env"

# Vérifier que les credentials existent
if [ ! -f "$CREDENTIALS_FILE" ]; then
    echo "❌ ERREUR: Fichier de credentials Coinbase introuvable!"
    exit 1
fi

# Activer l'environnement virtuel
source "$ENV_PATH"

echo "🔒 Configuration des identifiants Coinbase pour le trading réel..."

# Extraire les informations des credentials
API_KEY=$(grep COINBASE_API_KEY "$CREDENTIALS_FILE" | cut -d= -f2)
PRIVATE_KEY_START=$(grep -n "COINBASE_PRIVATE_KEY=" "$CREDENTIALS_FILE" | cut -d: -f1)
PRIVATE_KEY=$(tail -n +$PRIVATE_KEY_START "$CREDENTIALS_FILE" | head -n 6 | awk 'NR>1')

if [ -z "$API_KEY" ] || [ -z "$PRIVATE_KEY" ]; then
    echo "❌ ERREUR: Identifiants Coinbase incomplets dans le fichier credentials!"
    exit 1
fi

# Créer un fichier temporaire pour le patch
TMP_PATCH=$(mktemp)

cat > "$TMP_PATCH" << EOL
--- dashboard_trading_pro.py.orig
+++ dashboard_trading_pro.py
@@ -10,6 +10,7 @@
 import traceback
 import sqlite3
 import numpy as np
+import os
 import pandas as pd
 import ta
 from datetime import datetime, timedelta
@@ -30,6 +31,17 @@
 except ImportError as e:
     print(f"⚠️ Modules IA avancés non disponibles: {e}")
     AI_MODULES_AVAILABLE = False
+
+# Charger les variables d'environnement depuis le fichier coinbase_credentials.env
+def load_env_file(env_file):
+    if os.path.exists(env_file):
+        with open(env_file, 'r') as f:
+            for line in f:
+                line = line.strip()
+                if line and not line.startswith('#'):
+                    key, value = line.split('=', 1)
+                    os.environ[key] = value
+load_env_file(os.path.join(os.path.dirname(__file__), 'coinbase_credentials.env'))
 
 # Configuration Flask
 app = Flask(__name__)
@@ -133,16 +145,26 @@
     def setup_exchange(self):
         """Configuration de l'exchange Coinbase"""
         try:
-            private_key = """-----BEGIN EC PRIVATE KEY-----
-MHcCAQEEIDdqwLclidk5lL0hF0rev6nDBBZFQYBjbs4r+ZdqqdZPoAoGCCqGSM49
-AwEHoUQDQgAEFpDQesMVJlwz1CA5dgfDDfvigRXUimALaJE7bn6Hn8WNDMkGasds
-Wqk/bwMFJGkLuyeXWMIUyMZFbuwVpptwNg==
------END EC PRIVATE KEY-----"""
+            # Récupérer les clés API depuis les variables d'environnement
+            api_key = os.environ.get('COINBASE_API_KEY', '')
+            
+            # La clé privée est généralement stockée en plusieurs lignes
+            # On va la récupérer directement du fichier pour être sûr
+            private_key_path = os.path.join(os.path.dirname(__file__), 'coinbase_credentials.env')
+            private_key = ""
+            capture = False
+            
+            with open(private_key_path, 'r') as f:
+                for line in f:
+                    if "-----BEGIN EC PRIVATE KEY-----" in line:
+                        capture = True
+                        private_key = "-----BEGIN EC PRIVATE KEY-----\\n"
+                    elif "-----END EC PRIVATE KEY-----" in line:
+                        private_key += "-----END EC PRIVATE KEY-----"
+                        capture = False
+                    elif capture:
+                        private_key += line.strip() + "\\n"
             
-            exchange_config = {
-                'apiKey': '08d4759c-8572-4224-a3c8-6a63cf877fd6',
-                'secret': private_key,
-                'sandbox': False,
-                'enableRateLimit': True,
-            }
+            print(f"🔑 Utilisation de l'API Key Coinbase: {api_key[:5]}...{api_key[-5:]}")
+            print("🔐 Clé privée EC chargée pour l'authentification")
+            
+            # Configuration du mode trading
+            trading_mode = os.environ.get('TRADING_MODE', 'LIVE').upper()
+            sandbox_mode = trading_mode != 'LIVE'
+            
+            if sandbox_mode:
+                print("⚠️ MODE SANDBOX ACTIVÉ - Pas de vrais trades")
+            else:
+                print("🔴 MODE LIVE ACTIVÉ - TRADES RÉELS EN COURS")
+            
+            # Configuration exchange
+            exchange_config = {
+                'apiKey': api_key,
+                'secret': private_key,
+                'sandbox': sandbox_mode,
+                'enableRateLimit': True,
+            }
             
             self.exchange = ccxt.coinbaseadvanced(exchange_config)
-            print("✅ TradingBot Pro connecté à Coinbase!")
+            self.exchange.load_markets()  # Forcer le chargement des marchés
+            
+            print(f"✅ TradingBot Pro connecté à Coinbase! ({trading_mode})")
+            
+            # Configurer les limites de risque
+            risk_level = os.environ.get('RISK_LEVEL', 'MEDIUM').upper()
+            max_trade_amount = float(os.environ.get('MAX_TRADE_AMOUNT', '100'))
+            
+            self.config.max_total_investment = max_trade_amount
+            
+            if risk_level == 'LOW':
+                self.config.max_portfolio_risk = 0.01  # 1%
+                self.config.stop_loss_percent = 0.03   # 3%
+                self.config.take_profit_percent = 0.05 # 5%
+            elif risk_level == 'HIGH':
+                self.config.max_portfolio_risk = 0.05  # 5%
+                self.config.stop_loss_percent = 0.10   # 10%
+                self.config.take_profit_percent = 0.15 # 15%
+            else:  # MEDIUM (par défaut)
+                self.config.max_portfolio_risk = 0.03  # 3%
+                self.config.stop_loss_percent = 0.05   # 5%
+                self.config.take_profit_percent = 0.10 # 10%
+            
+            print(f"⚙️ Niveau de risque configuré: {risk_level}")
+            print(f"💰 Montant max par trade: ${max_trade_amount}")
+            
             return True
             
         except Exception as e:
             print(f"❌ Erreur connexion bot: {e}")
+            traceback.print_exc()
             return False
     
     def get_portfolio(self):
EOL

# Appliquer le patch au dashboard_trading_pro.py
cd "$PROJET_DIR" && patch -p0 < "$TMP_PATCH"

# Vérifier si le patch a réussi
if [ $? -eq 0 ]; then
    echo "✅ Configuration du trading LIVE réussie!"
else
    echo "❌ ERREUR lors de l'application du patch. Impossible d'activer le trading réel."
    exit 1
fi

# Améliorer le script de lancement pour passer en mode trading réel
cd .. && cat > lancer_dashboard_trading_reel.sh << EOL
#!/bin/bash

# Script de lancement du dashboard trading RÉEL
echo "🚀 Lancement du dashboard trading RÉEL avec Coinbase..."

# Chemin absolu du répertoire du projet
PROJET_DIR="/Users/johan/ia_env/bot-trading-/TradingBot_Pro_2025"

# Activation de l'environnement virtuel
source /Users/johan/ia_env/bin/activate

# Aller dans le bon répertoire
cd "\$PROJET_DIR"
echo "📂 Répertoire actuel: \$(pwd)"

# Vérification des ports
echo "🔍 Vérification des ports..."
if lsof -ti:8088 > /dev/null; then
  echo "⚠️  Le port 8088 est déjà utilisé, nettoyage..."
  lsof -ti:8088 | xargs kill -9
fi
if lsof -ti:8081 > /dev/null; then
  echo "⚠️  Le port 8081 est déjà utilisé, nettoyage..."
  lsof -ti:8081 | xargs kill -9
fi

echo "✨ Lancement du dashboard TRADING RÉEL..."
echo "📊 URL du dashboard: http://localhost:8088"
echo "🔴 MODE LIVE - TRADES RÉELS ACTIVÉS"
echo ""

# Lancement du script Python avec mode trading réel
python "\$PROJET_DIR/dashboard_trading_pro.py" --live-trading
EOL

# Rendre le script exécutable
chmod +x lancer_dashboard_trading_reel.sh

echo ""
echo "🔴 ATTENTION: Le trading RÉEL avec votre vrai portfolio Coinbase est maintenant configuré!"
echo "💰 Pour lancer le bot et commencer le trading, exécutez:"
echo ""
echo "    ./lancer_dashboard_trading_reel.sh"
echo ""
echo "⚠️  ATTENTION: Le bot va effectuer des trades RÉELS avec VOTRE ARGENT!"
echo "💸 Montant maximum par trade configuré: $(grep MAX_TRADE_AMOUNT $CREDENTIALS_FILE | cut -d= -f2)$"
echo "🔒 Niveau de risque configuré: $(grep RISK_LEVEL $CREDENTIALS_FILE | cut -d= -f2)"
