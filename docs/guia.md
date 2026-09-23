---
hide:
  - toc
---

# Cómo leer este visor

Versión condensada de la tesis para lectura en línea: problema de investigación,
criterio de asignación de dominios y selección del clasificador. El
[PDF (págs. 1–151)](tesis-pdf.md) conserva el texto original.

La forma más directa de **probar** el método es la réplica en el navegador:
[geoia.site/dominios-ml](https://geoia.site/dominios-ml/) (Fase 1 firma
`MOD_ALT`, Fase 2 lienzo Orange, Fase 3 predice el 60 % ciego). Los
[cuadernos](09-orange-colab.md) hacen lo mismo con los hiperparámetros de la
tesis.

!!! abstract "Lectura mínima"
    1. [Réplica GeoIA](10-geoia-dominios.md) — recorrer las tres fases.
    2. [Resumen](00-resumen.md) — formulación y resultados.
    3. [Asignación de dominios](03-asignacion-dominios.md) — clúster espectral frente a `MOD_ALT`.
    4. [Resultados](04-modelamiento-ml.md) — Random Forest frente a SVM, k-NN y MLP.

## Qué página responde a qué

| Si te preguntas… | Ve a |
| --- | --- |
| ¿Puedo verlo funcionar ahora, sin instalar nada? | [GeoIA · Dominios ML](https://geoia.site/dominios-ml/) |
| ¿Cómo se mapean las fases de GeoIA a la tesis? | [Réplica en el navegador](10-geoia-dominios.md) |
| ¿De qué trata la tesis, en una página? | [Resumen y abstract](00-resumen.md) |
| ¿Por qué hace falta ML en alteración? | [Introducción](00b-introduccion-tesis.md) y [planteamiento](01-introduccion.md) |
| ¿Qué es un sistema HS y qué ve el SWIR? | [Marco teórico](02-marco-teorico.md) |
| ¿Cuáles son las seis etapas del flujo? | [Metodología](02-metodologia.md) |
| ¿El K-Means *es* el dominio? **No.** | [El geólogo asigna los dominios](03-asignacion-dominios.md) |
| ¿Qué minerales y elementos se usaron? | [Espectro y geoquímica](03-analisis-espectral.md) |
| ¿Quién gana: RF, red, k-NN o SVM? | [Resultados de ML](04-modelamiento-ml.md) |
| ¿Qué se concluye y qué se recomienda? | [Conclusiones](05-conclusiones.md) |
| ¿Quiero Orange, Colab o los cuadernos 01–03? | [Orange, Colab y cuadernos](09-orange-colab.md) |
| ¿Puedo pegarlo a mis sondajes en Python? | [Replicar en Python](06-replicacion.md) |

## Orden recomendado (no es el de los capítulos)

```mermaid
flowchart TD
  A[Resumen] --> B[Asignación de dominios]
  B --> C[Metodología]
  C --> D[Resultados]
  D --> E{¿Quieres profundidad?}
  E -->|Sí| F[Introducción, marco, espectro]
  E -->|Probar| G[GeoIA / Colab / Orange]
  F --> H[PDF págs. 1–151]
```

Los capítulos 1, 2 y 4 (planteamiento, marco, espectro) son **fondo**. Sirven
cuando ya tienes clara la distinción clúster ≠ dominio.

## Tres avisos para no mezclar cifras

1. **Dato de la tesis** (Orange, calibración real), **dato de este repo**
   (scikit-learn, sintético) y **GeoIA** (implementación en el navegador) no
   se promedian. El ranking cualitativo sí se reproduce: Random Forest primero,
   SVM último.
2. K-Means usa **k = 5** sobre scores minerales. Los dominios geológicos son
   **seis** (`Arg`, `ArgAvd`, `Fil`, `Oxd`, `Pro`, `Sk`) porque el geólogo
   nombra ensambles, no números de clúster. En GeoIA el polígono sobre el PCA
   es esa firma.
3. El visor omite geometría y logística de la unidad. El análogo geológico es
   un epitermal Au–Cu de alta sulfuración con transición a pórfido/skarn.
   GeoIA reserva **40 % / 60 % de collares**; la tesis partió 80/20 sobre
   tramos ya etiquetados.

<div class="siguiente" markdown>

**Siguiente:** [Resumen y abstract](00-resumen.md) — el argumento de la tesis
en dos idiomas.

</div>
