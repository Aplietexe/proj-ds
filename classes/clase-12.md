---
title: "Compromiso Sesgo-Varianza: ¿Cómo Encontrar el Equilibrio?"
---

## Diapositiva 1

**Portada**

- Compromiso sesgo-varianza
- ¿Cómo encontrar el equilibrio?
- Ciencia de Datos
- FaMAF
- Clase 12 - 2026-05-07

## Diapositiva 2. Roles en Ciencia de Datos

La diapositiva muestra una escena humorística con varios roles del ecosistema de datos:
*data scientist*, *data engineer*, *data analyst*, *MLOps engineer*, *machine learning engineer*, *analytics engineer* y *data architect*.

![Roles en ciencia de datos y aprendizaje automático](figures/clase-12/fig-02-data-roles.png){width=100%}

## Diapositiva 3. Hoja de Ruta

La clase se organiza en tres bloques:

1. **Teoría de la decisión bajo desbalance**
   - Acciones sobre los datos
   - Acciones sobre los modelos
2. **Descomposición sesgo-varianza**
3. **Optimización de hiperparámetros**

## Diapositiva 4. ¿Dónde Estamos en la Materia?

Ya sabemos:

- construir models bastante versátiles;
- evaluar su desempeño con métricas adecuadas;
- por qué un modelo con bajo error de entrenamiento puede fallar en producción.

**Preguntas**

- ¿Cómo trato muestras desbalanceadas?
- ¿Cómo ajusto hiperparámetros? ¿Qué busco?

## Diapositiva 5. Teoría de la Decisión Bajo Desbalance

**Sección:** Teoría de la decisión bajo desbalance.

## Diapositiva 6. El Problema del Desbalance Estructural

Sea $\mathcal{D}=\{(x_1,y_1),\ldots,(x_n,y_n)\}$ un conjunto de entrenamiento donde:

$$
P(\omega_{maj}) \gg P(\omega_{min}).
$$

- **Criterio de error mínimo:** un clasificador que minimiza $P(\text{error})$ tenderá a ignorar $\omega_{min}$ si la evidencia de la clase mayoritaria es abrumadora.
- **Frontera de decisión:** en el espacio de características $\mathbb{R}^d$, la frontera se desplaza hacia la región de baja densidad de $\omega_{min}$, eliminando su representatividad.

**Objetivo:** ajustar artificialmente las densidades $\hat p(x\mid \omega_i)$ o las proporciones $P(\omega_i)$ para restaurar la visibilidad de la clase minoritaria en la región de decisión.

## Diapositiva 7. Remuestreo: Mapa General

Para tratar desbalance podemos actuar **sobre los datos**:

1. **Undersampling:** reducir la clase mayoritaria.
2. **Oversampling:** replicar o sintetizar minoritarios.
3. **SMOTE:** generar ejemplos sintéticos por interpolación local.
4. **Regla de oro:** jamás evaluar (*test*) sobre datos remuestreados o manipulados. La evaluación debe reflejar la realidad del despliegue.

O actuar **sobre el algoritmo**:

- **pesos de clase:** asignar según los *priors*;
- **pérdidas asimétricas:** ajustar la función de costo para penalizar más ciertos errores;
- **ajuste de umbral:** decidir $\omega_1$ si $P(\omega_1\mid x)>\tau$ con $\tau\ne 0.5$.

El objetivo no es equilibrar los números, sino equilibrar el riesgo de decisión.

## Diapositiva 8. Undersampling

**Random Undersampling (RUS)**

**Definición:** eliminación aleatoria de muestras del subconjunto $\mathcal{D}_{maj}$ hasta que:

$$
\lvert \mathcal{D}_{maj}\rvert \approx \lvert \mathcal{D}_{min}\rvert.
$$

- **Interpretación:** estamos reduciendo la información disponible para estimar la covarianza $\Sigma_{maj}$ de la clase mayoritaria.
- **Riesgo:** alta varianza en la estimación de la densidad de $\omega_{maj}$. Podemos eliminar muestras críticas, como vectores de soporte, que definen la frontera óptima.
- **Idea:** elimina patrones de la clase mayoritaria, con pérdida de información.
- **Ventajas:** simple, rápido y reduce costo computacional.
- **Riesgo:** perder estructura importante de la clase mayoritaria.

![Esquema de random undersampling](figures/clase-12/fig-08-rus.png)

## Diapositiva 9. Naive Oversampling

**Oversampling "naive" o Random Oversampling (ROS)**

Replicar minoritarios preserva información existente, pero:

- no agrega variabilidad real;
- puede inducir sobreajuste;
- algunos modelos memorizarán esos duplicados;
- produce duplicación exacta de muestras de $\mathcal{D}_{min}$.

Aun así, es una línea base útil y a veces suficiente.

**Problema**

ROS no expande el soporte de la densidad $p(x\mid\omega_{min})$. Simplemente aumenta el peso de puntos específicos, lo que en términos de *bias-variance* conduce a un sobreajuste (*high variance*) masivo. La frontera de decisión se "fractura" para rodear puntos duplicados.

![Esquema de random oversampling](figures/clase-12/fig-09-ros.png)

## Diapositiva 10. SMOTE

**SMOTE: Synthetic Minority Oversampling Technique**

Crea patrones sintéticos interpolando los ya conocidos. Para un ejemplo minoritario $x_i$ y un vecino minoritario $x_j$, construye:

$$
x_{\text{new}} = x_i+\lambda(x_j-x_i),
\qquad
\lambda\sim U(0,1).
$$

En lugar de duplicar puntos, crea ejemplos sintéticos en segmentos locales de la nube minoritaria.

**Algoritmo (Chawla et al., 2002):** para cada $x_i\in\mathcal{D}_{min}$:

1. Seleccionar un vecino cercano $x_{z_i}\in k\text{-NN}(x_i)$.
2. Generar una muestra sintética:

$$
x_{\text{new}} = x_i+\delta(x_{z_i}-x_i),
\qquad
\delta\in[0,1].
$$

**Interpretación geométrica:** estamos asumiendo que el subespacio que une dos muestras de la misma clase también pertenece a dicha clase, es decir, una propiedad de convexidad local.

![Esquema de generación SMOTE](figures/clase-12/fig-10-smote.png)

## Diapositiva 11. ADASYN

**ADASYN: Muestreo Adaptativo Sintético**

Difiere de SMOTE en la distribución de generación:

- calcula un ratio de dificultad $r_i$ para cada muestra de la clase minoritaria basado en cuántos vecinos de la clase mayoritaria la rodean;
- **intuición:** genera más muestras sintéticas donde el clasificador actual tiene más dificultades, es decir, zonas de alta ambigüedad de Bayes.

Ponderación:

$$
\Gamma_i=\frac{r_i}{\sum_j r_j}.
$$

Por lo tanto:

$$
\Longrightarrow
\text{mayor densidad sintética en la frontera.}
$$

![Esquema de generación ADASYN](figures/clase-12/fig-11-adasyn.png)

## Diapositiva 12. Tomek Links: Limpieza de la Frontera

Un par de muestras $(x_i,x_j)$ con $y_i\ne y_j$ es un **Tomek Link** si no existe $x_k$ tal que:

$$
d(x_i,x_k)<d(x_i,x_j)
\quad
\text{o}
\quad
d(x_j,x_k)<d(x_i,x_j).
$$

**Efecto en el clasificador:**

- eliminar el elemento de $\omega_{maj}$ aumenta la separación, o margen, entre las clases;
- reduce el traslape de densidades, facilitando la convergencia de métodos discriminantes.

![Ejemplo de Tomek links en un conjunto sintético](figures/clase-12/fig-12-tomek-scatter.png)

![Flujo de limpieza con Tomek links](figures/clase-12/fig-12-tomek-workflow.png)

## Diapositiva 13. Near Miss: Submuestreo Informado

Cuando:

$$
P(\omega_{maj}) \gg P(\omega_{min}),
$$

se desplaza la frontera de decisión hacia la región de baja densidad de la clase minoritaria. Pero la precisión del clasificador depende de la calidad de la estimación de la densidad en la **frontera de decisión**.

- **Problema:** el submuestreo aleatorio puede eliminar vectores de soporte críticos.
- **Solución Near Miss:** seleccionar ejemplares de la clase mayoritaria basándose en su proximidad, medida típicamente con distancia euclidiana, a la clase minoritaria.

Sea $\mathcal{D}=\{(x_1,y_1),\ldots,(x_n,y_n)\}$ nuestro conjunto de entrenamiento. Definimos:

$$
\mathcal{X}_{min}=\{x_i\in\mathcal{D}:y_i=\omega_{min}\},
$$

$$
\mathcal{X}_{maj}=\{x_j\in\mathcal{D}:y_j=\omega_{maj}\}.
$$

Sea $d(x_i,x_j)$ la métrica de distancia, típicamente $L_2$. Definimos la función de vecindad para $x\in\mathcal{X}_{maj}$ respecto a $\mathcal{X}_{min}$ como el promedio de distancias a los $k$ vecinos más cercanos:

$$
\bar d_k(x,\mathcal{X}_{min})
=
\frac{1}{k}\sum_{i=1}^k d(x,\operatorname{NN}_i(x,\mathcal{X}_{min})).
$$

## Diapositiva 14. Near Miss-1, Near Miss-2 y Near Miss-3

**Near Miss-1 (Proximidad Local)**

Mantiene los ejemplares $x\in\mathcal{X}_{maj}$ tales que $\bar d_k(x,\mathcal{X}_{min})$ sea mínima. **Intuición:** selecciona puntos en la zona de solapamiento.

**Near Miss-2 (Cobertura Global)**

Mantiene los ejemplares $x\in\mathcal{X}_{maj}$ tales que la distancia promedio a los $k$ vecinos más lejanos de $\mathcal{X}_{min}$ sea mínima. **Intuición:** busca puntos que estén en el "centro" de la distribución minoritaria.

**Near Miss-3 (Localidad por Instancia)**

Para cada $x\in\mathcal{X}_{min}$, se seleccionan sus $M$ vecinos más cercanos en $\mathcal{X}_{maj}$. **Intuición:** garantiza que cada ejemplar minoritario esté rodeado por la clase mayoritaria para definir la frontera local.

Desde el análisis de **celdas de Voronoi**:

- el algoritmo NM-1 comprime la representación de la clase mayoritaria contra la frontera;
- esto equivale a una estimación de densidad no paramétrica, $k$-NN, donde forzamos a que $p(x\mid\omega_{maj})$ tenga soporte únicamente cerca de la región de transición.

| Atributo | Ventaja | Desventaja |
| --- | --- | --- |
| NM-1 | Alta precisión en frontera | Sensible a ruido (outliers) |
| NM-2 | Estabilidad global | Puede ignorar fronteras complejas |
| NM-3 | Preservación local | Computacionalmente costoso |

## Diapositiva 15. Near Miss Sampling

- **Control heurístico:** a diferencia del submuestreo aleatorio, Near Miss permite una selección determinista de la información.
- **Riesgo de Bayes:** al alterar artificialmente $P(\omega_i)$, estamos moviendo el umbral de decisión $\theta$. Es crítico recalibrar el modelo si se desea recuperar las probabilidades posteriores reales.
- **Recomendación:** utilizar NM-3 en conjuntos de datos con múltiples *clusters* minoritarios dispersos en el espacio de características $\mathbb{R}^d$.

![Esquema de near miss sampling](figures/clase-12/fig-15-near-miss.png)

## Diapositiva 16. Edited Nearest Neighbor (ENN)

Sea $\mathcal{D}=\{(x_1,y_1),\ldots,(x_n,y_n)\}$ el conjunto de entrenamiento. Para cada muestra $x_i\in\mathcal{D}$:

1. Se identifica el conjunto de sus $k$ vecinos más cercanos en $\mathcal{D}\setminus\{x_i\}$, denotado como $\mathcal{N}_k(x_i)$.
2. Se aplica la regla de votación mayoritaria sobre las etiquetas de $\mathcal{N}_k(x_i)$:

$$
\hat y_i = \operatorname{mode}(\{y_j:x_j\in\mathcal{N}_k(x_i)\}).
$$

3. **Regla de edición:** la muestra $(x_i,y_i)$ se elimina de $\mathcal{D}$ si su etiqueta original no coincide con la predicción de su vecindad:

$$
\text{si } y_i\ne \hat y_i
\Longrightarrow
\mathcal{D}_{edited}
=
\mathcal{D}\setminus\{(x_i,y_i)\}.
$$

Wilson (1972) demostró propiedades asintóticas relevantes para este procedimiento.

**Teorema de suavizado de frontera**

A medida que $n\to\infty$, el conjunto editado $\mathcal{D}_{edited}$ tiende a contener solo muestras que se encuentran en regiones donde su probabilidad posterior $P(\omega_i\mid x)>0.5$, para el caso binario.

**Interpretación en Duda, Hart & Stork:** este proceso actúa como un filtro de paso bajo sobre la superficie de decisión. Al eliminar muestras inconsistentes, la regla 1-NN aplicada sobre el conjunto editado aproxima mejor la regla de decisión óptima de Bayes que si se aplicara sobre el conjunto original ruidoso.

## Diapositiva 17. Edited Nearest Neighbor (ENN)

Geométricamente, ENN altera el diagrama de Voronoi del conjunto de datos:

- **Sin edición:** los *outliers* crean pequeñas "islas" o polígonos aislados de una clase dentro del territorio de otra.
- **Con ENN:** estas islas desaparecen, permitiendo que los polígonos de Voronoi se fusionen en regiones continuas y convexas.

**Relación con otros métodos:**

- **Vs. Near Miss:** NM busca los puntos más difíciles para mantenerlos; ENN busca los puntos más difíciles para eliminarlos por considerarlos poco fiables.
- **PCA:** mientras PCA reduce la dimensionalidad del espacio, ENN reduce la "complejidad" de la distribución de las muestras.

**Cuándo utilizarlo:**

- datos con alto nivel de ruido;
- fronteras de clase muy solapadas;
- como paso previo a otros algoritmos de aprendizaje.

**Cuándo evitarlo:**

- datos perfectamente separados, linealmente o no;
- cuando cada muestra es extremadamente costosa y no se puede permitir perder información legítima.

## Diapositiva 18. ENN como Limpieza Informada

ENN es una técnica de limpieza de datos informada que prioriza la consistencia local sobre la integridad global del conjunto original.

![Esquema de edited nearest neighbor](figures/clase-12/fig-18-enn.png)

## Diapositiva 19. Priors, Umbrales y Decisiones

Incluso con un *score* probabilístico $\hat p(x)\approx P(\omega_1\mid x)$, el umbral $0.5$ no siempre es apropiado. Con costos desiguales:

$$
\text{decidir } \omega_1
\Longleftrightarrow
\hat p(x)>\tau.
$$

Donde $\tau$ depende de:

- *priors*;
- costos de falsos positivos y falsos negativos;
- objetivo operativo.

Formalmente, el desbalance es un sesgo en los *priors* $P(\omega_i)$. Decidimos $\omega_1$ si:

$$
\frac{p(x\mid \omega_1)}{p(x\mid \omega_2)}
>
\frac{P(\omega_2)}{P(\omega_1)}.
$$

- Si $P(\omega_2)\gg P(\omega_1)$, el umbral de verosimilitud se vuelve prohibitivo.
- El clasificador óptimo "desplaza" la frontera para favorecer a la clase mayoritaria.

## Diapositiva 20. Ajuste de Priors en la Práctica

Hay al menos tres estrategias para trabajar con muestras desbalanceadas:

1. usar *priors* empíricos del dataset;
2. imponer *priors* poblacionales conocidos;
3. compensar desbalance con pesos de clase o remuestreo.

**sklearn**

Ajustar `class_weight='balanced'` en logística o SVM es una forma práctica de corregir el sesgo inducido por la frecuencia de clases.

## Diapositiva 21. Aprendizaje Sensible al Costo

En el problema primal, si las clases están desbalanceadas, la frontera de margen suave estándar puede sesgarse hacia la clase minoritaria. Una corrección formal consiste en usar penalizaciones distintas:

$$
\min_{w,b,\xi}
\frac{1}{2}\lVert w\rVert^2
+
C_1\sum_{x_i\in\omega_1}\xi_i
+
C_2\sum_{x_i\in\omega_2}\xi_i
$$

sujeto a:

$$
y_i(w^\top\Phi(x_i)+b)\ge 1-\xi_i,
\qquad
\xi_i\ge 0.
$$

- Si $C_1>C_2$, penalizamos más fallar en la clase minoritaria.
- Esto compensa el sesgo de los *priors* sin alterar la muestra de datos.

## Diapositiva 22. Post-Tuning del Umbral

Si el modelo entrega probabilidades o *scores*, la regla:

$$
\hat y=\mathbb{I}\{s(x)\ge t\}
$$

depende del umbral $t$.

En aprendizaje sensible a costos, $t$ puede elegirse minimizando una función de costo empírico:

$$
\hat t
=
\arg\min_t
\left[
c_{FP}\widehat{\mathrm{FP}}(t)
+
c_{FN}\widehat{\mathrm{FN}}(t)
\right].
$$

Esto conecta directamente teoría de Bayes, evaluación y despliegue operativo.

## Diapositiva 23. ¿Cuándo Usar Qué?

Guía rápida:

- **k-NN:** muy sensible al desbalance local; SMOTE o pesos pueden ayudar.
- **Perceptrón / logística / SVM:** probar primero `class_weight`.
- **Naive Bayes:** ajustar *priors* puede ser muy natural.
- **GMM:** útil si el desbalance responde a mezcla poblacional real.

Hemos unido tres capas:

1. **Geometría:** margen, separación, hiperplanos.
2. **Probabilidad:** *priors*, *posteriors*, regla de Bayes.
3. **Evaluación:** métricas, Kappa, ROC/PR, remuestreo.

Un buen clasificador debe ser razonable en las tres.

| Problema | Herramienta principal |
| --- | --- |
| Accuracy engañosa | Recall, precision, F1, Kappa |
| Clase positiva rara | PR curve, PR-AUC |
| Distinto costo de error | Umbral, pesos de clase, priors |
| Sesgo por frecuencias | Class weights, SMOTE, undersampling |
| Comparación final de modelos | CV + test separado |

## Diapositiva 24. Trivia

**TRIVIA time!**

1. ¿Cómo afecta un desbalance extremo $P(\omega_1)\ll P(\omega_2)$ a la frontera de decisión en un clasificador bayesiano?

   A. La desplaza hacia la región de alta densidad de $\omega_1$.  
   B. La desplaza hacia la región de alta densidad de $\omega_2$.  
   C. No tiene efecto si las densidades condicionales $p(x\mid\omega_i)$ son Gaussianas.

2. Verdadero o falso: el método de *Near Miss-1* es preferible al submuestreo aleatorio porque preserva exclusivamente los ejemplos de la clase mayoritaria que están más alejados de la frontera, reduciendo así el ruido.

3. ¿Cuál es la interpretación de la técnica SMOTE desde la estimación de densidades?

   A. Una reducción de la varianza del estimador por eliminación de *outliers*.  
   B. Una interpolación lineal que busca rellenar el soporte de $p(x\mid\omega_{min})$.  
   C. Un ajuste de las probabilidades a priori sin modificar la evidencia.

4. En un problema de detección de fraudes, clase rara, ¿por qué la métrica de *accuracy* es un estimador sesgado de la utilidad del modelo?

5. El método *Edited Nearest Neighbors* (ENN) se diferencia de las técnicas de balanceo puro porque:

   A. Su objetivo primordial es la limpieza de la frontera y la eliminación de traslape (*overlapping*).  
   B. Siempre aumenta el número de muestras de la clase minoritaria.  
   C. Es un método puramente paramétrico basado en vectores de medias.

## Diapositiva 25. Descomposición Sesgo-Varianza

**Sección:** Descomposición sesgo-varianza.

## Diapositiva 26. Predicción como Aproximación de una Función Desconocida

Esto es repaso con lenguaje actualizado.

Supongamos una variable respuesta escalar $Y$ y un vector de características $X\in\mathbb{R}^d$. El modelo conceptual clásico es:

$$
Y=f(X)+\varepsilon,
$$

donde:

$$
\mathbb{E}[\varepsilon\mid X]=0,
\qquad
\operatorname{Var}(\varepsilon\mid X)=\sigma^2(X).
$$

**Lectura**

$f$ representa la regularidad sistemática y $\varepsilon$ la parte no predecible del fenómeno.

Entrenamos un modelo sobre una muestra $\mathcal{D}=\{(x_i,y_i)\}_{i=1}^n$. El resultado del entrenamiento no es un número fijo, sino una función aleatoria $\hat f_{\mathcal{D}}(x)$, porque depende de la muestra observada.

**Punto clave**

Al cambiar la muestra, cambia la regla aprendida. Esa dependencia es la raíz de la varianza del estimador.

## Diapositiva 27. Error Cuadrático Esperado en un Punto

Para un punto fijo $x$, consideramos:

$$
\operatorname{Err}(x)
=
\mathbb{E}\left[
\left(Y-\hat f_{\mathcal{D}}(x)\right)^2
\mid X=x
\right].
$$

La esperanza es sobre:

- el ruido $\varepsilon$ que afecta a $Y$;
- la aleatoriedad de la muestra $\mathcal{D}$, que determina $\hat f_{\mathcal{D}}$.

Esta es la cantidad cuya estructura vamos a descomponer.

Un modelo muy rígido cambia poco con la muestra:

$$
\hat f_{\mathcal{D}_1}(x)\approx \hat f_{\mathcal{D}_2}(x),
$$

pero puede quedar lejos de $f(x)$. Un modelo muy flexible puede acercarse mucho a los datos observados, pero variar violentamente con $\mathcal{D}$.

**Compromiso**

La generalización requiere balancear error sistemático y sensibilidad a la muestra.

## Diapositiva 28. Definición del Predictor Medio

Para un punto $x$, definimos el predictor medio:

$$
\bar f(x)=\mathbb{E}_{\mathcal{D}}\left[\hat f_{\mathcal{D}}(x)\right].
$$

Entonces podemos comparar:

- la función verdadera $f(x)$;
- la predicción promedio $\bar f(x)$;
- una realización particular $\hat f_{\mathcal{D}}(x)$.

Esa triple comparación separa error sistemático de error por fluctuación muestral.

El sesgo del procedimiento de aprendizaje en $x$ es:

$$
\operatorname{Bias}(x)
=
\mathbb{E}_{\mathcal{D}}\left[\hat f_{\mathcal{D}}(x)\right]-f(x)
=
\bar f(x)-f(x).
$$

Su cuadrado mide qué tan lejos está, en promedio, el procedimiento de la verdad:

$$
\operatorname{Bias}^2(x)
=
\left(\bar f(x)-f(x)\right)^2.
$$

**Interpretación**

Un modelo subparametrizado o demasiado rígido suele tener sesgo alto.

## Diapositiva 29. Varianza en un Punto

La varianza del procedimiento es:

$$
\operatorname{Var}_{\mathcal{D}}\left(\hat f_{\mathcal{D}}(x)\right)
=
\mathbb{E}_{\mathcal{D}}
\left[
\left(\hat f_{\mathcal{D}}(x)-\bar f(x)\right)^2
\right].
$$

Mide cuánto se mueve la predicción cuando cambiamos la muestra.

**Interpretación**

Un modelo muy flexible puede tener varianza alta aunque ajuste muy bien en entrenamiento.

Partimos de:

$$
\operatorname{Err}(x)
=
\mathbb{E}\left[
\left(Y-\hat f_{\mathcal{D}}(x)\right)^2
\mid X=x
\right].
$$

Usamos:

$$
Y=f(x)+\varepsilon
$$

y sumamos y restamos $\bar f(x)$:

$$
Y-\hat f_{\mathcal{D}}(x)
=
\underbrace{f(x)-\bar f(x)}_{A}
+
\underbrace{\bar f(x)-\hat f_{\mathcal{D}}(x)}_{B}
+
\underbrace{\varepsilon}_{C}.
$$

## Diapositiva 30. Expansión del Cuadrado

Entonces:

$$
(A+B+C)^2
=
A^2+B^2+C^2+2AB+2AC+2BC.
$$

Aplicando esperanza condicional:

$$
\operatorname{Err}(x)
=
\mathbb{E}[A^2]
+
\mathbb{E}[B^2]
+
\mathbb{E}[C^2]
+
2\mathbb{E}[AB]
+
2\mathbb{E}[AC]
+
2\mathbb{E}[BC].
$$

Ahora analizamos cada término por separado.

Observemos:

$$
A=f(x)-\bar f(x)
$$

es determinista para $x$ fijo. Además:

$$
\mathbb{E}_{\mathcal{D}}[B]
=
\mathbb{E}_{\mathcal{D}}\left[\bar f(x)-\hat f_{\mathcal{D}}(x)\right]
=0
$$

y:

$$
\mathbb{E}[\varepsilon\mid X=x]=0.
$$

Por lo tanto:

$$
\mathbb{E}[AB]=A\mathbb{E}[B]=0,
\qquad
\mathbb{E}[AC]=A\mathbb{E}[C]=0.
$$

## Diapositiva 31. El Último Término Cruzado

También:

$$
\mathbb{E}[BC]
=
\mathbb{E}\left[
\left(\bar f(x)-\hat f_{\mathcal{D}}(x)\right)\varepsilon
\right].
$$

Bajo la hipótesis usual de independencia entre el ruido del nuevo dato y la muestra de entrenamiento:

$$
\mathbb{E}[BC]
=
\mathbb{E}[B]\mathbb{E}[C]
=0.
$$

**Hipótesis implícita**

La nueva perturbación $\varepsilon$ no depende de las fluctuaciones de la muestra $\mathcal{D}$.

Sobreviven solo tres términos:

$$
\operatorname{Err}(x)
=
A^2+\mathbb{E}[B^2]+\mathbb{E}[C^2].
$$

Es decir:

$$
\operatorname{Err}(x)
=
\underbrace{\left(\bar f(x)-f(x)\right)^2}_{\operatorname{Bias}^2(x)}
+
\underbrace{\operatorname{Var}_{\mathcal{D}}\left(\hat f_{\mathcal{D}}(x)\right)}_{\operatorname{Variance}(x)}
+
\underbrace{\operatorname{Var}(\varepsilon\mid X=x)}_{\operatorname{Noise}(x)}.
$$

## Diapositiva 32. Forma Clásica

La expresión final es:

$$
\operatorname{Err}(x)
=
\operatorname{Bias}^2(x)
+
\operatorname{Var}_{\mathcal{D}}\left(\hat f_{\mathcal{D}}(x)\right)
+
\sigma^2(x).
$$

Si además el ruido es homocedástico:

$$
\sigma^2(x)=\sigma^2,
$$

entonces:

$$
\operatorname{Err}(x)
=
\operatorname{Bias}^2(x)
+
\operatorname{Var}_{\mathcal{D}}\left(\hat f_{\mathcal{D}}(x)\right)
+
\sigma^2.
$$

Esta es la versión estándar de la descomposición sesgo-varianza.

Si ahora promediamos respecto de la distribución de $X$:

$$
\operatorname{Err}
=
\mathbb{E}_X[\operatorname{Err}(X)].
$$

Entonces:

$$
\operatorname{Err}
=
\mathbb{E}_X[\operatorname{Bias}^2(X)]
+
\mathbb{E}_X\left[
\operatorname{Var}_{\mathcal{D}}\left(\hat f_{\mathcal{D}}(X)\right)
\right]
+
\mathbb{E}_X[\sigma^2(X)].
$$

El compromiso sesgo-varianza no es local a un punto; es una propiedad global del procedimiento de aprendizaje.

## Diapositiva 33. Compromiso

La descomposición sesgo-varianza formaliza la tensión en términos estadísticos de:

- aproximar la regla óptima con datos finitos;
- controlar la complejidad del clasificador;
- evitar que la solución se ajuste a peculiaridades de la muestra.

**Bajo sesgo, alta varianza.** Ejemplos típicos:

- 1-NN;
- árboles muy profundos;
- SVM RBF con $\gamma$ demasiado grande;
- polinomios de grado alto.

Error de entrenamiento muy bajo, pero fuerte sensibilidad a perturbaciones de la muestra.

**Alto sesgo, baja varianza.** Ejemplos típicos:

- clasificador lineal para una frontera claramente no lineal;
- k-NN con $k$ demasiado grande;
- regularización excesiva;
- un modelo generativo demasiado restringido.

El modelo es estable, pero sistemáticamente incapaz de capturar la estructura verdadera.

## Diapositiva 34. El Ruido Irreducible

El término:

$$
\sigma^2(x)
=
\operatorname{Var}(\varepsilon\mid X=x)
$$

no puede eliminarse cambiando el algoritmo.

Surge de:

- variables omitidas;
- medición imperfecta;
- aleatoriedad intrínseca del fenómeno;
- etiquetas ruidosas.

Ningún ajuste de hiperparámetros puede empujar el error esperado por debajo del nivel de ruido irreducible.

**Consecuencia**

Conexión con riesgo empírico: minimizar $\hat R_{\mathcal{D}}(h)$ puede reducir el sesgo observable sobre la muestra, pero muchas veces aumenta la varianza.

> menor error de entrenamiento no implica menor error de generalización

Este es el motivo estructural por el cual un modelo "gana" en entrenamiento y falla en producción.

## Diapositiva 35. Trivia

**TRIVIA time! Estas afirmaciones son verdaderas o falsas?**

- Generalizar es solo minimizar error de entrenamiento.
- La matriz de confusión organiza la evaluación y sugerir métricas.
- Kappa corrige el acuerdo por azar.
- El desbalance afecta al entrenamiento pero no a la decisión.
- ROC y PR muestran los mismos compromisos con diferentes variables.
- Remuestreo y pesos de clase son herramientas, no soluciones.

## Diapositiva 36. Optimización de Hiperparámetros

**Sección:** Optimización de hiperparámetros.

## Diapositiva 37. Hiperparámetros como Control del Compromiso

Los hiperparámetros ajustan complejidad y, por lo tanto, sesgo y varianza. Por ejemplo:

- $k$ en k-NN;
- $C$ y $\gamma$ en SVM;
- profundidad en árboles;
- fuerza de regularización en logística.

Elegirlos bien es un problema de optimización estadística, no solo computacional.

Con **validación cruzada k-fold**, partimos la muestra en $K$ bloques:

$$
\mathcal{D}
=
\mathcal{D}_1\cup\cdots\cup\mathcal{D}_K.
$$

Para cada configuración $\lambda$:

$$
\operatorname{CV}_K(\lambda)
=
\frac{1}{K}\sum_{k=1}^K \hat R_k(\lambda),
$$

donde $\hat R_k(\lambda)$ es el error al validar sobre $\mathcal{D}_k$ entrenando sobre $\mathcal{D}\setminus\mathcal{D}_k$. Finalmente elegimos:

$$
\hat\lambda
=
\arg\min_{\lambda\in\Lambda}
\operatorname{CV}_K(\lambda).
$$

## Diapositiva 38. Búsqueda de Hiperparámetros

**Grid Search**

En búsqueda exhaustiva definimos una grilla:

$$
\Lambda=\Lambda_1\times\cdots\times\Lambda_m
$$

y evaluamos todos sus elementos.

**Ventajas:** simple, reproducible, útil cuando hay pocos hiperparámetros relevantes.

**Costo:** crece mucho con la dimensión de $\Lambda$.

**Random Search**

En lugar de recorrer sistemáticamente toda la grilla, muestreamos:

$$
\lambda^{(1)},\ldots,\lambda^{(N)}
\sim
\Pi
$$

desde una distribución sobre el espacio de hiperparámetros. Luego elegimos:

$$
\hat\lambda
=
\arg\min_{1\le j\le N}
\operatorname{CV}_K(\lambda^{(j)}).
$$

**Ventaja:** explora más eficientemente espacios grandes cuando solo algunos hiperparámetros dominan el rendimiento.

## Diapositiva 39. Consideraciones Prácticas

**Importancia de la escala en la búsqueda**

Muchos hiperparámetros viven naturalmente en escala logarítmica:

$$
C\in[10^{-3},10^3],
\qquad
\gamma\in[10^{-4},10^1].
$$

Por eso suele ser mejor muestrear:

$$
\log C,\log\gamma
$$

uniformemente que usar una escala lineal.

Esto vale tanto para Grid Search como para Random Search.

**Selección y evaluación final**

Si usamos validación cruzada para elegir $\hat\lambda$, todavía necesitamos un conjunto final de test o una evaluación externa. Reutilizar los mismos datos para búsqueda y evaluación final induce un sesgo optimista.

**Práctica correcta**

- train/validation/test, o
- validación cruzada anidada.

## Diapositiva 40. Lectura Estadística de la Búsqueda

La búsqueda de hiperparámetros no elimina el compromiso sesgo-varianza. Solo intenta encontrar una región del espacio de modelos donde:

$$
\text{sesgo razonable}
\qquad
\text{y}
\qquad
\text{varianza controlada}
$$

produzcan el mejor error fuera de muestra. Por lo tanto:

> Optimizar hiperparámetros es una aproximación empírica al equilibrio sesgo-varianza.

## Diapositiva 41. Trivia

**TRIVIA time!**

- En la descomposición del error cuadrático esperado $\operatorname{Err}(x)$, ¿qué componente es "irreducible" y no puede eliminarse cambiando el algoritmo?
- Los modelos con alta capacidad y con regularización excesiva son estables, baja varianza, pero incapaces de aprender patrones complejos, alto sesgo. ¿Verdadero o falso?
- ¿Qué valor de $k$ da como resultado un ejemplo de un modelo con bajo sesgo pero alta varianza en k-NN?
- ¿El compromiso entre sesgo y varianza es una propiedad local o global del proceso de aprendizaje?
- Si solo algunos hiperparámetros dominan el rendimiento, ¿qué método de búsqueda es más eficiente: Grid Search o Random Search?
- ¿Qué riesgo se corre al reutilizar los mismos datos para la búsqueda de hiperparámetros y para la evaluación final del modelo?
  - Un sesgo optimista en la estimación del error fuera de muestra.
  - Que el modelo deje de ser aleatorio y se vuelva determinista.
  - Un aumento innecesario del sesgo del modelo.
  - Una subestimación de la varianza del estimador.
- Si no tenemos suficientes datos para un esquema train/validation/test fijo, podemos usar un bucle interno para elegir hiperparámetros y uno externo para evaluar la capacidad de generalización.
- El objetivo final de la búsqueda de hiperparámetros es asegurar que el error de entrenamiento sea igual al error de test.
- Menor error de entrenamiento no implica menor error de generalización: ¿por qué?
