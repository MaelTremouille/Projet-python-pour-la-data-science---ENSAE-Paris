import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from barcodes import Barcodes

class Statistiques:
    def __init__(self, filename='database/barcodes.json'):
        self.df = self.__create_df()
        self.__convert_types()

    def __create_df(self):
        data = Barcodes().barcodes
        rows = []
        for key, value in data.items():
            if value is not None:
                row = {"Barcode": key, **value}
                rows.append(row)
        df = pd.DataFrame(rows)
        df.reset_index(drop=True, inplace=True)
        df.set_index("Barcode", inplace=True)
        return df

    def __convert_types(self):
        self.df["Ecoscore"] = pd.to_numeric(self.df["Ecoscore"], errors="coerce")
        self.df["Taux de proteine"] = pd.to_numeric(self.df["Taux de proteine"], errors="coerce")
        self.df["Taux de sucre"] = pd.to_numeric(self.df["Taux de sucre"], errors="coerce")
        self.df["Energie (Kcal)"] = pd.to_numeric(self.df["Energie (Kcal)"], errors="coerce")

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





