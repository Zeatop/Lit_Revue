# LITRevu

LITRevu est une application web Django permettant aux utilisateurs de demander et publier des critiques de livres, ainsi que de suivre d'autres utilisateurs.

## Fonctionnalités

- Inscription et authentification des utilisateurs
- Création de tickets (demandes de critique)
- Publication de critiques de livres
- Système de suivi entre utilisateurs
- Flux d'activités personnalisé

## Prérequis

- Python 3.8+
- pip
- virtualenv (recommandé)

## Installation

1. Clonez le dépôt :
   ```
   git clone https://github.com/votre-nom/LITRevu.git
   cd LITRevu
   ```

2. Créez un environnement virtuel et activez-le :
   ```
   python -m venv venv
   source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
   ```

3. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

4. Effectuez les migrations :
   ```
   python manage.py migrate
   ```

5. Créez un superutilisateur :
   ```
   python manage.py createsuperuser
   ```

6. Lancez le serveur de développement :
   ```
   python manage.py runserver
   ```

L'application sera accessible à l'adresse `http://127.0.0.1:8000/`.

## Structure du projet

- `LITRevu/` : Configuration principale du projet Django
- `users/` : Application gérant l'authentification et les profils utilisateurs
- `website/` : Application principale pour les tickets, critiques et flux d'activités

## Utilisation

### Inscription et Connexion

- Accédez à la page d'accueil et utilisez les formulaires d'inscription ou de connexion.

### Création d'un Ticket

1. Connectez-vous à votre compte.
2. Naviguez vers "Créer un Ticket".
3. Remplissez le formulaire avec les détails du livre.

### Publication d'une Critique

1. Depuis la liste des tickets, choisissez un ticket à critiquer.
2. Cliquez sur "Créer une critique" et remplissez le formulaire.

### Suivi d'Utilisateurs

1. Accédez au profil d'un utilisateur.
2. Cliquez sur "Suivre" pour commencer à suivre ses activités.

## Personnalisation

### Modification des Modèles

Les modèles sont définis dans `website/models.py` et `users/models.py`. Pour ajouter ou modifier des champs :

1. Modifiez le fichier modèle approprié.
2. Créez et appliquez les migrations :
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

### Personnalisation des Vues

Les vues sont dans `website/views.py` et `users/views.py`. Pour modifier le comportement :

1. Localisez la vue concernée (par exemple, `ReviewCreateView`).
2. Modifiez la logique selon vos besoins.
3. Si nécessaire, mettez à jour le template correspondant dans le dossier `templates/`.

### Ajout de Nouvelles Fonctionnalités

1. Créez une nouvelle vue dans le fichier `views.py` approprié.
2. Ajoutez une nouvelle URL dans `urls.py` correspondant.
3. Créez un nouveau template dans le dossier `templates/` si nécessaire.
