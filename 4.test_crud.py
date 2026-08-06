from db_utils import connecter_mongodb


def creer_patient(collection):
    """CREATE : Crée un nouveau patient et retourne son ID."""
    print("\n" + "=" * 70)
    print("1  CREATE - Créer un nouveau document")
    print("=" * 70)

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

    return patient_id


def lire_patients(collection, patient_id):
    """READ : Effectue plusieurs lectures (par ID, par filtre) et retourne le patient créé."""
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
    cancer_count = collection.count_documents({"Medical Condition": "Cancer"})
    print(f"    {cancer_count} patients atteints de Cancer trouvés")

    first_cancer = list(collection.find({"Medical Condition": "Cancer"}).limit(1))
    if first_cancer:
        print(f"      Exemple : {first_cancer[0]['Name']} ({first_cancer[0]['Age']} ans)")
        
    return patient



def modifier_patient(collection, patient_id, patient):
    """UPDATE : Modifie la chambre, la facturation."""
    print("\n" + "=" * 70)
    print("3  UPDATE - Modifier un document")
    print("=" * 70)

    # UPDATE 1 : Modifier UN champ d'un document
    print("\n  Modification 1 : Changer le numéro de chambre du nouveau patient")
    print(f"   Avant : Chambre {patient['Room Number']}")

    collection.update_one({"_id": patient_id}, {"$set": {"Room Number": 502}})
    updated_patient = collection.find_one({"_id": patient_id})
    print(f"   Après : Chambre {updated_patient['Room Number']}")
    print(f"    Mise à jour effectuée")

    # UPDATE 2 : Modifier le montant de facturation
    print(f"\n  Modification 2 : Changer la facturation du patient")
    print(f"   Avant : {patient['Billing Amount']:.2f}€")

    collection.update_one({"_id": patient_id}, {"$set": {"Billing Amount": 6500.75}})
    updated_patient = collection.find_one({"_id": patient_id})
    print(f"   Après : {updated_patient['Billing Amount']:.2f}€")
    print(f"    Mise à jour effectuée")


def supprimer_patient(collection, patient_id):
    """DELETE : Supprime le patient créé."""
    print("\n" + "=" * 70)
    print("4  DELETE - Supprimer un document")
    print("=" * 70)

    print(f"\n  Supprimer le patient créé (Jean Dupont)")
    print(f"   Avant : {collection.count_documents({})} patients au total")

    result = collection.delete_one({"_id": patient_id})

    print(f"    {result.deleted_count} patient supprimé")
    print(f"   Après : {collection.count_documents({})} patients au total")


def crud_operations(collection):
    """
    Démonstration des opérations CRUD (Create, Read, Update, Delete)
    sur la collection patients de MongoDB.
    """
    print("=" * 70)
    print(" OPÉRATIONS CRUD - CREATE, READ, UPDATE, DELETE")
    print("=" * 70)

    try:
        patient_id = creer_patient(collection)
        patient = lire_patients(collection, patient_id)
        modifier_patient(collection, patient_id, patient)
        supprimer_patient(collection, patient_id)

        print("\n" + "=" * 70)
        print(" OPÉRATIONS CRUD COMPLÉTÉES AVEC SUCCÈS !")
        print("=" * 70)

    except Exception as e:
        print(f"\n ERREUR : {e}")


if __name__ == "__main__":
    client, collection = connecter_mongodb()
    crud_operations(collection)
    client.close()
    print("\n Connexion MongoDB fermée")
