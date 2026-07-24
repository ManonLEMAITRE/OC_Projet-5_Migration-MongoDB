import pandas as pd
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Créer ou accéder à la base de données
db = client['healthcare_db']

# Créer ou accéder à la collection
collection = db['patients']

# Charger les données nettoyées
df = pd.read_csv('healthcare_dataset_cleaned.csv')

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