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
        plt.figure(figsize=(10, 6))
        ax = sns.boxplot(x=self.df['Categorie'], y=self.df[variable], palette="Set3")
        ax.set_title(f"Boxplot de {variable} par catégorie")
        return ax






