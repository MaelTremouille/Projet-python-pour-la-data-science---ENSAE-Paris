from sklearn.linear_model import LogisticRegression
from src.services.abstract_prediction import AbstractModelPrediction
import pandas as pd


class LogisticRegressionPrediction(AbstractModelPrediction):
    def train_model(self):
        """
        Entraîne un modèle de régression logistique.
        """
        self.model = LogisticRegression()
        self.model.fit(self.X_train, self.y_train)

    def get_model_details(self):
        """
        Affiche les coefficients du modèle de régression logistique.
        """
        if not self.model:
            print("Veuillez d'abord entraîner le modèle avec train_model()")
            return
        cols = ['Ecoscore', 'Taux de sel (100g)', 'Taux de matieres grasses (100g)',
                'Taux de matieres grasses saturees (100g)', 'Taux de proteine (100g)',
                'Taux de sucre (100g)', 'Energie (Kcal) (100g)']
        coefficients_df = pd.DataFrame(
            self.model.coef_,
            columns=cols,
            index= [self.encoding_dict[elt] for elt in self.model.classes_]   
        )
        return(coefficients_df)
        

    
