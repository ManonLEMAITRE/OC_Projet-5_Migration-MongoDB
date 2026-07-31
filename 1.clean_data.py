import pandas as pd 


#============= AVANT NETTOYAGE : Chargement et exploration ================
def explorer_data():
    """
    Charge le dataset brut et affiche une exploration initiale
    (aperçu, types, statistiques, doublons, valeurs manquantes).
    """
    # Charger les données depuis le fichier CSV
    df = pd.read_csv('healthcare_dataset.csv')

    print("Exploration des données :")
    print("=" * 50)

    # Afficher les premières lignes du DataFrame
    print("\nPremières lignes du DataFrame :")
    print(df.head())

    # Afficher les informations sur le DataFrame
    print("\nInformations sur le DataFrame :")
    print(df.info())

    # Afficher les statistiques descriptives du DataFrame
    print("\nStatistiques descriptives :")
    print(df.describe())

    # Doublons
    print(f"\nNombre de doublons : {df.duplicated().sum()}")

    # Exploration des doublons (on compare toutes les colonnes)
    duplicates = df[df.duplicated(keep=False)].sort_values(by='Name')
    print(f"\nPremiers doublons trouvés :")
    print(duplicates.head(10))

    # Valeurs manquantes
    print(f"\nNombre de valeurs manquantes : {df.isnull().sum().sum()}")

    # Exemple de nom non normalisé
    print("\nExemples de nom non normalisé :")
    print(df['Name'].head(10))

    return df


#============= NETTOYAGE : Suppression des doublons et normalisation ================

def nettoyer_data(df):
    """
    Nettoie le DataFrame en supprimant les doublons, en normalisant les noms
    et en convertissant les colonnes de dates en format datetime.
    """
    # Supprimer les doublons (garder le premier)
    df = df.drop_duplicates(keep='first').copy()

    # Nettoyage des noms pour mettre en majuscule la première lettre de chaque mot
    df['Name'] = df['Name'].str.title()  

    # Conversion des colonnes dates en format datetime
    df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
    df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])

    return df



#============= APRES NETTOYAGE : Vérification================

def verifier_nettoyage(df):
    """
    Vérifie le DataFrame après nettoyage pour s'assurer que les doublons
    ont été supprimés et que les types de données sont corrects.
    """
    print("\nVérification après nettoyage :")
    print("=" * 50)

    # Vérifier les doublons restants
    print(f"Doublons restants : {df.duplicated().sum()}")

    # Afficher les informations sur le DataFrame après nettoyage
    print(df.head())

    # Vérifier les types de données après nettoyage
    print(df.info())



#============= SAUVEGARDER les données nettoyées ================
def sauvegarder_data(df):
    """
    Sauvegarde le DataFrame nettoyé dans un nouveau fichier CSV.
    """
    df.to_csv('healthcare_dataset_cleaned.csv', index=False)
    print("\n✅ Données nettoyées sauvegardées dans 'healthcare_dataset_cleaned.csv'")



#============= MAIN =================
if __name__ == "__main__":
    df = explorer_data()
    df = nettoyer_data(df)
    verifier_nettoyage(df)
    sauvegarder_data(df)