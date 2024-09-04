# AgroApp - Gestion de l'irrigation des tomates

## Description
AgroApp est une application de bureau conçue pour aider les agriculteurs à gérer efficacement la culture des tomates. Elle offre des fonctionnalités pour suivre les variétés de tomates, les parcelles, les irrigations, les fertilisations et les résultats de production.

## Fonctionnalités principales
- Gestion des variétés de tomates
- Suivi des parcelles
- Enregistrement et analyse des irrigations
- Planification et suivi des fertilisations
- Suivi des résultats de production
- Analyses graphiques des rendements

## Prérequis
- Python 3.7+
- Microsoft Access (pour la base de données)
- Pilote ODBC pour Microsoft Access

## Installation
1. Clonez ce dépôt :
   ```
   git clone https://github.com/maxolex/agroapp.git
   ```
2. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

## Configuration
1. Assurez-vous que le pilote ODBC pour Microsoft Access est installé sur votre système.
2. Modifiez la chaîne de connexion dans le fichier `main.py` pour qu'elle pointe vers votre base de données Access.

## Utilisation
Lancez l'application en exécutant :
```
python main.py
```

## Structure du projet
- `main.py` : Le script principal contenant toute la logique de l'application
- `agroapp.accdb` : La base de données Microsoft Access
- `requirements.txt` : Liste des dépendances Python

## Dépendances principales
- tkinter : pour l'interface graphique
- pyodbc : pour la connexion à la base de données
- matplotlib : pour la visualisation des données
- pandas : pour la manipulation des données

## Contribution
Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence
Ce projet est sous licence MIT.

## Contact
Pour toute question ou suggestion, veuillez contacter [maxolex12@gmail.com](mailto:maxolex12@gmail.com).
