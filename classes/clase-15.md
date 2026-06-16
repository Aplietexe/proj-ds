---
title: "Redes Neuronales Artificiales"
---

## Diapositiva 1

**Portada**

- Redes neuronales artificiales
- Ciencia de Datos
- FaMAF
- Clase 15 - 2026-05-21

## Diapositiva 2. Modelos Globales con Detalle Local

**Sección:** Modelos globales con detalle local.

## Diapositiva 3. La Falla de los Árboles

![Sobres manuscritos como ejemplo de variaciones geométricas](figures/clase-15/fig-03-envelopes.png){width=90%}

Los árboles de decisión, incluso combinados por miles con heurísticas de ensamble, fallaban sistemáticamente ante sutiles **variaciones geométricas**. ¿Por qué?

## Diapositiva 4. La Falla de los Árboles

Un árbol de decisión divide el espacio mediante hiperplanos ortogonales a los ejes, es decir, pregunta si el $\operatorname{Pixel}(14,15)>0.5$.

Si un ciudadano dibujaba el número 2 perfectamente centrado, el modelo lo identificaba. Pero si otro ciudadano escribía el mismo 2 con una ligera **rotación** de 5 grados o un **desplazamiento** de dos píxeles hacia la izquierda, el árbol colapsaba.

Para el árbol, los píxeles activados eran completamente diferentes. El ensamble de árboles requería una cantidad exponencial de datos para aprender cada posible traslación, rotación y grosor de línea de forma independiente, volviéndose ineficiente, masivo y perdiendo capacidad de generalización. El problema no era el clasificador sino la **representación rígida del espacio**.

![Dígitos con variaciones geométricas](figures/clase-15/fig-04-digit-variations.png){width=80%}

## Diapositiva 5. Motivación: Limitaciones de la Combinación Lineal

Surgió entonces una necesidad imperativa: el sistema de clasificación no podía depender de los píxeles crudos y aislados. Necesitaba una arquitectura que fuera capaz de aprender de forma automática una **representación intermedia de los datos**; un mecanismo que extrajera **conceptos geométricos abstractos** (líneas horizontales, bucles, curvas) antes de clasificar.

![Activaciones locales sobre dígitos manuscritos](figures/clase-15/fig-05-local-features-digits.png){width=100%}

## Diapositiva 6. Límites del Particionado Local: Repaso de CART

- **Mecánica de CART:** aproxima la regla óptima de Bayes mediante particionado jerárquico y codicioso del espacio de características $\mathcal{X}$.
- **Estructura matemática de la frontera:** la función discriminante estimada $g_i(x)$ es una combinación de funciones indicadoras sobre hiperrectángulos disjuntos $R_m$:

$$
g_i(x)
=
\sum_{m=1}^M
c_{im}\mathbb{I}(x\in R_m)
\tag{1}
$$

**Pero...**

- **No diferenciabilidad:** $\nabla_x g_i(x)=0$ casi en todo punto. Impide el uso de métodos de optimización basados en gradiente local sobre el espacio de características.
- **Falta de regularidad:** cambios infinitesimales en $x$ cerca de un umbral provocan saltos discretos en la asignación de la clase $\omega_i$.

## Diapositiva 7. Intuición Geométrica: Tallar vs. Moldear

**El dilema del diseño de fronteras**

Para aproximar una frontera de decisión no lineal y suave:

**Enfoque CART / Ensambles**

- "Talla" el espacio recursivamente mediante cortes ortogonales.
- Requiere un número exponencial de divisiones (nodos) para aproximar una superficie curva.
- Localismo extremo y fragmentación de datos.

**Nuevo enfoque**

- Necesitamos "moldear" y deformar el espacio de características de forma global.
- Componer funciones diferenciables acotadas.
- Aprender representaciones continuas distribuidas.
- Permitir que el modelo capture relaciones no lineales y dependencias complejas entre características.
- Usar un algoritmo de optimización global.

## Diapositiva 8. El Camino Hacia la Flexibilidad Global Suave

Recordemos el discriminante lineal clásico:

$$
g(x)=w^\top x+w_0.
\tag{2}
$$

Establece una frontera rígida (hiperplano). Su capacidad de generalización es alta, pero su sesgo es prohibitivo frente a distribuciones no convexas o multimodales.

Ahora, en lugar de segmentar rígidamente el espacio (como CART) o proyectar heurísticamente a dimensiones arbitrarias (como SVM kernel), proponemos una **composición jerárquica de funciones discriminantes suaves**.

Cada función $j$ actúa como un clasificador suave elemental:

$$
z_j=f_j(x)
=
f\left(
\sum_i w_{ji}x_i+w_{j0}
\right).
\tag{3}
$$

donde $f(\cdot)$ es una **activación no lineal, continua y diferenciable**.

Estas funciones son pasos intermedios entre la entrada y la salida, por lo que están "ocultas".

## Diapositiva 9. Preguntas

Siguiendo estas ideas, necesitamos definir:

- ¿Qué función $f(\cdot)$ es adecuada para lograr la descripción local?
- ¿Cómo combinamos estas funciones ocultas para obtener una frontera global flexible?
- ¿Cómo optimizamos los parámetros $\{w_{ji}\}$ de forma eficiente en un espacio de funciones tan complejo?
- ¿Cómo regularizamos este modelo para evitar sobreajuste dada su alta capacidad de representación?
- ¿Cómo interpretamos y visualizamos las representaciones intermedias aprendidas por las funciones ocultas?

## Diapositiva 10. Motivación: Limitaciones de la Combinación Lineal

Vimos que hay tres estrategias para resolver problemas:

1. transformar el espacio;
2. expandir con base de funciones;
3. descripciones locales.

¿Cómo diseñamos un clasificador que mantenga la elegancia y continuidad del cálculo matemático (como en 1 ó 2), pero que tenga la flexibilidad para resolver problemas complejos (como en 3)?

**1. Descripción local (margen de tolerancia)**

Creamos una función matemática que actúe localmente: toma valores cercanos a 1 (se "activa") solo si el vector $x$ cae dentro de un rango de interés, y se queda atenuada (cercana a 0) en el resto del espacio. Una función suave mantiene el modelo dentro del terreno del cálculo diferencial, permitiendo gradientes limpios.

$$
z=f(x)
\quad
\Longleftarrow
\quad
\text{activación local: pesos ajustables para definir regiones de interés}.
$$

## Diapositiva 11. Motivación: Limitaciones de la Combinación Lineal

Vimos que hay tres estrategias para resolver problemas:

1. transformar el espacio;
2. expandir con base de funciones;
3. descripciones locales.

¿Cómo diseñamos un clasificador que mantenga la elegancia y continuidad del cálculo matemático (como en 1 ó 2), pero que tenga la flexibilidad para resolver problemas complejos (como en 3)?

**2. Transformar el espacio (cambio de base)**

Si los datos en el espacio original no son linealmente separables, usamos las funciones locales para crear un nuevo espacio de variables latentes o intermedias en donde sí lo sean.

$$
\varphi(x)=f(z)
\quad
\Longleftarrow
\quad
\text{función de activación: transforma la salida de la activación local}.
$$

## Diapositiva 12. Motivación: Limitaciones de la Combinación Lineal

Vimos que hay tres estrategias para resolver problemas:

1. transformar el espacio;
2. expandir con base de funciones;
3. descripciones locales.

¿Cómo diseñamos un clasificador que mantenga la elegancia y continuidad del cálculo matemático (como en 1 ó 2), pero que tenga la flexibilidad para resolver problemas complejos (como en 3)?

**3. Expandir en funciones (combinación bayesiana)**

Finalmente, para obtener nuestra función de discriminación global $g(x)$, combinamos linealmente estas nuevas variables latentes. Esto no es más que una expansión en funciones base adaptativas. En lugar de fijar las funciones de antemano (como haríamos en una aproximación por series de Fourier o polinomios), permitimos que los parámetros de las transformaciones locales se ajusten óptimamente para minimizar el riesgo empírico.

$$
g(x)=w_1z_1+w_2z_2+w_3z_3+w_0
\quad
\Longleftarrow
\quad
\text{frontera de decisión: separación lineal en el espacio transformado}.
$$

## Diapositiva 13. Representación Gráfica

La transformación del espacio mediante **funciones locales** para formar un clasificador global se puede visualizar como una **red de nodos interconectados**. Cada nodo representa una función de activación local.

Esta arquitectura es la base de las **Redes Neuronales Artificiales**, donde cada capa de nodos transforma el espacio de características de manera no lineal, permitiendo que el modelo capture relaciones complejas entre las variables de entrada.

![Transformación del espacio mediante capas de una red](figures/clase-15/fig-13-network-block.png){width=45%}

- **Capa de entrada:** define el espacio de características original.
- **Capa Oculta (Hidden):** cada unidad $j$ define un hiperplano suave que "corta" el espacio. Al tener $m$ unidades, tenemos $m$ cortes independientes.
- **Capa de Salida:** realiza una operación de combinación, análoga a una conjunción lógica suave, sobre los cortes de la capa oculta.

## Diapositiva 14. Representación Gráfica

Las **conexiones** entre los nodos representan los pesos que combinan estas funciones de activación local para producir la salida final. Las funciones de activación aportan la no linealidad necesaria para que el modelo pueda aprender fronteras de decisión complejas, mientras que la estructura de la red permite que estas funciones se compongan y se ajusten conjuntamente durante el entrenamiento.

![Conexiones ponderadas entre nodos de una red](figures/clase-15/fig-14-weighted-connections.png){width=75%}

## Diapositiva 15. Representación Gráfica

Las funciones ocultas representan transformaciones intermedias del espacio de características, que vuelven **linealmente separables** las clases que originalmente estaban entrelazadas. Cada función local actúa como un detector de patrones específico (por ejemplo, detectar la presencia de un bucle o una línea horizontal). Al combinar estas funciones a través de pesos ajustables, el modelo puede moldear la frontera de decisión de manera flexible y suave, adaptándose a la complejidad inherente de los datos.

La capa oculta aprende representaciones jerárquicas y abstractas, y la capa de salida combina estas transformaciones para realizar la clasificación final.

![Funciones suaves y frontera de decisión en una capa oculta](figures/clase-15/fig-15-hidden-transform.png){width=50%}

## Diapositiva 16. Representación Gráfica

Al agregar más capas ocultas, el modelo puede aprender representaciones cada vez más abstractas y complejas. Cada capa adicional permite que el modelo capture interacciones no lineales de orden superior entre las características de entrada, a través de **composiciones sucesivas de funciones no lineales simples**.

![Composición jerárquica de funciones en una red](figures/clase-15/fig-16-composition-layers.png){width=55%}

La red no es más que la arquitectura que permite combinar estos detectores elementales mediante una jerarquía de operaciones.

## Diapositiva 17. Cambio de Paradigma: Aprendizaje de Representaciones

**Tesis central de esta clase**

Mientras que los árboles y ensambles operan directamente particionando las dimensiones originales del vector de características $x$, las Redes Neuronales operan en dos fases concurrentes bajo el mismo criterio de optimización:

1. **Transformación del espacio:** las capas ocultas aprenden un mapeo no lineal continuo $\Phi(x):\mathbb{R}^d\to\mathbb{R}^h$.
2. **Decisión óptima:** la capa de salida ejecuta un clasificador lineal (o Softmax) en el nuevo espacio proyectado $\Phi(x)$, maximizando la verosimilitud de las clases anteriores.

En lugar de imponer manualmente funciones de base (como en métodos polinomiales o kernels fijos), estos modelos aprenden simultáneamente:

1. una transformación no lineal del espacio donde las clases se vuelven linealmente separables;
2. un hiperplano de decisión óptimo en dicho espacio transformado.

## Diapositiva 18. Redefiniendo el Espacio de Características

Para el problema de clasificación con $c$ clases, $\omega_1,\ldots,\omega_c$, buscamos un conjunto de funciones discriminantes $g_i(x)$ tal que decidimos $\omega_i$ si $g_i(x)>g_j(x)$ para todo $j\ne i$. Si la frontera de decisión óptima es fuertemente no lineal, se puede aproximar por medio de la combinación lineal de funciones base no lineales: mapeando el espacio original $x\in\mathbb{R}^d$ a un espacio de características ocultas (o latentes) $z\in\mathbb{R}^m$ con una transformación continua y paramétrica:

$$
z_j
=
f\left(
\sum_{i=1}^d w_{ji}^{(1)}x_i+w_{j0}^{(1)}
\right)
=
f\left((w_j^{(1)})^\top x+w_{j0}^{(1)}\right),
$$

donde $f(\cdot)$ es una función de activación no lineal y diferenciable.

**Composición de funciones:** una vez transformado el espacio a la representación $z$, definimos las funciones discriminantes finales como combinaciones lineales en este nuevo espacio:

$$
g_k(x)
=
\sum_{j=1}^m
w_{kj}^{(2)}z_j+w_{k0}^{(2)}.
$$

Por lo tanto,

$$
g_k(x)
=
\sum_{j=1}^m
w_{kj}^{(2)}
f\left(
\sum_{i=1}^d
w_{ji}^{(1)}x_i+w_{j0}^{(1)}
\right)
+
w_{k0}^{(2)}.
$$

## Diapositiva 19. Idea de Red Neuronal

Este conjunto de funciones forma una red, en donde cada nodo o "neurona" representa una de las funciones base. La red neuronal resultante es un **sistema paramétrico de funciones de discriminación generalizadas que transforma el espacio de características para hacer las clases linealmente separables**.

![Idea de red neuronal como sistema de funciones discriminantes](figures/clase-15/fig-19-neural-network-idea.png){width=75%}

## Diapositiva 20. Una Red con una Capa Oculta

Consideremos

$$
z_j
=
f\left(
w_{j0}+\sum_{i=1}^d w_{ji}x_i
\right),
\qquad
j=1,\ldots,m.
$$

Los *scores* de salida son

$$
a_k
=
v_{k0}+\sum_{j=1}^m v_{kj}z_j,
\qquad
k=1,\ldots,c.
$$

**Forma funcional**

$$
g_k(x)
=
v_{k0}
+
\sum_{j=1}^m
v_{kj}f(w_{j0}+w_j^\top x).
$$

Es una combinación lineal de funciones base aprendidas.

## Diapositiva 21. Relación con Expansiones de Características

En un modelo lineal con expansión fija:

$$
g_k(x)
=
v_{k0}
+
\sum_{j=1}^m
v_{kj}\varphi_j(x).
$$

En una red:

$$
\varphi_j(x)
=
f(w_{j0}+w_j^\top x)
$$

también se aprende.

- Modelos lineales generalizados: características elegidas de antemano.
- Redes: características internas ajustadas por datos.
- Esto aumenta flexibilidad, pero vuelve la optimización no convexa.

## Diapositiva 22. Interpretación Geométrica: Construcción de Convexos

**Teorema de Aproximación Universal**

Una red con una única capa oculta y una cantidad suficiente de unidades puede aproximar cualquier función continua en un conjunto compacto con precisión arbitraria, siempre que la función de activación sea no lineal y diferenciable.

Por ejemplo, 3 neuronas ocultas $\to$ 3 rectas $\to$ 1 triángulo (región cerrada).

Con suficientes unidades ocultas, una red puede aproximar indicadores suaves de regiones:

$$
\mathbb{I}\{x\in R\}
\approx
\text{combinación de sigmoides}.
$$

- El teorema es de existencia, no de entrenamiento.
- No dice cuántas unidades se necesitan en problemas reales.
- No garantiza buena generalización.

## Diapositiva 23. Representación Interactiva del Espacio

La diapositiva muestra una interfaz interactiva donde parámetros de neuronas ocultas transforman un problema XOR en un espacio de características linealmente separable.

![Interfaz interactiva para transformar un problema XOR](figures/clase-15/fig-23-interactive-xor.png){width=100%}

## Diapositiva 24. Descripción Local: Funciones de Activación Suaves

Para permitir el aprendizaje mediante el descenso de gradiente, elegimos mapeos no lineales $f(a)$ diferenciables. La derivada $f'(a)$ determina la dinámica de actualización de los pesos $w$.

| Función | Formulación $f(a)$ | Derivada $f'(a)$ |
|---|---|---|
| Sigmoide | $\frac{1}{1+e^{-a}}$ | $f(a)(1-f(a))$ |
| $\tanh$ | $\frac{e^a-e^{-a}}{e^a+e^{-a}}$ | $1-f(a)^2$ |
| ReLU | $\max(0,a)$ | $\begin{cases}1 & a>0\\0 & a<0\end{cases}$ |
| Step | $\begin{cases}1 & a\ge 0\\0 & a<0\end{cases}$ | Indefinida |

![Tabla de funciones de activación y perfiles geométricos](figures/clase-15/fig-24-activation-functions.png){width=85%}

**Saturación del gradiente**

La sigmoide y la tangente hiperbólica, cuando $|a|\to\infty$, cumplen $f'(a)\to 0$. Este fenómeno, intrínseco a las funciones acotadas, es el responsable del problema de *vanishing gradient* en redes profundas.

## Diapositiva 25. Interpretación Geométrica de una Neurona Sigmoide

Una unidad

$$
z=f(w^\top x+w_0)
$$

cambia más rápido cerca del hiperplano

$$
w^\top x+w_0=0.
$$

- Para una sigmoide, $z$ pasa suavemente de 0 a 1.
- El vector $w$ define la orientación de la transición.
- $\lVert w\rVert$ controla la pendiente de la transición.

Una capa oculta crea múltiples transiciones suaves; la salida las combina.

## Diapositiva 26. Red Feed-Forward

Una red *feed-forward* con $L$ capas se define recursivamente:

$$
z^{(0)}=x,
$$

$$
a^{(\ell)}
=
W^{(\ell)}z^{(\ell-1)}+b^{(\ell)},
\qquad
z^{(\ell)}=f^{(\ell)}(a^{(\ell)}),
$$

para $\ell=1,\ldots,L$.

En clasificación, la última capa produce *scores*:

$$
g(x;\theta)=a^{(L)}\in\mathbb{R}^c.
$$

Los parámetros son

$$
\theta=\{W^{(\ell)},b^{(\ell)}\}_{\ell=1}^L.
$$

Si todas las capas son lineales (o sea, $f$ es la función identidad), entonces cada capa es una transformación lineal:

$$
z^{(1)}=W^{(1)}x,
\qquad
z^{(2)}=W^{(2)}z^{(1)},
\qquad
y=W^{(3)}z^{(2)}.
$$

Entonces

$$
y
=
W^{(3)}W^{(2)}W^{(1)}x
=
W^\star x.
$$

La profundidad no aumenta la clase de funciones representables a menos que se introduzcan activaciones no lineales.

## Diapositiva 27. Red como Familia de Discriminantes

Para $c$ clases, la red produce

$$
g_i(x;\theta),
\qquad
i=1,\ldots,c.
$$

La regla de clasificación es

$$
\widehat{\omega}(x)=\omega_j
\quad
\text{si}
\quad
g_j(x;\theta)=\max_i g_i(x;\theta).
$$

**Fronteras**

La frontera entre $i$ y $j$ satisface

$$
g_i(x;\theta)-g_j(x;\theta)=0.
$$

Como $g_i-g_j$ es una composición no lineal, la frontera puede ser altamente no lineal.

## Diapositiva 28. Ejemplo: Problema del Estanque

Supongamos una clase que se encuentra en una **región confinada** y rodeada por otra clase en $\mathbb{R}^2$. Por ejemplo, una clase $\omega_1$ que representa un estanque de agua circular, y la clase $\omega_2$ que representa el terreno circundante.

Asumamos una arquitectura de red con una capa oculta de dos neuronas $(h=2)$ y funciones de activación idénticas $\sigma(a)=a^2$. Las funciones discriminantes para cada clase se modelan como:

$$
g_1(x;\theta)
=
w_{11}^{(2)}
\sigma\left(w_{1\cdot}^{(1)}x+b_1^{(1)}\right)
+
w_{12}^{(2)}
\sigma\left(w_{2\cdot}^{(1)}x+b_2^{(1)}\right)
+
b_1^{(2)}.
$$

$$
g_2(x;\theta)=0
\qquad
\text{(Clase de referencia)}.
$$

Fijemos los pesos del primer nivel para proyectar sobre los ejes coordenados de forma ortogonal:

$$
w_{1\cdot}^{(1)}=[1,0]^\top,
\qquad
b_1^{(1)}=0
\Longrightarrow
a_1=x_1.
$$

$$
w_{2\cdot}^{(1)}=[0,1]^\top,
\qquad
b_2^{(1)}=0
\Longrightarrow
a_2=x_2.
$$

Configuramos los pesos de la segunda capa para modelar una penalización por distancia:

$$
w_{11}^{(2)}=-1,
\qquad
w_{12}^{(2)}=-1,
\qquad
b_1^{(2)}=r^2
\quad
(r>0).
$$

Sustituyendo los parámetros en la definición del discriminante $g_1(x;\theta)$:

$$
g_1(x;\theta)
=
-1\cdot(x_1)^2-1\cdot(x_2)^2+r^2
=
r^2-(x_1^2+x_2^2).
$$

## Diapositiva 29. Ejemplo: Problema del Estanque

La regla de decisión óptima determina que la frontera satisface:

$$
g_1(x;\theta)-g_2(x;\theta)=0
\Longrightarrow
r^2-(x_1^2+x_2^2)=0.
$$

Luego, la ecuación algebraica resultante de la composición no lineal es:

$$
x_1^2+x_2^2=r^2,
$$

la cual define analíticamente una circunferencia de radio $r$ centrada en el origen.

- **Región de Decisión $\mathcal{R}_1$:** $\{x\in\mathbb{R}^2\mid \lVert x\rVert_2<r\}$ (interior del disco).
- **Región de Decisión $\mathcal{R}_2$:** $\{x\in\mathbb{R}^2\mid \lVert x\rVert_2>r\}$ (exterior del disco).

Modificando la matriz de pesos del segundo nivel $W^{(2)}$, la frontera adopta formas de secciones cónicas generales (elipses, parábolas, hipérbolas: hacer como ejercicio). En este ejemplo, la combinación de funciones de activación no lineales genera fronteras de decisión altamente no lineales (cónicas) en el espacio de entrada.

## Diapositiva 30. Salida Probabilística

Para interpretar *scores* como probabilidades posteriores estimadas, usamos softmax:

$$
y_i(x;\theta)
=
\frac{\exp(a_i)}
{\sum_{j=1}^c \exp(a_j)},
\qquad
i=1,\ldots,c.
$$

Entonces

$$
y_i(x;\theta)\ge 0,
\qquad
\sum_{i=1}^c y_i(x;\theta)=1.
$$

- $a_i$ son logits o *scores* previos a softmax.
- $y_i$ se interpreta como aproximación a $P(\omega_i\mid x)$.
- La decisión sigue siendo $\arg\max_i y_i(x;\theta)$.

## Diapositiva 31. Codificación de Targets

Para clasificación multiclase usamos codificación *one-hot*:

$$
t_k=(t_{k1},\ldots,t_{kc})^\top,
$$

donde

$$
t_{ki}
=
\begin{cases}
1, & \text{si } x_k \text{ pertenece a } \omega_i,\\
0, & \text{en otro caso}.
\end{cases}
$$

La red produce

$$
y_k=y(x_k;\theta)=(y_{k1},\ldots,y_{kc})^\top.
$$

Buscamos que $y_k$ asigne alta probabilidad a la clase correcta.

**Ejemplo:** clasificación de dígitos manuscritos.

![Red neuronal para clasificación de un dígito manuscrito](figures/clase-15/fig-31-digit-network.png){width=75%}

## Diapositiva 32. Funciones de Pérdida

**Error cuadrático:** en formulaciones clásicas, una función objetivo posible es

$$
J(\theta)
=
\frac{1}{2}
\sum_{k=1}^n
\sum_{i=1}^c
(t_{ki}-y_i(x_k;\theta))^2.
$$

- Natural para salidas continuas.
- Se conecta con regresión y mínimos cuadrados.
- No siempre es la mejor opción para clasificación probabilística.

**Cross-entropy:** para clasificación con softmax, la pérdida usual es

$$
J(\theta)
=
-
\sum_{k=1}^n
\sum_{i=1}^c
t_{ki}\log y_i(x_k;\theta).
$$

Si $x_k$ pertenece a la clase $r$, entonces $J_k(\theta)=-\log y_r(x_k;\theta)$.

Minimizar entropía cruzada equivale a maximizar la log-verosimilitud condicional de un modelo categórico:

$$
\prod_{k=1}^n
\prod_{i=1}^c
y_i(x_k;\theta)^{t_{ki}}.
$$

## Diapositiva 33. Optimización

**Sección:** Optimización.

## Diapositiva 34. Entrenamiento como Optimización

El aprendizaje consiste en resolver

$$
\widehat{\theta}
=
\arg\min_\theta J(\theta).
$$

A diferencia de muchos modelos lineales convexos, en redes profundas $J$ suele ser no convexa.

- Hay múltiples mínimos locales y puntos silla.
- La parametrización tiene simetrías: permutar unidades ocultas puede representar la misma función.
- La optimización usa gradientes calculados eficientemente.

La herramienta central es el algoritmo de **backpropagation**.

Publicado en 1986 por David Rumelhart, Geoffrey Hinton y Ronald Williams: "Learning representations by back-propagating errors" (*Nature*).

## Diapositiva 35. Descenso por Gradiente

La regla básica es

$$
\theta^{(m+1)}
=
\theta^{(m)}
-
\eta_m\nabla_\theta J(\theta^{(m)}),
$$

donde $\eta_m>0$ es la tasa de aprendizaje.

- Si $\eta_m$ es muy grande, el entrenamiento puede diverger.
- Si $\eta_m$ es muy pequeña, el entrenamiento puede ser muy lento.
- En la práctica se usan variantes estocásticas y adaptativas.

## Diapositiva 36. Gradiente Estocástico

Para una pérdida descompuesta

$$
J(\theta)
=
\sum_{k=1}^n
J_k(\theta),
$$

el gradiente completo es

$$
\nabla J(\theta)
=
\sum_{k=1}^n
\nabla J_k(\theta).
$$

En SGD usamos una observación o mini-batch $B_m$:

$$
\theta^{(m+1)}
=
\theta^{(m)}
-
\eta_m
\frac{1}{|B_m|}
\sum_{k\in B_m}
\nabla J_k(\theta^{(m)}).
$$

- Reduce costo por actualización.
- Introduce ruido que puede ayudar a escapar de regiones planas.
- Hace necesario controlar escalas, inicialización y *learning rate*.

## Diapositiva 37. Backpropagation: Problema Computacional

Queremos calcular derivadas de $J$ respecto de todos los pesos:

$$
\frac{\partial J}{\partial w_{ji}^{(\ell)}}.
$$

Una red puede tener miles o millones de parámetros. Calcular derivadas por diferencias finitas sería inviable:

$$
\frac{\partial J}{\partial\theta_r}
\approx
\frac{J(\theta_r+\varepsilon)-J(\theta_r)}
{\varepsilon}.
$$

**Idea**

Backpropagation aplica la regla de la cadena reutilizando cantidades intermedias para obtener todos los gradientes en tiempo proporcional al costo de evaluar la red.

## Diapositiva 38. Notación Local de una Unidad

Para una unidad $j$ en una capa:

$$
a_j=\sum_i w_{ji}z_i,
\qquad
z_j=f(a_j).
$$

Aquí $z_i$ son salidas de la capa anterior.

Definimos la señal de error local

$$
\delta_j
=
\frac{\partial J}{\partial a_j}.
$$

Entonces

$$
\frac{\partial J}{\partial w_{ji}}
=
\frac{\partial J}{\partial a_j}
\frac{\partial a_j}{\partial w_{ji}}
=
\delta_j z_i.
$$

Esta fórmula es el núcleo operativo de backpropagation.

## Diapositiva 39. Delta en la Capa de Salida

Supongamos error cuadrático:

$$
J_k
=
\frac{1}{2}
\sum_j(t_j-z_j)^2.
$$

Para una unidad de salida $j$:

$$
\delta_j
=
\frac{\partial J_k}{\partial a_j}
=
\frac{\partial J_k}{\partial z_j}
\frac{\partial z_j}{\partial a_j}.
$$

Como

$$
\frac{\partial J_k}{\partial z_j}
=
z_j-t_j,
$$

obtenemos

$$
\delta_j
=
(z_j-t_j)f'(a_j).
$$

## Diapositiva 40. Delta en una Capa Oculta

Para una unidad oculta $j$, su efecto sobre $J$ pasa por unidades posteriores $k$:

$$
\delta_j
=
\frac{\partial J}{\partial a_j}
=
f'(a_j)
\sum_k w_{kj}\delta_k.
$$

**Interpretación**

La responsabilidad de error de una unidad oculta es una suma ponderada de las responsabilidades de error de las unidades a las que alimenta, multiplicada por la derivada local.

Esta recursión se evalúa desde la salida hacia atrás.

## Diapositiva 41. Algoritmo de Backpropagation

Para cada mini-batch:

1. **Forward pass:** calcular activaciones

$$
a^{(\ell)},z^{(\ell)},
\qquad
\ell=1,\ldots,L.
$$

2. Calcular pérdida $J$ y deltas de salida.
3. **Backward pass:** propagar deltas

$$
\delta^{(\ell)}
=
\left((W^{(\ell+1)})^\top\delta^{(\ell+1)}\right)
\odot
f'(a^{(\ell)}).
$$

4. Calcular gradientes

$$
\frac{\partial J}{\partial W^{(\ell)}}
=
\delta^{(\ell)}(z^{(\ell-1)})^\top.
$$

5. Actualizar parámetros por descenso.

## Diapositiva 42. Backpropagation Algorithm

La diapositiva descompone una neurona como suma ponderada seguida de un elemento no lineal:

$$
e=x_1w_1+x_2w_2,
\qquad
y=f(e).
$$

![Descomposición de una neurona para backpropagation](figures/clase-15/fig-42-backprop-neuron.png){width=80%}

## Diapositiva 43. Backpropagation Algorithm

La red de ejemplo tiene entradas $x_1,x_2$, tres unidades en la primera capa, dos en la segunda y una salida $y$.

![Red de ejemplo para la secuencia de backpropagation](figures/clase-15/fig-43-backprop-network.png){width=80%}

## Diapositiva 44. Backpropagation Algorithm

Primera activación oculta:

$$
y_1
=
f_1\left(w_{(x1)1}x_1+w_{(x2)1}x_2\right).
$$

![Cálculo de la activación y1](figures/clase-15/fig-44-backprop-y1.png){width=80%}

## Diapositiva 45. Backpropagation Algorithm

Segunda activación oculta:

$$
y_2
=
f_2\left(w_{(x1)2}x_1+w_{(x2)2}x_2\right).
$$

![Cálculo de la activación y2](figures/clase-15/fig-45-backprop-y2.png){width=80%}

## Diapositiva 46. Backpropagation Algorithm

Tercera activación oculta:

$$
y_3
=
f_3\left(w_{(x1)3}x_1+w_{(x2)3}x_2\right).
$$

![Cálculo de la activación y3](figures/clase-15/fig-46-backprop-y3.png){width=80%}

## Diapositiva 47. Backpropagation Algorithm

Activación en la segunda capa:

$$
y_4
=
f_4(w_{14}y_1+w_{24}y_2+w_{34}y_3).
$$

![Cálculo de la activación y4](figures/clase-15/fig-47-backprop-y4.png){width=80%}

## Diapositiva 48. Backpropagation Algorithm

Otra activación en la segunda capa:

$$
y_5
=
f_5(w_{15}y_1+w_{25}y_2+w_{35}y_3).
$$

![Cálculo de la activación y5](figures/clase-15/fig-48-backprop-y5.png){width=80%}

## Diapositiva 49. Backpropagation Algorithm

Salida de la red:

$$
y
=
f_6(w_{46}y_4+w_{56}y_5).
$$

![Cálculo de la salida de la red](figures/clase-15/fig-49-backprop-output.png){width=80%}

## Diapositiva 50. Backpropagation Algorithm

La señal de error de salida se representa como:

$$
\delta = z-y.
$$

![Delta en la salida](figures/clase-15/fig-50-backprop-delta-output.png){width=80%}

## Diapositiva 51. Backpropagation Algorithm

Retropropagación hacia la unidad $4$:

$$
\delta_4=w_{46}\delta.
$$

![Retropropagación hacia delta4](figures/clase-15/fig-51-backprop-delta4.png){width=80%}

## Diapositiva 52. Backpropagation Algorithm

Retropropagación hacia la unidad $5$:

$$
\delta_5=w_{56}\delta.
$$

![Retropropagación hacia delta5](figures/clase-15/fig-52-backprop-delta5.png){width=80%}

## Diapositiva 53. Backpropagation Algorithm

Retropropagación hacia la unidad $1$:

$$
\delta_1=w_{14}\delta_4+w_{15}\delta_5.
$$

![Retropropagación hacia delta1](figures/clase-15/fig-53-backprop-delta1.png){width=80%}

## Diapositiva 54. Backpropagation Algorithm

Retropropagación hacia la unidad $2$:

$$
\delta_2=w_{24}\delta_4+w_{25}\delta_5.
$$

![Retropropagación hacia delta2](figures/clase-15/fig-54-backprop-delta2.png){width=80%}

## Diapositiva 55. Backpropagation Algorithm

Retropropagación hacia la unidad $3$:

$$
\delta_3=w_{34}\delta_4+w_{35}\delta_5.
$$

![Retropropagación hacia delta3](figures/clase-15/fig-55-backprop-delta3.png){width=80%}

## Diapositiva 56. Backpropagation Algorithm

Actualización de pesos de entrada hacia la unidad $1$:

$$
w'_{(x1)1}
=
w_{(x1)1}
+
\eta\delta_1
\frac{df_1(e)}{de}x_1,
$$

$$
w'_{(x2)1}
=
w_{(x2)1}
+
\eta\delta_1
\frac{df_1(e)}{de}x_2.
$$

![Actualización de pesos hacia la unidad 1](figures/clase-15/fig-56-backprop-update-input1.png){width=80%}

## Diapositiva 57. Backpropagation Algorithm

Actualización de pesos de entrada hacia la unidad $2$:

$$
w'_{(x1)2}
=
w_{(x1)2}
+
\eta\delta_2
\frac{df_2(e)}{de}x_1,
$$

$$
w'_{(x2)2}
=
w_{(x2)2}
+
\eta\delta_2
\frac{df_2(e)}{de}x_2.
$$

![Actualización de pesos hacia la unidad 2](figures/clase-15/fig-57-backprop-update-input2.png){width=80%}

## Diapositiva 58. Backpropagation Algorithm

Actualización de pesos de entrada hacia la unidad $3$:

$$
w'_{(x1)3}
=
w_{(x1)3}
+
\eta\delta_3
\frac{df_3(e)}{de}x_1,
$$

$$
w'_{(x2)3}
=
w_{(x2)3}
+
\eta\delta_3
\frac{df_3(e)}{de}x_2.
$$

![Actualización de pesos hacia la unidad 3](figures/clase-15/fig-58-backprop-update-input3.png){width=80%}

## Diapositiva 59. Backpropagation Algorithm

Actualización de pesos hacia la unidad $4$:

$$
w'_{14}=w_{14}+\eta\delta_4\frac{df_4(e)}{de}y_1,
$$

$$
w'_{24}=w_{24}+\eta\delta_4\frac{df_4(e)}{de}y_2,
$$

$$
w'_{34}=w_{34}+\eta\delta_4\frac{df_4(e)}{de}y_3.
$$

![Actualización de pesos hacia la unidad 4](figures/clase-15/fig-59-backprop-update-hidden4.png){width=80%}

## Diapositiva 60. Backpropagation Algorithm

Actualización de pesos hacia la unidad $5$:

$$
w'_{15}=w_{15}+\eta\delta_5\frac{df_5(e)}{de}y_1,
$$

$$
w'_{25}=w_{25}+\eta\delta_5\frac{df_5(e)}{de}y_2,
$$

$$
w'_{35}=w_{35}+\eta\delta_5\frac{df_5(e)}{de}y_3.
$$

![Actualización de pesos hacia la unidad 5](figures/clase-15/fig-60-backprop-update-hidden5.png){width=80%}

## Diapositiva 61. Backpropagation Algorithm

Actualización de pesos de salida:

$$
w'_{46}=w_{46}+\eta\delta\frac{df_6(e)}{de}y_4,
$$

$$
w'_{56}=w_{56}+\eta\delta\frac{df_6(e)}{de}y_5.
$$

![Actualización de pesos de salida](figures/clase-15/fig-61-backprop-update-output.png){width=80%}

## Diapositiva 62. Softmax y Entropía Cruzada: Simplificación

Si la salida es softmax y la pérdida es entropía cruzada:

$$
y_i
=
\frac{e^{a_i}}{\sum_j e^{a_j}},
\qquad
J_k
=
-
\sum_i t_i\log y_i,
$$

entonces la derivada respecto del logit es

$$
\frac{\partial J_k}{\partial a_i}
=
y_i-t_i.
$$

**Resultado importante**

Para softmax + cross-entropy, el delta de salida es simplemente

$$
\delta_i=y_i-t_i.
$$

Esta simplicidad explica su uso dominante en clasificación multiclase.

## Diapositiva 63. Controlando Sesgo-Varianza

**Sección:** Controlando sesgo-varianza.

## Diapositiva 64. Profundidad Versus Anchura

Una sola capa oculta ancha puede aproximar muchas funciones, pero la profundidad puede representar ciertas composiciones de forma más eficiente.

$$
x\mapsto z^{(1)}\mapsto z^{(2)}\mapsto \cdots \mapsto z^{(L)}.
$$

- Capas tempranas aprenden transformaciones locales o simples.
- Capas posteriores combinan representaciones previas.
- La composición puede reutilizar subestructuras.

## Diapositiva 65. Redes ReLU y Fronteras por Partes Lineales

Con ReLU,

$$
f(a)=\max(0,a),
$$

la red es una función por partes lineal.

- Cada unidad introduce un pliegue en el espacio.
- La composición de capas crea muchas regiones lineales.
- La frontera de decisión puede ser muy compleja aunque cada pieza sea lineal.

**Comparación con CART**

CART crea regiones rectangulares alineadas a ejes. Redes ReLU crean regiones poliedrales con orientaciones aprendidas.

## Diapositiva 66. Clasificación Binaria con Salida Logística

Para dos clases, una red puede producir un logit $a(x)$:

$$
y(x)=\sigma(a(x)).
$$

Interpretamos

$$
y(x)\approx P(\omega_1\mid x),
\qquad
1-y(x)\approx P(\omega_2\mid x).
$$

La frontera es

$$
y(x)=\frac{1}{2}
\Longleftrightarrow
a(x)=0.
$$

Por lo tanto, la geometría de la frontera está determinada por el conjunto de nivel cero del logit aprendido.

## Diapositiva 67. ANN Interactivo

La diapositiva muestra un *playground* interactivo de una red neuronal artificial para visualizar fronteras y activaciones.

![Playground interactivo de una red neuronal artificial](figures/clase-15/fig-67-ann-playground.png){width=100%}

**Playground interactive 2**

## Diapositiva 68. Clasificación Multiclase con Softmax

En $c$ clases:

$$
y(x)=\operatorname{softmax}(a(x)),
$$

y se decide

$$
\widehat{\omega}(x)=\omega_j,
\qquad
j=\arg\max_i y_i(x).
$$

Como softmax preserva el orden de los logits:

$$
\arg\max_i y_i(x)
=
\arg\max_i a_i(x).
$$

**Frontera por pares**

Entre clases $i$ y $j$:

$$
a_i(x)-a_j(x)=0.
$$

## Diapositiva 69. Regularización por Penalización de Pesos

Una forma clásica de controlar complejidad es *weight decay*:

$$
J_\lambda(\theta)
=
J(\theta)
+
\frac{\lambda}{2}
\sum_\ell
\lVert W^{(\ell)}\rVert_F^2.
$$

La actualización por gradiente incluye

$$
\frac{\partial J_\lambda}{\partial W^{(\ell)}}
=
\frac{\partial J}{\partial W^{(\ell)}}
+
\lambda W^{(\ell)}.
$$

- Pesos pequeños tienden a funciones más suaves.
- Reduce varianza efectiva.
- No reemplaza validación; $\lambda$ es hiperparámetro.

## Diapositiva 70. Regularización por Early Stopping

Durante el entrenamiento, monitoreamos pérdida en validación:

$$
J_{\text{val}}(\theta^{(m)}).
$$

- Al inicio, train y validación suelen mejorar.
- Luego train puede seguir mejorando mientras validación empeora.
- Early stopping guarda el modelo antes del sobreajuste.

**Lectura estadística**

El número de iteraciones funciona como parámetro de complejidad. Entrenar más no siempre mejora generalización.

**Visualización sugerida**

Curvas train/validation loss con marca vertical en la época elegida por early stopping.

## Diapositiva 71. Dropout

Dropout apaga aleatoriamente unidades durante entrenamiento:

$$
\widetilde{z}_j=r_jz_j,
\qquad
r_j\sim\operatorname{Bernoulli}(q).
$$

- Evita coadaptaciones excesivas.
- Puede interpretarse como entrenar muchos submodelos compartiendo pesos.
- En predicción se usa la red completa con escalamiento apropiado.

Dropout introduce una idea tipo ensamble dentro del entrenamiento de una red: muchas subredes implícitas contribuyen a un predictor final. Esto reduce varianza efectiva, mejora generalización, pero puede aumentar sesgo.

![Dropout como ensamble implícito de subredes](figures/clase-15/fig-71-dropout-ensemble.png){width=70%}

## Diapositiva 72. Normalización y Escala de Entrada

Redes entrenadas por gradiente son sensibles a escalas:

$$
x_j'
=
\frac{x_j-\mu_j}{s_j}.
$$

- Variables con escalas muy distintas distorsionan gradientes.
- Normalizar acelera y estabiliza entrenamiento.
- En clasificación tabular, estandarización suele ser requisito práctico.

**Comparación**

Árboles son invariantes a transformaciones monótonas de variables individuales; redes y modelos lineales no lo son.

## Diapositiva 73. Inicialización de Pesos

Si todos los pesos se inicializan iguales, unidades de una capa reciben el mismo gradiente y permanecen simétricas.

Por eso inicializamos aleatoriamente:

$$
w_{ji}^{(\ell)}
\sim
\text{distribución centrada en }0.
$$

- Pesos demasiado grandes saturan sigmoides.
- Pesos demasiado pequeños reducen señal.
- Inicializaciones Xavier/He ajustan varianza según tamaño de capa.

La inicialización afecta optimización, estabilidad y reproducibilidad.

## Diapositiva 74. Gradientes que Desaparecen

Para sigmoide:

$$
\sigma'(a)=\sigma(a)(1-\sigma(a)).
$$

Si $|a|$ es grande, $\sigma'(a)\approx 0$.

En redes profundas, backprop multiplica muchas derivadas:

$$
\delta^{(\ell)}
=
\left((W^{(\ell+1)})^\top\delta^{(\ell+1)}\right)
\odot
f'(a^{(\ell)}).
$$

**Problema**

Si muchas derivadas son pequeñas, las capas tempranas aprenden muy lentamente.

ReLU y normalización ayudan a mitigar este fenómeno.

## Diapositiva 75. Gradientes Explosivos

Si las matrices de pesos amplifican repetidamente la señal:

$$
\lVert \delta^{(\ell)}\rVert
\gg
\lVert \delta^{(L)}\rVert,
$$

los gradientes pueden crecer demasiado.

**Consecuencias**

- Actualizaciones inestables.
- Pérdida que diverge.
- Sensibilidad extrema al *learning rate*.

**Remedios comunes**

- normalización;
- *clipping* de gradientes;
- inicialización adecuada;
- arquitecturas con conexiones residuales.

## Diapositiva 76. Capacidad y Dimensión VC

En clasificación estadística, la capacidad de una familia afecta generalización. Para una clase $\mathcal{G}$, el riesgo empírico puede subestimar el riesgo verdadero si $\mathcal{G}$ es muy rica.

$$
\widehat{R}_n(g)
=
\frac{1}{n}
\sum_{k=1}^n
\mathbb{I}\{g(x_k)\ne y_k\}.
$$

Redes con muchos parámetros pueden tener alta capacidad.

**Idea clave**

La generalización no depende solo del número de parámetros, sino también de regularización, optimización, datos y arquitectura.

## Diapositiva 77. Comparación con Modelos Lineales

| Lineales | Redes |
|---|---|
| $g_i(x)=w_i^\top x+w_{i0}$ | $g_i(x)=g_i(x;\theta)$ |
| Optimización más simple. | Optimización no convexa. |
| Menor varianza. | Mayor flexibilidad. |
| Fronteras rígidas. | Fronteras no lineales. |
| Interpretación directa de coeficientes. | Interpretación menos directa. |

## Diapositiva 78. Comparación con CART

CART aprende particiones mediante reglas:

$$
x_j\le c.
$$

Una red aprende transformaciones:

$$
z^{(\ell)}
=
f(W^{(\ell)}z^{(\ell-1)}+b^{(\ell)}).
$$

- CART: reglas locales, interpretables, *axis-aligned*.
- Red: representaciones distribuidas, diferenciables, menos transparentes.
- CART maneja variables mixtas naturalmente.
- Redes requieren codificación, escalado y cuidado de optimización.

## Diapositiva 79. Comparación con Bagging

Bagging promedia modelos entrenados en muestras perturbadas:

$$
\widehat{f}_{\text{bag}}(x)
=
\frac{1}{B}
\sum_{b=1}^B
\widehat{f}_b(x)
$$

en regresión, o voto mayoritario en clasificación.

Redes suelen entrenar un único modelo grande:

$$
\widehat{f}(x)=f(x;\widehat{\theta}).
$$

- Bagging reduce varianza por agregación externa.
- Redes controlan varianza por regularización, datos y arquitectura.
- También se pueden ensamblar redes, pero el costo es mayor.

## Diapositiva 80. Comparación con Boosting

Boosting suma modelos débiles:

$$
F_M(x)
=
\sum_{m=1}^M
\alpha_m h_m(x).
$$

Una red con una capa oculta tiene forma análoga:

$$
g(x)
=
v_0
+
\sum_{j=1}^m
v_j f(w_j^\top x+w_{j0}).
$$

**Diferencia esencial**

En boosting, las funciones base se agregan secuencialmente. En una red, todas las unidades se ajustan conjuntamente por gradiente.

Esta diferencia cambia optimización, regularización e interpretación.

## Diapositiva 81. Arquitectura como Sesgo Inductivo

La arquitectura define qué funciones son fáciles de representar y aprender.

- **MLP denso:** apropiado para datos tabulares o representaciones ya vectorizadas.
- **Convolucional:** aprovecha localidad y traslación en imágenes.
- **Recurrente / secuencial:** modela dependencias temporales.
- **Transformer:** atención y relaciones globales entre tokens.

**Principio general**

La arquitectura no es un detalle computacional: expresa hipótesis sobre la estructura de los datos.

## Diapositiva 82. MLP para Datos Tabulares

En datos tabulares, una red densa no siempre supera a ensambles de árboles.

**Razones**

- Variables heterogéneas y escalas distintas.
- Interacciones irregulares.
- Tamaños muestrales moderados.
- Necesidad de *tuning* cuidadoso.

Aun así, MLPs son útiles cuando:

- hay muchas variables continuas;
- se combinan con *embeddings*;
- hay grandes volúmenes de datos;
- se integran con otros módulos diferenciables.

## Diapositiva 83. Diagnóstico: Curva de Aprendizaje

Para analizar entrenamiento, graficamos

$$
J_{\text{train}}(m),
\qquad
J_{\text{val}}(m)
$$

por época $m$.

**Patrones comunes**

- Ambas altas: subajuste o mala optimización.
- Train baja, validación alta: sobreajuste.
- Curvas ruidosas: *learning rate* alto o mini-batches pequeños.
- Meseta temprana: *learning rate* bajo, activaciones saturadas o arquitectura insuficiente.

## Diapositiva 84. Costos y Decisiones

Con costos $\lambda(\alpha_i\mid\omega_j)$, la decisión óptima minimiza riesgo condicional:

$$
R(\alpha_i\mid x)
=
\sum_{j=1}^c
\lambda(\alpha_i\mid\omega_j)P(\omega_j\mid x).
$$

Si la red estima $P(\omega_j\mid x)$, podemos decidir por

$$
\alpha^\star(x)
=
\arg\min_i
\sum_{j=1}^c
\lambda(\alpha_i\mid\omega_j)y_j(x).
$$

**Conexión con Duda et al.**

La red no reemplaza la teoría de decisión bayesiana; puede proveer estimaciones de posteriores para aplicar reglas de decisión con costos.

## Diapositiva 85. Errores Comunes al Entrenar Redes

- No escalar variables de entrada.
- Usar *learning rate* demasiado alto.
- Elegir arquitectura excesiva para pocos datos.
- Evaluar en test mientras se tunean hiperparámetros.
- Interpretar softmax como probabilidad calibrada sin verificar.
- Confundir pérdida baja en train con buena clasificación futura.

**Regla práctica**

Antes de hacer la red más grande, verificar datos, escalado, curva de aprendizaje, baseline lineal y baseline de árboles.

## Diapositiva 86. Resumen Matemático

**Discriminantes**

$$
\widehat{\omega}(x)
=
\omega_{\arg\max_i g_i(x)}.
$$

**Red feed-forward**

$$
z^{(\ell)}
=
f^{(\ell)}(W^{(\ell)}z^{(\ell-1)}+b^{(\ell)}).
$$

**Softmax**

$$
y_i
=
\frac{e^{a_i}}{\sum_j e^{a_j}}.
$$

**Cross-entropy**

$$
J
=
-
\sum_k
\sum_i
t_{ki}\log y_i(x_k;\theta).
$$

**Backprop**

$$
\frac{\partial J}{\partial w_{ji}^{(\ell)}}
=
\delta_j^{(\ell)}z_i^{(\ell-1)}.
$$

## Diapositiva 87. Resumen Conceptual

1. Una red neuronal es una familia de funciones discriminantes no lineales.
2. La no linealidad proviene de activaciones compuestas en capas.
3. Backpropagation calcula gradientes eficientemente mediante regla de la cadena.
4. Softmax y entropía cruzada conectan redes con estimación de posteriores.
5. La flexibilidad requiere regularización y validación cuidadosa.
6. Frente a bagging/boosting, las redes aprenden representaciones diferenciables en lugar de combinar árboles.

**Idea final**

Las redes neuronales extienden la lógica de funciones discriminantes: en lugar de elegir manualmente una frontera, aprenden una transformación del espacio donde la decisión se vuelve más simple.

## Diapositiva 88. Sugerencias de Experimentación

Utilizar los notebooks provistos para experimentar con redes en un dataset 2D. Sugerencias:

- Construir un dataset 2D no lineal. Probar con *moons*, XOR o discos concéntricos.
- Comparar discriminantes lineales, CART, boosting y MLP.
- Visualizar frontera por época de entrenamiento.
- Mostrar activaciones ocultas como mapas de calor.
- Graficar pérdida, accuracy, márgenes y calibración.
- Experimentar con profundidad, ancho, activación y early stopping.
- Experimentar con distintas arquitecturas.
- Experimentar con dropout y regularización por peso.
