import json
from src.services.api import Api
import pandas as pd
import os


class Barcodes:
    def __init__(self, path='src/database/dataframe.csv'):
        """Initialise l'objet avec le fichier où les codes-barres sont stockés."""
        self.path = os.getenv('DATABASE_PATH')
        self.api = Api()
        self.df = self.get_df()
        self.initialisation_path = os.getenv('INITIALISATION_PATH')

    
    def __create_new_df(self):
        """
        Charge les données depuis un fichier JSON.

        Returns: 
            df (pd.DataFrame) contenant les données.
        """
        self.barcodes_dict = self.dict_database_init()
        rows = []
        for key, value in self.barcodes_dict.items():
            if value is not None:
                row = {"Barcode": key, **value}
                rows.append(row)
        df = pd.DataFrame(rows)
        df.reset_index(drop=True, inplace=True)
        df.set_index("Barcode", inplace=True)
        df.to_csv(self.path, index=True)
        return df
    
    def dict_database_init(self):
        barcodes_dict = dict()

        with open(self.initialisation_path, "r") as file:
            barcodes = json.load(file)
        for barcode in barcodes:
            produit = self.api.recherche(barcode)
            barcodes_dict[barcode] = produit
        return barcodes_dict

    def get_df(self):
        try:
            with open(self.path, 'r') as f:
                df = pd.read_csv(self.path, index_col=0)
                if df.empty:
                    df = self.__create_new_df()
        except FileNotFoundError:
            df = self.__create_new_df()
        return df
        
    def __add_produit(self, barcode):
        produit = self.api.recherche(barcode)
        self.df.loc[barcode] = produit
        self.df.to_csv(self.path, index=True)

    def get_produit(self, barcode:str):
        """Retourne la valeur associée à un barcode, ou None si il n'existe pas."""
        if barcode not in self.df.index:
            self.__add_produit(barcode)
            print(f"Ce produit associé au code barre {barcode} \
                  vient d'être ajouté à la BDD")
        return self.df.loc[barcode]
    
    def delete_produit(self, barcode: str):
        if barcode in self.df.index:
            self.df.drop(barcode, inplace=True)
        print(f"Suppression de {barcode} confirmée.")

    def vider_database(self):
        self.df = pd.DataFrame()
        self.df.to_csv(self.path, index=True)
