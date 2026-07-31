import os 
from pymongo import MongoClient, ASCENDING, DESCENDING

def create_indexes():
    """
    Création des index MongoDB pour optimiser les performances
    des requêtes fréquentes.
    """
    
    # Connexion à MongoDB
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    client = MongoClient(mongo_uri)
    db = client['healthcare_db']
    collection = db['patients']
    
    print("=" * 70)
    print("⚡ CRÉATION DES INDEX MONGODB")
    print("=" * 70)
    
    try:
        # Lister les index existants
        print("\n Index existants avant création :")
        existing_indexes = collection.list_indexes()
        for index in existing_indexes:
            print(f"   - {index['name']}")
        
        print("\n" + "=" * 70)
        print(" Création des nouveaux index")
        print("=" * 70)
        
        # INDEX 1 : Index sur Name (recherche de patients par nom)
        print("\n1  Index sur 'Name' (recherche par nom)")
        index_name = collection.create_index([("Name", ASCENDING)])
        print(f"    Index créé : {index_name}")
        print(f"   Utilité : Accélère les recherches par nom patient")
        
        # INDEX 2 : Index conjugué sur la pathologie et sur le médicament 
        print("\n2  Index conjugué sur Pathologie et Médicament")
        index_patho_medic = collection.create_index([("Medical Condition", ASCENDING), ("Medication", ASCENDING)])
        print(f"    Index créé : {index_patho_medic}")
        print(f"   Utilité : Accélère les recherches par pathologie et médicament")
        
        # INDEX 3 : Index sur Date of Admission (filtrage par date d'admission)
        print("\n3  Index sur 'Date of Admission' (recherche par date)")
        index_admission = collection.create_index([("Date of Admission", ASCENDING)])
        print(f"    Index créé : {index_admission}")
        print(f"   Utilité : Accélère les filtres par date d'admission")
        
        # INDEX 4 : Index sur Hospital (recherche par hôpital)
        print("\n4 Index sur 'Hospital' (recherche par hôpital)")
        index_hospital = collection.create_index([("Hospital", ASCENDING)])
        print(f"    Index créé : {index_hospital}")
        print(f"   Utilité : Accélère les recherches par hôpital")
    
        ## INDEX 5 : Index sur Docteur (recherche par docteur)
        print("\n5 Index sur 'Doctor' (recherche par docteur)")
        index_doctor = collection.create_index([("Doctor", ASCENDING)])
        print(f"    Index créé : {index_doctor}")
        print(f"   Utilité : Accélère les recherches par docteur")

        
        print("\n" + "=" * 70)
        print(" TOUS LES INDEX ONT ÉTÉ CRÉÉS AVEC SUCCÈS !")
        print("=" * 70)

        
    except Exception as e:
        print(f"\n ERREUR : {e}")
    
    finally:
        client.close()
        print("\nConnexion MongoDB fermée")

if __name__ == "__main__":
    create_indexes()