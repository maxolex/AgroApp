import pyodbc

# Chemin vers votre fichier Access
connection_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Maxolex\Documents\Projects\agroApp\agroApp.accdb;'

# Connexion à la base de données Access
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Obtenir les noms des tables
table_names = [table.table_name for table in cursor.tables(tableType='TABLE')]

# Obtenir les colonnes pour chaque table
table_structure = {}
for table in table_names:
    cursor.execute(f"SELECT * FROM {table} WHERE 1=0")
    columns = [column[0] for column in cursor.description]
    table_structure[table] = columns

# Afficher la structure des tables
for table, columns in table_structure.items():
    print(f"Table: {table}")
    for column in columns:
        print(f"  - {column}")

# Fermer la connexion
conn.close()
