---
title: "Regularización y SVM"
---

## Diapositiva 1

**Portada**

- Ciencia de Datos
- Clase 10 - Regularización y SVM
- FaMAF
- Ciencias de datos 2026

## Diapositiva 2. Del Rigor en la Ciencia

La diapositiva presenta el texto **Del Rigor en la Ciencia**, atribuido a Jorge Luis Borges:

> En aquel Imperio, el arte de la cartografía logró tal perfección que el mapa de una sola provincia ocupaba toda una ciudad, y el mapa del imperio, toda una provincia. Con el tiempo, estos mapas desmesurados no satisficieron y los colegios de cartógrafos levantaron un mapa del imperio, que tenía el tamaño del imperio y coincidía puntualmente con él.

> Menos adictas al estudio de la cartografía, las generaciones siguientes entendieron que ese dilatado mapa era inútil y no sin impiedad lo entregaron a las inclemencias del sol y los inviernos. En los desiertos del oeste perduran despedazadas ruinas del mapa, habitadas por animales y por mendigos; en todo el país no hay otra reliquia de las disciplinas geográficas.

Suárez Miranda, *Viajes de Varones Prudentes*, Libro Cuarto, Cap. XLV, Lérida, 1658.

**FIN**

## Diapositiva 3. Clasificador Lineal y Riesgo

**Sección:** Clasificador lineal y riesgo.

## Diapositiva 4. Formalización: Riesgo y Función de Pérdida

Sea $x\in\mathcal{X}$ un patrón y $y\in\mathcal{Y}$ su etiqueta verdadera. Sea $f(x;\theta)$ nuestro clasificador parametrizado por $\theta$.

Definimos una función de pérdida:

$$
L(y,f(x;\theta)).
$$

En las primeras clases, esta pérdida aparecía como:

$$
L=\lambda(a_i\mid \omega_j).
$$

Para clasificación, comúnmente usamos la pérdida 0-1:

$$
L(y,\hat y)
=
\begin{cases}
0 & \text{si } y=\hat y,\\
1 & \text{si } y\ne \hat y.
\end{cases}
$$

Suponemos que los datos $(x,y)$ provienen de una distribución conjunta desconocida $P(x,y)$.

El riesgo verdadero de un clasificador es:

$$
R(f)=\mathbb{E}_{(x,y)\sim P}\left[L(y,f(x;\theta))\right].
$$

## Diapositiva 5. Función de Pérdida Cuadrática para Clasificación

Ya conocemos mínimos cuadrados. Entonces:

> Si podemos resolver regresión lineal con una fórmula cerrada, ¿por qué no usar mínimos cuadrados para clasificar?

Codificamos clases binarias como $y_i\in\{-1,+1\}$. Ajustamos un score lineal:

$$
f_w(x)=w^Tx+b,
$$

y decidimos:

$$
\hat y=\operatorname{sign}(f_w(x)).
$$

Pero cuadrados mínimos puede fallar en clasificación, porque la pérdida cuadrática penaliza magnitudes:

$$
(y_i-f_w(x_i))^2,
$$

mientras que para clasificar solo importa el signo:

$$
y_i f_w(x_i)>0.
$$

Consecuencias:

- puntos bien clasificados pero alejados pueden dominar el ajuste;
- outliers arrastran la frontera;
- el score no está naturalmente acotado entre 0 y 1;
- minimizar distancia a etiquetas no equivale a minimizar error de decisión.

## Diapositiva 6. La Patología de los Mínimos Cuadrados (LMS)

**Problema: métrica inadecuada**

La pérdida cuadrática:

$$
(y_i-w^Tx_i)^2
$$

no busca separar clases, sino ajustar valores.

- **Sensibilidad a la "Corrección Extrema":** un punto correctamente clasificado pero muy alejado de la frontera genera un error cuadrático grande. LMS mueve la frontera para acercarse a él, arruinando la clasificación de puntos cercanos.
- **Inestabilidad numérica:** si las variables están correlacionadas, $X^TX$ es mal condicionada y $\lVert w\rVert$ explota.

Conclusión: LMS es un ajustador de etiquetas, no un separador de regiones.

![Comparación de robustez entre LMS y regresión logística](figures/clase-10/fig-06-lms-vs-logistic.png)

## Diapositiva 7. Hoja de Ruta de la Clase

La clase se organiza en tres bloques:

1. **Clasificador lineal y riesgo**
   - Riesgo empírico regularizado
   - Regresión logística y mínimos cuadrados
2. **SVM y optimización**
   - Margen geométrico y problema primal
   - Dualidad de Lagrange y condiciones KKT
   - SVM de margen blando
3. **Capacidad, generalización y evaluación**
   - Selección de modelos y complejidad

## Diapositiva 8. ¿Dónde Estamos en la Materia?

- Vimos que perceptrón, regresión logística y SVM pueden leerse como minimización de distintas funciones de pérdida.
- Aprendimos que el error de entrenamiento no alcanza para estimar generalización.
- Hoy estudiamos mecanismos matemáticos para controlar complejidad.

Pregunta:

> Si una frontera ajusta demasiado o demasiado poco, ¿qué elemento matemático estamos moviendo?

## Diapositiva 9. Capacidad de Modelos

La diapositiva ilustra el concepto de capacidad con curvas de distinta complejidad ajustando el mismo patrón.

![Curvas de distinta capacidad ajustando los datos](figures/clase-10/fig-09-model-capacity.png)

## Diapositiva 10. Capacidad de Modelos

La medida más estándar de capacidad para clasificadores binarios es la **dimensión de Vapnik-Chervonenkis**, o **dimensión VC**.

Se define como el número máximo de puntos $n$ que pueden ser fragmentados por la familia de funciones $\mathcal{H}$.

Decimos que un conjunto de puntos es fragmentado si, para cualquier asignación de etiquetas posibles, es decir, para las $2^n$ combinaciones, existe una función en $\mathcal{H}$ que los clasifica perfectamente.

Ejemplo: en $\mathbb{R}^2$, la capacidad de los hiperplanos, o líneas, es 3. Pueden clasificar cualquier combinación de 3 puntos, pero fallan con 4, como en el problema de XOR.

Generalizar requiere controlar capacidad, no solo minimizar el error observado. La capacidad es el nivel de detalle:

- **Baja capacidad:** un modelo demasiado simple, por ejemplo una constante. Tiene sesgo alto porque no puede representar la complejidad de los datos.
- **Alta capacidad:** un modelo extremadamente flexible, por ejemplo SVM con kernel RBF y $\gamma$ muy alto. Puede representar cualquier detalle de la muestra, pero corre el riesgo de fragmentar incluso el ruido aleatorio.

Riesgo: si la capacidad es infinita, el error de entrenamiento será cero, pero la discrepancia entre el error de entrenamiento y el error real será máxima.

## Diapositiva 11. Procedimiento de Validación Cruzada y Complejidad

**Contexto:** dado que la distribución $p(x,y)$ es desconocida, no podemos calcular el riesgo real $R(f)$. El riesgo empírico $\hat R_{\text{train}}$ es un estimador sesgado hacia la baja debido al sobreajuste. La validación cruzada actúa como un proxy del riesgo de generalización.

Sea:

$$
\mathcal{D}=\{(x_1,y_1),\ldots,(x_n,y_n)\}
$$

el conjunto de datos, y sea:

$$
\Lambda=\{\lambda_1,\ldots,\lambda_m\}
$$

el espacio de búsqueda de la complejidad.

Procedimiento:

1. **Partición estocástica:** se divide $\mathcal{D}$ en $K$ subconjuntos disjuntos $\{\mathcal{D}_1,\ldots,\mathcal{D}_K\}$ de tamaño $n/K$.
2. **Ciclo de evaluación para cada $\lambda\in\Lambda$:**
   Para cada fold $k\in\{1,\ldots,K\}$, se define $\mathcal{T}_k=\mathcal{D}\setminus \mathcal{D}_k$, se halla el parámetro óptimo $\hat\theta_{k,\lambda}$ minimizando el costo sobre $\mathcal{T}_k$, y se calcula el error sobre el conjunto de validación:

$$
E_k(\lambda)
=
\frac{1}{|\mathcal{D}_k|}
\sum_{(x_i,y_i)\in\mathcal{D}_k}
L\left(y_i,f(x_i;\hat\theta_{k,\lambda})\right).
$$

El estimador de riesgo promedia los $K$ experimentos:

$$
\operatorname{CV}(\lambda)
=
\frac{1}{K}\sum_{k=1}^K E_k(\lambda).
$$

3. **Selección óptima:**

$$
\lambda^\ast=\arg\min_{\lambda\in\Lambda}\operatorname{CV}(\lambda).
$$

## Diapositiva 12. Selector de Complejidad

Elegimos hiperparámetros con validación cruzada:

$$
\hat\lambda=\arg\min_{\lambda\in\Lambda}\operatorname{CV}_K(\lambda).
$$

Pero queda una pregunta más estructural:

$$
\text{¿qué representa realmente }\lambda\text{?}
$$

**Idea:** en muchos modelos, $\lambda$ controla cuánto permitimos que la solución se adapte a detalles de la muestra.

## Diapositiva 13. El Problema de Fondo

Queremos elegir un clasificador:

$$
f:\mathcal{X}\to\mathcal{Y}
$$

con bajo riesgo verdadero:

$$
R(f)=\mathbb{E}_{(x,y)\sim P}\left[L(y,f(x;\theta))\right].
$$

Como $P(x,y)$ es desconocida, minimizamos una cantidad empírica:

$$
\hat R_\mathcal{D}(f)
=
\frac{1}{n}\sum_{i=1}^n L(y_i,f(x_i;\theta)).
$$

Si la familia de clasificadores es muy grande, minimizar $\hat R_\mathcal{D}$ puede producir un modelo demasiado sensible a $\mathcal{D}$, es decir, sobreajuste.

La minimización:

$$
\min_f \hat R_\mathcal{D}(f)
$$

no controla por sí sola la complejidad de $f$.

## Diapositiva 14. Riesgo Empírico Regularizado

La respuesta clásica es penalizar complejidad:

$$
\hat h
\in
\arg\min_{h\in\mathcal{H}}
\left\{
\frac{1}{n}\sum_{i=1}^n L(y_i,f(x_i;\theta))
+
\lambda\Omega(h)
\right\}.
$$

Interpretación:

- $L$ mide ajuste a los datos.
- $\Omega(h)$ mide complejidad.
- $\lambda\ge 0$ controla el compromiso.

**Lectura:** no buscamos el modelo que comete menos errores en entrenamiento, sino el más simple entre los que explican razonablemente los datos.

## Diapositiva 15. Modelo Lineal

Consideremos:

$$
f_w(x)=w^Tx+b.
$$

Para simplificar, usamos vectores aumentados:

$$
\tilde x=(1,x_1,\ldots,x_d)^T,
\qquad
\tilde w=(b,w_1,\ldots,w_d)^T.
$$

Entonces:

$$
f_{\tilde w}(x)=\tilde w^T\tilde x.
$$

En modelos lineales, la complejidad suele medirse con normas de $w$:

$$
\lVert w\rVert_2^2,
\qquad
\lVert w\rVert_1,
\qquad
\text{o combinaciones}.
$$

## Diapositiva 16. Por Qué Penalizar Pesos Grandes

Si:

$$
f_w(x)=w^Tx+b,
$$

entonces, para dos puntos cercanos:

$$
\left|f_w(x)-f_w(x')\right|
=
\left|w^T(x-x')\right|
\le
\lVert w\rVert_2\lVert x-x'\rVert_2.
$$

La norma $\lVert w\rVert_2$ controla cuán rápido puede cambiar el score.

**Consecuencia:** pesos grandes permiten fronteras muy sensibles a pequeñas variaciones de los datos. Penalizarlos favorece estabilidad.

## Diapositiva 17. Regularización L2

La penalización Ridge o L2 usa:

$$
\Omega(w)=\lVert w\rVert_2^2=\sum_{j=1}^d w_j^2.
$$

El problema general es:

$$
\min_w
\left\{
\frac{1}{n}\sum_{i=1}^n L(y_i,w^Tx_i+b)
+
\lambda\lVert w\rVert_2^2
\right\}.
$$

Propiedades:

- castiga fuertemente pesos grandes;
- produce soluciones estables cuando hay colinealidad;
- generalmente no hace coeficientes exactamente cero.

## Diapositiva 18. Geometría L2

La diapositiva muestra la geometría de la regularización L2: las curvas de nivel de la pérdida se intersectan con una región factible redondeada.

![Geometría de regularización L2](figures/clase-10/fig-18-l2-geometry.png)

## Diapositiva 19. Regularización L1

La penalización Lasso o L1 usa:

$$
\Omega(w)=\lVert w\rVert_1=\sum_{j=1}^d |w_j|.
$$

El problema general es:

$$
\min_w
\left\{
\frac{1}{n}\sum_{i=1}^n L(y_i,w^Tx_i+b)
+
\lambda\lVert w\rVert_1
\right\}.
$$

Propiedades:

- induce soluciones *sparse*;
- hace selección implícita de variables;
- puede ser inestable con variables muy correlacionadas.

## Diapositiva 20. Geometría L1 vs. L2

La diapositiva compara la región factible de la penalización L1, con esquinas sobre los ejes, contra la región L2, redondeada.

![Comparación geométrica entre regularización L1 y L2](figures/clase-10/fig-20-l1-l2-geometry.png)

## Diapositiva 21. Geometría L1 vs. L2

La forma restringida muestra la diferencia:

$$
\min_w \hat R_\mathcal{D}(w)
\quad
\text{sujeto a}
\quad
\lVert w\rVert_q\le c.
$$

Para $q=2$, la región factible es redondeada. Para $q=1$, la región tiene esquinas sobre los ejes.

**Intuición:** si el óptimo toca la región factible L1 o L2, algunos coeficientes quedan exactamente en cero.

Penalizar $\lVert w\rVert$ solo tiene sentido si las variables están en escalas comparables. Si una variable se mide en metros y otra en milímetros, sus coeficientes cambian de escala aunque la información sea la misma:

$$
x'_j=cx_j
\quad\Longrightarrow\quad
w'_j=\frac{w_j}{c}.
$$

**Cuidado:** estandarizar variables debe hacerse dentro de cada fold de validación, no antes de dividir los datos.

## Diapositiva 22. Ejemplo: Regresión Logística

Para clasificación binaria:

$$
P(Y=1\mid x;w,b)=\sigma(w^Tx+b),
\qquad
\sigma(z)=\frac{1}{1+e^{-z}}.
$$

La pérdida de entropía cruzada es:

$$
J(w,b)
=
-
\sum_{i=1}^n
\left[
y_i\log p_i+(1-y_i)\log(1-p_i)
\right],
\qquad
p_i=\sigma(w^Tx_i+b).
$$

La versión regularizada es:

$$
J_\lambda(w,b)
=
-
\sum_{i=1}^n
\left[
y_i\log p_i+(1-y_i)\log(1-p_i)
\right]
+
\frac{\lambda}{2}\lVert w\rVert_2^2.
$$

Su gradiente respecto de $w$:

$$
\nabla_w J_\lambda
=
\sum_{i=1}^n (p_i-y_i)x_i+\lambda w.
$$

La regularización agrega una fuerza hacia el origen:

$$
w_{t+1}
=
w_t
-
\eta
\left[
\sum_i (p_i-y_i)x_i+\lambda w_t
\right].
$$

## Diapositiva 23. La Patología de los Mínimos Cuadrados (LMS)

Si codificamos $y_i\in\{-1,+1\}$, el estimador lineal óptimo en sentido cuadrático es:

$$
w=X^\dagger y.
$$

Pregunta: ¿es suficiente para clasificar?

El problema es la métrica inadecuada. La pérdida cuadrática:

$$
(y_i-w^Tx_i)^2
$$

no busca separar clases, sino ajustar valores.

- **Sensibilidad a la corrección extrema:** un punto correctamente clasificado pero muy alejado de la frontera genera un error cuadrático grande. LMS mueve la frontera para acercarse a él, arruinando la clasificación de puntos cercanos.
- **Inestabilidad numérica:** si las variables están correlacionadas, $X^TX$ es mal condicionada y $\lVert w\rVert$ explota.

Conclusión: LMS es un ajustador de etiquetas, no un separador de regiones.

## Diapositiva 24. Hacia una Teoría de Decisión Más Robusta

Hasta ahora vimos la regularización como un método general para evitar que los pesos exploten.

En SVM, la regularización se interpreta como maximizar el margen geométrico, es decir, la distancia mínima entre los datos y la frontera de decisión. La vimos como un algoritmo para una pérdida particular.

Ahora veremos que SVM tiene una teoría fuerte que justifica su capacidad de generalización, en donde la regularización es un elemento fundamental que define la geometría del modelo.

## Diapositiva 25. SVM y Optimización

**Sección:** SVM y optimización.

## Diapositiva 26. El Paradigma del Riesgo Empírico Regularizado

Todo aprendizaje supervisado busca equilibrar la fidelidad a los datos con la simplicidad del modelo para garantizar generalización.

**Funcional de costo general:**

$$
J(w,w_0,\lambda)
=
\sum_{i=1}^n L(y_i,f(x_i))
+
\lambda\Omega(w).
\tag{1}
$$

Donde:

- $L$ es una función de pérdida, por ejemplo cuadrática, logística o hinge.
- $\Omega(w)=\frac{1}{2}\lVert w\rVert^2$ es la penalización de Tikhonov, L2.
- $\lambda$ es el parámetro de regularización que controla el *trade-off* entre sesgo y varianza.

Regularizar es imponer un presupuesto de complejidad a los pesos para evitar que el modelo sea una réplica exacta del ruido.

## Diapositiva 27. Muchas Fronteras Separan

Si los datos son linealmente separables, existen muchos hiperplanos:

$$
H=\{x:w^Tx+b=0\}.
$$

Todos pueden tener error de entrenamiento cero, por lo que el error empírico no decide entre ellos:

$$
\hat R_\mathcal{D}(h_1)=\hat R_\mathcal{D}(h_2)=0.
$$

Entre todas las fronteras que separan, ¿cuál es más robusta?

En modelos lineales, la distancia de un punto $x$ al hiperplano $g(x)=w^Tx+w_0=0$ es:

$$
r=\frac{|g(x)|}{\lVert w\rVert}.
$$

En efecto, la distancia euclídea de $x$ a $H$ es:

$$
d(x,H)=\frac{|w^Tx+b|}{\lVert w\rVert_2}.
$$

Si $y_i\in\{-1,+1\}$ y el punto está bien clasificado:

$$
y_i(w^Tx_i+b)>0.
$$

La distancia entonces es:

$$
\frac{y_i(w^Tx_i+b)}{\lVert w\rVert_2}.
$$

## Diapositiva 28. Margen Geométrico

El margen geométrico de un hiperplano sobre la muestra es:

$$
\gamma(w,b)
=
\min_{i=1,\ldots,n}
\frac{y_i(w^Tx_i+b)}{\lVert w\rVert_2}.
$$

Buscamos maximizar:

$$
\max_{w,b}\gamma(w,b).
$$

- El margen mide la distancia mínima entre los datos y la frontera.
- Un margen grande implica que la frontera es robusta a pequeñas perturbaciones.
- Maximizar el margen es una estrategia para elegir la mejor frontera entre las que separan.

Si multiplicamos $(w,b)$ por $c>0$, la frontera no cambia:

$$
\operatorname{sign}\left(c(w^Tx+b)\right)
=
\operatorname{sign}(w^Tx+b).
$$

Por eso debemos fijar una escala.

![Margen geométrico de un hiperplano](figures/clase-10/fig-28-geometric-margin.png)

## Diapositiva 29. Escala Canónica

Podemos elegir la escala de modo que el punto más cercano satisfaga:

$$
\min_i y_i(w^Tx_i+b)=1.
$$

Entonces las restricciones son:

$$
y_i(w^Tx_i+b)\ge 1,
\qquad
i=1,\ldots,n.
$$

Bajo esta escala, el margen geométrico es:

$$
\gamma=\frac{1}{\lVert w\rVert_2}.
$$

La distancia entre los dos hiperplanos, o líneas de trazos:

$$
w^Tx+b=1,
\qquad
w^Tx+b=-1,
$$

es:

$$
\frac{2}{\lVert w\rVert_2}.
$$

## Diapositiva 30. Margen Duro

Maximizar margen equivale a minimizar la norma de $w$:

$$
\min_{w,b}\frac{1}{2}\lVert w\rVert_2^2
$$

sujeto a:

$$
y_i(w^Tx_i+b)\ge 1,
\qquad
i=1,\ldots,n.
$$

**Lectura:** no buscamos cualquier separador. Buscamos el separador con mayor distancia mínima a los datos.

El margen es:

$$
\frac{2}{\lVert w\rVert}.
$$

Maximizarlo equivale a minimizar $\lVert w\rVert$.

Como $\lVert w\rVert$ y $\frac{1}{2}\lVert w\rVert^2$ tienen el mismo minimizador, y la segunda función es diferenciable y convexa, usamos:

$$
\frac{1}{2}\lVert w\rVert^2.
$$

El problema resultante es de optimización cuadrática convexa con restricciones lineales.

## Diapositiva 31. De la Norma L2 al Margen Geométrico

- **Normalización canónica:** escalamos $(w,w_0)$ tal que para los puntos más cercanos, los bordes de la banda, $|g(x)|=1$.
- **El margen:** la distancia total entre las clases es:

$$
M=\frac{2}{\lVert w\rVert}.
$$

Maximizar el margen $M$ es equivalente a minimizar la norma $\lVert w\rVert$. Por lo tanto, en SVM, la regularización es la geometría del pasillo de seguridad.

Entonces buscamos el hiperplano con menor complejidad que clasifique correctamente todas las muestras.

**Optimización primal, margen duro:**

$$
\min_{w,w_0}\frac{1}{2}\lVert w\rVert^2
\quad
\text{sujeto a}
\quad
y_i(w^Tx_i+w_0)\ge 1,
\qquad
\forall i=1,\ldots,n.
$$

Propiedades:

- es un problema de programación cuadrática en el espacio de parámetros;
- su complejidad computacional depende de la dimensión $d$ del vector $w$;
- recorrer todos los puntos para encontrar el margen es ineficiente.

## Diapositiva 32. Hacia una Estructura Superior: La Dualidad

Vamos a abandonar el espacio de los pesos $w$ y buscar una solución alternativa.

- **Limitación dimensional:** en el primal, si $d\gg n$, la optimización es ineficiente.
- **No linealidad:** no es evidente cómo proyectar datos a espacios de mayor dimensión $\phi(x)$ sin colapsar computacionalmente.

**La propuesta de Lagrange:** transformar el problema de minimización con restricciones en un problema de búsqueda de un punto de silla (*saddle point*), donde las restricciones se incorporan al funcional. Esto permite pasar del espacio de pesos al espacio de las muestras.

## Diapositiva 33. Vectores de Soporte

Las restricciones activas satisfacen:

$$
y_i(w^Tx_i+b)=1.
$$

Esos puntos están sobre los márgenes:

$$
w^Tx+b=1
\qquad
\text{o}
\qquad
w^Tx+b=-1.
$$

**Definición:** los puntos que tocan el margen son los vectores de soporte.

Si movemos puntos lejos del margen, la solución no cambia. Si movemos un vector de soporte, la frontera puede cambiar.

## Diapositiva 34. Vectores de Soporte

Solo los vectores de soporte definen la frontera de decisión. El resto de los puntos no afecta la solución.

![Vectores de soporte sobre los márgenes](figures/clase-10/fig-34-support-vectors.png)

## Diapositiva 35. Lagrangiano

Para el problema primal:

$$
\min_{w,b}\frac{1}{2}\lVert w\rVert^2
\quad
\text{sujeto a}
\quad
1-y_i(w^Tx_i+b)\le 0,
$$

introducimos multiplicadores:

$$
\alpha_i\ge 0.
$$

Para resolver el problema primal con restricciones de desigualdad, definimos el Lagrangiano $L$ como la suma de la función objetivo y las restricciones ponderadas por multiplicadores $\alpha_i\ge 0$:

$$
L(w,b,\alpha)
=
\frac{1}{2}\lVert w\rVert^2
-
\sum_{i=1}^n
\alpha_i
\left[
y_i(w^Tx_i+w_0)-1
\right].
$$

## Diapositiva 36. Reformulación: El Funcional Lagrangiano

**Definición del Lagrangiano:**

$$
L(w,w_0,\alpha)
=
\frac{1}{2}\lVert w\rVert^2
-
\sum_{i=1}^n
\alpha_i
\left[
y_i(w^Tx_i+w_0)-1
\right].
\tag{2}
$$

Anatomía de la penalización:

- si un punto pasa el margen, $y_i g(x_i)<1$, el término entre corchetes es negativo. El signo menos externo hace que el valor de $L$ aumente;
- si el punto cumple holgadamente, $y_i g(x_i)>1$, el término es positivo. Para minimizar $L$, el optimizador tenderá a hacer $\alpha_i=0$.

## Diapositiva 37. Geometría L2

La diapositiva vuelve a mostrar la geometría L2 como conexión entre regularización, restricciones y solución geométrica.

![Geometría L2 en el contexto del margen](figures/clase-10/fig-37-l2-geometry.png)

## Diapositiva 38. Comparativa Analítica: Problema Primal vs. Problema Dual

| Aspecto | Problema primal | Problema dual |
|---|---|---|
| Interpretación | Optimización de la frontera | Optimización de la evidencia |
| Variable | Vector de pesos $w\in\mathbb{R}^d$ y sesgo $w_0$ | Multiplicadores de Lagrange $\alpha_i\in\mathbb{R}^n$, uno por muestra |
| Objetivo | Minimizar $\frac{1}{2}\lVert w\rVert^2$ | Maximizar la suma de influencias menos productos internos de clase |
| Restricción | $y_i(w^Tx_i+w_0)\ge 1$ | $0\le\alpha_i\le C$ y $\sum_i \alpha_i y_i=0$ |
| Complejidad | Crece con la dimensión de entrada $d$ | Crece con el número de muestras $n$ |
| Enfoque | Determinar la inclinación y posición del hiperplano | Identificar muestras críticas, los vectores de soporte |

**Vínculo con KKT:** la solución es la misma gracias a la condición de estacionariedad:

$$
w^\ast=\sum_{i=1}^n \alpha_i y_i x_i.
$$

El primal da la forma; el dual dice qué piezas la construyen.

## Diapositiva 39. El Problema de Min-Max y el Punto de Silla

La reformulación busca un punto de silla (*saddle point*) en el espacio $(w,w_0,\alpha)$. El problema original se transforma en:

$$
\min_{w,w_0}\max_{\alpha\ge 0} L(w,w_0,\alpha).
\tag{3}
$$

Interpretación de la dualidad:

- el maximizador $\alpha_i$ intenta forzar que se cumplan las restricciones, subiendo el costo si hay violaciones;
- el minimizador $(w,w_0)$ intenta encontrar el hiperplano con menor norma que sobreviva a esa presión.

**La llave al dual:** al derivar respecto a las variables originales $(w,w_0)$ e igualar a cero, eliminaremos la dependencia del espacio de los pesos, sentando las bases para las condiciones KKT.

## Diapositiva 40. Las Condiciones de Karush-Kuhn-Tucker

Para que $(w^\ast,w_0^\ast,\alpha^\ast)$ sea una solución óptima, deben cumplirse las condiciones necesarias y suficientes para problemas convexos:

1. **Estacionariedad:** el gradiente del Lagrangiano respecto a las variables primales debe ser nulo.
2. **Viabilidad primal:** se deben respetar las restricciones originales.
3. **Viabilidad dual:** los multiplicadores deben ser no negativos, $\alpha_i\ge 0$.
4. **Holgura complementaria:**

$$
\alpha_i\left[1-y_i(w^Tx_i+w_0)\right]=0,
\qquad
\forall i.
\tag{4}
$$

Clave: la holgura complementaria es la condición que define la estructura de SVM.

## Diapositiva 41. Consecuencias de la Estacionariedad

Al derivar $L$ respecto a las variables de decisión primales e igualar a cero:

**Derivada respecto a $w$:**

$$
\frac{\partial L}{\partial w}
=
w-\sum_i \alpha_i y_i x_i
=0.
$$

Resultado:

$$
w^\ast=\sum_{i=1}^n \alpha_i y_i x_i.
$$

**Derivada respecto a $w_0$:**

$$
\frac{\partial L}{\partial w_0}
=
\sum_i \alpha_i y_i
=0.
$$

Restricción:

$$
\sum_i \alpha_i y_i=0.
$$

Implicancia: el vector de pesos $w$ es una combinación lineal de los datos de entrenamiento. Esto permite la transición al problema dual.

## Diapositiva 42. Condiciones de Estacionariedad

Derivando respecto de $w$:

$$
\nabla_w L
=
w-\sum_{i=1}^n \alpha_i y_i x_i
=0,
$$

por lo tanto:

$$
w=\sum_{i=1}^n \alpha_i y_i x_i.
$$

Derivando respecto de $w_0$:

$$
\frac{\partial L}{\partial w_0}
=
-
\sum_{i=1}^n \alpha_i y_i
=0,
$$

entonces:

$$
\sum_{i=1}^n \alpha_i y_i=0.
$$

## Diapositiva 43. Consecuencias de la Estacionariedad

Aplicando las derivadas parciales al Lagrangiano:

**1. Con respecto al vector de pesos $w$:**

$$
\frac{\partial L}{\partial w}
=
w-\sum_{i=1}^n \alpha_i y_i x_i
=0
\quad\Longrightarrow\quad
w^\ast=\sum_{i=1}^n \alpha_i y_i x_i.
\tag{5}
$$

**2. Con respecto al sesgo $w_0$:**

$$
\frac{\partial L}{\partial w_0}
=
-
\sum_{i=1}^n \alpha_i y_i
=0
\quad\Longrightarrow\quad
\sum_{i=1}^n \alpha_i y_i=0.
\tag{6}
$$

## Diapositiva 44. Holgura Complementaria y Sparsity

La condición:

$$
\alpha_i\left[y_i(w^Tx_i+w_0)-1\right]=0
$$

es la más reveladora de SVM.

- **Caso A:** $y_i(w^Tx_i+w_0)>1$. El punto está más allá del margen. Para que el producto sea cero, necesariamente $\alpha_i=0$. Estos puntos no influyen en la definición de $w^\ast$.
- **Caso B:** $\alpha_i>0$. Para que el producto sea cero, necesariamente:

$$
y_i(w^Tx_i+w_0)=1.
$$

**Teorema:** los puntos con $\alpha_i>0$ se sitúan exactamente sobre las fronteras del margen. Estos son los vectores de soporte. La solución es *sparse* porque depende solo de un subconjunto crítico de los datos.

## Diapositiva 45. Problema Dual

Sustituyendo en el Lagrangiano se obtiene:

$$
\max_\alpha
\sum_{i=1}^n \alpha_i
-
\frac{1}{2}
\sum_{i=1}^n
\sum_{j=1}^n
\alpha_i\alpha_j y_i y_j x_i^T x_j
$$

sujeto a:

$$
\alpha_i\ge 0,
\qquad
\sum_{i=1}^n \alpha_i y_i=0.
$$

**Punto clave:** los datos aparecen solamente mediante productos internos $x_i^Tx_j$.

## Diapositiva 46. Complementariedad KKT

Las condiciones KKT incluyen:

$$
\alpha_i\left[y_i(w^Tx_i+b)-1\right]=0.
$$

Por lo tanto:

$$
\alpha_i>0
\quad\Longrightarrow\quad
y_i(w^Tx_i+b)=1.
$$

Conclusión: solo los puntos con $\alpha_i>0$ contribuyen a:

$$
w=\sum_i \alpha_i y_i x_i.
$$

Esos son los vectores de soporte.

## Diapositiva 47. Función de Decisión

Como:

$$
w=\sum_{i=1}^n \alpha_i y_i x_i,
$$

la función discriminante puede escribirse como:

$$
f(x)
=
w^Tx+b
=
\sum_{i=1}^n \alpha_i y_i x_i^T x+b.
$$

En realidad solo suman los vectores de soporte:

$$
f(x)
=
\sum_{i\in SV}\alpha_i y_i x_i^T x+b.
$$

La decisión es:

$$
\hat y=\operatorname{sign}(f(x)).
$$

## Diapositiva 48. Vectores de Soporte: Solución es Sparse

Analicemos la condición de holgura complementaria:

$$
\alpha_i\left[1-y_i g(x_i)\right]=0.
$$

- Si el punto $x_i$ está fuera de la banda, $y_i g(x_i)>1$. Entonces, para cumplir la ecuación, necesariamente $\alpha_i=0$. Estos puntos no participan en la definición de $w^\ast$.
- Si el punto $x_i$ toca la banda, $y_i g(x_i)=1$. Entonces el multiplicador cumple $\alpha_i>0$.

**Definición de vector de soporte:** los vectores de soporte son los únicos puntos con $\alpha_i\ne 0$. El modelo final solo necesita recordar estos pocos puntos para definir la frontera óptima.

## Diapositiva 49. La Fragilidad del Margen Duro

El modelo presentado hasta ahora asume que los datos son linealmente separables. Sin embargo, en la práctica:

- un solo outlier cerca de la frontera puede reducir drásticamente el margen;
- si un punto de una clase se mezcla con la otra, el problema de optimización se vuelve inviable, porque no existe solución que satisfaga todas las restricciones.

Necesidad: debemos permitir que el modelo ignore o tolere ciertas violaciones a las restricciones para ganar robustez estructural.

Para ello introducimos variables:

$$
\xi_i\ge 0,
$$

llamadas holguras, que permiten que un punto traspase el margen:

$$
y_i(w^Tx_i+w_0)\ge 1-\xi_i.
$$

Interpretación:

- $\xi_i=0$: el punto está correctamente clasificado y fuera del margen;
- $0<\xi_i\le 1$: el punto está entre el margen y el hiperplano, es decir, viola el margen;
- $\xi_i>1$: el punto está del lado equivocado del hiperplano, es decir, es un error de clasificación.

## Diapositiva 50. El Problema Primal con Margen Blando

Ahora el objetivo es maximizar el margen y minimizar la suma de los cruces.

**Nuevo problema primal:**

$$
\min_{w,w_0,\xi}
\frac{1}{2}\lVert w\rVert^2
+
C\sum_{i=1}^n \xi_i
\tag{7}
$$

sujeto a:

$$
y_i(w^Tx_i+w_0)\ge 1-\xi_i,
\qquad
\xi_i\ge 0.
$$

El parámetro $C$:

- $C\to\infty$: recuperamos el margen duro, no toleramos errores;
- $C\to 0$: maximizamos el margen a toda costa, permitimos muchos errores.

$C$ es el hiperparámetro de regularización que conecta SVM con el *trade-off* sesgo-varianza.

## Diapositiva 51. Dualidad en Margen Blando: Box Constraint

Al aplicar KKT al nuevo primal, el problema dual resultante es casi idéntico al anterior, pero con una restricción adicional sobre los multiplicadores.

**Dual de margen blando:**

$$
\max_\alpha
\sum_i \alpha_i
-
\frac{1}{2}
\sum_{i,j}
\alpha_i\alpha_j y_i y_j x_i^T x_j
$$

sujeto a:

$$
0\le \alpha_i\le C,
\qquad
\sum_i \alpha_i y_i=0.
$$

¿Quién es quién en el modelo?

- $\alpha_i=0$: puntos irrelevantes, correctos y lejos del margen.
- $0<\alpha_i<C$: vectores de soporte libres, exactamente sobre el margen.
- $\alpha_i=C$: vectores de soporte acotados, dentro del margen o con errores.

## Diapositiva 52. El Kernel Trick

Observamos que tanto en el dual como en la función de decisión final, los datos $x$ aparecen solo como productos internos.

**Teorema de Mercer:** podemos sustituir $x_i^T x_j$ por una función de núcleo $K(x_i,x_j)$ que represente un producto interno en un espacio de Hilbert $\mathcal{H}$ de alta dimensión:

$$
K(x_i,x_j)=\langle \phi(x_i),\phi(x_j)\rangle.
\tag{8}
$$

Consecuencias:

- **No linealidad "gratis":** construimos fronteras complejas en $\mathbb{R}^d$ que son hiperplanos en $\mathcal{H}$.
- **Eficiencia:** jamás computamos explícitamente el mapeo $\phi(x)$.

## Diapositiva 53. Síntesis: Arquitectura Lógica del SVM

La arquitectura lógica conecta:

- regularización L2;
- máximo margen;
- inviabilidad ante datos no separables;
- margen blando y holguras $\xi_i$;
- parámetro $C$ como *trade-off* sesgo-varianza;
- condiciones KKT y vectores de soporte;
- problema dual y productos internos;
- kernel trick y espacios de dimensión infinita.

SVM combina estadística, regularización, geometría del margen y optimización dual.

![Arquitectura lógica del SVM](figures/clase-10/fig-53-svm-architecture.png)

## Diapositiva 54. Capacidad, Generalización y Evaluación

**Sección:** Capacidad, generalización y evaluación.

## Diapositiva 55. La Limitación Lineal

Una SVM lineal aprende:

$$
f(x)=w^Tx+b.
$$

Si las clases tienen estructura no lineal, podemos transformar:

$$
\phi:\mathbb{R}^d\to\mathbb{R}^p.
$$

Luego aprendemos una frontera lineal en el espacio transformado:

$$
f(x)=w^T\phi(x)+b.
$$

En el espacio original, esa frontera puede ser no lineal.

## Diapositiva 56. Ejemplo: Frontera Cuadrática

En una dimensión, separar puntos cerca del origen de puntos lejos del origen no es lineal en $x$.

Definimos:

$$
\phi(x)=
\begin{pmatrix}
x\\
x^2
\end{pmatrix}.
$$

Una frontera lineal en $\phi(x)$:

$$
a_1x+a_2x^2+b=0
$$

es una frontera cuadrática en el espacio original.

Esta idea ya apareció al discutir XOR y mapeos de características.

## Diapositiva 57. El Dual con $\phi$

Si trabajamos con $\phi(x)$, el dual usa productos internos:

$$
\phi(x_i)^T\phi(x_j).
$$

El problema dual:

$$
\max_\alpha
\sum_i \alpha_i
-
\frac{1}{2}
\sum_{i,j}
\alpha_i\alpha_j y_i y_j
\phi(x_i)^T\phi(x_j).
$$

**Observación:** no necesitamos conocer explícitamente $\phi(x)$ si podemos calcular esos productos internos.

## Diapositiva 58. Kernel Trick

Un kernel es una función:

$$
K:\mathcal{X}\times\mathcal{X}\to\mathbb{R}
$$

tal que:

$$
K(x,x')=\phi(x)^T\phi(x')
$$

para algún mapa de características $\phi$.

Entonces:

$$
f(x)=\sum_{i\in SV}\alpha_i y_i K(x_i,x)+b.
$$

**Ventaja:** podemos aprender fronteras no lineales sin construir explícitamente el espacio transformado.

## Diapositiva 59. Kernel RBF

El kernel gaussiano o RBF es:

$$
K(x,x')=\exp\left(-\gamma\lVert x-x'\rVert^2\right).
$$

Interpretación:

- mide similitud local;
- puntos cercanos tienen kernel cercano a 1;
- puntos lejanos tienen kernel cercano a 0.

El parámetro $\gamma$ controla el alcance:

$$
\gamma\text{ grande}
\quad\Longrightarrow\quad
\text{influencia muy local}.
$$

## Diapositiva 60. El Rol de $\gamma$

En RBF:

$$
K(x,x')=\exp\left(-\gamma\lVert x-x'\rVert^2\right).
$$

- $\gamma$ chico: fronteras suaves, vecindarios grandes.
- $\gamma$ grande: fronteras muy locales, alta flexibilidad.

**Relación con Parzen y k-NN:** como en métodos locales, hay una escala espacial. En Parzen era el ancho de banda $h$; aquí es aproximadamente:

$$
\frac{1}{\sqrt{\gamma}}.
$$

## Diapositiva 61. Selección Conjunta de $C$ y $\gamma$

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
\arg\min_{C,\gamma}\operatorname{CV}_K(C,\gamma).
$$

**Cuidado:** cuanto más grande la búsqueda, más importante es separar selección de evaluación final.

## Diapositiva 62. Margen y Generalización

La intuición central de SVM:

**Idea:** a igualdad de error de entrenamiento, una frontera con mayor margen debería ser menos sensible a perturbaciones de la muestra.

Si:

$$
\gamma
=
\min_i
\frac{y_i(w^Tx_i+b)}{\lVert w\rVert},
$$

maximizar $\gamma$ reduce la capacidad efectiva de la familia de clasificadores admisibles.

Por eso SVM conecta optimización convexa con control de complejidad.

## Diapositiva 63. Radio y Margen

Si los datos están contenidos en una bola de radio $R$:

$$
\lVert x_i\rVert\le R,
$$

y el clasificador separa con margen $\gamma$, entonces la complejidad efectiva puede acotarse en términos de:

$$
\frac{R^2}{\gamma^2}.
$$

No solo importa la dimensión $d$. Importa la relación entre escala de los datos y margen de separación.

## Diapositiva 64. Regularización, Margen y Norma

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

**Síntesis:** regularizar pesos y maximizar margen son dos caras de la misma geometría.

## Diapositiva 65. Comparación Conceptual

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

## Diapositiva 66. Relación con la Clase 9

La clase 9 dio el protocolo:

$$
\text{elegir } C,\gamma,\lambda,k,h \text{ con validación}.
$$

La clase 10 explica qué significan:

- $\lambda$: fuerza de regularización;
- $C$: costo de violar margen;
- $\gamma$: escala local del kernel RBF;
- grado polinomial: orden de interacciones;
- norma: geometría de la solución.

La selección empírica y el control matemático de capacidad son inseparables.

En SVM, el margen duro es un caso particular de una familia de clasificadores que maximizan el margen geométrico, y la SVM de margen blando es una versión regularizada de esa familia.

## Diapositiva 67. Bias-Variance Tradeoff en la Selección

Ahora que sabemos evaluar, ¿cómo decidimos entre un perceptrón lineal y un 1-NN altamente no lineal?

- **Modelos simples, como perceptrón:** alto sesgo, baja varianza. No se ajustan perfectamente, pero generalizan de forma estable.
- **Modelos complejos, como 1-NN o Parzen con $h\to 0$:** bajo sesgo, alta varianza. Memorizan el ruido del dataset.

El error esperado se descompone aditivamente:

$$
\text{Error esperado}
=
\text{sesgo}^2
+
\text{varianza}
+
\text{ruido irreducible}.
$$

Buscamos el punto adecuado. La pregunta es si hay un principio matemático fundamental que guíe esta elección.

## Diapositiva 68. Selección de Hiperparámetros y Capacidad del Modelo

**Motivación:** buscamos la generalización, es decir, la estructura que captura la esencia de la forma sin memorizar el ruido.

**Función discriminante con kernel RBF:**

$$
g(x)
=
\sum_{i\in SV}
\alpha_i y_i
\exp\left(-\gamma\lVert x-x_i\rVert^2\right)
+
b.
$$

El parámetro $\gamma$ define el radio de influencia de los vectores de soporte:

- $\uparrow\gamma$: influencia local, fronteras complejas, riesgo de memorización;
- $\downarrow\gamma$: influencia global, fronteras suaves, riesgo de sesgo.

El parámetro $C$ regula el *trade-off* en la función de costo:

$$
J(w,\xi)
=
\frac{1}{2}\lVert w\rVert^2
+
C\sum_{i=1}^n \xi_i.
$$

Donde $C$ controla la penalización de las variables de holgura $\xi_i$.

**Objetivo:** identificar la región del espacio $(C,\gamma)$ que minimiza el riesgo empírico y el riesgo estructural simultáneamente, evitando la divergencia entre el error de entrenamiento y el de validación.

## Diapositiva 69. Underfitting, Overfitting y la Curva de Validación

La diapositiva ilustra una frontera muy flexible, con error de entrenamiento bajo pero error de validación alto.

![Curva y mapa de validación para underfitting y overfitting](figures/clase-10/fig-69-validation-curve.png)

- **Underfitting:** modelo demasiado simple, por ejemplo perceptrón lineal con $\gamma$ muy bajo. Alto error de entrenamiento y validación.
- **Overfitting:** modelo demasiado complejo, por ejemplo 1-NN o SVM con $\gamma$ muy alto. Bajo error de entrenamiento pero alto error de validación.
- **Punto óptimo:** el valor de $\gamma$ y $C$ que minimiza el error de validación, logrando un equilibrio entre sesgo y varianza.
