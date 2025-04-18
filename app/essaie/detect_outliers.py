# import numpy as np
# def detect_outliers_iqr(df, column):
#     Q1 = df[column].quantile(0.25)
#     Q3 = df[column].quantile(0.75)
#     IQR = Q3 - Q1
#     lower_bound = Q1 - 1.5 * IQR
#     upper_bound = Q3 + 1.5 * IQR
#     outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
#     return outliers

# # def detect_outliers_iqr(data):
# #     Q1 = np.percentile(data, 25)
# #     Q3 = np.percentile(data, 75)
# #     IQR = Q3 - Q1
# #     lower_bound = Q1 - 1.5 * IQR
# #     upper_bound = Q3 + 1.5 * IQR
# #     outliers = data[(data < lower_bound) | (data > upper_bound)]
# #     return outliers, lower_bound, upper_bound


import pandas as pd
from sklearn.ensemble import IsolationForest

# Charger le fichier CSV généré à l'étape 1
df = pd.read_csv("processus_actifs.csv")

# On garde seulement les colonnes numériques utiles pour le modèle
X = df[["cpu", "memoire_MB"]]

# Création du modèle Isolation Forest
model = IsolationForest(contamination=0.1, random_state=42)
df["anomalie"] = model.fit_predict(X)

# -1 = anormal, 1 = normal → on rend ça plus lisible
df["anomalie"] = df["anomalie"].map({1: "normal", -1: "anormal"})

# Affichage des résultats
print(df[["nom", "cpu", "memoire_MB", "anomalie"]])

# Sauvegarde dans un nouveau fichier CSV
df.to_csv("resultats_anomalies_processus.csv", index=False)
print("✅ Résultats enregistrés dans 'resultats_anomalies_processus.csv'")
# Filtrer les processus anormaux
anormaux = df[df["anomalie"] == "anormal"]

# Affichage clair
print("\n🛑 Processus anormaux détectés :\n")
print(anormaux[["nom", "cpu", "memoire_MB"]])

if not anormaux.empty:
    print("\n🚨 ALERTE : Des processus suspects ont été détectés ! 🚨\n")
else:
    print("\n✅ Aucun processus anormal détecté.")
