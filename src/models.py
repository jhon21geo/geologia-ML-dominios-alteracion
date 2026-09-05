from sklearn.cluster import KMeans
import pandas as pd

def train_alteration_clustering(data: pd.DataFrame, n_clusters: int = 4):
    """Entrena modelo de clustering para delimitación de dominios de alteración."""
    model = KMeans(n_clusters=n_clusters, random_state=42)
    labels = model.fit_predict(data)
    return model, labels
