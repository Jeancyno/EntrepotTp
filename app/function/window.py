import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

import asyncio

class Window:
	def __init__(self, loop, afterMS=2000, actualiser_callback=None):
		self.afterMS = afterMS
		self.loop = loop
		self.setActualizer(actualiser_callback)
		self.config()

	def config(self):
		self.root = tk.Tk()
		self.root.title("Surveillance des processus - Détection d'anomalies Tp entrepot")
		self.root.geometry("1000x600")
	
		titre_h1 = tk.Label(self.root, text="Entrepot TP", 
							font=("Arial", 20, "bold"), 
							fg="#2c3e50")
		titre_h1.pack(pady=10)

		self.left_frame = tk.Frame(self.root)
		self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		self.right_frame = tk.Frame(self.root, padx=10, pady=10)
		self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)


		
		fig, self.ax = plt.subplots(figsize=(5, 5))
		self.canvas = FigureCanvasTkAgg(fig, master=self.left_frame)
		self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

		titre = tk.Label(self.right_frame, text="Anomalies détectées", font=("Arial", 16, "bold"))
		titre.pack()
		
		self.compteur = tk.Label(self.right_frame, text="Nombre : 0", font=("Arial", 12))
		self.compteur.pack(pady=5)

		colonnes = ("PID", "Nom", "CPU", "RAM")
		self.table = ttk.Treeview(self.right_frame, columns=colonnes, show="headings")
		for col in colonnes:
			self.table.heading(col, text=col)
			self.table.column(col, width=100)
		self.table.pack(fill=tk.BOTH, expand=True)
		# print('testons')
	
	def setActualizer(self, actualiser_callback):
		self.actualiser_callback = actualiser_callback
		return self
	def mainLoop(self):
		if(self.root != None):
			self.root.mainloop()

	def updateAfter(self):
		future = asyncio.run_coroutine_threadsafe(self.appExec(), self.loop)
		future.add_done_callback(lambda fut: fut.exception())
		self.root.after(self.afterMS, self.updateAfter)
		return self
	
	async def appExec(self):

		self.actualiser_callback(self.root, self.ax, self.canvas, self.table, self.compteur)

		# print('Updated !')

		# return self
