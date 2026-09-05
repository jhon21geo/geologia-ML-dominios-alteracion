# 1. Planteamiento

## Problema

Las operaciones acumulan espectros TerraSpec, logs geológicos y ensayos
químicos, pero la integración suele ser visual y poco repetible. Eso produce
contactos de alteración inconsistentes entre sondajes y aumenta la varianza
intra-dominio en la estimación de recursos.

Pregunta de trabajo: **¿cómo delimitar dominios mineralógicos de alteración de
forma sistemática, vinculando la anomalía espectral con la geoquímica, para
reducir sesgo en el modelo geológico?**

## Objetivos que hereda el código

- Vincular scores SWIR/VNIR con intervalos de sondaje y ensayos químicos.
- Definir ensambles (clusters) coherentes con la mineralogía de alteración.
- Comparar algoritmos y elegir el de mejor desempeño predictivo.

## Alcance de este repositorio

| Incluye | No incluye |
| --- | --- |
| Flujo PCA → clustering → clasificación | Nombre, mapas ni leyes de la unidad original |
| Seis dominios y 13 minerales SWIR de la tesis | Espectros ASD crudos de operación |
| Hiperparámetros publicados | Leapfrog ni licencias comerciales |
| Datos sintéticos con ruido y desbalance | Datos confidenciales de perforación |

El análogo geológico es un sistema **epitermal de alta sulfuración** con
transiciones a **pórfido/skarn**: núcleo ácido, halo fílico, propilítica distal,
skarn cálcico en profundidad y oxidación supérgena.

## Hipótesis operativa

Si los ensambles espectrales se etiquetan con rigor y se mapean sobre
geoquímica estandarizada, un clasificador no lineal (en la tesis, Random Forest)
recupera la zonación mejor que la interpretación visual aislada, y mejor que un
SVM linealmente rígido en un espacio geoquímico mezclado.
