#!/bin/bash

# Script pour configurer l'accès distant au bot trading depuis iPhone
# Créé le 24 août 2025

# Configuration
PORT_PUBLIC=8088
PORT_LOCAL=8088
PROJET_DIR="/Users/johan/ia_env/bot-trading-"
NGROK_CONFIG="$PROJET_DIR/ngrok_config.yml"

# Vérifier si ngrok est installé
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok n'est pas installé. Installation en cours..."
    brew install ngrok/ngrok/ngrok || {
        echo "❌ Erreur lors de l'installation de ngrok."
        echo "📱 Pour installer manuellement ngrok:"
        echo "   1. Téléchargez-le depuis https://ngrok.com/download"
        echo "   2. Décompressez et copiez dans /usr/local/bin"
        exit 1
    }
    echo "✅ ngrok installé avec succès."
fi

# Vérifier si ngrok est configuré
if ! ngrok config check &> /dev/null; then
    echo "⚙️ Configuration de ngrok..."
    echo "📱 Vous devez créer un compte sur https://ngrok.com et obtenir un token d'authentification."
    echo "📝 Entrez votre token d'authentification ngrok:"
    read -r NGROK_TOKEN
    
    # Configurer ngrok avec le token
    ngrok config add-authtoken "$NGROK_TOKEN" || {
        echo "❌ Erreur lors de la configuration de ngrok."
        exit 1
    }
    echo "✅ ngrok configuré avec succès."
fi

# Créer le fichier de configuration ngrok
cat > "$NGROK_CONFIG" << EOL
version: 2
authtoken: $(ngrok config get-value authtoken)
tunnels:
  tradingbot:
    proto: http
    addr: $PORT_LOCAL
    oauth:
      provider: google
EOL

echo "📱 Configuration de l'accès iPhone..."

# Arrêter les instances ngrok existantes
pkill -f ngrok || true
sleep 2

# Démarrer ngrok en arrière-plan
nohup ngrok start --config="$NGROK_CONFIG" tradingbot > "$PROJET_DIR/ngrok.log" 2>&1 &

# Attendre que ngrok démarre
echo "⏳ Démarrage du tunnel sécurisé..."
sleep 5

# Récupérer l'URL publique
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*' | grep -o 'http[^"]*')

if [ -z "$NGROK_URL" ]; then
    echo "❌ Erreur: Impossible de récupérer l'URL ngrok."
    echo "📊 Consultez les logs: $PROJET_DIR/ngrok.log"
    exit 1
fi

# Générer un QR code pour l'accès facile depuis l'iPhone
echo "📱 Voici l'URL pour accéder à votre bot depuis votre iPhone:"
echo "🔗 $NGROK_URL"

# Créer un QR code à scanner avec l'iPhone
cat > "$PROJET_DIR/iphone_access.html" << EOL
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Accès Bot Trading iPhone</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            text-align: center;
            margin: 0;
            padding: 20px;
            background: #f0f2f5;
            color: #333;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2a5298;
        }
        .qr-code {
            margin: 20px auto;
            width: 250px;
            height: 250px;
        }
        .url {
            word-break: break-all;
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            margin-top: 20px;
        }
        .note {
            margin-top: 20px;
            font-size: 0.9em;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📱 Accès Bot Trading depuis iPhone</h1>
        <p>Scannez ce code QR avec votre iPhone pour accéder au dashboard de trading:</p>
        
        <div class="qr-code">
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=$NGROK_URL" alt="QR Code">
        </div>
        
        <p>Ou utilisez cette URL:</p>
        <div class="url">$NGROK_URL</div>
        
        <div class="note">
            <p>⚠️ Note importante: Cette URL est valide tant que votre Mac est allumé et connecté à Internet.</p>
            <p>⏱️ Date de génération: $(date)</p>
        </div>
    </div>
</body>
</html>
EOL

# Ouvrir le QR code dans le navigateur
open "$PROJET_DIR/iphone_access.html"

# Créer un script pratique pour l'iPhone
cat > "$PROJET_DIR/ACCEDER_DEPUIS_IPHONE.command" << EOL
#!/bin/bash
cd "\$(dirname "\$0")"
open "iphone_access.html"
EOL

chmod +x "$PROJET_DIR/ACCEDER_DEPUIS_IPHONE.command"

echo ""
echo "✅ Configuration terminée!"
echo "📱 Vous pouvez maintenant accéder à votre bot de trading depuis votre iPhone"
echo "🔒 L'accès est sécurisé avec authentification Google"
echo ""
echo "💡 Pour partager à nouveau l'accès, double-cliquez sur:"
echo "   ACCEDER_DEPUIS_IPHONE.command"
echo ""
