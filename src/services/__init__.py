import os
from dotenv import load_dotenv

# Load the .env file from the root of the project
dotenv_path = os.path.join(os.path.dirname(__file__))
load_dotenv(dotenv_path)

print("Fichier .env chargé avec succès.")