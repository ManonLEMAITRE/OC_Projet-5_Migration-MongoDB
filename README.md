# Migration de données médicales vers MongoDB

## Contexte

Ce projet consiste en la migration d'un dataset de patients (55 500 enregistrements) depuis un fichier CSV vers MongoDB. Les données sont préalablement nettoyées avant d'être insérées dans une base de données NoSQL (MongoDB) pour améliorer la scalabilité.

---

## Objectifs

- Nettoyer les données (suppression des doublons, normalisation, typage)
- Migrer les données vers MongoDB
- Mettre en place une structure de base de données flexible et performante
- Conteneuriser l'application avec Docker
- Préparer le déploiement sur AWS

---

## Structure du Projet
```
Projet 5 - Migration MongoDB/
├── requirements.txt                      # Dépendances Python
├── README.md                             # Documentation
├── healthcare_dataset.csv                # Données brutes originales
├── healthcare_dataset_cleaned.csv        # Données nettoyées
├── Dockerfile                            # Image Docker de l'application Python
├── docker-compose.yml                    # Orchestration des services (app + MongoDB)
├── .dockerignore                         # Fichiers exclus du build Docker
├── orchestration_migration_complete.py   # Orchestrateur du pipeline complet
├── 1.clean_data.py                       # Nettoyage des données
├── 2.migration_mongodb.py                # Migration vers MongoDB
├── 3.test_migration.py                   # Validation post-migration
├── 4.test_crud.py                        # Opérations CRUD
└── 5.generer_index.py                    # Création des index MongoDB
```

---

## 🐳 Exécution via Docker (méthode recommandée)

### Prérequis
- Docker Desktop installé et lancé

### Lancer le projet complet
```bash
docker-compose up
```

Cette commande :
- Construit l'image Python (si nécessaire) et démarre MongoDB
- Exécute automatiquement les 5 étapes du pipeline dans l'ordre :
  nettoyage → migration → tests → CRUD → création des index
- Chaque étape affiche ✅ (succès) ou ❌ (erreur), avec arrêt immédiat en cas d'échec

### Vérifier le résultat
```bash
docker exec -it mongodb mongosh
```
Puis dans le shell Mongo :
```javascript
use healthcare_db
db.patients.countDocuments()   // doit retourner 54966
```

### Architecture Docker
- **Service `mongodb`** : image officielle `mongo:8.3.7`, données persistées dans le volume `mongo_data`
- **Service `app`** : construit depuis le `Dockerfile` local (Python 3.12-slim), exécute `orchestration_migration_complete.py`
- **Réseau nommé** : `healthcare_network`, permet aux deux services de communiquer via leur nom de service (`mongodb://mongodb:27017/`)
- **Volumes** :
  - `mongo_data` (volume Docker géré) : persistance des données MongoDB entre les redémarrages
  - Bind mount du CSV : `./healthcare_dataset.csv:/app/healthcare_dataset.csv`

Le pipeline est **idempotent** : chaque script de migration vide la collection (`delete_many({})`) avant réinsertion, donc relancer `docker-compose up` autant de fois que voulu ne crée jamais de doublons.

### Arrêter et nettoyer
```bash
docker-compose down
```

---

## Exécution manuelle (alternative, sans Docker)

### 1. Installation des dépendances (macOS)
```bash
# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Lancer MongoDB
```bash
# Sur macOS avec Homebrew
brew services start mongodb-community

# Vérifier que MongoDB tourne
mongosh
# Puis taper : exit
```

### 3. Exécuter la migration complète, étape par étape

#### Étape 1 : Nettoyer les données
```bash
python 1.clean_data.py
```
- Supprime 534 doublons
- Normalise la casse des noms
- Convertit les dates en format datetime
- Génère `healthcare_dataset_cleaned.csv`

#### Étape 2 : Migrer vers MongoDB
```bash
python 2.migration_mongodb.py
```
Insère 54 966 patients nettoyés dans MongoDB.

#### Étape 3 : Valider la migration
```bash
python 3.test_migration.py
```
Vérifie que toutes les données sont bien en base.

#### Étape 4 : Tester les opérations CRUD
```bash
python 4.test_crud.py
```
Démontre Create, Read, Update, Delete sur les patients.

#### Étape 5 : Créer les index
```bash
python 5.generer_index.py
```
Optimise les performances pour les requêtes fréquentes.

---

## Processus de Nettoyage des Données

### Problèmes Identifiés

| Problème | Nombre | Solution |
|----------|--------|----------|
| Doublons exacts | 534 | Suppression (keep='first') |
| Casse incohérente (Name) | 55 500 | Normalisation en Title Case |
| Dates en texte | 2 colonnes | Conversion en datetime64 |
| Valeurs manquantes | 0 | Aucune action nécessaire |

### Résultat du Nettoyage
```
AVANT  : 55 500 lignes
APRÈS  : 54 966 lignes (-534 doublons)
```

---

## Structure MongoDB

### Base de Données
- **Nom** : `healthcare_db`
- **Type** : Base de données NoSQL flexible

### Collection
- **Nom** : `patients`
- **Type** : Collection de documents JSON-like
- **Nombre de documents** : 54 966

### Document Exemple
```json
{
  "_id": ObjectId("..."),
  "Name": "Bobby Jackson",
  "Age": 30,
  "Gender": "Male",
  "Blood Type": "B-",
  "Medical Condition": "Cancer",
  "Date of Admission": "2024-01-31",
  "Doctor": "Matthew Smith",
  "Hospital": "Sons and Miller",
  "Insurance Provider": "Blue Cross",
  "Billing Amount": 18856.28,
  "Room Number": 328,
  "Admission Type": "Urgent",
  "Discharge Date": "2024-02-02",
  "Medication": "Paracetamol",
  "Test Results": "Normal"
}
```

---

## 🛠️ Outils et Technologies Utilisés

### Python
- **Pandas** : Manipulation et nettoyage des données CSV
- **PyMongo** : Librairie Driver MongoDB pour Python
- **Python-dotenv** : Gestion des variables d'environnement

### Base de Données
- **MongoDB** : Base de données NoSQL orientée documents
  - Version locale : 8.3.4
  - Version conteneurisée (Docker) : 8.3.7 (même branche mineure)
- **mongosh** : Shell interactif pour MongoDB

### Conteneurisation
- **Docker** : conteneurisation de l'application Python (image `python:3.12-slim`)
- **Docker Compose** : orchestration des services `app` + `mongodb`, volumes, réseau

### Concepts Clés

#### NoSQL vs SQL
MongoDB offre une **flexibilité supérieure** à SQL :
- Schéma adaptif (pas de migration nécessaire)
- Champs avec espaces autorisés
- Scalabilité horizontale (sharding)
- Performance pour les lectures massives

#### PyMongo
Traducteur entre Python et MongoDB :
- Connexion à la base
- Opérations CRUD
- Gestion des erreurs
- Création d'index

---

## Points de Vigilance

### Typage des Champs
- Age, Room Number : entiers (int)
- Billing Amount : décimaux (float)
- Dates : datetime64 (pour les opérations temporelles)
- Textes : chaînes de caractères (str)

### Index
Les index améliorent les performances des requêtes fréquentes :
- Index sur `Name` : recherches par nom patient
- Index sur `Date of Admission` : filtrage par date
- Index composé `Hospital + Medical Condition` : requêtes combinées

### Idempotence de la migration
Le script `2.migration_mongodb.py` vide systématiquement la collection (`delete_many({})`) avant réinsertion, afin d'éviter la création de doublons en cas de ré-exécution (manuelle ou via `docker-compose up`).

### Ressources
- Fermeture correcte des connexions MongoDB
- Gestion des erreurs (DuplicateKeyError, etc.)
- Libération de la mémoire après chaque opération

---

## Sécurité et Authentification

**À noter** : MongoDB fonctionne actuellement **sans authentification** (mode développement).

Pour la production, il faudrait :
- Créer des utilisateurs avec rôles
- Activer l'authentification
- Configurer les permissions par rôle

---

## Prochaines Étapes

- **Phase 3** : Déploiement sur AWS
  - Amazon DocumentDB (MongoDB compatible)
  - Amazon ECS (Elastic Container Service)
  - Amazon RDS (Relational Database Service)

---

## Auteur

Manon Lemaitre - Data Engineer en formation