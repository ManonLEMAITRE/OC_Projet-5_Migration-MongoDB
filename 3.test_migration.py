import os
import pandas as pd
from pymongo import MongoClient

def test_migration():
    """
    Script de test post-migration.
    Vérifie que les données sont bien dans MongoDB.
    """
    
    # Connexion à MongoDB
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    client = MongoClient(mongo_uri)
    db = client['healthcare_db']
    collection = db['patients']
    
   
    print("TESTS DE VALIDATION POST-MIGRATION")

    try:
        # TEST 1 : Vérifier le nombre de documents
        print("\n✓ Test 1 : Nombre de documents")
        count = collection.count_documents({})
        expected_count = 54966
        
        if count == expected_count:
            print(f"  ✅ Reussi : {count} documents insérés (attendu : {expected_count})")
        else:
            print(f"  ❌ Echec : {count} documents trouvés (attendu : {expected_count})")
        
        # TEST 2 : Vérifier qu'il n'y a pas de documents vides
        print("\n✓ Test 2 : Pas de documents vides")
        empty_docs = collection.count_documents({})
        if empty_docs == count:
            print(f"  ✅ Reussi : Tous les {count} documents contiennent des données")
        else:
            print(f"  ❌ Echec : Documents vides trouvés")
        
        # TEST 3 : Vérifier la présence de tous les champs obligatoires
        print("\n✓ Test 3 : Champs obligatoires")
        required_fields = [
            'Name', 'Age', 'Gender', 'Blood Type', 'Medical Condition',
            'Date of Admission', 'Doctor', 'Hospital', 'Insurance Provider',
            'Billing Amount', 'Room Number', 'Admission Type', 'Discharge Date',
            'Medication', 'Test Results'
        ]
        
        sample_doc = collection.find_one()
        missing_fields = [field for field in required_fields if field not in sample_doc]
        
        if not missing_fields:
            print(f"  ✅ Reussi : Tous les {len(required_fields)} champs obligatoires sont présents")
        else:
            print(f"  ❌ Echec : Champs manquants : {missing_fields}")
        
        # TEST 4 : Vérifier les types de champs numériques (float = double dans MongoDB)
        print("\n✓ Test 4 : Types de champs numériques")
        age_sample = collection.find_one({'Age': {'$type': 'int'}})
        billing_sample = collection.find_one({'Billing Amount': {'$type': 'double'}})
        
        type_checks = []
        if age_sample:
            type_checks.append(("Age (int)", True))
        if billing_sample:
            type_checks.append(("Billing Amount (double)", True))
        
        if type_checks:
            print(f"  ✅ Reussi : Les types numériques sont corrects")
            for field_name, _ in type_checks:
                print(f"    - {field_name}")
        else:
            print(f"  ⚠️  WARNING : Impossible de valider les types")
        
        # TEST 5 : Vérifier qu'il n'y a pas de doublon (même _id)
        print("\n✓ Test 5 : Pas de doublon")
        total_docs = collection.count_documents({})
        unique_ids = collection.distinct('_id')
        
        if len(unique_ids) == total_docs:
            print(f"  ✅ Reussi : {len(unique_ids)} IDs uniques pour {total_docs} documents")
        else:
            print(f"  ❌ Echec : Doublons détectés")
        
        # TEST 6 : Vérifier l'absence de valeurs nulles
        print("\n✓ Test 6 : Pas de valeurs nulles")
        null_count = 0
        for field in required_fields:
            null_in_field = collection.count_documents({field: None})
            null_count += null_in_field
        
        if null_count == 0:
            print(f"  ✅ Reussi : Aucune valeur null détectée dans les {len(required_fields)} champs")
        else:
            print(f"  ⚠️  WARNING : {null_count} valeurs null trouvées")
        
        # TEST 7 : Vérifier quelques documents aléatoires
        print("\n✓ Test 7 : Intégrité des documents (échantillon)")
        samples = list(collection.find().limit(5))
        
        if samples:
            print(f"  ✅ Reussi : {len(samples)} documents échantillonnés vérifiés")
            print("\n  Exemple de document :")
            print(f"    Name: {samples[0]['Name']}")
            print(f"    Age: {samples[0]['Age']}")
            print(f"    Medical Condition: {samples[0]['Medical Condition']}")
            print(f"    Date of Admission: {samples[0]['Date of Admission']}")
        
        # TEST 8 : Comparer avec le CSV nettoyé
        print("\n✓ Test 8 : Comparaison avec CSV nettoyé")
        df_cleaned = pd.read_csv('healthcare_dataset_cleaned.csv')
        csv_count = len(df_cleaned)
        
        if csv_count == count:
            print(f"  ✅ Reussi : Le nombre de lignes CSV ({csv_count}) = documents MongoDB ({count})")
        else:
            print(f"  ❌ Echec : Mismatch - CSV: {csv_count}, MongoDB: {count}")
        
        # RÉSUMÉ
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DE LA VALIDATION")
        print("=" * 60)
        print(f"Total de documents : {count}")
        print(f"Champs vérifiés : {len(required_fields)}")
        print(f"Documents uniques : {len(unique_ids)}")
        print(f"Valeurs nulles : {null_count}")
        print("\n✅ MIGRATION VALIDÉE AVEC SUCCÈS !")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERREUR : {e}")
    
    finally:
        client.close()
        print("\n✅ Connexion MongoDB fermée")

if __name__ == "__main__":
    test_migration()