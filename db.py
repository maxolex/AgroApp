import pyodbc

# Connect to the Access database
conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Maxolex\Documents\Projects\agroApp\agroApp.accdb;')
cursor = conn.cursor()

# Create the Varietes_Tomates table
cursor.execute('''
CREATE TABLE Varietes_Tomates (
    ID_Variete AUTOINCREMENT PRIMARY KEY,
    Nom_Variete TEXT,
    Cycle_Production INTEGER,
    Caracteristiques_Fruits TEXT
);
''')

# Create the Parcelles table
cursor.execute('''
CREATE TABLE Parcelles (
    ID_Parcelle AUTOINCREMENT PRIMARY KEY,
    ID_Variete INTEGER,
    Superficie DOUBLE,
    FOREIGN KEY (ID_Variete) REFERENCES Varietes_Tomates(ID_Variete)
);
''')

# Create the Irrigations table
cursor.execute('''
CREATE TABLE Irrigations (
    ID_Irrigation AUTOINCREMENT PRIMARY KEY,
    ID_Parcelle INTEGER,
    Type_Irrigation TEXT,
    Debit_Irrigation DOUBLE,
    Nombre_Arrosage INTEGER,
    Quantite_Eau_Utilisee DOUBLE,
    FOREIGN KEY (ID_Parcelle) REFERENCES Parcelles(ID_Parcelle)
);
''')

# Create the Fertilisations table
cursor.execute('''
CREATE TABLE Fertilisations (
    ID_Fertilisation AUTOINCREMENT PRIMARY KEY,
    ID_Parcelle INTEGER,
    Type_Engrais TEXT,
    Quantite_Epandue DOUBLE,
    Methode_Application TEXT,
    FOREIGN KEY (ID_Parcelle) REFERENCES Parcelles(ID_Parcelle)
);
''')

# Create the Resultats_Production table
cursor.execute('''
CREATE TABLE Resultats_Production (
    ID_Resultat AUTOINCREMENT PRIMARY KEY,
    ID_Parcelle INTEGER,
    Hauteur_Plants DOUBLE,
    Poids_Moyen_Fruits DOUBLE,
    Rendement_Estime DOUBLE,
    FOREIGN KEY (ID_Parcelle) REFERENCES Parcelles(ID_Parcelle)
);
''')

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()
