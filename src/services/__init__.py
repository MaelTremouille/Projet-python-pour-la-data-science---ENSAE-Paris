import os
from dotenv import load_dotenv

# Charge le fichier .env depuis la racine du projet
dotenv_path = os.path.join(os.path.dirname(__file__))
load_dotenv(dotenv_path)

print("Fichier .env chargé avec succès.")