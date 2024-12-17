from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from src.services.traitement import Traitement


class ModelPrediction(ABC):
    def __init__(self):
        self.df = Traitement().df
        if self.df.empty:
            raise ValueError("Le DataFrame chargé depuis Traitement est vide.")
        self.X, self.y = self.create_pred_df()
        self.X_train, self.X_test, self.y_train, self.y_test = self.create_train_test_df()
        self.model = None

    def create_pred_df(self):
        required_cols = ['Ecoscore', 'Taux de sel (100g)', 'Taux de matieres grasses (100g)',
                         'Taux de matieres grasses saturees (100g)', 'Taux de proteine (100g)',
                         'Taux de sucre (100g)', 'Energie (Kcal) (100g)', 'Nutriscore']
        missing_cols = set(required_cols) - set(self.df.columns)
        if missing_cols:
            raise ValueError(f"Colonnes manquantes dans le DataFrame : {missing_cols}")

        df_modele = self.df[required_cols]
        df_modele.ffill(inplace=True)
        self.label_encoder = LabelEncoder()
        df_modele['Nutriscore'] = self.label_encoder.fit_transform(df_modele['Nutriscore'])
        X = df_modele.drop(columns='Nutriscore')
        y = df_modele['Nutriscore']
        # Récupération du dictionnaire d'encodage
        interm_dict = {label: index for index, label in enumerate(self.label_encoder.classes_)}
        self.encoding_dict = {value: key for key, value in interm_dict.items()}
        return X, y

    def create_train_test_df(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42, stratify=self.y)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        return X_train, X_test, y_train, y_test

    @abstractmethod
    def train_model(self):
        """
        Méthode abstraite pour entraîner un modèle.
        Cette méthode doit être implémentée dans les classes filles.
        """
        pass

    def evaluate_performance(self):
        """
        Affiche les performances du modèle (matrice de confusion, rapport de classification, précision).
        """
        if not self.model:
            print("Veuillez d'abord entraîner le modèle avec train_model()")
            return
        y_pred = self.model.predict(self.X_test)
        print("Matrice de confusion :\n", confusion_matrix(self.y_test, y_pred))
        print('-' * 60)
        print('Rapport de classification')
        print(classification_report(self.y_test, y_pred, zero_division=0))
        print('-' * 60)
        print(f"Précision : {accuracy_score(self.y_test, y_pred) * 100:.2f}%")

    @abstractmethod
    def get_model_details(self):
        """
        Méthode abstraite pour obtenir les détails du modèle (par exemple, coefficients ou importances des caractéristiques).
        Cette méthode doit être implémentée dans les classes filles.
        """
        pass
    
    def predict_nutriscore(self, new_data):
        """
        Prédit le Nutriscore pour une ou plusieurs lignes de données.

        new_data : DataFrame
            Le DataFrame contenant les valeurs pour lesquelles on veut prédire le Nutriscore.
        
        return : Array
            Un tableau contenant les prédictions de Nutriscore.
        """
        if not self.model:
            print("Veuillez d'abord entraîner le modèle avec train_model()")
            return

        # Appliquer la même transformation aux nouvelles données
        scaler = StandardScaler()
        new_data_scaled = scaler.fit_transform(new_data)

        # Faire les prédictions
        predictions = self.model.predict(new_data_scaled)
        true_pred = self.encoding_dict[predictions[0]]
        
        return true_pred
