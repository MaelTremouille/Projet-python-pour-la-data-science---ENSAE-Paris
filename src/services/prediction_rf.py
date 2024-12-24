from sklearn.ensemble import RandomForestClassifier
from src.services.abstract_prediction import AbstractModelPrediction



class RandomForestPrediction(AbstractModelPrediction):
    """
    This class extends the AbstractModelPrediction class and implements the specific methods 
    for training a Random Forest model and retrieving its details.

    It uses the RandomForestClassifier from scikit-learn to perform classification tasks.
    """
    def train_model(self, n_estimators=100, max_depth=None):
        """
        Trains a Random Forest model with the given parameters.

        Parameters:
        n_estimators (int): The number of trees in the forest. Default is 100.
        max_depth (int or None): The maximum depth of the trees. Default is None, meaning nodes are expanded until all leaves are pure.

        Returns:
        None
        """
        self.model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        self.model.fit(self.X_train, self.y_train)

    def get_model_details(self):
        """
        Displays the feature importances for the trained Random Forest model.

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
        for i in range(len(cols)):
            print(f"{cols[i]} : {round(self.model.feature_importances_[i]*100)} %")
