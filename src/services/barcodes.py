import json
from api import Api


class Barcodes:
    def __init__(self, filename='src/database/barcodes.json'):
        """Initialise l'objet avec le fichier où les codes-barres sont stockés."""
        self.filename = filename
        self.barcodes = self.charger_barcodes()
        self.api = Api()


    def __vider_database(self):
        pass
    
    def initialiser_database(self):
        if self.barcodes == dict():
            with open("services/init/initialisation.json", "r") as file:
                barcodes = json.load(file)
            for barcode in barcodes:
                self.ajouter_barcode(barcode)
        self.barcodes = self.charger_barcodes()

    def charger_barcodes(self):
        """Charge le fichier JSON et retourne un dictionnaire de barcodes."""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            with open(self.filename, 'w') as f:
                json.dump({}, f)
            return {}

    def ajouter_barcode(self, barcode):
        """Ajoute un nouveau barcode (clé) et sa valeur dans le fichier JSON."""
        produit = self.api.recherche(barcode)
        self.barcodes[barcode] = produit

        self.sauvegarder_barcodes()

    def sauvegarder_barcodes(self):
        """Sauvegarde les barcodes (le dictionnaire) dans le fichier JSON."""
        with open(self.filename, 'w') as f:
            json.dump(self.barcodes, f, indent=4)

    def rechercher_barcode(self, barcode):
        """Retourne la valeur associée à un barcode, ou None si il n'existe pas."""
        if self.barcodes.get(barcode, None) is None:
            self.ajouter_barcode(barcode)
        return self.barcodes.get(barcode, None)  
    
    def supprimer_barcode(self, barcode):
        pass
