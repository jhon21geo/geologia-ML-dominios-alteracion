# Capítulo II. Marco teórico (condensado)

## 2.1 Epitermales de alta sulfuración

Los sistemas HS son hidrotermales someros (< 1,5 km), ligados a magmatismo
calco-alcalino, con fluidos ácidos, oxidantes y ricos en SO₂. La mineralización
típica es Au (a menudo refractario) y sulfuros de alta sulfuración
(enargita–luzonita), pirita y, en menor medida, covelina/digenita (Sillitoe,
1993; Corbett & Leach, 1998).

La condensación de SO₂ produce ácido sulfúrico y un *lithocap* de alunita,
caolinita, dickita, pirofilita y sílice vuggy. La zonación vertical clásica:

| Nivel | Ensamble |
| --- | --- |
| Superficial (*lithocap*) | Sílice vuggy, alunita, caolinita, dickita, pirofilita |
| Intermedio | Ilita–esmectita, dickita + cuarzo → sericita |
| Profundo / raíz porfíria | Cuarzo–sericita–pirita, enargita–luzonita |

### Asociaciones favorables a mineralización

- **Óxidos / supérgeno:** goethita, hematita, jarosita, alunita secundaria;
  buena respuesta a lixiviación.
- **Alunita–dickita–caolinita:** transiciones de litocap; K-alunita sugiere
  fluido magmático y cercanía al centro.
- **Sílice vuggy + pirita aurífera:** núcleo de lixiviación ácida.
- **Brechas con sílice + pirita:** conductos permeables.
- **Enargita–luzonita:** raíz HS, a veces conectada a pórfido Cu–Au.

SWIR no “ve” cuarzo ni sulfuros; por eso la sílice vuggy y la potásica quedan
ciegas en TerraSpec y deben inferirse con geoquímica, logueo o VNIR de óxidos.

## 2.2 Espectrometría SWIR/VNIR

El TerraSpec 4 registra reflectancia VNIR–SWIR. Ausspec (u otro unmixer)
devuelve scores 0–100 y minerales dominantes. Rasgos diagnósticos (Pontual,
2013):

| Enlace | nm | Minerales |
| --- | --- | --- |
| Al–OH | 2160–2220 | alunita, pirofilita, caolinita, ilita |
| Fe–OH | 2230–2295 | clorita férrica |
| Mg–OH / CO₃ | 2300–2360 | clorita, carbonato, epidota |
| OH / H₂O | ~1400, ~1900 | micas, caolinita, sílice hidratada |

Firmas de referencia (Tabla 7 de la tesis): alunita ~2160 nm; pirofilita
~2166 nm; caolinita ~2208 nm; ilita ~2200 nm; clorita ~2250 nm; epidota
~2330–2340 nm.

## 2.3 Aprendizaje automático usado

**No supervisado.** PCA reduce dimensión; el dendrograma (Ward) agrupa
minerales por perfil; K-Means parte *muestras* con k tomado del dendrograma
(aquí k = 5).

**Supervisado.** Se etiquetan tramos (`MOD_ALT`) y se predice con geoquímica:

- **Random Forest:** votos de árboles con submuestreo de atributos (Breiman,
  2001). Robusto a no linealidad y a mezcla de unidades (% y ppm).
- **k-NN:** vecinos en el espacio Z-score; sensible a escala y a clases raras.
- **MLP:** perceptrón de una capa oculta (ReLU, Adam).
- **SVM:** margen máximo con kernel RBF; frágil si no converge o si las clases
  no son separables con el C publicado.

**Métricas.** Matriz de confusión, precisión, recall, F1, ROC y AUC
one-vs-rest. En dominios desbalanceados el F1 macro y el recall de Arg/Pro
importan más que la exactitud global.

## 2.4 De la etiqueta al modelo 3D

Los intervalos predichos (`holeid`, from–to, dominio) entran a modelamiento
implícito (Leapfrog u otro). Un *back-flag* contra contactos > 90 % de
coincidencia espacial fue el criterio de la tesis para dar por estable el
sólido 3D.
