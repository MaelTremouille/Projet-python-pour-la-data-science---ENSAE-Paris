import matplotlib.pyplot as plt
import seaborn as sns
from stats import Statistiques

class PlotManager(Statistiques):
    def __init__(self):
        super().__init__()

    def plot_boxplot(self, ax):
        sns.boxplot(x=self.df['Categorie'], y=self.df['Energie (Kcal)'], palette="Set3", ax=ax)
        ax.set_title("Boxplot 1: Énergie par Catégorie")
        ax.set_xlabel("Catégorie")
        ax.set_ylabel("Énergie (Kcal)")
        ax.grid(axis="y", linestyle="--", alpha=0.7)

    def plot_boxplot_categorie(self, variable: str):
        

# Dans ton main.py
import pandas as pd
from plot_manager import PlotManager

if __name__ == "__main__":
    # Chargement des données (exemple simplifié)
    df = pd.DataFrame({
        "Categorie": ["Dairy", "Meat", "Dairy", "Vegetables", "Meat"],
        "Nutriscore": ["A", "B", "A", "C", "B"],
        "Energie (Kcal)": [120, 250, 150, 80, 200]
    })

    # Création d'une instance de PlotManager
    plotter = PlotManager(df)

    # Créer une figure avec des sous-graphes (2 lignes, 2 colonnes)
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))  # 1 ligne, 2 colonnes

    # Générer les graphiques sur les axes spécifiés
    plotter.plot_boxplot1(axs[0])  # Premier plot sur le premier sous-graphe
    plotter.plot_boxplot2(axs[1])  # Deuxième plot sur le deuxième sous-graphe

    # Ajuster les marges et l'affichage
    plt.tight_layout()  # Pour éviter que les labels se chevauchent
    plt.show()
