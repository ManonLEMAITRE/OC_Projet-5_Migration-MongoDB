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
        
        # INDEX 2 : Index sur Age (filtrage par âge)
        print("\n2  Index sur 'Age' (recherche par âge)")
        index_age = collection.create_index([("Age", ASCENDING)])
        print(f"    Index créé : {index_age}")
        print(f"   Utilité : Accélère les filtres par âge")
        
        # INDEX 3 : Index sur Date of Admission (filtrage par date d'admission)
        print("\n3  Index sur 'Date of Admission' (recherche par date)")
        index_admission = collection.create_index([("Date of Admission", ASCENDING)])
        print(f"    Index créé : {index_admission}")
        print(f"   Utilité : Accélère les filtres par date d'admission")
        
        # INDEX 4 : Index sur Medical Condition (regroupement par condition)
        print("\n4  Index sur 'Medical Condition' (recherche par condition)")
        index_condition = collection.create_index([("Medical Condition", ASCENDING)])
        print(f"    Index créé : {index_condition}")
        print(f"   Utilité : Accélère les recherches/agrégations par condition médicale")
        
        # INDEX 5 : Index sur Hospital (recherche par hôpital)
        print("\n5 Index sur 'Hospital' (recherche par hôpital)")
        index_hospital = collection.create_index([("Hospital", ASCENDING)])
        print(f"    Index créé : {index_hospital}")
        print(f"   Utilité : Accélère les recherches par hôpital")
    
        
        # INDEX 6 : Index sur Billing Amount (tri par montant)
        print("\n6  Index sur 'Billing Amount' (tri par montant)")
        index_billing = collection.create_index([("Billing Amount", DESCENDING)])
        print(f"   Index créé : {index_billing}")
        print(f"   Utilité : Accélère le tri par montant de facturation")
        
        # INDEX 7 : Index sur Insurance Provider
        print("\n7 Index sur 'Insurance Provider' (recherche par assureur)")
        index_insurance = collection.create_index([("Insurance Provider", ASCENDING)])
        print(f"    Index créé : {index_insurance}")
        print(f"   Utilité : Accélère les recherches par fournisseur d'assurance")
        
        # INDEX 8 : Index sur Admission Type
        print("\n8  Index sur 'Admission Type' (recherche par type d'admission)")
        index_admission_type = collection.create_index([("Admission Type", ASCENDING)])
        print(f"    Index créé : {index_admission_type}")
        print(f"   Utilité : Accélère les filtres par type d'admission")

        
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