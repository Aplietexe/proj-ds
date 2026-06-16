---
title: "Clustering y Aprendizaje No Supervisado: El Paradigma Algorítmico"
header-includes:
  - |
    <style>
    .katex-display, figure, img {
      break-inside: avoid;
      page-break-inside: avoid;
    }
    h2 {
      break-after: avoid;
    }
    </style>
---

## Diapositiva 1

**Portada**

- Clustering y aprendizaje no supervisado
- El Paradigma Algorítmico
- Ciencia de Datos
- FaMAF
- Clase 16 - 2026-05-21

## Diapositiva 2. Plan de la Clase

1. **Mapa de métodos**
   - Métodos particionales
   - Clustering jerárquico
   - Densidad, grafos y conectividad
2. **Validación e interpretación**
   - Reducción dimensional y representaciones
3. **Algoritmo t-SNE**
   - Reducción de dimensionalidad

## Diapositiva 3. Mapa de Métodos

**Sección:** Mapa de métodos.

## Diapositiva 4. Motivación Formal: Del Enfoque Generativo al Algorítmico

En el escenario supervisado modelamos la densidad conjunta condicionada por las clases $\omega_i$:

$$
p(x \mid \theta) = \sum_{i=1}^{c} P(\omega_i)p(x \mid \omega_i,\theta_i)
$$

donde las etiquetas de clase $\omega_i$ actúan como variables latentes no observables en el espacio muestral $\mathcal{D}=\{x_1,\ldots,x_n\}$.

En el enfoque generativo no supervisado de mezcla de modelos, se asume que cada componente $f_k(x;\theta_k)$ representa un cluster latente, y la asignación de cada observación $x_i$ a un cluster $k$ se modela mediante una variable indicadora binaria $z_{ik}$.

$$
p(x \mid \theta) = \sum_{k=1}^{c} \pi_k f_k(x;\theta_k)
$$

**El cambio de paradigma:** cuando prescindimos de la hipótesis de una distribución paramétrica subyacente $f(x;\theta)$, la pregunta estadística muta hacia una regla estrictamente computacional y geométrica.

## Diapositiva 5. De Modelos Estadísticos a Algoritmos

Ante casos en donde la aproximación generativa no es válida, debemos cambiar la pregunta:

**¿Qué regla computacional produce grupos útiles a partir de una noción de parecido entre observaciones?**

La respuesta no es un único algoritmo, sino una familia de decisiones:

- qué significa que dos objetos estén cerca;
- qué forma de grupo se considera admisible;
- si buscamos una partición, una jerarquía o regiones densas;
- si las asignaciones son duras, difusas o probabilísticas.

## Diapositiva 6. Taxonomía Operativa de Algoritmos

![Taxonomía operativa de algoritmos de clustering](figures/clase-17/fig-06-algorithm-taxonomy.png){width=95%}

## Diapositiva 7. Clasificación y Clustering

Encontramos métodos que pueden ser de dos tipos:

- **Basados en modelos:** se asume que las formas de los grupos siguen cierta distribución descripta por un modelo cuyos parámetros han de ser determinados, por ejemplo GMM. Son métodos iterativos que resuelven el problema generativo de asignar cada observación a un componente latente. Requieren una fuerte asunción sobre la forma de los grupos, pero permiten una interpretación probabilística y una evaluación de la incertidumbre.
- **Basados en distancias:** si no se hace ninguna asunción acerca de las formas de los grupos, los resultados pueden ser muy sensibles al cálculo de distancia elegido. En un espacio de parámetros, la distancia euclídea no es la única ni la más obvia. Estos métodos no paramétricos requieren herramientas numéricas y de visualización.

## Diapositiva 8. GMM

![Ejemplo de mezcla gaussiana y asignación de clusters](figures/clase-17/fig-08-gmm.png){width=85%}

## Diapositiva 9. Clustering: Clasificación de Algoritmos Basados en Distancias

- **Hierarchical Algorithms**
  - Agglomerative Algorithms
  - Divisive Algorithms
- **Partitioning Algorithms**
  - K-medoids Algorithms
  - K-means Algorithms
  - Probabilistic Algorithms
  - Density-Based Algorithms (Density-Based Connectivity Clustering, Density Functions Clustering)
- **Grid-Based Algorithms**
- **Algorithms Based on Co-Occurrence of Categorial Data**
- **Constraint-Based Clustering**
- **Evolutionary Algorithms**
- **Scalable Clustering Algorithms**
- **Algorithms for High Dimensional Data** (Subspace Clustering, Projection Algorithms, Co-Clustering)

## Diapositiva 10. Taxonomía Operativa

| Familia | Objeto producido | Decisión central |
| --- | --- | --- |
| Particional | una partición con $c$ grupos | prototipo y función objetivo |
| Jerárquica | dendrograma multiescala | distancia entre clusters |
| Densidad | regiones densas y ruido | vecindad local |
| Grafos | componentes o cortes | matriz de afinidad |
| Modelo probabilístico | distribución latente | verosimilitud y priors |

No son categorías excluyentes, por ejemplo:

- GMM es un modelo probabilístico pero también genera particiones;
- DBSCAN es un método de densidad pero también produce una partición;
- spectral clustering termina usando k-means;
- Ward es jerárquico pero minimiza varianza;
- GMM y k-means comparten una estructura de asignación y actualización.

## Diapositiva 11. La Dependencia de la Distancia

Todo método de clustering hereda una noción de distancia o similitud:

$$
d(x_i,x_j) \qquad \text{o} \qquad s(x_i,x_j).
$$

Esa elección aparece de formas distintas:

- k-means usa distancia euclidiana al centroide;
- jerárquico usa distancias entre pares y luego un *linkage*;
- DBSCAN define vecindades $N_{\varepsilon}(x_i)$;
- spectral construye un grafo de afinidad $W$.

Por eso cambiar escala, métrica o representación puede cambiar más la respuesta que cambiar de algoritmo.

## Diapositiva 12. Tres Preguntas Antes de Elegir Método

1. ¿Buscamos exactamente $c$ grupos o queremos explorar escalas?
2. ¿Los grupos deberían parecerse a bolas, cadenas, regiones densas o componentes de un grafo?
3. ¿La distancia entre observaciones tiene interpretación científica?

$$
\text{modelo de cluster}
= \text{representación} + \text{distancia} + \text{regla algorítmica}
$$

**Taxonomía de modelos**

El desarrollo de los métodos sigue esta estructura:

- A. particiones por prototipos;
- B. algoritmos jerárquicos;
- B.1. algoritmos aglomerativos;
- B.2. algoritmos divisivos;
- C. métodos basados en densidad o conectividad;
- D. clustering espectral.

## Diapositiva 13. Formulación Matemática de la Partición Dura

**Definición. Partición dura**

Sea $\mathcal{D}=\{x_1,\ldots,x_n\}$ un conjunto de vectores en $\mathbb{R}^d$. Una partición dura en $c$ clusters se define como una familia de subconjuntos $\mathcal{C}=\{C_1,C_2,\ldots,C_c\}$ que satisfacen:

1. $C_i\neq \emptyset$, para todo $i\in\{1,\ldots,c\}$;
2. $C_i\cap C_j=\emptyset$, para todo $i\neq j$;
3. $\bigcup_{i=1}^{c} C_i=\mathcal{D}$.

Introducimos la variable indicadora binaria, o matriz de pertenencia, $r_{ik}\in\{0,1\}$, donde

$$
r_{ik}=1 \quad \text{si } x_i\in C_k
$$

sujeta a la restricción canónica

$$
\sum_{k=1}^{c} r_{ik}=1,\qquad \forall i.
$$

Operativamente, buscamos generar una partición del espacio vectorial $\mathbb{R}^d$ de datos que minimice la dispersión interna de las observaciones basándose únicamente en una métrica algebraicamente consistente.

## Diapositiva 14. A. Particiones por Prototipos

Una partición dura busca subconjuntos disjuntos:

$$
\mathcal{D}=C_1\cup \cdots \cup C_c,\qquad C_i\cap C_j=\emptyset.
$$

La familia particional más común representa cada grupo por un prototipo:

$$
C_j \longleftrightarrow m_j.
$$

Luego alterna dos pasos:

- asignar observaciones al prototipo más conveniente;
- actualizar el prototipo con las observaciones asignadas.

![Asignación de observaciones a prototipos](figures/clase-17/fig-14-prototypes.png){width=80%}

Por ejemplo, los prototipos pueden ser medias, medianas, modos u observaciones reales (*medoids*).

## Diapositiva 15. (A) Criterio de Mínima Dispersión Intra-Cluster

Buscamos determinar el conjunto de prototipos $m_1,\ldots,m_c\in\mathbb{R}^d$ y las asignaciones $R=[r_{ik}]$ que minimicen la suma de errores cuadráticos ($J_{\mathrm{MSE}}$):

$$
J_{\mathrm{MSE}}
= J(R,m_1,\ldots,m_c)
= \sum_{i=1}^{n}\sum_{k=1}^{c} r_{ik}\lVert x_i-m_k\rVert^2.
\tag{1}
$$

**Conexión con Álgebra Lineal**

Este criterio equivale a minimizar la traza de la matriz de dispersión intra-cluster ($S_W$). Recordando la definición de la matriz de dispersión para la clase $C_k$:

$$
S_k=\sum_{x\in C_k}(x-m_k)(x-m_k)^T
\quad \Longrightarrow \quad
J=\sum_{k=1}^{c}\operatorname{Tr}(S_k)=\operatorname{Tr}(S_W).
$$

A diferencia de LDA, donde maximizamos la razón entre la dispersión entre-clases $S_B$ e intra-clases $S_W$ con clases conocidas, aquí buscamos minimizar de forma directa la métrica interna de $S_W$.

## Diapositiva 16. (A) Derivación Analítica del Paso de Actualización

**Optimalidad del centroide muestral**

Dada una asignación fija de los puntos a los clusters ($R$ fija), los prototipos óptimos $m_k^*$ que minimizan el funcional $J$ corresponden unívocamente a los centroides muestrales de cada subconjunto.

**Demostración.** Calculamos el gradiente de $J$ con respecto a un prototipo específico $m_j$:

$$
\nabla_{m_j}J
= \nabla_{m_j}\sum_{i=1}^{n} r_{ij}(x_i-m_j)^T(x_i-m_j)
= \sum_{i=1}^{n} r_{ij}\bigl(-2(x_i-m_j)\bigr).
$$

Igualando la condición de primer orden al vector nulo $0$ para garantizar la estacionariedad:

$$
-2\sum_{i=1}^{n} r_{ij}x_i
+2\sum_{i=1}^{n} r_{ij}m_j = 0
\quad \Longrightarrow \quad
m_j\sum_{i=1}^{n}r_{ij}=\sum_{i=1}^{n}r_{ij}x_i.
$$

Dado que $\sum_{i=1}^{n} r_{ij}=n_j$, el cardinal de $C_j$, despejamos formalmente:

$$
m_j^*=\frac{\sum_{i=1}^{n} r_{ij}x_i}{n_j}.
$$

## Diapositiva 17. (A) c-means k-means

Recordemos el peso posterior en una mezcla:

$$
\gamma_{ik}=P(\omega_i\mid x_k,\hat{\theta}).
$$

Si los componentes están bien separados, podemos aproximar:

$$
\gamma_{ik}\approx
\begin{cases}
1, & \text{si el componente } i \text{ explica mejor a } x_k,\\
0, & \text{en otro caso.}
\end{cases}
$$

Si además las covarianzas son esféricas e iguales, $\Sigma_i=\sigma^2 I$, la comparación de componentes se reduce a distancia euclidiana al centro.

Así aparece k-means como aproximación dura de un modelo de mezcla. k-means es el caso canónico de partición por prototipos:

- prototipo = media;
- distancia = euclidiana cuadrática.

## Diapositiva 18. (A) Objetivo de k-means

k-means resuelve aproximadamente:

$$
\min_{r_{ij},m_1,\ldots,m_c}
\sum_{i=1}^{n}\sum_{j=1}^{c} r_{ij}\lVert x_i-m_j\rVert^2
\quad
\text{sujeto a }
r_{ij}\in\{0,1\},
\quad
\sum_{j=1}^{c} r_{ij}=1.
$$

La asignación es "dura": cada observación pertenece a un único cluster. La geometría implícita es fuerte: se premian grupos compactos, aproximadamente esféricos y de escala comparable.

![Objetivo de k-means y partición encontrada](figures/clase-17/fig-18-kmeans-objective.png){width=85%}

## Diapositiva 19. (A) Algoritmo de k-means

Dado $c$ y centros iniciales $m_1^{(0)},\ldots,m_c^{(0)}$:

1. Asignar cada punto al centro más cercano:

$$
r_{ij}^{(t)}=1
\quad \Longleftrightarrow \quad
j=\arg\min_{\ell}\lVert x_i-m_{\ell}^{(t)}\rVert^2.
$$

2. Actualizar centros:

$$
m_j^{(t+1)}
=
\frac{\sum_i r_{ij}^{(t)}x_i}{\sum_i r_{ij}^{(t)}}.
$$

3. Repetir hasta que no cambien asignaciones o el descenso sea pequeño.

Tiene complejidad típica $O(ndc)$. Cada paso de k-means no aumenta el criterio:

$$
J^{(t+1)}\leq J^{(t)}.
$$

Esto ocurre porque:

- con centros fijos, cada punto elige el término mínimo;
- con asignaciones fijas, la media minimiza la suma de cuadrados.

Como hay finitas particiones, el algoritmo termina. Pero termina en un mínimo local o punto estacionario, no necesariamente global. Por eso importan la inicialización y múltiples corridas.

## Diapositiva 20. (A) Fronteras de Voronoi

Con centros fijos, k-means induce regiones:

$$
V_j=\{x:\lVert x-m_j\rVert^2\leq \lVert x-m_{\ell}\rVert^2,\ \forall \ell\}.
$$

La frontera entre $j$ y $\ell$ satisface:

$$
\lVert x-m_j\rVert^2 = \lVert x-m_{\ell}\rVert^2.
$$

Expandiendo:

$$
2(m_{\ell}-m_j)^T x = \lVert m_{\ell}\rVert^2-\lVert m_j\rVert^2.
$$

Las fronteras son hiperplanos: k-means produce celdas convexas.

![Celdas de Voronoi inducidas por k-means](figures/clase-17/fig-20-voronoi.png){width=70%}

## Diapositiva 21. (A) Inicialización y Elección de $c$

La inicialización afecta el mínimo local.

Prácticas comunes:

- múltiples corridas y quedarse con menor $J$;
- k-means++: elegir centros iniciales alejados probabilísticamente;
- usar conocimiento de dominio;
- inicializar con una solución jerárquica.

Si $c$ aumenta, el criterio siempre baja:

$$
J(1)\geq J(2)\geq \cdots \geq J(n)=0.
$$

Por eso $c$ se elige con validación, estabilidad, interpretabilidad o un criterio probabilístico externo.

## Diapositiva 22. (A) Desempeño con Distintos Datasets

Dependencia con el número de clusters, varianza y tamaño relativo:

![Desempeño de k-means con distintos números de clusters, varianzas y tamaños relativos](figures/clase-17/fig-22-kmeans-datasets-size.png){width=100%}

## Diapositiva 23. (A) Desempeño con Distintos Datasets

Dependencia con la forma de los clusters:

![Desempeño de k-means con distintas formas de clusters](figures/clase-17/fig-23-kmeans-datasets-shape.png){width=100%}

## Diapositiva 24. (A) Variantes Particionales

| Método | Asignación | Comentario |
| --- | --- | --- |
| k-means | dura | centros como medias |
| Mini-batch k-means | dura | escalable para $n$ grande |
| Fuzzy k-means | difusa | membresías $u_{ij}\in[0,1]$ |
| k-medoids | dura | prototipos son observaciones |
| GMM + EM | probabilística | parámetros de densidad |

En fuzzy k-means se minimiza

$$
J_m=\sum_{i=1}^{n}\sum_{j=1}^{c} u_{ij}^{m}\lVert x_i-m_j\rVert^2,
\qquad m>1,
$$

donde $m$ controla cuán difusas son las asignaciones.

## Diapositiva 25. (A) Limitaciones de la Familia

Los métodos particionales por prototipos funcionan bien cuando los clusters son:

- compactos;
- separables por la distancia elegida;
- razonablemente balanceados;
- bien resumidos por un representante central.

Fallas típicas:

- formas no convexas;
- anisotropía fuerte;
- densidades muy distintas;
- outliers;
- variables irrelevantes de alta dimensión.

![Falla típica de k-means en formas no convexas](figures/clase-17/fig-25-kmeans-limitations.png){width=70%}

## Diapositiva 26. B. Jerarquías: Organizar Escalas

A veces no hay un único nivel natural de agrupamiento. Una jerarquía produce una familia anidada de particiones:

$$
\mathcal{P}_n \preceq \mathcal{P}_{n-1} \preceq \cdots \preceq \mathcal{P}_1.
$$

Se presentan dos enfoques:

- **aglomerativo:** comienza con $n$ clusters y fusiona;
- **divisivo:** comienza con un cluster y divide.

En ambos casos, la distancia define qué fusiones o divisiones son razonables.

La representación habitual es un **dendrograma**. Un dendrograma codifica el orden de fusiones y sus alturas.

Cortar a altura $h$ produce una partición:

$$
\mathcal{P}(h)=\{\text{componentes debajo de }h\}.
$$

![Dendrograma cortado a una altura h](figures/clase-17/fig-26-dendrogram-cut.png){width=70%}

## Diapositiva 27. Algoritmo Aglomerativo

![Applet de clustering jerárquico aglomerativo](figures/clase-17/fig-27-hierarchical-applet.png){width=70%}

1. Inicializar $C_i=\{x_i\}$ para $i=1,\ldots,n$.
2. Calcular las distancias para todos los pares de clusters.
3. Fusionar los clusters más cercanos.
4. Actualizar la matriz de distancias entre clusters.
5. Repetir hasta obtener un único cluster.

Applet: `hierarchical.html`.

## Diapositiva 28. (B) Dos Niveles de Distancia

En clustering jerárquico hay que distinguir dos mediciones de distancias:

- **distancia entre observaciones:** define qué puntos están cerca, $d(x_i,x_j)$;
- **distancia entre clusters:** define qué grupos están cerca, $D(A,B)$, o *linkage*. Es una regla que transforma muchas distancias punto-punto en una distancia grupo-grupo.

Por tanto, el método jerárquico queda definido por:

$$
\text{datos} + d(x_i,x_j) + D(A,B) + \text{regla aglomerativa/divisiva}.
$$

## Diapositiva 29. (B) Linkages Principales

**Single linkage** une si hay un puente cercano; detecta formas alargadas, pero sufre encadenamiento.

$$
D_{\min}(A,B)=\min_{x\in A,\ x'\in B} d(x,x').
$$

**Complete linkage:** exige cercanía global; favorece grupos compactos.

$$
D_{\max}(A,B)=\max_{x\in A,\ x'\in B} d(x,x').
$$

**Average linkage:** compromiso entre ambos extremos.

$$
D_{\mathrm{avg}}(A,B)=\frac{1}{|A||B|}\sum_{x\in A}\sum_{x'\in B} d(x,x').
$$

![Comparación visual de single, complete y average linkage](figures/clase-17/fig-29-linkage-basic.png){width=45%}

## Diapositiva 30. (B) Linkages Principales

**Centroid linkage** une grupos por la distancia entre sus centroides:

$$
m_A=\frac{1}{|A|}\sum_{x\in A}x.
$$

**Ward linkage** fusiona los clusters que menos incrementan la suma de cuadrados intra-cluster:

$$
\Delta(A,B)=\frac{|A||B|}{|A|+|B|}\lVert m_A-m_B\rVert^2.
$$

Es el análogo jerárquico de un criterio de mínima varianza. Tiende a producir clusters compactos y de tamaño relativamente balanceado.

Conceptualmente conecta jerárquico con k-means, ya que ambos premian baja dispersión interna.

![Comparación visual de centroid linkage y Ward linkage](figures/clase-17/fig-30-linkage-centroid-ward.png){width=55%}

## Diapositiva 31. (B) Algoritmos Divisivos

El enfoque divisivo recorre el árbol en dirección opuesta:

$$
\{x_1,\ldots,x_n\}\longrightarrow \text{subgrupos cada vez más finos}.
$$

Esquema general:

1. comenzar con todos los puntos en un único cluster;
2. elegir un cluster para partir;
3. dividirlo según una regla de separación;
4. repetir hasta alcanzar una escala o número de grupos deseado.

![Secuencia de particiones divisivas](figures/clase-17/fig-31-divisive-sequence.png){width=90%}

## Diapositiva 32. (B) Aglomerativo vs. Divisivo

| Enfoque | Dirección | Sesgo práctico |
| --- | --- | --- |
| Aglomerativo | de puntos a grupos | decisiones locales de fusión |
| Divisivo | de todo a partes | decisiones globales de separación |

Aglomerativo es más común porque es simple y produce un dendrograma completo.

Divisivo puede capturar separaciones globales antes que detalles locales, pero requiere resolver problemas de partición potencialmente costosos.

Ambos son sensibles a la distancia inicial y a la regla usada para comparar o separar grupos.

![Direcciones aglomerativa y divisiva en un dendrograma](figures/clase-17/fig-32-agglomerative-divisive.png){width=60%}

## Diapositiva 33. (B) Ventajas y Límites de Jerárquico

| Ventajas | Límites |
| --- | --- |
| no exige fijar $c$ al inicio | decisiones *greedy* no se corrigen |
| da estructura multiescala | costo alto en memoria para $n$ grande |
| funciona con una matriz de distancias | dendrogramas pueden sugerir cortes espurios |
| útil para exploración y visualización | sensibilidad fuerte al *linkage* y a la métrica |

## Diapositiva 34. C. Clusters como Regiones Densas

Una definición de grupo basada en densidad es:

**Un cluster es una región de alta densidad separada de otras regiones densas por zonas de baja densidad.**

Esto evita exigir convexidad. La estimación de densidad:

$$
\hat{p}_h(x)
=
\frac{1}{nh^d}\sum_{i=1}^{n}K\left(\frac{x-x_i}{h}\right).
$$

Los modos y conjuntos de nivel de $\hat{p}_h$ inducen grupos.

De esta estrategia se derivan métodos tales como:

- mean shift;
- DBSCAN;
- clustering espectral.

## Diapositiva 35. (C) Mean Shift: Idea

Mean shift no busca centros que minimicen varianza, sino modos de una densidad suavizada.

A partir de una estimación por kernel,

$$
\hat{p}_h(x)
=
\frac{1}{nh^d}\sum_{i=1}^{n}K\left(\frac{x-x_i}{h}\right),
$$

cada observación se desplaza iterativamente hacia la zona donde la densidad local aumenta.

![Idea geométrica de mean shift](figures/clase-17/fig-35-mean-shift-idea.png){width=60%}

Algoritmo:

- poner una ventana de ancho $h$ alrededor de un punto;
- calcular el promedio ponderado de los datos dentro de esa ventana;
- mover el punto hacia ese promedio;
- repetir hasta llegar a un máximo local de densidad;
- puntos cercanos a un mismo modo convergen al mismo modo;
- cada modo define un cluster;
- no hay que fijar $c$ de antemano.

## Diapositiva 36. (C) Mean Shift: Actualización

Con kernel radial, el nuevo punto es una media local ponderada:

$$
x^{(t+1)}
=
\frac{
\sum_i x_i K\left(\frac{\lVert x^{(t)}-x_i\rVert^2}{h^2}\right)
}{
\sum_i K\left(\frac{\lVert x^{(t)}-x_i\rVert^2}{h^2}\right)
}.
$$

![Superficie de densidad y trayectorias de mean shift](figures/clase-17/fig-36-mean-shift-surface.png){width=60%}

El vector de desplazamiento

$$
m(x^{(t)})=x^{(t+1)}-x^{(t)}
$$

apunta hacia una región de mayor densidad estimada. Por eso el algoritmo puede verse como un ascenso por gradiente sobre $\hat{p}_h$, pero sin calcular explícitamente derivadas.

La asignación final se obtiene agrupando puntos cuyas trayectorias convergen al mismo modo, o a modos suficientemente cercanos.

## Diapositiva 37. (C) Mean Shift: Qué Controla el Ancho de Banda

El parámetro crítico es el ancho de banda $h$.

| $h$ pequeño | $h$ grande |
| --- | --- |
| estima mucho detalle local | suaviza la densidad |
| aparecen muchos modos | fusiona modos cercanos |
| puede fragmentar un mismo grupo | produce menos clusters |
| es sensible al ruido | puede ocultar subestructura real |

Ventaja: no hay que fijar $c$ de antemano.

Límite: el resultado depende mucho de la escala $h$ y el costo puede ser alto si se actualizan muchos puntos contra todos los datos.

## Diapositiva 38. (C) DBSCAN: Definiciones

En el método DBSCAN (*Density-Based Spatial Clustering of Applications with Noise*) se definen tres tipos de puntos: núcleo, borde y ruido, a partir de los parámetros radio $\varepsilon$ y mínimo de puntos $m$.

Definimos la vecindad de un punto $x_i$ como:

$$
N_{\varepsilon}(x_i)=\{x_j:d(x_i,x_j)\leq \varepsilon\}.
$$

- **Núcleo:** punto que tiene al menos $m$ vecinos dentro de una bola de radio $\varepsilon$, $\lvert N_{\varepsilon}(x_i)\rvert\geq m$.
- **Borde:** punto que no es núcleo, pero está en la vecindad de un núcleo.
- **Ruido:** punto que no es núcleo ni borde.

![Tipos de puntos según DBSCAN](figures/clase-17/fig-38-dbscan-points.png){width=55%}

## Diapositiva 39. (C) DBSCAN: Algoritmo

1. Elegir un punto no visitado.
2. Si no es núcleo, marcar como ruido provisional.
3. Si es núcleo, iniciar un cluster.
4. Agregar todos los puntos densamente alcanzables.
5. Repetir hasta visitar todos los puntos.

Dos núcleos cercanos conectan sus vecindades. Por eso DBSCAN puede encontrar formas no convexas.

![Comparación de DBSCAN contra k-means en formas no convexas](figures/clase-17/fig-39-dbscan-comparison.png){width=90%}

## Diapositiva 40. (C) DBSCAN: Fortalezas y Debilidades

| Ventajas | Límites |
| --- | --- |
| no requiere fijar $c$ | un solo $\varepsilon$ falla con densidades muy distintas |
| detecta ruido | sufre en alta dimensión |
| permite clusters de forma arbitraria | depende de la métrica |
| usa conectividad local | bordes pueden ser ambiguos |

![Efecto de epsilon y min_samples en DBSCAN](figures/clase-17/fig-40-dbscan-parameters.png){width=100%}

## Diapositiva 41. D. Clustering Espectral: Idea

Clustering espectral transforma un problema geométrico en un problema sobre un grafo.

1. Cada observación $x_i$ es un nodo.
2. Las aristas tienen pesos $W_{ij}$ que miden similitud.
3. Los clusters son subconjuntos con alta conexión interna y baja conexión con el resto del grafo.

La ventaja frente a k-means en el espacio original es que la separación puede estar codificada en la conectividad y no en fronteras lineales o regiones convexas.

Ejemplo: dos lunas no son separables por centroides euclidianos, pero sí pueden ser dos regiones conectadas débilmente entre sí en un grafo de vecinos.

## Diapositiva 42. D. Construcción del Grafo de Afinidad

La decisión central es cómo construir $W$.

Opciones frecuentes:

$$
W_{ij}=
\exp\left(-\frac{\lVert x_i-x_j\rVert^2}{2\sigma^2}\right)
\qquad \text{o} \qquad
W_{ij}=0 \text{ si } x_j\notin k\mathrm{NN}(x_i).
$$

Luego se define el grado del nodo:

$$
D_{ii}=\sum_j W_{ij}.
$$

Dos laplacianos usuales son:

$$
L=D-W,\qquad L_{\mathrm{sym}}=I-D^{-1/2}WD^{-1/2}.
$$

$\sigma$, $k$ y la métrica determinan qué significa "vecino". Si esa construcción es mala, el paso espectral sólo diagonaliza un grafo mal planteado.

## Diapositiva 43. D. ¿Por Qué Aparecen Autovectores?

Para cualquier señal $u\in\mathbb{R}^n$ definida sobre los nodos:

$$
u^T L u = \frac{1}{2}\sum_{i,j} W_{ij}(u_i-u_j)^2.
$$

Esta energía penaliza que nodos muy similares reciban valores muy distintos. Por lo tanto, las soluciones de baja energía son casi constantes dentro de regiones muy conectadas.

Si el grafo tuviera $c$ componentes conexas exactas, los primeros $c$ autovectores del laplaciano indicarían esas componentes. En datos reales las componentes no son perfectas: los autovectores de menor autovalor dan una versión continua y aproximada de esa estructura.

El k-means final no trabaja sobre las variables originales sino sobre una representación donde la conectividad del grafo quedó aproximadamente linealizada.

## Diapositiva 44. D. Algoritmo Espectral

Una versión estándar con $c$ clusters:

1. Construir la matriz de afinidad $W$.
2. Calcular $D$ y un laplaciano, por ejemplo $L_{\mathrm{sym}}$.
3. Tomar los $c$ autovectores asociados a los menores autovalores.
4. Formar una matriz $U\in\mathbb{R}^{n\times c}$: una fila por dato.
5. Normalizar las filas de $U$ si se usa $L_{\mathrm{sym}}$.
6. Aplicar k-means a las filas de $U$.

![Ejemplos de clustering espectral](figures/clase-17/fig-44-spectral-examples.png){width=60%}

## Diapositiva 45. (D) Cortes de Grafo

Para dos conjuntos $A,B$,

$$
\operatorname{cut}(A,B)=\sum_{i\in A,\ j\in B}W_{ij}.
$$

Un buen corte separa poca afinidad cruzada, pero evita conjuntos triviales.

Criterios normalizados:

$$
\operatorname{Ncut}(A,B)=
\frac{\operatorname{cut}(A,B)}{\operatorname{vol}(A)}
+
\frac{\operatorname{cut}(A,B)}{\operatorname{vol}(B)}.
$$

La relajación continua lleva a autovectores del laplaciano normalizado.

## Diapositiva 46

![Comparación de métodos de clustering sobre varios datasets](figures/clase-17/fig-46-method-comparison.png){width=100%}

## Diapositiva 47. Validación e Interpretación

**Sección:** Validación e interpretación.

## Diapositiva 48. El Problema de Validez

En supervisado tenemos error de test.

En clustering no hay una verdad observable en general.

Preguntas distintas:

- ¿la partición es compacta y separada?
- ¿es estable ante perturbaciones de los datos?
- ¿coincide con etiquetas externas disponibles?
- ¿es útil para una decisión científica u operativa?
- ¿es reproducible bajo cambios razonables de escala?

## Diapositiva 49. Índices Internos

Usan sólo $x_i$ y la partición.

Desean simultáneamente:

$$
\text{baja dispersión intra-cluster}
\qquad
\text{alta separación inter-cluster}.
$$

Ejemplos:

- silhouette;
- Calinski-Harabasz;
- Davies-Bouldin;
- gap statistic.

No son verdades universales: heredan la métrica y el tipo de cluster que premian.

## Diapositiva 50. Silhouette

Para el punto $i$:

$$
a(i)=\text{distancia media a puntos de su cluster},
$$

$$
b(i)=\min_{\ell\neq z_i}\text{ distancia media a puntos del cluster }\ell.
$$

Silhouette:

$$
s(i)=\frac{b(i)-a(i)}{\max\{a(i),b(i)\}}\in[-1,1].
$$

- cercano a 1: bien asignado;
- cercano a 0: frontera;
- negativo: probablemente mal asignado.

![Componentes a(i), b(i) y s(i) del índice silhouette](figures/clase-17/fig-50-silhouette-components.png){width=100%}

## Diapositiva 51. Silhouette: Lectura Práctica

El promedio

$$
\bar{s}=\frac{1}{n}\sum_{i=1}^{n}s(i)
$$

resume qué tan bien separados y compactos son los clusters.

- Premia clusters compactos y lejos de los demás.
- Puede calcularse con cualquier distancia, no sólo euclidiana.
- Sirve para comparar valores de $c$ o particiones alternativas.

Cuidado: favorece grupos aproximadamente convexos y bien separados. Puede penalizar estructuras válidas con forma de luna, cadenas o densidades muy desiguales.

![Diagrama silhouette por cluster](figures/clase-17/fig-51-silhouette-practical.png){width=60%}

## Diapositiva 52. Método del Codo

Para k-means se grafica el criterio intra-cluster:

$$
W_c=\sum_{k=1}^{c}\sum_{x_i\in C_k}\lVert x_i-\mu_k\rVert^2.
$$

Al aumentar $c$, $W_c$ siempre baja: con más centros se puede explicar mejor la variabilidad interna.

La regla del codo busca el punto donde agregar otro cluster deja de producir una mejora sustantiva:

$$
\text{gran mejora antes del codo}
\quad \longrightarrow \quad
\text{mejora marginal después del codo}.
$$

Es una heurística visual, no un test. Si la curva es suave y no hay codo claro, el dato no está sugiriendo un número de clusters bien definido bajo ese criterio.

## Diapositiva 53

![Método del codo y silhouette score para distintos valores de K](figures/clase-17/fig-53-elbow-silhouette.png){width=90%}

## Diapositiva 54. Calinski-Harabasz

El índice Calinski-Harabasz compara dispersión entre clusters contra dispersión dentro de clusters:

$$
CH(c)=\frac{\operatorname{tr}(B)/(c-1)}{\operatorname{tr}(W)/(n-c)}.
$$

Donde:

$$
W=\sum_{k=1}^{c}\sum_{x_i\in C_k}(x_i-\mu_k)(x_i-\mu_k)^T,
$$

$$
B=\sum_{k=1}^{c} n_k(\mu_k-\mu)(\mu_k-\mu)^T.
$$

Valores más altos indican clusters compactos y centroides bien separados. Hereda una geometría tipo k-means: favorece grupos globulares y separaciones euclidianas.

## Diapositiva 55. Davies-Bouldin

El índice Davies-Bouldin mide, para cada cluster, qué tan parecido es al cluster más problemático:

$$
DB(c)=\frac{1}{c}\sum_{k=1}^{c}\max_{\ell\neq k}\frac{S_k+S_{\ell}}{M_{k\ell}}.
$$

Donde:

$$
S_k=\frac{1}{n_k}\sum_{x_i\in C_k}\lVert x_i-\mu_k\rVert,
\qquad
M_{k\ell}=\lVert \mu_k-\mu_{\ell}\rVert.
$$

- $S_k$ mide tamaño o dispersión interna.
- $M_{k\ell}$ mide separación entre centroides.
- Valores más bajos son mejores.

Penaliza clusters dispersos o centroides cercanos. También asume que el centroide resume bien cada grupo.

## Diapositiva 56. Gap Statistic

El *gap statistic* pregunta si la estructura observada mejora lo esperable bajo una nube sin clusters.

Para cada $c$ se calcula la dispersión intra-cluster observada $W_c$ y se la compara con datos de referencia simulados sin estructura:

$$
\operatorname{Gap}(c)=\mathbb{E}_{\mathrm{ref}}[\log W_c^*]-\log W_c.
$$

Si $\operatorname{Gap}(c)$ es grande, la partición con $c$ clusters reduce la dispersión mucho más que una nube de referencia.

Regla usual: elegir el menor $c$ tal que

$$
\operatorname{Gap}(c)\geq \operatorname{Gap}(c+1)-s_{c+1},
$$

donde $s_{c+1}$ cuantifica la variabilidad Monte Carlo de la referencia.

## Diapositiva 57. AIC y BIC para Modelos Generativos

En modelos como GMM no sólo hay una partición: hay una verosimilitud probabilística.

Si $\hat{\theta}_c$ es el modelo ajustado con $c$ componentes y $q_c$ es el número de parámetros:

$$
\operatorname{AIC}(c)=2q_c-2\log \mathcal{L}(\hat{\theta}_c),
$$

$$
\operatorname{BIC}(c)=q_c\log n-2\log \mathcal{L}(\hat{\theta}_c).
$$

Ambos equilibran ajuste y complejidad:

- la verosimilitud premia modelos que explican mejor los datos;
- la penalización evita agregar componentes innecesarios;
- valores más bajos son mejores.

## Diapositiva 58. AIC vs BIC: Interpretación

AIC y BIC responden una pregunta distinta a silhouette o Calinski-Harabasz: comparan modelos probabilísticos, no sólo particiones geométricas.

| AIC | BIC |
| --- | --- |
| penalización $2q_c$ | penalización $q_c\log n$ |
| tiende a elegir modelos más flexibles | más conservador si $n$ es grande |
| enfocado en capacidad predictiva | usado para seleccionar número de componentes |

En GMM, una componente no siempre equivale a un cluster sustantivo: puede estar modelando asimetría, colas o subestructura de una misma población.

## Diapositiva 59. Índices Externos

Si hay etiquetas externas $y_i$, se comparan con clusters $\hat{z}_i$.

Matriz de contingencia:

$$
n_{ab}=\lvert\{i:y_i=a,\hat{z}_i=b\}\rvert.
$$

Medidas:

- homogeneidad: cada cluster contiene una clase;
- completitud: cada clase cae en un cluster;
- V-measure: media armónica;
- adjusted Rand index;
- información mutua ajustada.

Etiquetas externas pueden ser imperfectas o responder otra pregunta.

## Diapositiva 60. Adjusted Rand Index

Compara pares de observaciones.

Dos particiones coinciden en un par si:

- ambas ponen al par junto;
- o ambas lo separan.

Rand index ajustado:

$$
\operatorname{ARI}=
\frac{\operatorname{RI}-\mathbb{E}(\operatorname{RI})}
{\max(\operatorname{RI})-\mathbb{E}(\operatorname{RI})}.
$$

Propiedades:

- $\operatorname{ARI}=1$ si las particiones coinciden;
- valor esperado cercano a $0$ bajo azar;
- puede ser negativo.

## Diapositiva 61. Cómo Usar Métricas de Validación

Ningún índice decide por sí solo.

| Métrica | Mejor valor | Premia |
| --- | --- | --- |
| Silhouette | alto | compactación y separación |
| Codo | cambio de pendiente | mejora marginal decreciente |
| Calinski-Harabasz | alto | varianza entre / varianza dentro |
| Davies-Bouldin | bajo | baja dispersión y centroides separados |
| Gap statistic | alto | mejora sobre referencia sin clusters |
| AIC/BIC | bajo | verosimilitud penalizada |

La elección final debe combinar índice, estabilidad, interpretabilidad y conocimiento del problema.

## Diapositiva 62. Estabilidad

Una estructura confiable debería persistir bajo perturbaciones razonables.

Procedimiento:

1. remuestrear o partir datos;
2. clusterizar cada muestra;
3. comparar particiones con ARI o co-asociación;
4. evaluar variabilidad por $c$ y por hiperparámetros.

Advertencia: una partición estable puede ser establemente equivocada si la métrica codifica mal la similitud relevante.

## Diapositiva 63. PCA como Puente

PCA ya es aprendizaje no supervisado:

$$
\max_{\lVert w\rVert=1}\operatorname{Var}(w^T x).
$$

Solución:

$$
Sw=\lambda w,
$$

donde $S$ es la matriz de covarianza muestral.

Proyectar en las primeras componentes puede:

- reducir ruido;
- eliminar redundancia;
- mejorar distancias;
- facilitar visualización.

## Diapositiva 64. PCA Antes de Clustering

Si $x\in\mathbb{R}^d$ y $d$ es grande:

$$
z_i=W_q^T(x_i-\bar{x}),\qquad q\ll d.
$$

Clusterizamos $z_i$ en vez de $x_i$.

Esto es útil cuando:

- las primeras componentes capturan señal;
- variables originales están muy correlacionadas;
- hay ruido isotrópico de baja varianza.

Pero PCA preserva varianza, no necesariamente separabilidad de clusters.

## Diapositiva 65. Redes Neuronales y Embeddings

Una red supervisada aprende una transformación

$$
\phi:\mathbb{R}^d\to\mathbb{R}^q.
$$

Luego se puede clusterizar en el espacio latente:

$$
\{\phi(x_i)\}_{i=1}^{n}.
$$

Autoencoders:

$$
x \xrightarrow{\mathrm{encoder}} z
\xrightarrow{\mathrm{decoder}} \hat{x},
\qquad
\min \sum_i \lVert x_i-\hat{x}_i\rVert^2.
$$

La noción de similitud pasa del espacio original al espacio aprendido.

## Diapositiva 66. Mapa de Métodos

| Método | Define cluster por | Necesita $c$ |
| --- | --- | --- |
| K-means | centroide y varianza | sí |
| GMM | componente probabilístico | sí |
| Jerárquico | linkage multiescala | no al inicio |
| DBSCAN | densidad conectada | no |
| Mean shift | modo de densidad | no |
| Spectral | corte de grafo | sí |
| Affinity propagation | exemplar | no explícito |

## Diapositiva 67. Guía de Elección

- Clusters esféricos, $n$ grande: k-means o mini-batch k-means.
- Elipsoides y pertenencia probabilística: mezclas gaussianas.
- Exploración multiescala: jerárquico.
- Formas no convexas y ruido: DBSCAN.
- Estructura de grafo o *manifold*: spectral.
- Datos categóricos o similitudes no métricas: métodos basados en afinidad.

La elección debe justificarse por geometría, no sólo por disponibilidad en software.

## Diapositiva 68. Checklist Antes de Clusterizar

1. ¿Cuál es la unidad observacional?
2. ¿Qué variables definen similitud?
3. ¿Cómo se escalan o transforman?
4. ¿Hay outliers?
5. ¿Se espera convexidad, densidad o conectividad?
6. ¿El número de clusters tiene interpretación?
7. ¿Cómo se validará la partición?

## Diapositiva 69. Ejemplo de Flujo de Trabajo

1. Limpieza y definición de variables.
2. Estandarización robusta o transformación de dominio.
3. PCA exploratorio y diagnóstico de outliers.
4. K-means/GMM para hipótesis compacta.
5. DBSCAN o spectral si aparecen formas no convexas.
6. Validación interna, externa si existe, y estabilidad.
7. Interpretación con variables originales.

**Errores comunes**

- Clusterizar variables con escalas incompatibles.
- Elegir $c$ sólo porque el gráfico "se ve lindo".
- Usar t-SNE/UMAP como prueba de separación.
- Interpretar cada cluster como una clase natural.
- Ignorar outliers.
- Comparar algoritmos con métricas distintas sin declararlo.
- No revisar estabilidad.

## Diapositiva 70. Conexión con lo Visto Antes

**Discriminante lineal**

Misma matriz de dispersión, pero clases conocidas.

**Árboles**

Particiones del espacio, guiadas por $y$.

**Redes**

Representaciones aprendidas, luego separabilidad.

**Clustering**

Particiones, densidades o grafos sin $y$.

La pregunta geométrica es la misma; falta la supervisión.

## Diapositiva 71. Idea Estadística Final

No existe "el" clustering de un conjunto de datos.

Existe una familia de estructuras inducidas por:

$$
(\text{representación},\ \text{métrica},\ \text{criterio},\ \text{algoritmo}).
$$

El análisis estadístico consiste en justificar esa cuádrupla y cuantificar su estabilidad.

- El aprendizaje no supervisado busca estructura sin etiquetas.
- Las mezclas conectan clustering con inferencia probabilística.
- K-means minimiza dispersión intra-cluster y asume geometría convexa.
- Jerárquico organiza grupos por escalas y linkages.
- DBSCAN, mean shift y spectral cambian el foco a densidad o grafos.
- La validación requiere estabilidad, índices e interpretación sustantiva.

## Diapositiva 72. Algoritmo t-SNE

**Sección:** Algoritmo t-SNE.

## Diapositiva 73. t-SNE

t-SNE (*t-Distributed Stochastic Neighbor Embedding*) es un algoritmo no lineal de reducción de dimensionalidad, que funciona particularmente bien para visualización de conjuntos de datos de alta dimensionalidad.

Se usa en procesamiento de imágenes, NLP, procesamiento de lenguaje y datos genómicos.

![Comparación de PCA, ISOMAP y t-SNE](figures/clase-17/fig-73-tsne-intro.png){width=70%}

## Diapositiva 74. Reducción de Dimensionalidad

Hay varias formas de reducir la dimensionalidad de un problema:

- **Feature Elimination:** reducir el espacio de *features* eliminando algunos.
- **Feature Selection:** asignar una métrica de importancia a los *features* y quedarse con los más importantes.
- **Feature Extraction:** crear nuevos *features* que son funciones, lineales o no lineales, de los *features* originales.

Los métodos de reducción de dimensionalidad convierten datos multidimensionales en proyecciones de menor dimensionalidad. Lo que se busca es aprovechar la baja dimensionalidad para poder visualizar los datos, preservando tanto como se pueda la estructura de datos en espacios multidimensionales llevados a mapas de baja dimensionalidad.

![Esquema de eliminación, extracción y proyección de features](figures/clase-17/fig-74-dimensionality-reduction.png){width=60%}

## Diapositiva 75. Stochastic Neighbor Embedding (SNE)

SNE (*Stochastic Neighbor Embedding*, Hinton & Roweis 2002) convierte distancias euclídeas en $N$ dimensiones ($N\gg 2$) en probabilidades condicionales que representan "similaridad".

La similaridad entre un dato y otro es una medida de "qué tan parecidos son", y se define como la probabilidad de que un dato $x_i$ elija a otro dato $x_j$ como vecino, sorteando todos los vecinos en base a una distribución Gaussiana de la distancia Euclídea.

$$
p_{i|j}=
\frac{
\exp\left(-\lVert x_i-x_j\rVert^2/2\sigma_i^2\right)
}{
\sum_{k\neq i}\exp\left(-\lVert x_i-x_k\rVert^2/2\sigma_i^2\right)
}.
\tag{2}
$$

donde los parámetros $\sigma_i$ se deben optimizar. Notar que la **similaridad no es simétrica**.

La similaridad en el espacio de los datos tiene un equivalente en el espacio del mapa:

$$
q_{i|j}=
\frac{
\exp\left(-\lVert y_i-y_j\rVert^2/2\sigma_i^2\right)
}{
\sum_{k\neq i}\exp\left(-\lVert y_i-y_k\rVert^2/2\sigma_i^2\right)
}.
\tag{3}
$$

El mapa modela correctamente la similaridad entre los pares de datos en el espacio multidimensional, cuando las probabilidades condicionales sean iguales.

Se define entonces una función de costo que cuantifica la diferencia entre las dos distribuciones.

## Diapositiva 76. PCA vs. tSNE

![Comparación de PCA 2D y t-SNE sobre dígitos](figures/clase-17/fig-76-pca-vs-tsne.png){width=90%}

## Diapositiva 77. Perplexity

![Efecto de la perplexity en visualizaciones t-SNE](figures/clase-17/fig-77-perplexity.png){width=100%}

## Diapositiva 78. Estructura en los Grupos

![Estructura interna del grupo del dígito 8 en t-SNE](figures/clase-17/fig-78-digit8-structure.png){width=95%}

## Diapositiva 79. Kullback-Leibler Divergence

Es una medida de la diferencia entre dos distribuciones de probabilidad.

Para dos distribuciones discretas de probabilidad, $P$ y $Q$, la divergencia de Kullback-Leibler se define como el valor de expectación sobre $P$ de la diferencia logarítmica entre $P$ y $Q$:

$$
D_{\mathrm{KL}}
=
\sum_{x\in X} P_{i|j}\log\left(\frac{P_{i|j}}{Q_{i|j}}\right).
\tag{4}
$$

Luego,

$$
D_{\mathrm{SNE}}
=
\sum_i D_{\mathrm{KL}}(P_i\Vert Q_i)
\tag{5}
$$

$$
=
\sum_i\sum_{x\in X} P_{i|j}\log\left(\frac{P_{i|j}}{Q_{i|j}}\right),
\tag{6}
$$

donde $X$ es la población.

## Diapositiva 80. Similaridad

Similaridad en el espacio de los datos:

$$
p_{i|j}=
\frac{
\exp\left(-\lVert x_i-x_j\rVert^2/2\sigma_i^2\right)
}{
\sum_{k\neq i}\exp\left(-\lVert x_i-x_k\rVert^2/2\sigma_i^2\right)
}.
\tag{7}
$$

Similaridad en el mapa:

$$
q_{i|j}=
\frac{
\exp\left(-\lVert y_i-y_j\rVert^2/2\sigma_i^2\right)
}{
\sum_{k\neq i}\exp\left(-\lVert y_i-y_k\rVert^2/2\sigma_i^2\right)
}.
\tag{8}
$$

El método SNE define una función de costo para minimizar la diferencia entre $p_{i|j}$ y $q_{i|j}$, como la suma de las divergencias de Kullback-Leibler:

$$
C=\sum_i\sum_j p_{i|j}\log\left(\frac{p_{i|j}}{q_{i|j}}\right).
\tag{9}
$$

## Diapositiva 81. Entropía de Shannon

Una de las aplicaciones de la divergencia de Kullback-Leibler es la caracterización de la Entropía de Shannon.

En su desarrollo de la teoría de la información, a mediados del siglo XX, Claude E. Shannon introduce una función para medir el contenido de información de un evento $A$ de una fuente discreta:

$$
I(A)=-\log(P(A)).
\tag{10}
$$

La cantidad promedio de información de un sistema es el valor de expectación de la información $I(A)$, es decir,

$$
H_S(X)=\sum_i p(x_i)\log(p(x_i)).
\tag{11}
$$

## Diapositiva 82. Optimización de la Función de Costo

**Perplexity:** para el SNE, la perplexidad es una medida del número efectivo de vecinos, y se define como

$$
\operatorname{Perp}(P_i)=2^{H_S(P_i)}.
\tag{12}
$$

donde

$$
H_S(P_i)=-\sum_j p_{i|j}\log_2(p_{i|j}).
\tag{13}
$$

**Gradient descent:** la minimización de la función de costo

$$
D_{\mathrm{SNE}}
=
\sum_i\sum_{x\in\mathcal{X}} P_{i|j}\log\left(\frac{P_{i|j}}{Q_{i|j}}\right)
\tag{14}
$$

mediante el descenso por gradiente asume una forma simple:

$$
\frac{\partial D_{\mathrm{SNE}}}{\partial y_i}
=
2\sum_j
\left[p_{j|i}-q_{j|i}+p_{i|j}-q_{i|j}\right](y_i-y_j).
\tag{15}
$$

## Diapositiva 83. SNE: Elección de la Varianza $\sigma_i$

El parámetro $\sigma_i$, que da la varianza de la Gaussiana para elegir vecinos centrada en cada punto dato $i$, es un parámetro libre.

En general no hay un valor único que sea óptimo para todos los puntos, principalmente por los posibles cambios en la densidad de puntos: en las regiones densas es preferible usar varianzas más chicas que en las regiones escasas (*sparse*).

El valor $\sigma_i$ para el punto $i$ induce una distribución de probabilidad $P_i$ sobre todos los demás datos. La entropía de esta distribución aumenta con $\sigma$.

El algoritmo SNE busca los valores de las varianzas fijando la perplexidad.

## Diapositiva 84. Interpretación de la Función de Costo

$$
\frac{\partial D_{\mathrm{SNE}}}{\partial y_i}
=
2\sum_j
\left[p_{j|i}-q_{j|i}+p_{i|j}-q_{i|j}\right](y_i-y_j).
\tag{16}
$$

se puede interpretar "físicamente" (Van der Maaten & Hinton 2008) como la fuerza resultante de un conjunto de resortes entre el punto mapa $y_i$ y otros puntos mapa $y_j$.

Los resortes ejercen una fuerza en la dirección $y_i-y_j$. Estos resortes atraen o repelen pares de puntos mapa dependiendo si su distancia en el mapa es muy grande o muy chica para representar las similaridades entre los puntos multidimensionales.

![Interpretación de la función de costo como resortes](figures/clase-17/fig-84-cost-springs.png){width=60%}

## Diapositiva 85. t-SNE: Simetrización de la Función de Costo

SNE produce buenas visualizaciones, pero tiene algunos problemas:

- **optimization problem:** la función de costo es difícil de optimizar;
- **crowding problem.**

Se propone una variación del método, t-SNE, en donde:

- usa una versión simetrizada de la función de costo, con un gradiente más simple;
- reemplaza la distribución Gaussiana por una t-Student para calcular la similaridad en el espacio de baja dimensión.

En lugar de usar como función de costo la divergencia de KL entre las distribuciones condicionales $p_{i|j}$ y $q_{i|j}$, se puede usar la divergencia de KL entre las distribuciones conjuntas:

$$
D_{\mathrm{SNE}}
=
\sum_i\sum_{x\in X} P_{ij}\log\left(\frac{P_{ij}}{Q_{ij}}\right),
\tag{17}
$$

que tienen las propiedades:

$$
p_{ij}=p_{ji}\qquad \forall i,j.
$$

Pero, ¿qué quiere decir esta probabilidad conjunta?

## Diapositiva 86. t-SNE: Simetrización de la Función de Costo

La similaridad SNE en el mapa:

$$
q_{i|j}=
\frac{
\exp\left(-\lVert y_i-y_j\rVert^2/2\sigma_i^2\right)
}{
\sum_{k\neq i}\exp\left(-\lVert y_i-y_k\rVert^2/2\sigma_i^2\right)
}.
\tag{18}
$$

va a ser ahora:

$$
q_{i|j}=
\frac{
\exp\left(-\lVert y_i-y_j\rVert^2\right)
}{
\sum_{k\neq i}\exp\left(-\lVert y_i-y_k\rVert^2\right)
}.
\tag{19}
$$

y en el espacio de datos:

$$
p_{i|j}=
\frac{
\exp\left(-\lVert y_i-y_j\rVert^2/2\sigma_i^2\right)
}{
\sum_{k\neq i}\exp\left(-\lVert y_i-y_k\rVert^2/2\sigma_i^2\right)
}.
\tag{20}
$$

podría ser ahora:

$$
p_{i|j}=
\frac{
\exp\left(-\lVert y_i-y_j\rVert^2/2\sigma\right)
}{
\sum_{k\neq i}\exp\left(-\lVert y_i-y_k\rVert^2/2\sigma\right)
}.
\tag{21}
$$

pero causa problemas cuando hay datos que son outliers, ya que la función de costo casi no se ve afectada. Esto se soluciona redefiniendo una probabilidad conjunta simetrizada:

$$
p_{ij}=\frac{p_{i|j}+p_{j|i}}{2n}.
\tag{22}
$$

## Diapositiva 87. t-SNE: Simetrización de la Función de Costo

$$
p_{ij}=\frac{p_{i|j}+p_{j|i}}{2n}.
\tag{23}
$$

En la versión simetrizada de la función de costo, se cumple que $\sum_j p_{ij}$ es siempre no menor a $1/(2n)$, y por lo tanto cada dato hace una contribución no despreciable a la función de costo.

Esta propuesta tiene la ventaja de que la función de costo,

$$
D_{\mathrm{SNE}}
=
\sum_i\sum_{x\in\mathcal{X}} P_{ij}\log\left(\frac{P_{ij}}{Q_{ij}}\right)
\tag{24}
$$

tiene un gradiente más simple y fácil de calcular:

Antes:

$$
\frac{\partial D_{\mathrm{SNE}}}{\partial y_i}
=
2\sum_j
\left[p_{j|i}-q_{j|i}+p_{i|j}-q_{i|j}\right](y_i-y_j).
\tag{25}
$$

Ahora:

$$
\frac{\partial D_{\mathrm{SNE}}}{\partial y_i}
=
4\sum_j
\left[p_{ji}-q_{ij}\right](y_i-y_j).
\tag{26}
$$

## Diapositiva 88. Crowding Problem

La alta dimensionalidad induce algunos problemas: no se puede modelar perfectamente con puntos en 2 dimensiones una distribución de puntos en $N>2$ dimensiones.

En $N$ dimensiones podemos tener $N+1$ datos equidistantes. No hay manera de modelar esto en un mapa de 2 dimensiones.

Sea un conjunto de datos en un subespacio bidimensional curvo que es aproximadamente lineal en escalas pequeñas, incluido en otro espacio de mayor dimensión. El volumen de una esfera de radio $R$ en $N$ dimensiones escala como $R^N$. Por lo tanto, si en $N$ dimensiones tenemos una distribución de puntos uniforme, para modelarlos en 2 dimensiones hace falta mucho "más espacio".

![Ilustración del crowding problem en t-SNE](figures/clase-17/fig-88-crowding-problem.png){width=65%}
