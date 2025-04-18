import psutil
import pandas as pd
from datetime import datetime
from sklearn.ensemble import IsolationForest
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Création de la fenêtre principale
root = tk.Tk()
root.title("Surveillance des processus - Détection d'anomalies")
root.geometry("1000x600")

# Layout : 2 colonnes
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

right_frame = tk.Frame(root, padx=10, pady=10)
right_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Graphique matplotlib intégré
fig, ax = plt.subplots(figsize=(5, 5))
canvas = FigureCanvasTkAgg(fig, master=left_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Titre et compteur
titre = tk.Label(right_frame, text="Anomalies détectées", font=("Arial", 16, "bold"))
titre.pack()

compteur = tk.Label(right_frame, text="Nombre : 0", font=("Arial", 12))
compteur.pack(pady=5)

# Tableau (Treeview)
colonnes = ("PID", "Nom", "CPU", "RAM")
table = ttk.Treeview(right_frame, columns=colonnes, show="headings")
for col in colonnes:
    table.heading(col, text=col)
    table.column(col, width=100)
table.pack(fill=tk.BOTH, expand=True)

# Fonction de collecte et détection
def actualiser():
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

    df = pd.DataFrame(processus)
    if df.empty:
        root.after(10000, actualiser)
        return

    X = df[["cpu", "memoire_MB"]]
    model = IsolationForest(contamination=0.1, random_state=42)
    df["anomalie"] = model.fit_predict(X)
    df["anomalie"] = df["anomalie"].map({1: "normal", -1: "anormal"})

    # Update graph
    ax.clear()
    normaux = df[df["anomalie"] == "normal"]
    anormaux = df[df["anomalie"] == "anormal"]

    ax.set_title("CPU vs RAM (Anomalies)")
    ax.set_xlabel("CPU (%)")
    ax.set_ylabel("Mémoire (MB)")

    ax.scatter(normaux["cpu"], normaux["memoire_MB"], color='green', label='Normal', alpha=0.6)
    ax.scatter(anormaux["cpu"], anormaux["memoire_MB"], color='red', label='Anormal', s=100, edgecolors='black')
    ax.legend(loc='upper right')
    canvas.draw()

    # Update tableau
    for item in table.get_children():
        table.delete(item)

    for _, row in anormaux.iterrows():
        table.insert("", "end", values=(row["pid"], row["nom"], row["cpu"], row["memoire_MB"]))

    compteur.config(text=f"Nombre : {len(anormaux)}")

    root.after(10000, actualiser)  # relancer dans 10 secondes

# Démarrer la mise à jour
actualiser()

# Lancer la boucle principale
root.mainloop()