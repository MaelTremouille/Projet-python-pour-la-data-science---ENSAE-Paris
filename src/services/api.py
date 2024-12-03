import requests
import json


class Api:
    def __init__(self):
        self.url = 'https://world.openfoodfacts.org/api/v0/product/'

    def recherche(self,barcode: str):
        barcode_url = self.url + barcode + '.json'
        print(f"L'url associée au barcode est : {barcode_url}")
        response = requests.get(barcode_url)
    
        if response.status_code == 200:
            data = response.json()
            product_data = data.get("product", {})
            nutriments_data = product_data.get("nutriments", {})
            categories_tags = product_data.get("categories_tags", [])

            # Sélection de la catégorie en français (ou anglais en fallback)
            selected_category = next((cat for cat in categories_tags if cat.startswith("fr:")), None)
            if not selected_category:
                selected_category = next((cat for cat in categories_tags if cat.startswith("en:")), "N/A")
            
            # Création du dictionnaire du produit
            produit = {
                "Nom": product_data.get("product_name", "N/A"),
                "Categorie": selected_category,  # Catégorie principale en français ou anglais
                "Nutriscore": product_data.get("nutrition_grades_tags", ["N/A"])[0],
                "Novascore": product_data.get("nova_groups_tags", ["N/A"])[0],
                "Ecoscore": product_data.get("ecoscore_score", "N/A"),
                "Taux de proteine": nutriments_data.get("proteins_100g", "N/A"),
                "Taux de sucre": nutriments_data.get("sugars_100g", "N/A"),
                "Energie (Kcal)": nutriments_data.get("energy-kcal_100g", "N/A"),
            }
            return produit
        else:
            print(f"Erreur lors de la récupération des données pour \
                  le code-barres {barcode} : {response.status_code}")