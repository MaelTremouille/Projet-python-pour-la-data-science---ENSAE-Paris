import json

class Barcodes:
    def __init__(self, filename):
        """Initialise l'objet avec le fichier où les codes-barres sont stockés."""
        self.filename = filename
        self.barcodes = self.charger_barcodes()

    def charger_barcodes(self):
        """Charge le fichier JSON et retourne un dictionnaire de barcodes."""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)  # Retourne le contenu du fichier sous forme de dictionnaire
        except FileNotFoundError:
            # Si le fichier n'existe pas, le créer avec un dictionnaire vide
            with open(self.filename, 'w') as f:
                json.dump({}, f)  # Sauvegarde un dictionnaire vide
            return {}  # Retourne un dictionnaire vide

    def ajouter_barcode(self, barcode, valeur):
        """Ajoute un nouveau barcode (clé) et sa valeur dans le fichier JSON."""
        # Ajoute ou met à jour la valeur du barcode dans le dictionnaire
        self.barcodes[barcode] = valeur
        self.sauvegarder_barcodes()  # Sauvegarde après ajout

    def sauvegarder_barcodes(self):
        """Sauvegarde les barcodes (le dictionnaire) dans le fichier JSON."""
        with open(self.filename, 'w') as f:
            json.dump(self.barcodes, f, indent=4)  # Sauvegarde avec indentation

    def rechercher_barcode(self, barcode):
        """Retourne la valeur associée à un barcode, ou None si il n'existe pas."""
        return self.barcodes.get(barcode, None)  # Retourne None si le barcode n'existe pas
