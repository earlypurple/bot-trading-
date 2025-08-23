# Multi-stage build pour optimiser la taille de l'image
FROM python:3.10-slim as builder

# Installation des outils de compilation
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt

# Image de production
FROM python:3.10-slim

# Création d'un utilisateur non-root pour la sécurité
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copie des dépendances installées
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

# Configuration du répertoire de travail
WORKDIR /app
CHOWN appuser:appuser /app

# Copie du code source
COPY --chown=appuser:appuser src ./src
COPY --chown=appuser:appuser frontend ./frontend

# Variables d'environnement
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False
ENV PYTHONPATH=/app/src

# Exposition du port
EXPOSE 5000

# Changement vers l'utilisateur non-root
USER appuser

# Vérification de santé
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/status || exit 1

# Commande de démarrage avec Gunicorn pour la production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "src.app:app"]
