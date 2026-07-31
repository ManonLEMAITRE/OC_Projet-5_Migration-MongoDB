import os
from pymongo import MongoClient

def connecter_mongodb():
    """
    Établit la connexion à MongoDB et retourne le client
    ainsi que la collection 'patients'.
    """
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    client = MongoClient(mongo_uri)
    db = client['healthcare_db']
    collection = db['patients']
    return client, collection
