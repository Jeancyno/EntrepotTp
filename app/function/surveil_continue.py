import psutil
import pandas as pd
from datetime import datetime
from sklearn.ensemble import IsolationForest
import time
import os

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

print("🔁 Surveillance en temps réel des processus... (Ctrl+C pour arrêter)\n")

while True:
    df = collecter_processus()
    X = df[["cpu", "memoire_MB"]]

    model = IsolationForest(contamination=0.1, random_state=42)
    df["anomalie"] = model.fit_predict(X)
    df["anomalie"] = df["anomalie"].map({1: "normal", -1: "anormal"})

    anormaux = df[df["anomalie"] == "anormal"]

    os.system('cls' if os.name == 'nt' else 'clear')  # Efface l’écran à chaque boucle
    print(f"⏱️  Mise à jour : {datetime.now().strftime('%H:%M:%S')}")
    
    if not anormaux.empty:
        print("\n🚨 Anomalies détectées :")
        print(anormaux[["nom", "cpu", "memoire_MB"]])
    else:
        print("\n✅ Aucun processus suspect détecté.")

    time.sleep(2)  # Attente de 10 secondes
