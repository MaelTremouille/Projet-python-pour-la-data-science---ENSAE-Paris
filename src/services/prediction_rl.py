from sklearn.linear_model import LogisticRegression
from src.services.prediction import ModelPrediction


class LogisticRegressionPrediction(ModelPrediction):
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
        print("Coefficients :\n", self.model.coef_)
        print("Variables associées :\n", self.X.columns)
