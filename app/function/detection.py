import psutil
import pandas as pd
from model import detecter_anomalies 

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

def actualiser(root, ax, canvas, table, compteur):
    df = collecter_processus()
    if df.empty:
        root.after(10000, lambda: actualiser(root, ax, canvas, table, compteur))
        return

    df = detecter_anomalies(df)  
    from utils import mettre_a_jour_graphique, mettre_a_jour_tableau

    mettre_a_jour_graphique(df, ax, canvas)
    mettre_a_jour_tableau(df, table, compteur)
