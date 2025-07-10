# LitReview - Application de Critiques de Livres

## Description
Notre application permet de demander ou publier des critiques de livres ou d'articles. L'application présente trois cas d'utilisation principaux :

- La publication des critiques de livres ou d'articles
- La demande des critiques sur un livre ou sur un article particulier
- La recherche d'articles et de livres intéressants à lire, en se basant sur les critiques des autres

## Prérequis
- Python 3.10+ installé sur votre système
- Git installé
- pip (gestionnaire de paquets Python)

## Installation et Configuration

### 1. Cloner le projet
```bash
git clone https://github.com/Pumpkin-09/OCProjetP9.git
cd LITReview
```

### 2. Créer un environnement virtuel
```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows :
venv\Scripts\activate

# Sur macOS/Linux :
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer le serveur de développement
```bash
python manage.py runserver
```

Le serveur sera accessible à l'adresse : http://127.0.0.1:8000/

## Comptes de démonstration

### Superutilisateur (Admin)
Afin de gérer le serveur, un superutilisateur a déjà été créé :
- **URL admin** : http://127.0.0.1:8000/admin/
- **Username** : admin
- **Password** : Admin123!

### Utilisateurs de test
Afin de réaliser des tests, 4 utilisateurs sont déjà implémentés dans la base de données :

| Username | Password |
|----------|----------|
| utilisateur1 | Uti123! |
| utilisateur2 | Uti123! |
| utilisateur3 | Uti123! |
| utilisateur4 | Uti123! |

## Base de données
La base de données SQLite (`db.sqlite3`) contient des données de test incluant :
- Les comptes utilisateurs mentionnés ci-dessus
- Des exemples de critiques et de demandes de critiques
- Des données de test pour tester toutes les fonctionnalités de l'application

## Fonctionnalités principales
- Inscription et connexion des utilisateurs
- Publication de critiques de livres/articles
- Demande de critiques sur des ouvrages spécifiques
- Recherche d'utilisateurs et système de suivi (follow)
- Interface d'administration complète

## Notes importantes
- La base de données est déjà configurée et prête à l'emploi
- Aucune migration supplémentaire n'est nécessaire
- L'application utilise SQLite par défaut pour le développement
