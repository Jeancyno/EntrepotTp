import psutil
import pandas as pd
from datetime import datetime
from sklearn.ensemble import IsolationForest
import time
import matplotlib.pyplot as plt
import mplcursors
import os

plt.ion()
fig, ax = plt.subplots()
fig.set_size_inches(8, 6)

def collecter_processus():
    processus = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            infos = p.info
            processus.append({
                "pid": infos["pid"],
                "nom": infos["name"],
                "cpu": infos["cpu_percent"],
                "memoire_MB": round(infos["memory_info"].rss / (1024 * 1024), 2)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return pd.DataFrame(processus)

while True:
    df = collecter_processus()
    X = df[["cpu", "memoire_MB"]]

    model = IsolationForest(contamination=0.1, random_state=42)
    df["anomalie"] = model.fit_predict(X)
    df["anomalie"] = df["anomalie"].map({1: "normal", -1: "anormal"})

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"⏱️ Mise à jour : {datetime.now().strftime('%H:%M:%S')}")
    anormaux = df[df["anomalie"] == "anormal"]
    normaux = df[df["anomalie"] == "normal"]

    print(f"🔍 {len(anormaux)} processus anormaux détectés.")

    ax.clear()
    ax.set_title("Scatter Plot – CPU vs Mémoire (Anomalies)")
    ax.set_xlabel("CPU (%)")
    ax.set_ylabel("Mémoire (MB)")

    sc1 = ax.scatter(normaux["cpu"], normaux["memoire_MB"], color='green', label='Normal', alpha=0.6)
    sc2 = ax.scatter(anormaux["cpu"], anormaux["memoire_MB"], color='red', label='Anormal', s=100, edgecolors='black')

    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.pause(0.1)

    # Ajout des tooltips interactifs
    cursor = mplcursors.cursor([sc1, sc2], hover=True)
    @cursor.connect("add")
    def on_add(sel):
        idx = sel.index
        if sel.artist == sc1:
            proc = normaux.iloc[idx]
        else:
            proc = anormaux.iloc[idx]
        sel.annotation.set_text(f"{proc['nom']}\nCPU: {proc['cpu']}%\nRAM: {proc['memoire_MB']} MB")

    time.sleep(10)
