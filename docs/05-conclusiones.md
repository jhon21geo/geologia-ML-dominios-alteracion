# Conclusiones y recomendaciones

!!! abstract "En una frase"
    Los dominios de alteración se delimitan mejor cuando el geólogo firma el
    ensamble y un **Random Forest** extiende esa firma al resto de la malla.

## Conclusiones (tesis)

1. Un control geoestadístico de contactos (back-flag > 90 % entre tramos y
   sólidos Leapfrog) subió la exactitud predictiva a un rango **90–95 %** y
   estabilizó el modelo de bloques.
2. Integrar SWIR–VNIR (TerraSpec) con química, y compactar con PCA más del
   **80 %** de la varianza espectral, permite atar anomalías espectrales a la
   geometría 3D sin depender solo del ojo del logueo.
3. La correlación entre mineralogía espectral y elementos guía (Au, Cu, As, S)
   delimita dominios y **baja la varianza intra-dominio**, que es lo que
   necesita la estimación.
4. Entre SVM, k-NN, MLP y RF, **Random Forest** fue el más estable frente al
   ruido de perforación: accuracy > 90 % en la calibración publicada, con
   sobreajuste de validación controlado (~0,77). Es la herramienta elegida
   para clasificar dominios de alteración de forma automática.

## Recomendaciones

1. Ampliar y diversificar bases espectrales y geológicas.
2. Probar modelos híbridos (redes + árboles).
3. Validar el mismo flujo en otros tipos de yacimiento —este repositorio
   existe para eso, con dato sintético y plantilla de replicación.
4. Capacitar a geólogos en análisis de datos, no solo en el software 3D.
5. Mantener colaboración academia–industria con datos anonimizados.

## Qué hace este visor

Resume la tesis para lectura pública. El [PDF (págs. 1–151)](tesis-pdf.md) sigue
disponible. El [código](06-replicacion.md) replica el método sin publicar la
unidad de calibración.

<div class="siguiente" markdown>

**Para cerrar la lectura:** [PDF (págs. 1–151)](tesis-pdf.md) ·
[Probar sin Python](09-orange-colab.md) ·
[Dejar una opinión](07-contribuciones.md)

</div>
