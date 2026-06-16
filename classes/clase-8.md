---
title: "Modelos Lineales de Clasificación: Perceptrón, Regresión Logística y SVM"
---

## Diapositiva 1

**Portada**

- Ciencia de Datos - Clase 8
- FaMAF
- Abril 2026

## Diapositiva 2

La diapositiva muestra una imagen de un robot humanoide en un entorno industrial, como introducción visual al tema histórico del perceptrón y las máquinas capaces de reconocer su entorno.

![Robot humanoide en una fábrica](figures/clase-8/fig-02-robot-factory.png)

## Diapositiva 3

Sobre la misma imagen introductoria aparece la cita:

> "Yet we are about to witness the birth of such a machine - a machine capable of perceiving, recognizing and identifying its surroundings without any human training or control."

![Robot humanoide en una fábrica](figures/clase-8/fig-02-robot-factory.png)

## Diapositiva 4

Se completa la cita anterior con su atribución:

> "Yet we are about to witness the birth of such a machine - a machine capable of perceiving, recognizing and identifying its surroundings without any human training or control."

Frank Rosenblatt, 1958.

![Robot humanoide en una fábrica](figures/clase-8/fig-02-robot-factory.png)

## Diapositiva 5. Hoja de Ruta de la Clase

**¿Dónde estamos en la materia?**

- **Clases 1-5:** asumimos formas paramétricas, como Bayes gaussiano.
- **Clase 6:** cambiamos la geometría del espacio mediante PCA/FDA.
- **Clase 7:** abandonamos gaussianidad y dejamos que el dato "hable", por ejemplo con k-NN.
- **Hoy:** revisamos distintas opciones de la función a optimizar.
- **Próxima clase:** se introduce el rigor estadístico de la evaluación empírica para analizar si lo anterior no es una ilusión.

## Diapositiva 6. Hoja de Ruta de la Clase

La clase se organiza en tres bloques:

1. **Repaso**
2. **Modelos lineales de clasificación**
   - Perceptrón
   - Regresión logística
   - SVM
3. **Descenso por el gradiente y convergencia**
   - Mapeo y espacio de pesos

## Diapositiva 7. Repaso

**Sección:** Repaso.

## Diapositiva 8. El Cambio de Paradigma: De lo Local a lo Global

Pasamos de intentar estimar distribuciones a tratar de estimar directamente las fronteras. Ante la dificultad de una descripción global, en la clase anterior se recurrió a decisiones basadas en un entorno local.

- **Parzen, k-NN:** decisión local, memoria $O(n)$, geometría de Voronoi compleja.
- **Nuevo objetivo:** encontrar una única frontera global, simple y paramétrica, sin estimar densidades de probabilidad.

![Comparación entre decisiones locales y fronteras globales](figures/clase-8/fig-08-local-global-boundaries.png)

## Diapositiva 9. Definición del Problema

Para encontrar una frontera, hay que decidir:

- ¿existe una frontera única y óptima?
- ¿es posible separar las clases fijando la familia paramétrica de la frontera?

Motivación:

- queremos una frontera simple y paramétrica;
- queremos una frontera que se ajuste a los datos;
- no queremos guardar todos los vecinos;
- en k-NN, cada punto nuevo requiere recorrer todos los datos.

![Familias posibles de fronteras sobre una nube de dos clases](figures/clase-8/fig-09-frontier-families.png)

## Diapositiva 10. Modelos Lineales de Clasificación

**Sección:** Modelos lineales de clasificación.

## Diapositiva 11. Clases Separables con Frontera Lineal

Para comenzar se asume que:

- las clases son separables;
- la frontera de decisión es un hiperplano.

Si sabemos de antemano que las clases pueden separarse por un hiperplano, no es necesario calcular $p(x \mid \omega_i)$ ni guardar los vecinos. Solo debemos guardar los parámetros.

Idea:

- definir la forma de la frontera $g(x)=0$;
- usar los datos para ajustar sus parámetros.

Cuando asumimos que la función discriminante es lineal en los parámetros o en funciones de los parámetros, hablamos de **funciones lineales de discriminación**.

## Diapositiva 12. Funciones Discriminantes Lineales

Definimos la función discriminante como una combinación lineal de las características:

$$
g(x)=w^T x+w_0,
$$

donde $w$ es el vector de pesos y $w_0$ es el sesgo (*bias* o *threshold*).

La ecuación $g(x)=0$ define un hiperplano de decisión $H$. El vector $w$ es normal, u ortogonal, a cualquier vector contenido en $H$.

Regla de decisión para dos clases:

- decidir $\omega_1$ si $g(x)>0$;
- decidir $\omega_2$ si $g(x)<0$.

## Diapositiva 13. Geometría del Discriminante Lineal: El Caso de Dos Categorías

Una función discriminante lineal se define como:

$$
g(x)=w^T x+w_0.
$$

Donde $w$ es el vector de pesos y $w_0$ es el sesgo.

- La ecuación $g(x)=0$ define la superficie de decisión $H$, un hiperplano.
- Si $x_1$ y $x_2$ están en $H$, entonces:

$$
w^T x_1+w_0=w^T x_2+w_0
\quad \Longrightarrow \quad
w^T(x_1-x_2)=0.
$$

**Propiedad fundamental:** el vector de pesos $w$ es normal al hiperplano de decisión $H$.

## Diapositiva 14. Distancia Algebraica y Proyección

Cualquier vector $x$ puede expresarse como su proyección sobre $H$, denotada $x_p$, más su distancia al hiperplano:

$$
x=x_p+r\frac{w}{\lVert w\rVert}.
$$

Donde $r$ es la distancia algebraica de $x$ a $H$.

Dado que $g(x_p)=0$, al evaluar $g(x)$ se obtiene:

$$
g(x)
=
w^T\left(x_p+r\frac{w}{\lVert w\rVert}\right)+w_0
=
r\lVert w\rVert.
$$

Por lo tanto:

$$
r=\frac{g(x)}{\lVert w\rVert}.
$$

La distancia desde el origen al hiperplano es:

$$
\frac{w_0}{\lVert w\rVert}.
$$

## Diapositiva 15. Distancia Algebraica y Proyección

La figura ilustra la descomposición geométrica de un punto $x$ en su proyección sobre el hiperplano y una componente normal, asociada a la distancia algebraica $r$.

![Distancia algebraica de un punto a un hiperplano](figures/clase-8/fig-15-algebraic-distance.png)

## Diapositiva 16. Distancia Algebraica y Proyección

La figura muestra la misma idea en tres dimensiones: el hiperplano $H$ separa las regiones $R_1$ y $R_2$, el vector $w$ es normal a $H$, y $r$ mide la distancia algebraica desde $x$ hasta su proyección $x_p$.

![Geometría del hiperplano, la normal y la distancia algebraica](figures/clase-8/fig-16-hyperplane-distance.png)

## Diapositiva 17. Extensión al Caso Multicategoría: Máquinas Lineales

Cuando hay $c>2$ clases, se definen $c$ funciones discriminantes:

$$
g_i(x)=w_i^T x+w_{i0},
\qquad
i=1,\ldots,c.
$$

**Regla de decisión (máquina lineal):** asignar $x$ a $\omega_i$ si

$$
g_i(x)>g_j(x)
\qquad
\text{para todo } j\ne i.
$$

Propiedades:

- las regiones de decisión $R_i$ son convexas;
- la frontera entre regiones contiguas $R_i$ y $R_j$ es un segmento del hiperplano $H_{ij}$ definido por:

$$
g_i(x)=g_j(x)
\quad \Longrightarrow \quad
(w_i-w_j)^T x+(w_{i0}-w_{j0})=0.
$$

## Diapositiva 18. Caso Multiclase

Para $c$ clases podemos usar:

$$
g_i(x)=w_i^T x+w_{i0},
\qquad
i=1,\ldots,c.
$$

La regla de decisión es:

$$
\delta(x)=\arg\max_i g_i(x).
$$

Las fronteras entre clases son intersecciones de hiperplanos pares a pares.

## Diapositiva 19. Clasificación Multiclase

En la formulación multiclase, cada clase tiene un discriminante lineal propio y la decisión depende de cuál de ellos es máximo. Esto puede verse como una colección de detectores lineales compitiendo entre sí.

La idea central es que varias funciones lineales coordinadas pueden construir regiones de decisión poliedrales.

![Esquemas de clasificación multiclase mediante discriminantes lineales](figures/clase-8/fig-19-multiclass-discriminants.png)

## Diapositiva 20. Notación: El Vector Aumentado

Manejar el término independiente $w_0$ es algebraicamente tedioso. Para evitarlo, se usa un mapeo a un espacio de características aumentado de dimensión $d+1$:

$$
y=
\begin{bmatrix}
1\\
x_1\\
\vdots\\
x_d
\end{bmatrix},
\qquad
a=
\begin{bmatrix}
w_0\\
w_1\\
\vdots\\
w_d
\end{bmatrix}.
$$

En este nuevo espacio, el hiperplano pasa por el origen y la función discriminante se simplifica a un producto interno:

$$
g(x)=a^T y.
$$

El problema de optimización consiste en encontrar los parámetros $a$ que mejor separen las clases en el espacio aumentado.

## Diapositiva 21. Historia: Frank Rosenblatt y el Mark I

En 1958, el psicólogo Frank Rosenblatt construyó el **Perceptrón Mark I**. Era una máquina física de 5 toneladas llena de cables y potenciómetros.

![Frank Rosenblatt junto al Perceptrón Mark I](figures/clase-8/fig-21-rosenblatt-mark-i.png)

El *New York Times* reportó que la máquina pronto "caminaría, hablaría, vería, escribiría y sería consciente de su existencia".

**Innovación:** no necesitaba que un programador escribiera las reglas lógicas; la máquina ajustaba sus propias conexiones, o pesos, basándose en los errores que cometía.

## Diapositiva 22. Normalización de las Muestras

Para simplificar el algoritmo, se aplica un truco algebraico a las muestras de entrenamiento $\mathcal{D}$.

Queremos que:

$$
a^T y_i>0
\quad \text{si } y_i\in\omega_1,
$$

$$
a^T y_i<0
\quad \text{si } y_i\in\omega_2.
$$

**Normalización:** si $y_i\in\omega_2$, se reemplaza por su negativo $-y_i$.

El problema de aprendizaje se reduce a buscar un único vector de pesos $a$ tal que:

$$
a^T y_i>0
\qquad
\forall i\in\{1,\ldots,n\}.
$$

Buscamos el vector $a$ que hace un ángulo agudo con todas las muestras normalizadas.

## Diapositiva 23. Normalización de las Muestras

La figura muestra cómo la normalización transforma el problema en encontrar una región de solución para $a$ en el espacio de pesos.

![Región de solución en el espacio de pesos para muestras normalizadas](figures/clase-8/fig-23-solution-cones.png)

## Diapositiva 24. Cono de Solución

La intersección de todos los semiespacios

$$
\{a:a^T y_i>0\}
$$

forma el conjunto de soluciones.

Si los datos son linealmente separables, este conjunto es no vacío y tiene estructura de cono. Si no lo son, el cono desaparece.

## Diapositiva 25. Función de Pérdida

En clasificación lineal, buscamos un vector de pesos $a$ que minimice un criterio escalar $J(a)$.

El problema general se define como:

$$
J(a)=\sum_{i=1}^n \Phi(a^T y_i).
\tag{1}
$$

Donde $y_i$ es el vector de características aumentado y normalizado, y $\Phi(\cdot)$ es la función de pérdida o castigo.

Preguntas:

- ¿cómo definimos $\Phi$ para que el aprendizaje sea estable, robusto o probabilísticamente interpretable?
- ¿existe un vector $a$ que satisfaga todas las restricciones a la vez?

## Diapositiva 26. Criterio del Perceptrón

Rosenblatt introdujo el **criterio del perceptrón**. Tomamos la función de pérdida $\Phi(z)$ como:

$$
\Phi(a^T y_i)=
\begin{cases}
-a^T y_i & \text{si } a^T y_i<0,\\
0 & \text{si } a^T y_i\ge 0.
\end{cases}
$$

O bien:

$$
\Phi(a^T y_i)=\max(0,-z),
\qquad
z=a^T y_i.
$$

Luego:

$$
J_p(a)=\sum_{y\in\mathcal{Y}}(-a^T y),
$$

donde $\mathcal{Y}$ es el conjunto de muestras mal clasificadas por $a$.

Si $y$ está mal clasificada, $a^T y\le 0$, por lo que $-a^T y$ es positivo. Además, $J_p\ge 0$, y $J_p=0$ si y solo si todas las muestras están bien clasificadas.

Lo que buscamos es minimizar el número total de errores.

## Diapositiva 27. Limitación: Separabilidad Lineal

Históricamente, el perceptrón es el punto de partida. Solo castiga las muestras mal clasificadas, es decir aquellas con $a^T y_i\le 0$.

- **Geometría:** el gradiente
  $$
  \nabla J_p=-\sum_{y\in\mathcal{Y}}y
  $$
  empuja a $a$ en dirección a las muestras erróneas.
- **Limitación:** si los datos son linealmente separables, converge; si no, oscila indefinidamente. No tiene noción de margen.
- **Limitación:** no modela incertidumbre ni probabilidades, solo una decisión dura.
- **Limitación matemática:** si el conjunto no es linealmente separable, el algoritmo de aprendizaje del perceptrón no converge.

Ejemplo clásico de fallo: el problema XOR en $\mathbb{R}^2$.

![Funciones lógicas AND, NAND, OR y XOR vistas como problemas de separación lineal](figures/clase-8/fig-27-xor-logic.png)

## Diapositiva 28. XOR

Consideremos la tabla:

| $x_1$ | $x_2$ | clase |
|---:|---:|:---:|
| $0$ | $0$ | $-$ |
| $0$ | $1$ | $+$ |
| $1$ | $0$ | $+$ |
| $1$ | $1$ | $-$ |

No existe una única recta en $\mathbb{R}^2$ que separe ambas clases. Las muestras positivas están en una diagonal y las negativas en la otra.

Cualquier hiperplano divide el plano en dos semiespacios convexos, pero el conjunto positivo de XOR no es convexamente separable del negativo por una sola frontera lineal.

## Diapositiva 29. Regresión Logística y el Perceptrón

En lugar de una discontinuidad, usamos una función sigmoidea para modelar $P(\omega_1\mid x)$.

**Log-verosimilitud negativa (cross-entropy):**

$$
\Phi_{\text{logit}}(z)=\ln(1+\exp(-z)),
\qquad
z=a^T y_i.
$$

Propiedades:

- es una función convexa y diferenciable en todo su dominio;
- castiga incluso a las muestras bien clasificadas si están cerca de la frontera, forzando al modelo a ganar confianza.

Origen histórico:

- pregunta original del siglo XIX: ¿cómo crecen las poblaciones con recursos limitados?
- modelo propuesto por Verhulst en la década de 1830;
- introduce la función logística;
- el crecimiento no es indefinido: inicialmente es exponencial, luego se desacelera y finalmente se satura.

## Diapositiva 30. Regresión Logística como Función de Criterio

Siguiendo la estructura general para discriminantes lineales:

$$
J(a)=\sum_{i=1}^n \Phi(a^T y_i).
$$

Para la regresión logística, la función de penalización se define como:

$$
\Phi(z)=\ln(1+\exp(-z)).
$$

Donde

$$
z=a^T y_i
$$

representa el margen escalar de la muestra normalizada.

- Si $a^T y_i\gg 0$, la muestra está correctamente clasificada con alta confianza y $\Phi(z)\to 0$.
- Si $a^T y_i\ll 0$, la muestra está mal clasificada y la penalización crece de forma lineal:

$$
\Phi(z)\approx -z.
$$

## Diapositiva 31. Equivalencia con la Verosimilitud (MLE)

Esta $\Phi$ es equivalente al negativo del *log-likelihood*. Partiendo de la probabilidad logística:

$$
P(\omega_1\mid y)=\frac{1}{1+\exp(-a^T y)}.
$$

El negativo del log-likelihood para una muestra normalizada $y_i$ es:

$$
\begin{aligned}
-\ln P(\text{correcta}\mid y_i)
&=
-\ln\left(\frac{1}{1+\exp(-a^T y_i)}\right)\\
&=
\ln(1+\exp(-a^T y_i)).
\end{aligned}
$$

Conclusión: minimizar la suma de estas funciones $\Phi$ es idéntico a maximizar la verosimilitud conjunta bajo el supuesto de independencia.

## Diapositiva 32. Comparativa de Funciones de Criterio

La familia de discriminantes lineales puede verse según la elección de $\Phi(z)$:

| Algoritmo | Función $\Phi(z)$ |
|---|---|
| Perceptrón | $\max(0,-z)$ |
| Regresión logística | $\ln(1+e^{-z})$ |

A diferencia del perceptrón, la función $\Phi$ logística es continuamente diferenciable, lo que permite usar métodos de optimización de segundo orden.

## Diapositiva 33. Transformación Logit

**Definición:**

$$
\operatorname{logit}(p)=\log\left(\frac{p}{1-p}\right).
$$

Propiedades:

- lleva $(0,1)$ a $\mathbb{R}$;
- permite usar modelos lineales.

**Modelo:**

$$
\log\left(\frac{p(x)}{1-p(x)}\right)=w^T x+b.
$$

La función logit puede usarse como inversa de la sigmoide. Sea $P(\omega_1\mid x)=p$. Definimos la función logit como el logaritmo de la razón de probabilidades, o *log-odds*:

$$
\operatorname{logit}(p)=\ln\left(\frac{p}{1-p}\right).
$$

En regresión logística, igualamos el logit a nuestra función lineal:

$$
\log\left(\frac{P(\omega_1\mid x)}{1-P(\omega_1\mid x)}\right)=w^T x+b.
$$

## Diapositiva 34. Derivación de la Función de Pérdida $\Phi$ desde el Logit

Consideremos una muestra normalizada $y_i$, donde ya se absorbió el signo de la clase. Queremos maximizar la probabilidad de acierto.

1. La probabilidad de acierto es:

$$
P(\text{correcta})=\sigma(a^T y_i).
$$

2. Por definición de la sigmoide:

$$
P=\frac{1}{1+e^{-a^T y_i}}.
$$

3. Para minimizar el error, minimizamos el logaritmo negativo:

$$
\Phi(a^T y_i)
=
-\ln\left(\frac{1}{1+e^{-a^T y_i}}\right).
$$

4. Usando propiedades de logaritmos:

$$
\Phi(a^T y_i)=\ln(1+e^{-a^T y_i}).
$$

Resultado: la función de pérdida es el logaritmo del denominador de la sigmoide, la cual es la inversa del logit.

## Diapositiva 35. Interpretación en el Espacio de Decisión

- **Logit $a^T y$:** representa la evidencia neta a favor de la clase $\omega_1$. Es una medida de distancia algebraica al hiperplano de decisión.
- **Probabilidad $\sigma(a^T y)$:** es la confianza de que la muestra pertenezca a dicha clase.

Cuando $a^T y=0$, el logit es $0$, lo que implica:

$$
P(\omega_1\mid x)=0.5.
$$

Este es exactamente el límite de decisión bayesiano para pérdidas simétricas en Duda, Hart & Stork.

## Diapositiva 36. La Función Logística

**Modelo:**

$$
p(x)=\frac{1}{1+e^{-x}}.
$$

Propiedades:

- rango: $(0,1)$;
- forma sigmoidea, en "S";
- interpretable como probabilidad.

**Insight:** es una transformación suave que lleva

$$
\mathbb{R}\to(0,1).
$$

## Diapositiva 37. El Problema Estadístico

**Objetivo:** modelar la probabilidad de un evento.

**Problema:** la probabilidad está acotada:

$$
0\le p\le 1.
$$

**Idea:** transformar la probabilidad a la recta real.

## Diapositiva 38. Regresión Logística

**Modelo final:**

$$
p(y=1\mid x)=\frac{1}{1+e^{-(w^T x+b)}}.
$$

Interpretación:

- modelo probabilístico;
- frontera de decisión lineal.

Decisión:

$$
y=
\begin{cases}
1 & \text{si } p(x)>0.5,\\
0 & \text{caso contrario.}
\end{cases}
$$

## Diapositiva 39. Comparación Conceptual con Perceptrón

| Modelo | Salida | Naturaleza |
|---|---|---|
| Perceptrón | $0/1$ | Determinística |
| Regresión logística | Probabilidad | Probabilística |

**Insight:** la regresión logística es una versión suave del perceptrón.

## Diapositiva 40. ¿Cómo Aprendemos los Parámetros?

Enfoques distintos:

- **Perceptrón:** regla de actualización basada en errores.
- **Regresión logística:** máxima verosimilitud.

## Diapositiva 41. Función de Pérdida

**Log-loss (cross-entropy):**

$$
L(w)
=
-\sum_i
\left[
y_i\log p_i+(1-y_i)\log(1-p_i)
\right].
$$

Propiedades:

- convexa;
- diferenciable;
- permite usar gradiente descendente.

## Diapositiva 42. Una Visión Unificada

Tres formas de ver el mismo problema:

- **Geométrica:** perceptrón.
- **Probabilística:** regresión logística.
- **Optimización:** minimización de pérdidas.

Mensaje final:

> Clasificar = modelar + decidir + optimizar.

## Diapositiva 43. Ejemplo Numérico: Evaluación de $J(a)$

Se consideran:

$$
y_1=[1,2]^T,
\qquad
y_2=[-1,1]^T,
$$

y se prueba con el vector de pesos:

$$
a=[0.5,1]^T.
$$

![Visualización del discriminante lineal para dos puntos](figures/clase-8/fig-43-linear-discriminant-example.png)

## Diapositiva 44. Ejemplo Numérico: Evaluación de $J(a)$

**Perceptrón:**

$$
g_1=a^T y_1=2.5,
\qquad
g_2=a^T y_2=0.5.
$$

Como $g_i>0$, el costo es:

$$
J_p(a)=0.
$$

El modelo está satisfecho.

**Regresión logística:**

La penalidad es:

$$
z_i=\ln(1+e^{-g_i}).
$$

Entonces:

$$
z_1=\ln(1+e^{-2.5})=0.078,
$$

$$
z_2=\ln(1+e^{-0.5})=0.474.
$$

Costo total:

$$
J_L(a)=0.552.
$$

El modelo busca reducir este valor.

Conclusión: mientras el perceptrón ignora los puntos bien clasificados, la logística sigue ajustando $a$ para aumentar el margen de confianza.

## Diapositiva 45. Ejemplo 2D: Cálculo Detallado de Costos

Datos:

$$
\omega_1=\{(1,1),(2,0)\},
\qquad
\omega_2=\left\{(0,2),(-1,1),\left(\frac{1}{2},3\right)\right\}.
$$

Modelo propuesto:

$$
a=[-1,1,0.5]^T
\quad \Longrightarrow \quad
g(x)=-1+x_1+0.5x_2.
$$

![Ejemplo 2D de frontera lineal y costos de clasificación](figures/clase-8/fig-45-cost-example-2d.png)

## Diapositiva 46. Ejemplo Numérico: Evaluación de $J(a)$

| Muestra | $y_i$ aumentado | $a^T y_i$ | Perceptrón (error) | Logística (coste) |
|---|---|---:|---:|---:|
| $x_1$ | $[1,1,1]^T$ | $0.5$ | $0$ | $0.474$ |
| $x_2$ | $[1,2,0]^T$ | $1.0$ | $0$ | $0.313$ |
| $x_3$ | $[-1,0,-2]^T$ | $0.0$ | $0$ | $0.693$ |
| $x_4$ | $[-1,1,-1]^T$ | $1.5$ | $0$ | $0.201$ |
| $x_5$ | $[-1,-0.5,-3]^T$ | $-1.0$ | $1.0$ | $1.313$ |
| **Total** |  |  | **$1.0$** | **$2.994$** |

Observaciones:

- el perceptrón solo se ve afectado por $y_5$, y marginalmente por $y_3$;
- la regresión logística penaliza fuertemente a $y_5$, pero también "siente" la inseguridad de $y_3$, que está sobre la frontera.

Interpretación:

- la línea negra sólida es el lugar geométrico donde $a^T y=0$;
- el punto $(0,2)$ cae exactamente sobre ella, por eso su costo de perceptrón es cero, aunque la logística le asigna una penalidad alta de incertidumbre $\ln(2)$;
- si se trazara el vector $[a_1,a_2]^T=[1,0.5]^T$ desde la frontera, apuntaría perpendicularmente hacia la región azul;
- el punto rojo en $(0.5,3)$ queda atrapado en la zona azul y "tira" de la frontera hacia arriba durante el gradiente descendente.

## Diapositiva 47. Limitación: Linealidad

Se asume que las log-probabilidades de las densidades son lineales en $x$:

$$
\ln\frac{P(\omega_1\mid x)}{P(\omega_2\mid x)}
=
w^T x+w_0.
$$

Ventajas sobre el perceptrón:

- minimiza la entropía cruzada, o *maximum likelihood*;
- converge incluso si las clases se solapan;
- **fallo:** la frontera de decisión
  $$
  \{x:P(\omega_1\mid x)=0.5\}
  $$
  sigue siendo un hiperplano.

## Diapositiva 48. Transición hacia Modelos Más Complejos

Tres formas de avanzar:

- cambiar la función de pérdida $\to$ SVM;
- cambiar la base de funciones $\to$ redes neuronales;
- cambiar la distribución $\to$ modelos generativos.

Idea clave:

> La regresión logística es un punto de encuentro.

## Diapositiva 49. SVM y el Salto No Lineal

Para resolver fronteras complejas, SVM maximiza el margen:

$$
\min_{w,b}\frac{1}{2}\lVert w\rVert^2
\quad
\text{sujeto a }
y_i\left(w^T\phi(x_i)+b\right)\ge 1.
$$

Puntos clave:

- **Mapeo no lineal:** $x\mapsto \phi(x)$ lleva los datos a una dimensión donde son separables.
- **Consistencia:** relaciona la minimización del error empírico con la complejidad del modelo, vía teoría VC.
- **Resultado:** capacidad de resolver XOR y distribuciones concéntricas mediante kernels, por ejemplo RBF o polinomial.

## Diapositiva 50. La Búsqueda del Hiperplano Ideal

Hasta ahora se estimaron densidades $p(x\mid \omega_i)$. Si las densidades son gaussianas con $\Sigma_i=\Sigma$, la frontera es un hiperplano.

Pregunta fundamental:

- ¿podemos encontrar ese hiperplano directamente, sin asumir distribuciones?

El problema:

$$
\mathcal{D}=\{(y_1,z_1),\ldots,(y_n,z_n)\}.
$$

Buscamos un vector $a$ tal que:

$$
a^T y_i>0
\qquad
\forall i,
$$

donde $y$ es el vector aumentado y las muestras están normalizadas.

## Diapositiva 51. Maximización del Margen

La figura muestra el hiperplano óptimo como aquel que maximiza el margen entre las dos clases.

![Hiperplano óptimo y margen máximo](figures/clase-8/fig-51-maximum-margin.png)

## Diapositiva 52. ¿Son las Clases Separables?

**Definición (separabilidad lineal):** un conjunto de muestras es linealmente separable si existe un vector $a$ tal que

$$
a^T y_i>0
$$

para todas las muestras.

Casos:

- **Caso separable:** existe un cono de solución en el espacio de pesos.
- **Caso no separable:** las restricciones son contradictorias, como en XOR.
- **Consecuencia:** si no hay separabilidad, el perceptrón original oscilará infinitamente. Necesitamos funciones de criterio más robustas.

## Diapositiva 53. Más Allá del Perceptrón: El Problema de la Ambigüedad

Si los datos son linealmente separables, existen infinitos hiperplanos que cumplen el criterio del perceptrón.

Preguntas:

- ¿son todos igual de buenos?
- ¿cuál elegiríamos para garantizar la mejor generalización ante datos nuevos?

Intuitivamente, queremos el hiperplano que pase lo más lejos posible de los puntos de ambas clases. Para eso buscamos maximizar la "calle" o margen entre las clases.

## Diapositiva 54. Geometría del Margen

Consideramos el clasificador:

$$
f(x)=\operatorname{sgn}(w^T x+b).
$$

Podemos reescalar $w$ y $b$ de modo que, para los puntos más cercanos al hiperplano:

$$
w^T x_i+b=1
\qquad
\text{para } y_i=1,
$$

$$
w^T x_i+b=-1
\qquad
\text{para } y_i=-1.
$$

La distancia entre estos dos hiperplanos paralelos, es decir el margen, es:

$$
\gamma=\frac{2}{\lVert w\rVert}.
$$

Maximizar el margen es equivalente a minimizar:

$$
\lVert w\rVert^2.
$$

## Diapositiva 55. Optimización Cuadrática (Primal Problem)

Planteamos el problema como una optimización con restricciones de desigualdad:

$$
\min_{w,b}\frac{1}{2}\lVert w\rVert^2
$$

sujeto a:

$$
y_i(w^T x_i+b)\ge 1,
\qquad
\forall i=1,\ldots,n.
$$

Es un problema de programación cuadrática (QP). La función objetivo es cuadrática y las restricciones son lineales. Existe un único mínimo global.

## Diapositiva 56. El Problema Dual y los Multiplicadores

Introducimos multiplicadores de Lagrange $\alpha_i\ge 0$. La teoría de optimización KKT permite resolver el problema dual:

$$
\max_\alpha
\sum_{i=1}^n \alpha_i
-
\frac{1}{2}\sum_{i,j}\alpha_i\alpha_j y_i y_j(x_i^T x_j).
$$

sujeto a:

$$
\sum_i \alpha_i y_i=0,
\qquad
\alpha_i\ge 0.
$$

**Propiedad crítica:** la solución depende solo de los productos internos entre los datos. Esto abre la puerta a los kernels.

## Diapositiva 57. ¿Qué son los Vectores de Soporte?

La solución final para los pesos es:

$$
w=\sum_{i=1}^n \alpha_i y_i x_i.
$$

En la práctica, la mayoría de los $\alpha_i$ serán cero.

Los puntos donde $\alpha_i>0$ son los que "sostienen" el margen.

**Vectores de soporte:** si eliminamos cualquier otro punto del dataset, el hiperplano no cambia. El modelo es extremadamente robusto a valores alejados, u *outliers*.

## Diapositiva 58. ¿Qué son los Vectores de Soporte?

La figura identifica los vectores de soporte como los puntos que tocan los hiperplanos paralelos que delimitan el margen.

![Vectores de soporte y margen en una SVM](figures/clase-8/fig-58-support-vectors.png)

## Diapositiva 59. Manejo de Ruido: Slack Variables

Si los datos no son perfectamente separables, el problema primal no tendría solución. Introducimos variables de holgura $\xi_i\ge 0$ en C-SVM:

$$
\min \frac{1}{2}\lVert w\rVert^2+C\sum_i \xi_i.
$$

Interpretación:

- el parámetro $C$ controla el compromiso entre maximizar el margen y minimizar el error de entrenamiento;
- un $C$ grande penaliza mucho el error y produce un margen estrecho;
- un $C$ pequeño permite errores para ganar un margen más ancho y mejorar la generalización.

## Diapositiva 60. No Linealidad: El Kernel Trick

¿Y si la frontera no es una línea, como en el problema XOR?

Mapeamos los datos a un espacio de mayor dimensión $\Phi(x)$ donde sí sean separables. Como en el dual solo usamos productos internos $x_i^T x_j$, definimos una función kernel:

$$
K(x_i,x_j)=\Phi(x_i)^T\Phi(x_j).
$$

Kernels populares:

- **Polinomial:**
  $$
  (1+x_i^T x_j)^d.
  $$
- **RBF (gaussiano):**
  $$
  \exp(-\gamma\lVert x_i-x_j\rVert^2),
  $$
  que mapea a una dimensión infinita.

## Diapositiva 61. Perceptrón vs SVM vs Regresión Logística

|  | Perceptrón | SVM | Regresión logística |
|---|---|---|---|
| Loss | $\max(0,-yf(x))$ | $\max(0,1-yf(x))$ | $\log(1+e^{-yf(x)})$ |
| Penaliza | solo errores | errores + margen | todos los puntos |
| Margen | $>0$ | $>1$ | suave, probabilístico |
| Gradiente | discontinuo | subgradiente | suave |
| Interpretación | corrección de errores | máxima separación | modelo probabilístico |

Idea clave:

- el perceptrón aprende solo de errores;
- SVM busca una frontera robusta;
- la logística modela probabilidades.

## Diapositiva 62. La Base Unificada: Minimización del Riesgo Empírico

En todos los modelos lineales, buscamos un vector aumentado $a$ que minimice una función de costo escalar $J(a)$.

Esquema general:

$$
a_{\text{nuevo}}=a_{\text{viejo}}-\eta\nabla J(a).
$$

Lo que define a cada modelo es la elección de la superficie de error $J$:

- **Perceptrón:** $J$ es lineal por tramos y solo penaliza errores.
- **Logística:** $J$ es la log-verosimilitud negativa, una penalización suave y diferenciable.
- **SVM:** $J$ combina margen, como regularización, y error, como *hinge loss*.

Minimizar $J$ es, esencialmente, empujar el hiperplano hasta que las muestras lleven el costo al mínimo posible.

## Diapositiva 63. Unificación por Funciones de Criterio

Todos los clasificadores lineales comparten la forma:

$$
g(x)=a^T y.
$$

Lo que los diferencia es la función de pérdida $J(a)$ que minimizan.

1. **Perceptrón:** penaliza solo la distancia de las muestras mal clasificadas:

$$
J_p(a)=\sum_{y\in\mathcal{Y}}(-a^T y).
$$

2. **Regresión logística:** minimiza la log-verosimilitud negativa, una pérdida logística suave.

3. **SVM (margen duro):** minimiza la norma del vector de pesos sujeta a un margen:

$$
J_{\text{svm}}(a)=\frac{1}{2}\lVert w\rVert^2.
$$

## Diapositiva 64. La Función de Costo Generalizada

Proponemos un marco unificado donde el aprendizaje consiste en minimizar:

$$
J(a)=\sum_{i=1}^n \Phi(a^T y_i).
\tag{2}
$$

Donde

$$
z_i=a^T y_i
$$

representa la distancia algebraica de la muestra a la frontera.

La "personalidad" del algoritmo depende de $\Phi(z)$:

- **Perceptrón:**
  $$
  \Phi(z)=\frac{1}{2}(|z|-z).
  $$
  "Solo me importa si estás del lado equivocado".
- **SVM (hinge loss):**
  $$
  \Phi(z)=\max(0,1-z).
  $$
  "Quiero que estés lejos de la frontera (margen)".
- **Logit (cross-entropy):**
  $$
  \Phi(z)=\log(1+e^{-z}).
  $$
  "Quiero maximizar la probabilidad de acierto".

## Diapositiva 65. El Motor del Aprendizaje: Descenso por el Gradiente

Para cualquier función de criterio $J(a)$ que sea continua y derivable, el esquema de actualización es:

$$
a(k+1)=a(k)-\eta\nabla J(a).
$$

**Ejemplo: gradiente del perceptrón**

$$
\nabla J_p=\sum_{y\in\mathcal{Y}}(-y).
$$

Sustituyendo:

$$
a(k+1)=a(k)+\eta\sum_{y\in\mathcal{Y}}y.
$$

Interpretación: si el algoritmo se equivoca, rota el hiperplano hacia la muestra mal clasificada para intentar incluirla en el semiespacio correcto.

## Diapositiva 66. Descenso por el Gradiente y Convergencia

**Sección:** Descenso por el gradiente y convergencia.

## Diapositiva 67. El Descenso por el Gradiente Universal

Independientemente de la función elegida, la regla de actualización es:

$$
a_{k+1}
=
a_k-\eta\sum_{i=1}^n \Phi'(z_i)y_i.
\tag{3}
$$

Aquí $\Phi'(z_i)$ actúa como peso del error.

Análisis de la derivada $\Phi'(z)$:

1. **Perceptrón:** $\Phi'=-1$ si hay error, y $0$ si no. La actualización es constante.
2. **Regresión logística:** el peso decae suavemente y queda asociado a la probabilidad de error.
3. **SVM:** $\Phi'=-1$ si $z<1$, y $0$ si $z>1$. La actualización ocurre solo por vectores de soporte.

El descenso por el gradiente generalizado queda:

$$
a(k+1)=a(k)-\eta(k)\nabla J(a).
$$

| Método | Pérdida | Comportamiento del gradiente |
|---|---|---|
| Perceptrón | Lineal por trozos | Constante para errores, $0$ para aciertos |
| Logit | Logística | Decae suavemente, nunca es $0$ |
| SVM | Hinge | $0$ para puntos fuera del margen |

La elección de la pérdida dicta la dinámica del aprendizaje y la robustez del clasificador final.

## Diapositiva 68. Descenso por el Gradiente para el Perceptrón

Dado que $J_p(a)$ es lineal por tramos y continua, podemos calcular su gradiente respecto de los pesos $a$:

$$
\nabla J_p
=
\frac{\partial J_p}{\partial a}
=
\sum_{y\in\mathcal{Y}}(-y).
$$

Para minimizar $J_p$, actualizamos los pesos en la dirección opuesta al gradiente:

$$
a(k+1)=a(k)-\eta\nabla J_p.
$$

Sustituyendo se obtiene la regla de aprendizaje del perceptrón en versión *batch*:

$$
a(k+1)=a(k)+\eta\sum_{y\in\mathcal{Y}}y.
$$

Donde $\eta$ es la tasa de aprendizaje.

## Diapositiva 69. Descenso por el Gradiente para el Perceptrón

¿Qué significa la actualización punto a punto?

$$
a(k+1)=a(k)+\eta y.
$$

Interpretación:

- el vector $a$ define la orientación del hiperplano;
- si el perceptrón se equivoca con $y$, significa que $a$ apunta demasiado lejos de $y$;
- al sumar $y$ a $a$, rotamos el vector normal del hiperplano para que apunte más directamente hacia el dato problemático.

## Diapositiva 70. Perceptrón: Gradiente Online y por Lotes

La versión clásica del perceptrón actualiza tras cada error:

$$
a^{(t+1)}=a^{(t)}+\eta_t y_k
\qquad
\text{si } (a^{(t)})^T y_k\le 0.
$$

Si la muestra está bien clasificada, no se modifica el vector de pesos.

También puede usarse una actualización agregada:

$$
a^{(t+1)}
=
a^{(t)}+\eta_t
\sum_{y\in\mathcal{Y}(a^{(t)})}y.
$$

Para un conjunto fijo de muestras mal clasificadas:

$$
\nabla J_p(a)
=
-
\sum_{y\in\mathcal{Y}(a)}y.
$$

Una regla de descenso de gradiente por lotes sería:

$$
a^{(t+1)}
=
a^{(t)}+\eta_t
\sum_{y\in\mathcal{Y}(a^{(t)})}y.
$$

La versión online suele reaccionar más rápido muestra a muestra. La versión *batch* es más estable analíticamente y conecta con descenso de gradiente clásico.

## Diapositiva 71. Algoritmo del Perceptrón y Tasa de Aprendizaje

Algoritmo:

1. Inicializar $a^{(0)}$.
2. Recorrer las muestras $y_k$.
3. Si $(a^{(t)})^T y_k>0$, continuar.
4. Si $(a^{(t)})^T y_k\le 0$, actualizar:

$$
a^{(t+1)}=a^{(t)}+\eta_t y_k.
$$

5. Repetir hasta no cometer errores o hasta un criterio externo de parada.

La constante $\eta_t$ puede ser:

- fija;
- decreciente;
- absorbida por la escala de $a$ si solo importa el signo.

En la versión más simple se toma:

$$
\eta_t=1.
$$

Dado que la clasificación depende del signo de $a^T y$, reescalar $a$ no cambia la frontera.

## Diapositiva 72. Teorema de Convergencia para el Perceptrón

**Teorema de convergencia del perceptrón (Novikoff, 1962).** Si los datos son linealmente separables, entonces el algoritmo del perceptrón está garantizado a encontrar un vector solución $a$ en un número finito de pasos.

Esto significaba que, sin importar con qué pesos aleatorios empezara la máquina, eventualmente aprendería la frontera perfecta.

Pero Marvin Minsky y Seymour Papert publicaron un libro en 1969 demostrando que el perceptrón es matemáticamente incapaz de aprender funciones que no son linealmente separables.

El problema XOR: ninguna línea recta puede separar los puntos de la función lógica XOR.

Si la naturaleza no es linealmente separable, el perceptrón iterará infinitamente sin converger.

## Diapositiva 73. Teorema de Convergencia

**Teorema (Rosenblatt).** Si existe un vector $a^*$ y un margen $\gamma>0$ tales que

$$
(a^*)^T y_i\ge \gamma
\qquad
\forall i,
$$

y además

$$
\lVert y_i\rVert\le R,
$$

entonces el algoritmo del perceptrón comete a lo sumo

$$
\left(\frac{R}{\gamma}\right)^2
$$

errores.

Es decir, el perceptrón converge si el problema es linealmente separable. Además, cuanto mayor es el margen $\gamma$:

- menos errores;
- convergencia más rápida;
- mayor robustez geométrica.

Idea de la prueba:

1. el producto $a^{(t)T}a^*$ crece al menos linealmente con el número de errores;
2. la norma $\lVert a^{(t)}\rVert^2$ crece a lo sumo linealmente.

Combinando ambas con Cauchy-Schwarz se obtiene una cota finita sobre el número de errores.

## Diapositiva 74. Prueba

Para la primera desigualdad, si en el paso $t$ hubo error con la muestra $y_k$, entonces:

$$
a^{(t+1)T}a^*
=
a^{(t)T}a^*+\eta_t y_k^T a^*.
$$

Si $\eta_t=1$ y la separabilidad con margen cumple $y_k^T a^*\ge \gamma$, resulta:

$$
a^{(t+1)T}a^*
\ge
a^{(t)T}a^*+\gamma.
$$

Para la segunda desigualdad, la norma satisface:

$$
\lVert a^{(t+1)}\rVert^2
=
\lVert a^{(t)}\rVert^2
+2a^{(t)T}y_k
+\lVert y_k\rVert^2.
$$

Como hubo error, $a^{(t)T}y_k\le 0$, así que:

$$
\lVert a^{(t+1)}\rVert^2
\le
\lVert a^{(t)}\rVert^2+R^2.
$$

Luego la norma crece a lo sumo como:

$$
\sqrt{t}\,R.
$$

## Diapositiva 75. Conclusión de la Prueba

Tras $M$ errores:

$$
a^{(M)T}a^*\ge M\gamma.
$$

Por Cauchy-Schwarz:

$$
a^{(M)T}a^*
\le
\lVert a^{(M)}\rVert \lVert a^*\rVert
\le
\sqrt{M}\,R\lVert a^*\rVert.
$$

Reordenando:

$$
M
\le
\left(\frac{R\lVert a^*\rVert}{\gamma}\right)^2.
$$

Normalizando $a^*$ se obtiene la cota estándar.

## Diapositiva 76. La Limitación de la Linealidad

El algoritmo de descenso por el gradiente no resuelve el problema de la no linealidad.

Si las clases no son separables linealmente en el espacio original, ninguna elección de $w,w_0$ resolverá el problema.

Ejemplos clásicos:

- clases circulares concéntricas;
- XOR.

![Ejemplos lineales, no lineales e inseparables](figures/clase-8/fig-76-linearity-limitations.png)

Pero aún podemos usar máquinas lineales con algunas adaptaciones, por ejemplo transformando los datos a un espacio donde sí sean separables o usando criterios más blandos.

## Diapositiva 77. Qué Ocurre si no Hay Separabilidad

Si no existe ningún $a$ que clasifique correctamente todas las muestras:

- el algoritmo puede no detenerse;
- los pesos pueden oscilar;
- la regla básica ya no es suficiente.

Algunas posibles soluciones:

- algoritmo Pocket, que conserva el mejor vector encontrado;
- criterios de parada operativos, como número máximo de iteraciones o mejora marginal;
- funciones de costo más suaves, como pérdida de margen o log-loss;
- mapeo a espacios de mayor dimensión, como kernel trick.

## Diapositiva 78. Algoritmo: Consideraciones

**Pocket Algorithm:** una solución práctica simple es guardar el mejor vector encontrado hasta el momento:

- ejecutar perceptrón por un número fijo de iteraciones;
- mantener en el "bolsillo" el $a$ con menor error empírico;
- devolver ese vector al final.

No resuelve la no separabilidad, pero evita devolver el último vector arbitrario.

**Criterios de parada en la práctica:** en datos reales rara vez esperamos separabilidad exacta. Por eso se usan criterios operativos:

- número máximo de épocas;
- error empírico estable;
- mejora marginal por debajo de un umbral;
- conservación del mejor vector encontrado.

Esto convierte al perceptrón en un procedimiento heurístico útil incluso fuera del caso ideal.

## Diapositiva 79. Procedimiento de Relajación

Otra idea es suavizar el criterio. Si fijamos un margen deseado $b>0$, podemos usar:

$$
J_r(a)
=
\frac{1}{2}
\sum_{y\in\mathcal{Y}}
\frac{(a^T y-b)^2}{\lVert y\rVert^2}.
$$

En lugar de exigir solo positividad, se exige positividad con margen. El gradiente del término individual lleva a una actualización del tipo:

$$
a^{(t+1)}
=
a^{(t)}
+\eta_t
\frac{b-a^{(t)T}y_k}{\lVert y_k\rVert^2}
y_k,
$$

cuando

$$
a^{(t)T}y_k\le b.
$$

Esto suaviza la dinámica respecto del perceptrón duro.

## Diapositiva 80. Problema XOR

Se introduce el mapeo:

$$
\phi(x_1,x_2)=(x_1,x_2,x_1x_2).
$$

La figura compara el espacio original con el espacio transformado, donde el problema XOR se vuelve linealmente separable.

![Mapeo de XOR a un espacio transformado](figures/clase-8/fig-80-xor-feature-map.png)

## Diapositiva 81. Mapeo de Características

Planteo más general: transformar la representación:

$$
\phi(x)=
\begin{bmatrix}
\phi_1(x)\\
\vdots\\
\phi_{\hat d}(x)
\end{bmatrix}.
$$

Entonces usamos un discriminante lineal en el nuevo espacio:

$$
g(x)=a^T\phi(x)+a_0.
$$

Un problema no lineal en $x$ puede ser lineal en $\phi(x)$.

## Diapositiva 82. Datos Concéntricos

En una dimensión, separar puntos cercanos al origen de puntos lejanos no es lineal en $x$.

Pero si definimos:

$$
\phi(x)=
\begin{bmatrix}
x\\
x^2
\end{bmatrix},
$$

entonces una frontera lineal en el espacio $(x,x^2)$ corresponde a una frontera cuadrática en el espacio original.

![Transformación de datos concéntricos a un espacio donde son separables](figures/clase-8/fig-82-concentric-feature-map.png)

## Diapositiva 83. Cómo se Resuelve XOR con un Mapeo

Si introducimos una nueva característica:

$$
z=x_1x_2,
$$

o más generalmente un mapa no lineal $\phi(x)$, el problema puede hacerse separable en el espacio aumentado.

Esto anticipa dos ideas posteriores:

- capas ocultas en redes neuronales;
- transformaciones de características en métodos kernel.

## Diapositiva 84. La Crítica de Minsky y Papert

El análisis clásico de *Perceptrons* mostró que los predicados lineales tienen limitaciones severas para representar funciones de conectividad, paridad y composición lógica.

La crítica no era que el perceptrón fuera inútil, sino que su geometría de una sola capa era insuficiente para problemas complejos.

La decepción con las limitaciones de los perceptrones de una capa contribuyó al primer "invierno" de las redes neuronales.

Sin embargo, la lección correcta no era abandonar la idea, sino reconocer que hacía falta:

- composición de representaciones;
- múltiples capas;
- aprendizaje más sofisticado.

## Diapositiva 85. Lo que Anticipa la Clase de Hoy

El perceptrón de una capa es insuficiente para aprender representaciones jerárquicas, pero ya contiene el núcleo conceptual del aprendizaje profundo:

- pesos ajustables;
- representación distribuida;
- entrenamiento iterativo sobre datos;
- composición de funciones lineales y no lineales.

La diferencia clave será aprender las transformaciones internas, no solo la última frontera.

Aun con sus limitaciones, el perceptrón deja varias ideas fundamentales:

- la clasificación como optimización geométrica;
- el aprendizaje por corrección de errores;
- la importancia del margen;
- la conexión entre separabilidad y complejidad computacional.

## Diapositiva 86. Próxima Clase

Hemos visto que hay diferentes métodos para aprender clasificadores lineales, cada uno con su propia función de costo y dinámica de aprendizaje.

Todos comparten la misma base: minimizar una función de costo que depende de la distancia de las muestras a la frontera.

Sin embargo, puede pasar que un modelo con bajo error de entrenamiento no generalice bien a datos nuevos, aun cuando el error de entrenamiento sea bajo.

La próxima clase vuelve al problema del balance entre sesgo y varianza, para ver cómo elegir el modelo correcto para cada situación.
