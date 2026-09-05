# Resumen y abstract

!!! success "Qué debe quedarte de esta página"
    1. El cuello de botella ya no es adquirir datos: es **integrar** espectro, química y logueo.
    2. Hay **seis dominios** de alteración. No salen solos del K-Means: el geólogo los nombra con el ensamble y la continuidad 3D.
    3. Entre SVM, k-NN, red neuronal y bosques aleatorios, **Random Forest** fue el más estable para predecir esos dominios desde la geoquímica.

| Código | Dominio | Ensamble que lo sostiene |
| --- | --- | --- |
| ArgAvd | Argílica avanzada | Pirofilita + alunita |
| Fil | Fílica | Mica blanca |
| Arg | Argílica | Caolinita + mica |
| Pro | Propilítica | Clorita + montmorillonita |
| Sk | Skarn | Clorita + montmorillonita + mica + caolinita |
| Oxd | Óxidos | Hematita / goethita (VNIR) |

El detalle de cómo se firman está en
[El geólogo asigna los dominios](03-asignacion-dominios.md).

=== "Resumen"

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

=== "Abstract"

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

<div class="siguiente" markdown>

**Siguiente lectura:** [Introducción](00b-introduccion-tesis.md) (contexto) o,
si ya tienes el problema claro,
[asignación de dominios](03-asignacion-dominios.md) (el paso decisivo).

</div>
