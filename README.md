# Migration de données médicales vers MongoDB

## Contexte

Dans le cadre de ce projet de migartion de DataSoluTech, on m'a confié un dataset de patients (55 500 lignes) en CSV à migrer vers MongoDB. 
L'objectif principal : nettoyer les données, les migrer, conteneuriser le tout avec Docker, et préparer un futur déploiement sur AWS.
L'objectif secondaire : mettre en place une structure de base flexible et scalable horizontalement. 

---

## Objectifs

- Nettoyer les données (doublons, casse, typage des dates)
- Migrer vers MongoDB
- Mettre en place une structure de base flexible et des index pertinents
- Conteneuriser l'application avec Docker
- Documenter la démarche

---

## Structure du projet
Projet 5 - Migration MongoDB/  
├── requirements.txt # Dépendances Python  
├── README.md  
├── healthcare_dataset.csv # Données brutes  
├── healthcare_dataset_cleaned.csv # Données nettoyées  
├── Dockerfile  
├── docker-compose.yml  
├── .dockerignore  
├── orchestration_migration_complete.py # Enchaîne les 6 scripts via subprocess  
├── db_utils.py # Connexion MongoDB centralisée (client + collection)  
├── 0.creation_utilisateurs.py # Création automatique de medecin_user et secretariat_user  
├── 1.clean_data.py # Nettoyage des données  
├── 2.migration_mongodb.py # Migration vers MongoDB  
├── 3.test_migration.py # Validation post-migration  
├── 4.test_crud.py # Démonstration CRUD  
└── 5.generer_index.py # Création des index  

Tous les scripts sont découpés en fonctions (chargement, nettoyage, insertion, tests unitaires, etc.), avec un point d'entrée `if __name__ == "__main__":` à la fin de chaque fichier. La connexion à MongoDB (client + accès à la collection `patients`) est centralisée dans `db_utils.py` et importée partout où elle est nécessaire, plutôt que dupliquée dans chaque script.

---

## Configuration requise avant de lancer le projet

**Étape indispensable, à faire avant `docker-compose up`.** 
Le projet utilise l'authentification MongoDB (voir section "Sécurité et authentification"), ce qui nécessite un fichier `.env` à la racine du projet, non fourni dans le dépôt Git (sécurité).

Créer un fichier `.env` à la racine du projet avec le contenu suivant :

```
MONGO_ROOT_USER=
MONGO_ROOT_PASSWORD=
```

- `MONGO_ROOT_USER` / `MONGO_ROOT_PASSWORD` : identifiants du compte `admin_si`, créé **automatiquement** par l'image officielle MongoDB au premier démarrage (mécanisme natif `MONGO_INITDB_ROOT_USERNAME`/`MONGO_INITDB_ROOT_PASSWORD`, alimenté par ces deux variables dans `docker-compose.yml`). 
Ce compte est ensuite utilisé par le pipeline pour la migration, les tests, la gestion des index, et la création des deux autres utilisateurs. Voir la section "Sécurité et authentification" pour le détail des rôles.

Sans ce fichier, `docker-compose up` échouera au démarrage du service `mongodb` (variables d'environnement manquantes) ou l'authentification échouera lors de la connexion du service `app`.

 Ce fichier `.env` n'a d'effet que si le volume `mongo_data` est **vide** (premier démarrage). Si vous relancez le projet après un `docker-compose down` (sans `-v`), les identifiants existants dans le volume restent ceux d'origine, peu importe ce qui est dans `.env`.

---

## Exécution via Docker (recommandé)

### Prérequis
- Docker Desktop installé et lancé
- Fichier `.env` créé (voir section précédente)

### Lancer le projet
```bash
docker-compose up
```
Ça construit l'image Python, démarre MongoDB, et exécute les 5 scripts dans l'ordre (nettoyage → migration → tests → CRUD → index). Si une étape échoue, le pipeline s'arrête.

### Vérifier le résultat
```bash
docker exec -it mongodb mongosh
```
```
use healthcare_db
db.patients.countDocuments()   // 54966 attendu
```

### Architecture
- **Service `mongodb`** : image officielle `mongo:8.3.7`, données dans le volume `mongo_data`
- **Service `app`** : construit depuis le `Dockerfile` (Python 3.12-slim), lance `orchestration_migration_complete.py`
- **Réseau** : `healthcare_network`, les deux services communiquent via `mongodb://mongodb:27017/`
- **Volumes** : `mongo_data` pour la persistance MongoDB, bind mount pour le CSV

Le pipeline est idempotent : la collection est vidée avant réinsertion (`delete_many({})`), et les index sont supprimés puis recréés à chaque exécution (`drop_indexes()`). On peut relancer `docker-compose up` autant de fois que voulu, le résultat final est toujours le même.

### Arrêter
```bash
docker-compose down
```

---

## Exécution manuelle (sans Docker)

### Installation (macOS)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Lancer MongoDB
```bash
brew services start mongodb-community
```

### Étapes, dans l'ordre

```bash
python 0.creation_utilisateurs.py # crée medecin_user et secretariat_user
python 1.clean_data.py       # nettoie et sauvegarde healthcare_dataset_cleaned.csv
python 2.migration_mongodb.py  # migre les 54 966 patients vers MongoDB
python 3.test_migration.py     # 8 tests de validation post-migration
python 4.test_crud.py          # démo Create/Read/Update/Delete
python 5.generer_index.py      # supprime les anciens index puis recrée les 5 actuels
```

Ou tout d'un coup avec l'orchestrateur :
```bash
python orchestration_migration_complete.py
```

---

## Nettoyage des données

| Problème | Nombre | Solution |
|----------|--------|----------|
| Doublons exacts | 534 | `drop_duplicates(keep='first')` |
| Casse incohérente (Name) | 55 500 | `.str.title()` |
| Dates stockées en texte | 2 colonnes | `pd.to_datetime()` |
| Valeurs manquantes | 0 | aucune action |

AVANT : 55 500 lignes
APRÈS : 54 966 lignes (-534 doublons)

Point d'attention : la conversion des dates avec `pd.to_datetime()` doit être refaite dans `2.migration_mongodb.py` juste avant l'insertion, même si elle a déjà été faite dans `1.clean_data.py`, en effet, le passage par le CSV intermédiaire (`to_csv` puis `read_csv`) fait perdre le typage `datetime` et repasse tout en texte. Sans ça, `Date of Admission` et `Discharge Date` se retrouvent en `string` dans MongoDB au lieu de `Date`.

---

## Structure MongoDB

- **Base** : `healthcare_db`
- **Collection** : `patients` (54 966 documents)

Chaque patient est stocké dans un document unique (pas de collections séparées) :

```json
{
  "_id": ObjectId("..."),
  "Name": "Bobby Jackson",
  "Age": 30,
  "Gender": "Male",
  "Blood Type": "B-",
  "Medical Condition": "Cancer",
  "Date of Admission": ISODate("2024-01-31"),
  "Doctor": "Matthew Smith",
  "Hospital": "Sons and Miller",
  "Insurance Provider": "Blue Cross",
  "Billing Amount": 18856.28,
  "Room Number": 328,
  "Admission Type": "Urgent",
  "Discharge Date": ISODate("2024-02-02"),
  "Medication": "Paracetamol",
  "Test Results": "Normal"
}
```

Un schéma détaillé (types de champs, index) est disponible dans le dossier du projet.

---

## Index

5 index actuellement, choisis en fonction des recherches probables dans un contexte hospitalier (recherche par pathologie, par médecin, par hôpital, par date d'admission), aucune spécification précise dans les consignes sur ce point, donc c'est une hypothèse, pas une donnée figée :

- `Name` : recherche par nom de patient
- `Medical Condition` + `Medication` (composé) : recherche par pathologie, éventuellement combinée au médicament
- `Date of Admission` : filtrage par date
- `Hospital` : recherche par hôpital
- `Doctor` : recherche par médecin

Pour l'index composé, l'ordre des champs compte : `Medical Condition` en premier permet d'optimiser aussi bien les requêtes sur la pathologie seule que sur pathologie + médicament ensemble.

`5.generer_index.py` supprime systématiquement tous les index existants (sauf `_id_`) avant d'en recréer 5, pour que le script reste idempotent et qu'on ne se retrouve pas avec des index résiduels d'anciennes versions.

---

## Outils et versions

- **Python** : 3.14.2 (local) / 3.12-slim (Docker)
- **Pandas** : 2.2.0
- **PyMongo** : 4.6.3
- **python-dotenv** : 1.2.2
- **MongoDB** : 8.3.4 (local) / 8.3.7 (Docker)

Les versions de PyMongo et python-dotenv ont été mises à jour suite à deux alertes de sécurité Dependabot.

---

## Typage des champs

- `Age`, `Room Number` : int
- `Billing Amount` : double
- `Date of Admission`, `Discharge Date` : Date (vérifié avec `typeof` en mongosh)
- Le reste : string

---

## Sécurité et authentification

### Utilisateurs et rôles

3 utilisateurs sont utilisés, avec des rôles différenciés selon les profils techniques supposés dans le projet :

| Utilisateur | Rôle | Justification | Création |
|---|---|---|---|
| `admin_si` | root (accès complet au serveur) | Compte technique d'administration, utilisé par le pipeline pour migrer les données et gérer les index | Automatique, par l'image Docker officielle de MongoDB (`MONGO_INITDB_ROOT_USERNAME`/`MONGO_INITDB_ROOT_PASSWORD`) |
| `pipeline_user` | `readWrite` sur `healthcare_db` | Les utilisateurs du pipeline consultent les informations et les modifient | Automatique, via `0.creation_utilisateurs.py` |
| `analyste_user` | `read` sur `healthcare_db` | L'analyste consulte les données pour générer des rapports | Automatique, via `0.creation_utilisateurs.py` |

**Note** : pour simplifier le projet, `admin_si` est ici un compte root global (créé nativement par Docker), plutôt qu'un rôle scopé uniquement sur `healthcare_db`. Dans un contexte réel, ce rôle serait restreint plus finement (`userAdmin` + `dbAdmin` + `readWrite` sur `healthcare_db` uniquement).

### Activation de l'authentification

L'authentification est activée sur le conteneur MongoDB via l'option `--auth` (dans `docker-compose.yml`, sur le service `mongodb`). Le compte `admin_si` est créé automatiquement par l'image officielle de MongoDB au tout premier démarrage (volume vide), à partir des variables `MONGO_ROOT_USER`/`MONGO_ROOT_PASSWORD` définies dans le `.env` (voir section "Configuration requise avant de lancer le projet").

`pipeline_user` et `analyste_user` sont ensuite créés automatiquement par le script `0.creation_utilisateurs.py`, première étape exécutée par `orchestration_migration_complete.py`. Ce script se connecte avec `admin_si` et crée les deux utilisateurs **s'ils n'existent pas déjà** (idempotent — pas de doublon en cas de relance).

### Hachage des mots de passe

MongoDB ne stocke jamais les mots de passe en clair : il applique automatiquement un hachage (algorithme SCRAM, basé sur SHA), avec un salage pour que deux mots de passe identiques ne produisent jamais le même résultat stocké. Ce hachage est **irréversible** (contrairement à un chiffrement, qui utilise une clé et peut être inversé) : même en cas de vol de la base, personne ne peut retrouver le mot de passe d'origine à partir de ce qui est stocké. On ne peut que **vérifier** si un mot de passe fourni correspond, pas le "récupérer".

### Limites connues

- MongoDB ne permet pas nativement de restreindre un utilisateur à **certaines données seulement** (par exemple, un médecin qui ne verrait que ses propres patients, ou une secrétaire limitée à certains champs). Ce filtrage nécessiterait soit une logique applicative en plus, soit des vues MongoDB dédiées, non implémenté ici, pour rester sur un périmètre réaliste pour ce projet.
- Les mots de passe utilisés sont volontairement simples (contexte d'exercice). En production, il faudrait des mots de passe forts.

---

## Auteur

Manon Lemaitre — Data Engineer en formation
