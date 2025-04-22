import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def setup_ui(actualiser_callback):
    root = tk.Tk()
    root.title("Surveillance des processus - Détection d'anomalies Tp entrepot")
    root.geometry("1000x600")
   
    titre_h1 = tk.Label(root, text="Entrepot TP", 
                        font=("Arial", 20, "bold"), 
                        fg="#2c3e50")
    titre_h1.pack(pady=10)

    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    right_frame = tk.Frame(root, padx=10, pady=10)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y)

    fig, ax = plt.subplots(figsize=(5, 5))
    canvas = FigureCanvasTkAgg(fig, master=left_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    titre = tk.Label(right_frame, text="Anomalies détectées", font=("Arial", 16, "bold"))
    titre.pack()
    
    compteur = tk.Label(right_frame, text="Nombre : 0", font=("Arial", 12))
    compteur.pack(pady=5)

    colonnes = ("PID", "Nom", "CPU", "RAM")
    table = ttk.Treeview(right_frame, columns=colonnes, show="headings")
    for col in colonnes:
        table.heading(col, text=col)
        table.column(col, width=100)
    table.pack(fill=tk.BOTH, expand=True)

    def update():
        actualiser_callback(root, ax, canvas, table, compteur)
        root.after(10000, update)

    return root, update
