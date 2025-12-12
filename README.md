# 🎬 Ethiens SME - API Cinéma

Une API RESTful construite avec **Flask** pour gérer la programmation de cinémas, les fiches de films, les acteurs et les séances. Ce projet inclut un système d'authentification par JWT (via Cookies) pour sécuriser les actions d'administration.

## 🚀 Fonctionnalités

* **Consultation (Accès Public)** :
    * 📜 Lister les films disponibles (liste simplifiée).
    * ℹ️ Consulter les détails complets d'un film (synopsis, réalisateur, casting, etc.).
    * 📍 Rechercher les séances programmées par ville.
* **Administration (Accès Sécurisé)** :
    * 🔐 Authentification (Login) avec gestion de Cookies HTTPOnly.
    * 🎬 Ajouter un nouveau film (avec gestion automatique "Get or Create" des acteurs).
    * 📅 Planifier une nouvelle séance (film, cinéma, salle, date).

## 🛠️ Prérequis

* **Langage** : Python 3.8+
* **Base de données** : MySQL Server

## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone [https://github.com/nayren23/Ehtiens-SME](https://github.com/nayren23/Ehtiens-SME)
cd ethiens-sme

```

### 2. Créer un environnement virtuel

# Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```
# Mac/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -e .
```

### 4. Configuration (.env)

Créez un fichier .env à la racine du projet avec vos informations :
```bash
# Front
FRONT_END_URL=http://localhost:4200

# Flask
FLASK_DEBUG=true
FLASK_HOST=127.0.0.1
FLASK_PORT=5050

# Base de données
DB_HOST=localhost
DB_NAME=nom_de_votre_bdd
DB_USER=root
DB_PWD=votre_mot_de_passe
DB_PORT=3306

# Sécurité JWT
JWT_SECRET_KEY=votre_super_cle_secrete_a_changer
```

Note importante : Dans le fichier ethiens_sme/config.py, assurez-vous que JWT_COOKIE_CSRF_PROTECT = False est défini pour faciliter les tests en développement.

## 🚀 Lancement
```bash
python .\rest_api.py
```

L'API sera accessible sur http://127.0.0.1:5050.

### 📡 Documentation des Endpoints
## 👤 Utilisateur (Auth)
| Méthode   | Endpoint    | Description  | Auth |
| ------ | ----- | ------- | ------- |
| POST | /user/auth | Authentification. Renvoie un Cookie HTTPOnly sécurisé | ❌ |



## 🎬 Films (Movies)
| Méthode   | Endpoint    | Description  | Auth |
| ------ | ----- | ------- | ------- |
| GET | /movie/list | Liste simplifiée (ID, Titre) triée alphabétiquement. | ❌ |
| GET | /movie/<id> | Fiche complète du film avec la liste des acteurs. | ❌ |
| POST | /movie/ | Créer un film et associer/créer les acteurs. | ✅ |
	        



## 🎟️ Séances (Seances)
| Méthode   | Endpoint    | Description  | Auth |
| ------ | ----- | ------- | ------- |
| GET | /seance/<ville> | Liste des séances disponibles pour une ville. | ❌ |
| POST | /seance/ | Ajouter une séance au planning d'un cinéma. | ✅ |
