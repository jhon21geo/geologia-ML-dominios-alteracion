# Replicar el pipeline

¿No usas Python a diario? Empieza por
**[Orange o Google Colab](09-orange-colab.md)**. Esta página es el camino con
código local.

## En este repositorio

```bash
pip install -e ".[dev]"
python -m alteration_ml.cli generate --holes 24 --seed 42
python -m alteration_ml.cli run --profile thesis
pytest
```

Notebooks:

0. `notebooks/00_colab_pipeline.ipynb` (Google Colab, un clic)
1. `notebooks/01_eda_espectral_geoquimica.ipynb`
2. `notebooks/02_unsupervised_ensambles.ipynb`
3. `notebooks/03_supervised_clasificacion.ipynb`

## En tus sondajes

Prepara un CSV con al menos:

```text
sample_id, holeid, from_m, to_m, x, y, z,
WhiteMica, Chlorite, Carbonate, Epidote, Kaolinite, Dickite, Montmor,
Alunite, Gypsum, Pyrophyllite, Diaspore, Zunyite, Water_silica,
Hematite, Goethite, Au_ppm, As_ppm, S_pct, ... , MOD_ALT, labeled
```

`MOD_ALT` puede ser nulo en tramos ciegos; `labeled=False` los excluye del
entrenamiento.

```python
import pandas as pd
from alteration_ml.preprocess import prepare_feature_matrix
from alteration_ml.unsupervised import fit_pca, fit_kmeans
from alteration_ml.supervised import split_labeled, train_models, predict_frame
from alteration_ml.evaluate import evaluate_model, metrics_table

df = pd.read_csv("mis_datos.csv")
spec, spec_z, _ = prepare_feature_matrix(df, feature_kind="spectral")
chem, chem_z, _ = prepare_feature_matrix(df, feature_kind="chemistry")
pca, scores, _ = fit_pca(spec[spec_z].to_numpy())
_, clusters, sil = fit_kmeans(spec[spec_z].to_numpy(), n_clusters=5)

labeled = chem[chem["labeled"] == True]
split = split_labeled(labeled, chem_z)
models = train_models(split, profile="robust")
print(metrics_table({n: evaluate_model(m, split.X_test, split.y_test) for n, m in models.items()}))
```

## Adaptaciones frecuentes

| Situación | Qué tocar |
| --- | --- |
| Otro ensamble (p. ej. sin skarn) | Recorta `DOMAINS` y reetiqueta `MOD_ALT` |
| Solo geoquímica, sin SWIR | Omite K-Means; el supervisado sigue en pie si hay etiquetas de log |
| Solo SWIR, sin química | Usa clustering como producto; no hay RF geoquímico |
| Clases aún más desbalanceadas | `class_weight="balanced"` ya está; prueba `robust` |
| Validación espacial | Parte por `holeid`, no por fila |

No subas a GitHub tablas reales. En el issue de replicación basta el tipo de
sistema, el tamaño de muestra y las métricas.
