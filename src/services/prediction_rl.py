from sklearn.linear_model import LogisticRegression
from src.services.abstract_prediction import AbstractModelPrediction
import pandas as pd


class LogisticRegressionPrediction(AbstractModelPrediction):
    """
    This class extends the AbstractModelPrediction class and implements the specific methods 
    for training a Logistic Regression model and retrieving its details.

    It uses the LogisticRegression from scikit-learn to perform classification tasks.
    """
    def train_model(self):
        """
        Trains a Logistic Regression model with the given parameters.
        """
        self.model = LogisticRegression()
        self.model.fit(self.X_train, self.y_train)

    def get_model_details(self):
        """
        Displays the feature importances for the trained Logistic Regression model.

        If the model is not trained yet, it prompts the user to train the model first using train_model().

        Returns:
        None
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
        

    
