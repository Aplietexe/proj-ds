---
title: "Evaluación de Clasificadores y Desbalance de Datos"
---

## Diapositiva 1

**Portada**

- Evaluación de clasificadores y desbalance de datos
- Clase 11 - 2026-05-05
- Ciencias de datos 2026 - FaMAF

## Diapositiva 2. Hoja de Ruta

La clase se organiza en dos bloques:

1. **Parámetros de regularización**
   - Repaso: márgenes geométricos y funcionales de costo
   - La matriz de Gram y su construcción explícita
   - Kernel SVM
2. **Evaluación y fiabilidad del clasificador**
   - Métricas de confusión y básicas
   - Análisis ROC y Precision-Recall
   - Índice Kappa de Cohen

## Diapositiva 3. Parámetros de Regularización

**Sección:** Parámetros de regularización.

## Diapositiva 4. Refuerzo de Aviones en la Segunda Guerra Mundial

Durante la Segunda Guerra Mundial, el ejército de EE.UU. analizó los aviones que regresaban de combate para decidir dónde poner más blindaje.

Los militares sugirieron reforzar las zonas con más agujeros de bala, como alas y fuselaje.

Los estadísticos, por ejemplo Abraham Wald, respondieron:

> "No. Deben blindar los motores, donde no hay agujeros. Los aviones que recibieron disparos ahí, nunca volvieron."

La idea es que mirar solo los casos observados puede inducir una conclusión equivocada.

![Avión usado para ilustrar sesgo de supervivencia](figures/clase-11/fig-04-survivorship-plane.png)

## Diapositiva 5. Motivación: Evaluación Más Allá del Margen Geométrico

La diapositiva muestra una escena donde el objeto relevante queda oculto entre la vegetación. La motivación es que una frontera o margen geométrico no alcanza si no sabemos evaluar el comportamiento real del sistema.

![Objeto oculto entre vegetación](figures/clase-11/fig-05-forest-hidden-object.png)

## Diapositiva 6. Motivación: Evaluación Más Allá del Margen Geométrico

La diapositiva muestra un dron frente a un avión, como ejemplo de una situación donde una decisión automática incorrecta puede ser costosa.

![Dron frente a un avión](figures/clase-11/fig-06-drone-airplane.png)

## Diapositiva 7. Motivación: Evaluación Más Allá del Margen Geométrico

Queremos que el modelo:

- no sea demasiado simple;
- no sea demasiado complejo;
- tenga buen rendimiento fuera de muestra.

Para eso necesitamos:

- medir bien;
- estimar errores.

## Diapositiva 8. Regularización y Margen: Formulación Primal

Partimos del clasificador lineal:

$$
g(x)=w^Tx+b.
$$

En un escenario no linealmente separable, buscamos minimizar el funcional de costo.

**Problema de optimización primal:**

$$
\min_{w,b,\xi} J(w,\xi)
=
\frac{1}{2}\lVert w\rVert^2
+
C\sum_{i=1}^n \xi_i
$$

sujeto a:

$$
y_i(w^Tx_i+b)\ge 1-\xi_i,
\qquad
\forall i,
$$

$$
\xi_i\ge 0.
$$

Las variables $\xi_i$ son variables de holgura, o *slack variables*.

Interpretación formal:

- el término $\frac{1}{2}\lVert w\rVert^2$ es el regularizador de Tikhonov, inversamente proporcional al margen geométrico $\gamma=1/\lVert w\rVert$;
- $C$ actúa como hiperparámetro de penalización que balancea el *bias-variance tradeoff*.

## Diapositiva 9. Mapeo No Lineal y Espacios de Características

Para abordar fronteras no lineales, proyectamos $x\in\mathbb{R}^d$ a un espacio de mayor dimensión $\mathcal{H}$ mediante una transformación:

$$
\phi:\mathbb{R}^d\to\mathcal{H}.
$$

- Sea $\mathcal{H}$ un **Reproducing Kernel Hilbert Space** (RKHS).
- El clasificador se define ahora como:

$$
f(x)=\langle w,\phi(x)\rangle_{\mathcal{H}}+b.
$$

**Proposición:** si $\phi(x)$ es una transformación cuadrática, por ejemplo:

$$
\phi(x)=[x_1,x_2,x_1^2,x_2^2,x_1x_2],
$$

una frontera hiperplana en $\mathcal{H}$ induce una sección cónica en $\mathbb{R}^d$.

## Diapositiva 10. Formulación de Lagrange para el Dual

Para resolver el problema con restricciones, construimos la función lagrangiana con multiplicadores:

$$
\alpha_i\ge 0,
\qquad
\mu_i\ge 0.
$$

El Lagrangiano es:

$$
L(w,b,\xi,\alpha,\mu)
=
\frac{1}{2}\lVert w\rVert^2
+
C\sum_i \xi_i
-
\sum_i \alpha_i
\left[
y_i(w^T\phi(x_i)+b)-1+\xi_i
\right]
-
\sum_i \mu_i\xi_i.
$$

Aplicando las condiciones de primer orden, o KKT:

$$
\frac{\partial L}{\partial w}=0
\quad\Longrightarrow\quad
w=\sum_{i=1}^n \alpha_i y_i\phi(x_i),
$$

$$
\frac{\partial L}{\partial b}=0
\quad\Longrightarrow\quad
\sum_{i=1}^n \alpha_i y_i=0,
$$

$$
\frac{\partial L}{\partial \xi_i}=0
\quad\Longrightarrow\quad
C-\alpha_i-\mu_i=0
\quad\Longrightarrow\quad
0\le \alpha_i\le C.
$$

## Diapositiva 11. El Problema Dual de Wolfe

Sustituyendo los resultados de las derivadas en $L$, obtenemos la forma dual.

**Dualidad de Wolfe:**

$$
\max_\alpha
\sum_{i=1}^n \alpha_i
-
\frac{1}{2}
\sum_{i,j}
\alpha_i\alpha_j y_i y_j
\langle \phi(x_i),\phi(x_j)\rangle_{\mathcal{H}}
$$

sujeto a:

$$
\sum_i \alpha_i y_i=0,
\qquad
0\le \alpha_i\le C.
$$

El producto interno se reemplaza por:

$$
K(x_i,x_j)=\langle \phi(x_i),\phi(x_j)\rangle_{\mathcal{H}}.
$$

**Kernel trick:** no requerimos la forma explícita de $\phi(x)$, solo la función de kernel $K(\cdot,\cdot)$ que representa el producto escalar en $\mathcal{H}$.

## Diapositiva 12. Teorema del Representador

A partir de la dualidad, la función de discriminación final para un vector de prueba $x$ se expresa como:

$$
g(x)
=
\sum_{i\in S}\alpha_i y_i K(x_i,x)+b.
$$

Donde $S$ es el conjunto de vectores de soporte, es decir, los puntos con $\alpha_i>0$.

- **Sparsity:** la solución es dispersa; solo los puntos sobre o dentro del margen, donde las restricciones KKT son activas, definen la frontera.
- **Complejidad:** depende del número de vectores de soporte, no necesariamente de la dimensión $d$.

Ejemplos de kernels comunes:

- **Lineal:** $K(x,x')=x^Tx'$.
- **Polinomial:** $K(x,x')=(x^Tx'+c)^p$.
- **RBF, o gaussiano:** $K(x,x')=\exp(-\gamma\lVert x-x'\rVert^2)$.

## Diapositiva 13. La Matriz de Gram $(G)$

En la formulación dual de SVM, el optimizador no requiere conocer $\phi(x)$, sino únicamente las interacciones mutuas capturadas en la matriz de Gram.

**Definición:** dada una muestra de entrenamiento $\{x_1,\ldots,x_n\}$, la matriz de Gram $G\in\mathbb{R}^{n\times n}$ se define como:

$$
G_{ij}
=
K(x_i,x_j)
=
\langle \phi(x_i),\phi(x_j)\rangle_{\mathcal{H}}.
$$

Propiedades fundamentales:

1. **Simetría:** $G_{ij}=G_{ji}$.
2. **Semidefinida positiva:** $v^TGv\ge 0$ para cualquier vector $v$. Esto garantiza que el problema de optimización cuadrática sea convexo.

## Diapositiva 14. Construcción Explícita de la Matriz de Gram $G$

Sea:

$$
\mathcal{D}=\{x_1,x_2,\ldots,x_n\}
$$

nuestro conjunto de entrenamiento con $n$ patrones en $\mathbb{R}^d$. La matriz de Gram es la representación exhaustiva de las similitudes en el RKHS.

La matriz $G\in\mathbb{R}^{n\times n}$ se construye evaluando el kernel para cada par de muestras:

$$
G=
\begin{pmatrix}
K(x_1,x_1) & K(x_1,x_2) & \cdots & K(x_1,x_n)\\
K(x_2,x_1) & K(x_2,x_2) & \cdots & K(x_2,x_n)\\
\vdots & \vdots & \ddots & \vdots\\
K(x_n,x_1) & K(x_n,x_2) & \cdots & K(x_n,x_n)
\end{pmatrix}.
$$

Para un kernel lineal:

$$
K(x_i,x_j)=x_i^Tx_j,
$$

entonces $G$ es simplemente el producto de la matriz de diseño $X$:

$$
G=XX^T.
$$

Para un kernel RBF:

$$
G_{ij}
=
\exp\left(
-\gamma
\sum_{k=1}^d
(x_{i,k}-x_{j,k})^2
\right).
$$

## Diapositiva 15. Implicancias Algebraicas de $G$

- **Almacenamiento:** el costo espacial es $O(n^2)$. Para $n=10^5$, $G$ requiere aproximadamente 40 GB, lo que motiva algoritmos como SMO (*Sequential Minimal Optimization*) para no cargarla completa en RAM.
- **Rango:** $\operatorname{rank}(G)\le \min(n,\dim(\mathcal{H}))$. En el caso de RBF, $\operatorname{rank}(G)$ suele ser $n$, indicando que los puntos son linealmente independientes en $\mathcal{H}$.
- **Criterio de positividad:** por el teorema de Mercer, para que el problema dual sea convexo, es necesario que:

$$
a^TGa
=
\sum_{i,j}a_i a_j K(x_i,x_j)
\ge 0,
\qquad
\forall a\in\mathbb{R}^n.
$$

## Diapositiva 16. Operación en el Dual y Superficie de Decisión

La importancia de la matriz de Gram radica en que toda la información geométrica necesaria para encontrar el hiperplano óptimo en $\mathcal{H}$ está contenida en ella.

**Entrenamiento:** se resuelve:

$$
\max_\alpha
\sum_i \alpha_i
-
\frac{1}{2}\alpha^T(G\odot yy^T)\alpha,
$$

donde $\odot$ es el producto de Hadamard.

**Inferencia:** para un nuevo punto $x_u$, la función de decisión es:

$$
g(x_u)
=
\sum_{i\in S}\alpha_i y_i K(x_i,x_u)+b.
$$

**Conclusión:** la matriz de Gram actúa como un resumen métrico del conjunto de datos en el espacio transformado, permitiendo que la complejidad del modelo dependa del número de muestras $n$ y no de la dimensión del espacio mapeado.

## Diapositiva 17. Ejemplo: Kernel Polinomial

El kernel polinomial homogéneo de grado $p=2$ en $\mathbb{R}^2$ es el caso más simple de un mapeo no lineal.

Para:

$$
x=[x_1,x_2]^T,
\qquad
x'=[x'_1,x'_2]^T,
$$

definimos:

$$
K(x,x')=(x^Tx')^2.
$$

Luego:

$$
\begin{aligned}
K(x,x')
&=
(x_1x'_1+x_2x'_2)^2\\
&=
(x_1x'_1)^2
+2(x_1x'_1)(x_2x'_2)
+(x_2x'_2)^2.
\end{aligned}
$$

Reordenando los términos para identificar el producto escalar:

$$
K(x,x')
=
\begin{pmatrix}
x_1^2\\
\sqrt{2}x_1x_2\\
x_2^2
\end{pmatrix}^T
\begin{pmatrix}
(x'_1)^2\\
\sqrt{2}x'_1x'_2\\
(x'_2)^2
\end{pmatrix}.
$$

Resultado: el kernel proyecta datos de $\mathbb{R}^2$ a un espacio de características $\mathcal{H}$ en $\mathbb{R}^3$.

## Diapositiva 18. Kernel Polinomial: Visualización del Espacio de Características $\mathcal{H}$

Consideremos el problema de datos de una clase rodeados por otra, es decir, datos concéntricos.

- En $\mathbb{R}^2$, no existe ninguna línea recta $w_1x_1+w_2x_2+b=0$ que separe las clases.
- En $\mathcal{H}(\mathbb{R}^3)$, al proyectar mediante:

$$
\phi(x)=
\begin{pmatrix}
x_1^2\\
\sqrt{2}x_1x_2\\
x_2^2
\end{pmatrix},
$$

la frontera de decisión es un hiperplano:

$$
w_1x_1^2
+
w_2(\sqrt{2}x_1x_2)
+
w_3x_2^2
+
b
=0.
$$

Esta ecuación en $\mathbb{R}^3$ es la forma general de una sección cónica en $\mathbb{R}^2$. Un corte plano en el espacio de alta dimensión se traduce en una elipse, parábola o hipérbola en el espacio original.

## Diapositiva 19. Kernel de Base Radial (RBF)

El kernel más utilizado en la práctica es el gaussiano:

$$
K(x,x')
=
\exp\left(-\gamma\lVert x-x'\rVert^2\right)
=
\exp\left(
-
\frac{\lVert x-x'\rVert^2}{2\sigma^2}
\right).
$$

Naturaleza del espacio $\mathcal{H}$:

- $\gamma=\frac{1}{2\sigma^2}$ controla la curvatura de la frontera.
- A diferencia de los kernels polinomiales, el kernel RBF mapea los datos a un espacio de características $\phi(x)$ de dimensión infinita.
- Límite $\gamma\to\infty$: el modelo tiende al sobreajuste, memorizando puntos.
- Límite $\gamma\to 0$: el modelo se vuelve extremadamente rígido, con sesgo alto.
- Usando la expansión en serie de Taylor de la exponencial, se puede demostrar que $\phi(x)$ contiene todas las combinaciones polinomiales de grado infinito de las componentes de $x$.
- Interpretación geométrica: cada punto $x$ se proyecta a la superficie de una hiperesfera de radio unitario en $\mathcal{H}$, ya que $K(x,x)=\langle\phi(x),\phi(x)\rangle=1$.

## Diapositiva 20. Kernel RBF y el Rol de $\gamma$

El kernel gaussiano o RBF:

$$
K(x,x')=\exp\left(-\gamma\lVert x-x'\rVert^2\right).
$$

Interpretación:

- mide similitud local;
- puntos cercanos tienen kernel cercano a 1;
- puntos lejanos tienen kernel cercano a 0.

El parámetro $\gamma$ controla el alcance:

- $\gamma$ chico: fronteras suaves, vecindarios grandes;
- $\gamma$ grande: fronteras muy locales, alta flexibilidad e influencia local.

**Relación con Parzen y k-NN:** como en métodos locales, hay una escala espacial. En Parzen era el ancho de banda $h$; aquí es aproximadamente:

$$
\frac{1}{\sqrt{\gamma}}.
$$

## Diapositiva 21. El Kernel RBF: De $\mathbb{R}^d$ a un Hilbert de Dimensión Infinita

Para simplificar la exposición sin perder generalidad, sea:

$$
\gamma=\frac{1}{2\sigma^2}=1,
\qquad
x,x'\in\mathbb{R}.
$$

El kernel RBF se expresa como:

$$
K(x,x')
=
e^{-\frac{1}{2}(x-x')^2}
=
e^{-\frac{1}{2}x^2}
e^{-\frac{1}{2}(x')^2}
e^{xx'}.
$$

Aplicando la expansión en serie de Taylor:

$$
e^{xx'}
=
\sum_{n=0}^\infty
\frac{(xx')^n}{n!}
=
1+xx'
+
\frac{(xx')^2}{2!}
+
\frac{(xx')^3}{3!}
+
\cdots.
$$

Reordenando para que $K(x,x')=\langle\phi(x),\phi(x')\rangle$, obtenemos:

$$
K(x,x')
=
\sum_{n=0}^\infty
\left(
e^{-\frac{1}{2}x^2}
\frac{x^n}{\sqrt{n!}}
\right)
\left(
e^{-\frac{1}{2}(x')^2}
\frac{(x')^n}{\sqrt{n!}}
\right).
$$

El vector de características implícito es:

$$
\phi(x)
=
e^{-\frac{1}{2}x^2}
\begin{pmatrix}
1\\
x\\
\frac{x^2}{\sqrt{2!}}\\
\frac{x^3}{\sqrt{3!}}\\
\vdots\\
\frac{x^n}{\sqrt{n!}}\\
\vdots
\end{pmatrix}.
$$

El espacio $\mathcal{H}$ es un espacio de sucesiones $\ell^2$, cuya dimensión es infinitamente numerable.

## Diapositiva 22. Selección Conjunta de $C$ y $\gamma$

En SVM RBF, típicamente buscamos en una grilla:

$$
C\in\{10^{-2},10^{-1},\ldots,10^3\},
$$

$$
\gamma\in\{10^{-3},10^{-2},\ldots,10^2\}.
$$

Seleccionamos:

$$
(\hat C,\hat\gamma)
=
\arg\min_{C,\gamma}
\operatorname{CV}_K(C,\gamma).
$$

**Cuidado:** cuanto más grande la búsqueda, más importante es separar selección de evaluación final.

## Diapositiva 23. Consistencia Metodológica: SVM vs. Parzen

Notemos la similitud estructural entre SVM RBF y las ventanas de Parzen:

$$
p(x\mid \omega_i)
\approx
\frac{1}{n_i}
\sum_{j=1}^{n_i}
\frac{1}{h^d}
\varphi\left(
\frac{x-x_j}{h}
\right).
$$

Diferencia fundamental:

- Parzen usa todos los puntos de la clase y asigna pesos uniformes $1/n_i$.
- SVM selecciona solo los vectores de soporte y asigna pesos óptimos $\alpha_i$ para maximizar el margen de separación, no la verosimilitud local.

## Diapositiva 24. Radio y Margen

Si los datos están contenidos en una bola de radio $R$:

$$
\lVert x_i\rVert\le R,
$$

y el clasificador separa con margen $\gamma$, entonces la complejidad efectiva puede acotarse en términos de:

$$
\frac{R^2}{\gamma^2}.
$$

No solo importa la dimensión $d$, sino también la relación entre escala de los datos y margen de separación.

En escala canónica:

$$
\gamma=\frac{1}{\lVert w\rVert}.
$$

Entonces:

$$
\text{maximizar margen}
\quad\Longleftrightarrow\quad
\text{minimizar }\lVert w\rVert.
$$

Esto muestra que SVM también es un método regularizado:

$$
\frac{1}{2}\lVert w\rVert^2
+
C\sum_i \xi_i.
$$

Regularizar pesos y maximizar margen son dos caras de la misma geometría.

## Diapositiva 25. Geometría y Capacidad (VC Dimension)

Vapnik demostró que la capacidad de generalización está ligada a la relación entre el radio $R$ de la bola que contiene los datos y el margen $\gamma$.

**Cota de generalización:** con probabilidad $1-\delta$, el error de prueba $R(h)$ está acotado por:

$$
R(h)
\le
\hat R_{\text{emp}}(h)
+
\sqrt{
\frac{
h_{\text{VC}}\left(\ln(2n/h_{\text{VC}})+1\right)-\ln(\delta/4)
}{n}
}.
$$

En SVM, se puede demostrar que:

$$
h_{\text{VC}}
\le
\left\lceil
\frac{R^2}{\gamma^2}
\right\rceil
+1.
$$

Minimizar $\lVert w\rVert^2$ equivale a maximizar $\gamma$, lo que minimiza la capacidad de la familia de funciones y, por ende, el riesgo de sobreajuste.

## Diapositiva 26. Síntesis Conceptual

1. **Margen:** la geometría es clave para la generalización. Maximizar el margen equivale a minimizar la norma del vector de pesos.
2. **Dualidad:** permite pasar de un problema de $d$ dimensiones a uno de $n$ dimensiones, habilitando el uso de kernels.
3. **Kernels:** permiten trabajar en RKHS de dimensión arbitraria sin costo computacional explícito en el mapeo.
4. **$C$:** el parámetro de costo es el puente entre la optimización exacta y la realidad de datos ruidosos o solapados.

La regularización es una necesidad teórica para controlar la capacidad del modelo en espacios de alta dimensión.

| Método | Score | Pérdida | Control |
|---|---|---|---|
| Perceptrón | lineal | errores | parada/margen implícito |
| Logística | lineal | log-loss | $\lambda\lVert w\rVert^2$ |
| SSE | lineal | cuadrática | Ridge/Lasso |
| SVM | lineal/kernel | hinge | margen y $C$ |

Todos pueden verse como:

$$
\text{ajuste a datos}
+
\text{control de complejidad}.
$$

## Diapositiva 27. Evaluación y Fiabilidad del Clasificador

**Sección:** Evaluación y fiabilidad del clasificador.

## Diapositiva 28. Generalización: La Cantidad que Realmente Importa

Sea $h\in\mathcal{H}$ un clasificador y $(X,Y)\sim P$ un dato nuevo.

$$
R(h)=\mathbb{E}\left[L(Y,\varphi(X))\right]
$$

es el riesgo verdadero o error de generalización.

Como $P$ es desconocida, trabajamos con:

$$
\hat R_\mathcal{D}(h)
=
\frac{1}{n}\sum_{i=1}^n L(y_i,\varphi(x_i)).
$$

**Problema:** $\hat R_\mathcal{D}(h)$ es observable, pero $R(h)$ no.

## Diapositiva 29. Error de Entrenamiento vs. Error de Prueba

Distinguimos dos cantidades:

$$
\hat R_{\text{train}}(h)
\qquad
\text{y}
\qquad
\hat R_{\text{test}}(h).
$$

- $\hat R_{\text{train}}$: mide ajuste a los datos usados para aprender.
- $\hat R_{\text{test}}$: estima capacidad de generalización.

El *gap* de generalización es:

$$
\hat R_{\text{test}}(h)-\hat R_{\text{train}}(h).
$$

Si este gap es grande, sospechamos sobreajuste. En una práctica prolija separamos:

- **Train:** ajusta parámetros.
- **Validation:** elige hiperparámetros.
- **Test:** estima rendimiento final.

Resumen:

$$
\text{Train}\to\hat\theta,
\qquad
\text{Validation}\to\hat\lambda,
\qquad
\text{Test}\to\text{reporte final}.
$$

**Recordar:** el test no participa en ninguna decisión de modelado.

## Diapositiva 30. Validación Cruzada

Cuando la muestra es limitada, usamos validación cruzada:

$$
\operatorname{CV}_K(\lambda)
=
\frac{1}{K}
\sum_{k=1}^K
\hat R_k(\lambda).
$$

Elegimos:

$$
\hat\lambda
=
\arg\min_{\lambda\in\Lambda}
\operatorname{CV}_K(\lambda).
$$

La validación cruzada:

- reduce la dependencia de una única partición;
- es esencial al comparar SVM, logística, k-NN, etc.;
- sigue siendo una estimación, no una verdad absoluta.

## Diapositiva 31. ¿Un Margen Grande es Estadísticamente Significativo?

No medimos directamente la significancia del margen $1/\lVert w\rVert$.

Lo que sí evaluamos es:

- estabilidad del rendimiento en validación cruzada;
- dispersión de métricas entre folds;
- diferencia frente a baselines simples;
- sensibilidad a cambios de umbral o priors.

**Lectura correcta:** un margen grande es una señal geométrica útil, pero la evidencia práctica viene del rendimiento fuera de muestra.

## Diapositiva 32. Matriz de Confusión

Para clasificación binaria:

$$
\begin{matrix}
& \hat\omega_1 & \hat\omega_2\\
\omega_1 & TP & FN\\
\omega_2 & FP & TN
\end{matrix}
$$

- $TP$: verdaderos positivos.
- $FN$: falsos negativos.
- $FP$: falsos positivos.
- $TN$: verdaderos negativos.

## Diapositiva 33. Sensibilidad y Especificidad

Algunas tasas básicas:

$$
\operatorname{Recall}
=
TPR
=
\frac{TP}{TP+FN},
\qquad
TNR
=
\frac{TN}{TN+FP}.
$$

- **Sensibilidad / Recall:** proporción de positivos detectados.
- **Recall:** de los positivos reales, ¿cuántos encontré?
- **Especificidad:** proporción de negativos correctamente descartados.

Además:

$$
FPR
=
1-TNR
=
\frac{FP}{FP+TN}.
$$

## Diapositiva 34. Precisión y F1

La precisión responde otra pregunta: de lo que marqué como positivo, ¿cuánto era correcto?

$$
\operatorname{Precision}
=
\frac{TP}{TP+FP}.
$$

La media armónica:

$$
F_1
=
2
\frac{
\operatorname{Precision}\cdot\operatorname{Recall}
}{
\operatorname{Precision}+\operatorname{Recall}
}.
$$

Es útil cuando queremos balancear omisiones y falsas alarmas.

## Diapositiva 35. Curvas ROC, PR y DET

Cuando un clasificador produce un score $s(x)$, podemos variar el umbral $t$ y estudiar el desempeño resultante:

$$
\hat\omega_t(x)
=
\begin{cases}
\omega_1 & \text{si } s(x)\ge t,\\
\omega_2 & \text{si } s(x)<t.
\end{cases}
$$

- **ROC (Receiver Operating Characteristic):** grafica $TPR(t)$ contra $FPR(t)$.
- **PR (Precision-Recall):** grafica $\operatorname{Precision}(t)$ contra $\operatorname{Recall}(t)$.
- **DET (Detection Error Tradeoff):** representa falsa alarma y falsos negativos en una escala útil para sistemas de detección.

Un clasificador lineal o SVM no se agota en su frontera por defecto; también debe estudiarse como familia de decisiones indexadas por un umbral.

## Diapositiva 36. Cuidado: ROC Puede Verse Optimista con Desbalance

La ROC usa $FPR$, que normaliza por el número total de negativos:

$$
FPR
=
\frac{FP}{FP+TN}.
$$

Si la clase negativa es enorme, muchos falsos positivos pueden seguir dando un $FPR$ pequeño.

En problemas raros, una ROC buena puede coexistir con una precisión muy baja.

## Diapositiva 37. ROC vs. PR

La curva PR grafica:

$$
(\operatorname{Recall}(t),\operatorname{Precision}(t)).
$$

Ventajas:

- enfatiza el comportamiento sobre la clase positiva;
- es más sensible al costo de falsos positivos bajo desbalance;
- resulta especialmente útil en detección de eventos raros.

Comparación conceptual:

- **ROC:** responde cómo balancear detección y falsa alarma.
- **PR:** responde qué pureza tienen los positivos predichos. Es esencial en desbalance, porque se enfoca en la capacidad del modelo de hallar la clase rara sin generar falsas alarmas masivas.

**Regla práctica:** si la clase positiva es rara y relevante, mirar PR-AUC además de ROC-AUC.

## Diapositiva 38. ROC y Precision-Recall en Código

```python
from sklearn.metrics import roc_curve, precision_recall_curve
from sklearn.metrics import roc_auc_score, average_precision_score

scores = clf.predict_proba(X_test)[:, 1]

fpr, tpr, thr_roc = roc_curve(y_test, scores)
prec, rec, thr_pr = precision_recall_curve(y_test, scores)

auc_roc = roc_auc_score(y_test, scores)
ap = average_precision_score(y_test, scores)
```

## Diapositiva 39. La Métrica Depende del Problema

Ejemplos:

- **Diagnóstico médico:** recall alto para no omitir casos.
- **Filtro de spam:** precision alta para no bloquear correos legítimos.
- **Fraude:** PR-AUC suele ser más informativa que accuracy.
- **Admisión de crédito:** importa integrar métricas y costos.

**Principio:** no existe una métrica universalmente correcta; la elección depende de la tarea, del costo de error y del desbalance.

## Diapositiva 40. Evaluación: Más Allá de la Tasa de Error

En problemas de clasificación multiclase con $c$ categorías, la tasa de acierto $P(C)$ puede ser engañosa si las probabilidades a priori $P(\omega_i)$ están desbalanceadas.

- Sea $C$ la matriz de confusión de tamaño $c\times c$.
- Un clasificador aleatorio que simplemente lanza dados siguiendo la distribución marginal de las predicciones tendrá un acierto no nulo.
- **Objetivo:** normalizar el desempeño del clasificador restando el efecto del acuerdo por azar.

Pregunta central: ¿qué proporción del éxito es azarosa?

Corregimos el acuerdo observado $p_o$. Cuando una clase es dominante, el *accuracy* miente; necesitamos una métrica que revele la verdadera calidad de la clasificación.

## Diapositiva 41. El Índice Kappa (Cohen, 1960): Definición

El estadístico $\kappa$ se define como la proporción del acuerdo observado que excede al acuerdo esperado por azar, normalizado por el máximo acuerdo posible sobre el azar.

**Definición formal:**

$$
\kappa
=
\frac{p_o-p_e}{1-p_e}.
$$

Donde:

- $p_o$: probabilidad de acuerdo observado (*observed agreement*).
- $p_e$: probabilidad de acuerdo esperado por azar (*expected agreement*).

Queremos una medida de concordancia corregida:

$$
\text{concordancia útil}
=
\frac{
\text{acuerdo observado}-\text{acuerdo azar}
}{
\text{máximo acuerdo posible}-\text{acuerdo azar}
}.
$$

**Lectura:** Kappa mide qué fracción del acuerdo no trivial fue efectivamente alcanzada.

## Diapositiva 42. Derivación a Partir de la Matriz de Confusión

Sea $n$ el número total de muestras y $n_{ij}$ el elemento de la matriz de confusión, es decir, muestras de la clase $\omega_i$ clasificadas como $\omega_j$.

**Acuerdo observado $p_o$:** es la traza de la matriz normalizada.

$$
p_o
=
\frac{1}{n}
\sum_{i=1}^c n_{ii}.
$$

**Acuerdo por azar $p_e$:** bajo independencia entre el clasificador y la etiqueta real, la probabilidad de que ambos coincidan en la clase $i$ es el producto de sus marginales.

$$
p_e
=
\sum_{i=1}^c
\left(
\frac{n_{i\cdot}}{n}
\cdot
\frac{n_{\cdot i}}{n}
\right)
=
\frac{1}{n^2}
\sum_{i=1}^c
(n_{i\cdot}n_{\cdot i}).
$$

Donde $n_{i\cdot}$ es el total de la fila $i$, es decir, *ground truth*, y $n_{\cdot i}$ es el total de la columna $i$, es decir, predicciones.

## Diapositiva 43. Análisis del Rango de $\kappa$

El índice $\kappa$ típicamente oscila en el intervalo $[-1,1]$, aunque en la práctica interesan más los valores positivos:

- $\kappa=1$: acuerdo perfecto entre el modelo y la realidad.
- $\kappa=0$: el clasificador no es mejor que una asignación aleatoria basada en las frecuencias marginales.
- $\kappa<0$: el acuerdo es peor que el azar, lo que indica una contradicción sistemática o un fallo estructural en el modelo.

**Nota sobre desbalance:** a diferencia del *accuracy*, $\kappa$ penaliza fuertemente si el modelo solo acierta la clase mayoritaria, ya que en ese caso $p_e$ será muy alto y reducirá el numerador.

## Diapositiva 44. Índice Kappa

La diapositiva ilustra el cálculo de Kappa con una matriz de confusión desbalanceada, mostrando que la exactitud puede ser alta mientras que la ganancia real corregida por azar es mucho menor.

![Panel ilustrativo del índice Kappa](figures/clase-11/fig-44-kappa-dashboard.png)

## Diapositiva 45. Kappa y la Regla de Decisión de Bayes

El índice $\kappa$ puede verse como una medida de cuán cerca está nuestra función de decisión $\phi(x)$ del límite de Bayes, corregida por la entropía de la distribución a priori.

- Si las clases son equiprobables, $P(\omega_i)=1/c$, y las predicciones también, entonces:

$$
p_e=\frac{1}{c}.
$$

- En este caso, $\kappa$ es una transformación lineal del *accuracy*.
- Sin embargo, cuando $P(\omega_i)$ es altamente informativa, es decir, cuando hay desbalance, $\kappa$ evalúa si el clasificador aprendió la densidad condicional de clase $p(x\mid\omega_i)$ o si simplemente explota la probabilidad a priori $P(\omega_i)$.

## Diapositiva 46. Propiedades de Kappa

Kappa:

- penaliza soluciones que aciertan solo por seguir la clase mayoritaria;
- puede bajar mucho en problemas muy desbalanceados;
- es simétrica respecto de los dos anotadores o, en nuestro caso, verdad y predicción;
- no reemplaza a precision y recall: las complementa.

Un *accuracy* alto no implica un $\kappa$ alto.

## Diapositiva 47. Ejemplo Rápido de Kappa

Supongamos 100 observaciones:

- 90 son de $\omega_2$ y 10 de $\omega_1$;
- el clasificador predice siempre $\omega_2$.

Entonces:

$$
p_o=0.90.
$$

Pero también:

$$
p_e=0.9\cdot 1+0.1\cdot 0=0.9.
$$

Por tanto:

$$
\kappa
=
\frac{0.90-0.9}{1-0.9}
=0.
$$

El acuerdo real es mucho menos impresionante de lo que sugiere el *accuracy*.

## Diapositiva 48. Kappa con `cohen_kappa_score`

```python
from sklearn.metrics import cohen_kappa_score

kappa = cohen_kappa_score(y_test, y_pred)
print(f"Kappa = {kappa:.3f}")
```

**Interpretación:** útil para comparar modelos cuando *accuracy* es poco informativa por azar o desbalance.
