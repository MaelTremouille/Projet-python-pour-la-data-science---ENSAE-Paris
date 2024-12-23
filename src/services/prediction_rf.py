from sklearn.ensemble import RandomForestClassifier
from src.services.abstract_prediction import AbstractModelPrediction



class RandomForestPrediction(AbstractModelPrediction):
    def train_model(self, n_estimators=100, max_depth=None):
        """
        Entraîne un modèle de Random Forest avec les paramètres donnés.
        """
        self.model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        self.model.fit(self.X_train, self.y_train)

    def get_model_details(self):
        """
        Affiche les importances des caractéristiques pour le modèle Random Forest.
        """
        if not self.model:
            print("Veuillez d'abord entraîner le modèle avec train_model()")
            return
        cols = ['Ecoscore', 'Taux de sel (100g)', 'Taux de matieres grasses (100g)',
                'Taux de matieres grasses saturees (100g)', 'Taux de proteine (100g)',
                'Taux de sucre (100g)', 'Energie (Kcal) (100g)']
        for i in range(len(cols)):
            print(f"{cols[i]} : {round(self.model.feature_importances_[i]*100)} %")
