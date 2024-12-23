import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.services.traitement import Traitement


class Statistiques:
    def __init__(self):
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
        numeric_columns =[
            'Taux de sel (100g)', 'Taux de matieres grasses (100g)',
            'Taux de matieres grasses saturees (100g)',
            'Taux de proteine (100g)', 'Taux de sucre (100g)',
            'Energie (Kcal) (100g)', 
            'Ecoscore'
            ]
        cov_matrix = self.df[numeric_columns].cov()
        plt.figure(figsize=(10, 8))

        # Définir les limites de la matrice pour centrer la palette sur 0
        vmin = cov_matrix.min().min()
        vmax = cov_matrix.max().max()
        abs_max = max(abs(vmin), abs(vmax)) 

        sns.heatmap(
            cov_matrix,
            annot=True,
            fmt=".2f",
            cmap=sns.color_palette(["#ADD8E6", "#FFB6C1"], as_cmap=True),
            vmin=-abs_max,  # Minimum symétrique négatif
            vmax=abs_max,   # Maximum symétrique positif
            square=True
        )

        plt.title("Matrice de covariance", fontsize=16)
        plt.xticks(rotation=45, ha="right", fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        plt.show()
        return cov_matrix
    
    def corr_matrix(self):
        numeric_columns = [
            'Taux de sel (100g)', 'Taux de matieres grasses (100g)',
            'Taux de matieres grasses saturees (100g)',
            'Taux de proteine (100g)', 'Taux de sucre (100g)',
            'Energie (Kcal) (100g)', 
            'Ecoscore'
        ]

        # Calcul de la matrice de corrélation
        corr_matrix = self.df[numeric_columns].corr()

        # Affichage de la matrice de corrélation avec un heatmap
        plt.figure(figsize=(10, 8))

        # Définir les limites de la matrice pour centrer la palette sur 0
        vmin = corr_matrix.min().min()
        vmax = corr_matrix.max().max()
        abs_max = max(abs(vmin), abs(vmax))

        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-abs_max, vmax=abs_max, center=0)

        # Affichage du titre
        plt.title('Matrice de Corrélation')
        plt.show()

    def boxplot_categorie(self, variable: str, few_obs: int = None):
        if few_obs is not None:
            filtered_df = pd.DataFrame(columns=self.df.columns)
            category_counts = self.df['Categorie_clean'].value_counts()

            categories_to_keep = category_counts[category_counts >= few_obs].index

            filtered_df = self.df[self.df['Categorie_clean'].isin(categories_to_keep)]
        else:
            filtered_df = self.df

        filtered_df = filtered_df.dropna(subset=[variable, 'Categorie_clean'])
        
        plt.figure(figsize=(12, 8)) 
        ax = sns.boxplot(x=filtered_df['Categorie_clean'], y=filtered_df[variable], palette="Set3")
        
        ax.set_title(f"Boxplot de {variable} par catégorie", fontsize=16) 
        ax.set_xlabel("Catégorie", fontsize=12)  
        ax.set_ylabel(variable, fontsize=12)  
        ax.tick_params(axis='x', rotation=45) 
        plt.tight_layout()
        plt.show() 


    def moy_par_categorie(self, variable : str = 'Ecoscore'):
        moyennes = self.df.groupby("Categorie_clean")[variable].mean().dropna()
        # Creer le graphe
        plt.figure(figsize=(10, 6))
        moyennes.sort_values().plot(kind="barh", color="skyblue", edgecolor="black")
        plt.title(f"{variable} moyen par categorie", fontsize=16)
        plt.xlabel(f"{variable} moyen", fontsize=14)
        plt.ylabel("Categories", fontsize=14)
        plt.grid(axis="x", linestyle="--", alpha=0.7)
        plt.tight_layout()

        # Afficher le graphique
        plt.show()


    

    







