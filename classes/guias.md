---
title: "Guías de Ejercicios de Ciencias de Datos 2026"
---

## Información General

### Docentes

| Nombre | Contacto |
| --- | --- |
| Dr. Marcelo Lares | `marcelo.lares@unc.edu.ar` |
| Dr. Luis Biedma | `lbiedma@unc.edu.ar` |
| Lic. Laura Montes | `laura.montes@unc.edu.ar` |

### Horarios

- Clases teóricas: martes y jueves de 14 hs a 16 hs.
- Clases prácticas: martes y jueves de 16 hs a 18 hs.
- Horarios de consulta: a coordinar con los docentes.

### Condiciones de regularidad

- Cumplir con un mínimo de 70 % de asistencia a las clases prácticas.
- Aprobar dos exámenes parciales.
- Habrá un examen de recuperación.
- Si no se cumple con los requisitos de regularidad, será posible rendir la materia en condición de libre, para lo cual el examen tendrá ejercicios adicionales a los del examen para regulares.
- No se pedirán las guías resueltas.

### Condiciones de promoción

La materia se podrá promocionar si se cumplen los siguientes requisitos:

- Tener aprobadas al día de la última clase todas las materias correlativas según el plan de estudio.
- Cumplir con todos los requisitos de regularidad.
- Cumplir con un mínimo de 80 % de asistencia a las clases prácticas.
- Aprobar las dos evaluaciones parciales con una nota no menor a 6 (seis), y obtener un promedio no menor a 7 (siete).

Al promocionar la materia, no será necesario rendir un examen final, y la nota final será la que resulte de promediar las notas de los exámenes parciales.

Referencia: Ordenanza HCD No 4/11.

## Fechas Importantes

| Examen | Fecha | Temas |
| --- | --- | --- |
| Parcial 1 | TBD | 1, 2 y 3 |
| Parcial 2 | TBD | 4 y 5 |
| Recuperatorio | TBD | Todos |

## Clave

En estas guías hay tres niveles de ejercicios:

1. **Nivel 1.** Es altamente recomendable terminar estos ejercicios durante las clases prácticas.
2. **Nivel 2.** Estos ejercicios son práctica adicional para los parciales. El nivel de complejidad es similar al del primer grupo.
3. **Nivel 3.** Ejercicios de dificultad un poco más elevada. No se debe perder mucho tiempo con ellos, pero son una buena práctica para los exámenes finales, o si se terminan los otros con tiempo antes de los parciales. Sin embargo, estos ejercicios no se explicarán si otros alumnos no han terminado todos los anteriores.

## Guía 1. Nivelación con Pandas y Seaborn

### Práctica

Kaggle es una plataforma online de acceso gratuito, lanzada en 2010, para dar soporte a la comunidad de *data scientists*, permitiendo explorar y publicar tanto bases de datos como modelos y desarrollar competencias para resolver desafíos de Ciencia de Datos. Desde 2017 es una subsidiaria de Google LLC. Para poder acceder a los recursos de la plataforma es necesario registrarse previamente como usuario, en caso de no tener cuenta. Entre los recursos, Kaggle proporciona cursos cortos, gratuitos y autocorregidos para adquirir destrezas básicas en el uso de herramientas usuales en la industria.

Por otro lado, Google proporciona Colaboratory, o Colab, un producto que permite escribir y ejecutar código en Python desde un navegador de internet, usando recursos de los propios servidores de Google, aunque en la versión gratuita están limitados.

A los fines de nivelar conocimientos, las primeras dos tareas consisten en hacer dos cursos y conseguir los correspondientes certificados, y luego resolver un desafío creando una *notebook* en Colab.

### Ejercicio 1 (Nivel 1)

Completar el curso sobre Pandas de Kaggle.

### Ejercicio 2 (Nivel 1)

Completar el curso sobre Data Visualization de Kaggle.

### Ejercicio 3 (Nivel 1)

Para aplicar lo aprendido se proponen las siguientes actividades:

1. Descargar el dataset *Airplane Crashes and Fatalities upto 2023* disponible en Kaggle. Estudiar el diccionario de variables. Luego almacenar el archivo CSV en el drive personal de la cuenta institucional de la UNC.
2. Crear una instancia en Colab y averiguar cómo acceder al sistema de archivos de drive para cargar el CSV usando Pandas, con la variable `Date` como índice de fecha. Usando lo aprendido con Pandas se obtiene un error porque el *encoding* del archivo no está en UTF-8, que es lo supuesto por *default*. Recordar: en la vida los datos nunca están en el formato deseado. Para cambiar el *encoding* en la lectura usar `encoding='latin-1'`.
3. Observar la información del dataset que proporcionan las funciones `info()` y `describe()`.
4. Mostrar un `lineplot` usando Seaborn con el número total de personas embarcadas muertas (`Fatalities`) en cada uno de los días. Para esto, agrupar previamente por fecha y sumar los datos de esa columna.
5. Reordenar el dataset usando la columna `Fatalities` en forma descendente para mostrar los dos accidentes con mayor número de muertes entre las personas embarcadas.
6. Calcular el número de personas embarcadas sobrevivientes en esos dos vuelos y la correspondiente proporción sobre el número total de personas embarcadas.
7. Crear un `DataFrame` con una variable que sume el número de `Fatalities` en cada uno de los meses del año, de enero a diciembre, usando el índice de la base, y otra columna con los correspondientes porcentajes sobre el total de `Fatalities`. Indicar cuáles son los meses con menores porcentajes.
8. Mostrar un `barplot` usando Seaborn con los porcentajes de sobrevivientes en cada uno de los meses del año.

Para completar esta tarea, el Colab debe contener al menos una celda para cada ítem con el código de Pandas y el resultado de ejecutarlo.

### Fijar Conceptos

### Ejercicio 4 (Nivel 2)

Desarrollar un *applet* interactivo utilizando Gemini Canvas, implementado en Streamlit o Dash, para explorar la relación entre la complejidad de los datos, el ruido estadístico y la capacidad de generalización de un modelo de regresión lineal. La herramienta deberá cumplir con los siguientes requisitos técnicos:

1. **Generación de datos.** Definir una función lineal base $y = mx + b$ dentro de un intervalo $[x_{\min}, x_{\max}]$. El usuario debe poder seleccionar un número natural $N$ tal que $10 \le N \le 10000$.
2. **Modelado del ruido.** Incorporar un ruido aditivo en el eje de las ordenadas siguiendo una distribución normal:

$$
\epsilon \sim \mathcal{N}(0,\sigma^2)
$$

La desviación estándar $\sigma$ debe ser ajustable interactivamente mediante un control deslizante.

3. **Partición de datos.** Implementar un mecanismo para dividir el conjunto de $N$ puntos en dos subconjuntos independientes: entrenamiento $D_{\mathrm{train}}$ y prueba $D_{\mathrm{test}}$.
4. **Visualización y métricas.** Mostrar un `scatter plot` que distinga visualmente ambos conjuntos y las rectas de ajuste resultantes. Calcular y desplegar el error cuadrático medio para cada conjunto:

$$
\mathrm{MSE} = \frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2
$$

Tras interactuar con el *applet*, responder de forma fundamentada:

1. Al fijar $\sigma$ y aumentar $N$, ¿cómo evoluciona la brecha entre $\mathrm{MSE}_{\mathrm{train}}$ y $\mathrm{MSE}_{\mathrm{test}}$?
2. Con un $N$ pequeño, ¿qué sucede con la estabilidad de la pendiente calculada al variar la semilla del ruido?
3. ¿Es posible observar un fenómeno de *overfitting* utilizando un modelo lineal sobre datos cuya naturaleza es puramente lineal? Justificar la respuesta basándose en la relación sesgo-varianza.

## Guía 2. Teoría Bayesiana

### Ejercicio 1 (Nivel 1)

En el caso de dos categorías, según la regla de decisión de Bayes, el error condicional viene dado por

$$
P(\mathrm{error}\mid x) = \min\bigl[P(\omega_1\mid x), P(\omega_2\mid x)\bigr],
$$

donde $\omega_i$ denota los posibles estados del sistema y $x$ es una variable aleatoria cuyo valor depende del estado del sistema. Incluso si las densidades *a posteriori* $P(\omega_i\mid x)$ son continuas, el error condicional casi siempre conduce a un integrando discontinuo en el cálculo del error total:

$$
P(\mathrm{error}) = \int P(\mathrm{error}\mid x)\,p(x)\,dx.
$$

Resolver:

1. Demostrar que, para densidades arbitrarias, una cota superior para el error total resulta del hecho de que siempre se cumple

$$
P(\mathrm{error}\mid x) \le 2\,P(\omega_1\mid x)\,P(\omega_2\mid x).
$$

2. Demostrar que si en la expresión para $P(\mathrm{error})$ se sustituye

$$
P(\mathrm{error}\mid x) = \alpha\,P(\omega_1\mid x)\,P(\omega_2\mid x)
$$

con $\alpha < 2$, entonces no puede garantizarse que la integral sea una cota superior para el error.
3. Análogamente, demostrar que puede utilizarse

$$
P(\mathrm{error}\mid x) = P(\omega_1\mid x)\,P(\omega_2\mid x)
$$

para obtener una cota inferior para el error total.
4. Demostrar que si

$$
P(\mathrm{error}\mid x) = \beta\,P(\omega_1\mid x)\,P(\omega_2\mid x)
$$

con $\beta > 1$, entonces la integral puede no ser una cota inferior para el error.

### Ejercicio 2 (Nivel 1)

Suponer dos variables aleatorias independientes idénticamente distribuidas con densidad de Laplace

$$
p(x\mid \omega_i) \propto \exp\left(-\frac{|x-a_i|}{b_i}\right), \qquad i = 1,2,\quad b_i > 0.
$$

Resolver:

1. Escribir las expresiones analíticas normalizadas de $p(x\mid \omega_i)$.
2. Calcular el radio de verosimilitud como función de los parámetros.
3. Graficar el radio $\frac{p(x\mid \omega_1)}{p(x\mid \omega_2)}$ para el caso $a_1 = 0$, $b_1 = 1$, $a_2 = 1$ y $b_2 = 2$.

### Ejercicio 3 (Nivel 1)

Considerar la siguiente regla de decisión para el problema unidimensional con dos categorías: se decide por $\omega_1$ si $x > \theta$ y en otro caso se decide por $\omega_2$.

1. Demostrar que la probabilidad de error para esta regla viene dada por

$$
P(\mathrm{error}) = \int P(\mathrm{error}\mid x)\,p(x)\,dx = P(\omega_1)\int_{-\infty}^{\theta} p(x\mid \omega_1)\,dx + P(\omega_2)\int_{\theta}^{\infty} p(x\mid \omega_2)\,dx.
$$

2. Demostrar que una condición necesaria para minimizar el error es

$$
p(\theta\mid \omega_1)\,P(\omega_1) = p(\theta\mid \omega_2)\,P(\omega_2).
$$

3. ¿Define esta ecuación un valor único de $\theta$?
4. Estudiar como ejemplo el caso en el que la variable $X$ condicional a $\omega_i$ tiene distribución normal con media $\mu_i$ y desvío $\sigma_i$; es decir,

$$
P(X\mid \omega_i) \sim \mathcal{N}(\mu_i,\sigma_i).
$$

### Ejercicio 4 (Nivel 1)

Suponer que se sustituye la función de decisión determinista $\alpha(x)$ por la regla aleatoria dada por la probabilidad $P(\alpha_i\mid x)$ de tomar la decisión $\alpha_i$ dado que se observó $x$.

1. Mostrar que el riesgo resultante viene dado por

$$
R = \int \left(\sum_{i=1}^{a} R(\alpha_i\mid x)\,P(\alpha_i\mid x)\right)p(x)\,dx.
$$

2. Demostrar además que $R$ se minimiza para $P(\alpha_i\mid x) = 1$ para la acción $\alpha_i$ asociada con el riesgo condicional mínimo $R(\alpha_i\mid x)$, lo que demuestra que no se obtiene ningún beneficio haciendo aleatoria la regla de decisión.

### Ejercicio 5 (Nivel 1)

En muchos problemas de clasificación multicategoría, con $\omega_i$ para $i = 1, \ldots, c$, es conveniente trabajar con una función de pérdida pesada. Por ejemplo, puede ocurrir que se rechace un patrón o estado del sistema si este resulta irreconocible:

$$
\lambda(\alpha_i\mid \omega_j) =
\begin{cases}
0 & \text{si } i=j,\ i,j=1,2,\ldots,c,\\
\lambda_r & \text{si } i=c+1,\\
\lambda_s & \text{en otro caso.}
\end{cases}
$$

donde $\lambda_r$ es la pérdida sufrida por la elección de rechazo y $\lambda_s$ es la pérdida incurrida por cometer un error.

Mostrar que el riesgo mínimo se obtiene si se decide $\alpha_i$ cuando $P(\omega_i\mid x) \ge P(\omega_j\mid x)$ para todo $j$ y además

$$
P(\omega_i\mid x) \ge 1 - \frac{\lambda_r}{\lambda_s},
$$

y, en caso contrario, se rechaza. Analizar qué sucede si $\lambda_r = 0$ y qué sucede si $\lambda_r > \lambda_s$.

### Ejercicio 6 (Nivel 1)

Retomar el problema de clasificación con opción de rechazo del ejercicio anterior.

1. Demostrar que las siguientes funciones discriminantes son óptimas para este tipo de problemas:

$$
g_i(x) =
\begin{cases}
p(x\mid \omega_i)\,P(\omega_i) & \text{si } i=1,2,\ldots,c,\\
\dfrac{\lambda_s-\lambda_r}{\lambda_s}\sum_{j=1}^{c} p(x\mid \omega_j)\,P(\omega_j) & \text{si } i=c+1.
\end{cases}
$$

2. Graficar la función discriminante y las regiones de decisión para el caso del problema unidimensional, $x \in \mathbb{R}$, con dos clases y los valores

$$
p(x\mid \omega_1) \sim \mathcal{N}(1,1), \qquad p(x\mid \omega_2) \sim \mathcal{N}(-1,1), \qquad P(\omega_1)=P(\omega_2), \qquad \frac{\lambda_r}{\lambda_s} = \frac{1}{4}.
$$

3. Describir cualitativamente lo que sucede cuando $\frac{\lambda_r}{\lambda_s}$ se incrementa desde $0$ hasta $1$.
4. Considerar nuevamente este problema, ahora en el caso particular

$$
p(x\mid \omega_1) \sim \mathcal{N}(1,1), \qquad p(x\mid \omega_2) \sim \mathcal{N}\left(0,\frac{1}{4}\right), \qquad P(\omega_1)=\frac{1}{3}, \qquad P(\omega_2)=\frac{2}{3}, \qquad \frac{\lambda_r}{\lambda_s} = \frac{1}{2}.
$$

### Ejercicio 7 (Nivel 1)

Estudiar la implementación del análisis discriminante lineal provista por `scikit-learn` para generar muestras aleatorias de acuerdo con una distribución normal bivariada y calcular la función discriminante para una distribución normal dada y probabilidades *a priori* $P(\omega_i)$.

1. Simular dos variables normales $(X_1, X_2)$ con

$$
\Sigma = C^T C, \qquad
C =
\begin{pmatrix}
0 & -0.23 \\
0.83 & 0.23
\end{pmatrix},
$$

y vectores de medias $\mu_1 = (0,0)$ y $\mu_2 = (1,1)$, respectivamente.
2. Suponer que las probabilidades *a priori* de las dos categorías son iguales, $P(\omega_1)=P(\omega_2)$, e implementar un clasificador para dos categorías utilizando sólo el valor de la característica $X_1$ especificada en el inciso anterior. El código resultante debe poder clasificar una nueva muestra basándose en esta información.
3. Determinar el error de entrenamiento empírico en la clasificación de muestras, esto es, el porcentaje de puntos mal clasificados, dividiendo aleatoriamente el número de muestras $n = 100$ en 80 % de entrenamiento y 20 % de test. Repetir incrementando los valores de $n$, desde $100$ hasta $10000$ en pasos de $100$, y graficar el error empírico obtenido.
4. Utilizar la cota de Bhattacharyya para acotar el error que obtendrán los nuevos patrones obtenidos muestreando las distribuciones.
5. Repetir todo lo anterior, pero usando ahora las dos características, $X_1$ y $X_2$.
6. Analizar resultados. ¿Es siempre posible, para un conjunto finito de datos, que el error empírico resulte mayor al aumentar la dimensión de los datos?

### Ejercicio 8 (Nivel 1)

La distribución de Poisson para una variable entera no negativa $x = 0, 1, \ldots$ y parámetro real $\lambda$ viene dada por

$$
P(x\mid \lambda) = e^{-\lambda}\frac{\lambda^x}{x!}.
$$

Considerar el problema de clasificación con dos categorías igualmente probables, $P(\omega_1)=P(\omega_2)$, y condicionales con distribuciones de Poisson con diferentes parámetros $\lambda_1 > \lambda_2$.

Resolver:

1. Especificar la regla de clasificación de Bayes.
2. Determinar la tasa de error de Bayes.
3. Escribir la función discriminante y determinar qué valores debe tener de entrada para clasificar un nuevo dato.
4. Simular una muestra aleatoria de tamaño $100$ con distribuciones de Poisson con $\lambda_1 = 1.8$ y $\lambda_2 = 0.4$, considerando igual probabilidad *a priori*. Usar la función de pérdida cero-uno y clasificar la muestra acorde a esta función. Estimar el error cometido en la muestra y compararlo con el error de Bayes calculado.

## Guía 3. Clasificación Binaria

### Ejercicio 1 (Nivel 1)

#### Matriz de Confusión

En los problemas de predicción con dos clases cobran relevancia los siguientes conceptos:

- $TP$: positivos verdaderos.
- $FP$: falsos positivos.
- $TN$: negativos verdaderos.
- $FN$: falsos negativos.

Una de las clases se considera el *target* para la clasificación y sus valores se denominan positivos, en contraposición al resto, que se consideran negativos. Cuando un ejemplo es clasificado correctamente, a esa clasificación se la toma como verdadera; en caso contrario, como falsa. De esta forma, un ejemplo positivo mal clasificado se llama falso negativo, mientras que un ejemplo negativo mal clasificado se denomina falso positivo.

La manera usual de presentar el número de ejemplos en cada una de estas categorías es mediante la matriz de confusión:

| Clase real / Clasificación | + | - |
| --- | --- | --- |
| + | `# TP` | `# FN` |
| - | `# FP` | `# TN` |

Estudiar la información disponible en la entrada de Wikipedia sobre la matriz de confusión, prestando especial atención a las métricas derivadas de la misma para clasificación binaria, en particular:

- Accuracy:

$$
\frac{\#TP + \#TN}{\#TP + \#TN + \#FP + \#FN} = \hat{p}
$$

- Recall:

$$
\frac{\#TP}{\#TP + \#FN} \qquad (= \text{Sensitivity})
$$

- Precision:

$$
\frac{\#TP}{\#TP + \#FP}
$$

- Specificity:

$$
\frac{\#TN}{\#TN + \#FN} \qquad (= \text{Selectivity})
$$

- F1 score:

$$
\frac{2\,\#TP}{2\,\#TP + \#FP + \#FN}
$$

Notar que estas métricas son sólo útiles para la clasificación binaria, mientras que la matriz de confusión puede construirse para cualquier problema multiclase.

### Ejercicio 2 (Nivel 1)

#### Loan dataset

1. Examinar el dataset *Loan Data* disponible en Kaggle. Indagar el diccionario de las columnas del dataset y en qué consiste el problema de predicción que puede implementarse con este dataset.
2. Estudiar la forma de disponer los datos directamente en memoria usando el disco virtual de la instancia de JupyterLab (Colab) que corre la `.ipynb` en la que se trabaja.
3. Explorar los datos, calcular el desbalance de clases y analizar los valores del único atributo no numérico.
4. Implementar la función `pandas.get_dummies` de Pandas para convertir el atributo de texto en un conjunto de variables binarias.
5. Separar los datos en un conjunto de entrenamiento, reservando el 33 % para *testing*.

### Ejercicio 3 (Nivel 1)

#### Clasificador Bayesiano

1. Calcular la media y la matriz de covarianza correspondiente a los datos de entrenamiento de cada una de las clases, para fijar los parámetros del clasificador bayesiano construido en el práctico anterior.
2. Predecir la clase de cada ejemplo del conjunto de test y evaluar la clasificación usando las funciones `accuracy_score`, `recall_score`, `precision_score` y `confusion_matrix` de la librería `sklearn.metrics`, y analizar los resultados.
3. Ignorar las correlaciones presentes entre las variables, reteniendo sólo los elementos diagonales, es decir, las varianzas, en las matrices de covarianza calculadas en el ítem 1.
4. Repetir la predicción sobre el conjunto de test usando el clasificador bayesiano sin correlaciones. Evaluar el resultado repitiendo el ítem 2.

### Ejercicio 4 (Nivel 1)

#### Naïve Bayes

1. Estudiar el tutorial de DataCamp para aprender a implementar un clasificador Naïve Bayes usando `scikit-learn`.
2. Usar este clasificador para predecir la clase del *Loan dataset* y evaluar con las mismas métricas usadas en el ejercicio anterior.
3. Comparar las tres evaluaciones obtenidas y discutir la conveniencia de cada clasificador.
