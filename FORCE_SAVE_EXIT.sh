#!/bin/bash

echo "🔧 FORCE SAVE & EXIT - Résolution problème VS Code"
echo "=================================================="

# 1. Forcer l'état Git propre
cd /Users/johan/ia_env/bot-trading-
echo "✅ Navigation vers repository"

# 2. Ajouter tous les changements potentiels
git add -A
echo "✅ Ajout de tous les fichiers"

# 3. Créer un commit de sauvegarde si nécessaire
if ! git diff --cached --quiet; then
    git commit -m "Force save: Résolution problème fermeture VS Code"
    echo "✅ Commit de sauvegarde créé"
else
    echo "✅ Aucun changement à commiter"
fi

# 4. Push vers GitHub
git push origin main
echo "✅ Push vers GitHub"

# 5. Nettoyer les processus VS Code
echo "🧹 Nettoyage des processus..."
pkill -f "Visual Studio Code" 2>/dev/null || true
pkill -f "Code" 2>/dev/null || true

# 6. Nettoyer les fichiers temporaires
find . -name "*.swp" -delete 2>/dev/null || true
find . -name "*.tmp" -delete 2>/dev/null || true

echo "🎉 TERMINÉ - Tu peux maintenant fermer VS Code proprement"
echo "Si le problème persiste: Cmd+Q pour force quit VS Code"
