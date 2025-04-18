from sklearn.ensemble import IsolationForest

def detecter_anomalies(df, contamination=0.1):
    if df.empty:
        return df

    X = df[["cpu", "memoire_MB"]]
    model = IsolationForest(contamination=contamination, random_state=42)
    df["anomalie"] = model.fit_predict(X)
    df["anomalie"] = df["anomalie"].map({1: "normal", -1: "anormal"})
    return df
