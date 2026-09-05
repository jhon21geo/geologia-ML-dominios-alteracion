# Capítulo I. Planteamiento

!!! question "Pregunta general"
    ¿Cómo la imprecisión en la delimitación de los dominios mineralógicos de las
    alteraciones impacta en el modelo de estimación del recurso mineral?

## 1.1 Generalidades

El machine learning se ha masificado en la última década por algoritmos
accesibles en Python. En estimación de recursos el referente clásico sigue
siendo el kriging; en geología, entornos como **Orange** (Universidad de
Ljubljana) permiten ensamblar flujos visuales sobre NumPy, SciPy y
scikit-learn. La densidad de datos de logueo exige reconocer patrones
multivariados y producir un modelo más estable, no solo más “pintado”.

Predecir características de sondaje a partir de geoquímica y espectro reduce
tiempo de interpretación y sube la consistencia entre taladros.

## 1.2 Problema

Faltan procesos que uniformicen criterios de descripción geológica y
herramientas que identifiquen patrones en conjuntos multivariados. Hill et al.
(2014) y la revisión de Dramsch (2020) muestran que el ML está más difundido
en geofísica que en geoquímica, geoestadística y geología de minas. En el
Perú, la aplicación sistemática aún no está consolidada, pese a protocolos de
control de calidad y a volúmenes TerraSpec ya existentes.

Las asociaciones mineralógicas definen dominios, y esos dominios se
relacionan con clusters económicos. De ahí la pregunta general:

> ¿Cómo la imprecisión en la delimitación de los dominios mineralógicos de las
> alteraciones impacta en el modelo de estimación del recurso mineral?

Preguntas específicas:

- ¿Hay vinculación sistemática de la anomalía espectral al modelo de recursos?
- ¿Están débiles los clusters económicos que relacionan mineralogía y estimación?
- ¿Qué algoritmo delimita mejor esos dominios?

## 1.3 Objetivos

**General.** Mejorar la precisión en la delimitación de los dominios
mineralógicos de alteración que alimentan el modelo de estimación.

**Específicos.**

1. Desarrollar una metodología que vincule la anomalía espectral al modelo de
   recursos.
2. Definir clusters (ensambles) entre mineralogía hidrotermal y el modelo de
   estimación.
3. Elegir el algoritmo de mejor rendimiento para delimitar dominios.

## 1.4 Antecedentes (síntesis)

| Trabajo | Aporte usado aquí |
| --- | --- |
| Cate et al. (2018a, 2018b) | ML como herramienta de geólogo; litogeoquímica → litología y alteración (Lalor, Canadá) |
| Chen et al. (2017) | One-class SVM para anomalías geoquímicas multivariadas |
| Sun et al. (2019) | RF vs SVM vs ANN en prospectividad; **RF** con mejor precisión |
| Carranza & Laborte (2015) | RF y k-NN en mapeo de prospectividad |
| Carrillo et al. (2019) | Ciencia de datos + geometalurgia en sondajes (UNI) |
| Cracknell & Reading (2014) | Comparación de cinco algoritmos en mapeo geológico |

Tao Sun et al. (2019) es el referente más directo para comparar SVM, redes y
Random Forest en un problema de clasificación espacial minera.

## 1.5 Hipótesis

**General.** La delimitación correcta de dominios geológicos impacta de forma
favorable el modelo de estimación.

**Específicas.** Vincular la anomalía espectral al modelo mejora el recurso;
fortalecer clusters económico-mineralógicos reduce incertidumbre; un algoritmo
adecuado (en este estudio, Random Forest) mejora la delimitación.

<div class="siguiente" markdown>

**Siguiente:** [Marco teórico](02-marco-teorico.md) (fondo HS/SWIR) o salta a
[metodología](02-metodologia.md) si ya dominas el contexto.

</div>
