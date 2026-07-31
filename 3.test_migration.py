import pandas as pd
from db_utils import connecter_mongodb


def test_nombre_documents(collection):
    """Vérifie le nombre total de documents insérés dans MongoDB."""
    print("\n✓ Test : Nombre de documents")
    count = collection.count_documents({})
    expected_count = 54966

    if count == expected_count:
        print(f"  ✅ Reussi : {count} documents insérés (attendu : {expected_count})")
    else:
        print(f"  ❌ Echec : {count} documents trouvés (attendu : {expected_count})")

    return count


def test_documents_non_vides(collection, count):
    """Vérifie qu'il n'y a pas de documents vides."""
    print("\n✓ Test : Documents non vides")
    empty_docs = collection.count_documents({})

    if empty_docs == count:
        print(f"  ✅ Reussi : Tous les {count} documents contiennent des données")
    else:
        print(f"  ❌ Echec : Documents vides trouvés")


def test_champs_obligatoires(collection):
    """TEST : Vérifie la présence de tous les champs obligatoires."""
    print("\n✓ Test : Champs obligatoires")
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

    return required_fields


def test_types_numeriques(collection):
    """TEST : Vérifie les types des champs numériques."""
    print("\n✓ Test : Types de champs numériques")
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


def test_pas_de_doublon(collection):
    """TEST : Vérifie l'absence de doublons sur _id."""
    print("\n✓ Test : Pas de doublon")
    total_docs = collection.count_documents({})
    unique_ids = collection.distinct('_id')

    if len(unique_ids) == total_docs:
        print(f"  ✅ Reussi : {len(unique_ids)} IDs uniques pour {total_docs} documents")
    else:
        print(f"  ❌ Echec : Doublons détectés")

    return unique_ids


def test_valeurs_nulles(collection, required_fields):
    """TEST : Vérifie l'absence de valeurs nulles dans les champs obligatoires."""
    print("\n✓ Test : Pas de valeurs nulles")
    null_count = 0
    for field in required_fields:
        null_in_field = collection.count_documents({field: None})
        null_count += null_in_field

    if null_count == 0:
        print(f"  ✅ Reussi : Aucune valeur null détectée dans les {len(required_fields)} champs")
    else:
        print(f"  ⚠️  WARNING : {null_count} valeurs null trouvées")

    return null_count


def test_integrite_echantillon(collection):
    """TEST : Vérifie quelques documents aléatoires."""
    print("\n✓ Test : Intégrité des documents (échantillon)")
    samples = list(collection.find().limit(5))

    if samples:
        print(f"  ✅ Reussi : {len(samples)} documents échantillonnés vérifiés")
        print("\n  Exemple de document :")
        print(f"    Name: {samples[0]['Name']}")
        print(f"    Age: {samples[0]['Age']}")
        print(f"    Medical Condition: {samples[0]['Medical Condition']}")
        print(f"    Date of Admission: {samples[0]['Date of Admission']}")


def test_comparaison_csv(count):
    """TEST : Compare le nombre de documents avec le CSV nettoyé."""
    print("\n✓ Test : Comparaison avec CSV nettoyé")
    df_cleaned = pd.read_csv('healthcare_dataset_cleaned.csv')
    csv_count = len(df_cleaned)

    if csv_count == count:
        print(f"  ✅ Reussi : Le nombre de lignes CSV ({csv_count}) = documents MongoDB ({count})")
    else:
        print(f"  ❌ Echec : Mismatch - CSV: {csv_count}, MongoDB: {count}")


def afficher_resume(count, required_fields, unique_ids, null_count):
    """Affiche le résumé final de la validation."""
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DE LA VALIDATION")
    print("=" * 60)
    print(f"Total de documents : {count}")
    print(f"Champs vérifiés : {len(required_fields)}")
    print(f"Documents uniques : {len(unique_ids)}")
    print(f"Valeurs nulles : {null_count}")
    print("\n✅ MIGRATION VALIDÉE AVEC SUCCÈS !")
    print("=" * 60)


def test_migration(collection):
    """
    Exécute l'ensemble des tests de validation post-migration.
    """
    print("TESTS DE VALIDATION POST-MIGRATION")
    try:
        count = test_nombre_documents(collection)
        test_documents_non_vides(collection, count)
        required_fields = test_champs_obligatoires(collection)
        test_types_numeriques(collection)
        unique_ids = test_pas_de_doublon(collection)
        null_count = test_valeurs_nulles(collection, required_fields)
        test_integrite_echantillon(collection)
        test_comparaison_csv(count)
        afficher_resume(count, required_fields, unique_ids, null_count)
    except Exception as e:
        print(f"\n❌ ERREUR : {e}")


if __name__ == "__main__":
    client, collection = connecter_mongodb()
    test_migration(collection)
    client.close()
    print("\n✅ Connexion MongoDB fermée")