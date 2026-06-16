---
title: "Estimación de Parámetros: Estimación Bayesiana"
---

## Diapositiva 1

**Portada**

- Clase 4
- FaMAF
- 2026-03-31

## Diapositiva 2. Roadmap de la Clase

La clase se organiza en dos grandes bloques:

- **Estimación Paramétrica Bayesiana:** repaso de MLE, estimación bayesiana y ejemplos con distribuciones normales.
- **Problemas de Dimensionalidad:** dificultades estadísticas y computacionales al crecer la dimensión.

## Diapositiva 3. Roadmap de la Clase

Diagrama conceptual del curso de decisión bayesiana:

- Tomar decisiones óptimas a partir de `priors` $P(\omega_i)$ y probabilidades condicionales de clase $P(x \mid \omega_i)$.
- Los datos $x$ llegan con incertidumbre.
- Enfoque generativo: maximizar la probabilidad posterior $P(\omega_i \mid x)$ para modelar probabilidades.
- Enfoque discriminativo: usar funciones discriminantes $g_i(x)$ para modelar la frontera de decisión.
- El modelado involucra supuestos de independencia o gaussianidad, estimación de parámetros o distribuciones, optimización de verosimilitud o error y elección de la forma de la frontera de decisión.

![Roadmap conceptual entre enfoques generativo y discriminativo](figures/clase-4/fig-03-roadmap.png)

## Diapositiva 4. Modelo físico de Kelvin

El Sol emite energía constantemente. La pregunta es cuánto tiempo puede sostener ese brillo si la fuente de energía fuera solo la contracción gravitacional.

Supuesto físico:

$$
E \approx \frac{GM^2}{R}
$$

Luminosidad observada:

$$
L = \frac{dE}{dt}
$$

Tiempo de vida estimado:

$$
T \approx \frac{E}{L} \approx \frac{GM^2}{RL} \Longrightarrow T \sim 10^7 - 10^8 \text{ años}
$$

## Diapositiva 5. Tensión entre modelos

Contraste visual entre dos explicaciones incompatibles para la edad del Sol o de la Tierra:

- **Física:** $T \sim 10^7$ años.
- **Geología:** $T \gg 10^8$ años.

![Contraste entre la predicción física y la evidencia geológica](figures/clase-4/fig-05-tension-modelos.png)

## Diapositiva 6. The Likelihood Function

Supongamos que la probabilidad $p(x \mid \omega)$ puede modelarse con un modelo paramétrico $M$ con parámetros $\theta$:

$$
p(x \mid \omega) \sim p(x \mid \theta; M)
$$

Sea $D = \{x_1, \ldots, x_n\}$ un conjunto de muestras i.i.d. extraídas de $p(x \mid \theta)$. La probabilidad conjunta de observar $D$ dado $\theta$ es:

$$
p(D \mid \theta) = \prod_{k=1}^n p(x_k \mid \theta)
$$

Definimos el log-likelihood:

$$
L(\theta) = \ln p(D \mid \theta) = \sum_{k=1}^n \ln p(x_k \mid \theta)
$$

## Diapositiva 7. Enfoque de Maximum Likelihood

El estimador de máxima verosimilitud es el valor del parámetro que maximiza el log-likelihood:

$$
\hat{\theta}_{ML} = \arg\max_{\theta} L(\theta)
$$

Equivalentemente,

$$
\hat{\theta}_{ML} = \arg\max_{\theta} P(D \mid \theta, M)
$$

Interpretación:

- $D$: datos observados.
- $\theta$: parámetros del modelo, por ejemplo edad u otras magnitudes físicas.
- $M$: modelo físico adoptado.

El resultado depende del modelo $M$.

## Diapositiva 8. El conflicto

La física usa un modelo $M_1$ y la geología usa un modelo $M_2$, por lo que:

$$
\hat{\theta}_{ML}^{(1)} \ne \hat{\theta}_{ML}^{(2)}
$$

Ambos modelos parecen razonables, pero no pueden tener razón al mismo tiempo. Al introducir una nueva fuente de energía:

$$
T \sim 10^9 \text{ años}
$$

Conclusiones de la diapositiva:

- Maximum Likelihood puede fallar si el modelo es incorrecto.
- $\hat{\theta}_{ML}$ depende críticamente de $M$.
- Una buena estimación debe contemplar la incertidumbre en los datos.
- También debe contemplar la incertidumbre en el modelo y cualquier otra fuente adicional de información.

## Diapositiva 9. Estimación Paramétrica Bayesiana

**Sección:** repaso de MLE, estimación bayesiana y ejemplos.

## Diapositiva 10. Maximum Likelihood vs. Bayesian Estimation

Dentro del mundo paramétrico, la diapositiva distingue dos escuelas principales:

1. **Maximum Likelihood Estimation (MLE):** asume que el parámetro $\theta$ es fijo pero desconocido, y busca el valor $\hat{\theta}$ que maximiza la probabilidad de observar los datos $D$.
2. **Bayesian Estimation:** asume que $\theta$ es una variable aleatoria con distribución a priori $p(\theta)$ y calcula la posterior $p(\theta \mid D)$.

Ideas centrales:

- ML considera a $\theta$ como fijo.
- Bayes considera a $\theta$ como una variable aleatoria.
- Los datos transforman un prior $p(\theta)$ en un posterior $p(\theta \mid D)$.
- Cuando $n \to \infty$, el posterior típicamente se concentra alrededor del valor verdadero.

## Diapositiva 11. Comparación

Comparación resumida entre los dos enfoques:

- **Maximum Likelihood:** $\hat{\theta} = \arg\max_{\theta} P(D \mid \theta)$.
- **Maximum Likelihood:** entrega una única respuesta y puede ser sobreconfiado.
- **Bayes:** produce $p(\theta \mid D)$.
- **Bayes:** entrega una distribución y representa explícitamente la incertidumbre.

## Diapositiva 12. Estimación Bayesiana

Por el teorema de Bayes:

$$
P(\omega_i \mid x) =
\frac{p(x \mid \omega_i)P(\omega_i)}{\sum_{j=1}^c p(x \mid \omega_j)P(\omega_j)}
$$

La diapositiva plantea la pregunta clave: ¿cómo proceder cuando no conocemos las cantidades necesarias?

- $p(x \mid \omega_i)$
- $P(\omega_i)$

Para resolver la ecuación debemos explicitar simplificaciones, hipótesis o aproximaciones.

## Diapositiva 13. Enfoque Bayesiano

En lugar de fijar un único modelo, el enfoque bayesiano hace explícita la dependencia en el modelo:

$$
P(\theta, M \mid D) \propto P(D \mid \theta, M)\,P(\theta \mid M)\,P(M)
$$

De esta forma:

- se consideran múltiples modelos;
- se incorpora conocimiento previo;
- se mantiene la incertidumbre.

## Diapositiva 14. Comparación

La diapositiva resume varias rutas de modelado:

- **Maximum Likelihood:** modela $P(x \mid \omega)$ mediante $p(x \mid \theta)$ y usa estimación puntual de parámetros.
- **Bayesian estimation:** trabaja con posterior, densidad predictiva y parámetros tratados como variables aleatorias.
- **Datos incompletos:** introduce variables latentes y el algoritmo EM.
- **Simplificación gaussiana:** covarianza igual implica LDA; covarianza distinta implica QDA.
- **Simplificación de dependencias:** las redes de creencias modelan dependencias; Naive Bayes asume independencia.

![Esquema comparativo entre ML, Bayes, EM, LDA, QDA y Naive Bayes](figures/clase-4/fig-14-comparacion.png)

## Diapositiva 15. Marco Conceptual

En el aprendizaje bayesiano, el vector de parámetros $\theta$ se trata como una variable aleatoria en lugar de un valor fijo.

Objetivo de clasificación:

$$
P(\omega_i \mid x, D) =
\frac{p(x \mid \omega_i, D_i)P(\omega_i)}{\sum_{j=1}^c p(x \mid \omega_j, D_j)P(\omega_j)}
$$

La diapositiva destaca:

- **Objetivo:** calcular las probabilidades a posteriori usando toda la información disponible.
- **Aprendizaje supervisado:** las muestras en $D_i$ solo influyen en la densidad de la clase $\omega_i$, lo que permite tratar las clases de forma independiente.

## Diapositiva 16. .e.g.: Métodos numéricos

Cuando la integral bayesiana es difícil de calcular, se proponen métodos numéricos como:

- muestreo de Monte Carlo;
- *Variational Inference*;
- aproximación de Laplace.

La figura ilustra una dinámica tipo aceptar/rechazar en una secuencia de propuestas.

![Esquema de actualización numérica con aceptación y rechazo](figures/clase-4/fig-16-metodos-numericos.png)

## Diapositiva 17. Densidades condicionales de clase

Otro enfoque más analítico consiste en extraer información directamente de los datos
$D = \{x_1, x_2, \ldots, x_n\}$.

En el problema supervisado, sabemos que los datos $D_i$ provienen de la clase $\omega_i$, y buscamos:

$$
P(\omega_i \mid x, D) =
\frac{p(x \mid \omega_i, D_i)P(\omega_i)}{\sum_{j=1}^c p(x \mid \omega_j, D_j)P(\omega_j)}
$$

Simplificaciones explícitas:

1. Las probabilidades a priori $P(\omega_i)$ son conocidas, es decir, $P(\omega_i) = P(\omega_i \mid D)$.
2. Independencia: $D_i$ solo afecta la densidad de la clase $\omega_i$.

La estrategia concreta dependerá del tipo y la complejidad del problema.

## Diapositiva 18. Modelos paramétricos

Tercera simplificación:

- asumimos que el modelo es paramétrico, con parámetros $\theta$;
- existe una distribución desconocida $p(x)$, y usamos los datos $D$ para estimarla mediante $p(x \mid D)$;
- se asume que la distribución pertenece a una familia paramétrica, por lo que la incertidumbre queda concentrada en los parámetros;
- una vez fijado $p(x \mid \theta)$, toda la incertidumbre se traslada a $\theta$;
- la evidencia permite concluir que algunos valores de $\theta$ son más razonables que otros.

## Diapositiva 19. .e.g.: Distrib. normal, caso univariado

Suposiciones del ejemplo:

1. $p(x \mid \mu) \sim N(\mu, \sigma^2)$ con $\sigma^2$ conocida.
2. El prior sobre la media es $p(\mu) \sim N(\mu_0, \sigma_0^2)$.

Observaciones:

- $\sigma^2$ es conocida, pero $\mu$ es desconocida.
- El posterior $p(\mu \mid D)$ es una densidad conjugada y permanece gaussiano.
- El prior expresa conocimiento previo sobre $\mu$.
- El objetivo es calcular $p(\mu \mid D)$ tras observar los datos.

## Diapositiva 20. .e.g.: Distrib. normal, caso univariado

Usando la regla de Bayes y la independencia de las muestras:

$$
p(\mu \mid D) =
\frac{p(D \mid \mu)p(\mu)}{\int p(D \mid \mu)p(\mu)\,d\mu}
=
\alpha \prod_{k=1}^n p(x_k \mid \mu)\,p(\mu)
$$

Como aparecen productos de exponenciales cuadráticas, el resultado adopta la forma:

$$
p(\mu \mid D) \propto
\exp\left[
-\frac{1}{2}
\left(
\sum_{k=1}^n \frac{(x_k - \mu)^2}{\sigma^2}
+
\frac{(\mu - \mu_0)^2}{\sigma_0^2}
\right)
\right]
$$

## Diapositiva 21. .e.g.: Distrib. normal, caso univariado

Al completar el cuadrado:

$$
p(\mu \mid D) \sim N(\mu_n, \sigma_n^2)
$$

Media posterior:

$$
\mu_n =
\frac{n\sigma_0^2}{n\sigma_0^2 + \sigma^2}\,\hat{\mu}_n
+
\frac{\sigma^2}{n\sigma_0^2 + \sigma^2}\,\mu_0
$$

Varianza posterior:

$$
\frac{1}{\sigma_n^2} = \frac{n}{\sigma^2} + \frac{1}{\sigma_0^2}
$$

Con

$$
\hat{\mu}_n = \frac{1}{n}\sum_{k=1}^n x_k
$$

Interpretación:

- $\mu_n$ es un promedio ponderado entre la evidencia observada y el prior.
- Si $n \to \infty$, entonces $\mu_n \to \hat{\mu}_n$.
- Si $n \to \infty$, entonces $\sigma_n^2 \to \sigma^2/n$.
- Si $\sigma_0^2 \gg \sigma^2$, el prior es vago y $\mu_n \approx \hat{\mu}_n$.
- La varianza posterior disminuye con cada nueva muestra.

## Diapositiva 22. .e.g.: Distrib. normal, caso univariado

Visualización de la jerarquía de estimación:

- **Prior:** $p(\mu) \sim N(\mu_0, \sigma_0^2)$.
- **Posterior:** $p(\mu \mid D) \sim N(\mu_n, \sigma_n^2)$.
- **Predictiva:** $p(x \mid D) \sim N(\mu_n, \sigma^2 + \sigma_n^2)$.

![Jerarquía prior-posterior-predictiva para la media gaussiana](figures/clase-4/fig-22-jerarquia-estimacion.png)

## Diapositiva 23. .e.g.: Distrib. normal, caso multivariado

Sea $x$ un vector de dimensión $d$. El modelo asume:

- verosimilitud $p(x \mid \mu) \sim N(\mu, \Sigma)$;
- prior $p(\mu) \sim N(\mu_0, \Sigma_0)$.

La matriz de covarianza $\Sigma$ se considera conocida y el objetivo es hallar la posterior $p(\mu \mid D)$ a partir de $n$ muestras.

Por conjugación gaussiana:

$$
p(\mu \mid D) \sim N(\mu_n, \Sigma_n)
$$

## Diapositiva 24. .e.g.: Distrib. normal, caso multivariado

La incertidumbre sobre $\mu$ se actualiza a través de matrices de precisión:

$$
\Sigma_n^{-1} = n\Sigma^{-1} + \Sigma_0^{-1}
$$

Interpretación:

- la precisión posterior es la suma de la precisión del prior y la precisión acumulada de las $n$ muestras;
- cuando $n \to \infty$, la precisión aumenta y el elipsoide de incertidumbre se contrae.

## Diapositiva 25. .e.g.: Distrib. normal, caso multivariado

El vector de medias posterior es un promedio matricial entre la media muestral y la media a priori:

$$
\mu_n =
\Sigma_0\left(\Sigma_0 + \frac{1}{n}\Sigma\right)^{-1}\hat{\mu}_n
+
\frac{1}{n}\Sigma\left(\Sigma_0 + \frac{1}{n}\Sigma\right)^{-1}\mu_0
$$

La media muestral es:

$$
\hat{\mu}_n = \frac{1}{n}\sum_{k=1}^n x_k
$$

Además:

- si $\Sigma_0 \to \infty$, entonces $\mu_n \to \hat{\mu}_n$;
- si $\Sigma_0 \to 0$, entonces $\mu_n \to \mu_0$.

## Diapositiva 26. .e.g.: Distrib. normal, caso multivariado

Para clasificar un nuevo punto $x$, integramos la incertidumbre sobre la media:

$$
p(x \mid D) = \int p(x \mid \mu)\,p(\mu \mid D)\,d\mu
$$

El resultado es otra normal:

$$
p(x \mid D) \sim N(\mu_n, \Sigma + \Sigma_n)
$$

La covarianza efectiva $\Sigma + \Sigma_n$ combina:

- el ruido inherente del proceso, representado por $\Sigma$;
- el error de estimación de la media, representado por $\Sigma_n$.

## Diapositiva 27. Generalización

La pregunta guía es:

- ¿cómo realizar la cuenta para cualquier distribución paramétrica?

## Diapositiva 28. La Distribución de Parámetros

Para encontrar la distribución desconocida $p(x)$, se integra sobre el espacio de parámetros:

$$
p(x \mid D) = \int p(x \mid \theta)\,p(\theta \mid D)\,d\theta
$$

Interpretación:

- esto promedia el modelo $p(x \mid \theta)$ usando la distribución posterior $p(\theta \mid D)$;
- si la posterior está muy concentrada, el resultado se aproxima al estimador ML;
- en general, resolver esta integral es una tarea difícil.

## Diapositiva 29. El Cambio de Paradigma

En estimación clásica se busca un único valor para $\theta$. En el enfoque bayesiano se admite explícitamente que $\theta$ no se conoce con certeza.

Definiciones clave:

- $D = \{x_1, \ldots, x_n\}$: datos observados.
- $\theta$: parámetros del modelo, vistos como variables aleatorias.
- $p(\theta)$: prior, es decir, lo que se cree antes de ver datos.
- $p(D \mid \theta)$: likelihood, o qué tan bien explica $\theta$ a los datos.

## Diapositiva 30. Paso 1: entrenamiento

El primer objetivo es actualizar la creencia sobre los parámetros usando la regla de Bayes:

$$
p(\theta \mid D) =
\frac{p(D \mid \theta)p(\theta)}{\int p(D \mid \theta)p(\theta)\,d\theta}
\tag{1}
$$

Interpretación:

- el numerador combina experiencia previa con evidencia observada;
- el denominador actúa como constante de normalización;
- el resultado no es un número sino una función de probabilidad sobre $\theta$.

## Diapositiva 31. Paso 2: predicción (densidad predictiva)

A diferencia de ML, no se usa un único "mejor" $\theta$, sino todos los posibles valores ponderados por su probabilidad posterior:

$$
p(x \mid D) = \int p(x \mid \theta)\,p(\theta \mid D)\,d\theta
\tag{2}
$$

Lectura conceptual:

- $p(x \mid \theta)$ es la opinión de un modelo específico;
- $p(\theta \mid D)$ es cuánto confiamos en ese modelo;
- la integral es un promedio ponderado de todas las realidades posibles.

Proceso en dos pasos:

1. aprender todos los parámetros;
2. predecir un dato nuevo a partir de los datos observados.

## Diapositiva 32. Objetivo Final: Decisión

Si debemos elegir una acción $\alpha$, evaluamos el riesgo bayesiano:

$$
R(\alpha \mid x, D) =
\sum_{j=1}^c \lambda(\alpha, \omega_j)P(\omega_j \mid x, D)
\tag{3}
$$

La diapositiva enfatiza:

1. $p(x \mid D)$ nos da la confianza real sobre el dato.
2. La teoría de decisión usa esa confianza para elegir la acción $\alpha$ que minimiza la pérdida esperada.

Conclusión: el objetivo final es encontrar la acción óptima bajo incertidumbre.

## Diapositiva 33. .e.g.: Estimación iterativa

La estimación bayesiana permite actualizaciones incrementales a medida que llegan nuevos datos
$D_n = \{x_1, \ldots, x_n\}$.

Regla recursiva:

$$
p(\theta \mid D_n) =
\frac{p(x_n \mid \theta)\,p(\theta \mid D_{n-1})}
{\int p(x_n \mid \theta)\,p(\theta \mid D_{n-1})\,d\theta}
$$

Comportamiento asintótico:

- el posterior de $n-1$ muestras se convierte en el prior para $x_n$;
- cuando $n \to \infty$, $p(\theta \mid D_n)$ típicamente converge a una delta de Dirac en el valor verdadero de $\theta$.

## Diapositiva 34. El Flujo de Decisión Bayesiano

La diapositiva organiza el razonamiento en cinco pasos:

1. **Decisión óptima:** el riesgo depende de la creencia actual sobre la clase.

$$
R(\alpha \mid x, D) =
\sum_{j=1}^c \lambda(\alpha, \omega_j)P(\omega_j \mid x, D)
$$

2. **Inferencia de clase:** la clase depende de qué tan bien predice cada modelo al nuevo dato.

$$
P(\omega_i \mid x, D) =
\frac{p(x \mid \omega_i, D)P(\omega_i)}{\sum_{j=1}^c p(x \mid \omega_j, D)P(\omega_j)}
$$

3. **Densidad predictiva:** se promedian todos los posibles parámetros según su posterior.

$$
p(x \mid \omega_i, D) = \int p(x \mid \theta_i)\,p(\theta_i \mid D)\,d\theta_i
$$

4. **Posterior de los parámetros:** se combinan prior y evidencia.

$$
p(\theta_i \mid D) =
\frac{p(D \mid \theta_i)p(\theta_i)}{\int p(D \mid \theta_i)p(\theta_i)\,d\theta_i}
$$

5. **Repetir:** el esquema se reutiliza cada vez que llega nueva información.

## Diapositiva 35. .e.g.: Gaussiana con priors

La diapositiva remite al cuaderno `gaussian_mean_mle_bayes_progressive.ipynb`, donde se muestra:

- una estimación progresiva de la media;
- la comparación entre MLE, posterior bayesiana y media verdadera;
- la evolución del error y de la incertidumbre al crecer $n$.

![Notebook con estimación progresiva de la media gaussiana](figures/clase-4/fig-35-gaussiana-priors.png)

## Diapositiva 36. .e.g.: Distribución uniforme

Se consideran muestras de una uniforme con límite superior desconocido:

$$
p(x \mid \theta) \sim U(0,\theta) =
\begin{cases}
\frac{1}{\theta}, & 0 \le x \le \theta, \\
0, & \text{en otro caso.}
\end{cases}
$$

Prior:

$$
p(\theta) \sim U(0,10)
$$

Se observa una secuencia de datos $D = \{x_1, x_2, \ldots, x_n\}$.

## Diapositiva 37. .e.g.: Distribución uniforme

Bajo Maximum Likelihood:

$$
p(D \mid \theta) = \prod_{k=1}^n p(x_k \mid \theta)
$$

Para que $p(x_k \mid \theta) > 0$, el parámetro debe satisfacer $\theta \ge \max(D)$. Como la verosimilitud contiene el factor $1/\theta^n$, el máximo se alcanza en el menor valor posible:

$$
\hat{\theta}_{ML} = \max(D) = \max\{x_1, \ldots, x_n\}
$$

La diapositiva remarca que este estimador es sesgado y subestima levemente el verdadero valor de $\theta$.

## Diapositiva 38. .e.g.: Distribución uniforme

Reformulación explícita del modelo:

Modelo de verosimilitud:

$$
p(x \mid \theta) =
\begin{cases}
\frac{1}{\theta}, & 0 \le x \le \theta, \\
0, & \text{en otro caso.}
\end{cases}
$$

Prior:

$$
p(\theta) =
\begin{cases}
\frac{1}{10}, & 0 \le \theta \le 10, \\
0, & \text{en otro caso.}
\end{cases}
$$

## Diapositiva 39. La Ecuación de Aprendizaje Bayesiano

Para actualizar la creencia sobre $\theta$ tras observar un único dato $D_1 = \{x\}$:

$$
p(\theta \mid D_1) =
\frac{p(x \mid \theta)p(\theta)}{\int p(x \mid \theta)p(\theta)\,d\theta}
\tag{4}
$$

Análisis del soporte:

1. El prior exige $\theta \in [0,10]$.
2. La verosimilitud exige $\theta \ge x$.

Por lo tanto:

- si $\theta < x$, la verosimilitud es cero;
- observar $x$ vuelve imposible cualquier valor $\theta < x$;
- en consecuencia, $p(\theta \mid D_1) = 0$ para todo $\theta < x$.

## Diapositiva 40. .e.g.: Distribución uniforme

En el rango válido $\theta \in [x,10]$:

$$
p(x \mid \theta)p(\theta) = \frac{1}{\theta}\cdot\frac{1}{10} = \frac{1}{10\theta}
\tag{5}
$$

La evidencia se obtiene integrando:

$$
\int_x^{10} \frac{1}{10\theta}\,d\theta =
\frac{1}{10}\int_x^{10} \frac{1}{\theta}\,d\theta
\tag{6}
$$

Aplicando el teorema fundamental del cálculo:

$$
\frac{1}{10}\left[\ln(\theta)\right]_x^{10} =
\frac{1}{10}\ln\left(\frac{10}{x}\right)
\tag{7}
$$

![Soporte y forma del posterior para el caso uniforme](figures/clase-4/fig-40-posterior-uniforme.png)

## Diapositiva 41. .e.g.: Distribución uniforme

Combinando numerador y denominador:

$$
p(\theta \mid D_1) =
\begin{cases}
0, & 0 \le \theta < x, \\
\frac{1}{\theta \ln(10/x)}, & x \le \theta \le 10, \\
0, & \text{en otro caso.}
\end{cases}
\tag{8}
$$

Conclusiones:

- en $[0,x]$ la probabilidad es nula;
- en $[x,10]$ la densidad decrece como $1/\theta$;
- la moda queda exactamente en $x$;
- el soporte siempre es cero para $\theta < \max(D)$;
- con más datos, la forma cae como $1/\theta^n$ y converge asintóticamente hacia ML.

## Diapositiva 42. .e.g.: Distribución uniforme

La actualización recursiva del enfoque bayesiano es:

$$
p(\theta \mid D_n) \propto p(x_n \mid \theta)\,p(\theta \mid D_{n-1})
$$

Después de la primera muestra:

$$
p(\theta \mid x_1) \propto \frac{1}{\theta}\,\operatorname{Prior}(\theta),
\qquad \theta \ge x_1
$$

A medida que llegan más datos:

$$
p(\theta \mid D_n) \propto \frac{1}{\theta^n},
\qquad \theta \ge \max(D_n)
$$

## Diapositiva 43. .e.g.: Distribución uniforme

La densidad predictiva bayesiana se define por:

$$
p(x \mid D) = \int p(x \mid \theta)\,p(\theta \mid D)\,d\theta
$$

Para el caso uniforme con $n$ muestras:

$$
p(x \mid D) =
\frac{n}{n+1}\cdot \frac{1}{\max(D)},
\qquad x < \max(D)
$$

La diapositiva aclara que existe una corrección adicional para el área por encima del máximo observado.

Conclusión: el enfoque bayesiano admite formalmente que el verdadero $\theta$ puede ser mayor que cualquier dato visto hasta ese momento.

## Diapositiva 44. .e.g.: Distribución uniforme

La diapositiva remite al cuaderno `uniform_theta_recursive_bayes_learning.ipynb`, con:

- secuencia de observaciones;
- evolución del posterior sobre $\theta$;
- densidad predictiva $p(x \mid D_n)$;
- evolución de la media posterior, el MAP y la desviación estándar.

![Notebook con aprendizaje bayesiano recursivo para una uniforme](figures/clase-4/fig-44-uniforme-recursiva.png)

## Diapositiva 45. Máxima Verosimilitud vs. Bayes

| Característica | Máxima Verosimilitud | Estimación Bayesiana |
| --- | --- | --- |
| Concepto | $\theta$ fijo, desconocido | $\theta$ como variable aleatoria |
| Complejidad | Optimización menor | Integración mayor |
| Salida | Un único modelo "mejor" | Promedio ponderado de modelos |
| Tamaño de datos | Mejor para $n$ grande | Superior para $n$ pequeño |
| A priori | No usa prior explícito | Requiere $p(\theta)$ |

Observaciones adicionales:

- las soluciones ML suelen ser más fáciles de explicar porque entregan un único conjunto de parámetros;
- Bayes utiliza más información porque trabaja con la distribución completa $p(\theta \mid D)$.

## Diapositiva 46. Priors No Informativos

Cuando el conocimiento previo es vago, la diapositiva recomienda priors no informativos o planos.

Puntos destacados:

- el posterior $p(\theta \mid D)$ con prior uniforme coincide con la densidad kernel sin ponderación adicional del prior;
- un prior uniforme en una parametrización no necesariamente es uniforme en otra, por ejemplo entre $\theta$ y $\theta^2$;
- las estimaciones MAP son sensibles a cambios de coordenadas;
- la integración bayesiana completa es más robusta frente a esa dependencia de parametrización.

## Diapositiva 47. Problemas de Dimensionalidad

**Sección:** problemas de dimensionalidad.

## Diapositiva 48. Maldición de la Dimensionalidad

En problemas complejos aparece naturalmente el problema de la dimensionalidad:

- "más datos mejor" no siempre alcanza;
- es difícil tener muchas variables con información realmente independiente;
- más dimensiones implican mayor complejidad del modelo y mayor carga de cómputo;
- estimar una matriz de covarianza completa $\Sigma$ requiere $O(d^2)$ parámetros.

Si $d$ es grande y $n$ es pequeño:

- $\hat{\Sigma}$ será singular, es decir, no invertible;
- aparece sobreajuste masivo.

La pregunta final de la diapositiva es cómo reducir el número de parámetros.

## Diapositiva 49. .e.g.: Normal multivariada con independencia

En el caso más simple se asume un modelo normal multivariado con variables estadísticamente independientes, por lo que la covarianza es diagonal:

$$
\Sigma =
\begin{pmatrix}
\sigma_1^2 & 0 & \cdots & 0 \\
0 & \sigma_2^2 & \cdots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \cdots & \sigma_d^2
\end{pmatrix}
$$

Propiedades resultantes:

$$
|\Sigma| = \prod_{i=1}^d \sigma_i^2
$$

$$
\Sigma^{-1} = \operatorname{diag}\left(
\frac{1}{\sigma_1^2}, \ldots, \frac{1}{\sigma_d^2}
\right)
$$

## Diapositiva 50. Derivación de la Función de Discriminación

Partimos de la función discriminante para una distribución normal:

$$
g_j(x) =
-\frac{1}{2}(x - \mu_j)^t \Sigma_j^{-1}(x - \mu_j)
- \frac{d}{2}\ln(2\pi)
- \frac{1}{2}\ln |\Sigma_j|
+ \ln P(\omega_j)
\tag{9}
$$

La diapositiva muestra luego la expansión del término cuadrático
$(x - \mu_j)^t \Sigma_j^{-1}(x - \mu_j)$ en coordenadas.

## Diapositiva 51. Simplificación a Sumatoria

Como $\Sigma_j^{-1}$ solo tiene elementos no nulos en la diagonal:

$$
(x - \mu_j)^t \Sigma_j^{-1}(x - \mu_j) =
\sum_{i=1}^d \frac{(x_i - \mu_{ji})^2}{\sigma_{ji}^2}
\tag{10}
$$

Sustituyendo este resultado y usando
$\ln |\Sigma_j| = \sum_{i=1}^d \ln \sigma_{ji}^2$, se obtiene:

$$
g_j(x) =
-\frac{1}{2}\sum_{i=1}^d \frac{(x_i - \mu_{ji})^2}{\sigma_{ji}^2}
- \frac{1}{2}\sum_{i=1}^d \ln \sigma_{ji}^2
+ \ln P(\omega_j)
+ C
\tag{11}
$$

## Diapositiva 52. Resultado Final e Interpretación

Ignorando las constantes que no dependen de la clase:

$$
g_j(x) =
-\sum_{i=1}^d \frac{(x_i - \mu_{ji})^2}{\sigma_{ji}^2}
+ \text{términos de umbral}
\tag{12}
$$

Interpretación geométrica y estadística:

- las superficies de decisión son hiperelipsoides alineados con los ejes;
- cada característica $x_i$ se penaliza inversamente a su varianza $\sigma_i^2$;
- este es el fundamento del clasificador Naive Bayes para variables continuas.

## Diapositiva 53. Definición de Error Local

Para un valor observado $x$, el clasificador bayesiano decide la clase $\omega_i$ que maximiza la posterior.

La probabilidad de error condicional es:

$$
P(e \mid x) = 1 - P(\omega_{\max} \mid x)
\tag{13}
$$

donde $\omega_{\max}$ es la clase para la cual $P(\omega_i \mid x)$ es máxima.

## Diapositiva 54. Derivación de la Probabilidad de Error Total

La probabilidad de error promedio se obtiene integrando el error condicional en todo el espacio de características:

$$
P(e) =
\int_{\mathcal{R}} P(e,x)\,dx =
\int_{\mathcal{R}} P(e \mid x)p(x)\,dx
\tag{14}
$$

Para dos clases $\omega_1$ y $\omega_2$:

- si decidimos $\omega_1$, el error es $P(\omega_2 \mid x)$;
- si decidimos $\omega_2$, el error es $P(\omega_1 \mid x)$.

## Diapositiva 55. Regiones de Decisión

Se divide el espacio en $\mathcal{R}_1$ y $\mathcal{R}_2$:

$$
P(e) =
P(\omega_2)\int_{\mathcal{R}_1} p(x \mid \omega_2)\,dx
+
P(\omega_1)\int_{\mathcal{R}_2} p(x \mid \omega_1)\,dx
\tag{15}
$$

Interpretación:

- el primer término corresponde a ejemplos de $\omega_2$ que caen en la región asignada a $\omega_1$;
- el segundo término corresponde a ejemplos de $\omega_1$ que caen en la región asignada a $\omega_2$.

## Diapositiva 56. Interpretación en el Caso Gaussiano

Cuando las densidades son gaussianas $N(\mu, \sigma^2)$, el error es el área bajo las colas que cruza el umbral de decisión $x^*$.

La regla bayesiana minimiza esa integral al ubicar $x^*$ exactamente donde se cruzan las densidades a posteriori.

![Solapamiento entre dos gaussianas y umbral óptimo de decisión](figures/clase-4/fig-56-solapamiento-gaussiano.png)

## Diapositiva 57. La Distancia de Mahalanobis r

Para una normal $N(\mu, \Sigma)$, la distancia de Mahalanobis desde un punto $x$ a la media $\mu$ se define por:

$$
r^2 = (x - \mu)^t \Sigma^{-1}(x - \mu)
\tag{16}
$$

Interpretación:

- mide cuántas "desviaciones estándar" separan a $x$ de la media, considerando correlaciones;
- las superficies de equiprobabilidad son elipsoides donde $r$ es constante.

## Diapositiva 58. Transformación a una Variable Unidimensional

Para calcular $P(e)$ entre dos clases con la misma matriz de covarianza $\Sigma$, el problema multivariado puede proyectarse sobre la recta que une las medias.

La separación efectiva entre ambas clases se define como:

$$
r^2 = (\mu_1 - \mu_2)^t \Sigma^{-1}(\mu_1 - \mu_2)
\tag{17}
$$

Esta cantidad escalar resume la dificultad de separar las dos nubes de puntos.

## Diapositiva 59. Derivación de P(e) en función de r

Si $P(\omega_1) = P(\omega_2) = 0.5$ y $\Sigma_1 = \Sigma_2$, la probabilidad de error se reduce a la integral de una gaussiana estándar sobre la región de solapamiento:

$$
P(e) =
\int_{r/2}^{\infty}
\frac{1}{\sqrt{2\pi}}e^{-u^2/2}\,du
\tag{18}
$$

En términos de la función de distribución acumulada o de la función error complementaria:

$$
P(e) = 1 - \Phi\left(\frac{r}{2}\right)
= \frac{1}{2}\operatorname{erfc}\left(\frac{r}{2\sqrt{2}}\right)
\tag{19}
$$

## Diapositiva 60. Conclusiones Matemáticas

Conclusiones finales del bloque:

- **Dependencia inversa:** cuando la distancia de Mahalanobis $r$ aumenta, el error de Bayes $P(e)$ decrece exponencialmente.
- **Cota de error:** si $r = 0$, entonces $P(e) = 0.5$, equivalente a decidir al azar.
- **Significado físico:** la distancia $r$ normaliza el espacio; el error depende solo de esta distancia geométrica ponderada y no de la escala original de las variables.
