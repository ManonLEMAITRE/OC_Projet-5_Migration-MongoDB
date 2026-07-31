from pymongo import ASCENDING
from db_utils import connecter_mongodb


def lister_index_existants(collection):
    """Affiche les index actuellement présents sur la collection."""
    print("\n Index existants avant création :")
    for index in collection.list_indexes():
        print(f"   - {index['name']}")


def supprimer_index_existants(collection):
    """Supprime tous les index existants (sauf _id_), pour repartir sur une base propre."""
    collection.drop_indexes()
    print("\n Anciens index supprimés (hors _id_)")


def create_indexes(collection):
    """
    Création des index MongoDB pour optimiser les performances
    des requêtes fréquentes.
    """
    print("=" * 70)
    print("⚡ CRÉATION DES INDEX MONGODB")
    print("=" * 70)

    # Liste des index à créer : (champs, utilité)
    indexes_a_creer = [
        ([("Name", ASCENDING)], "Accélère les recherches par nom patient"),
        ([("Medical Condition", ASCENDING), ("Medication", ASCENDING)],
         "Accélère les recherches par pathologie et médicament"),
        ([("Date of Admission", ASCENDING)], "Accélère les filtres par date d'admission"),
        ([("Hospital", ASCENDING)], "Accélère les recherches par hôpital"),
        ([("Doctor", ASCENDING)], "Accélère les recherches par docteur"),
    ]

    try:
        lister_index_existants(collection)
        supprimer_index_existants(collection)

        print("\n" + "=" * 70)
        print(" Création des nouveaux index")
        print("=" * 70)

        for i, (champs, utilite) in enumerate(indexes_a_creer, start=1):
            noms_champs = " + ".join(champ for champ, _ in champs)
            print(f"\n{i}  Index sur '{noms_champs}'")
            index_cree = collection.create_index(champs)
            print(f"    Index créé : {index_cree}")
            print(f"   Utilité : {utilite}")

        print("\n" + "=" * 70)
        print(" TOUS LES INDEX ONT ÉTÉ CRÉÉS AVEC SUCCÈS !")
        print("=" * 70)

    except Exception as e:
        print(f"\n ERREUR : {e}")


if __name__ == "__main__":
    client, collection = connecter_mongodb()
    create_indexes(collection)
    client.close()
    print("\nConnexion MongoDB fermée")