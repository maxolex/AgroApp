import pyodbc
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class IrrigationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Système d'irrigation goutte à goutte")
        self.master.minsize(800, 600)  # Taille minimale de la fenêtre
        
        # Connexion à la base de données
        self.conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Maxolex\Documents\Projects\agroApp\agroApp.accdb;')
        self.cursor = self.conn.cursor()
        
        # Création de l'interface utilisateur
        self.create_widgets()
    
    def create_widgets(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Onglets existants (Irrigation et Fertilisation)
        self.irrigation_frame = ttk.Frame(self.notebook)
        self.fertilisation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.irrigation_frame, text="Irrigation")
        self.notebook.add(self.fertilisation_frame, text="Fertilisation")

        # Nouveaux onglets
        self.rapports_frame = ttk.Frame(self.notebook)
        self.besoins_frame = ttk.Frame(self.notebook)
        self.recommandations_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.rapports_frame, text="Rapports de croissance")
        self.notebook.add(self.besoins_frame, text="Besoins en eau et nutriments")
        self.notebook.add(self.recommandations_frame, text="Recommandations")

        # Widgets pour l'irrigation
        ttk.Label(self.irrigation_frame, text="Parcelle ID:").grid(row=0, column=0, padx=5, pady=5)
        self.irrigation_parcelle_id = ttk.Entry(self.irrigation_frame)
        self.irrigation_parcelle_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.irrigation_frame, text="Durée (minutes):").grid(row=1, column=0, padx=5, pady=5)
        self.irrigation_duree = ttk.Entry(self.irrigation_frame)
        self.irrigation_duree.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.irrigation_frame, text="Débit (L/min):").grid(row=2, column=0, padx=5, pady=5)
        self.irrigation_debit = ttk.Entry(self.irrigation_frame)
        self.irrigation_debit.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.irrigation_frame, text="Ajouter Irrigation", command=self.ajouter_irrigation).grid(row=3, column=0, columnspan=2, pady=10)

        # Widgets pour la fertilisation
        ttk.Label(self.fertilisation_frame, text="Parcelle ID:").grid(row=0, column=0, padx=5, pady=5)
        self.fertilisation_parcelle_id = ttk.Entry(self.fertilisation_frame)
        self.fertilisation_parcelle_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.fertilisation_frame, text="Type d'engrais:").grid(row=1, column=0, padx=5, pady=5)
        self.fertilisation_type_engrais = ttk.Entry(self.fertilisation_frame)
        self.fertilisation_type_engrais.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.fertilisation_frame, text="Quantité (kg):").grid(row=2, column=0, padx=5, pady=5)
        self.fertilisation_quantite = ttk.Entry(self.fertilisation_frame)
        self.fertilisation_quantite.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.fertilisation_frame, text="Ajouter Fertilisation", command=self.ajouter_fertilisation).grid(row=3, column=0, columnspan=2, pady=10)

    def clear_irrigation_fields(self):
        self.irrigation_parcelle_id.delete(0, tk.END)
        self.irrigation_duree.delete(0, tk.END)
        self.irrigation_debit.delete(0, tk.END)

    def clear_fertilisation_fields(self):
        self.fertilisation_parcelle_id.delete(0, tk.END)
        self.fertilisation_type_engrais.delete(0, tk.END)
        self.fertilisation_quantite.delete(0, tk.END)

        # Configuration des nouveaux onglets
        self.setup_rapports_tab()
        self.setup_besoins_tab()
        self.setup_recommandations_tab()

    def setup_rapports_tab(self):
        ttk.Label(self.rapports_frame, text="Sélectionnez une variété de tomate:").pack(pady=10)
        self.variete_combobox = ttk.Combobox(self.rapports_frame, values=self.get_varietes())
        self.variete_combobox.pack(pady=5)
        ttk.Button(self.rapports_frame, text="Afficher le rapport de croissance", command=self.afficher_rapport_croissance).pack(pady=10)
        
        self.graph_frame = ttk.Frame(self.rapports_frame)
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def setup_besoins_tab(self):
        ttk.Label(self.besoins_frame, text="Sélectionnez une variété de tomate:").pack(pady=10)
        self.besoins_variete_combobox = ttk.Combobox(self.besoins_frame, values=self.get_varietes())
        self.besoins_variete_combobox.pack(pady=5)
        ttk.Button(self.besoins_frame, text="Calculer les besoins", command=self.calculer_besoins).pack(pady=10)
        
        self.besoins_result = tk.Text(self.besoins_frame, height=10, width=50)
        self.besoins_result.pack(pady=10)

    def setup_recommandations_tab(self):
        ttk.Label(self.recommandations_frame, text="Sélectionnez une parcelle:").pack(pady=10)
        self.parcelle_combobox = ttk.Combobox(self.recommandations_frame, values=self.get_parcelles())
        self.parcelle_combobox.pack(pady=5)
        ttk.Button(self.recommandations_frame, text="Générer des recommandations", command=self.generer_recommandations).pack(pady=10)
        
        self.recommandations_result = tk.Text(self.recommandations_frame, height=10, width=50)
        self.recommandations_result.pack(pady=10)

    def get_varietes(self):
        self.cursor.execute("SELECT Nom_Variete FROM Varietes_Tomates")
        return [row.Nom_Variete for row in self.cursor.fetchall()]

    def get_parcelles(self):
        self.cursor.execute("SELECT ID_Parcelle FROM Parcelles")
        return [str(row.ID_Parcelle) for row in self.cursor.fetchall()]

    def afficher_rapport_croissance(self):
        variete = self.variete_combobox.get()
        if not variete:
            messagebox.showwarning("Attention", "Veuillez sélectionner une variété de tomate.")
            return

        # Simulons des données de croissance (à remplacer par des données réelles de votre base de données)
        jours = list(range(1, 31))
        croissance = [i * 1.5 for i in jours]  # Croissance linéaire simulée

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(jours, croissance)
        ax.set_xlabel("Jours")
        ax.set_ylabel("Croissance (cm)")
        ax.set_title(f"Croissance de la variété {variete}")

        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def calculer_besoins(self):
        variete = self.besoins_variete_combobox.get()
        if not variete:
            messagebox.showwarning("Attention", "Veuillez sélectionner une variété de tomate.")
            return

        # Simulons le calcul des besoins (à remplacer par des calculs réels basés sur votre base de données)
        besoins_eau = 2.5  # Litres par jour
        besoins_azote = 0.5  # grammes par jour
        besoins_phosphore = 0.3  # grammes par jour
        besoins_potassium = 0.7  # grammes par jour

        result = f"Besoins quotidiens pour la variété {variete}:\n\n"
        result += f"Eau: {besoins_eau} litres\n"
        result += f"Azote: {besoins_azote} g\n"
        result += f"Phosphore: {besoins_phosphore} g\n"
        result += f"Potassium: {besoins_potassium} g"

        self.besoins_result.delete('1.0', tk.END)
        self.besoins_result.insert(tk.END, result)

    def generer_recommandations(self):
        parcelle = self.parcelle_combobox.get()
        if not parcelle:
            messagebox.showwarning("Attention", "Veuillez sélectionner une parcelle.")
            return

        # Simulons des recommandations (à remplacer par des recommandations basées sur vos données réelles)
        recommandations = f"Recommandations pour la parcelle {parcelle}:\n\n"
        recommandations += "1. Augmenter la fréquence d'irrigation à 3 fois par jour.\n"
        recommandations += "2. Appliquer un engrais riche en potassium la semaine prochaine.\n"
        recommandations += "3. Surveiller les signes de carence en calcium sur les feuilles.\n"
        recommandations += "4. Maintenir une humidité du sol entre 60% et 70%."

        self.recommandations_result.delete('1.0', tk.END)
        self.recommandations_result.insert(tk.END, recommandations)

    def ajouter_irrigation(self):
        try:
            parcelle_id = int(self.irrigation_parcelle_id.get())
            duree = float(self.irrigation_duree.get())
            debit = float(self.irrigation_debit.get())
            date_heure = datetime.now()

            sql = """INSERT INTO Irrigations (ID_Parcelle, Date_Irrigation, Heure, Duree, Debit)
                     VALUES (?, ?, ?, ?, ?)"""
            self.cursor.execute(sql, (parcelle_id, date_heure.date(), date_heure.time(), duree, debit))
            self.conn.commit()

            messagebox.showinfo("Succès", "Nouvelle irrigation ajoutée avec succès!")
            self.clear_irrigation_fields()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

    def ajouter_fertilisation(self):
        try:
            parcelle_id = int(self.fertilisation_parcelle_id.get())
            type_engrais = self.fertilisation_type_engrais.get()
            quantite = float(self.fertilisation_quantite.get())
            date = datetime.now().date()

            sql = """INSERT INTO Fertilisations (ID_Parcelle, Date_Fertilisation, Type_Engrais, Quantite)
                     VALUES (?, ?, ?, ?)"""
            self.cursor.execute(sql, (parcelle_id, date, type_engrais, quantite))
            self.conn.commit()

            messagebox.showinfo("Succès", "Nouvelle fertilisation ajoutée avec succès!")
            self.clear_fertilisation_fields()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = IrrigationApp(root)
    root.mainloop()