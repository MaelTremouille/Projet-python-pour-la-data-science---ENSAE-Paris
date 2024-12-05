import pandas as pd
from services.barcodes import Barcodes


class Statistiques:
    def __init__(self, filename='database/barcodes.json'):
        """Initialise l'objet avec le fichier où les codes-barres sont stockés."""
        
        self.df = self.create_df()

    def create_df(self):
        # On récupère le dictionnaire stocké
        data = Barcodes().barcodes
        # On crée un dataframe
        rows = []
        for key, value in data.items():
            if value is not None:
                row = {"Barcode": key, **value}
                rows.append(row)
        df = pd.DataFrame(rows)
        df.reset_index(drop=True, inplace=True)
        df.set_index("Barcode", inplace=True)
        return df
    
    def moy_par_cat(self):
        df_moy_par_cat = pd.DataFrame()
        df_moy_par_cat["Ecoscore"] = pd.to_numeric(self.df["Ecoscore"], errors="coerce")
        # Ajouter la colonne 'Categorie_clean' en extrayant la catégorie principale
        df_moy_par_cat["Categorie_clean"] = self.df["Categorie"].str.split(":").str[-1]
        # Calculer l'ecoscore moyen par catégorie
        ecoscore_moyen = df_moy_par_cat.groupby("Categorie_clean")["Ecoscore"].mean().dropna()
        return ecoscore_moyen


    def stats_basiques(self, var_name: str):
        variable = pd.to_numeric(self.df[var_name], errors="coerce")
        stats = {
            'moyenne': variable.mean(),
            'median': variable.median(),
            'std':variable.std(),
            'min':variable.min(),
            'max':variable.max(),
            'nb_manquantes':variable.isna().sum(),
        }

    def boxplot(self):
        """Faire un boxplot pour un type d'aliment"""

    
        


    





# # Charger les données depuis le fichier JSON
# data = pd.read_json("produits.json")


