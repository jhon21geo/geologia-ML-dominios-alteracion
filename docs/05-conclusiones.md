# 5. Conclusiones y recomendaciones

## Conclusiones transferibles

1. Un protocolo de completitud, imputación por sondaje, recorte p99 y Z-score
   deja la geoquímica en un espacio comparable para distancias y árboles.
2. PCA + dendrograma + K-Means convierten 13 scores SWIR en ensambles
   discutibles con el geólogo; no sustituyen el etiquetado, lo ordenan.
3. Seis dominios (argílica, argílica avanzada, fílica, óxidos, propilítica,
   skarn) cubren un análogo AS–pórfido–skarn sin anclarse a una unidad.
4. Random Forest, en la tesis, fue el mejor compromiso entre discriminación y
   robustez; SVM fue el más frágil. El repo permite repetir esa comparación.
5. El producto útil para estimación es un intervalo `from–to` con `MOD_ALT`
   predicho, no un mapa pintado a mano.

## Recomendaciones para quien replique

- Empieza con el perfil `robust` si tus clases se solapan más que el sintético.
- Reporta F1 macro y recall de las clases raras, no solo accuracy.
- Separa sondajes (no filas aleatorias) si quieres una validación espacial.
- Documenta qué minerales SWIR *no* tienes: el método se degrada sin alunita
  o sin mica blanca, según el sistema.
- Abre un issue de replicación con métricas anonimizadas.

## Qué queda fuera a propósito

Detalle geomorfológico, logística de la unidad y tablas reales de laboratorio.
Quien necesite el relato académico completo puede leer [`Tesis.pdf`](Tesis.pdf).
