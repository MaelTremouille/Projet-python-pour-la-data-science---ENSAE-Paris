import json
import pandas as pd
from src.services.barcodes import Barcodes


class Traitement(Barcodes):
    def __init__(self):
        super().__init__()
        with open('src/services/init/category_map.json', 'r', encoding='utf-8') as fichier:
            self.category_map = json.load(fichier)
        self.__appliquer_transformation_categories()
        self.__convert_types()

    def __convert_types(self):
        """
        Convertit certaines colonnes en types numériques si elles existent dans le DataFrame.
        """
        numeric_columns =[
            'Taux de sel (100g)', 'Taux de matieres grasses (100g)',
            'Taux de matieres grasses saturees (100g)',
            'Taux de proteine (100g)', 'Taux de sucre (100g)',
            'Energie (Kcal) (100g)', 'Ecoscore'
            ]
        str_colums = [
            'Nom', 'Nutriscore','Categorie_clean'
        ]
        for col in numeric_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce")
                


    def __appliquer_transformation_categories(self):
        """
        Crée une nouvelle colonne 'Categorie_clean' en fonction de la colonne 'Categorie'
        et du dictionnaire self.category_map.
        """
        if "Categorie" in self.df.columns:
            self.df["Categorie_clean"] = (
                self.df["Categorie"]
                .str.split(":")
                .str[-1]
                .map(self.category_map)
            )
            self.df.drop(columns=["Categorie", "Novascore"], inplace=True)
        else:
            raise KeyError("La colonne 'Categorie' est manquante dans les données.")
        
    def get_categorie_clean_value(self):
        set_clean_values = set()
        indeces = self.df.index.to_list()
        for idx in indeces:
            set_clean_values.add(self.category_map[idx])
        return(list(set_clean_values))




