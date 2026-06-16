---
title: "Clustering y Aprendizaje No Supervisado"
---

## Diapositiva 1

**Portada**

- Clustering y aprendizaje no supervisado
- Geometría, espacio de mezclas y criterios de partición
- Ciencia de Datos
- FaMAF
- Clase 16 - 2026-05-26

## Diapositiva 2. Plan de la Clase

1. **Transición: de predicción a estructura**
2. **Geometría y medidas de similitud**
   - Criterios de partición
3. **Formulación probabilística**
   - Mezclas e identificabilidad
   - Máxima verosimilitud para mezclas
   - Aplicación a mezclas normales

## Diapositiva 3

![Campo estelar usado como motivación para estructura no supervisada](figures/clase-16/fig-03-star-field.png){width=100%}

## Diapositiva 4

![Secuencia espectral estelar sobre el campo de estrellas](figures/clase-16/fig-04-spectral-sequence.png){width=100%}

## Diapositiva 5. Desarrollo de la Secuencia de Harvard (reinterpretado)

**1863-1867.** Angelo Secchi comienza a **clasificar** estrellas según la morfología global de sus espectros. Analiza algunos cientos de estrellas y define 4 clases principales utilizando color, intensidad y estructura de líneas espectrales, sin conocer aún la física subyacente.

**1872-1882.** Henry Draper impulsa el uso sistemático de la espectroscopía fotográfica estelar. Obtiene algunos de los primeros espectros fotografiados de estrellas, sentando las bases para la construcción de grandes **catálogos** espectrales.

**1886-1890.** En el Observatorio de Harvard, Edward Pickering y Williamina Fleming desarrollan un **esquema sistemático de clasificación** espectral basado principalmente en la apariencia de las líneas de absorción, especialmente las de hidrógeno. El proyecto comienza a escalar hacia decenas de miles de espectros.

**1890.** Fleming publica una clasificación para $\sim 10^4$ estrellas del *Henry Draper Catalogue*. Las clases $A,B,C,\ldots$ quedan esencialmente ordenadas por la prominencia de ciertas líneas espectrales, especialmente las de $H$, lo que retrospectivamente puede interpretarse como una organización dominada por una **variable principal**.

**1897.** Antonia Maury analiza espectros de alta resolución de 681 estrellas brillantes y muestra que la intensidad de $H$ no basta para describir completamente la variabilidad observada. Introduce subclases basadas en la anchura y estructura fina de las líneas, sugiriendo la existencia de nuevas **variables latentes**.

**1901-1915.** Annie Jump Cannon clasifica más de $2\times 10^5$ estrellas y reorganiza el sistema de Harvard en la secuencia:

$$
O - B - A - F - G - K - M
$$

mostrando que los espectros estelares se distribuyen aproximadamente a lo largo de un continuo, lo que hoy reinterpretamos como una **variedad unidimensional** en un espacio espectral de alta dimensión.

**1925.** Cecilia Payne demuestra que la secuencia espectral no refleja principalmente diferencias de composición química, sino una dependencia dominante con la temperatura superficial $T$. La principal **variable latente física** detrás de la distribución espectral queda finalmente identificada.

## Diapositiva 6

![Diagrama de Hertzsprung-Russell como ejemplo de estructura latente](figures/clase-16/fig-06-hr-diagram.png){width=90%}

## Diapositiva 7. Desarrollo de la Secuencia de Harvard (reinterpretado)

Dado un conjunto de espectros estelares observados $\mathcal{D}=\{x_i(\lambda)\}_{i=1}^N$, donde cada estrella queda representada por una función de intensidad sobre la longitud de onda, el problema consiste en descubrir estructura sin disponer de etiquetas físicas (temperatura, masa, edad, etc.).

1. **Representación y extracción de características**

   Pasar de placas fotográficas a representaciones numéricas $x_i\in\mathbb{R}^d$ donde cada componente describe intensidades, líneas de absorción, anchuras espectrales o índices de color. Cada estrella es un punto en un espacio de alta dimensión.

2. **Clustering y organización morfológica**

   Identificar grupos naturales de espectros con morfología similar. Las primeras clases espectrales $(A,B,C,\ldots)$ eran una partición empírica del espacio de observaciones basada únicamente en similitud espectral. Antes de comprender la física subyacente, se habían detectado regularidades estadísticas en los datos.

3. **Descubrimiento de variables latentes**

   La aparición de secuencias continuas y subclases revela que los espectros no ocupan arbitrariamente el espacio $\mathbb{R}^d$. Los datos parecen concentrarse cerca de una estructura de baja dimensión: $x_i\approx f(z_i)$ donde $z_i$ representa un pequeño conjunto de variables físicas ocultas. La secuencia espectral emerge como una parametrización aproximadamente unidimensional gobernada principalmente por la temperatura superficial.

4. **Aprendizaje de variedades**

   La Secuencia Principal sugiere que la distribución estelar se concentra cerca de una variedad inmersa: $\mathcal{M}\subset\mathbb{R}^d$. Aunque los espectros viven en un espacio de muy alta dimensión, la dinámica física impone fuertes restricciones estructurales sobre los estados posibles de las estrellas.

## Diapositiva 8. Desarrollo de la Secuencia de Harvard (reinterpretado)

**Objetivo**

Descubrir la geometría oculta generada por un sistema físico.

La evolución histórica de la clasificación espectral muestra que el orden en los datos frecuentemente precede a la teoría física que lo explica. Primero aparecen regularidades geométricas y agrupamientos; luego emergen las variables latentes y finalmente las leyes físicas que generan la distribución observada.

Una vez comprendidos los procesos físicos, la geometría de los datos se vuelve interpretable y útil para tareas de predicción (con métodos supervisados), modelado y simulación.

## Diapositiva 9. Desarrollo de Otros Problemas

Historias similares se repiten en otras áreas de la ciencia, como la biología, la química, la lingüística, etc., donde el análisis de datos no etiquetados ha sido crucial para descubrir estructura y generar conocimiento.

| Disciplina / autor | Espacio de observación ($x$) | Estructura latente intuidita | Equivalente algorítmico moderno |
| --- | --- | --- | --- |
| Lingüística (Harris / Firth) | Co-ocurrencia de palabras en ventanas de texto continuas. | Espacio semántico continuo basado en vecindad contextual. | *Word embeddings* / reducción de dimensionalidad semántica. |
| Petrología (Bowen) | Concentración de óxidos y compuestos minerales. | Trayectorias termodinámicas continuas (líneas de evolución). | Aprendizaje de variedades no lineales (*manifold learning* / *principal curves*). |
| Ecología (Whittaker) | Vectores de abundancia de especies por sitio geográfico. | Gradientes ambientales subyacentes (humedad, altitud). | Análisis de componentes principales (PCA) y escalamiento multidimensional (MDS). |

En todos estos casos, la lección para la Ciencia de Datos es idéntica a la que nos legó la Secuencia de Harvard: **la alta dimensionalidad observada suele ser una manifestación redundante de un espacio intrínseco mucho más simple y compacto**.

## Diapositiva 10. Transición: de Predicción a Estructura

**Sección:** Transición: de predicción a estructura.

## Diapositiva 11. Extensión del Enfoque Geométrico

Hasta ahora usamos datos etiquetados:

$$
\mathcal{D}_n=\{(x_i,y_i)\}_{i=1}^n,
\qquad
y_i\in\{1,\ldots,c\}.
$$

El objetivo explícito era predecir:

$$
\hat{g}:\mathcal{X}\to\mathcal{Y},
\qquad
\hat{g}(x)\approx y.
$$

En aprendizaje **no supervisado** observamos solamente

$$
\mathcal{D}_n=\{x_1,\ldots,x_n\},
\qquad
x_i\in\mathbb{R}^d.
$$

La pregunta deja de ser "¿cuál es la etiqueta?" y pasa a ser:

**¿Qué estructura regular tiene la distribución que generó los datos?**

Los métodos aprendían una **geometría**:

- discriminantes lineales: **hiperplanos** y métricas cuadráticas;
- árboles: particiones rectangulares del **espacio**;
- ensambles: promedios de **particiones** inestables;
- redes: **representaciones** internas donde las clases se separan.

Formas de **estructura**:

- **grupos o clases latentes**;
- variables redundantes y subespacios de baja dimensión;
- modos de densidad;
- observaciones atípicas;
- representaciones útiles para una tarea posterior.

## Diapositiva 12. De Similitud Supervisada a Similitud No Supervisada

En clasificación, las etiquetas inducen una noción de similitud:

$$
x_i\sim x_j
\qquad
\text{si ayudan a predecir la misma } y.
$$

Sin etiquetas, la similitud debe ser **introducida o inferida** a partir de:

- geometría en el espacio de variables;
- densidad de probabilidad;
- conectividad local;
- estabilidad de una partición;
- una representación latente.

Esto se traduce en:

$$
x_i\sim x_j
\quad
\text{si } d(x_i,x_j) \text{ es pequeño},
$$

es decir, determinar cuándo los datos comparten vecindad, densidad, conectividad, representación, etc., a partir de medidas de distancia.

**Clustering**

Un algoritmo de clustering no descubre grupos en abstracto: descubre grupos respecto de una representación, una escala y un criterio.

## Diapositiva 13. De Similitud Supervisada a Similitud No Supervisada

Razones estadísticas y prácticas para identificar grupos de datos:

- Etiquetar grandes volúmenes de datos puede ser **costoso, lento o ambiguo**.
- Puede ser preferible **aprender primero** regularidades sobre datos no etiquetados y etiquetar después los grupos hallados.
- Clases conocidas pueden contener **subclases** relevantes.
- La distribución de los patrones puede **cambiar** lentamente en el tiempo y requerir adaptación.
- Los métodos no supervisados pueden actuar como **extracción de rasgos** o **preprocesamiento** dependiente de los datos.
- En una **etapa exploratoria**, interesa comprender estructura, subclases, similitudes o desviaciones importantes.

## Diapositiva 14. Dos Niveles del Problema

Distinguimos dos formulaciones:

**A. Enfoque probabilístico.**

Suponer que los datos provienen de una mezcla de distribuciones y estimar los parámetros desconocidos.

Esta formulación es más estructurada y matemática:

$$
p(x)=
\sum_{j=1}^{c}
\pi_j p(x\mid \omega_j,\theta_j).
$$

Muestras no etiquetadas $\Rightarrow$ estimar estructura probabilística o particiones.

![Enfoque probabilístico: mezcla de densidades y superficie de verosimilitud](figures/clase-16/fig-14-probabilistic-mixture.png){width=65%}

## Diapositiva 15. Dos Niveles del Problema

Distinguimos dos formulaciones:

**B. Enfoque algorítmico.**

Reformular el problema como una partición de la muestra en subconjuntos "coherentes" o clusters conduce a procedimientos efectivos aun cuando la teoría probabilística sea incompleta.

![Cuatro enfoques algorítmicos de clustering](figures/clase-16/fig-15-clustering-formulations.png){width=90%}

## Diapositiva 16. Clustering vs. Clasificación

| | Clasificación | Clustering |
| --- | --- | --- |
| Datos | $(x_i,y_i)$ | $x_i$ |
| Salida | regla $\hat{g}(x)$ | partición o asignación blanda |
| Criterio | riesgo predictivo | compacidad, densidad, grafo |
| Validación | error en test | estabilidad, índice, interpretación |
| Ambigüedad | menor | estructural |

![Comparación visual entre clasificación y clustering](figures/clase-16/fig-16-classification-vs-clustering.png){width=85%}

El número de clases suele estar dado en clasificación; pero en clustering es parte del problema.

## Diapositiva 17. Geometría y Medidas de Similitud

**Sección:** Geometría y medidas de similitud.

## Diapositiva 18. Antes del Algoritmo: el Espacio

Intuitivamente los elementos de un mismo grupo deben ser "cercanos" entre sí, y alejados de los de otros grupos.

Una representación de los datos es una función que asigna a cada objeto un vector de características numéricas:

$$
x_i \mapsto (x_i)_1,\ldots,(x_i)_d.
$$

La representación determina qué significa "cerca": es necesario definir una medida de **similitud o distancia entre objetos**, que a su vez define la geometría del espacio de datos.

Por ejemplo, si $x=(x_1,\ldots,x_d)$ mezcla unidades distintas, la distancia euclídea puede ser arbitraria:

$$
\|x_i-x_j\|^2
=
\sum_{k=1}^d
(x_{ik}-x_{jk})^2.
$$

Cambiar metros por centímetros cambia la contribución de esa coordenada.

Por eso el preprocesamiento define el problema estadístico; no es "solo cosmético".

## Diapositiva 19. Distancia Euclídea

$$
d_E(x,x')
=
\|x-x'\|_2.
$$

Propiedades:

- invariante a traslaciones y rotaciones;
- no invariante a reescalamientos de coordenadas;
- favorece grupos esféricos en la escala usada;
- muy usada por eficiencia computacional.

Si se usa Euclídea, conviene preguntarse:

$$
x_k
\leftarrow
\frac{x_k-\bar{x}_k}{s_k}
\qquad
\text{antes de clusterizar?}
$$

## Diapositiva 20. Distancia de Mahalanobis

Si $\Sigma$ representa escala y correlación,

$$
d_M^2(x,x')
=
(x-x')^t\Sigma^{-1}(x-x').
$$

Equivale a distancia euclídea luego de blanquear:

$$
z
=
\Sigma^{-1/2}(x-\mu).
$$

Precaución:

- blanquear con la covarianza total puede destruir separación entre grupos;
- estimar $\Sigma$ en alta dimensión puede ser inestable;
- una métrica global no captura escalas locales distintas.

## Diapositiva 21. Similitud No Métrica

A veces interesa una afinidad $s(x,x')$ grande cuando dos objetos son parecidos.

Coseno:

$$
s_{\cos}(x,x')
=
\frac{x^t x'}{\|x\|\|x'\|}.
$$

Para atributos binarios, coeficiente de Tanimoto/Jaccard:

$$
s_J(x,x')
=
\frac{x^t x'}{x^t x + x'^t x' - x^t x'}.
$$

El clustering de textos, usuarios o moléculas suele empezar por esta decisión.

## Diapositiva 22. Matrices de Distancia y Afinidad

Muchos algoritmos sólo necesitan

$$
D_{ij}=d(x_i,x_j)
\qquad
\text{o}
\qquad
W_{ij}=s(x_i,x_j).
$$

Ejemplos:

$$
W_{ij}
=
\exp\left(
-\frac{\|x_i-x_j\|^2}{2\sigma^2}
\right),
\qquad
W_{ij}
=
\mathbb{I}\{x_j\in k\text{-NN}(x_i)\}.
$$

Elegir $\sigma$ o $k$ decide si el grafo ve estructura local o global.

Ver:

- notebook: `distancias_similitud_escalamiento_no_supervisado.ipynb`
- exploración interactiva

## Diapositiva 23. La Maldición de la Dimensionalidad

En alta dimensión, las distancias tienden a concentrarse.

Si las coordenadas son independientes y comparables,

$$
\|x_i-x_j\|^2
=
\sum_{k=1}^d
(x_{ik}-x_{jk})^2
$$

tiene media y varianza que crecen con $d$, pero el coeficiente de variación suele decrecer.

Consecuencias:

- el vecino más cercano deja de ser muy distinto del más lejano;
- aparecen variables irrelevantes que dominan el criterio;
- PCA, selección de variables o *embeddings* pueden ser necesarios.

![Concentración de distancias al aumentar la dimensión](figures/clase-16/fig-23-distance-concentration.png){width=70%}

## Diapositiva 24. La Estandarización No Siempre Alcanza

Estandarizar coordenadas resuelve unidades pero no semántica.

Preguntas prácticas:

- ¿las variables numéricas son comparables?
- ¿hay variables ordinales o categóricas?
- ¿hay *outliers* que inflan la escala?
- ¿la similitud debe ser global o local?
- ¿la representación fue aprendida para otra tarea?

En aprendizaje no supervisado, estas decisiones no se pueden delegar a una métrica de error predictivo, y requieren análisis previo.

## Diapositiva 25. Partición Dura

Buscamos $c$ subconjuntos disjuntos:

$$
\mathcal{D}
=
\mathcal{D}_1\cup\cdots\cup\mathcal{D}_c,
\qquad
\mathcal{D}_i\cap\mathcal{D}_j=\emptyset.
$$

Equivalente: asignaciones

$$
r_{ij}\in\{0,1\},
\qquad
\sum_{j=1}^{c} r_{ij}=1.
$$

El centroide del cluster $j$ es

$$
\mu_j
=
\frac{1}{n_j}
\sum_{i:r_{ij}=1} x_i,
\qquad
n_j
=
\sum_i r_{ij}.
$$

Ahora falta un criterio para comparar particiones.

## Diapositiva 26. Criterio de Suma de Cuadrados

El criterio más usado:

$$
J_e
=
\sum_{j=1}^{c}
\sum_{x_i\in\mathcal{D}_j}
\|x_i-\mu_j\|^2.
$$

Interpretación:

- representar cada punto por el centroide de su grupo;
- minimizar el error cuadrático total de cuantización;
- buscar clusters compactos de varianza pequeña.

Se lo llama criterio de mínima varianza intra-cluster.

## Diapositiva 27. Motivación Formal del Problema

En el aprendizaje no supervisado (Clustering Particional), carecemos de etiquetas de clase a priori. Buscamos una partición óptima del espacio de características $\mathbb{R}^d$ en $c$ subconjuntos discretos y disjuntos, denotados como particiones lógicas $\mathcal{D}=\{\mathcal{D}_1,\mathcal{D}_2,\ldots,\mathcal{D}_c\}$.

Para fundamentar un algoritmo matemático de optimización elemental, es un requisito previo definir métricas globales sobre la **cohesión interna** de los grupos y su **separabilidad mutua**.

![Cohesión interna y separabilidad mutua entre clusters](figures/clase-16/fig-27-cohesion-separability.png){width=70%}

Demostraremos formalmente que la minimización de la varianza interna (el criterio estándar de traza) es algebraicamente equivalente a la maximización de la dispersión inter-cluster.

## Diapositiva 28. Trazas

![Visualización interactiva de trazas intra-cluster e inter-cluster](figures/clase-16/fig-28-traces.png){width=90%}

Ver: `trazas.html`.

## Diapositiva 29. Definiciones

Sea un conjunto de datos $\mathcal{X}=\{x_1,x_2,\ldots,x_n\}$ donde cada observación $x_k\in\mathbb{R}^d$. Sea $n_i=|\mathcal{D}_i|$ el cardinal de la partición $i$.

**Definición: vector de media global y local**

El vector de media global $\mu$ y el vector de media del cluster $\mathcal{D}_i$ (denotado como $\mu_i$) se definen respectivamente como:

$$
\mu
=
\frac{1}{n}
\sum_{k=1}^{n}
x_k,
\qquad
\mu_i
=
\frac{1}{n_i}
\sum_{x\in\mathcal{D}_i} x.
$$

**Definición: matriz de dispersión total**

La dispersión total del espacio muestral sin particionar se denota por:

$$
S_T
=
\sum_{k=1}^{n}
(x_k-\mu)(x_k-\mu)^T.
$$

## Diapositiva 30. Formulación de Matrices Intra-clase y Inter-clase

En consistencia con la notación multidimensional de Duda, Hart & Stork (Capítulo 10), definimos los operadores matriciales estructurales de la partición.

**Definición: matriz de dispersión intra-cluster (*within-cluster*)**

$$
S_W
=
\sum_{i=1}^{c}
S_i
=
\sum_{i=1}^{c}
\sum_{x\in\mathcal{D}_i}
(x-\mu_i)(x-\mu_i)^T.
$$

**Definición: matriz de dispersión entre-clusters (*between-cluster*)**

$$
S_B
=
\sum_{i=1}^{c}
n_i(\mu_i-\mu)(\mu_i-\mu)^T.
$$

Ambas matrices $S_W,S_B,S_T\in\mathbb{R}^{d\times d}$ son simétricas y semidefinidas positivas.

## Diapositiva 31. Derivación Paso a Paso

**Teorema: descomposición fundamental de dispersión**

Para cualquier partición válida $\mathcal{D}$ del conjunto de datos $\mathcal{X}$, se verifica la siguiente descomposición aditiva:

$$
S_T=S_W+S_B.
$$

Comenzamos reescribiendo el término de la dispersión total $S_T$ expandiendo cada observación mediante el elemento neutro sumando y restando la media local $\mu_i$:

$$
S_T
=
\sum_{i=1}^{c}
\sum_{x\in\mathcal{D}_i}
(x-\mu)(x-\mu)^T.
$$

$$
S_T
=
\sum_{i=1}^{c}
\sum_{x\in\mathcal{D}_i}
\left[(x-\mu_i)+(\mu_i-\mu)\right]
\left[(x-\mu_i)+(\mu_i-\mu)\right]^T.
$$

## Diapositiva 32. Derivación Paso a Paso

Aplicando la propiedad distributiva del producto externo vectorial, la expresión se descompone en tres sumas independientes:

$$
\begin{aligned}
S_T
&=
\sum_{i=1}^{c}
\sum_{x\in\mathcal{D}_i}
(x-\mu_i)(x-\mu_i)^T
\quad \to \text{Término 1}
\\
&\quad+
\sum_{i=1}^{c}
\sum_{x\in\mathcal{D}_i}
(\mu_i-\mu)(\mu_i-\mu)^T
\quad \to \text{Término 2}
\\
&\quad+
2\sum_{i=1}^{c}
\sum_{x\in\mathcal{D}_i}
(x-\mu_i)(\mu_i-\mu)^T
\quad \to \text{Término Cruzado}.
\end{aligned}
$$

Analicemos individualmente el Término Cruzado:

$$
\mathrm{TC}
=
2
\sum_{i=1}^{c}
\left[
\sum_{x\in\mathcal{D}_i}
(x-\mu_i)
\right]
(\mu_i-\mu)^T.
$$

## Diapositiva 33. Derivación Paso a Paso

Por definición analítica del vector de media condicional de la partición $\mu_i$:

$$
\sum_{x\in\mathcal{D}_i}x
=
n_i\mu_i
\quad\Rightarrow\quad
\sum_{x\in\mathcal{D}_i}(x-\mu_i)
=
n_i\mu_i-n_i\mu_i
=
0.
$$

Por consiguiente, el término cruzado se anula idénticamente $(\mathrm{TC}=0)$.

Evaluando ahora el Término 2, dado que $(\mu_i-\mu)$ no depende del índice interno de la sumatoria sobre las observaciones de $\mathcal{D}_i$:

$$
\sum_{i=1}^{c}
\sum_{x\in\mathcal{D}_i}
(\mu_i-\mu)(\mu_i-\mu)^T
=
\sum_{i=1}^{c}
n_i(\mu_i-\mu)(\mu_i-\mu)^T
=
S_B.
$$

Sustituyendo el Término 1 $(S_W)$ y el Término 2 $(S_B)$ se concluye:

$$
S_T=S_W+S_B.
$$

## Diapositiva 34. Equivalencia en la Traza

El operador lineal traza $(\operatorname{tr}(\cdot))$ es invariante ante permutaciones y representa la suma de los elementos de la diagonal (la varianza escalar totalizada del espacio):

$$
\operatorname{tr}(S_T)
=
\operatorname{tr}(S_W)
+
\operatorname{tr}(S_B).
$$

Dado que $\mathcal{X}$ está fijo desde el inicio del muestreo, $S_T$ y su traza $\operatorname{tr}(S_T)$ actúan como constantes invariantes ante cualquier cambio en la asignación de las particiones. Por lo tanto:

**Principio de dualidad del clustering**

$$
\arg\min_{\mathcal{D}}
\operatorname{tr}(S_W)
\equiv
\arg\max_{\mathcal{D}}
\operatorname{tr}(S_B).
$$

Minimizar la suma de distancias cuadráticas internas de las observaciones a sus prototipos locales ($J_e$ en K-means) es analíticamente equivalente a maximizar la dispersión e isolación mutua de los centroides inter-cluster en el espacio lineal.

## Diapositiva 35. Formulación Probabilística

**Sección:** Formulación probabilística.

## Diapositiva 36. Tres Objetos Matemáticos

Vamos a alternar entre tres formalizaciones:

1. **Modelo generativo:** una mezcla

$$
p(x)
=
\sum_{j=1}^{c}
\pi_j p(x\mid\omega_j,\theta_j).
$$

2. **Partición:** subconjuntos disjuntos

$$
\mathcal{D}
=
\mathcal{D}_1\cup\cdots\cup\mathcal{D}_c,
\qquad
\mathcal{D}_i\cap\mathcal{D}_j=\emptyset.
$$

3. **Grafo:** nodos $x_i$ y aristas que codifican vecindad o afinidad.

Cada formalización produce algoritmos y criterios distintos.

## Diapositiva 37. Variables Latentes de Clase

Supongamos que cada observación tiene una clase latente

$$
z_i\in\{1,\ldots,c\},
\qquad
\mathbb{P}(z_i=j)=\pi_j.
$$

Condicionalmente a $z_i=j$,

$$
x_i\mid z_i=j
\sim
p(x\mid\theta_j).
$$

El dato observado marginal tiene densidad:

$$
p(x\mid\theta,\pi)
=
\sum_{j=1}^{c}
\pi_j p(x\mid\theta_j),
\qquad
\sum_{j=1}^{c}\pi_j=1.
$$

La "etiqueta" ahora es una variable latente que se volvió no observada. En la formulación de las primeras clases, la variable latente $z_i$ es la clase $\omega_i$.

## Diapositiva 38. Hipótesis Paramétrica para Datos No Etiquetados

Consideramos el siguiente modelo:

1. Existe un número conocido $c$ de clases latentes.
2. Las probabilidades a priori $P(\omega_j)=\pi_j$ son conocidas.
3. Las densidades condicionales $p(x\mid\omega_j,\theta_j)$ tienen forma conocida.
4. Los parámetros $\theta_1,\ldots,\theta_c$ son desconocidos.
5. Las etiquetas de las muestras no se observan.

Si $\theta=(\theta_1,\ldots,\theta_c)$, la densidad marginal observada es

$$
p(x\mid\theta)
=
\sum_{j=1}^{c}
p(x\mid\omega_j,\theta_j)\pi_j.
$$

## Diapositiva 39. Densidades de Mezcla

La expresión

$$
p(x\mid\theta)
=
\sum_{j=1}^{c}
p(x\mid\omega_j,\theta_j)\pi_j
$$

define una **densidad de mezcla**.

Interpretación:

- $p(x\mid\omega_j,\theta_j)$: densidades componentes;
- $\pi_j=P(\omega_j)$: pesos o parámetros de mezcla;
- la generación de $x$ ocurre en dos etapas:

$$
\omega_j\sim\operatorname{Categorical}(\pi_1,\ldots,\pi_c),
$$

$$
x\mid\omega_j
\sim
p(x\mid\omega_j,\theta_j).
$$

Objetivo: estimar $\theta$ a partir de muestras no etiquetadas de $p(x\mid\theta)$.

![Densidad de mezcla como suma ponderada de componentes](figures/clase-16/fig-39-mixture-density.png){width=55%}

## Diapositiva 40. ¿Es Posible Recuperar la Estructura?

Antes de buscar un estimador, hay una cuestión lógica previa:

**Si con datos infinitos pudiéramos reconstruir exactamente $p(x\mid\theta)$, ¿sería posible recuperar unívocamente $\theta$?**

Si la respuesta es negativa, el problema es insoluble en principio, independientemente del algoritmo utilizado.

Esto motiva la noción de **identificabilidad**.

## Diapositiva 41. Definición de Identificabilidad

Una familia $p(x\mid\theta)$ es **identificable** si

$$
\theta\ne\theta'
\quad\Rightarrow\quad
\exists x \text{ tal que }
p(x\mid\theta)\ne p(x\mid\theta').
$$

Equivalentemente:

$$
p(x\mid\theta)
=
p(x\mid\theta')
\ \forall x
\quad\Rightarrow\quad
\theta=\theta'.
$$

Interpretación:

- la identificabilidad es una propiedad del *modelo*, no del estimador;
- si falla, pueden existir distintos parámetros que inducen exactamente la misma distribución observable;
- en ese caso, no hay forma de inferir una descomposición única a partir de datos no etiquetados.

En mezclas aparece una dificultad inevitable:

$$
\pi_1 p(x\mid\theta_1)
+
\pi_2 p(x\mid\theta_2)
=
\pi_2 p(x\mid\theta_2)
+
\pi_1 p(x\mid\theta_1).
$$

El cambio de nombres de componentes no cambia la densidad. Esto se llama *label switching*.

Más grave: puede haber no identificabilidad sustancial si distintas mezclas inducen la misma distribución marginal.

## Diapositiva 42. Ejemplo de No Identificabilidad Completa

Sea $x\in\{0,1\}$ y consideremos la mezcla

$$
P(x\mid\theta)
=
\frac{1}{2}\theta_1^x(1-\theta_1)^{1-x}
+
\frac{1}{2}\theta_2^x(1-\theta_2)^{1-x}.
$$

Entonces

$$
P(x=1\mid\theta)
=
\frac{\theta_1+\theta_2}{2},
\qquad
P(x=0\mid\theta)
=
1-\frac{\theta_1+\theta_2}{2}.
$$

Si observamos, por ejemplo, que

$$
P(x=1\mid\theta)=0.6,
$$

solo podemos concluir que

$$
\theta_1+\theta_2=1.2,
$$

pero no recuperar $\theta_1$ y $\theta_2$ por separado.

El modelo observable no determina la descomposición en componentes.

## Diapositiva 43. Observación sobre Mezclas Gaussianas

En distribuciones continuas, la identificabilidad suele ser menos problemática.

Por ejemplo, en una mezcla de gaussianas unidimensionales

$$
p(x\mid\theta)
=
\pi_1\phi(x;\mu_1,1)
+
\pi_2\phi(x;\mu_2,1),
$$

si $\pi_1=\pi_2$, el intercambio de $\mu_1$ y $\mu_2$ deja invariante la densidad:

$$
(\mu_1,\mu_2)
\mapsto
(\mu_2,\mu_1).
$$

Esto produce una ambigüedad de **etiquetado** de componentes.

**Convención práctica**

En lo que sigue se asume que la familia de mezclas considerada es identificable, salvo por simetrías triviales de permutación de etiquetas.

## Diapositiva 44. Muestra No Etiquetada y Verosimilitud

Sea

$$
\mathcal{D}
=
\{x_1,\ldots,x_n\}
$$

una muestra i.i.d. obtenida de

$$
p(x\mid\theta)
=
\sum_{j=1}^{c}
p(x\mid\omega_j,\theta_j)\pi_j.
$$

La verosimilitud es

$$
p(\mathcal{D}\mid\theta)
=
\prod_{k=1}^{n}
p(x_k\mid\theta),
$$

y el estimador de máxima verosimilitud es

$$
\hat{\theta}
=
\arg\max_{\theta}
p(\mathcal{D}\mid\theta).
$$

Trabajamos con la log-verosimilitud

$$
\ell(\theta)
=
\sum_{k=1}^{n}
\log p(x_k\mid\theta).
$$

## Diapositiva 45. Derivada de la Log-verosimilitud

Si derivamos $\ell$ respecto de $\theta_i$, obtenemos

$$
\nabla_{\theta_i}\ell
=
\sum_{k=1}^{n}
\frac{1}{p(x_k\mid\theta)}
\nabla_{\theta_i}
\left[
\sum_{j=1}^{c}
p(x_k\mid\omega_j,\theta_j)\pi_j
\right].
$$

Usando independencia funcional entre $\theta_i$ y $\theta_j$ para $i\ne j$, solo sobrevive la componente $i$:

$$
\nabla_{\theta_i}\ell
=
\sum_{k=1}^{n}
\frac{p(x_k\mid\omega_i,\theta_i)\pi_i}{p(x_k\mid\theta)}
\nabla_{\theta_i}
\log p(x_k\mid\omega_i,\theta_i).
$$

## Diapositiva 46. Posteriores Latentes y Ecuaciones Críticas

Definimos la probabilidad posterior de pertenencia a la clase $i$:

$$
P(\omega_i\mid x_k,\theta)
=
\frac{p(x_k\mid\omega_i,\theta_i)\pi_i}{p(x_k\mid\theta)}.
$$

Entonces

$$
\nabla_{\theta_i}\ell
=
\sum_{k=1}^{n}
P(\omega_i\mid x_k,\theta)
\nabla_{\theta_i}
\log p(x_k\mid\omega_i,\theta_i).
$$

Una condición necesaria para un máximo local $\hat{\theta}$ es

$$
\sum_{k=1}^{n}
P(\omega_i\mid x_k,\hat{\theta})
\nabla_{\theta_i}
\log p(x_k\mid\omega_i,\hat{\theta}_i)
=
0,
\qquad
i=1,\ldots,c.
$$

La forma es análoga al caso supervisado, pero con etiquetas reemplazadas por posteriores.

## Diapositiva 47. Cuando También Son Desconocidos los Pesos de Mezcla

Si $\pi_i=P(\omega_i)$ también es desconocido, debe satisfacerse

$$
\pi_i\ge 0,
\qquad
\sum_{i=1}^{c}\pi_i=1.
$$

En un máximo local interior, las ecuaciones necesarias toman la forma

$$
\hat{\pi}_i
=
\frac{1}{n}
\sum_{k=1}^{n}
P(\omega_i\mid x_k,\hat{\theta}),
$$

y

$$
\sum_{k=1}^{n}
P(\omega_i\mid x_k,\hat{\theta})
\nabla_{\theta_i}
\log p(x_k\mid\omega_i,\hat{\theta}_i)
=
0.
$$

Interpretación:

- $\hat{\pi}_i$ es la fracción promedio de pertenencia al componente $i$;
- cada parámetro $\hat{\theta}_i$ se ajusta usando observaciones ponderadas por esas pertenencias.

## Diapositiva 48. Mezclas Gaussianas como Caso Canónico

Supongamos

$$
p(x\mid\omega_i,\theta_i)
\sim
\mathcal{N}(\mu_i,\Sigma_i).
$$

Las incógnitas posibles son:

| Caso | $\mu_i$ | $\Sigma_i$ | $\pi_i$ |
| --- | --- | --- | --- |
| 1 | ? | conocidas | conocidos |
| 2 | ? | ? | ? |
| 3 | ? | ? | ? con $c$ desconocido |

El caso 1 es pedagógicamente limpio. El caso 2 es más realista. El caso 3 no puede resolverse por máxima verosimilitud estándar sin restricciones adicionales.

## Diapositiva 49. Caso 1: Medias Desconocidas, Covarianzas Conocidas

Para una normal multivariada,

$$
\log p(x\mid\omega_i,\mu_i)
=
-
\frac{d}{2}\log(2\pi)
-
\frac{1}{2}\log|\Sigma_i|
-
\frac{1}{2}
(x-\mu_i)^t
\Sigma_i^{-1}
(x-\mu_i).
$$

La derivada respecto de $\mu_i$ es

$$
\nabla_{\mu_i}
\log p(x\mid\omega_i,\mu_i)
=
\Sigma_i^{-1}(x-\mu_i).
$$

Sustituyendo en la ecuación crítica:

$$
\sum_{k=1}^{n}
P(\omega_i\mid x_k,\hat{\mu})
\Sigma_i^{-1}
(x_k-\hat{\mu}_i)
=
0.
$$

## Diapositiva 50. Caso 1: Fórmula de Actualización para las Medias

Reordenando términos se obtiene

$$
\hat{\mu}_i
=
\frac{
\sum_{k=1}^{n}
P(\omega_i\mid x_k,\hat{\mu})x_k
}{
\sum_{k=1}^{n}
P(\omega_i\mid x_k,\hat{\mu})
}.
$$

Interpretación:

- es una media muestral ponderada;
- el peso de $x_k$ es la probabilidad posterior de que provenga del componente $i$;
- si las pertenencias fueran 0 o 1, recuperaríamos la media habitual de cada grupo.

El problema es que la ecuación es implícita, porque los pesos dependen de las medias que deseamos estimar.

## Diapositiva 51. Caso 1: Esquema Iterativo

La ecuación anterior sugiere una iteración natural:

$$
\hat{\mu}_i^{(t+1)}
=
\frac{
\sum_{k=1}^{n}
P(\omega_i\mid x_k,\hat{\mu}^{(t)})x_k
}{
\sum_{k=1}^{n}
P(\omega_i\mid x_k,\hat{\mu}^{(t)})
}.
$$

Propiedades conceptuales:

- es un procedimiento de ascenso local sobre la log-verosimilitud;
- la convergencia depende del punto inicial;
- pueden existir múltiples máximos locales;
- si el modelo está mal especificado, la interpretación estadística se vuelve delicada.

Aquí aparece con claridad la dificultad central del clustering paramétrico: las variables latentes generan ecuaciones acopladas y no lineales.

## Diapositiva 52. Caso 2: Medias, Covarianzas y Pesos Desconocidos

Si todos los parámetros de cada componente son desconocidos, las ecuaciones de máximo local toman la forma

$$
\hat{\pi}_i
=
\frac{1}{n}
\sum_{k=1}^{n}
P(\omega_i\mid x_k,\hat{\theta}),
$$

$$
\hat{\mu}_i
=
\frac{
\sum_{k=1}^{n}
P(\omega_i\mid x_k,\hat{\theta})x_k
}{
\sum_{k=1}^{n}
P(\omega_i\mid x_k,\hat{\theta})
},
$$

$$
\hat{\Sigma}_i
=
\frac{
\sum_{k=1}^{n}
P(\omega_i\mid x_k,\hat{\theta})
(x_k-\hat{\mu}_i)(x_k-\hat{\mu}_i)^t
}{
\sum_{k=1}^{n}
P(\omega_i\mid x_k,\hat{\theta})
}.
$$

Son versiones ponderadas de:

- proporciones de clase,
- medias muestrales,
- matrices de covarianza.

## Diapositiva 53. Caso 2: La Dificultad de las Soluciones Singulares

En mezclas gaussianas completamente libres, la máxima verosimilitud global puede degenerar.

Idea del fenómeno:

- un componente puede ubicar su media exactamente sobre una observación $x_1$;
- su varianza puede colapsar hacia cero;
- la densidad en $x_1$ crece sin cota;
- por lo tanto, la verosimilitud total puede hacerse arbitrariamente grande.

Consecuencia:

**el máximo global puede ser singular y estadísticamente inútil.**

En la práctica se buscan máximos locales finitos o se imponen restricciones sobre covarianzas, regularización o parametrizaciones más rígidas.

## Diapositiva 54. Lección Conceptual del Enfoque por Mezclas

El modelo de mezcla aporta una semántica probabilística fuerte:

- un cluster es un componente generativo;
- la asignación puede ser blanda:

$$
\gamma_{ik}
=
P(\omega_i\mid x_k,\hat{\theta});
$$

- la estimación exige resolver un problema no convexo;
- la inferencia depende críticamente de supuestos paramétricos.

Esto explica por qué, históricamente, se desarrollaron métodos más simples de partición, menos ricos teóricamente pero muy útiles computacionalmente.

## Diapositiva 55. Mezclas Gaussianas

Sea

$$
p(x\mid z=j)
=
\mathcal{N}(x\mid\mu_j,\Sigma_j).
$$

Entonces

$$
p(x)
=
\sum_{j=1}^{c}
\pi_j
\frac{1}{(2\pi)^{d/2}|\Sigma_j|^{1/2}}
\exp\left\{
-
\frac{1}{2}
(x-\mu_j)^t
\Sigma_j^{-1}
(x-\mu_j)
\right\}.
$$

El clasificador Bayesiano inducido asigna

$$
\hat{z}(x)
=
\arg\max_j
\pi_j
\mathcal{N}(x\mid\mu_j,\Sigma_j).
$$

Clustering probabilístico: estimar los parámetros y luego asignar.

## Diapositiva 56. Medias Gaussianas Desconocidas

Si $\Sigma_j$ y $\pi_j$ son conocidas y sólo $\mu_j$ es desconocida,

$$
\nabla_{\mu_j}
\log\mathcal{N}(x_i\mid\mu_j,\Sigma_j)
=
\Sigma_j^{-1}(x_i-\mu_j).
$$

La condición de máximo da:

$$
\hat{\mu}_j
=
\frac{
\sum_{i=1}^{n}
\hat{\gamma}_{ij}x_i
}{
\sum_{i=1}^{n}
\hat{\gamma}_{ij}
}.
$$

Es la media muestral ponderada por pertenencia posterior.

## Diapositiva 57. EM

EM maximiza iterativamente una cota inferior de la log-verosimilitud.

**E-step:**

$$
\gamma_{ij}^{(t)}
=
P(z_i=j\mid x_i,\theta^{(t)},\pi^{(t)}).
$$

**M-step:**

$$
(\theta^{(t+1)},\pi^{(t+1)})
=
\arg\max_{\theta,\pi}
\sum_{i=1}^{n}
\sum_{j=1}^{c}
\gamma_{ij}^{(t)}
\log\{\pi_j p(x_i\mid\theta_j)\}.
$$

Garantía: la log-verosimilitud no decrece, pero puede converger a un óptimo local.

## Diapositiva 58. Actualizaciones Gaussianas

Defina $n_j=\sum_{i=1}^{n}\gamma_{ij}$. En una mezcla gaussiana general:

$$
\hat{\pi}_j
=
\frac{n_j}{n},
\qquad
\hat{\mu}_j
=
\frac{1}{n_j}
\sum_{i=1}^{n}
\gamma_{ij}x_i,
$$

$$
\hat{\Sigma}_j
=
\frac{1}{n_j}
\sum_{i=1}^{n}
\gamma_{ij}
(x_i-\hat{\mu}_j)(x_i-\hat{\mu}_j)^t.
$$

Estas son las versiones ponderadas de los estimadores supervisados.

La diferencia conceptual es que los pesos $\gamma_{ij}$ también son estimados.

## Diapositiva 59. Qué Aporta la Visión Probabilística

- Da probabilidades de pertenencia, no sólo etiquetas.
- Permite formas elipsoidales mediante $\Sigma_j$.
- Provee una verosimilitud para comparar modelos.

Pero:

- requiere especificar familia paramétrica;
- sufre con inicialización y óptimos locales;
- la verosimilitud puede degenerar si una covarianza colapsa;
- no todo grupo interpretable es un componente de mezcla.

## Diapositiva 60. Por Qué el Centroide es Óptimo

Para un conjunto fijo $\mathcal{D}_j$, minimizamos

$$
f(m)
=
\sum_{x_i\in\mathcal{D}_j}
\|x_i-m\|^2.
$$

$$
\nabla_m f(m)
=
-2
\sum_{x_i\in\mathcal{D}_j}
(x_i-m).
$$

Igualando a cero:

$$
\hat{m}
=
\frac{1}{n_j}
\sum_{x_i\in\mathcal{D}_j}
x_i.
$$

Por eso la media aparece como representante natural bajo pérdida cuadrática.

## Diapositiva 61. Criterios Invariantes

La traza depende de la escala de las coordenadas.

Alternativas:

$$
|S_W|,
\qquad
\operatorname{tr}(S_W^{-1}S_B),
\qquad
|S_W^{-1}S_B|.
$$

Los autovalores de $S_W^{-1}S_B$ miden razón entre separación y dispersión en direcciones discriminantes.

Precaución: $S_W$ puede ser singular si $d$ es grande o los clusters son pequeños.

## Diapositiva 62. La Función Objetivo No Basta

Minimizar $J_e$ puede preferir dividir un cluster grande en vez de aislar un grupo pequeño.

![Ejemplo donde la suma de cuadrados no coincide con la partición natural](figures/clase-16/fig-62-objective-not-enough.png){width=65%}

## Diapositiva 63. Interpretación Geométrica y Álgebra Lineal

- **Proyección en subespacios:** la traza mide la suma de las varianzas en todas las direcciones ortonormales de $\mathbb{R}^d$.
- **Geometría:** al usar la distancia euclídea implícita en $\operatorname{tr}(S_W)$, estamos asumiendo implícitamente que las densidades condicionales de clase $p(x\mid\omega_i)$ poseen matrices de covarianza esféricas e idénticas $(\Sigma_i=\sigma^2 I)$.
- **Criterios invariantes a escala:** para independizar el agrupamiento de transformaciones afines lineales no singulares $(y=Ax)$, se pueden optimizar criterios basados en el determinante (volumen hiperelipsoidal):

$$
J_d
=
\frac{|S_W|}{|S_T|}
=
|S_W^{-1}S_T|.
$$

## Diapositiva 64. Conexiones con Métodos Supervisados (LDA)

Existe una profunda homología matemática entre este marco de optimización no supervisado y el Análisis Discriminante Lineal de Fisher (LDA):

| Propiedad | LDA (Supervisado) | Criterios de Partición |
| --- | --- | --- |
| Origen de clases | Etiquetas reales observadas $y_i$. | Variables latentes de asignación $\mathcal{D}_i$. |
| Objetivo lineal | Maximizar la razón de dispersión Rayleigh: $\dfrac{w^T S_B w}{w^T S_W w}$. | Optimizar $\operatorname{tr}(S_W)$ o invariantes lineales $|S_W|$. |
| Mecánica | Proyección óptima mediante autovectores generales de $S_W^{-1}S_B$. | Reasignación iterativa (heurística de EM coordinada). |

El clustering particional clásico busca recrear de forma adaptativa e iterativa las fronteras hiperplanas óptimas que LDA calcularía si conociéramos las etiquetas de la naturaleza.

## Diapositiva 65. Qué Deja Esta Introducción

El capítulo plantea una secuencia conceptual importante:

1. comenzar con un problema bien especificado en términos probabilísticos;
2. advertir que la identificabilidad es condición previa de posibilidad;
3. derivar ecuaciones de máxima verosimilitud con variables latentes;
4. reconocer dificultades prácticas: no convexidad, múltiples máximos, singularidades;
5. pasar a procedimientos de partición más simples como $k$-means.

Esa secuencia fija una filosofía de trabajo:

$$
\text{clustering}
\ne
\text{una sola técnica},
$$

sino una familia de respuestas a distintas formalizaciones de "estructura".

## Diapositiva 66. Ideas que Conviene Retener

- El aprendizaje no supervisado requiere hipótesis adicionales para ser interpretable.
- La estructura inferida depende del modelo, de la métrica y de la parametrización.
- Un cluster puede entenderse como componente de mezcla, región de partición o modo de densidad.
- La identificabilidad separa problemas bien planteados de problemas insolubles en principio.
- $k$-means es simple y útil, pero su validez conceptual es restringida.

Próxima clase:

- Algoritmos de clustering: principios, tipos y aplicaciones.
- Algoritmo para visualización de datos de alta dimensión: t-SNE.
