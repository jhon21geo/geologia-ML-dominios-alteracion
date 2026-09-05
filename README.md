# Delimitación de dominios de alteración hidrotermal

Metodología abierta para integrar **espectrometría SWIR/VNIR** y **geoquímica
multielemental** con aprendizaje automático, y clasificar seis dominios de
alteración.

El código replica el flujo de la tesis de pregrado de Jhonatan Paul Mallma
Espinoza (Universidad Nacional de Ingeniería, 2026). El yacimiento original se
omite a propósito: el repositorio usa un **depósito sintético** con las mismas
asociaciones mineralógicas, proporciones de dominios e hiperparámetros
publicados, para que cualquiera pueda ejecutar, criticar y adaptar el método.

[![Tests](https://github.com/jhon21geo/geologia-ML-dominios-alteracion/actions/workflows/tests.yml/badge.svg)](https://github.com/jhon21geo/geologia-ML-dominios-alteracion/actions/workflows/tests.yml)

## Visor de lectura

**Tesis resumida en línea:**
[https://jhon21geo.github.io/geologia-ML-dominios-alteracion/](https://jhon21geo.github.io/geologia-ML-dominios-alteracion/)

Empieza por el [mapa de lectura](https://jhon21geo.github.io/geologia-ML-dominios-alteracion/guia/):
qué página responde a qué pregunta, la distinción clúster ≠ dominio, y cómo
probar el método en Orange o Colab. El PDF de 160 páginas queda en solo
lectura. No uses `jhonatanmallma.github.io` (esa cuenta no sirve este
repositorio).

## Qué resuelve

La delimitación visual de alteraciones en sondaje es lenta y sesgada. El flujo
propone:

1. Filtrar y estandarizar scores minerales SWIR (13 fases diagnósticas).
2. Descubrir ensambles con PCA, clustering jerárquico y K-Means (`k=5`).
3. Etiquetar seis dominios (`Arg`, `ArgAvd`, `Fil`, `Oxd`, `Pro`, `Sk`).
4. Entrenar Random Forest, k-NN, red neuronal y SVM sobre geoquímica.
5. Exportar predicciones listas para un modelo 3D (Leapfrog u otro).

En la tesis, **Random Forest** fue el clasificador más estable. En los datos
sintéticos el ranking se recalcula cada vez que corres el pipeline.

## Inicio rápido (elige un camino)

**Sin instalar Python**

- Lienzo de widgets, como la tesis:
  **[Orange 3](https://jhon21geo.github.io/geologia-ML-dominios-alteracion/09-orange-colab/#orange-como-en-la-tesis)**
- Un clic en el navegador:
  [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jhon21geo/geologia-ML-dominios-alteracion/blob/cursor/metodologia-tesis-sintetica-fd6d/notebooks/00_colab_pipeline.ipynb)

Guía: [Orange y Google Colab](https://jhon21geo.github.io/geologia-ML-dominios-alteracion/09-orange-colab/)

**Con Python en tu máquina**

```bash
git clone https://github.com/jhon21geo/geologia-ML-dominios-alteracion.git
cd geologia-ML-dominios-alteracion
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m alteration_ml.cli generate
python -m alteration_ml.cli run --profile thesis
pytest
```

Figuras en `outputs/figures/`. Métricas en `outputs/metrics_ranking.csv`.

```bash
# Perfil más estable (más árboles, MLP más profunda)
python -m alteration_ml.cli run --profile robust --regenerate
```

## Dominios que replica el sintético

| Código | Dominio | Ensamble diagnóstico |
| --- | --- | --- |
| `ArgAvd` | Argílica avanzada | Pirofilita + alunita ± diásporo ± zunyita |
| `Fil` | Fílica | Mica blanca (ilita/sericita) |
| `Arg` | Argílica | Caolinita + mica blanca |
| `Pro` | Propilítica | Clorita + montmorillonita ± carbonato ± epidota |
| `Sk` | Skarn | Clorita + montmorillonita + mica + caolinita |
| `Oxd` | Óxidos | Hematita/goethita ± sílice hidratada ± yeso |

Las frecuencias relativas siguen la Tabla 17 de la tesis (ArgAvd, Fil y Sk
dominan; Arg y Pro son minoritarios).

## Estructura

```
src/alteration_ml/   paquete Python
data/synthetic/      CSV generados (semilla 42)
notebooks/           Colab + EDA, no supervisado, supervisado
orange/              Recetario del lienzo Orange
docs/                sitio MkDocs
configs/pipeline.yaml
tests/
```

## Documentación

- **Visor de lectura (tesis resumida):** [jhon21geo.github.io/geologia-ML-dominios-alteracion](https://jhon21geo.github.io/geologia-ML-dominios-alteracion/)
- PDF original: [`docs/Tesis.pdf`](docs/Tesis.pdf)
- Cómo aplicar el método a *tus* sondajes: [docs/06-replicacion.md](docs/06-replicacion.md)
- **Sin programar:** [Orange y Google Colab](docs/09-orange-colab.md)

## Opiniones de terceros

Abre un issue con la plantilla **Opinión metodológica** o **Replicación**:

https://github.com/jhon21geo/geologia-ML-dominios-alteracion/issues/new/choose

Guía: [CONTRIBUTING.md](CONTRIBUTING.md)

## Citar

Mallma Espinoza, J. P. (2026). *Delimitación de los dominios geológicos de
alteración desde firmas espectrales y geoquímica mediante el empleo de machine
learning* [Tesis de pregrado, Universidad Nacional de Ingeniería].

Ver también [`CITATION.cff`](CITATION.cff).

## Licencia

[MIT](LICENSE). Los datos del repositorio son sintéticos. No se publican datos
de operaciones.
