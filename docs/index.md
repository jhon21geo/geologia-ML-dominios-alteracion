---
hide:
  - toc
---

<div class="hero" markdown>

# Delimitación de dominios de alteración con machine learning

Tesis de pregrado (versión resumida para leer en línea). El método une
**espectro SWIR–VNIR**, **geoquímica de sondaje** y el **juicio del geólogo**
para definir seis dominios de alteración y luego clasificarlos.

<p class="meta">
Jhonatan Paul Mallma Espinoza · Asesor: MSc. César Augusto Mendoza Tarazona<br>
Ingeniero Geólogo · FIGMM · Universidad Nacional de Ingeniería · Lima, 2026
</p>

<p class="contacto">
<a href="mailto:jhonatangeo21@gmail.com">jhonatangeo21@gmail.com</a>
·
<a href="https://www.linkedin.com/in/geomin">LinkedIn</a>
·
<a href="https://orcid.org/0009-0007-5912-5915">ORCID</a>
</p>

</div>

**Idea central:** el clustering propone grupos; el geólogo los convierte en
dominios (`MOD_ALT`); **Random Forest** extiende esa firma al resto de la
malla. Los datos de este repositorio son **sintéticos** (mismos ensambles, sin
detalle de la unidad de calibración).

<div class="pills">
  <span class="argavd">ArgAvd · argílica avanzada</span>
  <span class="fil">Fil · fílica</span>
  <span class="arg">Arg · argílica</span>
  <span class="pro">Pro · propilítica</span>
  <span class="sk">Sk · skarn</span>
  <span class="oxd">Oxd · óxidos</span>
</div>

## Empieza por aquí

El visor no hay que leerlo de cabo a rabo. Elige un camino:

<div class="ruta" markdown>

[**1 · Mapa de lectura**
<span>Qué página responde a qué pregunta, y en qué orden conviene ir.</span>](guia.md)

[**2 · Resumen (2 minutos)**
<span>Problema, seis dominios y por qué gana Random Forest.</span>](00-resumen.md)

[**3 · Asignación de dominios**
<span>La etapa que no se automatiza: algoritmo + criterio geológico.</span>](03-asignacion-dominios.md)

[**4 · Probar sin Python**
<span>Orange (como la tesis) o Google Colab (un clic en el navegador).</span>](09-orange-colab.md)

</div>

<div class="grid cards" markdown>

-   :material-book-open-page-variant: **Leer la tesis resumida**

    ---

    Capítulos condensados, figuras del flujo y el PDF (páginas 1–151) en
    solo lectura.

    [:octicons-arrow-right-24: Abrir el visor](guia.md)

-   :material-palette-swatch: **Orange o Google Colab**

    ---

    Para quien no programa: el mismo método en lienzo de widgets o en un
    cuaderno en la nube.

    [:octicons-arrow-right-24: Probar el método](09-orange-colab.md)

-   :material-language-python: **Replicar en Python**

    ---

    Pipeline con dato sintético, tests y plantilla para tus sondajes.

    [:octicons-arrow-right-24: Código local](06-replicacion.md)

</div>

## El método en un vistazo

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
  <figcaption>Figura guía: el clúster no es el dominio. El geólogo corta, fusiona o descarta intervalos antes de entrenar el clasificador.</figcaption>
</figure>

## Cómo citar

??? note "Formatos IEEE y APA 7"

    **IEEE.** Mallma Espinoza, J., “Delimitación de los dominios geológicos de alteración desde firmas espectrales y geoquímica mediante el empleo de machine learning” [Tesis de pregrado]. Lima, Perú: Universidad Nacional de Ingeniería, 2026.

    **APA 7.** Mallma, J. (2026). *Delimitación de los dominios geológicos de alteración desde firmas espectrales y geoquímica mediante el empleo de machine learning* [Tesis de pregrado, Universidad Nacional de Ingeniería]. Repositorio institucional Cybertesis UNI.

ORCID del autor: [0009-0007-5912-5915](https://orcid.org/0009-0007-5912-5915).
Asesor: [0009-0009-5452-3636](https://orcid.org/0009-0009-5452-3636).

## Contacto

- Correo: [jhonatangeo21@gmail.com](mailto:jhonatangeo21@gmail.com)
- LinkedIn: [linkedin.com/in/geomin](https://www.linkedin.com/in/geomin)
- GitHub: [jhon21geo](https://github.com/jhon21geo)

Sitio publicado:
[jhon21geo.github.io/geologia-ML-dominios-alteracion](https://jhon21geo.github.io/geologia-ML-dominios-alteracion/).[^url]

[^url]: La dirección `jhonatanmallma.github.io/...` no corresponde a este repositorio (muestra 404).
