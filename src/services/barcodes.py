import json
from src.services.api import Api
import pandas as pd


class Barcodes:
    def __init__(self, filename='src/database/barcodes.json'):
        """Initialise l'objet avec le fichier où les codes-barres sont stockés."""
        self.filename = filename
        self.api = Api()
        self.df = self.get_df()

    
    def __create_new_df(self, path: str = 'src/database/dataframe.csv'):
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
        df.to_csv(path, index=False)
        return df
    
    def dict_database_init(self):
        barcodes_dict = dict()

        with open("src/services/init/initialisation.json", "r") as file:
            barcodes = json.load(file)

        for barcode in barcodes:
            produit = self.api.recherche(barcode)
            barcodes_dict[barcode] = produit
        return barcodes_dict

    def get_df(self, path: str = 'src/database/dataframe.csv'):
        try:
            with open(path, 'r') as f:
                df = pd.read_csv('src/database/dataframe.csv')
                return df
        except FileNotFoundError:
            df = self.__create_new_df(path)
            return df
        
    def __add_produit(self, barcode):
        produit = self.api.recherche(barcode)
        self.df.loc[barcode] = produit
        pass
    def get_produit(self, barcode:str):
        """Retourne la valeur associée à un barcode, ou None si il n'existe pas."""
        if barcode not in self.df.index:
            self.__add_produit(barcode)
            print(f"Ce produit associé au code barre {barcode} \
                  vient d'être ajouté à la BDD")
        return self.df.loc[barcode]
    
    def delete_produit(self, barcode: str):
        pass
    def __vider_database(self):
        pass