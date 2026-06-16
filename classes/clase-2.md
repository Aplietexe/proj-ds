---
title: "Introducción a la Ciencia de Datos: Fundamentos Probabilísticos y teoría de decisiones"
---

## Diapositiva 1

**Portada**

- Clase 2
- FaMAF
- Ciencias de datos 2026-03-12

## Diapositiva 2. Métricas de clasificación

**Sección:** Métricas de clasificación.

## Diapositiva 3. Modelo de filtro de spam

Escena introductoria del problema de filtrado de spam.

![Escena inicial del filtro de spam](figures/clase-2/slide-03.png)

## Diapositiva 4. Modelo de filtro de spam

Distribución de clases del conjunto de e-mails:

- no spam: 98%
- spam: 2%

![Distribución de clases de e-mails](figures/clase-2/slide-04.png)

## Diapositiva 5. Modelo de filtro de spam

La colección de correos está fuertemente desbalanceada:

- no spam: 98%
- spam: 2%

![Desbalance entre e-mails spam y no spam](figures/clase-2/slide-05.png)

## Diapositiva 6. Modelo de filtro de spam

- Modelo: nada es spam.
- Anda bien el 98% de las veces.
- La accuracy alta no implica que el clasificador sea útil.

![Clasificador trivial que nunca marca spam](figures/clase-2/slide-06.png)

## Diapositiva 7. Modelo de filtro de spam

- Modelo: todo es spam.
- Anda bien el 80% de las veces.
- Filtra el 100% de los spams.

![Clasificador trivial que marca todo como spam](figures/clase-2/slide-07.png)

## Diapositiva 8. Modelo de filtro de spam

Ejemplo visual del costo de un falso negativo: un correo importante termina en la carpeta de spam.

![Correo importante clasificado como spam](figures/clase-2/slide-08.png)

## Diapositiva 9. Modelo de filtro de spam

Características simples para un clasificador de spam:

- Palabras clave: promoción, oferta, urgente, gratis.
- Tiene links.
- Identifica correctamente el 75% de los spam.
- Identifica correctamente el 95% de los no spam.

## Diapositiva 10. Modelo de filtro de spam

Ejemplo de e-mail con palabras promocionales y un link.

![Ejemplo de correo con texto promocional](figures/clase-2/slide-10.png)

## Diapositiva 11. Modelo de filtro de spam

- El 80% de los mails son spam. De esos, el 75% tienen las palabras.
- El 20% de los mails no son spam. De esos, el 95% no tienen las palabras.
- Antes de mirar el mail, el sistema "cree" que el mail es spam con probabilidad del 80%.
- Luego busca las palabras en el mail y "actualiza su creencia".

## Diapositiva 12. Modelo de filtro de spam

Motivación para aplicar Bayes: combinar la probabilidad previa con la evidencia observada.

![Motivación visual para usar Bayes](figures/clase-2/slide-12.png)

## Diapositiva 13

**Portada repetida**

- Clase 2
- FaMAF
- Ciencias de datos 2026-03-12

## Diapositiva 14. Métricas de Evaluación (Clasificación)

**Sección:** Métricas de Evaluación (Clasificación).

## Diapositiva 15. Métricas de Evaluación (Clasificación)

Las métricas más comúnmente utilizadas para evaluar el rendimiento de un modelo de clasificación son:

- **Accuracy:** proporción de instancias correctamente clasificadas entre todas las instancias del dataset.
- **Precision:** proporción de instancias correctamente clasificadas entre todas las instancias clasificadas como positivas.
- **Recall:** proporción de instancias correctamente clasificadas entre todas las instancias verdaderas positivas.
- **F1-Score:** media armónica entre Precision y Recall.

## Diapositiva 16. Métricas de Evaluación (Clasificación)

Interpretación geométrica de recall, precision y accuracy sobre la matriz de confusión.

![Áreas asociadas a recall, precision y accuracy](figures/clase-2/slide-16.png)

## Diapositiva 17. Métricas de Evaluación (Clasificación)

Ejemplo de matriz de confusión y conjunto de puntos reales/predichos.

![Matriz de confusión y ejemplo de predicciones](figures/clase-2/slide-17.png)

## Diapositiva 18. Métricas de Evaluación (Clasificación)

Ejemplo numérico:

$$
\text{precision} = \frac{2}{9}, \qquad
\text{recall} = \frac{2}{6}, \qquad
\text{accuracy} = \frac{6}{18}
$$

![Ejemplo numérico para precision, recall y accuracy](figures/clase-2/slide-18.png)

## Diapositiva 19. Métricas de Evaluación (Clasificación)

Resumen visual de las métricas:

$$
\text{accuracy} = \frac{T}{P + N}
$$

$$
\text{precision} = \frac{TP}{\text{predicted P}}
$$

$$
\text{recall} = \frac{TP}{P}
$$

![Resumen visual de accuracy, precision y recall](figures/clase-2/slide-19.png)

## Diapositiva 20. ROC Curve y AUC

Para clasificadores probabilísticos, variamos el umbral de decisión.

- **ROC Curve:** TPR vs. FPR.
- **AUC (Area Under Curve):** mide la capacidad del modelo para clasificar.
- $AUC = 0.5$: asignación aleatoria.
- $AUC = 1.0$: clasificador perfecto.
- $AUC \sim 1.0$: clasificador muy bueno.
- $AUC \sim -1.0$: anti-clasificador.

![Curva ROC y AUC](figures/clase-2/fig-20.png)

## Diapositiva 21. Introducción a la Teoría de Decisión Bayesiana

**Sección:** Introducción a la Teoría de Decisión Bayesiana.

## Diapositiva 22. Introducción: El Enfoque Estadístico

Ya sabemos cómo medir el desempeño de un modelo en datos empíricos, pero esas métricas no son deterministas.

Ahora veamos cómo decidir. Para eso vamos a suponer que conocemos las distribuciones involucradas.

## Diapositiva 23. Introducción: El Enfoque Estadístico

La **Teoría de Decisión Bayesiana** es el enfoque estadístico fundamental para la clasificación de patrones.

- Asumimos que la tarea de decisión se puede plantear en términos probabilísticos.
- Asumimos que todas las probabilidades relevantes son conocidas o estimables.
- **Objetivo:** minimizar el costo esperado de nuestras decisiones, por ejemplo el error de clasificación.

## Diapositiva 24. Definiciones Básicas

Sea

$$
\Omega = \{\omega_1, \ldots, \omega_c\}
$$

el conjunto de **estados de la naturaleza** (clases), y sea $\mathcal{X}$ el espacio de características (*feature space*).

- $\omega$: la clase verdadera, por ejemplo $\omega_1 = \text{Salmón}$, $\omega_2 = \text{Sea Bass}$.
- $x$: el vector de características observado, continuo o discreto.
- Nuestra meta es construir una regla de decisión $\alpha(x)$ que mapee cada $x \in \mathcal{X}$ a una clase $\omega_j$.

![Esquema de regla de decisión sobre el espacio de características](figures/clase-2/fig-24.png)

## Diapositiva 25. Definiciones Básicas

Debemos preguntarnos:

- ¿Cuántas clases?
- ¿Cuántas variables?
- ¿Qué distribuciones?
- ¿Qué quiero optimizar?

Y encontrar:

- ¿Cómo decido la clase?
- ¿Cómo mido el impacto de la decisión?

## Diapositiva 26. Definiciones Básicas

Caso del clasificador de spam:

- clases: spam / ham
- variables: cantidad de palabras y tiene/no tiene link
- distribuciones: ?
- objetivo: ¿aciertos?, ¿menos spam?, ¿perder menos plata?

## Diapositiva 27. Clasificación de pescados

Escenario ilustrativo para el problema de clasificación de pescados.

![Foto de salmón y lubina en una línea de procesamiento](figures/clase-2/slide-27.png)

## Diapositiva 28. Clasificación de pescados

Histogramas de variables observadas para salmón y *sea bass*.

![Histogramas de largo y luminosidad por clase](figures/clase-2/slide-28.png)

## Diapositiva 29. Clasificación de pescados

Comparación entre una frontera lineal simple y una frontera más compleja.

![Fronteras de decisión para salmón y sea bass](figures/clase-2/slide-29.png)

## Diapositiva 30. Clasificación de pescados

Caso del clasificador de pescados:

- clases: salmón / lubina
- variables: largo y luminosidad
- distribuciones: observadas
- objetivo: ¿aciertos?, ¿costo?

## Diapositiva 31. Clasificación de pescados

Un "naive classifier" sería decir que da lo mismo y que las chances de que sea salmón son del 50%.

Pero observamos que la frecuencia con la que aparece un salmón es diferente de la frecuencia con la que aparece una lubina.

![Ejemplo visual de frecuencia distinta entre clases](figures/clase-2/slide-31.png)

## Diapositiva 32. Caso 1: Priors

La **Prior Probability** $P(\omega_j)$ refleja nuestro conocimiento sobre qué tan probable es observar la clase $\omega_j$ antes de ver cualquier dato $x$.

Deben satisfacer:

$$
P(\omega_j) \ge 0
$$

$$
\sum_{j=1}^{c} P(\omega_j) = 1
$$

**Regla de decisión**

Decidir $\omega_1$ si $P(\omega_1) > P(\omega_2)$; si no, $\omega_2$.

## Diapositiva 33. Caso 1: Priors

Problema: esta regla ignora los datos actuales $x$. Siempre predice la clase mayoritaria.

![Ilustración del problema de decidir solo con priors](figures/clase-2/slide-33.png)

## Diapositiva 34. Caso 1: Probabilidad de Error

Al tomar la decisión, podemos equivocarnos.

Para el caso 1 (2 clases):

- decido por $\omega_i$ si $P(\omega_i) > P(\omega_j)$
- pero ocurrirá $\omega_j$ con probabilidad $P(\omega_j)$

Entonces:

- si $P(\omega_1) > P(\omega_2)$, elijo $\omega_1$ pero me puedo equivocar con probabilidad $P(\omega_2)$
- si $P(\omega_2) > P(\omega_1)$, elijo $\omega_2$ pero me puedo equivocar con probabilidad $P(\omega_1)$

$$
P(\text{error}) = \min\bigl(P(\omega_1), P(\omega_2)\bigr)
$$

Si son más de 2 clases:

$$
\text{decidir } \omega_i \text{ si } P(\omega_i) > P(\omega_j) \quad \forall j \ne i
$$

Pero el estado puede ser distinto de $\omega_i$ con probabilidad $1 - P(\omega_i)$.

## Diapositiva 35. Caso 2: Likelihood

La **Class-Conditional Density** o *Likelihood* $p(x \mid \omega_j)$ describe la distribución de los datos dentro de cada clase.

$$
p(x \mid \omega_j)
$$

- Es la densidad de probabilidad de observar el vector de características $x$ dado que la clase verdadera es $\omega_j$.
- En modelos generativos, modelamos explícitamente esta distribución, por ejemplo asumiendo que es Gaussiana.

Intuitivamente, elegimos el dato más probable.

**Regla de decisión**

Decidir $\omega_1$ si $p(x \mid \omega_1) > p(x \mid \omega_2)$; si no, $\omega_2$.

Para más de dos clases:

$$
\text{decidir } \omega_i \text{ si } p(x \mid \omega_i) > p(x \mid \omega_j) \quad \forall j \ne i
$$

## Diapositiva 36. Caso 2: Likelihood

Problema: este criterio no tiene en cuenta el conocimiento previo.

![Ejemplo visual del criterio de máximo likelihood](figures/clase-2/slide-36.png)

## Diapositiva 37. Caso 2: Probabilidad de Error

Para el caso 2 (2 clases):

$$
\text{decidir } \omega_i \text{ si } p(x \mid \omega_i) > p(x \mid \omega_j)
$$

$$
P(\text{error}) = \min\bigl(p(x \mid \omega_i), p(x \mid \omega_j)\bigr)
$$

Si son más de 2 clases:

$$
\text{decidir } \omega_i \text{ si } p(x \mid \omega_i) > p(x \mid \omega_j) \quad \forall j \ne i
$$

Pero el estado puede ser distinto de $\omega_i$ con probabilidad $1 - p(x \mid \omega_i)$. O sea que:

$$
P(\text{error} \mid x) = 1 - \max_i p(x \mid \omega_i)
$$

## Diapositiva 38. Teorema de Bayes

Queremos la probabilidad de que la clase sea $\omega_j$ dado que observamos $x$. Esto es la **Posterior Probability**.

Usando la regla de Bayes:

$$
P(\omega_j \mid x) = \frac{p(x \mid \omega_j) P(\omega_j)}{p(x)}
$$

Donde:

- $P(\omega_j \mid x)$: **Posterior** (lo que queremos).
- $p(x \mid \omega_j)$: **Likelihood** (del modelo).
- $P(\omega_j)$: **Prior** (del dominio).
- $p(x) = \sum_{j=1}^{c} p(x \mid \omega_j) P(\omega_j)$: **Evidence** (factor de normalización).

## Diapositiva 39. Caso 3: La Regla de Decisión de Bayes

Intuitivamente, elegimos la clase más probable dado el dato.

$$
\text{decidir } \omega_i \iff P(\omega_i \mid x) > P(\omega_j \mid x) \quad \forall j \ne i
$$

Dado que el denominador $p(x)$ es positivo e igual para todas las clases, podemos ignorarlo al maximizar.

**Regla de decisión**

$$
\text{decidir } \omega_i \iff p(x \mid \omega_i) P(\omega_i) > p(x \mid \omega_j) P(\omega_j)
$$

Esto divide el espacio $\mathcal{X}$ en regiones de decisión $\mathcal{R}_1, \ldots, \mathcal{R}_c$.

![Regiones de decisión inducidas por la regla de Bayes](figures/clase-2/fig-39.png)

## Diapositiva 40. Probabilidad de Error

Veamos el error para el caso binario (2 clases). Definimos la probabilidad de error dado un $x$ particular como:

$$
P(\text{error} \mid x) = \min\bigl(P(\omega_1 \mid x), P(\omega_2 \mid x)\bigr)
$$

El error promedio total es:

$$
P(\text{error}) = \int_{-\infty}^{\infty} P(\text{error} \mid x)\, p(x)\, dx
$$

**Teorema:** la regla de decisión de Bayes minimiza $P(\text{error})$. No existe ninguna otra regla que produzca un error menor, dadas las mismas distribuciones verdaderas.

## Diapositiva 41. Minimización del error

Sea un problema de clasificación con clases $\{\omega_1, \ldots, \omega_c\}$. La probabilidad de error condicional al observar un vector de características $x$ y elegir la clase $\omega_i$ se define como:

$$
P(\text{error} \mid x) = 1 - P(\omega_i \mid x) \tag{1}
$$

Para minimizar este error para cada valor de $x$, debemos elegir la clase que maximice la probabilidad a posteriori $P(\omega_i \mid x)$. La regla de decisión de Bayes selecciona la clase $\omega_j$ tal que:

$$
P(\omega_j \mid x) = \max_{i = 1, \ldots, c} P(\omega_i \mid x) \tag{2}
$$

La probabilidad de error total $P(\text{error})$ se obtiene integrando el error condicional sobre el espacio de características:

$$
P(\text{error}) = \int P(\text{error} \mid x)\, p(x)\, dx \tag{3}
$$

## Diapositiva 42. Minimización del error

Dado que la regla de Bayes minimiza el integrando $P(\text{error} \mid x)$ para cada punto $x$, la integral total resultante será mínima. Si $P_B(\text{error} \mid x)$ es el error de Bayes y $P_A(\text{error} \mid x)$ es el error de cualquier otra regla arbitraria $A$, se cumple que:

$$
P_B(\text{error} \mid x) \le P_A(\text{error} \mid x) \quad \forall x \tag{4}
$$

Integrando sobre todo el espacio:

$$
\int P_B(\text{error} \mid x)\, p(x)\, dx \le \int P_A(\text{error} \mid x)\, p(x)\, dx \tag{5}
$$

Por lo tanto:

$$
P(\text{error})_{\text{Bayes}} \le P(\text{error})_A
$$

## Diapositiva 43. Visualización del Error

El área bajo la curva de la mínima posterior representa el **Bayes Error Rate**.

- Es el error irreducible inherente a la superposición de las clases.
- Si las clases están perfectamente separadas, el error de Bayes es 0.

![Visualización del Bayes Error Rate](figures/clase-2/slide-43.png)

## Diapositiva 44. Más allá del Error: Loss Function

Minimizar el número de errores no siempre es el objetivo.

**Ejemplo médico**

- Clasificar un paciente sano como enfermo (falso positivo) implica molestia y más tests.
- Clasificar un paciente enfermo como sano (falso negativo) implica muerte.

Introducimos una función de pérdida $\lambda(\alpha_i \mid \omega_j)$: el costo de tomar la acción $\alpha_i$ cuando el estado real es $\omega_j$.

## Diapositiva 45. Conditional Risk

El **riesgo condicional** (o pérdida esperada) de tomar la acción $\alpha_i$ dado $x$ es:

$$
R(\alpha_i \mid x) = \sum_{j = 1}^{c} \lambda(\alpha_i \mid \omega_j) P(\omega_j \mid x)
$$

- Sumamos sobre todos los posibles estados verdaderos $\omega_j$.
- Ponderamos el costo $\lambda$ por la probabilidad posterior del estado.

## Diapositiva 46. Caso 4: Bayes Risk

Nuestra nueva regla de decisión es minimizar el riesgo.

**Minimum-Risk Decision Rule**

Seleccionar la acción $\alpha_i$ tal que $R(\alpha_i \mid x)$ sea mínimo.

El riesgo total del sistema (**Bayes Risk**) es la integral del riesgo condicional mínimo sobre todo $x$:

$$
R = \int R\bigl(\alpha(x) \mid x\bigr) p(x)\, dx
$$

El riesgo de Bayes es el mejor rendimiento posible para un problema dado.

![Ilustración del riesgo de Bayes](figures/clase-2/fig-46.png)

## Diapositiva 47. Caso Especial: Zero-One Loss

Ilustración del riesgo condicional bajo pérdida cero-uno.

![Riesgo condicional con zero-one loss](figures/clase-2/slide-47.png)

## Diapositiva 48. Caso Especial: Zero-One Loss

Si definimos la pérdida simétrica estándar:

$$
\lambda(\alpha_i \mid \omega_j) =
\begin{cases}
0 & \text{si } i = j \text{ (Correcto)} \\
1 & \text{si } i \ne j \text{ (Error)}
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

Minimizar el riesgo equivale a maximizar la posterior $P(\omega_i \mid x)$.

Recuperamos así la regla de Bayes de mínimo error.

## Diapositiva 49. Likelihood Ratio Test

Para el caso de dos categorías con costos generales $\lambda_{ij}$:

$$
(\lambda_{21} - \lambda_{11}) P(\omega_1 \mid x) > (\lambda_{12} - \lambda_{22}) P(\omega_2 \mid x)
$$

Reescribiendo usando la regla de Bayes y likelihoods:

$$
\frac{p(x \mid \omega_1)}{p(x \mid \omega_2)}
>
\frac{\lambda_{12} - \lambda_{22}}{\lambda_{21} - \lambda_{11}}
\frac{P(\omega_2)}{P(\omega_1)}
$$

El término

$$
\frac{p(x \mid \omega_1)}{p(x \mid \omega_2)}
$$

es el **Likelihood Ratio**. El umbral depende de los priors y los costos.

## Diapositiva 50. Discriminant Functions

Es útil representar el clasificador como un conjunto de funciones $g_i(x)$, una para cada clase.

$$
\text{decidir } \omega_i \iff g_i(x) > g_j(x) \quad \forall j \ne i
$$

Para el clasificador de Bayes (mínimo error), elegimos:

$$
g_i(x) = P(\omega_i \mid x)
$$

O equivalentemente, y más comúnmente usado por estabilidad numérica:

$$
g_i(x) = \ln P(\omega_i \mid x) = \ln p(x \mid \omega_i) + \ln P(\omega_i)
$$

ignorando términos comunes.

## Diapositiva 51. Decision Surfaces

Las regiones de decisión están separadas por superficies donde los discriminantes son iguales:

$$
g_i(x) = g_j(x)
$$

Esta ecuación define la **Decision Boundary**.

Dependiendo de la forma de $g_i(x)$, estas fronteras pueden ser hiperplanos (lineales) o hipersuperficies cuadráticas.

## Diapositiva 52. The Gaussian (Normal) Density

La distribución más importante en ML y Estadística (*Central Limit Theorem*).

**Univariada:** $x \sim N(\mu, \sigma^2)$

$$
p(x) = \frac{1}{\sqrt{2\pi}\sigma}
\exp\left[
-\frac{1}{2}\left(\frac{x - \mu}{\sigma}\right)^2
\right]
$$

**Multivariada:** $x \in \mathbb{R}^d$, $x \sim N(\mu, \Sigma)$

$$
p(x) = \frac{1}{(2\pi)^{d/2} |\Sigma|^{1/2}}
\exp\left[
-\frac{1}{2}(x - \mu)^T \Sigma^{-1} (x - \mu)
\right]
$$

Donde $\mu$ es el vector media y $\Sigma$ es la matriz de covarianza $d \times d$.

## Diapositiva 53. Propiedades de la Matriz de Covarianza $\Sigma$

La matriz $\Sigma$ es simétrica y positiva semidefinida.

$$
\Sigma = E\bigl[(x - \mu)(x - \mu)^T\bigr]
$$

Sus determinantes y autovalores nos dan información sobre la "forma" de la nube de datos.

- **Diagonal:** variables no correlacionadas.
- **Esférica** ($\sigma^2 I$): varianza igual en todas direcciones.
- **Full:** correlación entre variables (elipsoides rotados).

## Diapositiva 54. Distancia de Mahalanobis

El exponente de la normal multivariada contiene el término:

$$
r^2 = (x - \mu)^T \Sigma^{-1} (x - \mu)
$$

Esta es la **Mahalanobis Distance** al cuadrado entre $x$ y $\mu$.

- Las superficies de densidad constante son hiperelipsoides donde $r^2 = \text{cte.}$
- A diferencia de la distancia euclídea, esta métrica tiene en cuenta la dispersión (varianza) de los datos en cada dirección.

## Diapositiva 55. Geometría de las Covarianzas

Casos geométricos de covarianzas:

- A) covarianzas iguales y esféricas
- B) covarianzas iguales pero no esféricas
- C) covarianzas diferentes

![Geometría de diferentes estructuras de covarianza](figures/clase-2/slide-55.png)

## Diapositiva 56. Whitening Transform

Podemos transformar cualquier distribución Gaussiana $N(\mu, \Sigma)$ en una normal estándar esférica $N(0, I)$ mediante una transformación lineal $A_w$.

$$
y = \Phi \Lambda^{-1/2} \Phi^T (x - \mu)
$$

Donde $\Phi$ y $\Lambda$ vienen de la eigendecomposition de $\Sigma$.

Esto es fundamental en preprocesamiento de datos (*Whitening*).

## Diapositiva 57. Discriminante Gaussiano General

Asumamos que $p(x \mid \omega_i) \sim N(\mu_i, \Sigma_i)$.

| Hipótesis | Descripción |
| --- | --- |
| Densidad condicional | Gaussiana: $p(x \mid \omega_i) \sim N(\mu_i, \Sigma_i)$ |
| Parámetros | $\mu_i$, $\Sigma_i$ conocidos o estimables |
| Variables | $x \in \mathbb{R}^d$ ($n$ variables) |

Tomando $g_i(x) = \ln p(x \mid \omega_i) + \ln P(\omega_i)$:

$$
g_i(x) =
-\frac{1}{2}(x - \mu_i)^T \Sigma_i^{-1}(x - \mu_i)
-\frac{d}{2}\ln(2\pi)
-\frac{1}{2}\ln |\Sigma_i|
+ \ln P(\omega_i)
$$

Eliminando el término constante $\frac{d}{2}\ln(2\pi)$, obtenemos una forma cuadrática:

$$
g_i(x) =
-\frac{1}{2}(x - \mu_i)^T \Sigma_i^{-1}(x - \mu_i)
-\frac{1}{2}\ln |\Sigma_i|
+ \ln P(\omega_i)
$$

## Diapositiva 58. Caso 5: Covarianzas iguales y esféricas

Asumimos $\Sigma_i = \sigma^2 I$ para todas las clases (independencia y misma varianza).

| Simplificación | Descripción |
| --- | --- |
| Covarianzas | $\Sigma_i = \sigma^2 I$ (iguales y esféricas) |
| Variables | Independientes, misma varianza $\sigma^2$ |
| Fronteras | Lineales |

El término cuadrático se simplifica a la distancia euclídea:

$$
(x - \mu_i)^T (\sigma^2 I)^{-1} (x - \mu_i) = \frac{1}{\sigma^2} \lVert x - \mu_i \rVert^2
$$

El discriminante queda (lineal):

$$
g_i(x) = -\frac{1}{2\sigma^2}\lVert x - \mu_i \rVert^2 + \ln P(\omega_i)
$$

Desarrollando el cuadrado y tirando términos constantes ($x^T x$):

$$
g_i(x) = \frac{1}{\sigma^2}\mu_i^T x - \frac{1}{2\sigma^2}\mu_i^T \mu_i + \ln P(\omega_i)
$$

**Resultado:** un clasificador lineal $(w^T x + w_0)$.

## Diapositiva 59. Geometría del Caso 1

Si los priors son iguales, $P(\omega_i) = P(\omega_j)$, la frontera de decisión es el **Perpendicular Bisector** (mediatriz) del segmento que une las medias $\mu_i$ y $\mu_j$.

Este es el clasificador de **Minimum Distance**. Simplemente asignamos $x$ a la media más cercana.

## Diapositiva 60. Case 6: Covarianzas iguales pero arbitrarias

Asumimos $\Sigma_i = \Sigma$ para todas las clases (misma forma y orientación, pero no necesariamente esférica).

| Simplificación | Descripción |
| --- | --- |
| Covarianzas | $\Sigma_i = \Sigma$ (iguales, arbitrarias) |
| Variables | Mismas correlaciones y varianzas |
| Fronteras | Lineales (LDA) |

El término cuadrático $x^T \Sigma^{-1} x$ es común a todas las clases y se cancela.

$$
g_i(x) = -\frac{1}{2}(x - \mu_i)^T \Sigma^{-1}(x - \mu_i) + \ln P(\omega_i)
$$

Linealizando:

$$
g_i(x) = (\Sigma^{-1}\mu_i)^T x - \frac{1}{2}\mu_i^T \Sigma^{-1}\mu_i + \ln P(\omega_i)
$$

**Resultado:** nuevamente un **Linear Discriminant Analysis (LDA)**. Las fronteras son hiperplanos, pero no necesariamente perpendiculares a la línea que une las medias; se ajustan por la covarianza.

## Diapositiva 61. Geometría del Caso 2

La decisión se basa en la **Mahalanobis Distance**.

$$
d_M^2 = (x - \mu_i)^T \Sigma^{-1} (x - \mu_i)
$$

Si los priors son iguales, asignamos $x$ a la clase con menor distancia de Mahalanobis a su media.

## Diapositiva 62. Case 7: Covarianzas Arbitrarias

Aquí $\Sigma_i \ne \Sigma_j$. Cada clase tiene su propia dispersión y orientación.

| Simplificación | Descripción |
| --- | --- |
| Covarianzas | $\Sigma_i$ arbitrarias (distintas) |
| Variables | Diferentes correlaciones y varianzas por clase |
| Fronteras | Cuadráticas (QDA) |

Los términos cuadráticos $x^T \Sigma_i^{-1} x$ no se cancelan.

$$
g_i(x) = x^T W_i x + w_i^T x + w_{i0}
$$

Donde:

$$
W_i = -\frac{1}{2}\Sigma_i^{-1}
$$

$$
w_i = \Sigma_i^{-1}\mu_i
$$

**Resultado:** un **Quadratic Discriminant Analysis (QDA)**. Las fronteras de decisión son hipersuperficies cuadráticas (hipérbolas, parábolas, elipses).

## Diapositiva 63. Ejemplo del Caso 3

Si una clase es muy compacta (varianza pequeña) y otra es muy dispersa, la frontera tenderá a rodear a la clase compacta.

Esto permite modelar relaciones complejas y no lineales, pero requiere estimar muchos más parámetros,

$$
\frac{d(d + 1)}{2}
$$

para cada matriz $\Sigma_i$, lo que aumenta el riesgo de *overfitting* si $N$ es pequeño.

## Diapositiva 64. Chernoff & Bhattacharyya Bounds

Calcular la probabilidad exacta de error en altas dimensiones implica integrales complejas. A veces preferimos cotas superiores (*upper bounds*).

Para dos Gaussianas:

$$
P(\text{error}) \le P(\omega_1)^s P(\omega_2)^{1-s} e^{-k(s)}
$$

Donde $k(s)$ es la distancia de Chernoff.

El caso especial $s = 1/2$ nos da la **Bhattacharyya Bound**, útil para *feature selection* (elegir *features* que maximicen esta distancia entre clases).

## Diapositiva 65. Caso 1: Información a Priori

Índice de casos:

- Información a Priori — diapositiva 32
- Modelo Generativo Simple — diapositiva 35
- Regla de Bayes (Mínimo Error) — diapositiva 39
- Riesgo de Bayes (Pérdida) — diapositiva 46
- Normales: $\Sigma_i = \sigma^2 I$ — diapositiva 58
- Normales: $\Sigma_i = \Sigma$ — diapositiva 60
- Normales: $\Sigma_i = \text{Cualquiera}$ — diapositiva 62

## Diapositiva 66. Caso 1: Información a Priori

Resumen del caso:

- **Variables ($x$):** 0
- **Clases ($\omega$):** 2 o más
- **Hipótesis:** no se observa el dato $x$; solo se conoce la probabilidad previa $P(\omega_j)$
- **¿Conozco Dist.?** parcial ($P(\omega)$)
- **Regla de Decisión:** decidir $\omega_1$ si $P(\omega_1) > P(\omega_2)$
- **Ver diapositiva:** 32

## Diapositiva 67. Caso 2: Modelo Generativo Simple

Resumen del caso:

- **Variables ($x$):** 1
- **Clases ($\omega$):** 2
- **Hipótesis:** se asume conocimiento de la verosimilitud $p(x \mid \omega_j)$ (caso mero vs. salmón)
- **¿Conozco Dist.?** sí ($p(x \mid \omega)$)
- **Regla de Decisión:** máximo a posteriori (MAP), $P(\omega_j \mid x)$
- **Ver diapositiva:** 35

## Diapositiva 68. Caso 3: Regla de Bayes (Mínimo Error)

Resumen del caso:

- **Variables ($x$):** $d$
- **Clases ($\omega$):** $c$
- **Hipótesis:** se busca minimizar la probabilidad de error total con costo de error uniforme
- **¿Conozco Dist.?** sí
- **Regla de Decisión:** decidir $\omega_i$ si $P(\omega_i \mid x) > P(\omega_j \mid x)$ para todo $j \ne i$
- **Ver diapositiva:** 39

## Diapositiva 69. Caso 4: Riesgo de Bayes (Pérdida)

Resumen del caso:

- **Variables ($x$):** $d$
- **Clases ($\omega$):** $c$
- **Hipótesis:** se introduce una matriz de pérdida $\lambda_{ij}$; permite acción de "rechazo"
- **¿Conozco Dist.?** sí
- **Regla de Decisión:** minimizar el riesgo condicional $R(\alpha_i \mid x)$
- **Ver diapositiva:** 46

## Diapositiva 70. Caso 5: Normales: $\Sigma_i = \sigma^2 I$

Resumen del caso:

- **Variables ($x$):** $d$
- **Clases ($\omega$):** $c$
- **Hipótesis:** varianzas iguales y variables independientes; fronteras lineales (hiperplanos)
- **¿Conozco Dist.?** sí (Normal)
- **Regla de Decisión:** distancia euclídea al centroide
- **Ver diapositiva:** 58

## Diapositiva 71. Caso 6: Normales: $\Sigma_i = \Sigma$

Resumen del caso:

- **Variables ($x$):** $d$
- **Clases ($\omega$):** $c$
- **Hipótesis:** matrices de covarianza idénticas para todas las clases; fronteras lineales
- **¿Conozco Dist.?** sí (Normal)
- **Regla de Decisión:** distancia de Mahalanobis
- **Ver diapositiva:** 60

## Diapositiva 72. Caso 7: Normales: $\Sigma_i = \text{Cualquiera}$

Resumen del caso:

- **Variables ($x$):** $d$
- **Clases ($\omega$):** $c$
- **Hipótesis:** caso general; las covarianzas difieren por clase; fronteras cuadráticas
- **¿Conozco Dist.?** sí (Normal)
- **Regla de Decisión:** clasificador cuadrático (gaussiano general)
- **Ver diapositiva:** 62
