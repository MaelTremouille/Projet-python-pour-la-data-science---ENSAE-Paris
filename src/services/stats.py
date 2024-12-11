import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.services.traitement import Traitement


class Statistiques:
    def __init__(self, filename='database/barcodes.json'):
        self.df = Traitement().df

    def stats_univariees(self, var_name: str):
        variable = self.df[var_name]
        stats = {
            'moyenne': variable.mean(),
            'median': variable.median(),
            'std': variable.std(),
            'min': variable.min(),
            'max': variable.max(),
            'nb_manquantes': variable.isna().sum(),
        }
        return stats

    def stats_covariances(self):
        cov_matrix = self.df[["Taux de proteine", "Taux de sucre", "Energie (Kcal)"]].cov()
        return cov_matrix

    def boxplot_categorie(self, variable: str):
        plt.figure(figsize=(12, 8))  # Taille plus grande pour plus de lisibilité
        ax = sns.boxplot(x=self.df['Categorie_clean'], y=self.df[variable], palette="Set3")
        ax.set_title(f"Boxplot de {variable} par catégorie", fontsize=16)  # Taille du titre
        ax.set_xlabel("Catégorie", fontsize=12)  # Taille du label x
        ax.set_ylabel(variable, fontsize=12)  # Taille du label y
        ax.tick_params(axis='x', rotation=45)  # Rotation des labels de l'axe x
        plt.tight_layout()  # Ajustement des marges pour éviter le chevauchement
        return ax






