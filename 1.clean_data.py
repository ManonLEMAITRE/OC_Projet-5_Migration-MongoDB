import pandas as pd 


# Charger les données depuis le fichier CSV
df = pd.read_csv('healthcare_dataset.csv')


#=============AVANT NETTOYAGE================

# Afficher les premières lignes du DataFrame
print(df.head())

# Afficher les informations sur le DataFrame
print(df.info())

# Afficher les statistiques descriptives du DataFrame
print(df.describe())

# Doublons 
print(f"Nombre de doublons : {df.duplicated().sum()}")

## Exploration des doublons 
# Trouve les doublons (on compare toutes les colonnes)
duplicates = df[df.duplicated(keep=False)].sort_values(by='Name')

print(f"\nPremiers doublons trouvés :")
print(duplicates.head(10))


#Valeurs manquantes 
print(f"Nombre de valeurs manquantes : {df.isnull().sum().sum()}")

# Exemple de nom non normalisé
print("Exemples de nom non normalisé :")
print(df['Name'].head(10))



#=============NETTOYAGE================
# Supprimer les doublons (garder le premier)
df = df.drop_duplicates(keep='first')

# Nettoyage des noms pour mettre en majuscule la première lettre de chaque mot
df['Name'] = df['Name'].str.title()  

# Conversion des colonnes dates en format datetime
df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])


#=============APRES NETTOYAGE================
print(f"Doublons restants : {df.duplicated().sum()}")

# Afficher les informations sur le DataFrame après nettoyage
print(df.head())

# Vérifier les types de données après nettoyage
print(df.info())



#=============SAUVEGARDE================
df.to_csv('healthcare_dataset_cleaned.csv', index=False)