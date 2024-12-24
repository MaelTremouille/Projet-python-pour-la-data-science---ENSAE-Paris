import requests
import time
import os

class Api:
    """
    A class to interact with a product API using barcode identifiers.
    Provides functionality to retrieve product information, including 
    nutrition and category data.

    Attributes:
        url (str): The base URL of the API, retrieved from environment variables.

    Methods:
        research(barcode: str):
            Fetches product details based on the given barcode and returns 
            a dictionary of product attributes.
    """
    def __init__(self):
        """
        Initializes the Api class by setting the base URL from the environment variable 'URL'.
        """
        self.url = os.getenv('URL')

    def research(self,barcode: str):
        """
        Fetches product information from the API based on the given barcode.

        Args:
            barcode (str): The barcode of the product to search for.

        Returns:
            dict: A dictionary containing product attributes, including:
                - "Nom" (str): Product name.
                - "Categorie" (str): Primary category in French or English.
                - "Nutriscore" (str): Nutrition grade.
                - "Novascore" (str): Nova group score.
                - "Ecoscore" (str): Ecoscore.
                - "Taux de sel (100g)" (float): Salt content per 100g.
                - "Taux de matieres grasses (100g)" (float): Fat content per 100g.
                - "Taux de matieres grasses saturees (100g)" (float): Saturated fat content per 100g.
                - "Taux de proteine (100g)" (float): Protein content per 100g.
                - "Taux de sucre (100g)" (float): Sugar content per 100g.
                - "Energie (Kcal) (100g)" (float): Energy in kilocalories per 100g.

        Raises:
            ValueError: If the API response status code is not 200 and data cannot be retrieved.
        """
        barcode_url = self.url + barcode + '.json'
        print(f"L'url associée au barcode est : {barcode_url}")
        response = requests.get(barcode_url)
    
        if response.status_code == 429:
            time.sleep(0.5)
            self.research(barcode)
            
        if response.status_code == 200:
            data = response.json()
            product_data = data.get("product", {})
            nutriments_data = product_data.get("nutriments", {})
            categories_tags = product_data.get("categories_tags", [])

            # Selecting the category in French (or falling back to English)
            selected_category = next((cat for cat in categories_tags if cat.startswith("fr:")), None)
            if not selected_category:
                selected_category = next((cat for cat in categories_tags if cat.startswith("en:")), "N/A")
            
            # Creation of the dictionary of products
            produit = {
                "Nom": product_data.get("product_name", "N/A"),
                "Categorie": selected_category, 
                "Nutriscore": product_data.get("nutrition_grades_tags", ["N/A"])[0],
                "Novascore": product_data.get("nova_groups_tags", ["N/A"])[0],
                "Ecoscore": product_data.get("ecoscore_score", "N/A"),
                "Taux de sel (100g)": nutriments_data.get("salt_100g", "N/A"),
                "Taux de matieres grasses (100g)": nutriments_data.get("fat_100g", "N/A"),
                "Taux de matieres grasses saturees (100g)": nutriments_data.get("saturated-fat_100g", "N/A"),
                "Taux de proteine (100g)": nutriments_data.get("proteins_100g", "N/A"),
                "Taux de sucre (100g)": nutriments_data.get("sugars_100g", "N/A"),
                "Energie (Kcal) (100g)": nutriments_data.get("energy-kcal_100g", "N/A"),
            }
            return produit
        else:
            print(f"Erreur lors de la récupération des données pour \
                  le code-barres {barcode} : {response.status_code}")