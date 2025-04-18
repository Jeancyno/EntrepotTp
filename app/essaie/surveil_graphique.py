import psutil
import pandas as pd
from datetime import datetime
from sklearn.ensemble import IsolationForest
import time
import os
import matplotlib.pyplot as plt

# Fonction de collecte des processus
def collecter_processus():
    processus = []

    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'status', 'create_time']):
        try:
            infos = p.info
            processus.append({
                "pid": infos["pid"],
                "nom": infos["name"],
                "cpu": infos["cpu_percent"],
                "memoire_MB": round(infos["memory_info"].rss / (1024 * 1024), 2),
                "etat": infos["status"],
                "heure_lancement": datetime.fromtimestamp(infos["create_time"]).strftime("%H:%M:%S")
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return pd.DataFrame(processus)

# Configuration du graphique
plt.ion()  # Mode interactif pour mise à jour en temps réel
fig, ax = plt.subplots()
ax.set_xlabel("Processus")
ax.set_ylabel("CPU (%) / Mémoire (MB)")
ax.set_title("Processus anormaux (en temps réel)")

# Les listes qui vont contenir les données pour le graphique
nom_processus = []
cpu_data = []
memoire_data = []

while True:
    df = collecter_processus()
    X = df[["cpu", "memoire_MB"]]

    # Modèle d'Isolation Forest pour détecter les anomalies
    model = IsolationForest(contamination=0.1, random_state=42)
    df["anomalie"] = model.fit_predict(X)
    df["anomalie"] = df["anomalie"].map({1: "normal", -1: "anormal"})

    # Filtrer les processus anormaux
    anormaux = df[df["anomalie"] == "anormal"]

    os.system('cls' if os.name == 'nt' else 'clear')  # Effacer l'écran à chaque boucle
    print(f"⏱️ Mise à jour : {datetime.now().strftime('%H:%M:%S')}")
    
    if not anormaux.empty:
        print("\n🚨 Anomalies détectées :")
        print(anormaux[["nom", "cpu", "memoire_MB"]])

        # Mettre à jour les listes pour le graphique
        nom_processus = anormaux["nom"].tolist()
        cpu_data = anormaux["cpu"].tolist()
        memoire_data = anormaux["memoire_MB"].tolist()
        
        # Réinitialiser et afficher le graphique
        ax.clear()  # Effacer les anciennes données
        ax.set_xlabel("Processus")
        ax.set_ylabel("CPU (%) / Mémoire (MB)")
        ax.set_title("Processus anormaux (en temps réel)")
        
        ax.barh(nom_processus, cpu_data, label="CPU (%)", color='r')
        ax.barh(nom_processus, memoire_data, label="Mémoire (MB)", color='b', alpha=0.5)
        ax.legend()

        plt.pause(1)  # Pause pour mettre à jour le graphique
    else:
        print("\n✅ Aucun processus suspect détecté.")

    time.sleep(10)  # Attente de 10 secondes avant la prochaine mise à jour
