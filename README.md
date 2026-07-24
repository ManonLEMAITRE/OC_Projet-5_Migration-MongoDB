# Migration de données médicales vers MongoDB

## Contexte

Ce projet consiste en la la migration d'un dataset de patients (55 500 enregistrements) depuis un fichier CSV vers MongoDB. Les données sont préalablement nettoyées avant d'être insérées dans une base de données NoSQL (MongoDB)pour améliorer la scalabilité.

---

## Objectifs

- Nettoyer les données (suppression des doublons, normalisation, typage)
- Migrer les données vers MongoDB
- Mettre en place une structure de base de données flexible et performante
- Préparer la conteneurisation avec Docker et déploiement sur AWS

---

## Structure du Projet
Projet 5 - Migration MongoDB/
├── requirements.txt              # Dépendances Python
├── README.md                     # Documentation 
├── healthcare_dataset.csv        # Données brutes originales
├── healthcare_dataset_cleaned.csv # Données nettoyées
├── clean_data.py                 # Script de nettoyage des données
└── migration_mongodb.py         # Script de migration vers MongoDB

Non crées pour l'instant :
├── test_migration.py             # Script de validation post-migration
├── crud_operations.py            # Opérations CRUD sur MongoDB
└── create_indexes.py             # Création des index MongoDB


---

## Comment utiliser le projet ?

### 1. Installation des dépendances (macOS)
# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt


### 2. Lancer MongoDB
# Sur macOS avec Homebrew
brew services start mongodb-community

# Vérifier que MongoDB tourne
mongosh
# Puis taper : exit


### 3. Exécuter la migration complète
#### Étape 1 : Nettoyer les données
python clean_data.py

- Supprime 534 doublons
- Normalise la casse des noms
- Convertit les dates en format datetime
- Génère `healthcare_dataset_cleaned.csv`

#### Étape 3 : Migrer vers MongoDB
python migrate_to_mongodb.py
Insère 54 966 patients nettoyés dans MongoDB.
















#### Étape 4 : Valider la migration
python test_migration.py
Vérifie que toutes les données sont bien en base.

#### Étape 5 : Tester les opérations CRUD
python crud_operations.py
Démontre Create, Read, Update, Delete sur les patients.

#### Étape 6 : Créer les index
python create_indexes.py

Optimise les performances pour les requêtes fréquentes.

---

##  Processus de Nettoyage des Données

### Problèmes Identifiés

| Problème | Nombre | Solution |
|----------|--------|----------|
| Doublons exacts | 534 | Suppression (keep='first') |
| Casse incohérente (Name) | 55 500 | Normalisation en Title Case |
| Dates en texte | 2 colonnes | Conversion en datetime64 |
| Valeurs manquantes | 0 | Aucune action nécessaire |

### Résultat du Nettoyage
AVANT  : 55 500 lignes
APRÈS  : 54 966 lignes (-534 doublons)

---

##  Structure MongoDB

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
- **MongoDB 8.3.4** : Base de données NoSQL orientée documents
- **mongosh** : Shell interactif pour MongoDB

### Concepts Clés

#### NoSQL vs SQL
MongoDB offre une **flexibilité supérieure** à SQL :
-  Schéma adaptif (pas de migration nécessaire)
-  Champs avec espaces autorisés
-  Scalabilité horizontale (sharding)
-  Performance pour les lectures massives

#### PyMongo
Traducteur entre Python et MongoDB :
- Connexion à la base
- Opérations CRUD
- Gestion des erreurs
- Création d'index

---

##  Points de Vigilance

### Typage des Champs
-  Age, Room Number : entiers (int)
-  Billing Amount : décimaux (float)
-  Dates : datetime64 (pour les opérations temporelles)
-  Textes : chaînes de caractères (str)

### Index
Les index améliorent les performances des requêtes fréquentes :
- Index sur `Name` : recherches par nom patient
- Index sur `Date of Admission` : filtrage par date
- Index composé `Hospital + Medical Condition` : requêtes combinées

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

##  Prochaines Étapes

- **Phase 2** : Conteneurisation avec Docker
  - Dockerfile pour l'application Python
  - Dockerfile pour MongoDB
  - docker-compose.yml pour l'orchestration

- **Phase 3** : Déploiement sur AWS
  - Amazon DocumentDB (MongoDB compatible)
  - Amazon ECS (Elastic Container Service)
  - Amazon RDS (Relational Database Service)

---

##  Auteur

Manon Lemaitre - Data Engineer en formation

##  Date

Juillet 2026

