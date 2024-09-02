import pyodbc
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime
from datetime import timedelta

class AgroApp:
    def __init__(self, master):
        self.master = master
        self.master.title("AgroApp - Gestion de l'irrigation des tomates")
        
        # Connexion à la base de données
        self.conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Maxolex\Documents\Projects\agroApp\agroApp.accdb;')
        self.cursor = self.conn.cursor()
        
        # Création des onglets
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Onglets pour chaque fonctionnalité
        self.create_varietes_tab()
        self.create_parcelles_tab()
        self.create_irrigations_tab()
        self.create_fertilisations_tab()
        self.create_resultats_tab()
    
    def create_varietes_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Variétés de Tomates")
        
        # Champs de saisie
        ttk.Label(tab, text="Nom de la variété:").grid(row=0, column=0, padx=5, pady=5)
        self.nom_variete = ttk.Entry(tab)
        self.nom_variete.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Cycle de production (jours):").grid(row=1, column=0, padx=5, pady=5)
        self.cycle_production = ttk.Entry(tab)
        self.cycle_production.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Caractéristiques des fruits:").grid(row=2, column=0, padx=5, pady=5)
        self.caracteristiques = ttk.Entry(tab)
        self.caracteristiques.grid(row=2, column=1, padx=5, pady=5)
        
        # Boutons
        ttk.Button(tab, text="Ajouter", command=self.ajouter_variete).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(tab, text="Afficher toutes", command=self.afficher_varietes).grid(row=3, column=1, padx=5, pady=5)

    def ajouter_variete(self):
        nom = self.nom_variete.get()
        cycle = self.cycle_production.get()
        caract = self.caracteristiques.get()
        try:
            self.cursor.execute("INSERT INTO Varietes_Tomates (Nom_Variete, Cycle_Production, Caracteristiques_Fruits) VALUES (?, ?, ?)", (nom, cycle, caract))
            self.conn.commit()
            messagebox.showinfo("Succès", "Variété ajoutée avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout : {str(e)}")
    
    def afficher_varietes(self):
        self.cursor.execute("SELECT * FROM Varietes_Tomates")
        varietes = self.cursor.fetchall()

        style = ttk.Style()
        style.configure("Treeview", rowheight=100)
        
        result_window = tk.Toplevel(self.master)
        result_window.title("Toutes les variétés")
        
        # Créez un widget Treeview pour afficher les données sous forme de tableau
        tree = ttk.Treeview(result_window, columns=("ID", "Nom", "Cycle", "Caractéristiques"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nom", text="Nom de la variété")
        tree.heading("Cycle", text="Cycle de production")
        tree.heading("Caractéristiques", text="Caractéristiques des fruits")

        # Set column widths
        tree.column("ID", width=50)
        tree.column("Nom", width=150)
        tree.column("Cycle", width=150)
        tree.column("Caractéristiques", width=300)
        
        for variete in varietes:
            tree.insert("", "end", values=(variete[0], variete[1], variete[2], variete[3]))
        
        tree.pack(fill=tk.BOTH, expand=True)
    
    def create_parcelles_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Parcelles")
        
        # Partie gauche : Formulaire de gestion des parcelles
        frame_gestion = ttk.LabelFrame(tab, text="Gestion des parcelles")
        frame_gestion.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(frame_gestion, text="ID Parcelle:").grid(row=0, column=0, padx=5, pady=5)
        self.id_parcelle = ttk.Entry(frame_gestion)
        self.id_parcelle.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_gestion, text="Superficie (m²):").grid(row=1, column=0, padx=5, pady=5)
        self.superficie_parcelle = ttk.Entry(frame_gestion)
        self.superficie_parcelle.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_gestion, text="Variété de tomate:").grid(row=2, column=0, padx=5, pady=5)
        self.variete_parcelle = ttk.Combobox(frame_gestion)
        self.variete_parcelle.grid(row=2, column=1, padx=5, pady=5)
        self.update_varietes_combobox()
        
        ttk.Label(frame_gestion, text="Type de sol:").grid(row=3, column=0, padx=5, pady=5)
        self.type_sol = ttk.Combobox(frame_gestion, values=["Argileux", "Limoneux", "Sableux", "Argilo-limoneux", "Limono-sableux"])
        self.type_sol.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(frame_gestion, text="Date de plantation:").grid(row=4, column=0, padx=5, pady=5)
        self.date_plantation = ttk.Entry(frame_gestion)
        self.date_plantation.grid(row=4, column=1, padx=5, pady=5)
        self.date_plantation.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Button(frame_gestion, text="Ajouter/Modifier Parcelle", command=self.ajouter_modifier_parcelle).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(frame_gestion, text="Supprimer Parcelle", command=self.supprimer_parcelle).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Partie droite : Informations sur les parcelles
        frame_info = ttk.LabelFrame(tab, text="Informations sur les parcelles")
        frame_info.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.tree_parcelles = ttk.Treeview(frame_info, columns=("ID", "Superficie", "Variété", "Type de sol", "Date plantation"), show="headings")
        for col in self.tree_parcelles["columns"]:
            self.tree_parcelles.heading(col, text=col)
        self.tree_parcelles.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(frame_info, orient="vertical", command=self.tree_parcelles.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_parcelles.configure(yscrollcommand=scrollbar.set)
        
        self.tree_parcelles.bind("<<TreeviewSelect>>", self.on_parcelle_select)
        
        # Boutons d'action
        ttk.Button(tab, text="Afficher carte des parcelles", command=self.afficher_carte_parcelles).grid(row=1, column=0, pady=10)
        ttk.Button(tab, text="Analyser rendements", command=self.analyser_rendements_parcelles).grid(row=1, column=1, pady=10)
        
        # Initialisation de l'affichage des parcelles
        self.afficher_parcelles()

    def update_varietes_combobox(self):
        self.cursor.execute("SELECT Nom_Variete FROM Varietes_Tomates")
        varietes = self.cursor.fetchall()
        self.variete_parcelle['values'] = [v[0] for v in varietes]

    def ajouter_modifier_parcelle(self):
        try:
            id_parcelle = self.id_parcelle.get()
            superficie = float(self.superficie_parcelle.get())
            variete = self.variete_parcelle.get()
            type_sol = self.type_sol.get()
            date_plantation = self.date_plantation.get()
            
            if id_parcelle:  # Modification
                self.cursor.execute("""
                    UPDATE Parcelles 
                    SET Superficie = ?, ID_Variete = (SELECT ID_Variete FROM Varietes_Tomates WHERE Nom_Variete = ?),
                        Type_Sol = ?, Date_Plantation = ?
                    WHERE ID_Parcelle = ?
                """, (superficie, variete, type_sol, date_plantation, id_parcelle))
            else:  # Ajout
                self.cursor.execute("SELECT ID_Variete FROM Varietes_Tomates WHERE Nom_Variete = ?", (variete,))
                id_variete = self.cursor.fetchone()[0]
                self.cursor.execute("""
                    INSERT INTO Parcelles (Superficie, ID_Variete, Type_Sol, Date_Plantation)
                    VALUES (?, ?, ?, ?)
                """, (superficie, id_variete, type_sol, date_plantation))
            
            self.conn.commit()
            messagebox.showinfo("Succès", "Parcelle ajoutée/modifiée avec succès!")
            self.afficher_parcelles()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout/modification de la parcelle : {str(e)}")

    def supprimer_parcelle(self):
        selected_item = self.tree_parcelles.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une parcelle à supprimer.")
            return
        
        id_parcelle = self.tree_parcelles.item(selected_item)['values'][0]
        
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cette parcelle ?"):
            try:
                self.cursor.execute("DELETE FROM Parcelles WHERE ID_Parcelle = ?", (id_parcelle,))
                self.conn.commit()
                messagebox.showinfo("Succès", "Parcelle supprimée avec succès!")
                self.afficher_parcelles()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression de la parcelle : {str(e)}")

    def afficher_parcelles(self):
        self.tree_parcelles.delete(*self.tree_parcelles.get_children())
        self.cursor.execute("""
            SELECT p.ID_Parcelle, p.Superficie, v.Nom_Variete, p.Type_Sol, p.Date_Plantation
            FROM Parcelles p
            INNER JOIN Varietes_Tomates v ON p.ID_Variete = v.ID_Variete
        """)
        parcelles = self.cursor.fetchall()

        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        for parcelle in parcelles:
            self.tree_parcelles.insert("","end",values=(parcelle[0], parcelle[1], parcelle[2], parcelle[3],parcelle[4]))

    def on_parcelle_select(self, event):
        selected_item = self.tree_parcelles.selection()
        if selected_item:
            parcelle = self.tree_parcelles.item(selected_item)['values']
            self.id_parcelle.delete(0, tk.END)
            self.id_parcelle.insert(0, parcelle[0])
            self.superficie_parcelle.delete(0, tk.END)
            self.superficie_parcelle.insert(0, parcelle[1])
            self.variete_parcelle.set(parcelle[2])
            self.type_sol.set(parcelle[3])
            self.date_plantation.delete(0, tk.END)
            self.date_plantation.insert(0, parcelle[4])

    def afficher_carte_parcelles(self):
        # Cette fonction simule l'affichage d'une carte des parcelles
        carte_window = tk.Toplevel(self.master)
        carte_window.title("Carte des parcelles")
        
        canvas = tk.Canvas(carte_window, width=600, height=400)
        canvas.pack()
        
        self.cursor.execute("SELECT ID_Parcelle, Superficie FROM Parcelles")
        parcelles = self.cursor.fetchall()
        
        colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink']
        for i, parcelle in enumerate(parcelles):
            x = (i % 3) * 200 + 50
            y = (i // 3) * 150 + 50
            size = min(100, max(20, parcelle[1] / 10))  # Taille proportionnelle à la superficie
            canvas.create_rectangle(x, y, x+size, y+size, fill=colors[i % len(colors)])
            canvas.create_text(x+size/2, y+size/2, text=f"Parcelle {parcelle[0]}\n{parcelle[1]} m²")

    def analyser_rendements_parcelles(self):
        # Step 1: Execute Subquery
        self.cursor.execute("""
            SELECT r.ID_Parcelle, r.Rendement_Estime
            FROM Resultats_Production r
        """)
        resultats = self.cursor.fetchall()
        resultats_dict = {row[0]: row[1] for row in resultats}  # Convert to a dictionary

        # Step 2: Execute Main Query
        self.cursor.execute("""
            SELECT p.ID_Parcelle, v.Nom_Variete, p.Superficie
            FROM Parcelles p
            INNER JOIN Varietes_Tomates v ON p.ID_Variete = v.ID_Variete
        """)
        parcelles = self.cursor.fetchall()

        # Combine the results manually in Python
        data = []
        for parcelle in parcelles:
            id_parcelle = parcelle[0]
            rendement_estime = resultats_dict.get(id_parcelle, None)  # Get the rendement value or None
            parcelle_tuple = tuple(parcelle)  # Convert pyodbc.Row to tuple
            data.append(parcelle_tuple + (rendement_estime,))

        # data now contains the combined data

        #data = self.cursor.fetchall()
        
        df = pd.DataFrame(data, columns=["ID_Parcelle", "Variété", "Rendement", "Superficie"])
        df['Rendement_par_m2'] = df['Rendement'] / df['Superficie']
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
        
        # Graphique des rendements totaux par parcelle
        df.plot(kind='bar', x='ID_Parcelle', y='Rendement', ax=ax1)
        ax1.set_title("Rendement total par parcelle")
        ax1.set_xlabel("ID Parcelle")
        ax1.set_ylabel("Rendement (tonnes)")
        
        # Graphique des rendements par m² pour chaque variété
        df.groupby('Variété')['Rendement_par_m2'].mean().plot(kind='bar', ax=ax2)
        ax2.set_title("Rendement moyen par m² pour chaque variété")
        ax2.set_xlabel("Variété")
        ax2.set_ylabel("Rendement par m² (tonnes/m²)")
        
        plt.tight_layout()
        
        graph_window = tk.Toplevel(self.master)
        graph_window.title("Analyse des rendements par parcelle")
        
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_irrigations_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Irrigations")
        
        # Champs de saisie
        ttk.Label(tab, text="Parcelle:").grid(row=0, column=0, padx=5, pady=5)
        self.parcelle_combobox = ttk.Combobox(tab)
        self.parcelle_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.update_parcelles_combobox()
        
        ttk.Label(tab, text="Type d'irrigation:").grid(row=1, column=0, padx=5, pady=5)
        self.type_irrigation = ttk.Entry(tab)
        self.type_irrigation.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Débit d'irrigation (m³/ha):").grid(row=2, column=0, padx=5, pady=5)
        self.debit_irrigation = ttk.Entry(tab)
        self.debit_irrigation.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Nombre d'arrosages:").grid(row=3, column=0, padx=5, pady=5)
        self.nombre_arrosage = ttk.Entry(tab)
        self.nombre_arrosage.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Quantité d'eau utilisée (m³):").grid(row=4, column=0, padx=5, pady=5)
        self.quantite_eau = ttk.Entry(tab)
        self.quantite_eau.grid(row=4, column=1, padx=5, pady=5)
        
        # Boutons
        ttk.Button(tab, text="Ajouter", command=self.ajouter_irrigation).grid(row=5, column=0, padx=5, pady=5)
        ttk.Button(tab, text="Afficher toutes", command=self.afficher_irrigations).grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(tab, text="Calculer eau", command=self.calculer_eau).grid(row=5, column=2, padx=5, pady=5)

    def update_parcelles_combobox(self):
        self.cursor.execute("SELECT ID_Parcelle, Superficie FROM Parcelles")
        parcelles = self.cursor.fetchall()
        self.parcelle_combobox['values'] = [f"{p[0]} - {p[1]} m²" for p in parcelles]

    def update_parcelle_resultats_combobox(self, combobox):
            self.cursor.execute("""
                SELECT Parcelles.ID_Parcelle, Parcelles.Superficie, Varietes_Tomates.Nom_Variete 
                FROM [Parcelles]
                INNER JOIN [Varietes_Tomates] ON Parcelles.ID_Variete = Varietes_Tomates.ID_Variete
            """)

            parcelles = self.cursor.fetchall()
            combobox['values'] = [f"{p[0]} - {p[1]} m² - {p[2]}" for p in parcelles]

    def ajouter_irrigation(self):
        try:
            parcelle_id = int(self.parcelle_combobox.get().split('-')[0].strip())
            type_irr = self.type_irrigation.get()
            debit = float(self.debit_irrigation.get())
            nb_arrosage = int(self.nombre_arrosage.get())
            quantite_eau = float(self.quantite_eau.get())
            
            self.cursor.execute("INSERT INTO Irrigations (ID_Parcelle, Type_Irrigation, Debit_Irrigation, Nombre_Arrosage, Quantite_Eau_Utilisee) VALUES (?, ?, ?, ?, ?)", 
                                (parcelle_id, type_irr, debit, nb_arrosage, quantite_eau))
            self.conn.commit()
            messagebox.showinfo("Succès", "Irrigation ajoutée avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout : {str(e)}")

    def afficher_irrigations(self):
        self.cursor.execute("""
            SELECT i.ID_Irrigation, p.Superficie, i.Type_Irrigation, i.Debit_Irrigation, i.Nombre_Arrosage, i.Quantite_Eau_Utilisee 
            FROM Irrigations i 
            INNER JOIN Parcelles p ON i.ID_Parcelle = p.ID_Parcelle
        """)
        irrigations = self.cursor.fetchall()
        
        result_window = tk.Toplevel(self.master)
        result_window.title("Toutes les irrigations")
        
        tree = ttk.Treeview(result_window, columns=("ID", "Superficie", "Type", "Debit", "Nb Arrosages", "Quantité Eau"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Superficie", text="Superficie (m²)")
        tree.heading("Type", text="Type d'irrigation")
        tree.heading("Debit", text="Débit (m³/ha)")
        tree.heading("Nb Arrosages", text="Nombre d'arrosages")
        tree.heading("Quantité Eau", text="Quantité d'eau (m³)")
        
        for irrigation in irrigations:
            tree.insert("", "end", values=(irrigation[0],irrigation[1],irrigation[2],irrigation[3],irrigation[4],irrigation[5]))
        
        tree.pack(fill=tk.BOTH, expand=True)

    def calculer_eau(self):
        try:
            parcelle_id = int(self.parcelle_combobox.get().split('-')[0].strip())
            debit = float(self.debit_irrigation.get())
            nb_arrosage = int(self.nombre_arrosage.get())
            
            self.cursor.execute("SELECT Superficie FROM Parcelles WHERE ID_Parcelle = ?", (parcelle_id,))
            superficie = self.cursor.fetchone()[0]
            
            quantite_eau = (debit * superficie / 10000) * nb_arrosage  # Conversion m³/ha en m³/m²
            self.quantite_eau.delete(0, tk.END)
            self.quantite_eau.insert(0, f"{quantite_eau:.2f}")
            
            messagebox.showinfo("Calcul", f"Quantité d'eau calculée : {quantite_eau:.2f} m³")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du calcul : {str(e)}")
    
    def create_fertilisations_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Fertilisations")
        
        # Champs de saisie
        ttk.Label(tab, text="Parcelle:").grid(row=0, column=0, padx=5, pady=5)
        self.parcelle_ferti_combobox = ttk.Combobox(tab)
        self.parcelle_ferti_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.update_parcelle_resultats_combobox(self.parcelle_ferti_combobox)
        
        ttk.Label(tab, text="Type d'engrais:").grid(row=1, column=0, padx=5, pady=5)
        self.type_engrais = ttk.Entry(tab)
        self.type_engrais.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Quantité épandue (kg/ha):").grid(row=2, column=0, padx=5, pady=5)
        self.quantite_epandue = ttk.Entry(tab)
        self.quantite_epandue.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Méthode d'application:").grid(row=3, column=0, padx=5, pady=5)
        self.methode_application = ttk.Combobox(tab, values=["Épandage", "Fertigation", "Foliaire"])
        self.methode_application.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Date d'application:").grid(row=4, column=0, padx=5, pady=5)
        self.date_application = ttk.Entry(tab)
        self.date_application.grid(row=4, column=1, padx=5, pady=5)
        self.date_application.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Boutons
        ttk.Button(tab, text="Ajouter fertilisation", command=self.ajouter_fertilisation).grid(row=5, column=0, padx=5, pady=5)
        ttk.Button(tab, text="Afficher fertilisations", command=self.afficher_fertilisations).grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(tab, text="Planifier fertilisations", command=self.planifier_fertilisations).grid(row=5, column=2, padx=5, pady=5)
        ttk.Button(tab, text="Exporter données", command=self.exporter_donnees_fertilisation).grid(row=6, column=0, padx=5, pady=5)

    def ajouter_fertilisation(self):
        try:
            parcelle_id = int(self.parcelle_ferti_combobox.get().split('-')[0].strip())
            type_engrais = self.type_engrais.get()
            quantite = float(self.quantite_epandue.get())
            methode = self.methode_application.get()
            date = self.date_application.get()
            
            self.cursor.execute("""
                INSERT INTO Fertilisations (ID_Parcelle, Type_Engrais, Quantite_Epandue, Methode_Application, Date_Application) 
                VALUES (?, ?, ?, ?, ?)
            """, (parcelle_id, type_engrais, quantite, methode, date))
            self.conn.commit()
            messagebox.showinfo("Succès", "Fertilisation ajoutée avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout de la fertilisation : {str(e)}")

    def afficher_fertilisations(self):
        self.cursor.execute("""
            SELECT f.ID_Fertilisation, subquery.Superficie, subquery.Nom_Variete, f.Type_Engrais, f.Quantite_Epandue, f.Methode_Application, f.Date_Application
            FROM [Fertilisations] f
            INNER JOIN (
                SELECT p.ID_Parcelle, p.Superficie, v.Nom_Variete
                FROM [Parcelles] p
                INNER JOIN [Varietes_Tomates] v ON p.ID_Variete = v.ID_Variete
            ) subquery ON f.ID_Parcelle = subquery.ID_Parcelle
        """)

        fertilisations = self.cursor.fetchall()

        print(fertilisations)
        
        result_window = tk.Toplevel(self.master)
        result_window.title("Historique des fertilisations")
        
        tree = ttk.Treeview(result_window, columns=("ID", "Superficie", "Variété", "Type Engrais", "Quantité", "Méthode", "Date"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Superficie", text="Superficie (m²)")
        tree.heading("Variété", text="Variété de tomate")
        tree.heading("Type Engrais", text="Type d'engrais")
        tree.heading("Quantité", text="Quantité (kg/ha)")
        tree.heading("Méthode", text="Méthode d'application")
        tree.heading("Date", text="Date d'application")
        
        for fertilisation in fertilisations:
            tree.insert("", "end", values=(fertilisation[0], fertilisation[1], fertilisation[2],fertilisation[3],fertilisation[4],fertilisation[5],fertilisation[6]))
        
        tree.pack(fill=tk.BOTH, expand=True)

    def planifier_fertilisations(self):
        plan_window = tk.Toplevel(self.master)
        plan_window.title("Planification des fertilisations")
        
        ttk.Label(plan_window, text="Parcelle:").grid(row=0, column=0, padx=5, pady=5)
        parcelle_combobox = ttk.Combobox(plan_window)
        parcelle_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.update_parcelle_resultats_combobox(parcelle_combobox)
        
        ttk.Label(plan_window, text="Nombre d'applications:").grid(row=1, column=0, padx=5, pady=5)
        nb_applications = ttk.Entry(plan_window)
        nb_applications.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(plan_window, text="Intervalle (jours):").grid(row=2, column=0, padx=5, pady=5)
        intervalle = ttk.Entry(plan_window)
        intervalle.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(plan_window, text="Générer plan", command=lambda: self.generer_plan_fertilisation(parcelle_combobox.get(), nb_applications.get(), intervalle.get())).grid(row=3, column=0, columnspan=2, pady=10)

    def generer_plan_fertilisation(self, parcelle, nb_applications, intervalle):
        try:
            parcelle_id = int(parcelle.split('-')[0].strip())
            nb_applications = int(nb_applications)
            intervalle = int(intervalle)
            
            dates = [datetime.now() + timedelta(days=i*intervalle) for i in range(nb_applications)]
            
            plan_window = tk.Toplevel(self.master)
            plan_window.title("Plan de fertilisation")
            
            tree = ttk.Treeview(plan_window, columns=("Date", "Action"), show="headings")
            tree.heading("Date", text="Date prévue")
            tree.heading("Action", text="Action")
            
            for date in dates:
                tree.insert("", "end", values=(date.strftime("%Y-%m-%d"), "Appliquer fertilisation"))
            
            tree.pack(fill=tk.BOTH, expand=True)
            
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")

    def exporter_donnees_fertilisation(self):
        self.cursor.execute("""
            SELECT p.ID_Parcelle, v.Nom_Variete, f.Type_Engrais, f.Quantite_Epandue, f.Methode_Application, f.Date_Application
            FROM (Fertilisations f
            INNER JOIN Parcelles p ON f.ID_Parcelle = p.ID_Parcelle)
            INNER JOIN Varietes_Tomates v ON p.ID_Variete = v.ID_Variete
        """)
        data = self.cursor.fetchall()

        data = [tuple(row) for row in data]

        if len(data) > 0:
            df = pd.DataFrame(data, columns=["ID Parcelle", "Variété", "Type Engrais", "Quantité (kg/ha)", "Méthode", "Date"])

            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Exportation réussie", f"Les données ont été exportées vers {file_path}")
        else:
            print("Error: No data fetched or data format is incorrect.")
            messagebox.showerror("Erreur d'exportation", "Les données récupérées ne correspondent pas au format attendu.")


    
    def create_resultats_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Résultats de Production")
        
        # Champs de saisie
        ttk.Label(tab, text="Parcelle:").grid(row=0, column=0, padx=5, pady=5)
        self.parcelle_resultats_combobox = ttk.Combobox(tab)
        self.parcelle_resultats_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.update_parcelle_resultats_combobox(self.parcelle_resultats_combobox)
        
        ttk.Label(tab, text="Hauteur des plants (m):").grid(row=1, column=0, padx=5, pady=5)
        self.hauteur_plants = ttk.Entry(tab)
        self.hauteur_plants.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Poids moyen des fruits (g):").grid(row=2, column=0, padx=5, pady=5)
        self.poids_moyen_fruits = ttk.Entry(tab)
        self.poids_moyen_fruits.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(tab, text="Rendement estimé (tonnes):").grid(row=3, column=0, padx=5, pady=5)
        self.rendement_estime = ttk.Entry(tab)
        self.rendement_estime.grid(row=3, column=1, padx=5, pady=5)
        
        # Boutons
        ttk.Button(tab, text="Ajouter résultat", command=self.ajouter_resultat).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(tab, text="Afficher résultats", command=self.afficher_resultats).grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(tab, text="Analyser rendements", command=self.analyser_rendements).grid(row=4, column=2, padx=5, pady=5)

    def ajouter_resultat(self):
        try:
            parcelle_id = int(self.parcelle_resultats_combobox.get().split('-')[0].strip())
            hauteur = float(self.hauteur_plants.get())
            poids_moyen = float(self.poids_moyen_fruits.get())
            rendement = float(self.rendement_estime.get())
            
            self.cursor.execute("""
                INSERT INTO Resultats_Production (ID_Parcelle, Hauteur_Plants, Poids_Moyen_Fruits, Rendement_Estime) 
                VALUES (?, ?, ?, ?)
            """, (parcelle_id, hauteur, poids_moyen, rendement))
            self.conn.commit()
            messagebox.showinfo("Succès", "Résultat de production ajouté avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout du résultat : {str(e)}")

    def afficher_resultats(self):
        self.cursor.execute("""
            SELECT r.ID_Resultat, subquery.Superficie, subquery.Nom_Variete, r.Hauteur_Plants, r.Poids_Moyen_Fruits, r.Rendement_Estime
            FROM [Resultats_Production] r
            INNER JOIN (
                SELECT p.ID_Parcelle, p.Superficie, v.Nom_Variete
                FROM [Parcelles] p
                INNER JOIN [Varietes_Tomates] v ON p.ID_Variete = v.ID_Variete
            ) subquery ON r.ID_Parcelle = subquery.ID_Parcelle
        """)

        resultats = self.cursor.fetchall()
        
        result_window = tk.Toplevel(self.master)
        result_window.title("Résultats de production")
        
        tree = ttk.Treeview(result_window, columns=("ID", "Superficie", "Variété", "Hauteur", "Poids Moyen", "Rendement"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Superficie", text="Superficie (m²)")
        tree.heading("Variété", text="Variété de tomate")
        tree.heading("Hauteur", text="Hauteur des plants (m)")
        tree.heading("Poids Moyen", text="Poids moyen des fruits (g)")
        tree.heading("Rendement", text="Rendement estimé (tonnes)")
        
        for resultat in resultats:
            tree.insert("", "end", values=(resultat[0], resultat[1], resultat[2],resultat[3],resultat[4],resultat[5]))
        
        tree.pack(fill=tk.BOTH, expand=True)

    def analyser_rendements(self):
        # Subquery to get average yields
        self.cursor.execute("""
            SELECT p.ID_Variete, Avg(r.Rendement_Estime) AS Rendement_Moyen
            FROM Resultats_Production AS r
            INNER JOIN Parcelles AS p ON r.ID_Parcelle = p.ID_Parcelle
            GROUP BY p.ID_Variete
        """)
        resultats_rendements = self.cursor.fetchall()
        
        # Query to get variety names
        self.cursor.execute("SELECT ID_Variete, Nom_Variete FROM Varietes_Tomates")
        varietes = dict(self.cursor.fetchall())
        
        # Combine results
        resultats = [(varietes.get(id_variete, "Unknown"), rendement) 
                    for id_variete, rendement in resultats_rendements]
        
        varietes = [r[0] for r in resultats]
        rendements = [r[1] for r in resultats]
        
        # Create the graph
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(varietes, rendements)
        ax.set_xlabel('Variétés de tomates')
        ax.set_ylabel('Rendement moyen estimé (tonnes)')
        ax.set_title('Rendement moyen par variété de tomate')
        plt.xticks(rotation=45, ha='right')
        
        graph_window = tk.Toplevel(self.master)
        graph_window.title("Analyse des rendements")
        
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = AgroApp(root)
    root.mainloop()