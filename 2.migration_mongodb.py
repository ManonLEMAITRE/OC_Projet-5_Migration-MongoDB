import os 
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Connexion à MongoDB
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongo_uri)

# Créer ou accéder à la base de données
db = client['healthcare_db']

# Créer ou accéder à la collection
collection = db['patients']

# Supprimer les documents existants pour éviter les doublons lors de l'insertion
collection.delete_many({})

# Charger les données nettoyées
df = pd.read_csv('healthcare_dataset_cleaned.csv')

# Refaire la conversion des colonnes dates en format datetime avant migration
df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])


print(f"📊 Chargement de {len(df)} patients...")

# Convertir chaque ligne du DataFrame en document MongoDB
try:
    # Convertir le DataFrame en liste de dictionnaires
    documents = df.to_dict('records')
    
    # Insérer les documents dans MongoDB
    insertion = collection.insert_many(documents)
    
    print(f"✅ {len(insertion.inserted_ids)} patients insérés avec succès!")
    print(f"Premier ID inséré : {insertion.inserted_ids[0]}")
    
except DuplicateKeyError as e:
    print(f"❌ Erreur : Doublon détecté - {e}")
except Exception as e:
    print(f"❌ Erreur lors de l'insertion : {e}")

finally:
    client.close()
    print("✅ Connexion fermée")