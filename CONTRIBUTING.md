# Contribuciones, opiniones y replicaciones

Este repositorio está pensado para que terceros **lean la metodología, la ejecuten
con datos sintéticos y la repliquen en sus propios proyectos**.

## Cómo participar

1. Abre un [issue](https://github.com/jhon21geo/geologia-ML-dominios-alteracion/issues) con la plantilla adecuada:
   - **Opinión metodológica** — crítica, sugerencia o duda sobre el flujo (PCA, k=5, hiperparámetros, ensambles).
   - **Replicación** — resultados al aplicar el pipeline en otro yacimiento o dataset.
   - **Error** — fallo reproducible del código o de la documentación.
   - **Mejora** — nueva métrica, visualización, algoritmo o traducción.
2. Si tienes código, abre un *pull request* desde un fork.
3. Discute en el issue **antes** de un PR grande (nuevo algoritmo, cambio de dominios, etc.).

## Replicar en tu yacimiento

No se requiere el dato original. Necesitas dos tablas unidas por `sample_id`:

- **Espectral:** abundancias (0–100) de minerales SWIR/VNIR, o al menos los 13
  minerales de `SPECTRAL_MINERALS`.
- **Geoquímica:** elementos multielementales en ppm o %. El clasificador
  supervisado usa estas columnas para predecir `MOD_ALT`.

Pasos mínimos:

```python
import pandas as pd
from alteration_ml.preprocess import prepare_feature_matrix
from alteration_ml.supervised import split_labeled, train_models
from alteration_ml.evaluate import evaluate_model, metrics_table

data = pd.read_csv("mis_sondajes.csv")  # debe incluir MOD_ALT en tramos etiquetados
ready, z_cols, _ = prepare_feature_matrix(data, feature_kind="chemistry")
split = split_labeled(ready, z_cols)
models = train_models(split, profile="robust")
results = {n: evaluate_model(m, split.X_test, split.y_test) for n, m in models.items()}
print(metrics_table(results))
```

Al reportar una replicación, indica (sin datos confidenciales):

- tipo de yacimiento (epitermal AS, pórfido, skarn, otro);
- número de sondajes e intervalos;
- minerales SWIR disponibles;
- métricas (AUC, F1 macro) y si Random Forest sigue siendo el mejor;
- qué cambiaste (k, umbral de completitud, hiperparámetros).

## Estilo de código

- Python 3.10+.
- Tests con `pytest`.
- Documentación en español.
- No subir datos reales de operaciones ni coordenadas de unidades productivas.

```bash
pip install -e ".[dev]"
pytest
```

## Conducta

Participa bajo el [código de conducta](CODE_OF_CONDUCT.md).
