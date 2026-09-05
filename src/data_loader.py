import pandas as pd

def load_geochemical_data(file_path: str) -> pd.DataFrame:
    """Carga y valida datos geoquímicos multi-elementales."""
    df = pd.read_csv(file_path)
    return df
