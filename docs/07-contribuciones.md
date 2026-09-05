# Opiniones y contribuciones

El objetivo de publicar el método con datos sintéticos es que **otras personas
puedan discutirlo y llevarlo a sus proyectos** sin pedir acceso a una unidad.

!!! tip "Antes de opinar"
    Conviene haber visto [cómo se asignan los dominios](03-asignacion-dominios.md)
    y, si puedes, haber corrido [Orange o Colab](09-orange-colab.md). Así la
    crítica apunta al método y no a un malentendido de k=5 vs seis dominios.

## Canales

| Quiero… | Dónde |
| --- | --- |
| Criticar k=5, los seis dominios o el SVM | [Issue de opinión](https://github.com/jhon21geo/geologia-ML-dominios-alteracion/issues/new?template=opinion.yml) |
| Contar una replicación | [Issue de replicación](https://github.com/jhon21geo/geologia-ML-dominios-alteracion/issues/new?template=replicacion.yml) |
| Reportar un error de código | [Issue de error](https://github.com/jhon21geo/geologia-ML-dominios-alteracion/issues/new?template=bug.yml) |
| Enviar código | Pull request (ver [CONTRIBUTING.md](https://github.com/jhon21geo/geologia-ML-dominios-alteracion/blob/main/CONTRIBUTING.md)) |

## Cómo probar el método si no programas

Orange (lienzo) o Google Colab:
https://jhon21geo.github.io/geologia-ML-dominios-alteracion/09-orange-colab/

## Qué es útil en una opinión

- ¿El dendrograma de *minerales* aporta algo que no dé K-Means sobre muestras?
- ¿Conviene un séptimo dominio (p. ej. sílice vuggy) aunque SWIR no vea cuarzo?
- ¿La profundidad máxima 4 y 10 árboles del RF publicado son un artefacto de
  Orange o una regularización deseable?
- ¿Hay que agrupar sondajes en la partición train/test?

## Código de conducta

La discusión es técnica y sobre datos sintéticos o resultados anonimizados.
No se aceptan tablas de operaciones ni identificación de unidades productivas.
Detalles en el [código de conducta](https://github.com/jhon21geo/geologia-ML-dominios-alteracion/blob/main/CODE_OF_CONDUCT.md).
