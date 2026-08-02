import subprocess 

scripts = [
    ["python", "0.creation_utilisateurs.py"],
    ["python", "1.clean_data.py"],
    ["python", "2.migration_mongodb.py"],
    ["python", "3.test_migration.py"],
    ["python", "4.test_crud.py"],
    ["python", "5.generer_index.py"]
]

for script in scripts:
    resultat = subprocess.run(script)
    if resultat.returncode != 0:
        print(f"Erreur à l'étape : {script}")
        break
    else:
        print(f" Étape réussie : {script}")
    
