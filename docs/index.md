---
hide:
  - toc
---

<div class="hero" markdown>

# Delimitación de dominios geológicos de alteración mediante firmas espectrales, geoquímica y aprendizaje automático

Tesis de pregrado. Flujo cuantitativo para clasificar dominios de alteración
hidrotermal a partir de espectrometría **SWIR–VNIR**, geoquímica de sondaje y
criterio geológico: seis clases mineralógicas y comparación de clasificadores
supervisados.

<p class="meta">
Jhonatan Paul Mallma Espinoza · Asesor: MSc. César Augusto Mendoza Tarazona<br>
Ingeniero Geólogo · FIGMM · Universidad Nacional de Ingeniería · Lima, 2026
</p>

</div>

La hipótesis de trabajo es que el aprendizaje no supervisado (PCA, agrupamiento
jerárquico y K-Means) **propone** agrupaciones espectrales, pero el dominio
geológico (`MOD_ALT`) se define cuando el geólogo valida el ensamble diagnóstico
y la continuidad espacial. El clasificador supervisado —**Random Forest** en
esta investigación— extiende esa firma al resto de la malla. El repositorio
reproduce el flujo con **datos sintéticos** de los mismos ensambles, sin
geometría de la unidad de calibración.

<div class="pills">
  <span class="argavd">ArgAvd · argílica avanzada</span>
  <span class="fil">Fil · fílica</span>
  <span class="arg">Arg · argílica</span>
  <span class="pro">Pro · propilítica</span>
  <span class="sk">Sk · skarn</span>
  <span class="oxd">Oxd · óxidos</span>
</div>

## Recorrido de lectura

El visor condensa la tesis. No es necesario seguir el orden capitular:

<div class="ruta" markdown>

[**1 · Mapa de lectura**
<span>Correspondencia entre preguntas de investigación y secciones del visor.</span>](guia.md)

[**2 · Resumen y abstract**
<span>Problema, seis dominios y desempeño relativo de los clasificadores.</span>](00-resumen.md)

[**3 · Asignación de dominios**
<span>Etapa crítica: clustering espectral y corte geológico de `MOD_ALT`.</span>](03-asignacion-dominios.md)

[**4 · Replicación experimental**
<span>Orange, Google Colab o pipeline en Python sobre el conjunto sintético.</span>](09-orange-colab.md)

</div>

<div class="grid cards" markdown>

-   :material-book-open-page-variant: **Tesis resumida**

    ---

    Capítulos condensados, figuras del flujo y el PDF (páginas 1–151).

    [:octicons-arrow-right-24: Abrir el visor](guia.md)

-   :material-palette-swatch: **Orange o Google Colab**

    ---

    Reproducción del experimento sin entorno Python local (lienzo de widgets o cuaderno en la nube).

    [:octicons-arrow-right-24: Protocolo experimental](09-orange-colab.md)

-   :material-language-python: **Implementación en Python**

    ---

    Paquete `alteration_ml`, datos sintéticos, pruebas automáticas y plantilla para sondajes propios.

    [:octicons-arrow-right-24: Replicar el pipeline](06-replicacion.md)

</div>

## Esquema metodológico

```mermaid
flowchart LR
  A[Espectro SWIR/VNIR] --> C[No supervisado<br/>PCA · K-Means]
  B[Geoquímica] --> D[Supervisado<br/>RF · kNN · MLP · SVM]
  C --> G[Geólogo firma<br/>MOD_ALT]
  G --> D
  D --> E[Predicción 3D]
```

<figure markdown>
  ![Esquema de asignación de dominios](assets/13_asignacion_esquema.png)
  <figcaption>Figura 1. El clúster espectral no equivale al dominio geológico. El geólogo recorta, fusiona o descarta intervalos antes del entrenamiento supervisado.</figcaption>
</figure>

## Cómo citar

??? note "Formatos IEEE y APA 7"

    **IEEE.** Mallma Espinoza, J., “Delimitación de los dominios geológicos de alteración desde firmas espectrales y geoquímica mediante el empleo de machine learning” [Tesis de pregrado]. Lima, Perú: Universidad Nacional de Ingeniería, 2026.

    **APA 7.** Mallma, J. (2026). *Delimitación de los dominios geológicos de alteración desde firmas espectrales y geoquímica mediante el empleo de machine learning* [Tesis de pregrado, Universidad Nacional de Ingeniería]. Repositorio institucional Cybertesis UNI.

ORCID del autor: [0009-0007-5912-5915](https://orcid.org/0009-0007-5912-5915) ·
Asesor: [0009-0009-5452-3636](https://orcid.org/0009-0009-5452-3636).

## Filiación y contacto

<div class="filiacion" markdown>
<a href="https://www.uni.edu.pe/"><img class="escudo" src="assets/uni-escudo-sm.png" alt="UNI"/> Universidad Nacional de Ingeniería</a>
<a href="mailto:jhonatangeo21@gmail.com"><img src="assets/icon-correo.svg" alt=""/> jhonatangeo21@gmail.com</a>
<a href="https://www.linkedin.com/in/geomin"><img src="assets/icon-linkedin.svg" alt=""/> linkedin.com/in/geomin</a>
</div>

Sitio publicado:
[jhon21geo.github.io/geologia-ML-dominios-alteracion](https://jhon21geo.github.io/geologia-ML-dominios-alteracion/).[^url]

[^url]: La dirección `jhonatanmallma.github.io/...` no corresponde a este repositorio (muestra 404).
