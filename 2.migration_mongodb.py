import pandas as pd
from pymongo.errors import DuplicateKeyError
from db_utils import connecter_mongodb


def clear_collection(collection):
    """
    Supprime tous les documents de la collection MongoDB.
    """
    try:
        result = collection.delete_many({})
        print(f"🗑️  {result.deleted_count} documents supprimés de la collection.")
    except Exception as e:
        print(f"❌ Erreur lors de la suppression des documents : {e}")


def charger_donnees_nettoyees():
    """
    Charge le CSV nettoyé et reconvertit les colonnes de dates en datetime.
    """
    df = pd.read_csv('healthcare_dataset_cleaned.csv').copy()
    df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
    df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])
    return df


def migrer_data(collection, df):
    """
    Insère les documents du DataFrame dans la collection MongoDB.
    """
    print(f"📊 Chargement de {len(df)} patients...")
    try:
        documents = df.to_dict('records')
        insertion = collection.insert_many(documents)
        print(f"✅ {len(insertion.inserted_ids)} patients insérés avec succès!")
        print(f"Premier ID inséré : {insertion.inserted_ids[0]}")
    except DuplicateKeyError as e:
        print(f"❌ Erreur : Doublon détecté - {e}")
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion : {e}")


if __name__ == "__main__":
    client, collection = connecter_mongodb()
    clear_collection(collection)
    df = charger_donnees_nettoyees()
    migrer_data(collection, df)
    client.close()
    print("✅ Connexion fermée")