---
title: "Simplicidad y Datos Incompletos: Naive Bayes, Redes Bayesianas y Expectation-Maximization"
---

## Diapositiva 1

**Portada**

- Clase 5
- Data Science & Machine Learning
- FaMAF
- 2026-04-07

## Diapositiva 2. Roadmap de la Clase

La clase se organiza en tres bloques:

1. **Naive Bayes**
   - la maldición de la dimensionalidad;
   - clasificador de Naive Bayes;
   - ejemplos.
2. **Modelos Gráficos y Redes Bayesianas**
   - modelos gráficos;
   - ejemplos.
3. **Datos Faltantes y Variables Latentes**
   - motivaciones;
   - algoritmo EM;
   - ejemplos con gaussianas.

## Diapositiva 3. Naive Bayes

**Sección:** Naive Bayes.

## Diapositiva 4. Introducción

En la clase anterior se trabajó con inferencia bayesiana:

$$
P(\omega_i \mid x) = \frac{p(x \mid \omega_i)P(\omega_i)}{p(x)}
$$

El problema central pasa por especificar o estimar $p(x \mid \omega_i)$.

Estrategias ya vistas:

- asumir una forma paramétrica, por ejemplo gaussiana;
- esto funciona bien cuando hay muchos datos.

Cuando $d$ es grande o los datos están incompletos:

- los modelos complejos tienen demasiados parámetros;
- la estimación se vuelve inestable;
- la verosimilitud observada puede ser difícil de maximizar.

## Diapositiva 5. Dimensionalidad

En problemas relativamente complejos emerge naturalmente el problema de la dimensionalidad:

- "más datos mejor";
- es difícil tener muchas variables que aporten información independiente;
- más dimensiones implican mayor complejidad del modelo;
- más dimensiones implican mayor carga de cómputo.

Si $d$ es grande y $n$ es pequeño:

- $\hat{\Sigma}$ será singular;
- aparece sobreajuste masivo.

Además, estimar una matriz de covarianza completa $\Sigma$ requiere $O(d^2)$ parámetros.

## Diapositiva 6. Espectro electromagnético e imágenes hiperespectrales

La figura muestra:

- el espectro electromagnético y las regiones donde la atmósfera es opaca;
- el rango hiperespectral y la banda visible;
- una escena de ejemplo observada a distintas longitudes de onda.

![Espectro electromagnético, banda hiperespectral y escena de ejemplo](figures/clase-5/fig-06-spectrum.png)

## Diapositiva 7. Comparación entre modalidades de imagen

Comparación visual entre:

- imagen pancromática;
- imagen RGB;
- imagen multiespectral;
- imagen hiperespectral.

La idea es que, al aumentar la resolución espectral, aumenta la riqueza descriptiva pero también la dimensión del problema.

![Comparación entre imágenes pancromáticas, RGB, multiespectrales e hiperespectrales](figures/clase-5/fig-07-imaging-comparison.png)

## Diapositiva 8. Maldición de la Dimensionalidad

El término refiere a varios fenómenos relacionados con la cantidad de variables $d$:

- el volumen del espacio crece rápidamente;
- las muestras se vuelven relativamente escasas;
- las densidades locales son difíciles de estimar;
- aumenta la varianza de los estimadores paramétricos.

## Diapositiva 9. Cuando n es Pequeño Relativo a d

Sea la covarianza muestral:

$$
\hat{\Sigma} = \frac{1}{n}\sum_{k=1}^n (x_k - \hat{\mu})(x_k - \hat{\mu})^T
$$

Entonces:

- $\operatorname{rank}(\hat{\Sigma}) \le n - 1$;
- si $n \le d$, la matriz es necesariamente singular;
- el discriminante gaussiano completo no puede evaluarse de manera estable.

La diapositiva remarca que este es un problema matemático, no solo computacional.

## Diapositiva 10. Cuando d es grande

Si $x \in \mathbb{R}^d$ y cada clase $\omega_i$ se modela con una gaussiana multivariada:

$$
p(x \mid \omega_i) =
\frac{1}{(2\pi)^{d/2}|\Sigma_i|^{1/2}}
\exp\left[
-\frac{1}{2}(x-\mu_i)^T\Sigma_i^{-1}(x-\mu_i)
\right]
$$

Cantidad de parámetros:

- estimar $\mu_i$ requiere $d$ parámetros;
- estimar $\Sigma_i$ requiere $d(d+1)/2$ parámetros.

Ejemplos:

| $d$ | parámetros en $\mu$ | parámetros en $\Sigma$ |
| --- | --- | --- |
| 4 | 4 | 10 |
| 20 | 20 | 210 |
| 100 | 100 | 5050 |
| 1000 | 1000 | 500500 |

Si hay $c$ clases, el total crece como $O(cd^2)$: la dificultad práctica queda dominada por la covarianza.

## Diapositiva 11. Otros problemas de dimensionalidad

**Complejidad computacional**

- entrenamiento ML: calcular $\hat{\mu}$ cuesta $O(nd)$ y calcular $\hat{\Sigma}$ cuesta $O(nd^2)$;
- clasificación: evaluar la función discriminante de un punto de prueba cuesta $O(d^2)$.

**Sobreajuste y regularización**

- si $n$ es inadecuado respecto de $d$, el modelo puede ajustarse al ruido;
- una opción es encogimiento o regularización de covarianzas:

$$
\Sigma_i(\alpha) =
\frac{(1-\alpha)n_i\Sigma_i + \alpha n\Sigma}{(1-\alpha)n_i + \alpha n}
$$

Esto empuja las covarianzas de clase hacia una covarianza común, y $\alpha \in [0,1]$ controla el grado de regularización.

## Diapositiva 12. Sesgo, Varianza y Sobreajuste

Un modelo muy flexible puede aproximar mejor la distribución verdadera, pero también tiene mayor error de estimación.

En clasificación generativa:

- más parámetros reducen sesgo de modelado;
- pero aumentan la varianza de $\hat{\theta}$;
- con pocas muestras, el riesgo total puede empeorar.

Idea central: simplificar la familia de modelos puede mejorar la decisión final.

## Diapositiva 13. La Maldición de la Dimensionalidad: ¿Cómo reducimos el número de parámetros?

La clase propone analizar casos particulares:

- **esta clase**
  - variables latentes;
  - redes de dependencias;
  - suposición naive de independencia.
- **próxima clase**
  - eliminar variables;
  - transformar variables.

## Diapositiva 14. Objetivo: simplificar

A partir del análisis de las correlaciones entre variables, se plantean dos estrategias:

1. imponer estructura sobre $p(x \mid \omega)$, por ejemplo independencia condicional;
2. introducir variables latentes y optimizar indirectamente cuando faltan datos.

Pregunta guía: ¿cuándo conviene usar un modelo más expresivo y cuándo conviene imponer simplicidad para estimar mejor?

## Diapositiva 15. .e.g.: Normal multivariada con independencia

En el caso más simple, se asume un modelo normal multivariado con variables estadísticamente independientes, por lo que la covarianza es diagonal:

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
\Sigma^{-1} =
\operatorname{diag}\left(
\frac{1}{\sigma_1^2}, \ldots, \frac{1}{\sigma_d^2}
\right)
$$

## Diapositiva 16. .e.g.: Normal multivariada con independencia

Partimos de la función discriminante para una distribución normal:

$$
g_j(x) = \ln P(\omega_j \mid x) = \ln p(x \mid \omega_j) + \ln P(\omega_j)
$$

$$
g_j(x) =
-\frac{1}{2}(x-\mu_j)^T\Sigma_j^{-1}(x-\mu_j)
- \frac{d}{2}\ln(2\pi)
- \frac{1}{2}\ln |\Sigma_j|
+ \ln P(\omega_j)
\tag{1}
$$

La cantidad cuadrática se interpreta como distancia de Mahalanobis.

## Diapositiva 17. .e.g.: Normal multivariada con independencia

Como $\Sigma_j^{-1}$ solo tiene elementos no nulos en la diagonal:

$$
(x-\mu_j)^T\Sigma_j^{-1}(x-\mu_j) =
\sum_{i=1}^d \frac{(x_i-\mu_{ji})^2}{\sigma_{ji}^2}
\tag{2}
$$

Sustituyendo esto y usando
$\ln |\Sigma_j| = \sum_{i=1}^d \ln \sigma_{ji}^2$, se obtiene:

$$
g_j(x) =
-\frac{1}{2}\sum_{i=1}^d \frac{(x_i-\mu_{ji})^2}{\sigma_{ji}^2}
- \frac{1}{2}\sum_{i=1}^d \ln \sigma_{ji}^2
+ \ln P(\omega_j)
+ C
\tag{3}
$$

## Diapositiva 18. .e.g.: Normal multivariada con independencia

Ignorando las constantes que no dependen de la clase:

$$
g_j(x) =
-\sum_{i=1}^d \frac{(x_i-\mu_{ji})^2}{\sigma_{ji}^2}
+ \text{términos de umbral}
\tag{4}
$$

Interpretación:

- las superficies de decisión son hiperelipsoides alineados con los ejes;
- cada característica $x_i$ es penalizada inversamente por su varianza $\sigma_i^2$.

## Diapositiva 19. Probabilidad de Error Total

Para un valor observado $x$, el clasificador bayesiano decide la clase $\omega_i$ que maximiza la posterior.

Error condicional:

$$
P(e \mid x) = 1 - P(\omega_{\max} \mid x)
\tag{5}
$$

La probabilidad de error promedio se obtiene integrando sobre todo el espacio de características:

$$
P(e) =
\int_{\mathcal{R}} P(e,x)\,dx =
\int_{\mathcal{R}} P(e \mid x)p(x)\,dx
\tag{6}
$$

Para dos clases:

- si decidimos $\omega_1$, el error es $P(\omega_2 \mid x)$;
- si decidimos $\omega_2$, el error es $P(\omega_1 \mid x)$.

## Diapositiva 20. Probabilidad de Error Total

Dividiendo el espacio en $\mathcal{R}_1$ y $\mathcal{R}_2$:

$$
P(e) =
P(\omega_2)\int_{\mathcal{R}_1} p(x \mid \omega_2)\,dx
+
P(\omega_1)\int_{\mathcal{R}_2} p(x \mid \omega_1)\,dx
\tag{7}
$$

Interpretación:

- el primer término corresponde a falsos positivos;
- el segundo corresponde a falsos negativos.

## Diapositiva 21. Transformación a una Variable Unidimensional

Si ambas clases tienen la misma matriz de covarianza, el problema puede proyectarse sobre la recta que une las medias.

Separación efectiva:

$$
r^2 = (\mu_1-\mu_2)^T\Sigma^{-1}(\mu_1-\mu_2)
\tag{8}
$$

Si además $P(\omega_1)=P(\omega_2)=0.5$ y $\Sigma_1=\Sigma_2$:

$$
P(e) =
\int_{r/2}^{\infty}
\frac{1}{\sqrt{2\pi}}e^{-u^2/2}\,du
\tag{9}
$$

Equivalentemente:

$$
P(e) = 1 - \Phi\left(\frac{r}{2}\right)
= \frac{1}{2}\operatorname{erfc}\left(\frac{r}{2\sqrt{2}}\right)
\tag{10}
$$

## Diapositiva 22. .e.g.: Normal multivariada con independencia

Conclusiones:

- a medida que la distancia de Mahalanobis $r$ aumenta, el error de Bayes decrece;
- si $r=0$, entonces $P(e)=0.5$;
- el error depende de la distancia geométrica ponderada, no de la escala original.

Entonces:

- **promesa teórica:** si las variables son independientes, la tasa de error de Bayes puede tender a $0$ al crecer $d$ si también aumenta $r$;
- **realidad práctica:** con muestras finitas, agregar características puede empeorar el rendimiento por error de estimación.

## Diapositiva 23. Solución: Imponer Estructura

En lugar de estimar una covarianza completamente libre, se puede asumir:

- independencia condicional total;
- independencia condicional parcial;
- variables latentes que expliquen dependencia residual.

La simplificación de independencia condicional permite definir el clasificador **Naive Bayes**.

## Diapositiva 24. Naive Bayes

Cuando las relaciones de dependencia son desconocidas, se toma la suposición más simple: las características son condicionalmente independientes dada la categoría.

Fórmula fundamental:

$$
p(\omega_k \mid x) \propto \prod_{i=1}^d p(x_i \mid \omega_k)
\tag{11}
$$

A pesar de su simplicidad, este modelo funciona sorprendentemente bien en la práctica.

## Diapositiva 25. El Supuesto "Naive"

Se asume que $x_1,\ldots,x_d$ son condicionalmente independientes dada la clase $\omega_j$:

$$
p(x \mid \omega_j) = p(x_1,\ldots,x_d \mid \omega_j) = \prod_{k=1}^d p(x_k \mid \omega_j)
$$

Esto equivale a asumir covarianza diagonal:

$$
\Sigma_j =
\operatorname{diag}\left(
\sigma_{j1}^2, \sigma_{j2}^2, \ldots, \sigma_{jd}^2
\right)
$$

Ventaja: solo se estiman $d$ varianzas en lugar de $d(d+1)/2$ covarianzas.

Consecuencias:

- no se modelan covarianzas cruzadas;
- el número de parámetros cae drásticamente;
- el aprendizaje se desacopla coordenada por coordenada.

## Diapositiva 26. Supuesto Naive

La figura compara la distribución real correlacionada con la aproximación de Naive Bayes, que ignora la covarianza y usa solo las marginales.

![Comparación entre distribución real correlacionada y aproximación de Naive Bayes](figures/clase-5/fig-26-naive-ellipse.png)

## Diapositiva 27. Naive Bayes Discreto y Continuo

El modelo sirve tanto para variables continuas como discretas.

Caso continuo:

$$
p(x_k \mid \omega_j) =
\frac{1}{\sqrt{2\pi}\sigma_{jk}}
\exp\left[
-\frac{(x_k-\mu_{jk})^2}{2\sigma_{jk}^2}
\right]
$$

Caso discreto o multinomial:

$$
\hat{P}(x_k=\text{word}\mid \omega_j) =
\frac{\operatorname{Count}(\text{word},\omega_j)}
{\text{Total Words in }\omega_j}
$$

## Diapositiva 28. Fortalezas y Limitaciones

**Fortalezas**

- entrenamiento rápido;
- pocos parámetros;
- robustez sorprendente en alta dimensión.

**Limitaciones**

- no modela correlaciones importantes;
- las probabilidades posteriores pueden estar mal calibradas;
- el supuesto de independencia puede romperse sistemáticamente.

## Diapositiva 29. Clasificador Bayesiano

Bajo pérdida $0$-$1$, la regla óptima es:

$$
\delta^*(x) = \arg\max_j P(\omega_j \mid x)
= \arg\max_j p(x \mid \omega_j)P(\omega_j)
$$

El término $p(x)$ es común a todas las clases y no afecta la decisión.

Por lo tanto, el foco es modelar $p(x \mid \omega_j)$ de forma estadísticamente razonable.

## Diapositiva 30. Cuánto Ganamos

Una gaussiana completa por clase requiere:

$$
d + \frac{d(d+1)}{2}
$$

parámetros.

Una gaussiana diagonal por clase requiere:

$$
d + d = 2d
$$

parámetros.

En alta dimensión, la diferencia entre $O(d^2)$ y $O(d)$ cambia por completo el régimen estadístico del problema.

## Diapositiva 31. .e.g.: (Caso Continuo) Gaussian Naive Bayes

Si cada coordenada es gaussiana condicionalmente a la clase:

$$
p(x_k \mid \omega_j) =
\frac{1}{\sqrt{2\pi}\sigma_{jk}}
\exp\left[
-\frac{(x_k-\mu_{jk})^2}{2\sigma_{jk}^2}
\right]
$$

entonces la densidad conjunta es:

$$
p(x \mid \omega_j) = \prod_{k=1}^d p(x_k \mid \omega_j)
$$

Esto es equivalente a una gaussiana multivariada con covarianza diagonal.

## Diapositiva 32. .e.g.: (Caso Continuo) Gaussian Naive Bayes

Tomando logaritmos:

$$
g_j(x) = \ln P(\omega_j) + \sum_{k=1}^d \ln p(x_k \mid \omega_j)
$$

Sustituyendo la forma gaussiana:

$$
g_j(x) =
\ln P(\omega_j)
- \frac{1}{2}\sum_{k=1}^d \ln(2\pi \sigma_{jk}^2)
- \frac{1}{2}\sum_{k=1}^d \frac{(x_k-\mu_{jk})^2}{\sigma_{jk}^2}
$$

La clasificación elige $\arg\max_j g_j(x)$.

## Diapositiva 33. .e.g.: (Caso Continuo) Gaussian Naive Bayes

La contribución de cada coordenada es separable:

$$
-\frac{1}{2}\frac{(x_k-\mu_{jk})^2}{\sigma_{jk}^2}
$$

Por lo tanto:

- cada variable penaliza de manera independiente;
- las variables con gran varianza pesan menos;
- la geometría está dada por elipsoides alineados con los ejes.

Naive Bayes no elimina la geometría gaussiana: la simplifica.

## Diapositiva 34. .e.g.: (Caso Continuo) Gaussian Naive Bayes

Con datos etiquetados $D_j = \{x_1,\ldots,x_{n_j}\}$ para la clase $\omega_j$:

$$
\hat{\mu}_{jk} = \frac{1}{n_j}\sum_{x\in D_j} x_k
$$

$$
\hat{\sigma}_{jk}^2 = \frac{1}{n_j}\sum_{x\in D_j}(x_k-\hat{\mu}_{jk})^2
$$

También se estima la prior de clase:

$$
\hat{P}(\omega_j) = \frac{n_j}{n}
$$

El entrenamiento es lineal en $n$ y $d$.

## Diapositiva 35. .e.g.: (Caso Discreto) Multinomial Naive Bayes

Para documentos, cada texto se representa por conteos
$x=(x_1,\ldots,x_V)$, donde $V$ es el vocabulario y
$N=\sum_{k=1}^V x_k$.

Modelo multinomial:

$$
p(x \mid \omega_j) =
\frac{N!}{x_1!\cdots x_V!}
\prod_{k=1}^V \theta_{jk}^{x_k},
\qquad
\sum_{k=1}^V \theta_{jk} = 1
$$

Si $N_{jk}$ es la cantidad total de ocurrencias de la palabra $k$ en la clase $j$:

$$
\hat{\theta}_{jk}^{ML} =
\frac{N_{jk}}{\sum_{\ell=1}^V N_{j\ell}}
$$

El discriminante queda:

$$
g_j(x) = \ln P(\omega_j) + \sum_{k=1}^V x_k \ln \hat{\theta}_{jk} + \text{cte}(x)
$$

Esto explica por qué el clasificador es tan eficiente en texto.

## Diapositiva 36. .e.g.: (Caso Discreto) Multinomial Naive Bayes

El estimador ML tiene un problema: si $N_{jk}=0$, entonces $\hat{\theta}_{jk}=0$ y una sola palabra no observada anula la verosimilitud.

Corrección estándar con pseudoconteos:

$$
\hat{\theta}_{jk} =
\frac{N_{jk}+\alpha}{\sum_{\ell=1}^V N_{j\ell} + \alpha V},
\qquad
\alpha > 0
$$

Interpretación: agregar pseudoconteos equivale a usar un prior de Dirichlet simétrico.

## Diapositiva 37. .e.g.: Aplicación: Spam

En filtrado de spam, clasificación de noticias o análisis temático:

- $d$ puede estar en miles o decenas de miles;
- las matrices de covarianza completas son inviables;
- la independencia condicional es falsa, pero útil.

El éxito empírico del modelo viene de que, para decidir la clase, muchas dependencias finas importan menos que unas pocas diferencias robustas en frecuencias marginales.

![Ejemplo de mensaje de spam usado como motivación para Multinomial Naive Bayes](figures/clase-5/fig-37-spam-email.png)

## Diapositiva 38. .e.g.: Aplicación: Iris dataset

A pesar de su simplicidad, el clasificador suele funcionar muy bien en Iris:

- $d=4$ y $c=3$;
- cada clase tiene una media $\mu_j \in \mathbb{R}^4$;
- cada clase tiene una covarianza diagonal $\Sigma_j$.

Aunque el supuesto naive no es exacto, rinde bien porque:

- las clases están moderadamente separadas;
- el tamaño muestral es pequeño;
- el ahorro de parámetros compensa parte del sesgo del modelo.

## Diapositiva 39. .e.g.: Aplicación: Iris dataset

La figura muestra el diagrama de dispersión por pares del conjunto Iris, con histogramas marginales y tres especies.

![Diagrama de dispersión por pares del dataset Iris](figures/clase-5/fig-39-iris-pairplot.png)

## Diapositiva 40. Ejercicio Rápido

Supongamos un problema con $d=50$ características y dos clases:

1. ¿Cuántos parámetros por clase requiere una gaussiana completa?
2. ¿Cuántos requiere Gaussian Naive Bayes?
3. ¿Qué implica esto si $n$ es del orden de $100$?

Objetivo: cuantificar la diferencia entre $O(d^2)$ y $O(d)$.

## Diapositiva 41. Cuando Naive Bayes es demasiado "naive"

Naive Bayes resuelve el problema imponiendo máxima simplicidad.

Pero a veces sabemos algo más:

- ciertas variables sí dependen entre sí;
- otras quedan independientes dadas unas pocas causas comunes;
- puede haber variables no observadas que estructuren la dependencia.

Para expresar estas dependencias se introducen los modelos gráficos probabilísticos.

## Diapositiva 42. Modelos Gráficos y Redes Bayesianas

**Sección:** modelos gráficos y redes bayesianas.

## Diapositiva 43. Introducción a las Redes Bayesianas

Las técnicas previas parametrizan distribuciones mediante un vector de características $\theta$, pero muchas veces el conocimiento previo se refiere más bien a dependencias e independencias estadísticas.

Una red bayesiana es un grafo acíclico dirigido:

$$
G = (V,E)
$$

donde:

- $V$ es el conjunto de nodos;
- $E$ es el conjunto de aristas;
- cada nodo representa una variable aleatoria $X_i$;
- cada arista representa dependencia condicional $P(X_i \mid \operatorname{pa}(X_i))$;
- la distribución conjunta factoriza de acuerdo con el grafo.

Factorización general:

$$
p(x_1,\ldots,x_m) = \prod_{i=1}^m p(x_i \mid \operatorname{pa}(X_i))
$$

## Diapositiva 44. Introducción a las Redes Bayesianas

Ejemplos visuales de DAGs en distintos dominios:

- alarma causada por robo o terremoto;
- lluvia y rociador condicionados por nubosidad;
- gripe, fiebre y temperatura;
- dos estructuras posibles para variables morfológicas de flores.

![Ejemplos de grafos acíclicos dirigidos en distintos dominios](figures/clase-5/fig-44-bn-examples.png)

## Diapositiva 45. Representación Gráfica de Dependencias

Una red de creencia bayesiana permite especificar, mediante su topología, las dependencias e independencias funcionales entre variables.

Las flechas indican influencia causal o dependencia condicional.

![Ejemplo de red bayesiana con dependencias locales y factores condicionales](figures/clase-5/fig-45-bn-dependencies.png)

## Diapositiva 46. Lectura Gráfica: Padres e Hijos

En el DAG:

- $A$ es padre de $B$ y $C$;
- $D$ es hijo de $B$ y $C$;
- $\operatorname{pa}(D)=\{B,C\}$.

La conjunta factoriza como:

$$
p(a,b,c,d) = p(a)\,p(b \mid a)\,p(c \mid a)\,p(d \mid b,c)
$$

Leer flechas en un DAG equivale a leer qué depende de qué.

![Ejemplo simple de relaciones padre-hijo en un DAG](figures/clase-5/fig-46-parents-children.png)

## Diapositiva 47. La Propiedad de Markov Local

En una red bayesiana, cada nodo es condicionalmente independiente de sus no descendientes dado el conjunto de sus padres:

$$
X_i \perp\!\!\!\perp \operatorname{NoDesc}(X_i) \mid \operatorname{pa}(X_i)
$$

Esta propiedad justifica la factorización de la conjunta.

La estructura del grafo codifica hipótesis estadísticas explícitas.

## Diapositiva 48. Tres Patrones Básicos

Hay tres motivos locales fundamentales:

1. **Cadena:** $X \to Y \to Z$.
2. **Fork:** $X \leftarrow Y \to Z$.
3. **Collider:** $X \to Y \leftarrow Z$.

Cada uno induce propiedades de independencia distintas.

## Diapositiva 49. Cadena

En la cadena
$X \to Y \to Z$,
suele cumplirse:

$$
X \perp\!\!\!\perp Z \mid Y
$$

Interpretación: una vez observado el nodo intermedio $Y$, conocer $X$ no agrega información adicional sobre $Z$.

![Patrón de cadena en un DAG](figures/clase-5/fig-49-chain.png)

## Diapositiva 50. Fork

En el patrón
$X \leftarrow Y \to Z$,
puede darse:

$$
X \perp\!\!\!\perp Z \mid Y
$$

Aquí $Y$ actúa como causa común. Sin condicionar en $Y$, $X$ y $Z$ suelen aparecer correlacionadas.

![Patrón de fork en un DAG](figures/clase-5/fig-50-fork.png)

## Diapositiva 51. Collider

En el patrón
$X \to Y \leftarrow Z$,
ocurre el fenómeno opuesto:

$$
X \perp\!\!\!\perp Z
$$

marginalmente, pero al condicionar en $Y$ o en un descendiente de $Y$ aparece dependencia inducida.

![Patrón de collider en un DAG](figures/clase-5/fig-51-collider.png)

## Diapositiva 52. d-Separation

El criterio general de independencia en DAGs es la d-separación.

Dos conjuntos de nodos $A$ y $B$ están d-separados por $C$ si todo camino entre $A$ y $B$ queda bloqueado por $C$.

La idea práctica es que el grafo no es decorativo: es un sistema algebraico de independencias condicionales.

## Diapositiva 53. Naive Bayes es un Caso Particular

La red naive:

$$
\omega \to x_1,\ldots,\omega \to x_d
$$

es una red bayesiana particular en la que:

$$
x_i \perp\!\!\!\perp x_j \mid \omega,
\qquad
i \ne j
$$

Por eso Naive Bayes es el caso extremo de estructura mínima.

## Diapositiva 54. Inferencia y Propagación

Ideas básicas de inferencia en redes:

- **fijación:** establecer variables observadas a valores conocidos;
- **inferencia bayesiana:** calcular $P(X_{\text{hidden}} \mid X_{\text{observed}})$ para nodos desconocidos;
- **complejidad:** la inferencia se simplifica porque se trabaja con dependencias locales.

## Diapositiva 55. .e.g.: Enfermedad cardíaca

Variables del ejemplo:

- $A$: apnea del sueño;
- $O$: obesidad;
- $I$: insuficiencia cardíaca;
- $P$: pulmones con líquido o edema;
- $F$: fatiga.

La red modela factores de riesgo, patología central y signos clínicos.

![Red bayesiana para el ejemplo de enfermedad cardíaca](figures/clase-5/fig-55-heart-network.png)

## Diapositiva 56. .e.g.: Enfermedad cardíaca

Problema de dimensionalidad:

- con $d$ variables binarias, una tabla conjunta requiere $2^d-1$ parámetros;
- si $d=10$, eso da $1023$ parámetros.

Las redes bayesianas reducen esa carga si se conocen relaciones de dependencia.

## Diapositiva 57. .e.g.: Enfermedad cardíaca

Comparación de complejidad:

- sin red: $2^5 - 1 = 31$ parámetros independientes;
- con red bayesiana:
  - $P(A)$: 1;
  - $P(O)$: 1;
  - $P(I \mid A,O)$: 4;
  - $P(P \mid I)$: 2;
  - $P(F \mid I,P)$: 4.

Total con red: $12$ parámetros.

Conclusión: al aprovechar independencias condicionales, la carga de datos necesaria se reduce en un 61%.

![La misma red estructural usada para reducir la cantidad de parámetros](figures/clase-5/fig-55-heart-network.png)

## Diapositiva 58. .e.g.: Enfermedad cardíaca

La factorización en DAGs toma la forma:

$$
P(x_1,\ldots,x_d) = \prod_{i=1}^d P(x_i \mid \operatorname{pa}(x_i))
$$

En este ejemplo:

$$
P(A,O,I,P,F) = P(A)P(O)P(I \mid A,O)P(P \mid I)P(F \mid I,P)
$$

Cambios estructurales relevantes:

- $P(O \mid A)=P(O)$;
- $P(P \mid A,O,I)=P(P \mid I)$;
- $P(F \mid A,O,I,P)=P(F \mid I,P)$.

## Diapositiva 59. .e.g.: Enfermedad cardíaca

**Inferencia causal (top-down)**: predecir efectos a partir de causas conocidas.

Ejemplo: probabilidad de edema dado que el paciente es obeso.

Como $O$ no es padre directo de $P$, se marginaliza sobre $I$:

$$
P(P \mid O) = \sum_{i \in \{0,1\}} P(P \mid I=i)P(I=i \mid O)
$$

Esto usa el estado patológico intermedio para conectar factor de riesgo y síntoma.

## Diapositiva 60. .e.g.: Enfermedad cardíaca

**Inferencia evidencial (bottom-up)**: a partir de la evidencia $E$, inferir la hipótesis $H$.

$$
P(H \mid E) = \frac{P(E \mid H)P(H)}{P(E)}
$$

Ejemplo: probabilidad de insuficiencia dada la fatiga.

$$
P(I \mid F) = \frac{P(F \mid I)P(I)}{P(F)}
$$

Además:

$$
P(F \mid I) = \sum_p P(F \mid I, P=p)P(P=p \mid I)
$$

## Diapositiva 61. .e.g.: Enfermedad cardíaca

Para calcular el denominador se usa marginalización:

$$
P(E) = \sum_h P(E \mid H=h)P(H=h)
$$

En el ejemplo:

$$
P(F) = \sum_{i \in \{0,1\}} P(F \mid I=i)P(I=i)
$$

La figura contrapone la dirección diagnóstica con la generativa.

![Relación entre dirección generativa y diagnóstica](figures/clase-5/fig-61-generative-diagnostic.png)

## Diapositiva 62. .e.g.: Pescados

Variables:

- $A$: estación;
- $B$: localidad;
- $X$: especie;
- $C$: color o luminosidad;
- $D$: ancho o espesor.

Factorización:

$$
p(a,b,x,c,d) = p(a)\,p(b)\,p(x \mid a,b)\,p(c \mid x)\,p(d \mid x)
$$

En este ejemplo, $A$ y $B$ son independientes, y $C$ y $D$ quedan independientes al condicionar en la especie $X$.

![Red bayesiana del ejemplo de pescados](figures/clase-5/fig-62-fish-network.png)

## Diapositiva 63. .e.g.: Pescados

Con evidencia parcial $C=c$ y $D=d$, interesa calcular:

$$
P(X=x \mid C=c, D=d)
$$

Por Bayes:

$$
P(x \mid c,d) \propto P(x)P(c \mid x)P(d \mid x)
$$

cuando
$C \perp\!\!\!\perp D \mid X$.

La estructura determina qué términos aparecen y cuáles pueden omitirse.

## Diapositiva 64. Aprender o Especificar la Estructura

En la práctica, la red puede surgir de:

- conocimiento experto;
- restricciones causales conocidas;
- aprendizaje estructural a partir de datos.

Aun si la estructura es dada, hay que estimar densidades o tablas locales:

$$
p(x_i \mid \operatorname{pa}(X_i))
$$

Esto aporta modularidad: se puede modificar un nodo sin redefinir toda la conjunta.

## Diapositiva 65. Un Nuevo Problema

Las redes bayesianas permiten introducir variables no observadas.

Esto es poderoso porque:

- modela causas ocultas;
- representa datos faltantes;
- conecta clasificación, clustering y mezclas.

Pero también complica la estimación, porque la verosimilitud observable deja de tener una forma simple.

## Diapositiva 66. Ejercicio de Estructura

Considere tres variables:

- lluvia $R$;
- aspersor $S$;
- césped mojado $W$.

Preguntas:

1. proponer un DAG razonable;
2. escribir la factorización de la conjunta;
3. indicar una independencia condicional que se desprenda del grafo.

## Diapositiva 67. Datos Faltantes y Variables Latentes

**Sección:** datos faltantes y variables latentes.

## Diapositiva 68. Datos Completos vs. Datos Incompletos

Si se observan datos completos $z$, maximizar

$$
\ell(\theta) = \ln p(z \mid \theta)
$$

suele ser directo.

Si una parte está oculta y observamos solo $x$, con variable latente $y$:

$$
p(x \mid \theta) = \sum_y p(x,y \mid \theta)
$$

o, en el caso continuo:

$$
p(x \mid \theta) = \int p(x,y \mid \theta)\,dy
$$

La marginalización destruye la simplicidad algebraica.

## Diapositiva 69. Qué Significa "Dato Faltante"

Hay dos situaciones matemáticamente cercanas:

- faltan algunas coordenadas de $x$;
- existe una variable latente $Z$ que explica la observación.

En ambos casos, la verosimilitud observada se obtiene eliminando variables no observadas mediante suma o integración.

## Diapositiva 70. .e.g.: GMM como red Bayesiana

La figura muestra una mezcla gaussiana como red bayesiana:

- $\pi$ parametriza la mezcla;
- $\theta$ parametriza las componentes;
- $z_i$ es la variable latente de asignación;
- $x_i$ es la observación;
- la placa recorre $i=1,\ldots,n$.

![Diagrama de placas para una mezcla gaussiana como red bayesiana](figures/clase-5/fig-70-gmm-plate.png)

## Diapositiva 71. Ejemplos Típicos

Situaciones típicas:

- algunas entradas del vector de características no fueron medidas;
- la clase es desconocida en un problema de mezcla;
- un documento tiene tema latente no observado;
- una población es combinación de varias subpoblaciones gaussianas.

La pregunta común es:

$$
\hat{\theta} = \arg\max_{\theta} \ln p(D_{\text{obs}} \mid \theta)
$$

## Diapositiva 72. Por Qué ML Directo se Vuelve Difícil

El logaritmo de una suma no se separa:

$$
\ln \sum_y p(x,y \mid \theta) \ne \sum_y \ln p(x,y \mid \theta)
$$

Por eso:

- las derivadas no suelen dar ecuaciones cerradas;
- la optimización directa puede ser inestable;
- conviene introducir una cota inferior más manejable.

## Diapositiva 73. La Idea de EM

Expectation-Maximization construye una secuencia
$\theta^{(0)}, \theta^{(1)}, \ldots$
tal que la verosimilitud observada no disminuye.

Intuición:

1. completar probabilísticamente la información faltante usando el modelo actual;
2. resolver luego el problema de máxima verosimilitud de "datos completos esperados".

## Diapositiva 74. La Función Auxiliar Q

Se define:

$$
Q(\theta,\theta^{(t)}) =
\mathbb{E}_{Y \mid X,\theta^{(t)}}\left[\ln p(X,Y \mid \theta)\right]
$$

Interpretación:

- $X$ son los datos observados;
- $Y$ representa lo faltante o latente;
- la esperanza se toma bajo el parámetro actual $\theta^{(t)}$;
- $\theta^{(t)}$ es fijo;
- $\theta$ es la variable respecto de la cual se optimiza.

## Diapositiva 75. Algoritmo EM

Dado $\theta^{(t)}$:

- **Paso E:** calcular $Q(\theta,\theta^{(t)})$.
- **Paso M:** elegir

$$
\theta^{(t+1)} = \arg\max_{\theta} Q(\theta,\theta^{(t)})
$$

Se repite hasta convergencia.

La clave es que el paso M suele tener la misma forma que el problema de máxima verosimilitud con datos completos.

EM no garantiza óptimo global, pero sí una subida monótona hasta un punto fijo local.

## Diapositiva 76. Vista Variacional Básica

Para cualquier distribución $q(Y)$:

$$
\ln p(X \mid \theta) =
\mathcal{L}(q,\theta) +
\operatorname{KL}\left(q(Y)\,\|\,p(Y \mid X,\theta)\right)
$$

Si se elige

$$
q(Y) = p(Y \mid X,\theta^{(t)})
$$

la cota es exacta en $\theta=\theta^{(t)}$, y maximizar $\mathcal{L}$ respecto de $\theta$ produce el paso M.

## Diapositiva 77. .e.g.: Gaussianas 2D

La diapositiva muestra una interfaz de ejemplo para EM en una mezcla gaussiana bidimensional, con dos componentes, elipses estimadas y centros reales.

![Interfaz de ejemplo para EM en gaussianas 2D](figures/clase-5/fig-77-em-2d.png)

## Diapositiva 78. Análisis de la Convergencia EM

Puntos destacados:

- **mejora garantizada:** cada paso aumenta la verosimilitud de los datos observados;
- **eficiencia:** si el paso M tiene solución cerrada, EM suele converger más rápido que métodos de gradiente;
- **puntos fijos:** el algoritmo termina cuando $\mu_{i+1} \approx \mu_i$ y ya no mejora la función $Q$.

## Diapositiva 79. .e.g.: Gaussiana con Coordenadas Faltantes

Supongamos:

$$
x_k \sim N(\mu, I)
$$

y que en algunas muestras falta una coordenada.

Si la covarianza es $I$, cada coordenada faltante tiene esperanza condicional igual a la media actual:

$$
\mathbb{E}[x_{kj} \mid \text{observado}, \mu^{(t)}] = \mu_j^{(t)}
$$

En el paso E, cada valor ausente se reemplaza por su esperanza condicional bajo el modelo actual.

## Diapositiva 80. Paso M en el Ejemplo Gaussiano

La actualización de la media toma la forma:

$$
\mu_j^{(t+1)} =
\frac{1}{n}\sum_{k=1}^n
\mathbb{E}[x_{kj} \mid \text{observado}, \mu^{(t)}]
$$

Es decir:

- para coordenadas observadas se usa el valor real;
- para coordenadas faltantes se usa el valor esperado.

EM convierte un promedio imposible en un promedio de observaciones y esperanzas.

## Diapositiva 81. Ejemplo 2: El Problema de las Monedas

Dos monedas $A$ y $B$ tienen probabilidades de cara $\theta_A$ y $\theta_B$.

En cada experimento:

1. se elige una moneda no observada;
2. se lanza varias veces;
3. se observa solo el número de caras.

La variable latente es $Z_k \in \{A,B\}$, que indica qué moneda generó el experimento $k$.

## Diapositiva 82. Paso E para las Monedas

Para un experimento con $h_k$ caras y $t_k$ cruces:

$$
\gamma_k = P(Z_k=A \mid h_k,t_k,\theta^{(t)}) =
\frac{
\pi_A(\theta_A^{(t)})^{h_k}(1-\theta_A^{(t)})^{t_k}
}{
\pi_A(\theta_A^{(t)})^{h_k}(1-\theta_A^{(t)})^{t_k}
+
\pi_B(\theta_B^{(t)})^{h_k}(1-\theta_B^{(t)})^{t_k}
}
$$

Los $\gamma_k$ son las responsabilidades.

## Diapositiva 83. Paso M para las Monedas

Con las responsabilidades del paso E:

$$
\theta_A^{(t+1)} =
\frac{\sum_k \gamma_k h_k}{\sum_k \gamma_k(h_k+t_k)}
$$

$$
\theta_B^{(t+1)} =
\frac{\sum_k (1-\gamma_k) h_k}{\sum_k (1-\gamma_k)(h_k+t_k)}
$$

La actualización coincide con ML, pero usando conteos esperados.

EM no asigna duramente cada experimento a una moneda: asigna pesos probabilísticos.

## Diapositiva 84. Convergencia y Puntos Fijos

Un punto fijo de EM satisface:

$$
\theta^{(t+1)} = \theta^{(t)}
$$

En ese punto, no puede aumentarse localmente la cota construida en el paso E.

En la práctica:

- EM depende de la inicialización;
- puede converger a máximos locales o puntos silla;
- suele ser muy efectivo cuando el paso M tiene solución cerrada.

## Diapositiva 85. Ejercicio de EM

En el ejemplo de las monedas:

1. identificar la variable latente;
2. escribir qué calcula exactamente el paso E;
3. interpretar el paso M como un problema de máxima verosimilitud con conteos esperados.

Si esas tres piezas están claras, la mecánica de EM queda fijada.

## Diapositiva 86. Chequeo Final de la Clase

Preguntas de salida:

1. ¿qué relación conceptual hay entre Naive Bayes y redes bayesianas?
2. ¿qué vuelve difícil la optimización con datos incompletos?
3. ¿qué garantiza EM y qué no garantiza?

## Diapositiva 87. Resumen Conceptual

Tres niveles de complejidad vistos en la clase:

1. **Naive Bayes:** independencia condicional total.
2. **Redes Bayesianas:** dependencia estructurada.
3. **EM:** variables latentes y datos faltantes.

Cada paso aumenta la expresividad, pero también el costo inferencial y de aprendizaje.

## Diapositiva 88. Próxima clase

En esta clase se simplificó el modelo probabilístico.

En la próxima clase se simplificará el espacio de representación mediante:

- whitening;
- PCA;
- discriminante lineal de Fisher.
