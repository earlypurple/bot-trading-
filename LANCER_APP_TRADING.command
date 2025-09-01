#!/bin/bash

# Script de lancement de l'application Trading Bot
# Créé le 24 août 2025

# Détection de l'environnement Python
PYTHON_PATH="/Users/johan/ia_env/bin/python"
if [ ! -f "$PYTHON_PATH" ]; then
    # Essayer de trouver Python automatiquement
    PYTHON_PATH=$(which python3)
    if [ -z "$PYTHON_PATH" ]; then
        osascript -e 'display dialog "Erreur: Python non trouvé. Veuillez installer Python 3." buttons {"OK"} default button "OK" with icon stop'
        exit 1
    fi
fi

# Vérifier les dépendances
$PYTHON_PATH -c "import tkinter" 2>/dev/null || {
    osascript -e 'display dialog "Tkinter manquant. Installation en cours..." buttons {"OK"} default button "OK" with icon note'
    # Sur macOS, tkinter est généralement déjà installé avec Python
}

# Chemin du projet
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Lancer l'application
cd "$DIR"
"$PYTHON_PATH" BOT_TRADING_APP.py
