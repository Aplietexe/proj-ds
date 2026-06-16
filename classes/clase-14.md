---
title: "Heurísticas de Ensamble para Clasificadores Inestables"
---

## Diapositiva 1

**Portada**

- Heurísticas de ensamble para clasificadores inestables
- Ciencia de Datos
- FaMAF
- Clase 14 - 2026-05-19

## Diapositiva 2. Hoja de Ruta

La clase se organiza en tres bloques:

1. **De la inestabilidad a la agregación**
2. **Decorrelación y bosques aleatorios**
3. **Boosting como corrección secuencial**

## Diapositiva 3. USPS: La Crisis Combinatoria y la Inestabilidad de CART

![Escena de clasificación postal con sobres manuscritos](figures/clase-14/fig-03-mailroom.png){width=100%}

## Diapositiva 4. USPS: La Crisis Combinatoria y la Inestabilidad de CART

A finales de la década de 1980, el Servicio Postal de EE.UU. (USPS) colapsó ante la imposibilidad de clasificar manualmente millones de códigos postales escritos a mano. Las imágenes se digitalizaron en matrices de $16\times 16$ píxeles, definiendo un espacio de características estructurado en $\mathcal{X}\subset\mathbb{R}^{256}$.

**La Patología del Estimador Local (Alta Varianza)**

Los árboles de decisión individuales (CART) calculan particiones ortogonales del espacio maximizando localmente la ganancia de información. No obstante, pequeñas variaciones en el trazo manuscrito alteran la raíz del árbol, propagando un error estructural a lo largo de toda la arquitectura jerárquica:

$$
g_T(x)=\sum_{t\in L(T)} c_t\,\mathbb{I}\{x\in A_t\}.
$$

Un desplazamiento infinitesimal de intensidad en un único píxel central provocaba que un dígito "7" fuera clasificado catastróficamente como un "4".

## Diapositiva 5. De la Inestabilidad a la Agregación

**Sección:** De la inestabilidad a la agregación.

## Diapositiva 6. Costo de la Flexibilidad Local

En la clase anterior vimos que un árbol de decisión define una regla

$$
g_T(x)=\sum_{t\in L(T)} c_t\,\mathbb{I}\{x\in A_t\},
$$

donde las hojas $A_t$ son regiones rectangulares obtenidas por partición recursiva. La notación $\mathbb{I}\{\cdot\}$ representa la función indicadora: vale 1 cuando el evento entre llaves ocurre y vale 0 en caso contrario.

- La frontera puede adaptarse a geometrías muy complejas.
- Las interacciones entre variables aparecen sin ser especificadas de antemano.
- La regla es interpretable como una secuencia de decisiones locales.

**Problema estadístico**

La misma capacidad de adaptación que reduce sesgo puede inducir alta varianza: pequeñas perturbaciones de $\mathcal{D}_n$ alteran nodos tempranos y cambian todo el árbol.

## Diapositiva 7. Clasificador Aprendido como Variable Aleatoria

![Interfaz ilustrativa de un árbol aprendido como variable aleatoria](figures/clase-14/fig-07-variable-aleatoria.png){width=100%}

## Diapositiva 8. Clasificador Aprendido como Variable Aleatoria

**Nueva idea:** fijemos un algoritmo de aprendizaje $\mathcal{A}$ y una muestra aleatoria

$$
\mathcal{D}_n=\{(x_i,y_i)\}_{i=1}^n,
\qquad
(x_i,y_i)\sim P_{X,Y}.
$$

El clasificador entrenado

$$
\widehat{g}_n=\mathcal{A}(\mathcal{D}_n)
$$

es una variable aleatoria funcional de la muestra.

Para un punto fijo $x\in\mathcal{X}$, la predicción $\widehat{g}_n(x)$ también es aleatoria.

**Inestabilidad**

Diremos informalmente que $\mathcal{A}$ es inestable si la distribución de $\widehat{g}_n(x)$ cambia apreciablemente cuando reemplazamos una pequeña fracción de $\mathcal{D}_n$.

## Diapositiva 9. Por Qué los Árboles son Inestables

La construcción de CART es recursiva y codiciosa:

$$
s^\star(t)=\arg\max_{s\in S_t}\Delta i(s,t).
$$

- Si dos cortes tienen ganancias de impureza similares, pequeñas fluctuaciones pueden invertir el orden.
- Un cambio en la raíz modifica la partición completa y altera los nodos descendientes.
- Hojas pequeñas producen estimaciones $\widehat{p}_{tk}$ con alta variabilidad.

**Consecuencia**

Un árbol profundo puede tener bajo error de entrenamiento pero alta sensibilidad muestral. Esta es exactamente la situación en la que un ensamble puede mejorar el desempeño.

**Idea de "consenso"**

Si un árbol individual es un estimador ruidoso de la regla de Bayes, podemos intentar promediar varios árboles entrenados en versiones perturbadas de los datos.

## Diapositiva 10. Heurísticas de Ensamble y Riesgo de Clasificación

Los métodos que siguen son **heurísticos** en un sentido preciso:

- no resuelven en forma cerrada la minimización de

$$
R(g)=\mathbb{P}(g(X)\ne Y),
$$

- pero construyen aproximaciones sistemáticas mediante **agregación**, **aleatorización** o **corrección secuencial**,
- y su análisis combina resultados de estabilidad, descomposición sesgo-varianza y minimización de pérdidas.

**Principio metodológico**

En lugar de fijar una sola regla discriminante, se considera una familia de clasificadores base y se define sobre ella un operador de agregación.

Probemos...

## Diapositiva 11. Bootstrap: Muestra Observada y Pseudo-Muestras

El aprendizaje supervisado solo observa una muestra

$$
\mathcal{D}_n=\{(x_i,y_i)\}_{i=1}^n
$$

extraída de una distribución desconocida.

**Pregunta**

¿Cómo aproximar la variabilidad del clasificador respecto de nuevas muestras de entrenamiento si solo observamos una?

El bootstrap responde generando pseudo-muestras

$$
\mathcal{D}_n^{\ast 1},\mathcal{D}_n^{\ast 2},\ldots,\mathcal{D}_n^{\ast B}
$$

mediante remuestreo con reemplazo desde $\mathcal{D}_n$. Una muestra bootstrap $\mathcal{D}_n^\ast$ se obtiene eligiendo $n$ veces con reemplazo de entre las observaciones originales.

Formalmente,

$$
\mathcal{D}_n^\ast=\{(x_{I_1},y_{I_1}),\ldots,(x_{I_n},y_{I_n})\},
$$

donde

$$
I_1,\ldots,I_n \overset{\text{i.i.d.}}{\sim}\operatorname{Unif}\{1,\ldots,n\}.
$$

- Algunas observaciones se repiten.
- Otras no aparecen.
- Cada $\mathcal{D}_n^\ast$ define una perturbación aleatoria de entrenamiento inducida por la distribución empírica.

## Diapositiva 12. Cuántos Puntos Quedan Fuera

Para una observación fija $(x_i,y_i)$,

$$
\mathbb{P}\left((x_i,y_i)\notin\mathcal{D}_n^\ast\right)
=
\left(1-\frac{1}{n}\right)^n.
$$

Luego,

$$
\left(1-\frac{1}{n}\right)^n
\to
e^{-1}
\approx
0.368.
$$

- Aproximadamente el $63.2\%$ de los puntos aparece al menos una vez en una muestra bootstrap.
- Aproximadamente el $36.8\%$ queda fuera.

**Interpretación**

Este subconjunto excluido es la base del error *out-of-bag*, que actúa como un conjunto de validación interno.

## Diapositiva 13. Promedio Sobre Perturbaciones Muestrales

Si $\widehat{g}^{\ast b}=\mathcal{A}(\mathcal{D}_n^{\ast b})$ es un clasificador base, el clasificador final es el promedio respecto de las perturbaciones de entrenamiento:

$$
\overline{g}_B(x)
=
\arg\max_k
\sum_{b=1}^B
\mathbb{I}\{\widehat{g}_b(x)=\omega_k\}.
$$

Es decir, la votación mayoritaria: elijo la clase que más coincidencias tiene en todas las realizaciones bootstrap.

Análogamente en regresión, si tenemos un regresor $\widehat{f}_b^\ast=\mathcal{A}(\mathcal{D}_n^{\ast b})$, entonces

$$
\overline{f}_B(x)
=
\frac{1}{B}
\sum_{b=1}^B
\widehat{f}_b(x).
$$

Es decir, derivamos el promedio de todas las estimaciones individuales.

**Interpretación estadística**

El agregado aproxima la esperanza del algoritmo respecto de perturbaciones muestrales. El beneficio principal es la estabilización de la regla aprendida, no la mejora uniforme de cada clasificador individual.

## Diapositiva 14. Definición de Bagging

*Bagging* significa *bootstrap aggregating*. Se compone de dos pasos:

1. Generar muestras bootstrap $\mathcal{D}_n^{\ast 1},\ldots,\mathcal{D}_n^{\ast B}$.
2. Entrenar un clasificador base $\widehat{g}_b$ en cada una y agregarlos.

En clasificación:

$$
\widehat{g}_{\text{bag}}(x)
=
\arg\max_k
\sum_{b=1}^B
\mathbb{I}\{\widehat{g}_b(x)=\omega_k\}.
$$

En regresión:

$$
\widehat{f}_{\text{bag}}(x)
=
\frac{1}{B}
\sum_{b=1}^B
\widehat{f}_b(x).
$$

## Diapositiva 15. Condiciones Bajo las Cuales Bagging es Efectivo

Si el clasificador base es estable, entonces

$$
\widehat{g}_b(x)\approx \widehat{g}_{b'}(x)
$$

para la mayoría de las réplicas bootstrap, y el promedio aporta poco.

**Condición favorable**

Bagging es especialmente útil cuando el clasificador base tiene:

- baja o moderada correlación entre réplicas;
- alta varianza;
- y bajo sesgo relativo.

Los árboles profundos satisfacen estas condiciones mucho mejor que clasificadores lineales regulares.

## Diapositiva 16. Análisis de Varianza del Promedio

Sea $Z_1,\ldots,Z_B$ una familia con

$$
\operatorname{Var}(Z_b)=\sigma^2,
\qquad
\operatorname{Corr}(Z_b,Z_{b'})=\rho
\quad
(b\ne b').
$$

Entonces

$$
\operatorname{Var}\left(
\frac{1}{B}\sum_{b=1}^B Z_b
\right)
=
\rho\sigma^2+\frac{1-\rho}{B}\sigma^2.
$$

- Si $\rho=1$, el promedio no reduce varianza.
- Si $\rho<1$, el promedio sí reduce varianza.
- Si además $B$ es grande, el término $\frac{1-\rho}{B}\sigma^2$ se vuelve pequeño.

**Variables para reducir la varianza**

La reducción de varianza depende tanto del número de modelos como de su correlación.

## Diapositiva 17. Efecto Sobre el Sesgo

En regresión, si cada predictor individual satisface

$$
\mathbb{E}[\widehat{f}_b(x)]\approx m(x),
$$

entonces el promedio cumple

$$
\mathbb{E}[\widehat{f}_{\text{bag}}(x)]\approx m(x).
$$

- Bagging no está diseñado para reducir sesgo sistemáticamente.
- Su ganancia principal proviene de estabilizar un estimador inestable.
- En clasificación, la votación puede modificar levemente la frontera, pero la mejora dominante sigue siendo varianza.

**Interpretación estadística**

Bagging transforma un clasificador de alta dispersión en un estimador promedio más robusto.

## Diapositiva 18. Bagging: Efecto Sobre el Sesgo

![Efecto de bagging sobre realizaciones bootstrap y voto mayoritario](figures/clase-14/fig-18-bagging-sesgo.png){width=100%}

## Diapositiva 19. Votación Mayoritaria y Promedio de Posteriores

Si cada clasificador base entrega posteriores estimadas $\widehat{p}_{bk}(x)$, podemos combinar de dos formas:

**Votación mayoritaria**

$$
\widehat{g}_{\text{hard}}(x)
=
\arg\max_k
\sum_{b=1}^B
\mathbb{I}\{\widehat{g}_b(x)=\omega_k\}.
$$

**Votación suave**

$$
\widehat{g}_{\text{soft}}(x)
=
\arg\max_k
\frac{1}{B}
\sum_{b=1}^B
\widehat{p}_{bk}(x).
$$

La segunda forma es más cercana a la regla de Bayes, pero requiere que las posteriores estimadas por los clasificadores base sean comparables y suficientemente estables.

## Diapositiva 20. Algoritmo de Bagging

**Algoritmo de bagging para clasificación**

1. Dado $\mathcal{D}_n$, fijar el número de réplicas $B$.
2. Para $b=1,\ldots,B$:
   - generar $\mathcal{D}_n^{\ast b}$ por bootstrap;
   - ajustar un árbol $\widehat{g}_b$ sin poda agresiva;
   - almacenar la predicción o las probabilidades por clase.
3. Devolver la regla agregada por votación o promedio.

**Elección del árbol base**

Se prefieren árboles grandes o débilmente regularizados: si el clasificador base es demasiado rígido, se reduce la diversidad útil del ensamble.

## Diapositiva 21. Knowledge Check I: Inestabilidad y Agregación (Bagging)

**Contexto analítico**

Bagging aproxima la esperanza del algoritmo respecto a perturbaciones de la muestra de entrenamiento mediante la distribución empírica $\widehat{P}_n$ (principio *plug-in*).

**Preguntas**

1. **Estabilidad e inoperancia:** si aplicamos el operador de Bagging a un clasificador lineal obtenido mediante mínimos cuadrados ordinarios (OLS) en un entorno donde $n\gg p$, ¿espera usted que el error de generalización varíe significativamente respecto al estimador base único? Justifique en términos de la distribución funcional de $\widehat{g}_n(x)$.
2. **La paradoja de la votación suave:** al implementar votación suave

$$
\widehat{g}_{\text{soft}}(x)
=
\arg\max_k
\frac{1}{B}
\sum_b
\widehat{p}_{bk}(x),
$$

se asume que las probabilidades a posteriori estimadas por las hojas son estables. ¿Por qué un árbol profundo sin podar puede distorsionar esta agregación a pesar de tener un bajo sesgo marginal?

## Diapositiva 22. USPS: La Asamblea de Bell Labs y la Decorrelación de Breiman

Para mitigar la inestabilidad de un solo árbol, Leo Breiman introdujo Bagging (1994), construyendo una asamblea democrática mediante remuestreo Bootstrap $\mathcal{D}_n^\ast\sim\widehat{P}_n$. Sin embargo, en el problema postal, los píxeles adyacentes altamente informativos introducían una colinealidad crítica entre los árboles $(\rho\to 1)$.

**Solución analítica: inyección de aleatoriedad subespacial**

La varianza del promedio de $B$ clasificadores con varianza marginal $\sigma^2$ y correlación par a par $\rho$ está acotada por:

$$
\operatorname{Var}(\overline{Z})
=
\rho\sigma^2+\frac{1-\rho}{B}\sigma^2.
$$

En 2001, Breiman formaliza Random Forests:

- En lugar de evaluar las $p=256$ dimensiones en cada nodo, se restringe la optimización del *split* a un subconjunto aleatorio de cardinalidad $m=\lfloor\sqrt{p}\rfloor=16$.
- Esto fuerza analíticamente a que $\rho\to 0$, logrando que $\lim_{B\to\infty}\operatorname{Var}(\overline{Z})\approx 0$ y estabilizando la frontera de decisión en entornos de alta dimensionalidad.

$$
\text{random forests}
\leftarrow
\text{CART}+\text{bagging}+\text{subespacios aleatorios de las variables}
$$

## Diapositiva 23. Decorrelación y Bosques Aleatorios

**Sección:** Decorrelación y bosques aleatorios.

## Diapositiva 24. El Límite de Bagging Puro

Bagging promedia clasificadores entrenados sobre muestras distintas, pero todos usan:

- la misma familia de hipótesis;
- el mismo conjunto de variables;
- y un criterio de *split* similar.

**Problema**

Si algunas variables predictoras son muy dominantes, muchos árboles bootstrap elegirán cortes iniciales parecidos. Entonces las predicciones quedan altamente correlacionadas.

Alta correlación implica que la reducción de varianza del promedio se estanca.

![Árboles bootstrap con cortes iniciales correlacionados](figures/clase-14/fig-24-limite-bagging.png){width=80%}

## Diapositiva 25. Varianza del Ensamble y Correlación

Retomemos

$$
\operatorname{Var}\left(
\frac{1}{B}\sum_{b=1}^B Z_b
\right)
=
\rho\sigma^2+\frac{1-\rho}{B}\sigma^2.
$$

En el límite $B\to\infty$ obtenemos

$$
\lim_{B\to\infty}
\operatorname{Var}\left(
\frac{1}{B}\sum_{b=1}^B Z_b
\right)
=
\rho\sigma^2.
$$

**Conclusión**

Aumentar el número de árboles no basta. También debemos reducir la correlación $\rho$ entre ellos.

Esta es la motivación central de los Random Forests.

## Diapositiva 26. Diversidad Útil

En un ensamble, la diversidad no significa arbitrariedad total.

- Si todos los clasificadores son idénticos, el promedio no aporta.
- Si todos son muy malos, la diversidad tampoco ayuda.
- Lo útil es combinar clasificadores razonables cuyos errores no coincidan sistemáticamente.

**Objetivo**

Construir una familia $\{\widehat{g}_b\}_{b=1}^B$ con buen desempeño marginal y errores parcialmente desacoplados.

El diseño de Random Forest logra esto introduciendo **aleatoriedad controlada en el espacio de variables**.

## Diapositiva 27. Subespacios Aleatorios

En vez de permitir que cada nodo examine todas las variables

$$
x_1,\ldots,x_p,
$$

se elige un subconjunto aleatorio

$$
\mathcal{J}_t\subset\{1,\ldots,p\},
\qquad
|\mathcal{J}_t|=m.
$$

El mejor *split* del nodo se busca sólo entre variables de $\mathcal{J}_t$. Por ejemplo, de $p=100$ variables elijo $m=20$ y construyo el árbol solamente con esas variables.

![Ejemplo de cortes al restringir el subespacio de variables](figures/clase-14/fig-27-subespacios-aleatorios.png){width=70%}

**Efecto**

Variables muy fuertes no monopolizan todos los cortes iniciales y árboles diferentes exploran geometrías distintas de la frontera.

## Diapositiva 28. Compromiso Sesgo-Varianza en la Decorrelación

Restringir variables por nodo puede empeorar levemente el mejor corte local.

- Cada árbol individual puede aumentar su sesgo.
- Pero el ensamble completo reduce de manera más fuerte la varianza.
- El resultado global suele ser una disminución del error predictivo.

**Compromiso estadístico**

Un bosque puede estar compuesto por árboles individualmente menos precisos que los de bagging puro, pero cuyo promedio resulta superior porque la disminución de correlación domina el deterioro marginal de cada árbol.

## Diapositiva 29. Definición Operativa de Random Forest

Un Random Forest para clasificación construye árboles $\widehat{g}_1(x)=T_1,\ldots,\widehat{g}_B(x)=T_B$ de la siguiente manera:

**Algoritmo**

1. Generar una muestra bootstrap $\mathcal{D}_n^{\ast b}$.
2. Crecer un árbol grande sobre $\mathcal{D}_n^{\ast b}$.
3. En cada nodo, elegir al azar $m$ variables candidatas.
4. Escoger el mejor *split* sólo entre esas $m$ variables.
5. Repetir hasta alcanzar el criterio de detención.

La predicción final es

$$
\widehat{g}_{\text{RF}}(x)
=
\arg\max_k
\sum_{b=1}^B
\mathbb{I}\{\widehat{g}_b(x)=\omega_k\}.
$$

## Diapositiva 30. Error Out-of-Bag

Para cada árbol $T_b$, alrededor del $36.8\%$ de las observaciones no participa en $\mathcal{D}_n^{\ast b}$. Denotemos ese conjunto por $\mathcal{D}_{n,\text{OOB}}^{(b)}$.

Para una observación $x_i$, recolectamos predicciones de los árboles en los que $i$ quedó fuera y definimos una predicción agregada OOB:

$$
\widehat{g}_{\text{OOB}}(x_i).
$$

Entonces el error OOB es

$$
\widehat{R}_{\text{OOB}}
=
\frac{1}{n}
\sum_{i=1}^n
\mathbb{I}\{\widehat{g}_{\text{OOB}}(x_i)\ne y_i\}.
$$

**Validación OOB**

Permite estimar error de generalización sin separar explícitamente un conjunto de validación externo.

## Diapositiva 31. Importancia de Variables por Permutación

Una medida clásica de importancia consiste en:

1. calcular el error OOB del bosque;
2. permutar aleatoriamente los valores de una variable $x_j$ en las observaciones OOB;
3. recalcular el error;
4. medir el incremento de error.

**Definición**

$$
\operatorname{Imp}(j)
=
\widehat{R}_{\text{OOB},\operatorname{perm}(j)}
-
\widehat{R}_{\text{OOB}}.
$$

Si permutar $x_j$ deteriora mucho la predicción, esa variable es importante para el bosque.

## Diapositiva 32. Árboles Individuales

![Fronteras de árboles individuales y del bosque completo](figures/clase-14/fig-32-arboles-individuales.png){width=100%}

## Diapositiva 33. Parámetros Principales del Bosque

Los hiperparámetros más importantes son:

- número de árboles $B$ (bootstrap);
- número de variables por nodo $m$ (subespacio);
- tamaño mínimo de hoja;
- profundidad máxima;
- criterio de impureza, por ejemplo Gini o entropía.

**Regla empírica: $m$**

En clasificación suele elegirse

$$
m\approx \sqrt{p},
$$

mientras que en regresión son comunes valores del orden de $p/3$.

**Tarea:** modificar un notebook cambiando $m$ y observar el efecto.

## Diapositiva 34. Parámetros Principales del Bosque

**Regla empírica: $B$**

$B$ debe ser tal que el error de generalización se estabilice.

![Efecto del número de estimadores en train, test y OOB](figures/clase-14/fig-34-efecto-n-estimators.png){width=70%}

Estas reglas no son universales, pero expresan el compromiso entre calidad individual y diversidad.

**Implementación en sklearn**

## Diapositiva 35. Bosque como Agregado de Particiones Aleatorias

Cada árbol $T_b$ induce una partición

$$
\mathcal{X}
=
A_{b1}\cup\cdots\cup A_{bM_b}.
$$

La predicción del bosque agrega muchas particiones rectangulares distintas.

**Interpretación geométrica**

Un árbol individual produce una frontera escalonada y dependiente de cortes concretos. El bosque promedia muchas fronteras escalonadas y genera una aproximación más estable de la regla de Bayes.

El efecto no es suavidad analítica, sino **estabilidad geométrica por promedio**.

## Diapositiva 36. Posteriores Empíricas en el Bosque

Si el árbol $b$ entrega una estimación de posterior para la clase $k$, $\widehat{p}_{bk}(x)$, el bosque puede definir

$$
\widehat{p}_{k}^{\text{RF}}(x)
=
\frac{1}{B}
\sum_{b=1}^B
\widehat{p}_{bk}(x).
$$

Luego

$$
\widehat{g}_{\text{RF}}(x)
=
\arg\max_k
\widehat{p}_{k}^{\text{RF}}(x).
$$

- Esta forma lo conecta directamente con la regla de Bayes.
- El bosque puede interpretarse como un estimador no paramétrico de las posteriores.
- La agregación reduce la inestabilidad de las probabilidades de hoja.

## Diapositiva 37. Complejidad Computacional

El costo del bosque crece con:

- el número de árboles $B$;
- el número de observaciones $n$;
- el número de variables $p$;
- la profundidad media de los árboles.

**Ventaja práctica**

Los árboles del bosque se entrenan casi independientemente y pueden paralelizarse fácilmente. Esta propiedad distingue a bagging y random forests de boosting (próxima sección).

## Diapositiva 38. Comparación Conceptual: Bagging Versus Random Forest

| Aspecto | Bagging | Random Forest |
|---|---|---|
| Bootstrap | Sí | Sí |
| Submuestreo de variables | No | Sí |
| Objetivo principal | Reducir varianza | Reducir varianza y correlación |
| Diversidad entre árboles | Moderada | Mayor |
| Árboles base | Profundos | Profundos |

**Síntesis**

Random Forest es bagging más una inyección adicional de aleatoriedad estructurada.

## Diapositiva 39. Importancia por Descenso de Impureza

Otra medida resume cuánto reduce la impureza una variable a lo largo del bosque:

$$
\operatorname{MDI}(j)
=
\sum_{b=1}^B
\sum_{t:v(t)=j}
\frac{N_t}{n}\Delta i(t),
$$

donde $v(t)$ indica la variable usada en el nodo $t$.

- Es simple de computar.
- Está alineada con el criterio interno de entrenamiento.
- Puede sesgarse hacia variables continuas o con muchos puntos de corte.

Por eso, para interpretación inferencial suele preferirse la importancia por permutación.

## Diapositiva 40. Knowledge Check II: Decorrelación y Bosques Aleatorios

**Contexto analítico**

La varianza asintótica del promedio de $B$ clasificadores idénticamente distribuidos está gobernada estrictamente por la correlación par a par:

$$
\lim_{B\to\infty}\operatorname{Var}(\overline{Z})=\rho\sigma^2.
$$

**Preguntas**

1. **El límite de la inyección de aleatoriedad:** si reducimos la cardinalidad del subespacio aleatorio de variables en cada nodo al límite extremo $m=1$, forzamos analíticamente a que la correlación tienda a cero $(\rho\to 0)$ [?, ?]. ¿Por qué esta condición no garantiza que el error del bosque converja a cero cuando $B\to\infty$? Relacione con el compromiso sesgo-varianza de Breiman.
2. **MDI vs. permutación:** explique formalmente por qué la Importancia por Descenso de Impureza (MDI) presenta un sesgo sistemático hacia variables continuas con alta cardinalidad de valores únicos, mientras que la importancia por permutación sobre el conjunto Out-of-Bag (OOB) mitiga esta distorsión estructural.

## Diapositiva 41. Propiedades Inferenciales y Transición a Boosting

**Random forests**

- Buen desempeño predictivo con poca ingeniería manual de variables.
- Maneja interacciones y no linealidades de forma automática.
- Es robusto frente a ruido moderado y transformaciones monótonas.
- La interpretación es menor que en un árbol individual.
- Las probabilidades estimadas pueden requerir calibración.

Random Forest representa la primera gran heurística moderna que transforma un clasificador base inestable en un predictor competitivo mediante agregación y aleatorización.

## Diapositiva 42. USPS: Grupos de Especialistas y la Convergencia al Margen Bayesiano

A pesar del éxito de Random Forests, ciertos dígitos sumamente ambiguos, por ejemplo un "8" deformado que asemeja un "3", persistían como errores sistemáticos insensibles a la votación mayoritaria tradicional. Nace entonces el enfoque aditivo secuencial de AdaBoost (Freund & Schapire, 1995).

**Resultado teórico fundamental: maximización del margen**

En Bell Labs se observó un fenómeno que desafiaba la teoría clásica: el error de prueba de AdaBoost continuaba descendiendo de forma asintótica incluso después de que el error de entrenamiento alcanzaba cero.

- **Explicación formal:** al minimizar la pérdida exponencial $L(y,F(x))=\exp(-yF(x))$, el algoritmo maximiza de forma implícita el margen de clasificación de los vectores más difíciles, convergiendo a la mitad del *log-odds* de las probabilidades a posteriori de la regla óptima de Bayes:

$$
F^\star(x)
=
\frac{1}{2}
\ln
\frac{P(\omega_1\mid x)}{P(\omega_2\mid x)}.
$$

## Diapositiva 43. Propiedades Inferenciales y Transición a Boosting

**Idea de Freund & Schapire 1995**

¿Qué ocurre si, en lugar de promediar modelos construidos en paralelo, construimos una secuencia de modelos en la que cada uno corrige errores del anterior?

Esta es la motivación de **boosting**:

- reemplazar el promedio casi independiente por una construcción secuencial;
- convertir una familia de aprendices débiles en una regla discriminante fuerte;
- reinterpretar la agregación como optimización en un espacio funcional.

![Escena ilustrativa de Bell Labs y AdaBoost](figures/clase-14/fig-43-bell-labs-adaboost.png){width=70%}

Bell Labs implementó AdaBoost y encontraron que el error de validación seguía decreciendo...

## Diapositiva 44. Boosting como Corrección Secuencial

**Sección:** Boosting como corrección secuencial.

## Diapositiva 45. Motivación Formal: El Comité de Especialistas

**Intuición mnemónica**

Considere un problema complejo de decisión dicotómica. Un único clasificador base, por ejemplo un médico generalista, posee un alto sesgo.

- **Bagging:** agrega especialistas en paralelo para promediar y reducir la varianza.
- **Boosting:** opera de forma secuencial. Cada nuevo clasificador orienta de manera estricta su capacidad geométrica hacia los residuos o errores del clasificador precedente.

**Propósito del enfoque**

Construir un clasificador fuertemente consistente a partir de una combinación lineal ponderada de hipótesis de alta varianza o alto sesgo local, optimizando un funcional de riesgo empírico.

## Diapositiva 46. Dos Filosofías de Ensamble

| Aspecto | Bagging / RF | Boosting |
|---|---|---|
| Construcción | Paralela | Secuencial |
| Objetivo dominante | Reducir varianza | Reducir sesgo y error residual |
| Dependencia entre modelos | Débil | Fuerte |
| Modelo base típico | Árbol profundo | Árbol pequeño / stump |

**Cambio de perspectiva**

Boosting no parte de aprendices potentes e inestables, sino de aprendices débiles que son apenas mejores que el azar, pero cuya combinación produce una regla discriminante de alta capacidad.

## Diapositiva 47. Formulación en el Espacio de Funciones

Sea $\mathcal{D}=\{(x_1,y_1),\ldots,(x_n,y_n)\}$ el conjunto de entrenamiento, con $x_i\in\mathbb{R}^d$ y etiquetas $y_i\in\mathcal{Y}=\{-1,+1\}$. Definimos el clasificador final $G(x)$ mediante una expansión aditiva en un espacio funcional de Hilbert $\mathcal{H}$:

$$
f_M(x)
=
\sum_{m=1}^M
\alpha_m h_m(x)
\Longrightarrow
G(x)=\operatorname{sign}(f_M(x))
\quad
\text{(decisión final)}.
$$

donde:

- $h_m(x)\in\mathcal{H}$ representa la hipótesis o clasificador base en la iteración $m$.
- $h_m:\mathcal{X}\to\{-1,+1\}$ es un **clasificador base débil**.
- $\alpha_m\in\mathbb{R}^+$ es el coeficiente de confianza asignado a dicha hipótesis.

El ensamble ya no es una simple mayoría no ponderada: cada aprendiz recibe un peso $\alpha_m$ que depende de su calidad y de la etapa del algoritmo.

![Clasificador débil de un solo corte](figures/clase-14/fig-47-stump-clasificador.png){width=45%}

Un clasificador débil. Típicamente se elige un árbol de un solo nivel o *stump*.

![Tocón de árbol usado como analogía de decision stump](figures/clase-14/fig-47-stump-photo.png){width=35%}

## Diapositiva 48. Aprendiz Débil

La noción clásica de *weak learner* supone que, respecto de una distribución dada sobre los ejemplos, el clasificador $h$ satisface

$$
\mathbb{P}(h(X)\ne Y)
<
\frac{1}{2}-\gamma
$$

para alguna ventaja $\gamma>0$.

- No se exige gran precisión absoluta.
- Sí se exige desempeño ligeramente mejor que azar.
- El poder del método reside en recombinar muchos clasificadores modestos.

En la práctica, un *decision stump* suele ser el ejemplo paradigmático de aprendiz débil. En boosting, cada *weak learner* se entrena sobre una distribución de pesos que enfatiza los ejemplos mal clasificados por los aprendices anteriores, buscando corregir sus errores residuales.

![Comparación de tres aprendices de distinta complejidad](figures/clase-14/fig-48-aprendices-mini.png){width=50%}

## Diapositiva 49. Aprendiz Débil

![Secuencia de aprendices débiles de AdaBoost](figures/clase-14/fig-49-aprendices-debiles.png){width=100%}

## Diapositiva 50. Aprendiz Débil

![Evolución del consenso del ensamble a partir de aprendices débiles](figures/clase-14/fig-50-consenso-aprendiz-debil.png){width=80%}

## Diapositiva 51. Pérdidas Sustitutas y Modelo Aditivo por Etapas

La pérdida 0-1 es discontinua y difícil de optimizar directamente. Por ello boosting trabaja con pérdidas sustitutas convexas y con una expansión aditiva construida por etapas.

En binario con $y\in\{-1,+1\}$:

$$
L_{\exp}(y,f(x))=\exp(-y f(x)).
$$

**Riesgo empírico exponencial**

$$
\widehat{R}_{\exp}(f)
=
\frac{1}{n}
\sum_{i=1}^n
\exp(-y_i f(x_i)).
$$

AdaBoost puede interpretarse como un procedimiento que construye $F_M$ minimizando heurísticamente esta cantidad. En cada iteración se actualiza

$$
f_m(x)=f_{m-1}(x)+\alpha_m h_m(x).
$$

- $f_{m-1}$ resume el conocimiento acumulado.
- $h_m$ busca corregir errores remanentes.
- $\alpha_m$ cuantifica cuánto confiar en esa corrección.

**Lectura estructural**

El procedimiento define otra expansión en funciones base, con la particularidad de que las bases no están prefijadas: son aprendidas secuencialmente a partir de la muestra.

## Diapositiva 52. AdaBoost: Ancla Bayesiana de la Pérdida Exponencial

Supongamos dos clases $\omega_1,\omega_2$ y codificación $y=+1$ para $\omega_1$, $y=-1$ para $\omega_2$. Para un valor fijo de $x$, el riesgo condicional asociado a

$$
L_{\exp}(y,f(x))=\exp(-y f(x))
$$

es

$$
\mathcal{R}_{\exp}(f\mid x)
=
P(\omega_1\mid x)e^{-f(x)}
+
P(\omega_2\mid x)e^{f(x)}.
$$

Derivando respecto de $f(x)$:

$$
-P(\omega_1\mid x)e^{-f(x)}
+
P(\omega_2\mid x)e^{f(x)}
=
0.
$$

Por lo tanto,

$$
e^{2f^\star(x)}
=
\frac{P(\omega_1\mid x)}{P(\omega_2\mid x)},
\qquad
f^\star(x)
=
\frac{1}{2}
\ln
\frac{P(\omega_1\mid x)}{P(\omega_2\mid x)}.
$$

La segunda derivada es positiva:

$$
P(\omega_1\mid x)e^{-f}
+
P(\omega_2\mid x)e^f
>
0.
$$

![Pérdida exponencial como cota suave de la pérdida 0-1](figures/clase-14/fig-52-perdida-exponencial.png){width=40%}

**Conexión con la regla de Bayes**

Como

$$
P(\omega_i\mid x)
=
\frac{p(x\mid\omega_i)P(\omega_i)}
{\sum_j p(x\mid\omega_j)P(\omega_j)},
$$

el signo de $f^\star(x)$ coincide con el signo de la razón de posteriores. Minimizar $\mathcal{R}_{\exp}(f)$ preserva, en población, la frontera bayesiana.

## Diapositiva 53. Dinámica del Vector de Pesos $D_m$

El algoritmo induce una secuencia de medidas de probabilidad $D_m$ sobre la muestra $\mathcal{D}$:

1. **Inicialización:** $D_1(i)=1/n$, $\forall i=1,\ldots,n$.
2. **Minimización del error ponderado:** en la iteración $m$, se selecciona $h_m$ tal que:

$$
\varepsilon_m
=
\sum_{i=1}^n
D_m(i)\mathbb{I}(y_i\ne h_m(x_i)).
$$

3. **Actualización de medida:**

$$
D_{m+1}(i)
=
\frac{D_m(i)\exp(-\alpha_m y_i h_m(x_i))}
{Z_m}.
$$

Donde $Z_m$ es la constante de normalización para asegurar que $\sum_i D_{m+1}(i)=1$.

![Evolución de los pesos sobre las observaciones en distintas rondas](figures/clase-14/fig-53-dinamica-pesos.png){width=100%}

## Diapositiva 54. Deducción Formal de $\alpha_m$: Criterio de Pérdida Exponencial

Definimos la función de pérdida exponencial sobre el conjunto de entrenamiento como:

$$
E=
\sum_{i=1}^n
\exp(-y_i f_M(x_i)).
$$

Asumiendo un esquema de optimización secuencial hacia adelante (*forward stagewise*), fijamos los parámetros de las primeras $m-1$ iteraciones y expandimos para la iteración $m$:

$$
f_m(x_i)
=
f_{m-1}(x_i)+\alpha_m h_m(x_i).
$$

Sustituyendo esta expresión en el funcional de error $E$:

$$
\begin{aligned}
E
&=
\sum_{i=1}^n
\exp\left(-y_i[f_{m-1}(x_i)+\alpha_m h_m(x_i)]\right) \\
&=
\sum_{i=1}^n
\exp(-y_i f_{m-1}(x_i))
\exp(-\alpha_m y_i h_m(x_i)).
\end{aligned}
$$

Definiendo el peso intermedio (no normalizado) como $w_i^{(m)}=\exp(-y_i f_{m-1}(x_i))$, reescribimos:

$$
E=
\sum_{i=1}^n
w_i^{(m)}
\exp(-\alpha_m y_i h_m(x_i)).
$$

## Diapositiva 55. Deducción Formal de $\alpha_m$: Partición del Error Empírico

Dado que $y_i\in\{-1,+1\}$ y $h_m(x_i)\in\{-1,+1\}$, el producto condicional $y_i h_m(x_i)$ solo admite dos valores del espacio canónico:

$$
y_i h_m(x_i)
=
\begin{cases}
+1 & \text{si } y_i=h_m(x_i) \quad \text{(Clasificación Correcta)},\\
-1 & \text{si } y_i\ne h_m(x_i) \quad \text{(Clasificación Errónea)}.
\end{cases}
$$

Particionamos la suma del error $E$ en estos dos subconjuntos mutuamente excluyentes:

$$
E
=
\sum_{y_i=h_m(x_i)}
w_i^{(m)}\exp(-\alpha_m)
+
\sum_{y_i\ne h_m(x_i)}
w_i^{(m)}\exp(\alpha_m).
$$

Sumando y restando el término $\sum_{y_i\ne h_m(x_i)} w_i^{(m)}\exp(-\alpha_m)$ para homogeneizar la base:

$$
\begin{aligned}
E
&=
e^{-\alpha_m}
\sum_{i=1}^n w_i^{(m)}
-
e^{-\alpha_m}
\sum_{y_i\ne h_m(x_i)} w_i^{(m)}
+
e^{\alpha_m}
\sum_{y_i\ne h_m(x_i)} w_i^{(m)} \\
&=
e^{-\alpha_m}
\sum_{i=1}^n w_i^{(m)}
+
\left(e^{\alpha_m}-e^{-\alpha_m}\right)
\sum_{y_i\ne h_m(x_i)} w_i^{(m)}.
\end{aligned}
$$

## Diapositiva 56. Deducción Formal de $\alpha_m$: Conexión con la Tasa de Error $\varepsilon_m$

Definimos formalmente la tasa de error ponderada $\varepsilon_m$ en la iteración $m$ como la fracción de masa de probabilidad incorrecta respecto a la distribución actual:

$$
\varepsilon_m
=
\frac{
\sum_{y_i\ne h_m(x_i)} w_i^{(m)}
}{
\sum_{i=1}^n w_i^{(m)}
}
\Longrightarrow
\sum_{y_i\ne h_m(x_i)} w_i^{(m)}
=
\varepsilon_m
\sum_{i=1}^n w_i^{(m)}.
$$

Sustituyendo esta relación en nuestra función de pérdida $E$:

$$
E
=
e^{-\alpha_m}
\sum_{i=1}^n w_i^{(m)}
+
\left(e^{\alpha_m}-e^{-\alpha_m}\right)
\varepsilon_m
\sum_{i=1}^n w_i^{(m)}.
$$

Factorizando la masa total de los pesos constantes $\sum_{i=1}^n w_i^{(m)}$:

$$
E
=
\left(
\sum_{i=1}^n w_i^{(m)}
\right)
\left[
(1-\varepsilon_m)e^{-\alpha_m}
+
\varepsilon_m e^{\alpha_m}
\right].
$$

## Diapositiva 57. Deducción Formal de $\alpha_m$: Condición de Optimalidad

Para hallar el valor óptimo de $\alpha_m$ que minimiza el riesgo, aplicamos la condición de primer orden derivando $E$ respecto a $\alpha_m$ e igualando a cero:

$$
\frac{\partial E}{\partial\alpha_m}
=
\left(
\sum_{i=1}^n w_i^{(m)}
\right)
\left[
-(1-\varepsilon_m)e^{-\alpha_m}
+
\varepsilon_m e^{\alpha_m}
\right]
=
0.
$$

Dado que $\sum_i w_i^{(m)}>0$, el término remanente debe anularse estrictamente:

$$
\varepsilon_m e^{\alpha_m}
=
(1-\varepsilon_m)e^{-\alpha_m}.
$$

Multiplicando ambos miembros por $e^{\alpha_m}$ para despejar el término exponencial:

$$
e^{2\alpha_m}
=
\frac{1-\varepsilon_m}{\varepsilon_m}.
$$

Aplicando el logaritmo natural a ambos lados y multiplicando por el inverso multiplicativo de 2, obtenemos el resultado teórico fundamental:

$$
\alpha_m
=
\frac{1}{2}
\ln
\left(
\frac{1-\varepsilon_m}{\varepsilon_m}
\right).
$$

## Diapositiva 58. ¿Por Qué no Conservar Únicamente el Último Modelo $h_M(x)$?

Dado que $h_M(x)$ se entrena específicamente en los casos remanentes más complejos, ¿se podría inferir que encapsula la máxima especialización del algoritmo? No.

**Razón 1: distorsión de la medida de probabilidad $(D_M)$**

- $h_M(x)$ ha sido optimizado respecto a una distribución $D_M$ masivamente concentrada en las regiones de solapamiento de clases o anomalías.
- Evaluado de forma aislada sobre la distribución real $p(x)$, $h_M(x)$ exhibe un desempeño deficiente debido a que ha ignorado la estructura macroscópica de los datos.

**Razón 2: capacidad restringida del clasificador base (*weak learner*)**

- $h_m\in\mathcal{H}$ posee un sesgo restrictivo, por ejemplo *decision stumps*: $h_m(x)=\operatorname{sign}(x_j-\theta)$.
- Un único clasificador de esta familia es incapaz de generar fronteras de decisión complejas o no lineales, sin importar los pesos asignados a los datos.

**Razón 3: interpretación geométrica de la frontera por capas**

- Cada término $\alpha_m h_m(x)$ actúa como un vector de corrección ortogonal en el espacio de funciones.
- $h_1(x)$ captura la macro-estructura de las densidades de clase; $h_M(x)$ computa el micro-ajuste residual de la frontera.

## Diapositiva 59. Analogía Analítica: Expansiones en Series de Taylor

El enfoque de boosting se puede relacionar con una expansión en una base de funciones que aplican correcciones sucesivas.

Consideremos la aproximación de una función no lineal $f(x)$ mediante su polinomio de Taylor:

$$
f(x)
\approx
P_M(x)
=
\sum_{m=0}^M
\frac{f^{(m)}(a)}{m!}
(x-a)^m.
$$

- El término de orden superior $\frac{f^{(M)}(a)}{M!}(x-a)^M$ está diseñado exclusivamente para corregir el error de curvatura residual que los monomios de menor grado no absorbieron.
- **Conclusión:** descartar $\{h_1,\ldots,h_{M-1}\}$ y utilizar solo $h_M$ equivale a aproximar una función reteniendo únicamente el término de grado $M$. Se pierde la base de la aproximación y la consistencia asintótica del modelo.

## Diapositiva 60. Visualización de la Serie: Estudiantes Débiles

![Visualización de una serie de estudiantes débiles](figures/clase-14/fig-60-estudiantes-debiles.png){width=100%}

## Diapositiva 61. Visualización de la Serie: Consenso

![Visualización del consenso acumulado por la serie](figures/clase-14/fig-61-serie-consenso.png){width=100%}

## Diapositiva 62. Planteo de AdaBoost

Trabajamos con etiquetas $y_i\in\{-1,+1\}$ y pesos sobre observaciones

$$
w_i^{(m)}\ge 0,
\qquad
\sum_{i=1}^n w_i^{(m)}=1.
$$

Inicialmente, $w_i^{(1)}=1/n$. En la iteración $m$:

- se entrena un clasificador $h_m$ usando los pesos actuales;
- se calcula su error ponderado;
- se aumentan los pesos de ejemplos mal clasificados.

El error de $h_m$ bajo los pesos vigentes es

$$
\varepsilon_m
=
\sum_{i=1}^n
w_i^{(m)}
\mathbb{I}\{h_m(x_i)\ne y_i\}.
$$

Para que el paso sea informativo necesitamos $\varepsilon_m<\frac{1}{2}$. Si esto no ocurre, el clasificador no aporta ventaja sobre azar bajo la distribución de pesos actual.

## Diapositiva 63. Peso del Clasificador y Actualización de Pesos

AdaBoost asigna al clasificador $h_m$ el peso

$$
\alpha_m
=
\frac{1}{2}
\log
\left(
\frac{1-\varepsilon_m}{\varepsilon_m}
\right).
$$

- Si $\varepsilon_m$ es pequeño, $\alpha_m$ es grande.
- Si $\varepsilon_m$ se aproxima a $1/2$, $\alpha_m$ tiende a cero.
- Clasificadores mejores reciben mayor influencia en la regla final.

La actualización global queda

$$
F_m(x)=F_{m-1}(x)+\alpha_m h_m(x).
$$

Los pesos de observación se actualizan por

$$
w_i^{(m+1)}
=
\frac{
w_i^{(m)}
\exp(-\alpha_m y_i h_m(x_i))
}{
Z_m
},
$$

donde $Z_m$ normaliza para que sumen 1.

- Si $h_m(x_i)=y_i$, entonces el factor es $e^{-\alpha_m}$.
- Si $h_m(x_i)\ne y_i$, entonces el factor es $e^{\alpha_m}$.

**Interpretación**

La iteración induce una redistribución adaptativa de masa sobre la muestra: los ejemplos mal clasificados por la etapa $m$ reciben mayor influencia en la etapa $m+1$.

## Diapositiva 64. Algoritmo Completo de AdaBoost

1. Inicializar $w_i^{(1)}=1/n$.
2. Para $m=1,\ldots,M$:
   - entrenar $h_m$ con pesos $w_i^{(m)}$;
   - calcular $\varepsilon_m$;
   - definir $\alpha_m=\frac{1}{2}\log\frac{1-\varepsilon_m}{\varepsilon_m}$;
   - actualizar pesos usando la fórmula exponencial.
3. Devolver

$$
g_M(x)
=
\operatorname{sign}
\left(
\sum_{m=1}^M
\alpha_m h_m(x)
\right).
$$

Este es el esquema canónico en clasificación binaria.

## Diapositiva 65. Interpretación Probabilística y Margen

Para un ejemplo $(x_i,y_i)$, el margen del ensamble es

$$
y_iF_M(x_i).
$$

- Es positivo si el ejemplo está bien clasificado.
- Su magnitud mide confianza de la clasificación.
- La pérdida exponencial

$$
e^{-y_iF_M(x_i)}
$$

penaliza fuertemente márgenes pequeños o negativos.

**Mensaje**

AdaBoost no solo intenta clasificar bien, sino empujar ejemplos hacia márgenes positivos grandes.

## Diapositiva 66. De AdaBoost a Gradient Boosting

AdaBoost puede verse como un caso particular de una idea más amplia: construir un modelo aditivo

$$
F_M(x)
=
\sum_{m=1}^M
\nu h_m(x)
$$

minimizando una pérdida diferenciable sobre el conjunto de entrenamiento.

**Paso conceptual**

En lugar de reponderar ejemplos con una regla específica, se sigue aproximadamente una dirección de descenso del riesgo empírico en un espacio funcional.

## Diapositiva 67. Gradient Boosting: Cada Árbol Corrige

Antes de escribir derivadas, conviene fijar la imagen operativa. Pensemos en un golfista que no intenta embocar de un solo golpe: observa dónde quedó la pelota, estima el error restante y ejecuta un golpe más corto para corregir la trayectoria.

**Traducción estadística**

El árbol $h_m$ no intenta resolver otra vez el problema completo de clasificación. Intenta aproximar lo que todavía falta corregir después de $F_{m-1}$.

$$
F_m(x)=F_{m-1}(x)+\nu h_m(x),
\qquad
0<\nu\le 1.
$$

Para pérdida cuadrática, la corrección visible es el residuo ordinario:

$$
r_{im}=y_i-F_{m-1}(x_i).
$$

Para clasificación, el "residuo" será definido por la pérdida: mide la discrepancia entre la etiqueta observada y la evidencia acumulada por $F_{m-1}$.

![Flujo de corrección secuencial en gradient boosting](figures/clase-14/fig-67-flujo-correccion.png){width=55%}

**Idea clave para XGBoost**

XGBoost conserva esta lógica, pero calcula cada corrección usando información local de primer y segundo orden de la pérdida y penaliza explícitamente la complejidad del árbol.

## Diapositiva 68. Descenso Funcional del Gradiente

Sea

$$
\widehat{R}(F)
=
\sum_{i=1}^n
L(y_i,F(x_i)).
$$

El gradiente funcional en los puntos de entrenamiento está dado por

$$
r_{im}
=
-
\left.
\frac{\partial L(y_i,F(x_i))}
{\partial F(x_i)}
\right|_{F=F_{m-1}}.
$$

**Pseudo-residuos**

El algoritmo ajusta el nuevo árbol $h_m$ para predecir los pseudo-residuos $r_{im}$.

Así, cada etapa corrige la dirección local de mayor error según la pérdida elegida.

## Diapositiva 69. Gradient Boosting para Clasificación

Para pérdida logística binaria,

$$
L(y,F)
=
\log(1+e^{-2yF}),
\qquad
y\in\{-1,+1\},
$$

los pseudo-residuos dependen de la discrepancia entre etiqueta observada y probabilidad inducida por $F$.

- El clasificador final sigue siendo aditivo.
- Cada árbol corrige el error de la etapa previa.
- Los árboles base suelen ser poco profundos para controlar complejidad.

**Diferencia con Random Forest**

Random Forest promedia muchos árboles grandes e independientes. Gradient Boosting suma árboles pequeños y dependientes.

## Diapositiva 70. Regularización en Boosting

Boosting puede sobreajustar si se agregan demasiadas etapas o árboles demasiado complejos. Los controles más comunes son:

- *learning rate* o *shrinkage* $\nu\in(0,1]$;
- número total de iteraciones $M$;
- profundidad máxima de cada árbol;
- tamaño mínimo de hoja;
- submuestreo de observaciones.

**Idea**

Un $\nu$ pequeño obliga a muchas correcciones pequeñas, lo que actúa como regularización y suele mejorar generalización.

## Diapositiva 71. XGBoost como Boosting Regularizado

XGBoost extiende gradient boosting con una formulación explícita de costo:

$$
\mathcal{L}^{(m)}
=
\sum_{i=1}^n
L(y_i,\widehat{y}_i^{(m-1)}+f_m(x_i))
+
\Omega(f_m),
$$

donde

$$
\Omega(f)
=
\gamma T
+
\frac{\lambda}{2}
\sum_{j=1}^T
w_j^2
$$

penaliza complejidad del árbol. Aquí $T$ es el número de hojas, $w_j$ el peso de la hoja $j$ y $\gamma,\lambda$ son hiperparámetros de regularización.

- Usa expansión de segundo orden de la pérdida.
- Optimiza pesos de hojas y estructura de *splits*.
- Incorpora regularización explícita y tratamiento eficiente de datos dispersos.

## Diapositiva 72. Comparación Global de Heurísticas

| Método | Árbol base | Dinámica | Mejora dominante |
|---|---|---|---|
| Bagging | Profundo | Paralela | Varianza |
| Random Forest | Profundo | Paralela + aleatoria | Varianza + decorrelación |
| AdaBoost | Débil / stump | Secuencial | Márgenes / error |
| Gradient Boosting | Poco profundo | Secuencial | Riesgo empírico |

**Lectura final**

Las tres familias reutilizan árboles, pero explotan propiedades distintas: inestabilidad, diversidad y corrección secuencial.

## Diapositiva 73. Resumen Matemático

$$
\widehat{g}_{\text{bag}}(x)
=
\arg\max_k
\sum_{b=1}^B
\mathbb{I}\{\widehat{g}_b(x)=\omega_k\}.
$$

$$
\operatorname{Var}\left(
\frac{1}{B}\sum_{b=1}^B Z_b
\right)
=
\rho\sigma^2+\frac{1-\rho}{B}\sigma^2.
$$

$$
\widehat{g}_{\text{RF}}(x)
=
\arg\max_k
\sum_{b=1}^B
\mathbb{I}\{\widehat{g}_b(x)=\omega_k\}
\quad
\text{con subespacios aleatorios}.
$$

$$
F_M(x)
=
\sum_{m=1}^M
\alpha_m h_m(x),
\qquad
g_M(x)=\operatorname{sign}(F_M(x)).
$$

## Diapositiva 74. Análisis Macroscópico de Complejidad Completa

Sea $\mathcal{D}_n=\{(x_i,y_i)\}_{i=1}^n$ el conjunto de entrenamiento con $x_i\in\mathbb{R}^p$. Asumamos un árbol balanceado de profundidad máxima $d\le \lfloor\log_2 n\rfloor$. El costo de evaluar un *split* óptimo bajo criterios informacionales, por ejemplo Entropía o Gini, requiere ordenar los valores marginales, denotando un costo por nivel de $\mathcal{O}(p\cdot n\log_2 n)$.

**Definición formal de órdenes de complejidad en entrenamiento**

En un espacio asintótico, definimos las funciones de transiciones temporales máximas como:

- **CART Base:** $T_{\text{CART}}\in\mathcal{O}(d\cdot p\cdot n\log_2 n)$.
- **Bagging ($B$ árboles):** $T_{\text{Bag}}\in\mathcal{O}(B\cdot d\cdot p\cdot n\log_2 n)$.
- **Random Forest ($B$ árboles, $m$ variables):** $T_{\text{RF}}\in\mathcal{O}(B\cdot d\cdot m\cdot n\log_2 n)$.

**Restricción dimensional (el cuello de botella)**

Donde $m\subset p$. Típicamente en clasificación $m=\lfloor\sqrt{p}\rfloor$ o $m=\lfloor\log_2 p\rfloor$. El factor de aceleración teórica de Random Forest frente a Bagging convencional viene dado estrictamente por la razón del subespacio lineal:

$$
\gamma=\frac{p}{m}.
$$

## Diapositiva 75. Validación Numérica en Escenarios de Alta Dimensionalidad

**Caso de estudio: clasificación ómica / microarrays**

Fijemos un problema bioinformático con estructura masiva:

- Cardinalidad muestral: $n=10^4$.
- Espacio de características (genes): $p=2\times 10^4\approx 20.000$.
- Hiperparámetros de ensamble: $B=500$ árboles, profundidad máxima acotada en $d=10$.

**Evaluación de operaciones elementales relativas** ($n\log_2 n\approx 1.33\times 10^5$):

1. **Bagging tradicional:** requiere procesar el total de atributos en cada nodo.

$$
\text{Operaciones}
\propto
500\cdot 10\cdot (2\times 10^4)\cdot (1.33\times 10^5)
\approx
1.33\times 10^{13}
\text{ operaciones}.
$$

2. **Random Forest**, restringiendo la selección a $m=\lfloor\sqrt{p}\rfloor=\lfloor\sqrt{20000}\rfloor=141$:

$$
\text{Operaciones}
\propto
500\cdot 10\cdot 141\cdot (1.33\times 10^5)
\approx
9.37\times 10^{10}
\text{ operaciones}.
$$

**Conclusión estructural:** Random Forest reduce la carga computacional en un $99.3\%$ ($\gamma\approx 141.8$ veces más veloz) preservando o mejorando el límite del error de generalización gracias a la decorrelación inducida.

## Diapositiva 76. Cierre Conceptual

**De una frontera a una comunidad de fronteras**

La clase 13 mostró que un árbol reemplaza una frontera global por una colección de decisiones locales. La clase 14 extiende esa idea: en vez de confiar en un único árbol, combinamos muchos árboles para aproximar mejor la regla de Bayes.

- Bagging explota inestabilidad para reducir varianza.
- Random Forest agrega decorrelación para mejorar el promedio.
- Boosting construye un clasificador fuerte como suma secuencial de aprendices débiles.

La próxima pregunta natural es cómo comparar, calibrar e interpretar estos ensambles en aplicaciones concretas.

## Diapositiva 77. Referencias Sugeridas

- Duda, Hart y Stork. *Pattern Classification*. Wiley.
- Hastie, Tibshirani y Friedman. *The Elements of Statistical Learning*. Springer.
- Breiman. *Bagging Predictors*. *Machine Learning*.
- Breiman. *Random Forests*. *Machine Learning*.
- Implementación XGBoost.

## Diapositiva 78. Knowledge Check III: Boosting como Corrección Secuencial

**Contexto analítico**

AdaBoost minimiza por etapas el riesgo empírico exponencial

$$
\widehat{R}_{\exp}(F)
=
\frac{1}{n}
\sum_i
\exp(-y_iF(x_i)),
$$

el cual actúa como una cota convexa superior de la pérdida 0-1 [?, ?].

**Preguntas**

1. **Inversión logística del error:** en un escenario de clasificación binaria balanceada, si un clasificador base débil en la iteración $m$ arroja una tasa de error ponderado de $\varepsilon_m=0.72$, ¿por qué el algoritmo no detiene la ejecución ni penaliza el peso del modelo, sino que fortalece la estructura aditiva del ensamble? [?, ?].
2. **Convergencia al margen Bayesiano:** hemos demostrado analíticamente que la función óptima de población minimiza la pérdida exponencial en

$$
F^\star(x)
=
\frac{1}{2}
\ln
\frac{P(\omega_1\mid x)}{P(\omega_2\mid x)}
$$

[?, ?]. Si el conjunto de entrenamiento posee un solapamiento masivo de clases en una región del espacio de características tal que $P(\omega_1\mid x)\approx P(\omega_2\mid x)$, ¿cómo afecta esto a la dinámica de actualización del vector de pesos $D_m$ en las iteraciones subsecuentes? [?, ?, ?].

## Diapositiva 79. El Epílogo en Bell Labs y el Nacimiento de LeNet-1

Hacia fines de los 90, los ensambles demostraron que la combinación lineal de funciones base locales podía aproximar fronteras de decisión altamente complejas. No obstante, tratar las imágenes como vectores planos en $\mathbb{R}^{256}$ destruía la topología bidimensional implícita y las invarianzas por traslación de los caracteres manuscritos.

**El punto de inflexión: extracción de características orientada a la topología**

Para resolver de raíz las dependencias espaciales de los píxeles, Yann LeCun y su equipo en Bell Labs desarrollaron arquitecturas que abandonaban las particiones ortogonales rígidas de CART en favor de operadores de circunvolución local aplicados directamente sobre la matriz de la imagen.

**Conexión con la próxima clase**

La insuficiencia de los hiperplanos paralelos a los ejes para modelar topologías espaciales nos obliga a migrar hacia composiciones continuas de funciones no lineales.

## Diapositiva 80. USPS: Nacimiento de LeNet-1

![Escena de Bell Labs con reconocimiento de dígitos manuscritos](figures/clase-14/fig-80-lenet1.png){width=100%}
