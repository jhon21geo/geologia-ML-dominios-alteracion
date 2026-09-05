# Capítulo III. Metodología

El diseño es cuantitativo, correlacional y aplicado: se busca predecir el
**dominio geológico de alteración** a partir de espectro y química de sondaje.

## 3.1 Flujo en seis etapas

```mermaid
flowchart LR
  A[1. Datos] --> B[2. EDA]
  B --> C[3. No supervisado]
  C --> D[4. Etiquetado]
  D --> E[5. Supervisado]
  E --> F[6. Modelo 3D]
```

1. **Recolección.** Espectros TerraSpec y ensayos multielementales, validados
   y unidos por muestra / from–to.
2. **EDA.** Variables categóricas (`aiMineral1`, `VNIRMinerals`) y numéricas
   (13 scores SWIR).
3. **No supervisado.** PCA, dendrograma y K-Means (k = 5) **sobre espectro**.
4. **Segmentación.** El geólogo valida clústeres y define `MOD_ALT` (seis
   dominios). En la tesis eso se apoyó en Leapfrog.
5. **Supervisado.** 80 % / 20 % estratificado sobre tramos etiquetados;
   comparación RF, k-NN, MLP y SVM **sobre geoquímica**.
6. **Predicción 3D.** El mejor modelo etiqueta el resto de intervalos.

En la tesis el modelado se hizo en Orange. Este repositorio reproduce las
mismas etapas en scikit-learn.

## 3.2 Datos espectrales

Ausspec entrega ~69 columnas. Tras tirar minerales de media cero quedan
**13 scores SWIR** (Tabla 15):

WhiteMica, Chlorite, Carbonate, Epidote, Kaolinite, Dickite, Montmor,
Alunite, Gypsum, Pyrophyllite, Diaspore, Zunyite, Water_silica.

VNIR aporta hematita/goethita para el dominio de óxidos. Pares con Pearson y
Spearman > 0,65 se leyeron como ensamble.

## 3.3 Datos químicos

Protocolo (sección 3.10):

1. Completitud ≥ **80 %** (se eliminaron variables raras: AuCN, CuCN, Hg, etc.).
2. Imputación: **mediana por sondaje**, luego mediana global.
3. Outliers: recorte al **percentil 99** (no se borran filas).
4. **Z-score**, porque conviven `%` y `ppm`.

La variable objetivo es `MOD_ALT`. Las coordenadas **no** entran al
clasificador (evitar fuga espacial).

## 3.4 Seis dominios (sección 3.12.2)

| Código | Dominio | Criterio mineralógico |
| --- | --- | --- |
| ArgAvd | Argílica avanzada | Pirofilita + alunita (± diásporo, zunyita). Se fusionan dos variantes ácidas |
| Fil | Fílica | Mica blanca dominante |
| Arg | Argílica | Caolinita + mica blanca |
| Pro | Propilítica | Montmorillonita + clorita ± carbonato/epidota |
| Sk | Skarn | Clorita + montmorillonita + mica + caolinita |
| Oxd | Óxidos | Hematita/goethita VNIR ± yeso/sílice hidratada |

En la tesis, 86 538 intervalos etiquetados (Tabla 17): Fil 28 669, Sk 25 266,
ArgAvd 23 308, Pro 5 050, Oxd 3 297, Arg 978. Fil, Sk y ArgAvd dominan; Arg y
Pro son clases raras (sesgo de recall).

## 3.5 Hiperparámetros publicados (Tablas 19–22)

| Modelo | Ajuste |
| --- | --- |
| Random Forest | 10 árboles, `max_features=8`, profundidad 4, `min_samples_split=5`, clases balanceadas |
| k-NN | k = 5, Euclidean, pesos por distancia |
| MLP | 100 neuronas, ReLU, Adam, α = 10⁻⁴, 200 iteraciones |
| SVM | C = 1, kernel RBF, tope de **100 iteraciones** en Orange |

El tope de 100 iteraciones del SVM explica, en parte, su mal desempeño. El
perfil `robust` del código relaja árboles, red e iteraciones.

## 3.6 División train / test

Tramos validados en 3D: 86 538. De ellos, 80 % (69 231) calibran; el resto de
la química (≈ 147 820) se usó como población más ciega. Una partición
puramente aleatoria por fila inflaría métricas por correlación espacial a lo
largo del mismo taladro.
