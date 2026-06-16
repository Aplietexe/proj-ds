---
title: "Introducción a la Ciencia de Datos y Machine Learning"
---

# Introducción a la Ciencia de Datos y Machine Learning

## Diapositiva 1

Clase 1 - Fundamentos

FaMAF

Ciencias de datos 2026

## Diapositiva 2

![Gustav Doré, "Over London by rail"](figures/clase-1/fig-002-000.png)

## Diapositiva 3

![Mapa histórico de Londres](figures/clase-1/fig-003-001.png)

## Diapositiva 4. El Paradigma de ML vs. Programación Tradicional

El primer paradigma: ciencia experimental.

Las preguntas y conclusiones están motivadas por experimentos, y muchas veces surgen de prueba y error. Registro empírico de lo que se observa a partir de la observación directa y la experimentación física con elementos de medición básicos. Descripción de fenómenos naturales.

![Ciencia experimental](figures/clase-1/fig-004-002.png)

## Diapositiva 5. El Paradigma de ML vs. Programación Tradicional

El segundo paradigma: ciencia teórica.

Búsqueda de leyes universales. Fuerte uso de modelos matemáticos para explicar e interpretar la realidad. Se plantean ideas que buscan simplicidad, belleza, etc. Por ejemplo, las leyes de la termodinámica, las leyes de la gravedad, etc.

![Ciencia teórica](figures/clase-1/fig-005-004.png)

## Diapositiva 6. El Paradigma de ML vs. Programación Tradicional

El tercer paradigma: ciencia computacional.

Se usa la computadora para analizar sistemas que son demasiado complejos para su tratamiento con lápiz y papel. Se crean simulaciones o laboratorios virtuales para probar teorías mediante algoritmos. Por ejemplo, dinámica molecular, estructura en gran escala del universo, etc.

![Ciencia computacional](figures/clase-1/fig-006-006.png)

## Diapositiva 7. El Paradigma de ML vs. Programación Tradicional

El cuarto paradigma: ciencia basada en datos.

La tecnología ha permitido recabar cantidades masivas de información. El análisis de esa información con algoritmos permite detectar patrones que son demasiado complejos para elaborar una teoría basada en modelos matemáticos. La explicación queda subordinada a las aplicaciones.

![Ciencia basada en datos](figures/clase-1/fig-007-008.png)

## Diapositiva 8. El Paradigma de ML vs. Programación Tradicional

![Modelo, algoritmo, observaciones y predicciones](figures/clase-1/fig-008-010.png)

## Diapositiva 9. Roadmap de la Clase

1. Introducción a la Ciencia de Datos
   El Ecosistema de Datos
   Fundamentos de Machine Learning
   Definiciones Formales
   Tipos de Aprendizaje
2. Supervised vs. unsupervised Learning
   Supervised Learning
   Conceptos Clave
   Generalización y Overfitting
   Algoritmos Supervisados
   Unsupervised Learning
   Clustering
   Reducción de Dimensionalidad
   Conclusiones y Futuro

## Diapositiva 10. Introducción a la Ciencia de Datos

## Diapositiva 11. ¿Qué es Data Science?

La Ciencia de Datos no es una disciplina aislada. Es la intersección de múltiples campos.

- `Computer Science`: desarrollo de software, algoritmos eficientes, manejo de datos.
- `Math & Statistics`: modelado probabilístico, inferencia, álgebra lineal.
- `Domain Knowledge`: el contexto del negocio o la ciencia, por ejemplo finanzas o bioinformática.

Objetivo: extraer *insights* accionables a partir de datos crudos.

## Diapositiva 12. Ramas de la Ciencia de Datos

Distinguimos áreas clave que a menudo se confunden:

- `Artificial Intelligence (AI)`: el concepto más amplio. Agentes que imitan funciones cognitivas humanas, como razonar, ver o escuchar.
- `Machine Learning (ML)`: un subconjunto de AI. Algoritmos que mejoran su desempeño con la experiencia, es decir, con los datos, sin ser explícitamente programados para cada regla.
- `Data Mining`: exploración de grandes *datasets* para encontrar patrones.
- `Deep Learning`: un subconjunto de ML basado en redes neuronales profundas.

## Diapositiva 13. Data Science Lifecycle

Un proyecto de *Data Science* en la industria sigue un *pipeline* iterativo:

1. `Data Collection`: ingesta de datos, por ejemplo con SQL, APIs o *web scraping*.
2. `Data Cleaning & Preprocessing`: manejo de *missing values*, *outliers* y transformación de datos. El 80% del tiempo se gasta aquí.
3. `EDA (Exploratory Data Analysis)`: entender la distribución de los datos y sus correlaciones.
4. `Modeling`: selección de algoritmos, entrenamiento y *tuning* de hiperparámetros.
5. `Evaluation`: métricas de negocio y técnicas.
6. `Deployment`: poner el modelo en producción.

## Diapositiva 14. Big Data

**Large (Volumen)**

- Grandes cantidades de datos.
- Requiere computación distribuida, por ejemplo Hadoop o Spark.
- Ejemplo: LHC (CERN), logs de Facebook.

**Wide (Dimensionalidad)**

- Gran número de *features* o variables.
- *Curse of dimensionality*: a mayor dimensión, los datos se vuelven más dispersos.
- Requiere técnicas de reducción de dimensionalidad, como PCA.

Vamos a aprender a partir de los datos para predecir o clasificar a partir de datos nuevos.

## Diapositiva 15. ¿Qué es el Aprendizaje?

> "Learning is any process by which a system improves performance from experience."
>
> Herbert Simon

No buscamos programar las reglas, por ejemplo "si tiene bigotes y orejas puntiagudas es un gato", sino programar el sistema para que aprenda las reglas a partir de ejemplos.

## Diapositiva 16. Definición Formal (Mitchell, 1997)

Una máquina aprende una tarea $T$, con respecto a una medida de desempeño $P$, basada en una experiencia $E$, si su desempeño en $T$ medido por $P$ mejora con la experiencia $E$.

**Ejemplo: detección de spam**

- $T$: clasificar emails como *spam* o *no spam*.
- $P$: porcentaje de emails correctamente clasificados, es decir, *accuracy*.
- $E$: base de datos de emails etiquetados previamente por usuarios.

## Diapositiva 17. El Paradigma de ML vs. Programación Tradicional

- Tradicional: Datos + Reglas $\rightarrow$ Respuestas.
- *Machine Learning*: Datos + Respuestas (*labels*) $\rightarrow$ Reglas (Modelo).

El "modelo" es la hipótesis matemática que mejor aproxima la función real que genera los datos.

![Programación tradicional vs. machine learning](figures/clase-1/fig-017-011.png)

## Diapositiva 18. Taxonomía del Machine Learning

![Taxonomía del machine learning](figures/clase-1/fig-018-012.png)

## Diapositiva 19. Taxonomía del Machine Learning

- `Supervised Learning` (Supervisado): tenemos *ground truth*. Datos etiquetados $(x, y)$. Objetivo: predecir $y$ dado un nuevo $x$.
- `Unsupervised Learning` (No Supervisado): solo tenemos $x$. No hay etiquetas. Objetivo: encontrar estructura oculta, patrones o agrupamientos.
- `Reinforcement Learning` (Refuerzo): agentes toman acciones en un entorno para maximizar una recompensa acumulada. Por ejemplo, AlphaGo o robótica.
- `Semi-supervised / Self-supervised`: tendencias modernas donde usamos pocos datos etiquetados y muchos no etiquetados, por ejemplo LLMs.

## Diapositiva 20. Supervised vs. unsupervised Learning

## Diapositiva 21. Supervised Learning: El flujo

Dado un *training set* de pares $\{(x^{(i)}, y^{(i)})\}_{i=1}^N$:

1. Asumimos una familia de funciones, es decir, hipótesis $h_\theta(x)$.
2. Definimos una *loss function* $L(\hat y, y)$ que mide el error.
3. Minimizamos el error ajustando los parámetros $\theta$, es decir, realizamos el entrenamiento.

Dos tareas principales:

- `Regression`: el objetivo $y$ es continuo, por ejemplo el precio de una casa.
- `Classification`: el objetivo $y$ es discreto o categórico, por ejemplo decidir si algo es gato o perro.

![Flujo de supervised learning](figures/clase-1/fig-021-013.png)

## Diapositiva 22. Ejemplo Clásico: MNIST

- `Input (x)`: imagen de $28 \times 28$ píxeles, es decir, un vector de 784 dimensiones.
- `Output (y)`: clase del 0 al 9.
- `Modelo`: podría ser una regresión logística, SVM o CNN.

![Reconocimiento de dígitos manuscritos](figures/clase-1/fig-022-014.png)

## Diapositiva 23. Generalización

No nos importa que el modelo memorice los datos de entrenamiento. Nos importa que generalice bien a datos nuevos (*unseen data*).

Separamos los datos en:

- `Training Set`: para ajustar los parámetros.
- `Validation Set`: para ajustar hiperparámetros y seleccionar el modelo.
- `Test Set`: para la evaluación final. Nunca tocar durante el entrenamiento.

## Diapositiva 24. Overfitting vs. Underfitting

- `Underfitting (High Bias)`: el modelo es demasiado simple para capturar la estructura de los datos, por ejemplo usar una línea recta para datos cuadráticos.
- `Overfitting (High Variance)`: el modelo es demasiado complejo, memoriza el ruido del *training set* y falla en el *test set*.

Solución al *overfitting*:

- Más datos.
- Simplificar el modelo, por ejemplo usar menos *features*.
- Regularización ($L_1$, $L_2$).

Pero, ¿cómo lo mido?

## Diapositiva 25. Función de costo

En los algoritmos de aprendizaje automático, el objetivo es encontrar una función para una variable de salida $Y$ dado un conjunto de variables de entrada $X$. Esta función se denomina genéricamente función de costo (*target function*, *cost function*, *loss function*).

Mide la diferencia entre lo que el modelo predice y lo que se espera que devuelva.

El hecho de que la función de costo no sea perfecta produce necesariamente un error en un conjunto de datos nuevos, llamado error de predicción o de validación.

## Diapositiva 26. Función de costo

Por ejemplo, para medir qué tanto un modelo se parece a un conjunto de datos, se define el error cuadrático medio:

$$
\operatorname{MSE} = \frac{1}{n}\sum_{i=1}^n \bigl(y_i - M(x_i; \theta)\bigr)^2
$$

Este error surge naturalmente en el planteo de los cuadrados mínimos a partir del procedimiento bayesiano de *maximum likelihood*.

Según usemos un conjunto de entrenamiento o de validación, tendremos un MSE de entrenamiento y uno de validación, respectivamente.

El MSE es solo un ejemplo de las funciones de error o funciones de costo, o *loss functions*, que podríamos usar.

La función error en los datos de validación tiene varios componentes y es difícil controlarlos simultáneamente.

## Diapositiva 27. Overfitting vs. Underfitting

**Underfitting (Sesgo Alto)**

- El modelo es demasiado simple.
- No captura la estructura.
- Error alto en *train* y *test*.

**Overfitting (Varianza Alta)**

- El modelo es demasiado complejo.
- Memoriza el ruido.
- Error bajo en *train* y alto en *test*.

![Underfitting y overfitting](figures/clase-1/fig-027-015.png)

## Diapositiva 28. El Modelo Generador de Datos

Asumimos que la realidad sigue el proceso:

$$
y = f(x) + \epsilon
$$

- $f(x)$: la función real, es decir, el objetivo ideal.
- $\epsilon$: ruido aleatorio irreducible.

**Propiedades del ruido**

$$
\mathbb{E}[\epsilon] = 0
\qquad
\operatorname{Var}(\epsilon) = \sigma^2
$$

Por lo tanto, la variabilidad de $y$ observada es intrínsecamente $\sigma^2$:

$$
\mathbb{E}[y] = f(x)
\qquad
\operatorname{Var}(y) = \sigma^2
$$

## Diapositiva 29. Descomposición del Error Cuadrático

Queremos minimizar el error esperado en un punto $x$ para un modelo $M(x)$:

$$
\operatorname{Err}(x) = \mathbb{E}\bigl[(y - M(x))^2\bigr]
$$

Tras expandir los términos, usando $y = f(x) + \epsilon$, el error se divide en:

$$
\operatorname{Err}(x) =
\underbrace{\bigl(\mathbb{E}[M(x)] - f(x)\bigr)^2}_{\operatorname{Bias}^2}
+
\underbrace{\mathbb{E}\bigl[(M(x) - \mathbb{E}[M(x)])^2\bigr]}_{\operatorname{Varianza}}
+
\underbrace{\sigma^2}_{\text{Ruido irreducible}}
$$

Nota: el ruido $\sigma^2$ es el límite inferior de error que cualquier modelo puede alcanzar.

## Diapositiva 30. Derivación Formal

Para descomponer el error esperado en un punto $x$, utilizaremos la técnica de sumar y restar el valor esperado del modelo $\mathbb{E}[M]$ dentro del cuadrado.

Sea el error del modelo, sin contar el ruido:

$$
\operatorname{Error}_M = \mathbb{E}\bigl[(f - M)^2\bigr]
$$

Aplicamos el truco algebraico:

$$
f - M = \underbrace{(f - \mathbb{E}[M])}_{A} + \underbrace{(\mathbb{E}[M] - M)}_{B}
$$

Recordando que $(A + B)^2 = A^2 + B^2 + 2AB$, al aplicar la esperanza $\mathbb{E}[\cdot]$ obtenemos:

$$
\mathbb{E}\bigl[(f - M)^2\bigr] = \mathbb{E}[A^2] + \mathbb{E}[B^2] + 2\mathbb{E}[AB]
$$

## Diapositiva 31. Derivación Formal: Análisis de Términos

Analicemos cada componente por separado:

1. Término $A^2$ (Sesgo): como $f$ y $\mathbb{E}[M]$ son deterministas, es decir, no varían con el conjunto de entrenamiento, su diferencia es constante:

$$
\mathbb{E}\bigl[(f - \mathbb{E}[M])^2\bigr] = (f - \mathbb{E}[M])^2 = \operatorname{Bias}^2
$$

2. Término $B^2$ (Varianza): por definición de varianza de una variable aleatoria,

$$
\operatorname{Var}(X) = \mathbb{E}\bigl[(X - \mathbb{E}[X])^2\bigr]
$$

tenemos:

$$
\mathbb{E}\bigl[(\mathbb{E}[M] - M)^2\bigr] = \operatorname{Var}(M)
$$

Queda demostrar que el término cruzado $2\mathbb{E}[AB]$ es igual a cero.

## Diapositiva 32. Derivación Formal: El Término Cruzado

Expandimos $\mathbb{E}[AB]$ aprovechando la linealidad de la esperanza:

$$
\mathbb{E}[AB] = \mathbb{E}\bigl[(f - \mathbb{E}[M])(\mathbb{E}[M] - M)\bigr]
$$

Como $(f - \mathbb{E}[M])$ es constante, podemos sacarlo fuera de la esperanza:

$$
\mathbb{E}[AB] = (f - \mathbb{E}[M])\,\mathbb{E}[\mathbb{E}[M] - M]
$$

Distribuimos la esperanza interna:

$$
\mathbb{E}[AB] = (f - \mathbb{E}[M]) \bigl(\mathbb{E}[\mathbb{E}[M]] - \mathbb{E}[M]\bigr)
$$

Por lo tanto,

$$
\mathbb{E}[AB] = (f - \mathbb{E}[M]) \cdot 0 = 0
$$

Conclusión: el error del modelo es puramente la suma del cuadrado del sesgo y la varianza.

## Diapositiva 33. Resumen de la Descomposición

Si añadimos de nuevo el ruido irreducible $\sigma^2$ que aislamos al inicio:

$$
\mathbb{E}\bigl[(y - M)^2\bigr] = \operatorname{Bias}^2(M) + \operatorname{Var}(M) + \sigma^2
$$

- `Bias`: qué tan lejos está el "promedio" de mis modelos de la realidad. Es error debido a supuestos erróneos en el algoritmo, por ejemplo asumir linealidad cuando no existe.
- `Varianza`: qué tan sensible es mi modelo a cambios en los datos de entrenamiento. Es error debido a la sensibilidad a fluctuaciones en el conjunto de entrenamiento.
- `Ruido`: el límite físico de precisión de nuestro problema, originado en la incertidumbre de la naturaleza. No depende del modelo.

## Diapositiva 34. Bias-Variance Trade-off

Existe un compromiso fundamental:

- Modelos simples $\rightarrow$ alto *bias*, baja varianza.
- Modelos complejos $\rightarrow$ bajo *bias*, alta varianza.

A medida que aumentamos la complejidad del modelo:

- El sesgo disminuye, es decir, mejora el ajuste a los datos.
- La varianza aumenta, es decir, el modelo se vuelve inestable.

El objetivo del aprendizaje automático es encontrar el equilibrio que minimiza:

$$
\mathbb{E}\bigl[(y - M(x))^2\bigr]
$$

Este equilibrio se conoce como el *bias-variance trade-off*.

## Diapositiva 35. El Compromiso Sesgo-Varianza

![Compromiso sesgo-varianza](figures/clase-1/fig-035-016.png)

## Diapositiva 36. Regresión Lineal y Logística

**Linear Regression (Para regresión)**

$$
h_\theta(x) = \theta_0 + \theta_1 x_1 + \cdots + \theta_n x_n
$$

Optimizamos usando *gradient descent* o ecuaciones normales.

**Logistic Regression (Para clasificación)**

$$
h_\theta(x) = \frac{1}{1 + e^{-\theta^T x}}
$$

- Produce una probabilidad entre 0 y 1.
- Usamos un *threshold* o umbral para decidir la clase.

## Diapositiva 37. Árboles de Decisión y Random Forests

**Decision Trees**

- Modelos no lineales, fáciles de interpretar.
- Dividen el espacio de *features* en rectángulos mediante reglas "if-then".
- Propensos a *overfitting*.

**Random Forests (Ensemble)**

- Entrenamos muchos árboles con subconjuntos aleatorios de datos y *features*.
- Promediamos sus resultados. Esto reduce drásticamente la varianza y evita *overfitting*.
- *State of the art* para muchos problemas tabulares.

## Diapositiva 38

![Carretero & Tallada / Euclid Consortiu](figures/clase-1/fig-038-017.png)

## Diapositiva 39. Aprendizaje No Supervisado: Pattern Discovery

Aquí los datos no tienen etiquetas $y$. Buscamos estructura intrínseca.

Aplicaciones:

- Segmentación de clientes.
- Genómica, por ejemplo agrupar genes con expresión similar.
- Detección de anomalías, por ejemplo fraude bancario.

## Diapositiva 40. Clustering: K-Means

El algoritmo de *clustering* más popular.

Pasos:

1. Inicializar $K$ centroides aleatoriamente.
2. Asignar cada punto al centroide más cercano.
3. Mover los centroides al promedio de los puntos asignados.
4. Repetir hasta convergencia.

Nota: debemos elegir $K$ a priori, por ejemplo usando el "Elbow Method".

## Diapositiva 41. Dimensionality Reduction

¿Qué hacemos si tenemos 10,000 *features*? Visualizar y procesar es imposible.

**PCA (Principal Component Analysis)**

- Proyecta los datos a un espacio de menor dimensión preservando la mayor cantidad de varianza posible.
- Es una transformación lineal.
- Útil para compresión y visualización en 2D o 3D.

**t-SNE / UMAP**

- Técnicas no lineales para visualización.
- Preservan la estructura local, es decir, los vecindarios.

## Diapositiva 42. Sistemas de Recomendación

Un caso híbrido o no supervisado.

- `Content-based`: recomendar ítems similares a los que le gustaron al usuario, basado en *features* del ítem.
- `Collaborative Filtering`: recomendar ítems que le gustaron a usuarios "parecidos" a mí, por ejemplo mediante factorización matricial.
- Ejemplos: Netflix, Amazon, Spotify.

## Diapositiva 43. Deep Learning: La revolución actual

Cuando tenemos *Big Data*, por ejemplo imágenes, texto o audio, las redes neuronales profundas superan a los algoritmos clásicos.

- `CNNs (Convolutional Neural Networks)`: visión por computadora.
- `Transformers`, por ejemplo GPT o BERT: procesamiento de lenguaje natural.

Requieren GPUs masivas para entrenamiento.

## Diapositiva 44. Ética y Sesgo en Data Science

> "With great power comes great responsibility".

- `Bias` en los datos: si entrenamos con datos históricos sesgados, por ejemplo contrataciones discriminatorias, el modelo aprenderá a discriminar.
- `Fairness`: auditar modelos, por ejemplo para asegurar equidad en grupos demográficos.
- `Explainability (XAI)`: en medicina o finanzas, no podemos usar "cajas negras". Necesitamos saber por qué el modelo tomó una decisión.

## Diapositiva 45. Resumen

- Data Science combina computación, estadística y conocimiento de dominio.
- Machine Learning se divide principalmente en supervisado, para predicción, y no supervisado, para patrones.
- El *overfitting* es el enemigo principal: usar validación cruzada y regularización.
- La evaluación correcta, es decir, las métricas, es crítica para el éxito del negocio.
- El futuro es ético, interpretable y masivo: *Big Data* más *Deep Learning*.
