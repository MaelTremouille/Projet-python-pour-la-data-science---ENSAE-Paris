import json
import pandas as pd
from src.services.barcodes import Barcodes


class Traitement:
    """
    Classe Traitement pour charger et transformer les données des produits à partir d'un fichier JSON.
    Elle applique des transformations sur les données, comme la conversion des types de certaines colonnes
    et l'ajout d'une colonne 'Categorie_clean' basée sur un mappage défini.
    
    Attributs :
        filename (str) : Le chemin vers le fichier JSON contenant les données des produits.
        df (pd.DataFrame) : Le DataFrame contenant les données transformées des produits.
        category_map (dict) : Un dictionnaire mappant les catégories des produits en catégories plus lisibles.
    """
    def __init__(self, filename: str='src/database/barcodes.json'):
        """
        Initialise la classe en chargeant les données depuis un fichier JSON.
        """
        self.filename = filename
        self.df = self.__create_df()
        self.category_map = {
            "dairies": "Produits laitiers",
            "fromages-du-nord-pas-de-calais": "Produits laitiers",
            "beurre-a-tartiner": "Produits laitiers",
            "plant-based-foods-and-beverages": "Aliments vegetaux",
            "meals": "Repas et plats prepares",
            "flocons-d-avoine-complete": "Repas et plats prepares",
            "cereales-preparees": "Repas et plats prepares",
            "beverages-and-beverages-preparations": "Boissons",
            "beverages": "Boissons",
            "snacks": "Snacks et sucreries",
            "chocolats-noirs-au-quinoa": "Snacks et sucreries",
            "lunettes-a-la-fraise": "Snacks et sucreries",
            "meats-and-their-products": "Viandes et produits carnes",
            "charcuteries-cuites": "Viandes et produits carnes",
            "rosette-tranchee": "Viandes et produits carnes",
            "canned-foods": "Conserves",
            "saguaro-water-juice-fraise": "Boissons",
            "sirops-de-verveine": "Boissons",
            "terrines-de-foie-de-volaille": "Viandes et produits carnes",
            "terrines-de-chevreuil": "Viandes et produits carnes",
            "rillettes-de-viande-rouge": "Viandes et produits carnes",
            "betteraves-sous-vide": "Legumes et feculents",
            "confitures-de-cedrats": "Confiserie et produits sucres",
            "choucroute-crue": "Legumes et feculents",
            "100-legumes": "Legumes et feculents",
            "biscuits-edulcores": "Confiserie et produits sucres",
            "breakfasts": "Repas et plats prepares",
            "pates-de-figues": "Confiserie et produits sucres",
            "condiments": "Sauces et epices",
            "sauce-pate": "Sauces et epices",
            "sauces-pour-feculents": "Sauces et epices",
            "sauces-crudites": "Sauces et epices",
            "desserts": "Confiserie et produits sucres",
            "seafood": "Poissons et fruits de mer",
            "chips-and-fries": "Snacks et sucreries",
            "the-vert-glace": "Boissons",
            "cocoa-and-its-products": "Aliments vegetaux",
            "sandwiches": "Repas et plats prepares",
            "thons-albacore-au-naturel": "Poissons et fruits de mer",
            "pates-a-tartiner": "Confiserie et produits sucres",
            "hauts-de-cuisse-de-poulet-rotis": "Viandes et produits carnes",
            "aiguillettes-de-poulet": "Viandes et produits carnes",
            "canned-foods": "Conserves",
            "poulets-fermiers": "Viandes et produits carnes",
            "parmentiers-de-poulet": "Repas et plats prepares",
            "miels-du-gatinais": "Produits sucres",
            "miels-de-nigelle": "Produits sucres",
            "pains-de-tradition-francaise": "Produits cerealiers",
            "aliments-d-origine-vegetale": "Aliments vegetaux",
            "gateaux-nantais": "Confiserie et produits sucres",
            "gateaux-basques": "Confiserie et produits sucres",
            "madeleines-ker-cadelac": "Confiserie et produits sucres",
            "madeleines-vracs": "Confiserie et produits sucres",
            "huile-d-olive-de-provence": "Huiles et graisses"
        }
        self.__appliquer_transformation_categories()
        self.__convert_types()

    
    def __create_df(self):
        """
        Charge les données depuis un fichier JSON.

        Returns: 
            df (pd.DataFrame) contenant les données.
        """
        data = Barcodes().barcodes
        rows = []
        for key, value in data.items():
            if value is not None:
                row = {"Barcode": key, **value}
                rows.append(row)
        df = pd.DataFrame(rows)
        df.reset_index(drop=True, inplace=True)
        df.set_index("Barcode", inplace=True)
        return df

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




