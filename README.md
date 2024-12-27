# Projet Python pour la Data Science – ENSAE Paris : Analyse OpenFoodFacts

Ce projet propose une exploration approfondie de données issues d’Open Food Facts, suivie d’analyses statistiques et de la mise en œuvre de modèles prédictifs (régression logistique et forêts aléatoires) pour estimer le Nutriscore de produits alimentaires à partir de leurs caractéristiques nutritionnelles.

---
## 0. Instructions d’Utilisation 

**Installation et Pré-requis**  
   - Python 3.9+ (possibilité que cela fonctionne avec des versions antérieures)  
   - Bibliothèques : `pandas`, `numpy`, `requests`, `scikit-learn`, `matplotlib`, `seaborn`,`python-dotenv`.  
   - Cloner le dépôt :
```bash
git clone https://github.com/MaelTremouille/Projet-python-pour-la-data-science---ENSAE-Paris.git
```
   - Installer les packages requis :
```bash
pip install -r requirements.txt
pip list
```
Disclaimer : il est possible d'avoir un problème en lien avec `dotenv` :
```bash
pip install python-dotenv
```




---

## 1. Contexte et Objectifs

### Contexte
Open Food Facts est une base de données collaborative qui recense des milliers de produits alimentaires, avec des informations sur leur composition (taux de sel, sucre, matières grasses, etc.), leur origine, leurs labels (Nutriscore, Novascore, Ecoscore), et bien plus encore. Aujourd’hui, les consommateurs se préoccupent de plus en plus de la qualité nutritionnelle et de l’impact environnemental de leur alimentation. Ce projet vise à :

- **Mieux comprendre** la répartition des nutriments dans les produits,  
- **Analyser** les liens entre les indicateurs (Nutriscore, Ecoscore, Catégories d’aliments, etc.),  
- **Construire** un modèle prédictif permettant d’anticiper le Nutriscore d’un produit à partir de ses caractéristiques nutritionnelles.

### Problématique
La question directrice retenue est :  
> *« Peut-on prédire le Nutriscore d’un produit alimentaire en s’appuyant sur ses informations nutritionnelles (taux de sel, sucre, gras, protéines, etc.) et ainsi mieux comprendre les facteurs qui influencent cette note ? »*

---

## 2. Architecture du Projet

1. **Chargement et préparation des données**  
   - Les données sont initialisées à partir d’un fichier JSON contenant des listes de codes-barres, puis enrichies via l’API d’Open Food Facts.  
   - On utilise la classe `Barcodes` pour gérer la base de données des produits (lecture, ajout, suppression, mise à jour dynamique).  
   - Un traitement supplémentaire (`Traitement`) permet de nettoyer les données, de créer de nouvelles variables (ex. `Categorie_clean`), et de s’assurer que le DataFrame final est cohérent (typage des colonnes, gestion des valeurs manquantes, etc.).

2. **Exploration et Statistiques Descriptives**  
   - Répartition des produits selon différentes variables :  
     - **Nutriscore** (a, b, c, d, e, ou inconnu / non applicable),  
     - **Ecoscore**,  
     - **Taux de sel / sucre / matières grasses / protéines**, etc.  
   - Calcul des statistiques univariées (moyennes, médianes, écarts-types) et inspection des distributions (histogrammes, boxplots).  
   - Analyse multivariée (matrice de corrélation) pour détecter les corrélations fortes (par exemple, entre matières grasses et énergie).  

3. **Mise à jour dynamique de la BDD**  
   - Possibilité de rechercher un produit via son code-barres et, s’il est inconnu, de l’ajouter après requête à l’API Open Food Facts.  
   - Suppression sélective de produits, mise à jour, et même réinitialisation complète de la base (si nécessaire).  

4. **Modèles Prédictifs**  
   - **Régression Logistique** : un premier modèle supervisé, relativement simple à interpréter, qui essaye de prédire la classe Nutriscore à partir des variables (sel, sucre, matières grasses, etc.).  
   - **Forêts Aléatoires (Random Forest)** : un second modèle plus robuste et capable de capturer des relations non linéaires.  

5. **Évaluation des performances**  
   - Affichage de la **matrice de confusion** pour visualiser les classes réelles vs. les classes prédites, et repérer les confusions les plus fréquentes.  
   - Calcul d’indicateurs classiques : **accuracy** (précision globale), **rappel** (recall), **précision** (precision), **score F1**, etc.  
   - Comparaison des performances de la régression logistique et de la Random Forest.  

---

## 3. Résultats Principaux

### Statistiques Descriptives
- **Répartition Nutriscore** : On observe une majorité de produits en “d”, puis “c” et “a”. Les classes “b” et “e” sont généralement moins représentées, et de nombreux produits peuvent être *unknown* ou *not-applicable*.  
- **Lien entre les catégories et le Nutriscore** : Les catégories plus riches en sel, sucre ou matières grasses (ex. “Snacks et sucreries”, “Viandes et produits carnés”) s’orientent souvent vers de moins bonnes notes (Nutriscore “d” ou “e”).  
- **Corrélations notables** :  
  - Forte corrélation entre les matières grasses et l’énergie (les lipides contribuant fortement aux calories),  
  - Faible corrélation directe entre Ecoscore et les nutriments, suggérant que la dimension environnementale dépasse la seule composition nutritionnelle.

### Modèle 1 : Régression Logistique
- **Précision** autour de **57 %** 
- Meilleure reconnaissance pour les classes “d” (majoritaire) et “a”, plus difficile pour “b” et “e” sous-représentées.  
- Les matrices de confusion montrent des confusions fréquentes entre les classes intermédiaires.

### Modèle 2 : Forêts Aléatoires (Random Forest)
- **Précision** de l’ordre de **70–75 %** sur 5 classes Nutriscore, sensiblement meilleure que la régression logistique.  
- Classe “d” la mieux reconnue (parfois plus de 90 % de rappel), classe “b” la plus délicate (faible effectif, profil intermédiaire).  
- La Random Forest gère mieux la diversité des profils nutritionnels grâce à sa capacité à modéliser des interactions non linéaires.

---

## 4. Conclusions et Perspectives

1. **Utilité de la Base Open Food Facts**  
   Ce projet démontre l’intérêt de données ouvertes et collaboratives pour mieux comprendre les tendances alimentaires, en particulier l’impact du sel, du sucre et des matières grasses sur la note nutritionnelle (Nutriscore).

2. **Performances de la Prédiction**  
   - Un **taux de précision** de ~70 %+ sur un problème à 5 classes illustre la possibilité d’anticiper la qualité nutritionnelle d’un produit à partir de données partielles.  
   - Il reste toutefois des axes d’amélioration, comme l’équilibrage des classes ou l’intégration de variables supplémentaires (Nova score, pays de production, liste d’ingrédients).

3. **Pistes d’Amélioration**  
   - **Collecte de plus de données** : mieux représenter certaines catégories ou certains Nutriscores rares (b, e).  
   - **Hyperparamétrage** : affiner les paramètres de la Random Forest (nombre d’arbres, profondeur max, etc.), ou tester d’autres algorithmes (Gradient Boosting, XGBoost).

4. **Ouverture** 
   - L’analyse de la dimension “Environnement” (emballage, labels bio, empreinte carbone) pourrait être un prolongement pour comprendre plus globalement l’impact de notre alimentation.

---


3. **Structure Simplifiée du Projet**  
   - `src/services/api.py` : classe de création et renseignement des produits à partir de l'API.
   - `src/services/barcodes.py` : classe de gestion de la base.  
   - `src/services/traitement.py` : nettoyage, transformations (ex. `Categorie_clean`).  
   - `src/services/stats.py` : visualisations statistiques (boxplots, histogrammes, corrélations, etc.).  
   - `src/services/prediction_rl.py` : implémentation de la régression logistique.  
   - `src/services/prediction_rf.py` : implémentation de la forêt aléatoire (Random Forest).  
   - `food_facts.ipynb` : notebook principal (analyses, graphiques, interprétations).

---

**Merci d’avoir consulté ce projet !**  
N’hésitez pas à proposer des retours, des suggestions ou des améliorations. L’objectif est de continuer à enrichir la base de données et d’affiner les modèles pour mieux comprendre et anticiper la qualité nutritionnelle de notre alimentation.
