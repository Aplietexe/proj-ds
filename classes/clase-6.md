---
title: "Geometría y Reducción de la Dimensión: Whitening, PCA y Fisher Linear Discriminant"
---

## Diapositiva 1

**Portada**

- Clase 6
- Data Science & Machine Learning
- FaMAF
- 2026-04-09

## Diapositiva 2. Roadmap de la Clase

La clase se organiza en tres bloques:

1. **Whitening**
2. **PCA**
3. **Fisher Linear Discriminant**

## Diapositiva 3. Continuidad con la Clase 5

En la clase anterior se simplificó el modelo probabilístico imponiendo estructura.

Otro camino consiste en reducir la dimensionalidad en el espacio de datos. Para eso se mencionan, por ejemplo:

- eliminación de *features*;
- transformación a un espacio de *features* nuevos de menor dimensión.

Entre los métodos de transformación de *features* aparecen:

- PCA (*Principal Component Analysis*);
- tSNE (*t-distributed Stochastic Nearest Neighbors*);
- LDA (*Linear Discriminant Analysis*);
- autoencoders.

## Diapositiva 4. Perspectiva Geométrica

Ahora se toma una perspectiva geométrica:

- la covarianza define una métrica;
- un cambio lineal de coordenadas puede "esferizar" los datos;
- luego se buscan proyecciones de baja dimensión.

Se analizará el caso de la gaussiana multivariada para desarrollar intuición y formalismo, aunque los métodos son aplicables más allá de esa familia.

Pregunta central:

- ¿cómo medimos distancia cuando hay correlaciones?
- ¿cómo eliminamos esas correlaciones mediante un cambio de base?
- ¿cómo proyectamos a dimensión menor preservando estructura relevante?

## Diapositiva 5. La Gaussiana Multivariada como Objeto Geométrico

Si

$$
x \sim \mathcal{N}(\mu,\Sigma),
$$

entonces

$$
p(x) \propto \exp\left[-\frac{1}{2}(x-\mu)^T\Sigma^{-1}(x-\mu)\right].
$$

Las superficies de igual densidad están dadas por

$$
(x-\mu)^T\Sigma^{-1}(x-\mu)=c.
$$

Son elipsoides centrados en $\mu$.

## Diapositiva 6. Por Qué la Distancia Euclídea No Basta

La distancia euclídea

$$
\lVert x-\mu\rVert^2
$$

trata todas las direcciones como equivalentes.

Pero si una distribución tiene:

- gran varianza en una dirección;
- pequeña varianza en otra;
- correlación entre coordenadas;

entonces alejarse una unidad en cada eje no tiene el mismo significado estadístico.

La distancia cuadrática de Mahalanobis a la media es

$$
r^2(x) = (x-\mu)^T\Sigma^{-1}(x-\mu).
$$

Propiedades:

- es adimensional;
- incorpora escala y correlación;
- coincide con la distancia euclídea si $\Sigma = I$.

## Diapositiva 7. Ejemplo con Covarianza Diagonal

En el caso diagonal,

$$
\Sigma = \operatorname{diag}(\sigma_1^2,\ldots,\sigma_d^2)
\quad \Longrightarrow \quad
r^2(x) = \sum_{k=1}^d \frac{(x_k-\mu_k)^2}{\sigma_k^2}.
$$

Interpretación: cada coordenada se mide en unidades de su desviación estándar. Esta es exactamente la forma que aparecía en Gaussian Naive Bayes.

Si dos clases gaussianas comparten una covarianza $\Sigma$, la separación entre sus medias se resume en

$$
r^2 = (\mu_1-\mu_2)^T\Sigma^{-1}(\mu_1-\mu_2).
$$

Esta cantidad:

- crece si las medias se alejan;
- decrece si la dispersión compartida aumenta;
- es la separación natural para problemas gaussianos.

## Diapositiva 8. Ejemplo con Covarianza No Diagonal

Si $\Sigma$ no es diagonal, el término cuadrático mezcla coordenadas:

$$
r^2(x) = \sum_{i,j}(x_i-\mu_i)(\Sigma^{-1})_{ij}(x_j-\mu_j).
$$

Por eso:

- la métrica ya no se interpreta coordenada a coordenada;
- la orientación de los elipsoides depende de los autovectores de $\Sigma$;
- conviene diagonalizar la covarianza.

## Diapositiva 9. Invariancia Afín

Sea

$$
y = Ax + b,
$$

con $A$ invertible. Entonces

$$
\mu_y = A\mu + b,
\qquad
\Sigma_y = A\Sigma A^T.
$$

La distancia de Mahalanobis se preserva:

$$
(y-\mu_y)^T\Sigma_y^{-1}(y-\mu_y) = (x-\mu)^T\Sigma^{-1}(x-\mu).
$$

Es, por lo tanto, una noción geométrica intrínseca de la nube gaussiana.

## Diapositiva 10. Bayes Error y Separación

En el caso de dos gaussianas con igual covarianza y *priors* iguales, el error de Bayes decrece al aumentar la separación de Mahalanobis.

Entonces:

- la geometría de $\Sigma$ afecta directamente la dificultad del problema;
- medir bien la distancia ya es parte de la clasificación.

La idea resaltada en la diapositiva es:

> La covarianza define la geometría efectiva del problema. Por eso medir, blanquear y proyectar son operaciones íntimamente relacionadas.

## Diapositiva 11. Whitening

**Sección:** Whitening.

## Diapositiva 12. Diagonalización Espectral

Como $\Sigma$ es simétrica definida positiva, existe una descomposición

$$
\Sigma = \Phi\Lambda\Phi^T,
$$

donde:

- $\Phi$ es ortogonal;
- $\Lambda = \operatorname{diag}(\lambda_1,\ldots,\lambda_d)$, con $\lambda_i > 0$.

Los autovectores de $\Sigma$ determinan las direcciones principales de dispersión.

## Diapositiva 13. Construcción del Whitening

Se define

$$
W = \Lambda^{-1/2}\Phi^T.
$$

Para datos centrados,

$$
z = W(x-\mu).
$$

Esta transformación:

- rota hacia la base de autovectores;
- reescala cada eje por $1/\sqrt{\lambda_i}$;
- produce una nube con covarianza identidad.

## Diapositiva 14. Prueba de que la Nueva Covarianza es I

Si $z = W(x-\mu)$, entonces

$$
\operatorname{Cov}(z) = W\Sigma W^T.
$$

Sustituyendo $\Sigma = \Phi\Lambda\Phi^T$:

$$
W\Sigma W^T
=
(\Lambda^{-1/2}\Phi^T)(\Phi\Lambda\Phi^T)(\Phi\Lambda^{-1/2})
=
\Lambda^{-1/2}\Lambda\Lambda^{-1/2}
=
I.
$$

Además,

$$
\lVert z\rVert^2
=
(x-\mu)^T W^T W (x-\mu)
=
(x-\mu)^T \Sigma^{-1} (x-\mu).
$$

Es decir,

$$
r^2(x)=\lVert z\rVert^2.
$$

Whitening convierte la métrica de Mahalanobis en métrica euclídea estándar.

## Diapositiva 15. Interpretación Geométrica

El whitening hace tres cosas a la vez:

1. centra la nube;
2. elimina correlaciones;
3. iguala la varianza de todas las direcciones a $1$.

Después del cambio de coordenadas, los elipsoides de nivel se convierten en esferas.

Muchos métodos lineales son más fáciles de analizar en espacio blanqueado, y muchos algoritmos asumen que los *features* son comparables, es decir, que tienen la misma escala y no hay correlación. Se mencionan como ejemplos:

- K-means;
- KNN;
- gradiente descendente, por mejor condicionamiento;
- redes neuronales, por entrenamiento más estable.

Whitening evita que las primeras componentes, es decir, las de mayor varianza, dominen.

## Diapositiva 16. Ejercicio

Si

$$
\Sigma = \Phi\Lambda\Phi^T,
$$

se propone:

1. escribir una transformación que vuelva identidad a la covarianza;
2. explicar qué parte de la transformación rota y cuál reescala;
3. relacionar el resultado con la distancia de Mahalanobis.

## Diapositiva 17. Whitening

El blanqueo o whitening de variables es un método que transforma un conjunto de variables aleatorias con una distribución multivariada en otro conjunto de variables aleatorias que son linealmente independientes y tienen varianza unitaria.

Es una preparación para algunos métodos que asumen que las variables de entrada son independientes y tienen la misma escala.

La diapositiva cierra con la observación:

> Pero hasta ahora no redujimos la dimensionalidad.

## Diapositiva 18. PCA

**Sección:** PCA.

## Diapositiva 19. Definición de PCA

**Definición.** PCA (*Principal Component Analysis*) es un algoritmo que busca la proyección ortogonal de los datos en un subespacio tal que la varianza de los datos proyectados sea máxima.

La diapositiva destaca:

- los datos suelen tener muchos *features* con cierto grado de correlación;
- PCA permite describirlos con un conjunto reducido de nuevas variables;
- esas nuevas variables son representativas de la muestra y explican la mayor parte de la variabilidad del conjunto original;
- las componentes principales son direcciones en las que los datos originales tienen alta variabilidad;
- esas direcciones generan un subespacio que queda lo más cerca posible de la nube de puntos.

La figura ilustra una nube correlacionada y sus direcciones principales:

![Nube correlacionada y direcciones principales](figures/clase-6/fig-19-pca-cloud.png)

## Diapositiva 20. PCA

La figura compara el conjunto de datos original con su reconstrucción luego de proyectar sobre una recta. La pregunta guía es:

> ¿Cómo encontramos esa proyección?

![Datos originales y reconstrucción lineal después de PCA](figures/clase-6/fig-20-pca-reconstruction.png)

## Diapositiva 21. PCA

La figura muestra una proyección lineal sobre un eje rotado y las distribuciones resultantes en una dimensión. Sirve como intuición visual sobre cómo cambia la separación y la variabilidad al elegir una dirección de proyección.

![Demostración visual de una proyección lineal y sus distribuciones proyectadas](figures/clase-6/fig-21-pca-projection-demo.png)

## Diapositiva 22. PCA

Supongamos que tenemos $n$ observaciones de una variable aleatoria $\tilde{X}$ que consta de $p$ *features*.

Si queremos visualizar este conjunto de datos, podemos considerar proyecciones en dos dimensiones.

La cantidad de tales proyecciones es

$$
\binom{p}{2} = \frac{p!}{(p-2)!2!} = \frac{p(p-1)}{2}.
$$

Por ejemplo, para $p=10$ hay en total $45$ gráficos.

La idea es graficar los mismos datos reduciendo la información en $p$ dimensiones a, por ejemplo, solo $2$.

## Diapositiva 23. PCA

Se asume que existen correlaciones en los datos, de modo que no todos los *features* son igualmente interesantes o representativos. Los más "interesantes" serán los que tengan mayor variación.

Cada una de las componentes principales, es decir, cada dirección, es una combinación lineal de los *features* del espacio original:

$$
Z = a_1X_1 + a_2X_2 + \cdots + a_pX_p.
$$

Se quiere encontrar los parámetros $a_i$ para pasar de los $p$ *features* a un conjunto menor $\{Z_1,Z_2,\ldots,Z_k\}$, donde

$$
Z_j = a_{j1}X_1 + a_{j2}X_2 + \cdots + a_{jp}X_p.
$$

## Diapositiva 24. PCA

A los coeficientes se les impone la condición de normalización

$$
\sum_{i=1}^p a_{jk}^2 = 1.
$$

Para que la dispersión sea lo más grande posible, se pide que la varianza de los $Z$ sea máxima. La diapositiva lo presenta como un problema de maximización con restricción sobre los parámetros $a$.

En particular, suponiendo variables ya centradas, se busca la dirección de la componente principal más importante y luego se reproduce el procedimiento para las siguientes.

## Diapositiva 25. PCA

La figura muestra una nube correlacionada, un eje de proyección y la varianza proyectada correspondiente. La idea visual es que PCA busca el ángulo donde esa varianza proyectada es máxima.

![Varianza proyectada sobre un eje de proyección](figures/clase-6/fig-25-pca-projected-variance.png)

## Diapositiva 26. PCA

De este procedimiento se concluye que, si los valores numéricos de alguna variable son altos, entonces dominarán las cuentas.

Antes de calcular las componentes principales, hay que:

- centrar los datos;
- escalar los datos;
- pero no corregir por correlaciones.

## Diapositiva 27. PCA

La figura resume la idea geométrica de que las componentes principales son las direcciones que maximizan la dispersión.

![Direcciones principales que maximizan la dispersión](figures/clase-6/fig-27-pca-max-dispersion.png)

## Diapositiva 28. PCA

La figura muestra que los datos en el espacio de dimensión reducida quedan "parecidos" a los datos en el espacio original, en el sentido de aproximarlos mediante proyección ortogonal.

![Proyección de puntos sobre una dirección principal](figures/clase-6/fig-28-pca-reduced-space.png)

## Diapositiva 29. PCA: Formulación Vectorial

Para una dirección unitaria $u$, la proyección escalar es

$$
y_k = u^T(x_k-m).
$$

La varianza proyectada es

$$
\Sigma_u^2 = \frac{1}{n}\sum_{k=1}^n y_k^2 = u^T\Sigma u.
$$

PCA busca la dirección que maximiza esta cantidad:

$$
\max_u u^T\Sigma u
\qquad
\text{sujeto a}
\qquad
u^Tu = 1.
$$

Interpretación:

- $u^T\Sigma u$ es la varianza en la dirección $u$;
- $u^Tu = 1$ evita soluciones triviales por escala arbitraria.

## Diapositiva 30. Lagrangiano y Condición de Óptimo

Se define

$$
\mathcal{L}(u,\lambda) = u^T\Sigma u - \lambda(u^Tu-1).
$$

Derivando respecto de $u$:

$$
\nabla_u \mathcal{L} = 2\Sigma u - 2\lambda u = 0
\qquad \Longrightarrow \qquad
\Sigma u = \lambda u.
$$

Conclusión: los puntos críticos son autovectores de $\Sigma$.

## Diapositiva 31. ¿Por Qué el Mayor Autovalor?

Sea la descomposición espectral

$$
\Sigma = \Phi\Lambda\Phi^T,
$$

donde

$$
\Lambda = \operatorname{diag}(\lambda_1,\ldots,\lambda_d).
$$

Se escribe $u$ en la base de autovectores:

$$
u = \sum_{i=1}^d \alpha_i\phi_i,
\qquad
\sum_{i=1}^d \alpha_i^2 = 1.
$$

Entonces

$$
u^T\Sigma u = \sum_{i=1}^d \lambda_i \alpha_i^2.
$$

Interpretación:

- es una combinación convexa de los autovalores;
- se maximiza poniendo todo el peso en el mayor $\lambda_i$.

Por lo tanto,

$$
\max_u u^T\Sigma u = \lambda_1
\qquad
\text{cuando}
\qquad
u = \phi_1.
$$

## Diapositiva 32. Resultado de PCA

La primera componente principal es

$$
u_1 = \text{autovector asociado a } \lambda_1 = \max_i \lambda_i.
$$

Además,

$$
\sigma_{u_1}^2 = \lambda_1.
$$

Conclusiones:

- los autovectores definen direcciones principales;
- los autovalores miden varianza explicada.

En síntesis: PCA consiste en encontrar la dirección donde la varianza es máxima.

## Diapositiva 33. Componentes Sucesivas

La segunda componente principal resuelve el mismo problema, pero imponiendo ortogonalidad con la primera:

$$
\max_u u^T\Sigma u
\qquad
\text{sujeto a}
\qquad
\lVert u\rVert = 1,
\qquad
u^Tu_1 = 0.
$$

La solución es el autovector asociado a $\lambda_2$.

En general, las $d'$ componentes principales son los autovectores principales de $\Sigma$.

## Diapositiva 34. Proyección de Dimensión Reducida

Si

$$
U = [u_1,\ldots,u_{d'}],
$$

entonces la representación reducida es

$$
y = U^T(x-m).
$$

La reconstrucción lineal correspondiente es

$$
\hat{x} = m + Uy.
$$

## Diapositiva 35. Varianza Explicada

Si los autovalores están ordenados como

$$
\lambda_1 \ge \lambda_2 \ge \cdots \ge \lambda_d \ge 0,
$$

la fracción de varianza explicada por los primeros $d'$ componentes es

$$
\frac{\sum_{i=1}^{d'} \lambda_i}{\sum_{i=1}^d \lambda_i}.
$$

Esto guía la selección de dimensión.

## Diapositiva 36. PCA y Error de Reconstrucción

La figura compara el espacio original en dos dimensiones con la reconstrucción obtenida usando solo la primera componente principal.

![Espacio original y reconstrucción por la primera componente principal](figures/clase-6/fig-36-pca-reconstruction-error.png)

## Diapositiva 37. PCA y Error de Reconstrucción

PCA no solo maximiza varianza retenida. También minimiza el error cuadrático medio de reconstrucción entre todos los subespacios lineales de dimensión $d'$:

$$
\min_{U^TU=I}
\frac{1}{n}
\sum_{k=1}^n
\left\lVert (x_k-m) - UU^T(x_k-m) \right\rVert^2.
$$

Ambas formulaciones son equivalentes.

## Diapositiva 38. PCA y Reconstrucción

Supongamos datos centrados:

$$
\frac{1}{n}\sum_{k=1}^n x_k = 0.
$$

Sea

$$
U \in \mathbb{R}^{d \times d'}
$$

una base ortonormal:

$$
U^TU = I.
$$

Proyección:

$$
y_k = U^T x_k.
$$

Reconstrucción:

$$
\hat{x}_k = Uy_k = UU^Tx_k.
$$

Idea: aproximamos los datos proyectándolos a un subespacio.

## Diapositiva 39. Error Cuadrático de Reconstrucción

Se define el error medio:

$$
E = \frac{1}{n}\sum_{k=1}^n \lVert x_k - \hat{x}_k \rVert^2.
$$

Sustituyendo:

$$
E = \frac{1}{n}\sum_{k=1}^n \lVert x_k - UU^Tx_k \rVert^2.
$$

Se usa la descomposición ortogonal:

$$
x_k = UU^T x_k + (I-UU^T)x_k.
$$

Entonces, por Pitágoras,

$$
\lVert x_k\rVert^2 = \lVert UU^T x_k\rVert^2 + \lVert (I-UU^T)x_k\rVert^2.
$$

## Diapositiva 40. Varianza vs Error: Resultado Fundamental

El error puede escribirse como

$$
E =
\frac{1}{n}\sum_{k=1}^n \lVert x_k\rVert^2
-
\frac{1}{n}\sum_{k=1}^n \lVert UU^T x_k\rVert^2.
$$

Interpretación:

- el primer término es la varianza total y es constante;
- el segundo término es la varianza explicada.

En forma matricial:

$$
E = \operatorname{Tr}(\Sigma) - \operatorname{Tr}(U^T\Sigma U).
$$

En consecuencia:

$$
\text{Minimizar error}
\Longleftrightarrow
\text{maximizar varianza proyectada}.
$$

## Diapositiva 41. PCA

La figura resume la dualidad geométrica entre:

- maximizar la varianza de los puntos proyectados sobre una dirección;
- minimizar los residuales ortogonales a esa dirección.

![Maximizar varianza versus minimizar residuales](figures/clase-6/fig-41-pca-variance-vs-residuals.png)

## Diapositiva 42. Interpretación Geométrica de PCA

PCA encuentra el subespacio lineal que mejor "ajusta" la nube en sentido cuadrático.

En $2$D:

- la primera componente sigue el eje de máxima elongación;
- la segunda es ortogonal y captura la variación residual.

El método ignora etiquetas de clase.

## Diapositiva 43. PCA Después de Whitening

Whitening y PCA no son lo mismo:

- whitening normaliza todas las direcciones para varianza $1$;
- PCA ordena direcciones por varianza decreciente.

Sin embargo, ambos usan la misma descomposición espectral de la covarianza.

Cuidado: si las variables tienen unidades muy distintas, PCA sin estandarización puede privilegiar solo la escala física.

## Diapositiva 44. Limitaciones de PCA

PCA es útil para compresión y visualización, pero no necesariamente para clasificación.

Puede ocurrir que la mayor varianza esté en una dirección irrelevante para separar clases. En ese caso:

- PCA retiene energía;
- pero pierde discriminación.

Esto motiva un método supervisado.

## Diapositiva 45. Chequeo Conceptual sobre PCA

La diapositiva propone revisar:

1. por qué el primer componente principal es un autovector;
2. qué mide un autovalor en PCA;
3. por qué PCA minimiza error de reconstrucción.

## Diapositiva 46. Fisher Linear Discriminant

**Sección:** Fisher Linear Discriminant.

## Diapositiva 47. Idea de Fisher

Queremos proyectar los datos sobre una dirección $w$ tal que:

- las medias de las clases queden muy separadas;
- la dispersión interna de cada clase sea pequeña.

Es un criterio señal-ruido.

Si proyectamos sobre $w$, las medias proyectadas son

$$
m_i' = w^T m_i.
$$

Para dos clases, queremos maximizar

$$
\lvert m_1' - m_2' \rvert^2
$$

y minimizar la suma de varianzas proyectadas intraclase.

## Diapositiva 48. PCA

La figura muestra dos clases proyectadas sobre un eje, junto con un resumen numérico del criterio de Fisher. Visualiza la tensión entre separación de medias y dispersión intraclase.

![Proyección de dos clases y criterio de Fisher](figures/clase-6/fig-48-fld-projection-demo.png)

## Diapositiva 49. Scatter Intraclase y Entre Clases

Se define

$$
S_i = \sum_{x \in D_i}(x-m_i)(x-m_i)^T.
$$

Si hay dos clases, la dispersión total intraclase es

$$
S_W = S_1 + S_2.
$$

La varianza proyectada total dentro de clase es

$$
w^T S_W w.
$$

Además, se define

$$
S_B = (m_1-m_2)(m_1-m_2)^T.
$$

Entonces

$$
w^T S_B w = \left(w^T(m_1-m_2)\right)^2,
$$

que mide la separación cuadrática entre medias proyectadas.

## Diapositiva 50. Criterio de Fisher

El cociente a maximizar es

$$
J(w) = \frac{w^T S_B w}{w^T S_W w}.
$$

El numerador recompensa separación entre medias. El denominador penaliza dispersión dentro de las clases.

En palabras:

$$
J(w) =
\frac{\text{separación entre clases}}{\text{dispersión dentro de clases}}.
$$

## Diapositiva 51. Derivación de la Solución

Para dos clases,

$$
J(w) = \frac{\left(w^T(m_1-m_2)\right)^2}{w^T S_W w}.
$$

La solución óptima es proporcional a

$$
w^\star = S_W^{-1}(m_1-m_2).
$$

Cualquier múltiplo no nulo de $w^\star$ produce la misma proyección ordenada.

## Diapositiva 52. Interpretación vía Whitening

La solución puede leerse así:

1. blanquear con respecto a la dispersión intraclase $S_W$;
2. en ese espacio esférico, proyectar en la dirección de la diferencia de medias.

Esto conecta directamente FLD con la geometría de Mahalanobis.

## Diapositiva 53. Extensión Multiclase

Para $c$ clases:

$$
S_W = \sum_{i=1}^c \sum_{x \in D_i}(x-m_i)(x-m_i)^T,
$$

$$
S_B = \sum_{i=1}^c n_i(m_i-m)(m_i-m)^T.
$$

El problema se vuelve

$$
\max_W \frac{\lvert W^T S_B W \rvert}{\lvert W^T S_W W \rvert}.
$$

La base discriminante multiclase se obtiene resolviendo

$$
S_B w = \lambda S_W w.
$$

Si $S_W$ es invertible:

$$
S_W^{-1}S_B w = \lambda w.
$$

Los autovectores asociados a los mayores autovalores definen el subespacio discriminante.

## Diapositiva 54. Dimensión Máxima del Subespacio LDA

Como

$$
\operatorname{rank}(S_B) \le c-1,
$$

el número máximo de direcciones discriminantes es

$$
d' \le c-1.
$$

Esto explica por qué LDA no busca compresión arbitraria: su dimensión útil está controlada por el número de clases.

Si las clases son gaussianas con covarianza común $\Sigma$, el discriminante bayesiano es lineal:

$$
g_i(x) = x^T\Sigma^{-1}\mu_i - \frac{1}{2}\mu_i^T\Sigma^{-1}\mu_i + \ln P(\omega_i).
$$

En ese régimen, la geometría de Fisher es consistente con la clasificación gaussiana óptima.

## Diapositiva 55. PCA vs. FLD

| PCA | FLD / LDA |
| --- | --- |
| No supervisado | Supervisado |
| Maximiza varianza total | Maximiza separabilidad |
| Ignora etiquetas | Usa etiquetas |
| Útil para compresión | Útil para clasificación |

## Diapositiva 56. Ejemplo Conceptual

Imaginemos dos clases alargadas en la misma dirección:

- PCA elige la dirección de mayor elongación global;
- pero esa dirección puede mezclar las clases;
- FLD elige la dirección que maximiza separación relativa al ruido intraclase.

La mayor varianza no coincide siempre con la mayor información discriminante.

## Diapositiva 57. Cuando SW es Singular

En alta dimensión puede pasar que

$$
d \gg n,
$$

y entonces $S_W$ sea singular.

Estrategias usuales:

- regularización;
- PCA previa para reducir dimensión;
- pseudoinversa;
- *shrinkage* de covarianza.

Vuelve a aparecer la tensión entre expresividad y estabilidad.

## Diapositiva 58. Ejercicio

Considere dos clases alargadas en la misma dirección principal.

1. ¿qué dirección tendería a elegir PCA?
2. ¿qué dirección tendería a elegir FLD?
3. ¿cuál sería más útil para clasificar y por qué?

Además:

1. ¿cómo se relacionan Mahalanobis y whitening?
2. ¿qué diferencia esencial separa PCA de FLD?
3. ¿por qué LDA puede necesitar regularización en alta dimensión?

## Diapositiva 59. Unificación

Hay una única historia matemática detrás de estos métodos:

- **Mahalanobis:** la covarianza define la métrica;
- **Whitening:** un cambio lineal elimina correlación y escala;
- **PCA:** proyectamos preservando varianza;
- **FLD:** proyectamos preservando separabilidad.

## Diapositiva 60. Próxima Clase

En la próxima clase cambiaremos otra vez de perspectiva.

En lugar de modelar densidades o buscar proyecciones óptimas, se construirán directamente fronteras lineales:

- funciones discriminantes;
- perceptrón;
- convergencia;
- limitaciones geométricas y XOR.
