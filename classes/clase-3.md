---
title: "Ciencia de Datos: Teoría de decisiones, introducción a métodos paramétricos"
---

# Ciencia de Datos: Teoría de decisiones, introducción a métodos paramétricos

## Diapositiva 1

Ciencia de Datos

Teoría de decisiones, introducción a métodos paramétricos

Clase 3

FaMAF

Ciencias de datos 2026-03-19

## Diapositiva 2. Roadmap de la Clase

1. Modelos paramétricos (conocidos)
   - Repaso
   - Error de Bayes y fronteras de decisión
   - Distribuciones discretas
2. Estimación de parámetros
   - Maximum Likelihood Estimation
   - MLE con distribuciones Gaussianas
   - Naive Bayes
3. Modelos no paramétricos
   - Modelo de mezcla de Gaussianas
   - Expectation-maximization

## Diapositiva 3. Modelos paramétricos (conocidos)

## Diapositiva 4. Elementos de la Teoría de Decisión

Para generalizar el problema de clasificación binaria a $c$ clases, definimos formalmente los elementos del sistema de decisión:

- **Estados de la Naturaleza:** $\Omega = \{\omega_1, \ldots, \omega_c\}$.
- **Acciones:** $\mathcal{A} = \{\alpha_1, \ldots, \alpha_a\}$.
  - Generalmente $a = c$ (decidir por una clase).
  - Puede ser $a > c$ (e.g., opción de rechazo).
- **Función de Pérdida (Loss Function):** $\lambda(\alpha_i \mid \omega_j)$.
  - Costo incurrido al tomar la acción $\alpha_i$ cuando el estado verdadero es $\omega_j$.

## Diapositiva 5. Riesgo Condicional

Dada una observación $x$, queremos minimizar el costo esperado.

**Def./ (Riesgo Condicional)**

El riesgo condicional $R(\alpha_i \mid x)$ es la pérdida esperada asociada a tomar la acción $\alpha_i$:

$$
R(\alpha_i \mid x) = \sum_{j=1}^c \lambda(\alpha_i \mid \omega_j) P(\omega_j \mid x)
$$

Donde $P(\omega_j \mid x)$ es la probabilidad a posteriori calculada por Bayes:

$$
P(\omega_j \mid x) = \frac{p(x \mid \omega_j) P(\omega_j)}{p(x)}
$$

## Diapositiva 6. Regla de Decisión de Bayes

Buscamos una regla de decisión $\alpha(x)$ que asigne a cada $x$ una acción del conjunto $\mathcal{A}$.

**Bayes Decision Rule**

Seleccionar la acción $\alpha_{opt}$ que minimice el riesgo condicional:

$$
\alpha_{opt} = \arg \min_{\alpha_i \in \mathcal{A}} R(\alpha_i \mid x)
$$

El **Riesgo de Bayes** $R^*$ es el riesgo total mínimo posible (la integral del riesgo condicional mínimo sobre todo el espacio $\mathcal{X}$):

$$
R^* = \int R(\alpha(x) \mid x) p(x) \, dx
$$

## Diapositiva 7. Función de Pérdida Simétrica (0/1)

El caso más común en clasificación pura (minimizar tasa de error).

$$
\lambda(\alpha_i \mid \omega_j) =
\begin{cases}
0 & \text{si } i = j \; (\text{Acierto}) \\
1 & \text{si } i \ne j \; (\text{Error})
\end{cases}
$$

| Caso | Pérdida |
| --- | ---: |
| Decisión Correcta | 0 |
| Decisión Incorrecta | 1 |

El riesgo condicional se simplifica:

$$
R(\alpha_i \mid x) = \sum_{j \ne i} P(\omega_j \mid x) = 1 - P(\omega_i \mid x)
$$

**Conclusión:** Minimizar el riesgo es equivalente a **Maximizar la Probabilidad A Posteriori (MAP)**.

$$
\text{Decidir } \omega_i \text{ si } P(\omega_i \mid x) > P(\omega_j \mid x) \qquad \forall j \ne i
$$

## Diapositiva 8. Classificación con opción a rechazo

En aplicaciones críticas (medicina, finanzas), preferimos no clasificar si la incertidumbre es alta. Definimos una acción extra $\alpha_{c+1}$ (Rechazar/Duda). **Loss Function:**

$$
\lambda(\alpha_i \mid \omega_j) =
\begin{cases}
0 & \text{si } i = j,\; i \le c \\
\lambda_s & \text{si } i \ne j,\; i \le c \; (\text{Error Sustitución}) \\
\lambda_r & \text{si } i = c + 1 \; (\text{Rechazo})
\end{cases}
$$

Generalmente $0 < \lambda_r < \lambda_s$.

El riesgo de clasificar como $\omega_i$ es $R(\alpha_i \mid x) = \lambda_s (1 - P(\omega_i \mid x))$. El riesgo de rechazar es $R(\alpha_{c+1} \mid x) = \lambda_r$.

**Regla de Decisión:** Decidir $\omega_i$ si:

1. $P(\omega_i \mid x) \ge P(\omega_j \mid x)$ para todo $j$.
2. $P(\omega_i \mid x) \ge 1 - \dfrac{\lambda_r}{\lambda_s}$.

Caso contrario: **Rechazar**. Esto define una "región de rechazo" donde ninguna clase tiene suficiente probabilidad posterior.

## Diapositiva 9. El Error de Bayes

Incluso con el clasificador óptimo, existe una probabilidad de error irreducible debido al solapamiento de las densidades.

$$
P(\text{error}) = \int \min[P(\omega_1 \mid x), P(\omega_2 \mid x)] p(x) \, dx
$$

Calcular esta integral exacta suele ser difícil analíticamente.

![Ejemplo gráfico del solapamiento entre densidades](figures/clase-3/fig-009-001.png)

[interactivo]

## Diapositiva 10. Cotas de Error (Bounds)

Para distribuciones normales, podemos acotar el error superiormente.

**Chernoff Bound:**

$$
P(\text{error}) \le P(\omega_1)^s P(\omega_2)^{1-s} e^{-k(s)}
$$

para $0 \le s \le 1$, donde $k(s)$ es la distancia de Chernoff.

**Bhattacharyya Bound:**

Caso particular con $s = 0.5$. Provee una cota un poco más suelta pero fácil de calcular.

$$
P(\text{error}) \le \sqrt{P(\omega_1) P(\omega_2)} e^{-k(0.5)}
$$

## Diapositiva 11. Representación de Clasificadores

$$
R^* = \int R(\alpha(x) \mid x) p(x) \, dx
$$

Es útil abstraer esto en funciones matemáticas que además generalicen la regla:

**Def./ (Función Discriminante)**

Un clasificador puede representarse por un conjunto de funciones $g_i(x)$, $i = 1, \ldots, c$.

La regla de decisión es:

$$
\text{Asignar } x \text{ a la clase } \omega_i
\Longleftrightarrow
g_i(x) > g_j(x)
\qquad
\forall j \ne i
$$

El clasificador es una red que calcula $c$ valores y elige el máximo ("Winner-takes-all").

## Diapositiva 12. Regiones de decisión

Las regiones de decisión $\mathcal{R}_i$ están separadas por superficies de decisión definidas por:

$$
g_i(x) = g_j(x)
\Longleftrightarrow
g_i(x) - g_j(x) = 0
$$

![Ejemplos de regiones y superficies de decisión](figures/clase-3/fig-012-002.png)

## Diapositiva 13. Regiones de decisión con Bayes

Para el clasificador de Bayes (Mínimo Error), la elección natural es:

$$
g_i(x) = P(\omega_i \mid x) = \frac{p(x \mid \omega_i) P(\omega_i)}{p(x)}
$$

Si pedimos que $g_i(x) = g_j(x) \Longleftrightarrow g_i(x) - g_j(x) = 0$, entonces:

$$
\frac{p(x \mid \omega_i) P(\omega_i)}{p(x)}
=
\frac{p(x \mid \omega_j) P(\omega_j)}{p(x)}
$$

Eliminando $p(x)$:

$$
p(x \mid \omega_i) P(\omega_i) = p(x \mid \omega_j) P(\omega_j)
$$

## Diapositiva 14. Regiones de decisión con Bayes

Para simplificar, notemos que cualquier función monótona creciente $f(\cdot)$ no altera el orden de decisión. Usando $f = \ln$:

$$
\ln \bigl(p(x \mid \omega_i) P(\omega_i)\bigr)
=
\ln \bigl(p(x \mid \omega_j) P(\omega_j)\bigr)
$$

$$
\Longrightarrow
\ln p(x \mid \omega_i) + \ln P(\omega_i)
=
\ln p(x \mid \omega_j) + \ln P(\omega_j)
$$

Definimos la función discriminante:

$$
g_i(x) = \ln p(x \mid \omega_i) + \ln P(\omega_i)
$$

Por lo tanto,

$$
\ln p(x \mid \omega_i) + \ln P(\omega_i)
=
\ln p(x \mid \omega_j) + \ln P(\omega_j)
$$

## Diapositiva 15. Gaussian Density (Univariada)

La probabilidad posterior de la regla de decisión de Bayes

$$
P(\omega_i \mid x) = \frac{p(x \mid \omega_i) P(\omega_i)}{p(x)}
$$

da la probabilidad de que $x$ pertenezca a la clase $\omega_i$, y permite calcular qué clase elegimos, pero solo si conocemos $P(\omega_i)$ y $p(x \mid \omega_i)$.

$$
P(\omega_i) \longleftrightarrow \text{un número}
$$

$$
p(x \mid \omega_i) \longleftrightarrow \text{una función}
$$

## Diapositiva 16. Densidad normal (Univariada)

Asumimos que las verosimilitudes $p(x \mid \omega_j)$ son Gaussianas:

$$
p(x \mid \omega_j) = \frac{1}{\sqrt{2\pi}\sigma_j} \exp\left[-\frac{1}{2}\left(\frac{x - \mu_j}{\sigma_j}\right)^2\right]
$$

| Hipótesis | Descripción |
| --- | --- |
| Densidad Condicional | Gaussiana univariada |
| Caso | Binario $(\omega_1, \omega_2)$ |
| Variable | $x \in \mathbb{R}$ |

Consideremos el caso binario $(\omega_1, \omega_2)$ con priors $P(\omega_1)$, $P(\omega_2)$. La regla de decisión (Loss general) utiliza el umbral de verosimilitud:

$$
\frac{p(x \mid \omega_1)}{p(x \mid \omega_2)} > T^*
$$

$$
T^* = \frac{\lambda_{12} - \lambda_{22}}{\lambda_{21} - \lambda_{11}} \frac{P(\omega_2)}{P(\omega_1)}
$$

## Diapositiva 17. Densidad normal (Univariada)

$$
p(x \mid \omega_j) = \frac{1}{\sqrt{2\pi}\sigma_j} \exp\left[-\frac{1}{2}\left(\frac{x - \mu_j}{\sigma_j}\right)^2\right]
$$

Tomando logaritmo:

$$
\ln p(x \mid \omega_j) = -\frac{1}{2}\ln(2\pi\sigma_j^2) - \frac{(x - \mu_j)^2}{2\sigma_j^2}
$$

Luego,

$$
\ln \frac{p(x \mid \omega_1)}{p(x \mid \omega_2)}
=
\left(-\frac{1}{2}\ln(2\pi\sigma_1^2) - \frac{(x - \mu_1)^2}{2\sigma_1^2}\right)
-
\left(-\frac{1}{2}\ln(2\pi\sigma_2^2) - \frac{(x - \mu_2)^2}{2\sigma_2^2}\right)
$$

$$
\ln \frac{p(x \mid \omega_1)}{p(x \mid \omega_2)}
=
\left(\frac{1}{2}\ln(2\pi\sigma_2^2) - \frac{1}{2}\ln(2\pi\sigma_1^2)\right)
-
\left(\frac{(x - \mu_2)^2}{2\sigma_2^2} - \frac{(x - \mu_1)^2}{2\sigma_1^2}\right)
$$

## Diapositiva 18. Caso 1: Igual Varianza ($\sigma_1 = \sigma_2 = \sigma$)

| Simplificación | Descripción |
| --- | --- |
| Varianzas | $\sigma_1 = \sigma_2 = \sigma$ (iguales) |
| Fronteras | Lineales |

Tomando logaritmos en la razón de verosimilitud (Log-Likelihood Ratio):

$$
\ln \frac{p(x \mid \omega_1)}{p(x \mid \omega_2)} > \ln T^*
$$

$$
-\frac{(x - \mu_1)^2}{2\sigma^2} + \frac{(x - \mu_2)^2}{2\sigma^2} > \ln T^*
$$

$$
\frac{(x - \mu_2)^2 - (x - \mu_1)^2}{2\sigma^2} > \ln T^*
$$

Desarrollando los cuadrados:

$$
(x - \mu_2)^2 - (x - \mu_1)^2 = (x^2 - 2\mu_2 x + \mu_2^2) - (x^2 - 2\mu_1 x + \mu_1^2)
$$

$$
= 2(\mu_1 - \mu_2)x + (\mu_2^2 - \mu_1^2)
$$

## Diapositiva 19. Caso 1: Igual Varianza ($\sigma_1 = \sigma_2 = \sigma$)

Sustituyendo:

$$
\frac{2(\mu_1 - \mu_2)x + (\mu_2^2 - \mu_1^2)}{2\sigma^2} > \ln T^*
$$

$$
(\mu_1 - \mu_2)x + \frac{1}{2}(\mu_2^2 - \mu_1^2) > \sigma^2 \ln T^*
$$

$$
x(\mu_1 - \mu_2) > \sigma^2 \ln T^* + \frac{1}{2}(\mu_1^2 - \mu_2^2)
$$

**Resultado:** La frontera de decisión es lineal (un punto en 1D).

$$
x(\mu_1 - \mu_2) > \sigma^2 \ln T^* + \frac{1}{2}(\mu_1^2 - \mu_2^2)
$$

Si los Priors son iguales y tenemos *zero/one loss*, entonces:

$$
x > \frac{\mu_1 + \mu_2}{2}
$$

## Diapositiva 20. Caso 2: Varianzas Distintas ($\sigma_1 \ne \sigma_2$)

| Simplificación | Descripción |
| --- | --- |
| Varianzas | $\sigma_1 \ne \sigma_2$ (distintas) |
| Fronteras | Cuadráticas |

Si las varianzas difieren, los términos cuadráticos $x^2$ NO se cancelan.

$$
\ln \frac{p(x \mid \omega_1)}{p(x \mid \omega_2)} > \ln T^*
$$

$$
-\frac{(x - \mu_1)^2}{2\sigma_1^2} + \frac{(x - \mu_2)^2}{2\sigma_2^2} > \ln T^*
$$

## Diapositiva 21. Caso 2: Varianzas Distintas ($\sigma_1 \ne \sigma_2$)

A partir del cociente de Likelihoods:

$$
\ln \frac{p(x \mid \omega_1)}{p(x \mid \omega_2)} > \ln T^*
$$

$$
\left[-\frac{1}{2}\ln(2\pi\sigma_1^2) - \frac{(x - \mu_1)^2}{2\sigma_1^2}\right]
-
\left[-\frac{1}{2}\ln(2\pi\sigma_2^2) - \frac{(x - \mu_2)^2}{2\sigma_2^2}\right]
>
\ln T^*
$$

Agrupamos términos logarítmicos y simplificamos:

$$
\frac{(x - \mu_2)^2}{2\sigma_2^2} - \frac{(x - \mu_1)^2}{2\sigma_1^2} + \ln \frac{\sigma_2}{\sigma_1} > \ln T^*
$$

Expandimos cuadrados y denominador común: $(2\sigma_1^2\sigma_2^2)$:

$$
\frac{\sigma_1^2(x^2 - 2\mu_2 x + \mu_2^2) - \sigma_2^2(x^2 - 2\mu_1 x + \mu_1^2)}{2\sigma_1^2\sigma_2^2}
>
\ln\left(T^* \frac{\sigma_1}{\sigma_2}\right)
$$

Agrupamos por potencias de $x$:

$$
\frac{(\sigma_1^2 - \sigma_2^2)x^2 + 2(\mu_1\sigma_2^2 - \mu_2\sigma_1^2)x + (\mu_2^2\sigma_1^2 - \mu_1^2\sigma_2^2)}{2\sigma_1^2\sigma_2^2}
>
\ln\left(T^* \frac{\sigma_1}{\sigma_2}\right)
$$

## Diapositiva 22. Decision Boundaries

A partir del cociente de Likelihoods:

$$
\ln \frac{p(x \mid \omega_1)}{p(x \mid \omega_2)} > \ln T^*
$$

Forma cuadrática final:

$$
Ax^2 + Bx + C > 0
$$

$$
x^2 \left(\frac{\sigma_1^2 - \sigma_2^2}{2\sigma_1^2\sigma_2^2}\right)
+
x \left(\frac{\mu_1\sigma_2^2 - \mu_2\sigma_1^2}{\sigma_1^2\sigma_2^2}\right)
+
\left(\frac{\mu_2^2\sigma_1^2 - \mu_1^2\sigma_2^2}{2\sigma_1^2\sigma_2^2} - \ln \frac{T^*\sigma_1}{\sigma_2}\right)
>
0
$$

Implicación: La región de decisión para una clase puede estar desconectada (e.g., decidir $\omega_1$ si $x$ es muy pequeño O muy grande, y $\omega_2$ si está en el medio).

## Diapositiva 23. Decision Boundaries

![Ejemplo gráfico de fronteras de decisión cuadráticas](figures/clase-3/fig-023-003.png)

[interactivo]

## Diapositiva 24. Ejemplo Numérico

**Datos:** $\omega_1 : N(2, 0.5)$, $\omega_2 : N(1.5, 0.2)$. Con $T^* = 1$.

- **Sustitución:**

$$
\frac{(x - 1.5)^2}{0.4} - \frac{(x - 2)^2}{1} + \ln \sqrt{\frac{0.2}{0.5}} = 0
$$

- **Polinomio Resultante:** $1.5x^2 - 3.5x + 1.1669 = 0$

**Resultados**

Las raíces de la ecuación definen los puntos de decisión:

- $x_1 \approx 0.403$
- $x_2 \approx 1.930$

**Decisión:** Se elige $\omega_1$ (mayor varianza) en los extremos ($x < 0.403$ o $x > 1.930$) y $\omega_2$ en el intervalo central.

## Diapositiva 25. Ejemplo 2: Impacto de los Costos Asimétricos

**Configuración:** $\omega_1 : N(10, 1)$, $\omega_2 : N(12, 4)$. $P(\omega_1) = 0.2$, $P(\omega_2) = 0.8$. Costos: $\lambda_{21} = 10$ (Falso Negativo crítico).

**Cálculo del Umbral**

$$
T^* = \frac{1}{10} \cdot \frac{0.8}{0.2} = 0.4
$$

- **Ecuación resultante:** $-3x^2 + 56x - 243.12 = 0$
- **Fronteras:** $x_1 \approx 6.87$ y $x_2 \approx 11.80$

**Análisis:** A pesar de que la media de la clase "Sana" ($\omega_2$) es 12, el alto costo de omitir un enfermo hace que empecemos a clasificar como $\omega_1$ (enfermo) mucho antes, en $x = 11.80$. La región de la clase de mayor varianza ($\omega_2$) queda "encerrada" o desplazada por el peso del costo de $\omega_1$.

## Diapositiva 26. Multivariate Normal Density

La generalización a $d$ dimensiones de la Gaussiana es fundamental en ML.

$$
p(x) = \frac{1}{(2\pi)^{d/2} |\Sigma|^{1/2}} \exp\left[-\frac{1}{2}(x - \mu)^T \Sigma^{-1}(x - \mu)\right]
$$

Donde:

- $x$: vector de características $d$-dimensional.
- $\mu$: vector de medias $d$-dimensional.
- $\Sigma$: matriz de covarianza $d \times d$ (simétrica, definida positiva).
- $|\Sigma|$: determinante de $\Sigma$.

Escribimos abreviadamente $x \sim N(\mu, \Sigma)$.

## Diapositiva 27. La Matriz de Covarianza $\Sigma$

Elemento $\sigma_{ij} = E[(x_i - \mu_i)(x_j - \mu_j)]$.

- La matriz determina la "forma" de la dispersión de los datos.
- Los autovectores de $\Sigma$ definen los ejes principales de los elipsoides de densidad constante.
- Los autovalores $\lambda_k$ determinan la varianza a lo largo de esos ejes.

![Interpretación geométrica de la covarianza](figures/clase-3/fig-027-004.png)

## Diapositiva 28. Mahalanobis Distance

El término en el exponente es una distancia cuadrática:

$$
\Delta^2 = (x - \mu)^T \Sigma^{-1} (x - \mu)
$$

Esta es la **Distancia de Mahalanobis**.

- Si $\Sigma = I$ (Identidad), recuperamos la distancia Euclídea cuadrada $\lVert x - \mu \rVert^2$.
- Si $\Sigma$ es diagonal, es una distancia Euclídea normalizada por la varianza de cada feature.
- En general, "blanquea" las correlaciones entre variables.

## Diapositiva 29. Derivación del Discriminante Gaussiano

Sustituyendo la densidad normal en $g_i(x) = \ln p(x \mid \omega_i) + \ln P(\omega_i)$:

$$
g_i(x) = -\frac{1}{2}(x - \mu_i)^T \Sigma_i^{-1}(x - \mu_i) - \frac{d}{2}\ln(2\pi) - \frac{1}{2}\ln |\Sigma_i| + \ln P(\omega_i)
$$

Eliminando el término constante $d/2 \ln(2\pi)$:

**Forma General**

$$
g_i(x) = -\frac{1}{2}(x - \mu_i)^T \Sigma_i^{-1}(x - \mu_i) - \frac{1}{2}\ln |\Sigma_i| + \ln P(\omega_i)
$$

La forma de la frontera depende de la relación entre las matrices $\Sigma_i$.

## Diapositiva 30. Caso 1: $\Sigma_i = \sigma^2 I$

Todas las clases tienen la misma varianza y las features son estadísticamente independientes.

$$
\Sigma_i^{-1} = \frac{1}{\sigma^2} I
$$

El término cuadrático $(x - \mu_i)^T (x - \mu_i)$ es simplemente $\lVert x - \mu_i \rVert^2$.

$$
g_i(x) = -\frac{\lVert x - \mu_i \rVert^2}{2\sigma^2} + \ln P(\omega_i)
$$

(Ignorando términos constantes de $|\Sigma_i|$). Expandiendo:

$$
g_i(x) = \frac{1}{\sigma^2}\mu_i^T x + \left(-\frac{1}{2\sigma^2}\mu_i^T \mu_i + \ln P(\omega_i)\right)
$$

Identificando

$$
w_i^T = \frac{1}{\sigma^2}\mu_i^T,
\qquad
w_{i0} = -\frac{1}{2\sigma^2}\mu_i^T \mu_i + \ln P(\omega_i)
$$

## Diapositiva 31. Caso 1: $\Sigma_i = \sigma^2 I$

La función es lineal:

$$
g_i(x) = w_i^T x + w_{i0}
$$

**Frontera de decisión** $(g_i = g_j)$:

$$
w^T(x - x_0) = 0
$$

Donde $w = \mu_i - \mu_j$.

- La frontera es un hiperplano perpendicular al segmento que une las medias.
- Si $P(\omega_i) = P(\omega_j)$, el hiperplano pasa exactamente por el punto medio.
- Es un clasificador de **Mínima Distancia Euclídea**.

(ver snippet `decision_boundary`)

## Diapositiva 32. Caso 1: $\Sigma_i = \sigma^2 I$

![Ejemplos geométricos de la frontera gaussiana lineal](figures/clase-3/fig-032-005.png)

## Diapositiva 33. Caso 1: $\Sigma_i = \sigma^2 I$

![Interfaz interactiva de Gaussian Decision Boundary](figures/clase-3/fig-033-006.png)

## Diapositiva 34. Caso 2: $\Sigma_i = \Sigma$

Las clases tienen la misma matriz de covarianza, pero puede haber correlación entre features (elipsoides paralelos). El término cuadrático $x^T \Sigma^{-1} x$ es idéntico para todas las clases y se cancela al comparar $g_i(x)$ con $g_j(x)$.

$$
g_i(x) = -\frac{1}{2}\left(\mu_i^T \Sigma^{-1}\mu_i - 2\mu_i^T \Sigma^{-1}x\right) + \ln P(\omega_i)
$$

Reordenando para obtener la forma lineal $w_i^T x + w_{i0}$:

$$
w_i = \Sigma^{-1}\mu_i
$$

$$
w_{i0} = -\frac{1}{2}\mu_i^T \Sigma^{-1}\mu_i + \ln P(\omega_i)
$$

## Diapositiva 35. Caso 2: $\Sigma_i = \Sigma$

- El resultado sigue siendo una frontera lineal (**Linear Discriminant Analysis**).
- La frontera NO es perpendicular a la línea que une las medias.
- Se ajusta por la dirección de mayor varianza de los datos.
- Clasificador de **Mínima Distancia de Mahalanobis**.
