import os
from pymongo import MongoClient
from datetime import datetime

def crud_operations():
    """
    Démonstration des opérations CRUD (Create, Read, Update, Delete)
    sur la collection patients de MongoDB.
    """
    
    # Connexion à MongoDB
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    client = MongoClient(mongo_uri)
    db = client['healthcare_db']
    collection = db['patients']
    
    print("=" * 70)
    print(" OPÉRATIONS CRUD - CREATE, READ, UPDATE, DELETE")
    print("=" * 70)
    
    try:
        # ============ CREATE (Créer) ============
        print("\n" + "=" * 70)
        print("1  CREATE - Créer un nouveau document")
        print("=" * 70)
        
        # Créer un nouveau patient
        new_patient = {
            "Name": "Jean Dupont",
            "Age": 45,
            "Gender": "Male",
            "Blood Type": "O+",
            "Medical Condition": "Hypertension",
            "Date of Admission": "2026-01-15",
            "Doctor": "Dr. François Lefevre",
            "Hospital": "Hôpital Central",
            "Insurance Provider": "MAAF",
            "Billing Amount": 5200.50,
            "Room Number": 501,
            "Admission Type": "Routine",
            "Discharge Date": "2026-01-20",
            "Medication": "Lisinopril",
            "Test Results": "Normal"
        }
        
        result = collection.insert_one(new_patient)
        patient_id = result.inserted_id
        
        print(f"\n Nouveau patient créé :")
        print(f"   ID généré : {patient_id}")
        print(f"   Nom : {new_patient['Name']}")
        print(f"   Condition médicale : {new_patient['Medical Condition']}")
        
        # ============ READ (Lire) ============
        print("\n" + "=" * 70)
        print("2 READ - Lire des documents")
        print("=" * 70)
        
        
        # READ 1 : Trouver UN document par ID
        print("\n  1 : Trouver le patient par ID")
        patient = collection.find_one({"_id": patient_id})
        
        print(f"    Patient trouvé :")
        print(f"      Nom : {patient['Name']}")
        print(f"      Age : {patient['Age']} ans")
        print(f"      Groupe sanguin : {patient['Blood Type']}")
        print(f"      Médecin : {patient['Doctor']}")
        
        
        # READ 2 : Trouver PLUSIEURS documents avec un filtre
        print("\n 2 : Trouver tous les patients atteints de Cancer")
        cancer_patients = collection.find({"Medical Condition": "Cancer"})
        cancer_count = collection.count_documents({"Medical Condition": "Cancer"})
        
        print(f"    {cancer_count} patients atteints de Cancer trouvés")
        
        first_cancer = list(collection.find({"Medical Condition": "Cancer"}).limit(1))
        if first_cancer:
            print(f"      Exemple : {first_cancer[0]['Name']} ({first_cancer[0]['Age']} ans)")
        
        
        # READ 3 : Trouver avec un filtre complexe
        print("\n 3 : Patients avec Age > 60 ET Insurance = Medicare")
        elderly_medicare = list(collection.find({
            "Age": {"$gt": 60},
            "Insurance Provider": "Medicare"
        }).limit(5))
        
        elderly_count = collection.count_documents({
            "Age": {"$gt": 60},
            "Insurance Provider": "Medicare"
        })
        
        print(f"    {elderly_count} patients correspondent à ces critères")
        if elderly_medicare:
            for patient in elderly_medicare[:2]:
                print(f"      - {patient['Name']} ({patient['Age']} ans)")
                
                
            
        # READ 4 : Lire avec tri et limite
        print("\n 4 : Top 3 patients avec montant de facturation le plus élevé")
        top_billing = list(collection.find().sort("Billing Amount", -1).limit(3))
        
        print(f"     Top 3 patients :")
        for i, patient in enumerate(top_billing, 1):
            print(f"      {i}. {patient['Name']} : {patient['Billing Amount']:.2f}€")
        
        
        
        
        # ============ UPDATE (Modifier) ============
        print("\n" + "=" * 70)
        print("3  UPDATE - Modifier un document")
        print("=" * 70)
        
        
        # UPDATE 1 : Modifier UN champ d'un document
        print("\n  Modification 1 : Changer le numéro de chambre du nouveau patient")
        print(f"   Avant : Chambre {patient['Room Number']}")
        
        collection.update_one(
            {"_id": patient_id},
            {"$set": {"Room Number": 502}}
        )
        
        updated_patient = collection.find_one({"_id": patient_id})
        print(f"   Après : Chambre {updated_patient['Room Number']}")
        print(f"    Mise à jour effectuée")
        
        
        # UPDATE 2 : Modifier le montant de facturation
        print(f"\n  Modification 2 : Changer la facturation du patient")
        print(f"   Avant : {patient['Billing Amount']:.2f}€")
        
        collection.update_one(
            {"_id": patient_id},
            {"$set": {"Billing Amount": 6500.75}}
        )
        
        updated_patient = collection.find_one({"_id": patient_id})
        print(f"   Après : {updated_patient['Billing Amount']:.2f}€")
        print(f"    Mise à jour effectuée")
        
        # UPDATE 3 : Modifier PLUSIEURS documents (tous les patients avec une condition)
        print(f"\n  Modification 3 : Mettre à jour le médecin de tous les patients Hypertension")
        
        count_before = collection.count_documents({"Medical Condition": "Hypertension"})
        
        result = collection.update_many(
            {"Medical Condition": "Hypertension"},
            {"$set": {"Doctor": "Dr. Cardiologie Générale"}}
        )
        
        print(f"    {result.modified_count} document(s) modifié(s)")
        
        # ============ DELETE (Supprimer) ============
        print("\n" + "=" * 70)
        print("4  DELETE - Supprimer un document")
        print("=" * 70)
        
        
        # DELETE 1 : Supprimer UN document
        print(f"\n  Suppression 1 : Supprimer le patient créé (Jean Dupont)")
        print(f"   Avant : {collection.count_documents({})} patients au total")
        
        result = collection.delete_one({"_id": patient_id})
        
        print(f"    {result.deleted_count} patient supprimé")
        print(f"   Après : {collection.count_documents({})} patients au total")
        
        
        # DELETE 2 : Information (sans vraiment supprimer)
        print(f"\n  Suppression 2 : Exemple de suppression par critère")
        print(f"   Si on voulait supprimer tous les patients avec Age < 18 :")
        count_minors = collection.count_documents({"Age": {"$lt": 18}})
        print(f"     {count_minors} patient(s) correspondrait/correspondraient")
        print(f"   (  Non supprimé pour préserver les données)")
        
        
        
        # ============ STATISTIQUES FINALES ============
        print("\n" + "=" * 70)
        print("STATISTIQUES FINALES")
        print("=" * 70)
        
        total_patients = collection.count_documents({})
        
        # Moyenne d'âge
        pipeline = [{"$group": {"_id": None, "age_moyen": {"$avg": "$Age"}}}]
        avg_age = list(collection.aggregate(pipeline))
        
        # Montant moyen de facturation
        pipeline = [{"$group": {"_id": None, "facturation_moyenne": {"$avg": "$Billing Amount"}}}]
        avg_billing = list(collection.aggregate(pipeline))
        
        
        print(f"\n Données globales :")
        print(f"   Total de patients : {total_patients}")
        print(f"   Âge moyen : {avg_age[0]['age_moyen']:.1f} ans")
        print(f"   Montant moyen de facturation : {avg_billing[0]['facturation_moyenne']:.2f}€")
        
        # Répartition par condition médicale (top 5)
        print(f"\n   Top 5 conditions médicales :")
        pipeline = [
            {"$group": {"_id": "$Medical Condition", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]
        conditions = list(collection.aggregate(pipeline))
        
        for i, condition in enumerate(conditions, 1):
            print(f"      {i}. {condition['_id']} : {condition['count']} patients")
        
        print("\n" + "=" * 70)
        print(" OPÉRATIONS CRUD COMPLÉTÉES AVEC SUCCÈS !")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n ERREUR : {e}")
    
    finally:
        client.close()
        print("\n Connexion MongoDB fermée")

if __name__ == "__main__":
    crud_operations()