import json
import pandas as pd
from src.services.barcodes import Barcodes


class Processing(Barcodes):
    def __init__(self):
        # Load category map from a JSON file to use for category transformations
        super().__init__()
        with open('src/services/init/category_map.json', 'r', encoding='utf-8') as fichier:
            self.category_map = json.load(fichier)
        self.__apply_category_transformation()
        self.__convert_types()

    def __convert_types(self):
        """
        Converts certain columns to numeric types if they exist in the DataFrame.
        
        Specifically, this method will attempt to convert columns that represent various nutritional values 
        (e.g., salt, fat, sugar content) and an Eco-score to numeric values. If conversion fails, it coerces errors.
        """
        numeric_columns =[
            'Taux de sel (100g)', 'Taux de matieres grasses (100g)',
            'Taux de matieres grasses saturees (100g)',
            'Taux de proteine (100g)', 'Taux de sucre (100g)',
            'Energie (Kcal) (100g)', 'Ecoscore'
            ]
        for col in numeric_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce")
                


    def __apply_category_transformation(self):
        """
        Creates a new 'Categorie_clean' column based on the 'Categorie' column
        and the self.category_map dictionary.
        
        This transformation splits the 'Category' column and maps the category part to a cleaned version
        using the category_map dictionary. It drops the old 'Category' and 'Novascore' columns.
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
        """
        Retrieves a list of unique cleaned category values from the 'category_map'.
        
        Iterates through the DataFrame's index to extract the mapped cleaned category values
        and returns them as a list.
        """
        set_clean_values = set()
        indeces = self.df.index.to_list()
        for idx in indeces:
            set_clean_values.add(self.category_map[idx])
        return(list(set_clean_values))