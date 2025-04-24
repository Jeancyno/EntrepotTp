import psutil
import pandas as pd
from model import detecter_anomalies 
import time

total_cpu = 100 * psutil.cpu_count(logical=True)
total_ram_bytes = psutil.virtual_memory().total
total_ram_mb = total_ram_bytes / (1024 ** 2)
# (total * perc) / 100 = x
# perc = (x * 100) / total
def collecter_processus():
    processus = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            infos = p.info
            cpu_percent = (infos["cpu_percent"] * 100) / total_cpu
            # ram_percent = ((round(infos["memory_info"].rss / (1024 * 1024), 2)) * 100) / total_ram_mb
            # print('--->', )
            # time.sleep(2)
            processus.append({
                "pid": infos["pid"],
                "nom": infos["name"],
                "cpu": cpu_percent,
                "memoire_MB": round(infos["memory_info"].rss / (1024 * 1024), 2)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return pd.DataFrame(processus)

def actualiser(root, ax, canvas, table, compteur):
    df = collecter_processus()
    if df.empty:
        return
    # Cette partie est inutile car le programme s'actualisera
    #     root.after(10000, lambda: actualiser(root, ax, canvas, table, compteur))
    #     return

    df = detecter_anomalies(df)  
    from utils import mettre_a_jour_graphique, mettre_a_jour_tableau

    mettre_a_jour_graphique(df, ax, canvas)
    mettre_a_jour_tableau(df, table, compteur)
