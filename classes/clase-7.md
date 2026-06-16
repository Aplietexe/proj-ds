---
title: "Técnicas No Paramétricas: Ventanas de Parzen y k-NN"
---

## Diapositiva 1

**Portada**

- Ciencia de Datos - Clase 7
- Técnicas no paramétricas: Ventanas de Parzen y k-NN
- Licenciatura en Matemática Aplicada - FaMAF
- FaMAF
- Abril 2026

## Diapositiva 2

La diapositiva es una motivación puramente visual: muestra una estructura radial suave, aproximadamente unimodal y simétrica.

![Campo radial suave con máxima intensidad en el centro](figures/clase-7/fig-02-radial-field.png)

## Diapositiva 3

La figura contrasta dos geometrías muy distintas:

- una estructura radial aproximadamente isotrópica;
- una estructura espiral con organización local mucho más compleja.

La idea implícita es que no todas las densidades reales se parecen a una gaussiana simple.

![Comparación entre una estructura radial y una estructura espiral](figures/clase-7/fig-03-radial-and-spiral.png)

## Diapositiva 4

La diapositiva reúne varios ejemplos de distribuciones empíricas muy diferentes:

- histogramas fuertemente asimétricos;
- relaciones entre magnitud y frecuencia de terremotos;
- histogramas con ajuste por densidad;
- histogramas tonales en imágenes.

Sirve como motivación para abandonar familias paramétricas demasiado rígidas.

![Galería de distribuciones empíricas con formas heterogéneas](figures/clase-7/fig-04-distribution-gallery.png)

## Diapositiva 5. Roadmap de la Clase

La clase se organiza en tres bloques:

1. **Estimación empírica**
   - el fin de las formas;
   - Parzen windows;
   - estimación y clasificación con k-NN.
2. **Regresión Logística: de la probabilidad a la optimización**
3. **Gradient Descent: el motor del aprendizaje**

## Diapositiva 6. Hoja de Ruta: ¿Hacia Dónde Vamos?

**Contexto metodológico**

- **Clase 6:** reducción de dimensionalidad con PCA y FDA; se aprendió a proyectar preservando varianza o separabilidad.
- **Clase 7:** se abandonan los supuestos funcionales sobre $p(x \mid \omega_i)$; se deja que el dato defina su propia estructura local.

La idea de cierre de la diapositiva es:

> PCA nos ayudó a "limpiar" el espacio; las técnicas de hoy nos dirán cómo clasificar en él sin recurrir a la conveniencia de la gaussiana.

## Diapositiva 7. Hoja de Ruta: ¿Hacia Dónde Vamos?

Es la misma hoja de ruta, pero con énfasis visual en la palabra **local**:

- ya no se impone una forma global a $p(x \mid \omega_i)$;
- la estructura relevante pasa a estar dictada por la vecindad de los datos.

## Diapositiva 8. Estimación Empírica

**Sección:** Estimación empírica.

## Diapositiva 9. Limitaciones del Enfoque Paramétrico

Hasta ahora se supuso que las densidades condicionales de clase tienen una forma conocida, por ejemplo:

$$
p(x \mid \omega_i) \sim \mathcal{N}(\mu_i,\Sigma_i).
$$

Pero aparecen varios problemas:

1. **Multimodalidad:** las distribuciones reales suelen tener múltiples picos que una sola gaussiana no puede capturar.
2. **Asimetría y soporte:** muchas variables poseen fronteras rígidas o colas pesadas.
3. **Error de modelo:** si la forma asumida es incorrecta, el clasificador de Bayes resultante será subóptimo, sin importar cuántos datos tengamos.

Necesidad: estimar directamente

$$
p(x \mid \omega_i)
$$

a partir de las muestras

$$
\mathcal{D} = \{x_1,\ldots,x_n\}.
$$

## Diapositiva 10. Estimación de Densidad: Fundamentos

Sea $x$ un vector aleatorio con densidad continua $p(x)$. La probabilidad $P$ de que un punto caiga en una región $\mathcal{R}$ es

$$
P = \int_{\mathcal{R}} p(x')\,dx'.
$$

Si tenemos $n$ muestras i.i.d. según $p(x)$ y $k$ de ellas caen en $\mathcal{R}$, entonces $k$ sigue una distribución binomial:

$$
P(k)=\binom{n}{k}P^k(1-P)^{n-k}.
$$

## Diapositiva 11. Estimador de $P$

Propiedades del estimador $k/n$:

- **Valor esperado:** como $E[k]=nP$, se tiene
  $$
  E\left[\frac{k}{n}\right]=P,
  $$
  de modo que $k/n$ es un estimador insesgado de la probabilidad.
- **Varianza y consistencia:** su varianza es
  $$
  \operatorname{Var}\left(\frac{k}{n}\right)=\frac{P(1-P)}{n},
  $$
  que tiende a $0$ cuando $n \to \infty$.
- **Ley de los grandes números:** la frecuencia relativa $k/n$ converge casi seguramente a $P$.

## Diapositiva 12. Estimación de Densidad: Aproximación

Si la región $\mathcal{R}$ es suficientemente pequeña para que $p(x)$ sea aproximadamente constante en su interior, entonces:

$$
P \approx p(x)V
\qquad \Longrightarrow \qquad
p(x) \approx \frac{k/n}{V}
\tag{1}
$$

donde $V$ es el volumen de $\mathcal{R}$.

Interpretación: $k/n$ actúa como una estimación de la masa de probabilidad capturada dentro del volumen $V$.

## Diapositiva 13. Ajustando la Densidad Puntual

La figura muestra una nube de puntos y una pequeña región alrededor de una ubicación de consulta. La intuición es estimar la densidad local contando cuántas muestras caen en esa vecindad.

![Ventana local alrededor de un punto de consulta en la nube de datos](figures/clase-7/fig-13-local-density-window.png)

## Diapositiva 14. Dos Caminos Analíticos

Se parte de la aproximación fundamental para la densidad en $x$:

$$
p(x) \approx \frac{k/n}{V}.
$$

Para que el estimador sea consistente cuando $n \to \infty$, necesitamos simultáneamente:

- $V \to 0$, para capturar densidad puntual;
- $k \to \infty$, para que la varianza del estimador tienda a $0$.

## Diapositiva 15. Dos Caminos Analíticos

La clase plantea dos estrategias:

1. **Ventanas de Parzen:** fijar el volumen $V_n$ como función de $n$ y dejar $k_n$ como variable aleatoria empírica.
2. **k-Nearest Neighbors:** fijar $k_n$ como función de $n$ y dejar que el volumen $V_n$ crezca hasta englobar $k_n$ muestras.

La diapositiva remarca el dilema geométrico:

- si fijamos $V$, en regiones vacías puede ocurrir que $k=0$;
- si fijamos $k$, el volumen puede crecer mucho.

## Diapositiva 16. Ventanas de Parzen: Definición Formal

Supongamos que la región $\mathcal{R}_n$ es un hipercubo de dimensión $d$ con lado $h_n$, centrado en $x$. Su volumen es:

$$
V_n = h_n^d.
$$

Definimos la función ventana

$$
\varphi(u)=
\begin{cases}
1 & \text{si } |u_j|\le \frac{1}{2}, \quad j=1,\ldots,d, \\
0 & \text{caso contrario.}
\end{cases}
$$

Esta función vale $1$ si $u$ está dentro del hipercubo unitario centrado en el origen.

La cantidad de muestras $k_n$ que caen en el hipercubo centrado en $x$ con lado $h_n$ es

$$
k_n = \sum_{i=1}^n \varphi\left(\frac{x-x_i}{h_n}\right).
$$

## Diapositiva 17. El Estimador de Densidad de Parzen

Sustituyendo $k_n$ en la aproximación inicial

$$
p_n = \frac{k_n}{nV_n},
$$

se obtiene el estimador clásico de Parzen-Rosenblatt:

$$
p_n(x)=\frac{1}{nV_n}\sum_{i=1}^n \varphi\left(\frac{x-x_i}{h_n}\right).
$$

Generalización:

- no estamos restringidos al hipercubo;
- la función $\varphi$ puede ser cualquier densidad válida, no negativa e integrable a $1$.

Interpretación:

- cada punto de entrenamiento $x_i$ "irradia" una pequeña probabilidad a su alrededor;
- el estimador global es la superposición de todas esas radiaciones locales.

## Diapositiva 18. Ventanas de Parzen

La figura ilustra varias ventanas centradas en distintos puntos. La densidad estimada se obtiene sumando todas estas contribuciones locales.

![Conjunto de ventanas locales de Parzen sobre una nube de puntos](figures/clase-7/fig-18-parzen-windows.png)

## Diapositiva 19. Convergencia del Estimador

Para estudiar si $p_n(x)$ es un buen estimador de $p(x)$, se analiza su valor esperado:

$$
E[p_n(x)]
=
\frac{1}{nV_n}\sum_{i=1}^n E\left[\varphi\left(\frac{x-x_i}{h_n}\right)\right]
=
\frac{1}{V_n}\int \varphi\left(\frac{x-v}{h_n}\right)p(v)\,dv.
$$

Interpretación geométrica:

- el valor esperado del estimador es la convolución de la densidad real con la ventana $\varphi$;
- por lo tanto, $E[p_n(x)]$ es una versión difuminada o borrosa de la densidad verdadera.

## Diapositiva 20. Condiciones Asintóticas de Convergencia

**Teorema.** Para que el estimador $p_n(x)$ converja a $p(x)$ cuando $n \to \infty$, se debe cumplir:

1. $$
   \lim_{n\to\infty} V_n = 0
   $$
   la ventana debe achicarse para dar resolución espacial;
2. $$
   \lim_{n\to\infty} nV_n = \infty
   $$
   el número de muestras en la ventana debe tender a infinito para eliminar el ruido estadístico.

Una elección típica sugerida en la diapositiva es

$$
V_n = \frac{1}{\sqrt{n}}.
$$

## Diapositiva 21. El Compromiso Sesgo-Varianza

Para un conjunto de datos finito, la elección de $h_n$ es crítica:

- **$h_n$ demasiado grande:** alto sesgo, o *underfitting*; se borran detalles y picos multimodales.
- **$h_n$ demasiado pequeño:** alta varianza, o *overfitting*; la densidad se vuelve una colección de picos aislados tipo delta de Dirac sobre cada punto $x_i$.

## Diapositiva 22

La figura muestra una estimación no paramétrica unidimensional mediante ventanas de Parzen con núcleo gaussiano. Se compara la densidad real con la densidad estimada y se visualiza el efecto del ancho de banda.

![Demostración interactiva de Parzen en una dimensión](figures/clase-7/fig-22-parzen-1d-demo.png)

## Diapositiva 23

La figura generaliza la idea al caso bidimensional: una nube de muestras sobre la que se superpone un mapa de intensidad correspondiente a la estimación no paramétrica.

![Demostración interactiva de Parzen en dos dimensiones](figures/clase-7/fig-23-parzen-2d-demo.png)

## Diapositiva 24. Conexión Algebraica: Kernels Multivariados

En la práctica se usa a menudo una ventana gaussiana multivariada en lugar del hipercubo:

$$
\varphi(x)=\frac{1}{(2\pi)^{d/2}|\Sigma|^{1/2}}
\exp\left(-\frac{1}{2}x^T\Sigma^{-1}x\right).
$$

Aquí, la matriz de covarianza $\Sigma$ juega el rol del ancho de banda $h_n$.

La conexión con PCA/whitening es directa:

- si $\Sigma$ es anisotrópica, el kernel incorpora la geometría de Mahalanobis;
- el kernel se adapta a la forma local de los datos.

## Diapositiva 25. Limitaciones: La Maldición de la Dimensionalidad

El gran enemigo de las ventanas de Parzen es la alta dimensión $d$.

- el volumen crece exponencialmente:
  $$
  V = h^d;
  $$
- para mantener una densidad de probabilidad constante, la cantidad de datos requerida crece exponencialmente con $d$;
- en espacios muy grandes, el espacio está esencialmente vacío, y la mayoría de las ventanas $V_n$ no contendrán ni una sola muestra.

Conclusión: Parzen es conceptualmente poderoso, pero inviable en dimensiones altas sin una reducción previa, por ejemplo con PCA.

## Diapositiva 26. De Parzen a k-NN

Problema de Parzen:

- si fijamos el tamaño de la ventana $h_n$, en regiones densas la ventana está llena de puntos;
- en regiones vacías la ventana queda vacía y la estimación se vuelve ruidosa.

Solución k-NN:

> En lugar de fijar el volumen y preguntar cuántos vecinos caen dentro, fijamos cuántos vecinos queremos y dejamos que el volumen crezca hasta atraparlos.

Esto da una resolución adaptativa:

- ventanas pequeñas en regiones densas;
- ventanas grandes en regiones poco densas.

## Diapositiva 27. Estimación de Densidad k-NN

Se retoma la ecuación fundamental:

$$
p_n(x) \approx \frac{k}{nV}.
$$

En el método de los $k$ vecinos más cercanos:

- se fija $k_n$ como función de $n$;
- el volumen $V_n$ se deja crecer hasta encapsular exactamente $k_n$ muestras.

La densidad estimada es

$$
p_n(x)=\frac{k_n}{nV_n}.
$$

Condiciones de convergencia:

1. $$
   \lim_{n\to\infty} k_n = \infty
   $$
   para que la varianza tienda a cero;
2. $$
   \lim_{n\to\infty} \frac{k_n}{n}=0
   $$
   para que $V_n \to 0$ y la estimación sea local.

Ejemplo típico:

$$
k_n = \sqrt{n}.
$$

## Diapositiva 28. Resumen de k-NN

La figura ilustra la idea geométrica central de k-NN: en zonas densas bastan ventanas pequeñas, mientras que en zonas vacías se requieren ventanas mayores para capturar la misma cantidad de vecinos.

![Resumen visual de vecindades adaptativas en k-NN](figures/clase-7/fig-28-knn-summary.png)

## Diapositiva 29. Clasificación: Estimando la Probabilidad a Posteriori

El verdadero poder de k-NN en clasificación no es estimar $p(x)$, sino estimar directamente

$$
P(\omega_i \mid x)
$$

usando la regla de Bayes.

Supongamos que en una celda de volumen $V$ alrededor de $x$ capturamos $k$ muestras en total, de las cuales $k_i$ pertenecen a la clase $\omega_i$.

Entonces:

$$
p_n(x \mid \omega_i)=\frac{k_i}{n_iV},
$$

$$
P_n(\omega_i)=\frac{n_i}{n}.
$$

Aplicando Bayes:

$$
P_n(\omega_i \mid x)
=
\frac{p_n(x \mid \omega_i)P_n(\omega_i)}
{\sum_j p_n(x \mid \omega_j)P_n(\omega_j)}
=
\frac{k_i}{k}.
$$

## Diapositiva 30. Estimación de Densidad: Aproximación

La figura muestra la nube de una de las clases por separado.

![Muestras de una clase en el espacio bidimensional](figures/clase-7/fig-30-class-1-samples.png)

## Diapositiva 31. Estimación de Densidad: Aproximación

La figura muestra la nube de la segunda clase por separado.

![Muestras de la segunda clase en el espacio bidimensional](figures/clase-7/fig-31-class-2-samples.png)

## Diapositiva 32. Estimación de Densidad: Aproximación

La figura superpone ambas clases en el mismo espacio de características.

![Superposición de ambas clases en el espacio bidimensional](figures/clase-7/fig-32-two-class-samples.png)

## Diapositiva 33. Estimación de Densidad: Aproximación

La figura destaca una vecindad local en una zona relativamente vacía. Sirve para mostrar que, con un volumen fijo, el conteo local puede ser muy pequeño o incluso nulo.

![Ventana local ubicada en una región poco densa](figures/clase-7/fig-33-knn-cell-sparse.png)

## Diapositiva 34. Estimación de Densidad: Aproximación

La figura destaca una vecindad local en una zona mucho más densa, donde la misma idea geométrica produce un conteo local significativamente mayor.

![Ventana local ubicada en una región más densa](figures/clase-7/fig-34-knn-cell-dense.png)

## Diapositiva 35. La Regla de Decisión k-NN

**Regla de decisión.** Dada una muestra de prueba $x$, se buscan los $k$ vecinos más cercanos en el conjunto de entrenamiento y se asigna $x$ a la clase $\omega_i$ que maximiza $k_i$.

Observación geométrica:

- la frontera de decisión no es una función analítica global;
- es un conjunto de parches locales, altamente no lineales, que se adaptan a la densidad empírica de los datos.

La diapositiva deja planteada la pregunta:

- ¿qué ocurre si $k=1$?
- ¿qué ocurre si $k=n$?

## Diapositiva 36. Regla del Vecino Más Cercano (1-NN)

Si $k=1$, asignamos $x$ a la clase de su vecino más próximo $x'$.

**Teselación de Voronoi**

- el clasificador 1-NN particiona el espacio de características en celdas poliédricas;
- cada celda contiene una única muestra de entrenamiento $x_i$;
- cualquier punto dentro de la celda está más cerca de $x_i$ que de cualquier otra muestra.

La frontera de decisión global es la unión de los segmentos de hiperplanos que separan celdas de diferentes clases.

![Teselación de Voronoi asociada al clasificador 1-NN](figures/clase-7/fig-36-voronoi-1nn.png)

## Diapositiva 37. El Teorema de Cover-Hart (1967)

A primera vista, la regla 1-NN parece demasiado simple y propensa al *overfitting*. Sin embargo, si $P^\*$ es el error óptimo de Bayes y $P$ es el error esperado del clasificador 1-NN cuando $n \to \infty$, entonces:

$$
P^\* \le P \le P^\*\left(2-\frac{c}{c-1}P^\*\right),
$$

donde $c$ es el número de clases.

## Diapositiva 38. Demostración Asintótica (Caso $c=2$)

Asumamos $n \to \infty$, por lo que el vecino más cercano $x'$ de $x$ está infinitesimalmente cerca:

$$
x' \to x.
$$

En consecuencia,

$$
P(\omega_i \mid x') \approx P(\omega_i \mid x).
$$

El error de Bayes en $x$ es

$$
P^\*(\text{error}\mid x)=\min\left[P(\omega_1 \mid x),P(\omega_2 \mid x)\right].
$$

La probabilidad de error del clasificador 1-NN en $x$ es

$$
P(\text{error}\mid x)
=
P(\omega_1 \mid x)P(\omega_2 \mid x')
+
P(\omega_2 \mid x)P(\omega_1 \mid x').
$$

## Diapositiva 39. Demostración Asintótica (Continuación)

Como $x' \to x$, sustituimos

$$
P(\omega_i \mid x') = P(\omega_i \mid x).
$$

Entonces:

$$
P(\text{error}\mid x)
=
2P(\omega_1 \mid x)P(\omega_2 \mid x)
=
2P^\*(x)(1-P^\*(x)).
$$

Para obtener el error global:

$$
P = \int 2P^\*(x)(1-P^\*(x))p(x)\,dx.
$$

Como $P^\*(x)\ge 0$, se deduce que

$$
P \le 2P^\*.
$$

Interpretación: nunca erramos más del doble del error de Bayes.

## Diapositiva 40. El Papel Fundamental de la Métrica

Toda la teoría de k-NN depende de cómo definimos la noción de vecino. La métrica $\mathcal{D}(a,b)$ define la geometría del espacio.

Se introduce la métrica de Minkowski:

$$
L_p(a,b)=\left(\sum_{i=1}^d |a_i-b_i|^p\right)^{1/p}.
$$

Casos importantes:

- $p=1$: distancia Manhattan;
- $p=2$: distancia euclídea.

Si las variables tienen distintas escalas o correlación, la euclídea falla. La solución propuesta es:

- usar distancia de Mahalanobis;
- o aplicar whitening previo.

## Diapositiva 41. Consideraciones Computacionales

A diferencia de Bayes paramétrico o Perceptrón, k-NN es un algoritmo de **lazy learning**.

- **Fase de entrenamiento:** costo $O(1)$; simplemente se almacena $\mathcal{D}$.
- **Fase de inferencia:** costo $O(n \cdot d)$ por cada muestra nueva; hay que calcular la distancia a todos los puntos.

La diapositiva menciona como alternativa el uso de estructuras espaciales, por ejemplo árboles.

## Diapositiva 42. Resumen de Métodos No Paramétricos

¿Qué se logró?

- dejar de asumir distribuciones funcionales;
- permitir que el dato dicte la densidad, con Parzen;
- permitir que el dato dicte la frontera, con Voronoi/k-NN.

Problema restante:

- guardar todo el *dataset* es ineficiente;
- computar distancias en alta dimensión vuelve a sufrir la maldición de la dimensionalidad.

La pregunta que abre la siguiente sección es:

> ¿Qué pasaría si, en lugar de guardar los datos, aprendemos una ecuación que resuma la frontera directamente?

## Diapositiva 43. Regresión Logística: De la Probabilidad a la Optimización

**Sección:** Regresión logística: de la probabilidad a la optimización.

## Diapositiva 44. De Densidades a Fronteras

La transición conceptual es la siguiente:

- las fronteras guardan una relación con las densidades, al menos en casos simples;
- hasta ahora se buscó modelar $p(x \mid \omega_i)$;
- la frontera termina siendo una función de las variables:
  $$
  g(x);
  $$
- para empezar por lo más simple, se propone una función lineal:
  $$
  g(x)=\mathbf{w}^T x + w_0.
  $$

## Diapositiva 45. De Densidades a Fronteras

Problemas y motivación:

- una combinación lineal puede tomar valores arbitrariamente grandes;
- sería mejor una función que mapee al intervalo $[0,1]$;
- surge la idea de que "cerca de $0$ es una clase y cerca de $1$ es otra";
- además, debería ser posible clasificar $c$ clases.

## Diapositiva 46. Funciones Discriminantes Lineales

Se define la función discriminante como una combinación lineal de las características:

$$
g(x)=\mathbf{w}^T x + w_0,
$$

donde $\mathbf{w}$ es el vector de pesos y $w_0$ es el sesgo.

Regla de decisión para dos clases:

- decidir $\omega_1$ si $g(x)>0$;
- decidir $\omega_2$ si $g(x)<0$.

La ecuación

$$
g(x)=0
$$

define un hiperplano de decisión $H$, y el vector $\mathbf{w}$ es normal a ese hiperplano.

## Diapositiva 47. Notación: El Vector Aumentado

Para manejar el término independiente $w_0$, se introduce un espacio aumentado de dimensión $d+1$:

$$
\mathbf{y}=
\begin{bmatrix}
1 \\
x_1 \\
\vdots \\
x_d
\end{bmatrix},
\qquad
\mathbf{a}=
\begin{bmatrix}
w_0 \\
w_1 \\
\vdots \\
w_d
\end{bmatrix}.
$$

En este nuevo espacio, el hiperplano pasa por el origen y la función discriminante se simplifica a:

$$
g(x)=\mathbf{a}^T\mathbf{y}.
$$

## Diapositiva 48. Normalización de las Muestras

Para simplificar aún más el algoritmo, se aplica un truco algebraico a las muestras de entrenamiento.

Se quiere que:

$$
\mathbf{a}^T\mathbf{y}_i > 0 \quad \text{si } \mathbf{y}_i \in \omega_1,
$$

$$
\mathbf{a}^T\mathbf{y}_i < 0 \quad \text{si } \mathbf{y}_i \in \omega_2.
$$

Normalización:

- si $\mathbf{y}_i \in \omega_2$, se reemplaza por su negativo $-\mathbf{y}_i$.

Entonces el aprendizaje se reduce a buscar un único vector $\mathbf{a}$ tal que:

$$
\mathbf{a}^T\mathbf{y}_i > 0
\qquad
\forall i \in \{1,\ldots,n\}.
$$

Interpretación: buscamos un vector que forme un ángulo agudo con todas las muestras normalizadas.

## Diapositiva 49. La Función Logística o Sigmoide

Queremos mapear el discriminante lineal

$$
z=\mathbf{w}^T x + w_0 \in (-\infty,\infty)
$$

al intervalo de probabilidades $[0,1]$.

Se define la sigmoide:

$$
\sigma(z)=\frac{1}{1+e^{-z}}.
$$

Propiedades clave:

- $$
  \lim_{z\to\infty}\sigma(z)=1;
  $$
- $$
  \lim_{z\to-\infty}\sigma(z)=0;
  $$
- $$
  \sigma'(z)=\sigma(z)(1-\sigma(z)).
  $$

Esta última propiedad es fundamental para calcular el gradiente.

## Diapositiva 50. El Modelo Logit (GLM)

Se postula que la probabilidad posterior sigue la forma:

$$
P(y=1 \mid x;\mathbf{w})=\sigma(\mathbf{w}^T x + w_0).
$$

Si despejamos el argumento, usando la notación aumentada:

$$
\ln\left(\frac{P(y=1 \mid x)}{1-P(y=1 \mid x)}\right)=\mathbf{a}^T\mathbf{y}.
$$

Interpretación:

- estamos ante un modelo lineal generalizado;
- no se asume que $y$ sea lineal en $x$;
- se asume que la *link function* logit es lineal.

Esto hace al enfoque más robusto que LDA cuando los datos no son gaussianos.

## Diapositiva 51. Estimación por Máxima Verosimilitud (MLE)

A diferencia de Bayes, donde se estiman $\mu$ y $\Sigma$, aquí se busca el vector de pesos $\mathbf{a}$ que maximiza la probabilidad de observar las etiquetas del conjunto $\mathcal{D}$.

Asumiendo independencia i.i.d., la verosimilitud es:

$$
\mathcal{L}(\mathbf{a})=
\prod_{i=1}^n
P(y_i \mid x_i;\mathbf{a})^{y_i}
\left[1-P(y_i \mid x_i;\mathbf{a})\right]^{1-y_i}.
$$

Para facilitar el cálculo, se minimiza el logaritmo negativo:

$$
J(\mathbf{a})=
-\sum_{i=1}^n
\left[
y_i\ln(\hat{y}_i) + (1-y_i)\ln(1-\hat{y}_i)
\right].
$$

Donde, en la notación aumentada de la diapositiva,

$$
\hat{y}_i=\sigma(\mathbf{a}^T\mathbf{y}_i).
$$

Esta función de costo es la **cross-entropy loss**.

## Diapositiva 52. Optimización: ¿Por Qué No Hay Solución Cerrada?

A diferencia de la regresión lineal, el gradiente de $J(\mathbf{a})$ no permite despejar $\mathbf{a}$ analíticamente:

$$
\nabla J(\mathbf{a})=
\sum_{i=1}^n
\left(\sigma(\mathbf{a}^T\mathbf{y}_i)-y_i\right)\mathbf{y}_i.
$$

Métodos de resolución:

- **descenso por el gradiente**
  $$
  \mathbf{a}_{\text{new}} = \mathbf{a}_{\text{old}} - \eta \nabla J(\mathbf{a});
  $$
- **Newton-Raphson (IRLS)**.

La diapositiva resalta que, como $J(\mathbf{a})$ es convexa, estos métodos convergen al óptimo global.

## Diapositiva 53. Extensión a Múltiples Clases: Regresión Logística Multinomial

**Motivación formal**

En el caso binario se modela el *log-ratio* de las probabilidades posteriores como una función lineal. Para $c$ clases, se busca particionar $\mathbb{R}^d$ en $c$ regiones de decisión separadas por hiperplanos.

**Definición: función softmax**

Sea un conjunto de clases

$$
\Omega=\{\omega_1,\ldots,\omega_c\}.
$$

Entonces:

$$
P(\omega_i \mid x)=
\frac{\exp(\mathbf{w}_i^T x)}
{\sum_{j=1}^c \exp(\mathbf{w}_j^T x)}
\tag{2}
$$

donde $\mathbf{w}_i$ es el vector de parámetros asociado a la clase $i$.

## Diapositiva 54. Consistencia con la Teoría de Decisión Bayesiana

Regla de decisión:

- para minimizar la probabilidad de error con pérdida $0$-$1$, se asigna $x$ a la clase $\omega_i$ que maximiza $P(\omega_i \mid x)$.

Superficies de decisión:

- la frontera entre $\omega_i$ y $\omega_j$ ocurre cuando
  $$
  P(\omega_i \mid x)=P(\omega_j \mid x)
  \qquad \Longrightarrow \qquad
  \mathbf{w}_i^T x = \mathbf{w}_j^T x
  \tag{3}
  $$
- esto equivale a
  $$
  (\mathbf{w}_i-\mathbf{w}_j)^T x = 0,
  $$
  que define un hiperplano.

Interpretación geométrica:

- cada clase compite por el espacio mediante su propio vector de pesos;
- el resultado es una partición del espacio en poliedros convexos, consistente con la teoría de discriminantes lineales.

## Diapositiva 55. Gradient Descent: El Motor del Aprendizaje

**Sección:** Gradient Descent.

## Diapositiva 56. Planteo Intuitivo

La diapositiva propone la analogía de una montaña cubierta por niebla:

- estamos en la cima y no vemos el valle, que representa el mínimo de $J(\mathbf{w})$;
- solo sentimos la inclinación local del suelo, es decir, el gradiente;
- para bajar lo más rápido posible, caminamos en la dirección opuesta a la máxima pendiente.

## Diapositiva 57. El Algoritmo de Descenso por el Gradiente

Dada una función de costo diferenciable $J(\mathbf{w})$, queremos encontrar:

$$
\mathbf{w}^\* = \arg\min_{\mathbf{w}} J(\mathbf{w}).
$$

Regla de actualización:

$$
\mathbf{w}_{t+1} = \mathbf{w}_t - \eta \nabla J(\mathbf{w}_t).
$$

Donde:

- $\nabla J(\mathbf{w})$ es el vector gradiente, que apunta hacia el máximo crecimiento;
- $\eta > 0$ es la *learning rate* o tasa de aprendizaje.

## Diapositiva 58. El Rol de la Tasa de Aprendizaje

¿Qué pasa si elegimos mal el paso $\eta$?

- **$\eta$ muy pequeño:** el descenso es muy lento; se corre el riesgo de tardar muchísimo en converger.
- **$\eta$ muy grande:** podemos pasarnos del mínimo, oscilar o incluso diverger.

## Diapositiva 59. Aplicación: El Gradiente de la Regresión Logística

Recordemos la función de costo:

$$
J(\mathbf{w})=
-\sum_{i=1}^n
\left[
y_i\ln(\sigma(\mathbf{w}^T x_i))
+
(1-y_i)\ln(1-\sigma(\mathbf{w}^T x_i))
\right].
$$

Usando

$$
\sigma'(z)=\sigma(z)(1-\sigma(z)),
$$

el gradiente resulta:

$$
\nabla J(\mathbf{w})=
\sum_{i=1}^n
\left(\sigma(\mathbf{w}^T x_i)-y_i\right)x_i.
$$

La diapositiva enfatiza la estructura:

- $\sigma(\mathbf{w}^T x_i)$ es la **predicción**;
- $y_i$ es el valor **real**.
