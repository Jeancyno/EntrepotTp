# 🧠 Détection d’anomalies non supervisée : Cas de la détection des valeurs aberrantes
#  Détection d'Anomalies des Processus 

Ce projet est une application graphique interactive développée en Python qui permet de surveiller les processus système en temps réel et de détecter les anomalies en utilisant l'algorithme **Isolation Forest**.

## 📌 Fonctionnalités

- 🎯 Détection automatique des processus anormaux (surconsommation CPU ou mémoire)
- 📈 Visualisation graphique des processus avec `matplotlib`
- 📋 Tableau interactif des anomalies détectées
- 🔄 Rafraîchissement automatique toutes les 10 secondes
- 🧪 Utilisation de Machine Learning (Isolation Forest)
- 🧰 Interface utilisateur avec `Tkinter`


## 🔧 Installation

1. Clone ce dépôt :

```bash
git clone https://github.com/Jeancyno/EntrepotTp/app.git
cd app
```

2. creer un environnement virtuel et active le
```bash
python -m env .venv
source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate
```
instaler les dependance 

```bash
pip install -r requirements.txt

pip install psutil,scikit-learn,matplotlib,pandas

#Execute projet avec :

 python main.py






