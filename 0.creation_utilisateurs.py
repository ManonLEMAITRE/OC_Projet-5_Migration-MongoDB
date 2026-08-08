"""
Création automatique des utilisateurs medecin_user et secretariat_user.

Le compte admin_si est créé automatiquement par Docker au premier démarrage
(via MONGO_INITDB_ROOT_USERNAME / MONGO_INITDB_ROOT_PASSWORD dans docker-compose.yml).

Ce script se connecte avec admin_si (seul compte existant à ce stade) pour créer
les deux autres utilisateurs. Idempotent : si un utilisateur existe déjà, il est
ignoré plutôt que recréé.
"""

import os
from pymongo import MongoClient
from pymongo.errors import OperationFailure


def connecter_admin():
    """Connexion avec le compte admin_si (root Docker), utilisé pour créer les autres users."""
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client["healthcare_db"]
    return client, db


def creer_utilisateur_si_absent(db, nom_utilisateur, mot_de_passe, roles):
    """Crée un utilisateur MongoDB s'il n'existe pas déjà."""
    utilisateurs_existants = db.command("usersInfo")["users"]
    noms_existants = [u["user"] for u in utilisateurs_existants]

    if nom_utilisateur in noms_existants:
        print(f"Utilisateur '{nom_utilisateur}' déjà existant, aucune action.")
        return

    db.command(
        "createUser",
        nom_utilisateur,
        pwd=mot_de_passe,
        roles=roles,
    )
    print(f"Utilisateur '{nom_utilisateur}' créé avec succès.")


def setup_utilisateurs():
    """Point d'entrée : crée medecin_user et analyste_user si nécessaire."""
    client, db = connecter_admin()

    try:
        creer_utilisateur_si_absent(
            db,
            "pipeline_user",
            "pipeline123",
            roles=[{"role": "readWrite", "db": "healthcare_db"}],
        )

        creer_utilisateur_si_absent(
            db,
            "analyste_user",
            "analyste123",
            roles=[{"role": "read", "db": "healthcare_db"}],
        )

    except OperationFailure as erreur:
        print(f"Erreur lors de la création des utilisateurs : {erreur}")
        raise
    finally:
        client.close()


if __name__ == "__main__":
    setup_utilisateurs()