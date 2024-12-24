import json
from src.services.api import Api
import pandas as pd
import os


class Barcodes:
    """
    A class for managing a product database using barcodes.
    Allows for adding, retrieving, and deleting products from a CSV database,
    and interacts with an external API to fetch product details based on barcode.

    Attributes:
        path (str): The path to the CSV file storing the barcode database.
        api (Api): An instance of the Api class to interact with the external API.
        df (pd.DataFrame): The DataFrame holding the product database.
        initialisation_path (str): The path to the initialization JSON file containing barcode data.

    Methods:
        __create_new_df():
            Loads product data from a JSON file and creates a new DataFrame.
        
        dict_database_init():
            Initializes the database by querying the API for product details based on barcodes.
        
        get_df():
            Loads the DataFrame from the CSV file, or creates a new one if the file doesn't exist.
        
        __add_product(barcode: str):
            Adds a new product to the database using the barcode.
        
        get_product(barcode: str):
            Retrieves a product by its barcode from the database. Adds it if not present.
        
        delete_product(barcode: str):
            Deletes a product from the database using its barcode.
        
        clear_database():
            Clears all data in the database and resets the DataFrame.
    """
    def __init__(self):
        """
        Initializes the Barcodes object with the path to the barcode database file.
        """
        self.path = os.getenv('DATABASE_PATH')
        self.api = Api()
        self.df = self.get_df()
        self.initialisation_path = os.getenv('INITIALISATION_PATH')

    
    def __create_new_df(self):
        """
        Loads data from a JSON file and creates a new DataFrame.
        
        Returns:
            pd.DataFrame: A DataFrame containing the product data.
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
        """
        Initializes the database by querying the API for product details based on barcodes.
        
        Returns:
            dict: A dictionary mapping barcodes to product data.
        """
        barcodes_dict = dict()

        with open(self.initialisation_path, "r") as file:
            barcodes = json.load(file)
        for barcode in barcodes:
            product = self.api.research(barcode)
            barcodes_dict[barcode] = product
        return barcodes_dict

    def get_df(self):
        """
        Loads the DataFrame from the CSV file or creates a new one if the file doesn't exist.
        
        Returns:
            pd.DataFrame: The DataFrame containing product data.
        """
        try:
            with open(self.path, 'r') as f:
                df = pd.read_csv(self.path, index_col=0)
                if df.empty:
                    df = self.__create_new_df()
        except FileNotFoundError:
            df = self.__create_new_df()
        return df
        
    def __add_product(self, barcode):
        """
        Adds a new product to the database using the provided barcode.
        
        Args:
            barcode (str): The barcode of the product to add.
        """
        product = self.api.research(barcode)
        self.df.loc[barcode] = product
        self.df.to_csv(self.path, index=True)

    def get_product(self, barcode:str):
        """
        Retrieves a product from the database using its barcode. If not present, adds it.
        
        Args:
            barcode (str): The barcode of the product to retrieve.
        
        Returns:
            pd.Series: The product data corresponding to the barcode.
        """
        if barcode not in self.df.index:
            self.__add_product(barcode)
            print(f"Ce produit associé au code barre {barcode} \
                  vient d'être ajouté à la BDD")
        return self.df.loc[barcode]
    
    def delete_product(self, barcode: str):
        """
        Deletes a product from the database using its barcode.
        
        Args:
            barcode (str): The barcode of the product to delete.
        """
        if barcode in self.df.index:
            self.df.drop(barcode, inplace=True)
        print(f"Suppression de {barcode} confirmée.")

    def clear_database(self):
        """
        Clears all data in the database and resets the DataFrame.
        """
        self.df = pd.DataFrame()
        self.df.to_csv(self.path, index=True)
