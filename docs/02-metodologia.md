# 2. Metodología

El pipeline está implementado en `src/alteration_ml` y se dispara con
`python -m alteration_ml.cli run`.

## Datos de entrada

Cada intervalo de sondaje tiene:

- Identificadores y geometría: `sample_id`, `holeid`, `from_m`, `to_m`, `x`, `y`, `z`
- 13 scores SWIR (0–100): mica blanca, clorita, carbonato, epidota, caolinita,
  dickita, montmorillonita, alunita, yeso, pirofilita, diásporo, zunyita, sílice hidratada
- VNIR: hematita, goethita y `VNIRMinerals`
- 34 elementos químicos (ppm o %)
- Etiqueta `MOD_ALT` en tramos de entrenamiento; el resto queda para predicción ciega

En la tesis esas tablas salían de Ausspec + laboratorio. Aquí las genera
`alteration_ml.synthetic` con semilla fija.

## Preproceso (sección 3.10 de la tesis)

1. **Completitud.** Se descartan columnas con menos del 80 % de datos.
2. **Imputación.** Mediana por sondaje y, si aún falta, mediana global.
3. **Outliers.** Recorte al percentil 99 (no se borran filas: se preserva la traza).
4. **Escala.** Z-score, porque conviven `%` y `ppm`.

```python
from alteration_ml.preprocess import prepare_feature_matrix
ready, z_cols, scaler = prepare_feature_matrix(df, feature_kind="chemistry")
```

## No supervisado (sección 3.11)

Se aplica **solo a las abundancias espectrales**:

| Técnica | Rol |
| --- | --- |
| PCA | Reduce ruido y muestra separación de ensambles en PC1–PC2 |
| Clustering jerárquico (Ward) | Agrupa los *13 minerales* por perfil de ocurrencia |
| K-Means (`k=5`) | Agrupa *muestras*; `k` se toma del dendrograma |

El valor `k=5` no es un dominio geológico todavía: es una partición estadística
que se interpreta con el ensamble mineral y se traduce a los seis `MOD_ALT`.

## Asignación de dominios (sección 3.12.2)

| Dominio | Criterio mineralógico |
| --- | --- |
| ArgAvd | Pirofilita + alunita (se fusionan dos variantes ácidas) |
| Fil | Mica blanca dominante |
| Arg | Caolinita + mica blanca |
| Pro | Montmorillonita + clorita ± carbonato/epidota |
| Sk | Clorita + montmorillonita + mica + caolinita |
| Oxd | Hematita/goethita (VNIR) ± yeso/sílice hidratada |

Las frecuencias del sintético **no copian el conteo exacto** de la Tabla 17
(eso forzaba a romper la zonación). Priorizan un análogo espacial: núcleo
ácido, halo fílico/argílico, propilítica distal, skarn a mayor profundidad y
óxidos someros. Arg sigue siendo la clase más chica.

## Supervisado (sección 3.12)

Variable objetivo: `MOD_ALT`. Variables predictoras: geoquímica Z-score
(no las coordenadas: evitar fugas espaciales). Partición 80/20 estratificada
sobre tramos etiquetados.

Hiperparámetros del perfil `thesis` (Tablas 19–22):

| Modelo | Ajustes publicados |
| --- | --- |
| Random Forest | 10 árboles, `max_features=8`, profundidad 4, `min_samples_split=5`, clases balanceadas |
| k-NN | k=5, Euclidean, pesos por distancia |
| MLP | 100 neuronas, ReLU, Adam, α=10⁻⁴ |
| SVM | C=1, kernel RBF |

El SVM de Orange usaba un tope de **100 iteraciones**. El perfil `thesis` lo
reproduce (suele no converger y quedar por debajo de RF). El perfil `robust`
sube árboles, capacidad de la red e iteraciones del SVM.

## Evaluación

Exactitud, precisión y recall macro, F1, AUC one-vs-rest, matriz de confusión y
curvas ROC por dominio. El modelo ganador etiqueta el resto de intervalos.

## Modelamiento 3D

La tesis exportaba predicciones a Leapfrog. Este repo se detiene en CSV
(`outputs/predicciones.csv`) y en secciones X–Y / Y–Z. Cualquier modelador
implícito puede consumir `holeid`, `from_m`, `to_m`, `best_pred`.
