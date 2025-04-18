def mettre_a_jour_graphique(df, ax, canvas):
    ax.clear()
    normaux = df[df["anomalie"] == "normal"]
    anormaux = df[df["anomalie"] == "anormal"]

    ax.set_title("CPU vs RAM (Anomalies)")
    ax.set_xlabel("CPU (%)")
    ax.set_ylabel("Mémoire (MB)")
    ax.set_facecolor("#f5f5f5")  # fond du graphique
    


    ax.scatter(normaux["cpu"], normaux["memoire_MB"], color='green', label='Normal', alpha=0.6)
    ax.scatter(anormaux["cpu"], anormaux["memoire_MB"], color='red', label='Anormal', s=100, edgecolors='black')
    ax.legend(loc='upper right')
    canvas.draw()

def mettre_a_jour_tableau(df, table, compteur):
    for item in table.get_children():
        table.delete(item)

    anormaux = df[df["anomalie"] == "anormal"]
    for _, row in anormaux.iterrows():
        table.insert("", "end", values=(row["pid"], row["nom"], row["cpu"], row["memoire_MB"]))

    compteur.config(text=f"Nombre d'anomalies  : {len(anormaux)}")
