from services.stats import Statistiques
import matplotlib.pyplot as plt


ecoscore_moyen = Statistiques().moy_par_cat()
# Créer le graphe
plt.figure(figsize=(10, 6))
ecoscore_moyen.sort_values().plot(kind="barh", color="skyblue", edgecolor="black")
plt.title("Ecoscore moyen par catégorie", fontsize=16)
plt.xlabel("Ecoscore moyen", fontsize=14)
plt.ylabel("Catégories", fontsize=14)
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()
# Afficher le graphique
plt.show()
# if __name__ == "__main__":
#     pass