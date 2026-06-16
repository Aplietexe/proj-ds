---
title: "Más Allá de la Linealidad"
---

## Diapositiva 1

**Portada**

- Más allá de la linealidad
- Ciencia de Datos
- FaMAF
- Clase 13 - 2026-05-12

## Diapositiva 2. Hoja de Ruta

La clase se organiza en tres bloques:

1. **Clasificación como partición del espacio**
   - Clasificación binaria y semiespacios
   - Clasificación multiclase y regiones de decisión
   - Complejidad geométrica de las regiones de Bayes
2. **Estrategias para construir regiones complejas**
   - Aprendizaje de representaciones y transformaciones
   - Modelos aditivos
   - Interacciones
3. **Modelos locales y particiones recursivas**
   - Particionamiento local
   - Particiones rectangulares
   - Partición recursiva y CART
   - Árboles de decisión y CART

## Diapositiva 3. Clasificación como Partición del Espacio

**Sección:** Clasificación como partición del espacio.

## Diapositiva 4. Modelo Estadístico de Clasificación

Sea $(X,Y)$ una variable aleatoria con:

$$
X\in\mathcal{X}\subseteq\mathbb{R}^d,
\qquad
Y\in\mathcal{Y}=\{\omega_1,\ldots,\omega_K\}.
$$

En aprendizaje supervisado observamos una muestra i.i.d.:

$$
\mathcal{D}_n=\{(x_i,y_i)\}_{i=1}^n,
\qquad
(x_i,y_i)\sim P_{X,Y}.
$$

**Regla de clasificación**

Una regla es una función medible $g:\mathcal{X}\to\mathcal{Y}$. Su calidad se evalúa por el riesgo:

$$
R(g)
=
P(g(X)\ne Y)
=
\mathbb{E}\left[\mathbb{I}\{g(X)\ne Y\}\right].
$$

La regla óptima es la regla de Bayes. El problema es construir una regla cuyas regiones de decisión aproximen a las regiones de Bayes.

## Diapositiva 5. Regla de Bayes y Clasificación Binaria

En el caso binario, $\mathcal{Y}=\{\omega_1,\omega_2\}$ y definimos las posteriores:

$$
g_i(x)
=
P(Y=\omega_i\mid X=x)
=
P(\omega_i\mid x)
=
P(x\mid\omega_i)P(\omega_i),
\qquad
i=1,2.
$$

Para pérdida 0-1, la regla óptima es:

$$
g^\star(x)
=
\arg\max_{k\in\{1,2\}} g_k(x).
$$

**Frontera de Bayes (caso binario)**

$$
\mathcal{B}^\star
=
\{x\in\mathcal{X}:g_1(x)=g_2(x)\}.
$$

En binario, clasificar equivale a separar el espacio en dos regiones cuya frontera es el conjunto donde las posteriores empatan.

## Diapositiva 6. Discriminantes Lineales e Hiperplanos

Una familia elemental de reglas binarias modela directamente la frontera de decisión mediante la función discriminante con la forma:

$$
g(x)=w^\top x+w_0,
\qquad
w\in\mathbb{R}^p,
\quad
w_0\in\mathbb{R}.
$$

donde la decisión es:

$$
\omega_1 \text{ si } g(x)>0,
\qquad
\omega_2 \text{ si } g(x)<0.
$$

Las regiones inducidas son:

$$
R_1=\{x:w^\top x+w_0>0\},
\qquad
R_2=\{x:w^\top x+w_0<0\}.
$$

- La frontera $\{x:w^\top x+w_0=0\}$ es un hiperplano.
- Cada región es un semiespacio, luego es convexa.
- La decisión depende de la proyección de $x$ en la dirección normal $w$.

## Diapositiva 7. Interpretación Geométrica

Los clasificadores lineales poseen una interpretación geométrica extremadamente rígida.

Un hiperplano divide $\mathbb{R}^d$ en dos semiespacios convexos. Por lo tanto, una regla lineal binaria solo puede representar clases separables mediante una única frontera global.

Mientras más crezca una variable, más favorece a una de las clases; no hay lugar para interacciones, anidamientos o regiones disconexas.

Esto explica simultáneamente dos hechos:

- su fuerza teórica y computacional;
- su limitación estructural cuando la clase positiva no es un semiespacio.

La pregunta natural es entonces: ¿qué ocurre cuando hay más de dos clases, o cuando las regiones de Bayes no son convexas?

![Separación mediante un SVM lineal](figures/clase-13/fig-07-svm-lineal.png){width=80%}

## Diapositiva 8. ¿No es Kernel SVM También no Lineal?

- **Dualidad espacial:** el clasificador es lineal en el espacio de características $\mathcal{H}$, espacio de Hilbert, pero no lineal en el espacio de entrada $\mathbb{R}^d$.
- El kernel es una implementación eficiente de las funciones de discriminación generalizadas.
- La superficie de decisión es el conjunto:

$$
\mathcal{S}
=
\left\{
x\in\mathcal{X}
\mid
\sum_i \alpha_i y_i K(x_i,x)+b=0
\right\}.
$$

Aunque la frontera en $\mathcal{X}$ sea compleja, la optimización sigue buscando la máxima separación en un espacio vectorial donde rigen las leyes de la geometría euclidiana simple.

La no linealidad es una manifestación de una linealidad en dimensión superior.

![Comparación entre SVM lineal y SVM con kernel RBF](figures/clase-13/fig-08-svm-lineal-rbf.png){width=100%}

## Diapositiva 9. De Dos Clases a K Clases

En multiclase, la regla de Bayes se escribe:

$$
g^\star(x)
=
\arg\max_{1\le k\le K} g_k(x),
\qquad
g_k(x)=P(Y=\omega_k\mid X=x).
$$

Las regiones de decisión de Bayes son:

$$
R_k^\star
=
\{x\in\mathcal{X}:g_k(x)\ge g_j(x)\ \forall j\ne k\}.
$$

- La frontera entre $\omega_k$ y $\omega_\ell$ está contenida en $\{x:g_k(x)=g_\ell(x)\}$.
- La decisión depende del orden completo de $K$ funciones.
- Clasificar equivale a construir una partición del espacio por comparación de discriminantes.

**Cambio conceptual**

En el caso multiclase ya no buscamos el signo de una única función, sino una partición completa del espacio en múltiples regiones competidoras.

![Regiones de decisión en clasificación multiclase](figures/clase-13/fig-09-multiclase-regiones.png){width=70%}

## Diapositiva 10. Particiones a Partir de Datos

La partición del espacio no solo surge de la clasificación multiclase, sino también de la necesidad de aproximar regiones de Bayes complejas a partir de datos.

![Datos de entrenamiento con tres clases](figures/clase-13/fig-10-datos-entrenamiento.png){width=85%}

## Diapositiva 11. Multiclase Lineal: Intersecciones de Semiespacios

Si cada discriminante es lineal:

$$
g_k(x)=w_k^\top x+w_{k0},
$$

entonces:

$$
R_k
=
\bigcap_{j\ne k}
\{x:(w_k-w_j)^\top x+(w_{k0}-w_{j0})\ge 0\}.
$$

**Consecuencia geométrica**

Cada región $R_k$ es una intersección de semiespacios; en consecuencia, es un politopo convexo, posiblemente vacío o no acotado.

La combinación de hiperplanos induce una teselación del espacio, análoga a una descomposición tipo Voronoi cuando los discriminantes provienen de distancias.

![Regiones multiclase como intersecciones de semiespacios](figures/clase-13/fig-11-intersecciones-semiespacios.png){width=75%}

## Diapositiva 12. Clasificar es Particionar el Espacio

Toda regla $g:\mathcal{X}\to\{\omega_1,\ldots,\omega_K\}$ induce una partición en regiones $R_i$:

$$
\mathcal{X}
=
R_1\cup\cdots\cup R_K.
$$

**Nuevo punto de vista**

La diferencia entre métodos de aprendizaje radica, esencialmente, en la geometría de las regiones $R_k$ que son capaces de construir.

A partir de aquí, la clasificación puede leerse como un problema de aproximación geométrica: estimar regiones de Bayes complejas usando familias de particiones estadísticamente manejables.

## Diapositiva 13. Cuando la Geometría de Bayes Deja de Ser Convexa

Aunque:

$$
R_k^\star
=
\{x:g_k(x)\ge g_j(x)\ \forall j\ne k\}
$$

es una definición formalmente simple, su geometría puede ser muy compleja.

- Una clase puede ocupar varias componentes conexas.
- Una región puede rodear completamente a otra.
- Las fronteras pueden presentar alta curvatura local.
- Una mezcla de gaussianas puede inducir múltiples cruces del cociente de verosimilitudes.

Las regiones de Bayes no tienen por qué ser lineales, cuadráticas, convexas ni conexas.

## Diapositiva 14. Del Fallo Lineal a una Nueva Pregunta

Si las regiones de Bayes pueden ser curvadas, anidadas o disconexas, entonces la linealidad global deja de ser suficiente.

**Pregunta directriz**

¿Cómo construir regiones complejas sin abandonar por completo la estructura matemática y estadística?

A partir de esta dificultad emergen tres estrategias generales:

1. cambiar la representación del problema;
2. componer funciones más flexibles conservando una forma global;
3. abandonar la geometría global y particionar localmente.

Casi todos los métodos de *machine learning* son uno o una combinación de estas estrategias.

## Diapositiva 15. Estrategias para Construir Regiones Complejas

**Sección:** Estrategias para construir regiones complejas.

## Diapositiva 16. Cambiar Coordenadas para Recuperar Linealidad

Una primera respuesta consiste en transformar la representación de entrada:

$$
\Phi:\mathbb{R}^p\to\mathbb{R}^M,
\qquad
x\mapsto \Phi(x)=(\phi_1(x),\ldots,\phi_M(x))^\top.
$$

Luego se ajusta una regla lineal en el espacio transformado:

$$
g(x)
=
\beta_0+\sum_{m=1}^M \beta_m\phi_m(x).
$$

**Idea**

La frontera es lineal en el espacio de parámetros y en las coordenadas transformadas, pero puede ser altamente no lineal en el espacio original.

## Diapositiva 17. Expansiones de Base como Objeto Unificador

La forma general:

$$
f(x)
=
\sum_{m=1}^M \beta_m\phi_m(x)
$$

será el objeto unificador.

- Los coeficientes $\beta_m$ se ajustan linealmente.
- La complejidad geométrica está codificada en las funciones base $\phi_m$.
- La familia sigue siendo global: una sola expresión funcional describe todo $\mathcal{X}$.

**Lectura geométrica**

Modificar las bases equivale a modificar la geometría accesible para la frontera de decisión.

## Diapositiva 18. Ejemplos de Transformaciones

Distintas elecciones de bases producen distintas geometrías:

- **Polinomios:** introducen curvatura mediante términos $x_j^2$, $x_jx_\ell$, etc.
- **Bases radiales:** funciones localizadas del tipo:

$$
\phi_m(x)
=
\exp\left(
-
\frac{\lVert x-\mu_m\rVert^2}{2\sigma^2}
\right).
$$

- **Kernels:** evitan construir explícitamente $\Phi(x)$ y operan mediante productos internos en el espacio transformado.

Las regiones ya no se generan por semiespacios en coordenadas originales, sino por la geometría inducida por $\Phi$.

## Diapositiva 19. Ventaja y Límite de la Estrategia Representacional

Las transformaciones permiten linealizar problemas no lineales, pero conservan una restricción importante: la regla sigue siendo global.

**Limitación**

Si la complejidad de la frontera es muy localizada, una familia global debe aumentar su dimensionalidad o su grado en todo el espacio, incluso allí donde la regla verdadera es simple.

![Frontera localizada no lineal](figures/clase-13/fig-19-frontera-localizada.png){width=60%}

Esta observación motiva un paso intermedio: permitir no linealidad global, pero de una forma estructurada y aún interpretable.

## Diapositiva 20. Un Compromiso entre Rigidez y Complejidad Total

Un modelo aditivo asume que la función discriminante tiene la forma:

$$
f(x)
=
\alpha+\sum_{j=1}^p f_j(x_j).
$$

En clasificación binaria, una formulación estándar es:

$$
\log
\frac{P(Y=\omega_1\mid X=x)}
{P(Y=\omega_2\mid X=x)}
=
\alpha+\sum_{j=1}^p f_j(x_j).
$$

**Lectura conceptual**

Permitimos que cada variable se deforme de manera no lineal, pero todavía no permitimos interacciones entre variables.

## Diapositiva 21. Geometría de las Fronteras Aditivas

La regla decide $\omega_1$ cuando:

$$
\alpha+\sum_{j=1}^p f_j(x_j)>0.
$$

Por lo tanto, la frontera está dada por:

$$
\mathcal{B}
=
\left\{
x\in\mathbb{R}^p:
\sum_{j=1}^p f_j(x_j)=-\alpha
\right\}.
$$

- La frontera ya no es un hiperplano.
- La curvatura proviene de funciones univariadas suaves.
- La contribución de cada variable puede estudiarse *ceteris paribus*.

Los modelos aditivos son, así, una aproximación global suave más flexible que la linealidad, pero todavía separable.

## Diapositiva 22. Interpretabilidad y Restricción Estructural

Los modelos aditivos son atractivos porque:

- mantienen interpretabilidad marginal;
- permiten aproximaciones suaves y globales;
- reducen la rigidez de la linealidad sin entrar aún en complejidad arbitraria.

**Restricción clave**

La estructura:

$$
f(x)
=
\alpha+\sum_{j=1}^p f_j(x_j)
$$

impone separabilidad aditiva: la contribución de $x_j$ no puede depender del valor de $x_\ell$.

Esta restricción es precisamente la que falla en problemas gobernados por interacciones.

## Diapositiva 23. Cuando las Variables Dejan de Contribuir Aisladamente

Revisitemos XOR. La etiqueta depende del producto $x_1x_2$, no de las variables por separado.

![XOR en el espacio original y en un espacio transformado](figures/clase-13/fig-23-xor-transformado.png){width=100%}

**Obstáculo estructural**

Ninguna representación puramente aditiva:

$$
f(x)
=
\alpha+f_1(x_1)+f_2(x_2)
$$

puede capturar una dependencia cuya señal cambia solo por combinación de variables.

En términos geométricos, la frontera no puede describirse como una deformación suave obtenida sumando efectos marginales independientes.

## Diapositiva 24. Interacciones, Términos Cruzados y Límites Globales

Una forma clásica de introducir interacciones es ampliar la base con términos cruzados:

$$
f(x)
=
\beta_0
+
\sum_{j=1}^p \beta_j x_j
+
\sum_{j<\ell}\beta_{j\ell}x_jx_\ell
+
\cdots
$$

- Esto incrementa la capacidad geométrica del modelo.
- Pero la complejidad combinatoria crece rápidamente con $p$.
- La forma funcional sigue siendo global: una sola expresión intenta describir todo el espacio.

Cuando la interacción es local o jerárquica, los modelos globales suaves comienzan a volverse poco naturales.

## Diapositiva 25. De las Interacciones a las Particiones Locales

La dificultad no es solo "hacer la función más no lineal". El problema es más profundo: regiones distintas del espacio pueden requerir reglas distintas.

**Nueva estrategia**

En lugar de forzar una única forma funcional global, podemos aproximar la regla de Bayes mediante celdas locales simples, cada una con una decisión elemental.

Esta transición marca el pasaje desde modelos globales a modelos locales.

## Diapositiva 26. Modelos Locales y Particiones Recursivas

**Sección:** Modelos locales y particiones recursivas.

## Diapositiva 27. Abandonar la Forma Funcional Global

Supongamos que particionamos el espacio en celdas:

$$
\mathcal{X}
=
A_1\cup\cdots\cup A_M,
$$

y asignamos una decisión constante a cada una:

$$
g(x)
=
\sum_{m=1}^M c_m\mathbb{I}\{x\in A_m\},
\qquad
c_m\in\mathcal{Y}.
$$

donde $\mathbb{I}$ es la función indicadora, definida como:

$$
\mathbb{I}\{x\in A_m\}
=
\begin{cases}
1, & x\in A_m,\\
0, & x\notin A_m.
\end{cases}
$$

**Interpretación**

La complejidad deja de residir en una única frontera suave y pasa a residir en la geometría de la partición. La regla es ahora una función escalonada, con fronteras que son las fronteras de las celdas.

## Diapositiva 28. Simplicidad Local, Complejidad Global

La aproximación por regiones constantes posee una propiedad decisiva:

- cada celda requiere una regla extremadamente simple;
- el ensamble de muchas celdas puede aproximar fronteras muy complejas;
- la adaptatividad proviene de la partición, no de una expresión analítica global.

**Complejidad local y *bias-variance trade-off***

Celdas pequeñas mejoran resolución geométrica, pero contienen menos datos y aumentan la varianza de las estimaciones locales.

![Partición local de una frontera compleja](figures/clase-13/fig-28-particion-compleja.png){width=90%}

## Diapositiva 29. Aproximación Local de las Posteriores

Si una celda $A_m$ es suficientemente pequeña, puede esperarse que:

$$
P(Y=\omega_k\mid X\in A_m)
\approx
g_k(x),
\qquad
\text{para } x\in A_m.
$$

Entonces tenemos una regla por mayoría local que aproxima localmente la regla de Bayes.

$$
c_m
=
\arg\max_k P(Y=\omega_k\mid X\in A_m).
$$

El problema ahora es geométrico: ¿cómo elegir una partición flexible y computacionalmente tratable?

![Celdas locales y partición rectangular](figures/clase-13/fig-29-celdas-rectangulares.png){width=75%}

## Diapositiva 30. Rectángulos Alineados a Ejes

Una familia natural de celdas en $\mathbb{R}^d$ está dada por rectángulos:

$$
A
=
\prod_{j=1}^d (a_j,b_j],
$$

con extremos eventualmente infinitos.

**Regla por mayoría**

En una celda $A$, la predicción empírica es:

$$
c_A
=
\arg\max_k
\sum_{i:x_i\in A}
\mathbb{I}\{y_i=\omega_k\}.
$$

Las fronteras resultantes son escalonadas y están alineadas con los ejes coordenados.

## Diapositiva 31. Aproximación Rectangular de una Frontera Curva

![Aproximación rectangular de una frontera curva](figures/clase-13/fig-31-aproximacion-rectangular.png){width=65%}

- Una frontera curva puede aproximarse refinando la partición.
- La complejidad geométrica se reemplaza por una complejidad combinatoria.
- La dificultad principal ya no es representar la curva, sino buscar la partición adecuada.

## Diapositiva 32. El Obstáculo Combinatorio

Si permitimos todas las particiones rectangulares posibles, la optimización se vuelve combinatoriamente inabordable.

Para que la idea de partición local sea utilizable, debemos restringir el espacio de particiones a una familia suficientemente rica, pero con una búsqueda tratable algorítmicamente.

Esta necesidad conduce de manera natural a una construcción recursiva basada en divisiones. Aquí estamos restringiendo la geometría de las celdas a cambio de una **estructura de búsqueda eficiente** (algoritmo) y un modelo con buena capacidad de aproximación, que tiene complejidad y admite regularización.

![De particiones arbitrarias a particiones recursivas](figures/clase-13/fig-32-recursive-partition.png){width=80%}

## Diapositiva 33. Ejemplo: Clasificación de la Canasta de Frutas

Debemos decidir qué fruta es en base a atributos:

- color;
- sabor;
- forma;
- tamaño.

![Canasta de frutas](figures/clase-13/fig-33-fruit-basket.png){width=95%}

## Diapositiva 34. Ejemplo: Clasificación de la Canasta de Frutas

La secuencia de decisiones recursivas da lugar a una estructura de árbol, donde cada nodo representa un corte y cada hoja representa una región terminal.

Existen muchas formas de construir árboles para el mismo problema.

![Árbol de decisión para clasificar frutas, primera variante](figures/clase-13/fig-34-fruit-tree-1.png){width=100%}

## Diapositiva 35. Ejemplo: Clasificación de la Canasta de Frutas

La secuencia de decisiones recursivas da lugar a una estructura de árbol, donde cada nodo representa un corte y cada hoja representa una región terminal.

Existen muchas formas de construir árboles para el mismo problema.

![Árbol de decisión para clasificar frutas, segunda variante](figures/clase-13/fig-35-fruit-tree-2.png){width=100%}

## Diapositiva 36. De Rectángulos Arbitrarios a Particiones Recursivas

El algoritmo CART (*Classification and Regression Trees*) restringe la búsqueda a particiones obtenidas por cortes sucesivos de la forma:

$$
x_j\le s
\qquad
\text{versus}
\qquad
x_j>s.
$$

Si una región $A$ se divide por el corte $(j,s)$, las dos nuevas regiones son:

$$
A_L
=
A\cap\{x:x_j\le s\},
\qquad
A_R
=
A\cap\{x:x_j>s\}.
$$

Un árbol de decisión no busca la mejor partición rectangular **global**, sino una secuencia de refinamientos locales recursivos.

Esta restricción hace que la búsqueda sea eficiente, pero no impide que la familia de particiones resultante sea lo suficientemente rica como para aproximar regiones de Bayes complejas.

![Corte recursivo alineado a ejes](figures/clase-13/fig-36-corte-recursivo.png){width=55%}

## Diapositiva 37. CART: Recursión

**Intuición:** si no podemos encontrar una regla global simple, dividamos el espacio $\mathcal{X}$ en celdas pequeñas donde la regla de Bayes sea localmente constante.

**Formulación matemática**

Un árbol de decisión induce una partición $\mathcal{P}=\{R_1,R_2,\ldots,R_m\}$ tal que:

$$
g(x)
=
\sum_{j=1}^m \operatorname{voto}(R_j)\cdot\mathbb{I}(x\in R_j).
$$

- **Criterio de selección de corte:** maximizar la "pureza" de los conjuntos finales.

## Diapositiva 38. CART: Binariedad

Buscar la mejor partición rectangular entre todas las posibilidades es combinatoriamente difícil. CART restringe la búsqueda a particiones binarias obtenidas por cortes recursivos:

$$
x_j\le s
\qquad
\text{versus}
\qquad
x_j>s.
$$

**División binaria**

Cada corte transforma una región $A$ en dos subregiones:

$$
A_L
=
A\cap\{x:x_j\le s\},
\qquad
A_R
=
A\cap\{x:x_j>s\}.
$$

Tras varios cortes, las hojas son rectángulos alineados a ejes.

## Diapositiva 39. Árbol de Decisión como Objeto Matemático

Un árbol binario $T$ define:

- nodos internos $t$, cada uno con un corte $(j_t,s_t)$;
- hijos o ramas izquierdo y derecho definidos por $x_{j_t}\le s_t$ y $x_{j_t}>s_t$;
- nodos terminales u "hojas" $\mathcal{L}(T)$;
- regiones terminales $A_t$, una por cada hoja $t\in\mathcal{L}(T)$;
- una etiqueta $\hat c_t$ para cada hoja $t\in\mathcal{L}(T)$;
- la ruta desde la raíz hasta una hoja es una explicación local de la decisión.

La predicción del árbol puede escribirse como:

$$
g_T(x)
=
\sum_{t\in\mathcal{L}(T)}
c_t\mathbb{I}\{x\in A_t\}.
$$

Cada $A_t$ es la intersección de todas las restricciones acumuladas en la ruta desde la raíz hasta la hoja.

$$
A_m
=
\{x:x_{j_1}\le s_1,\ x_{j_2}>s_2,\ldots,\ x_{j_r}\le s_r\}.
$$

Por ejemplo: no verde + amarillo + no redondo $\longrightarrow$ banana.

El árbol completo induce una partición rectangular de $\mathcal{X}$.

## Diapositiva 40. Predicción en una Hoja

Sea:

$$
N_t
=
\#\{i:x_i\in A_t\},
\qquad
N_{tk}
=
\#\{i:x_i\in A_t,\ y_i=\omega_k\}.
$$

Las frecuencias empíricas son:

$$
\hat p_{tk}
=
\frac{N_{tk}}{N_t}.
$$

Para pérdida 0-1, la decisión empírica óptima en la hoja es:

$$
c_t
=
\arg\max_k \hat p_{tk}.
$$

Esto convierte a cada hoja en un estimador local de las posteriores.

## Diapositiva 41. Impureza y Calidad de un Nodo

Para decidir dónde dividir, CART compara la heterogeneidad de clases en cada nodo.

**Impurezas estándar**

$$
i_{\mathrm{mis}}(t)
=
1-\max_k \hat p_{tk},
$$

$$
i_{\mathrm{Gini}}(t)
=
1-\sum_{k=1}^K \hat p_{tk}^2,
$$

$$
i_{\mathrm{Ent}}(t)
=
-
\sum_{k=1}^K \hat p_{tk}\log\hat p_{tk}.
$$

La división deseable es aquella que produce hijos más puros que el nodo padre.

## Diapositiva 42. Criterio 1: Error de Clasificación

**Motivación:** el riesgo de Bayes local bajo pérdida 0-1.

**Contexto:** si detuviéramos el crecimiento del árbol en un nodo $t$ y debiéramos asignar una etiqueta, la decisión óptima bajo pérdida 0-1 es la clase mayoritaria en dicho nodo.

**Definición (error de clasificación)**

Sea:

$$
\hat p_{tk}
=
\frac{1}{N_t}
\sum_{x_i\in A_t}
\mathbb{I}\{y_i=\omega_k\}
$$

la probabilidad empírica de la clase $\omega_k$ en el nodo $t$. Se define la impureza por error de clasificación como:

$$
i_{\mathrm{mis}}(t)
=
1-\max_k \hat p_{tk}.
\tag{1}
$$

- Mide la probabilidad de error si clasificamos cada punto en el nodo $t$ según la regla de la mayoría local.
- Es una función cóncava pero no estrictamente diferenciable en todos sus puntos. En la práctica de CART, suele ser poco sensible a cambios en las probabilidades que no alteren la clase mayoritaria, lo que dificulta el crecimiento del árbol mediante métodos de descenso.

## Diapositiva 43. Criterio 2: Índice de Impureza de Gini

**Motivación:** varianza de una distribución multinomial.

**Contexto:** en lugar de mirar solo la clase dominante, podemos considerar la variabilidad total de las etiquetas en el nodo. El índice de Gini surge al considerar el error esperado si asignáramos etiquetas al azar siguiendo la distribución de clases del nodo.

**Definición (índice de Gini)**

La impureza de Gini se define como la suma de las varianzas de las variables indicadoras de cada clase:

$$
i_{\mathrm{Gini}}(t)
=
\sum_{k=1}^K \hat p_{tk}(1-\hat p_{tk})
=
1-\sum_{k=1}^K \hat p_{tk}^2.
\tag{2}
$$

**Intuición y propiedades**

- Representa la probabilidad de que un elemento elegido al azar sea clasificado incorrectamente si se le asigna una etiqueta aleatoria según la distribución del nodo.
- Es una función estrictamente cóncava que alcanza su máximo en la incertidumbre total, $\hat p_{tk}=1/K$, y su mínimo, $0$, en nodos puros.
- Es el criterio preferido por el algoritmo CART original debido a su eficiencia computacional, ya que no requiere logaritmos.

## Diapositiva 44. Criterio 3: Entropía Cruzada (Deviance)

**Motivación:** teoría de la información y verosimilitud.

**Contexto:** desde una perspectiva bayesiana, buscamos minimizar la incertidumbre sobre la variable objetivo $Y$ dado que $X$ se encuentra en la región $A_t$. La medida natural de incertidumbre es la entropía de Shannon.

**Definición (entropía o desviación)**

Se define la impureza basada en la información como:

$$
i_{\mathrm{Ent}}(t)
=
-
\sum_{k=1}^K \hat p_{tk}\log_2(\hat p_{tk}).
\tag{3}
$$

Convención: $0\log 0=0$.

**Intuición y conexión estadística**

- Mide el número promedio de bits necesarios para codificar la clase de un objeto en el nodo $t$.
- Minimizar la entropía en los nodos hijos equivale a maximizar la ganancia de información (*Information Gain*) respecto al nodo padre.
- Está íntimamente relacionada con la *log-likelihood*: un árbol que minimiza la entropía está buscando el estimador de máxima verosimilitud para una distribución multinomial local.

## Diapositiva 45. Comparación Numérica de Criterios

Ejemplo en un nodo binario $(\omega_1,\omega_2)$.

Consideremos tres escenarios de distribución de clases en un nodo $t$ con $N_t=100$ muestras:

| Escenario | Puro | Equilibrado | Sesgado |
| --- | --- | --- | --- |
| Distribución $(\hat p_{t1},\hat p_{t2})$ | $(1.0,0.0)$ | $(0.5,0.5)$ | $(0.9,0.1)$ |
| $i_{\mathrm{mis}}(t)$ | $1-1.0=0.0$ | $1-0.5=0.5$ | $1-0.9=0.1$ |
| $i_{\mathrm{Gini}}(t)$ | $1-(1^2+0^2)=0.0$ | $1-(0.5^2+0.5^2)=0.5$ | $1-(0.9^2+0.1^2)=0.18$ |
| $i_{\mathrm{Ent}}(t)$ (base 2) | $-(1\log 1+0)=0.0$ | $-(0.5\log 0.5\times 2)=1.0$ | $-(0.9\log 0.9+0.1\log 0.1)\approx 0.47$ |

**Observaciones clave para el diseño de algoritmos:**

1. En el escenario sesgado, el error de clasificación, $0.1$, es menor que el de Gini, $0.18$, reflejando que el error de clasificación es más optimista o menos sensible a la presencia de clases minoritarias.
2. Gini y entropía penalizan más fuertemente las distribuciones impuras, lo que favorece la creación de nodos hijos más homogéneos durante la búsqueda codiciosa (*greedy search*) de CART.

## Diapositiva 46. Medidas en los Nodos

La diapositiva muestra una comparación visual de métricas de impureza en clasificación: error de clasificación, Gini y entropía, junto con una distribución binaria del nodo.

![Comparación visual de métricas de impureza](figures/clase-13/fig-46-impureza-dashboard.png){width=100%}

## Diapositiva 47. Formalización del Criterio de División en CART

**Definición 1: el parámetro de división $s$**

Sea $x\in\mathcal{X}\subseteq\mathbb{R}^d$ un vector de características. En un nodo $t$, un **corte binario** $s$ se define como el par ordenado:

$$
s=(j,\tau)\in\{1,\ldots,d\}\times\mathbb{R}
$$

donde $j$ indexa la dimensión del espacio y $\tau$ es el umbral de decisión local. Este par induce una partición de la región $A_t\subseteq\mathcal{X}$ en dos subregiones disjuntas:

$$
A_L=A_t\cap\{x\mid x_j\le\tau\},
\qquad
A_R=A_t\cap\{x\mid x_j>\tau\}.
$$

**Definición 2: el conjunto de cortes candidatos $S_t$**

Sea $\mathcal{D}_t=\{(x_1,y_1),\ldots,(x_{N_t},y_{N_t})\}$ el subconjunto de datos que alcanzan el nodo $t$. El espacio de búsqueda de cortes admisibles, $S_t$, se define formalmente como:

$$
S_t
=
\bigcup_{j=1}^d
\left\{
(j,\tau):
\tau=
\frac{x_{(i)j}+x_{(i+1)j}}{2},
\ i=1,\ldots,N_t-1
\right\}.
$$

donde $x_{(i)j}$ representa el $i$-ésimo estadístico de orden de la componente $j$ en $\mathcal{D}_t$.

## Diapositiva 48. Criterio de División en CART

Para un nodo $t$ y un corte admisible $s=(j,\tau)$, denotemos por $t_L,t_R$ a los hijos inducidos. La impureza posterior ponderada es:

$$
I(s,t)
=
\frac{N_{t_L}}{N_t}i(t_L)
+
\frac{N_{t_R}}{N_t}i(t_R).
$$

La ganancia de impureza es:

$$
\Delta i(s,t)
=
i(t)-I(s,t).
$$

**Selección codiciosa (algoritmo *greedy*)**

$$
s^\star(t)
=
\arg\max_{s\in S_t}\Delta i(s,t).
$$

![Curvas de Gini ponderado para cortes candidatos](figures/clase-13/fig-48-gini-cortes.png){width=85%}

## Diapositiva 49. Búsqueda de Cortes Candidatos

Para una variable continua $x_j$, los cortes relevantes se ubican entre valores observados ordenados:

$$
x_{(1)j}\le\cdots\le x_{(N_t)j},
$$

y los candidatos típicos son:

$$
\tau_r
=
\frac{x_{(r)j}+x_{(r+1)j}}{2},
\qquad
r=1,\ldots,N_t-1.
$$

- Se evalúan todos los cortes admisibles.
- El mejor corte se elige localmente.
- La construcción es *greedy*: no garantiza el óptimo global.

Esta heurística es precisamente lo que vuelve computable a la partición recursiva.

## Diapositiva 50. Algoritmo de Crecimiento

1. Comenzar con la raíz que contiene toda la muestra.
2. En cada nodo, calcular frecuencias $\hat p_{tk}$ e impureza $i(t)$.
3. Enumerar cortes admisibles $s=(j,\tau)$.
4. Elegir $s^\star(t)$ que maximiza $\Delta i(s,t)$.
5. Dividir el nodo si la mejora y los tamaños mínimos lo justifican.
6. Repetir recursivamente hasta alcanzar una regla de detención.

La recursión surge como la forma natural de construir particiones locales complejas a partir de divisiones binarias simples.

## Diapositiva 51. Sobreajuste y Poda

Un árbol grande puede adaptar su partición a fluctuaciones muestrales:

- el error de entrenamiento decrece monótonamente al crecer el árbol;
- hojas pequeñas producen estimaciones locales de alta varianza;
- pequeñas perturbaciones de datos pueden modificar cortes tempranos.

CART controla esta complejidad mediante poda por costo-complejidad:

$$
R_\alpha(T)
=
R(T)+\alpha\lvert\mathcal{L}(T)\rvert,
\qquad
\alpha\ge 0.
$$

La poda selecciona, entre subárboles anidados, aquel que mejor equilibra ajuste y complejidad.

## Diapositiva 52. CART como Estrategia de Aproximación de Bayes

Si las regiones terminales son localmente pequeñas pero contienen suficientes datos, entonces:

$$
\hat p_{tk}
\approx
P(Y=\omega_k\mid X\in A_t)
\approx
g_k(x),
\qquad
\text{para } x\in A_t.
$$

**Lectura estadística**

CART aproxima las regiones de Bayes reemplazando una frontera potencialmente complicada por una partición adaptativa de celdas rectangulares.

El problema de clasificación vuelve así a su forma central: aproximar una partición desconocida del espacio por una familia geométrica computable.

## Diapositiva 53. Mapa Conceptual Unificado

Cada paso relaja una restricción geométrica de la familia anterior.

![Mapa conceptual unificado de estrategias geométricas](figures/clase-13/fig-53-mapa-conceptual.png){width=65%}

## Diapositiva 54. Comparación entre Estrategias

| Método | Objeto central | Geometría | Alcance |
| --- | --- | --- | --- |
| Lineal | $w^\top x+w_0$ | Hiperplanos | Global |
| Bases / kernels | $\sum_m\beta_m\phi_m(x)$ | Geometría transformada | Global |
| Aditivo | $\alpha+\sum_j f_j(x_j)$ | Superficies suaves separables | Global |
| CART | $\sum_t c_t\mathbb{I}\{x\in A_t\}$ | Rectángulos recursivos | Local |

La principal diferencia entre estos enfoques es cómo cada método construye regiones de decisión. El algoritmo de ajuste es un detalle técnico que se adapta a la geometría de cada familia, pero la esencia de cada método radica en la forma de las regiones que puede construir, y las limitaciones que esto impone sobre la aproximación de la regla de Bayes.

## Diapositiva 55. Idea Unificadora

La historia del aprendizaje estadístico puede leerse como una relajación progresiva de restricciones geométricas sobre las regiones de decisión.

- Los clasificadores lineales particionan mediante semiespacios.
- Las transformaciones cambian la geometría accesible sin abandonar una regla global.
- Los modelos aditivos permiten curvatura suave, pero todavía separable, y con problemas para las regiones que son localmente complejas.
- Los árboles de decisión son el primer ejemplo de modelo que reemplaza la forma global por una construcción local y recursiva de regiones.

Sin embargo, todo sigue la misma idea unificadora: **clasificar es particionar el espacio de características**.

## Diapositiva 56. Referencias Sugeridas

Estas referencias cubren discriminantes clásicos, geometría de regiones, modelos aditivos y partición recursiva.

- Duda, Hart y Stork. *Pattern Classification*. Wiley.
- Breiman, Friedman, Olshen y Stone. *Classification and Regression Trees*. Wadsworth.
- Hastie, Tibshirani y Friedman. *The Elements of Statistical Learning*. Springer.
- James, Witten, Hastie y Tibshirani. *An Introduction to Statistical Learning*. Springer.
