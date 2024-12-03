# LITReview

LITRevu est une application Django permettant à une communauté d'utilisateurs de publier des critiques de livres ou d’articles et de consulter ou de solliciter une critique de livres à la demande.

## Fonctionnalités principales

- **Gestion des utilisateurs** : Inscription, connexion, déconnexion.
- **Billets (Tickets)** : Créez des demandes de critiques pour des livres ou des articles.
- **Critiques (Reviews)** :
  - Publiez une critique en réponse à un billet existant.
  - Créez une critique indépendante directement.
- **Suivi et relations utilisateurs** :
  - Suivez d'autres utilisateurs pour voir leurs critiques et billets.
  - Bloquez des utilisateurs pour ne plus voir leur contenu.
- **Flux personnalisé** : Affiche les billets et critiques des utilisateurs que vous suivez.
- **Système de permissions** : Modifiez ou supprimez uniquement vos propres critiques.

## Structure du programme
```
LITReview/
│
├── authentication/               # Gestion des utilisateurs (inscription, connexion)
    ├── static/                   # Fichier CSS et image (logo)
    ├── templates/authentication  # Templates HTML pour l'autentification
    ├── forms.py                  # Formulaires d'autentification
    ├── models.py                 # Modèle utilisateur
    ├── views.py 
├── blog/                         # Gestion des billets, critiques et relations utilisateurs
│   ├── templates/blog/           # Templates HTML pour le blog
│   └── forms.py                  # Formulaires des billets, critiques et relations entre utilisateurs
│   └── models.py                 # Modèles des billets, critiques et relations entre utilisateurs
│   └── views.py                  # Logique métier des billets et critiques
│
├── templates/                    # Templates partagés
│
├── .venv/                        # Environnement virtuel (non inclus dans le dépôt)
├── manage.py                     # Commandes de gestion Django
└── requirements.txt              # Dépendances Python
```
## Installation

### Prérequis

- Python 3.12+
- Django 5.1.3

### Étapes d'installation

1. **Cloner le dépôt** :

   ```sh
   git clone https://github.com/JCOzanne/LITReview
   cd LITReview
   
2. Créez et activez un environnement virtuel :
   ```bash
   python -m venv .venv
   source venv/bin/activate   # Sur Windows : venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Appliquez les migrations :
   ```bash
   python manage.py migrate
   ```

5. Lancez le serveur de développement :
   ```bash
   python manage.py runserver
   ```
   
6. Accédez à l'application :
   - Ouvrez [http://127.0.0.1:8000](http://127.0.0.1:8000) dans votre navigateur.

### Utilisation
Lorsque vous accédez à l'application, vous avez la possibilité de vous inscrire ou de vous identifier.

Une fois identifié, vous pouvez :
- Créer un billet avec son titre, sa description et une image en cliquant sur le lien 'demander une critique',
- Créer une critique à partir de zéro avec un billet associé en cliquant sur le lien 'créer une critique',
- Modifier ou supprimer son billet (ou sa critique) en cliquant sur le lien 'mes billets'(ou 'mes critiques'),
- Suivre/ne plus suivre ou bloquer/débloquer un utilisateur en cliquant sur le lien 'gérer mes abonnements',
- Voir votre flux avec vos billets, vos critiques et les demandes de critiques d'autres utilisateurs,
- Répondre à une demande de critique d'un utilisateur en cliquant sur le bouton 'Répondre' d'une demande de critique (si la demande à déjà fait l'objet d'une réponse, le bouton disparaît).

### Informations

La page d'administration est accessible à [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)  
Avec l'identifiant jco et le mot de passe charlotte

Les utilisateurs suivants ont été crées :

| Identifiant        | Username   |
|--------------------|------------|
| user1              | Username1! |
| user2              | Username2! |
| user3              | Username3! |

## Conformité PEP8
Rapport obtenu avec la commande :  
 ``` flake8 authentication blog webapp --format=html --htmldir=flake8-report  ```  
Conformément au fichier de configuration .flake8

![Rapport Flake8](https://github.com/JCOzanne/LITReview/blob/main/authentication/static/images/Rapport_Flake8.PNG?raw=True)
