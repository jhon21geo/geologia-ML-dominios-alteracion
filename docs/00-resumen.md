# Resumen y abstract

## Resumen

La industria minera acumula datos geológicos, geoquímicos, espectrales y
geofísicos, recientes e históricos. El cuello de botella ya no es adquirirlos, sino
**integrarlos e interpretarlos de forma conjunta**. El aprendizaje automático
permite hallar patrones que la inspección visual de testigos no sistematiza.

Esta investigación desarrolla una metodología para **vincular anomalías
espectrales con el modelo de estimación de recursos**, integrando
espectrometría (TerraSpec / SWIR–VNIR), registros geológicos y química de
sondaje. El análogo es un sistema **Au–Cu epitermal de alta sulfuración** con
transición hacia pórfido/skarn.

Los dominios se definieron a partir de scores minerales de sondaje, con
aprendizaje **no supervisado**: análisis jerárquico, K-Means y PCA. Se
identificaron y caracterizaron **seis dominios de alteración**. Luego, con
análisis exploratorio, se eligieron variables y tramos para entrenar
clasificadores **supervisados**: SVM, k-NN, bosques aleatorios y redes
neuronales.

**Random Forest** ofreció el mejor desempeño predictivo (precisión y
robustez). La integración sistemática de variables supera sesgos de la
interpretación visual y mejora la delimitación de zonas hidrotermales. El
modelamiento geométrico 3D (Leapfrog) validó continuidad espacial y zonación
mineralógica, con impacto directo en la estimación de recursos.

**Palabras clave:** machine learning, asociaciones mineralógicas, alteración
hidrotermal, dominios geológicos, Random Forest, espectrometría.

## Abstract

The mining industry can acquire geological, geochemical, spectral and
geophysical data at scale, yet joint interpretation remains difficult. Machine
learning recovers non-obvious patterns from those volumes.

This study develops a workflow that links spectral anomalies to resource
models by integrating spectrometry (TerraSpec), geological logs and
multielement chemistry. Unsupervised learning (hierarchical clustering,
K-Means, PCA) defined **six alteration domains**. Supervised classifiers
(SVM, k-NN, random forests, neural networks) were then trained on
geochemistry; **Random Forest** was the most accurate and robust.

Systematic variable integration reduces the bias of purely visual logging and
improves hydrothermal-zone outlines. Complementary 3D implicit modelling
confirmed spatial continuity and mineralogical zoning, with implications for
resource estimation.

**Keywords:** machine learning, mineral associations, hydrothermal alteration,
geological domains, Random Forest, spectrometry.
