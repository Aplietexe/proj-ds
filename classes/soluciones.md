
# Resoluciones de `guias.md`

## Nota previa

Estas resoluciones están escritas **a partir del material provisto**.  
Cuando un ejercicio depende de un dataset externo o de una actividad fuera del entorno adjunto (por ejemplo Kaggle, DataCamp o Gemini Canvas), dejo una **solución reproducible**: derivación, código Python e interpretación esperada.  
No invento resultados numéricos de archivos que no fueron adjuntados.

---

# Guía 1. Nivelación con Pandas y Seaborn

## Ejercicio 1

La “respuesta” de este ejercicio no es un desarrollo matemático sino la realización efectiva del curso de Pandas de Kaggle y la obtención del certificado correspondiente.

**Respuesta escrita:** completar el curso, conservar el certificado y verificar que se dominan al menos estas operaciones:

- carga de datos con `pd.read_csv`;
- indexado con `loc`, `iloc`;
- filtrado;
- agrupamientos con `groupby`;
- ordenamientos con `sort_values`;
- tratamiento de valores faltantes;
- combinación y agregación de tablas.

## Ejercicio 2

Análogamente, la resolución consiste en completar el curso de Data Visualization de Kaggle.

**Respuesta escrita:** completar el curso y verificar que se dominan al menos:

- gráficos de líneas;
- histogramas;
- boxplots;
- scatterplots;
- barplots;
- configuración básica de Seaborn y Matplotlib.

## Ejercicio 3

Como el dataset es externo, la resolución se dejó en un script reproducible que ejecuta exactamente cada inciso sobre el CSV descargado desde Kaggle.

Código ejecutable: `scripts/guide1_ex3_airplane.py`.

### 3.1. Carga del dataset

_Código movido a los archivos `.py` referenciados en esta sección._

_Código movido a los archivos `.py` referenciados en esta sección._

### 3.2. Información general e inspección

_Código movido a los archivos `.py` referenciados en esta sección._

_Código movido a los archivos `.py` referenciados en esta sección._

Esto responde al inciso 3: `info()` da tipos de variables, cantidad de no nulos y uso de memoria; `describe()` resume estadísticos descriptivos para columnas numéricas y, con `include="all"`, también para categóricas.

### 3.3. Muertes por día

_Código movido a los archivos `.py` referenciados en esta sección._

### 3.4. Dos accidentes con mayor número de muertes

_Código movido a los archivos `.py` referenciados en esta sección._

### 3.5. Sobrevivientes y proporción de supervivencia

Suponiendo que la columna `Aboard` representa el total de personas embarcadas:

_Código movido a los archivos `.py` referenciados en esta sección._

La fórmula usada es

$$
\text{Survivors} = \text{Aboard} - \text{Fatalities},
\qquad
\text{SurvivalRate} = \frac{\text{Survivors}}{\text{Aboard}}.
$$

### 3.6. Fatalities por mes y porcentajes

_Código movido a los archivos `.py` referenciados en esta sección._

Los meses con menor porcentaje de fatalities se obtienen con:

_Código movido a los archivos `.py` referenciados en esta sección._

### 3.7. Barplot de porcentajes de sobrevivientes

_Código movido a los archivos `.py` referenciados en esta sección._

### Conclusión del ejercicio 3

La resolución correcta del ejercicio consiste en:

1. leer el CSV descargado desde Kaggle con `encoding="latin-1"` y `Date` como índice;
2. usar `groupby`, `sort_values`, columnas derivadas y gráficos de Seaborn;
3. guardar tablas y figuras para verificar los resultados.

Los resultados concretos quedan generados por el script y guardados en `outputs/guide1_ex3/`.

## Ejercicio 4

El enunciado pide un *applet* interactivo y luego una interpretación conceptual. A continuación dejo una implementación completa en **Streamlit** y luego las respuestas pedidas.

Código ejecutable: `apps/guide1_ex4_linear_regression_app.py`.

### 4.1. Implementación en Streamlit

Archivo: `apps/guide1_ex4_linear_regression_app.py`.

_Código movido a los archivos `.py` referenciados en esta sección._

### 4.2. Respuestas conceptuales

#### (a) Al fijar $\sigma$ y aumentar $N$, ¿cómo evoluciona la brecha entre $\mathrm{MSE}_{\mathrm{train}}$ y $\mathrm{MSE}_{\mathrm{test}}$?

La brecha **tiende a reducirse**. La razón es que, cuando el modelo verdadero es lineal y el modelo ajustado también es lineal, el estimador de mínimos cuadrados tiene bajo sesgo y una varianza que decrece al aumentar el tamaño muestral. Por lo tanto, al crecer $N$:

- la recta estimada se estabiliza;
- el error de entrenamiento y el de test se acercan;
- ambos se aproximan al nivel de ruido irreducible.

En términos cualitativos:

$$
N \uparrow \quad \Longrightarrow \quad
\operatorname{Var}(\hat m),\operatorname{Var}(\hat b) \downarrow
\quad \Longrightarrow \quad
\mathrm{MSE}_{\text{train}} \approx \mathrm{MSE}_{\text{test}}.
$$

#### (b) Con un $N$ pequeño, ¿qué sucede con la estabilidad de la pendiente calculada al variar la semilla del ruido?

Con pocos datos, la pendiente estimada es **mucho más inestable**. Distintas realizaciones del ruido producen rectas bastante diferentes porque la varianza del estimador es alta.

En forma simplificada,

$$
\operatorname{Var}(\hat m) \propto \frac{\sigma^2}{\sum_i (x_i-\bar x)^2}.
$$

Si $N$ es chico, la suma del denominador suele ser menor y el efecto del ruido se amplifica.

#### (c) ¿Es posible observar *overfitting* usando un modelo lineal sobre datos puramente lineales?

En el sentido **estructural** fuerte, no debería aparecer un *overfitting* severo, porque la familia de hipótesis coincide con el mecanismo generador:

$$
y = mx + b + \epsilon,
\qquad
\hat y = \hat m x + \hat b.
$$

Es decir, el modelo tiene la complejidad correcta. Sin embargo, con pocos datos y ruido grande puede verse una **brecha finita entre train y test** debida a la varianza del estimador. Eso no significa que el modelo sea “demasiado complejo” para la realidad, sino que la estimación todavía es inestable.

En lenguaje de sesgo-varianza:

- el sesgo es bajo, porque la familia lineal contiene a la función verdadera;
- la varianza puede ser alta si $N$ es pequeño;
- al crecer $N$, esa varianza baja y la brecha desaparece.

---

# Guía 2. Teoría Bayesiana

## Ejercicio 1

Sea

$$
p = P(\omega_1\mid x), \qquad q = P(\omega_2\mid x),
$$

de modo que

$$
p \ge 0,\quad q \ge 0,\quad p+q=1.
$$

La probabilidad de error condicional es

$$
P(\mathrm{error}\mid x)=\min(p,q).
$$

### 1.1. Cota superior

Queremos probar que

$$
\min(p,q)\le 2pq.
$$

Si $p \le q$, entonces $\min(p,q)=p$ y como $p\le 1/2$ se tiene

$$
p \le 2p(1-p)=2pq.
$$

Si $q \le p$, el razonamiento es simétrico y se obtiene

$$
q \le 2q(1-q)=2pq.
$$

Luego, para todo $x$,

$$
P(\mathrm{error}\mid x)\le 2P(\omega_1\mid x)P(\omega_2\mid x).
$$

Integrando contra $p(x)$ se obtiene la cota superior

$$
P(\mathrm{error}) \le \int 2P(\omega_1\mid x)P(\omega_2\mid x)\,p(x)\,dx.
$$

### 1.2. Por qué $\alpha<2$ no garantiza cota superior

Si sustituyéramos

$$
P(\mathrm{error}\mid x)=\alpha pq,\qquad \alpha<2,
$$

basta tomar un caso con

$$
p=q=\frac12.
$$

Entonces el error exacto es

$$
\min(p,q)=\frac12,
$$

mientras que la aproximación vale

$$
\alpha pq=\frac{\alpha}{4}<\frac12.
$$

Por lo tanto, esa sustitución queda **por debajo** del error verdadero y ya no puede garantizar una cota superior.

### 1.3. Cota inferior con $pq$

Queremos probar que

$$
pq\le \min(p,q).
$$

Si $p\le q$, entonces

$$
pq \le p = \min(p,q),
$$

porque $q\le 1$. El caso $q\le p$ es simétrico. Por lo tanto,

$$
P(\mathrm{error}\mid x)\ge P(\omega_1\mid x)P(\omega_2\mid x),
$$

y al integrar:

$$
P(\mathrm{error})\ge \int P(\omega_1\mid x)P(\omega_2\mid x)\,p(x)\,dx.
$$

### 1.4. Por qué $\beta>1$ puede fallar como cota inferior

Si usamos

$$
P(\mathrm{error}\mid x)=\beta pq,\qquad \beta>1,
$$

podemos elegir un caso con $p=\varepsilon$ y $q=1-\varepsilon$, donde

$$
0<\varepsilon < 1-\frac{1}{\beta}.
$$

Entonces

$$
\min(p,q)=\varepsilon,
$$

pero

$$
\beta pq=\beta \varepsilon(1-\varepsilon) > \varepsilon = \min(p,q),
$$

porque $\beta(1-\varepsilon)>1$. Así, la aproximación puede quedar **por encima** del error exacto y dejar de ser cota inferior.

## Ejercicio 2

La forma normalizada de la densidad de Laplace centrada en $a_i$ y con escala $b_i$ es

Código ejecutable para la gráfica del inciso 3: `scripts/guide2_ex2_laplace_ratio.py`.

$$
p(x\mid \omega_i)=\frac{1}{2b_i}\exp\left(-\frac{|x-a_i|}{b_i}\right),
\qquad b_i>0.
$$

### 2.1. Expresiones analíticas normalizadas

La normalización se verifica porque

$$
\int_{-\infty}^{\infty} \frac{1}{2b_i}\exp\left(-\frac{|x-a_i|}{b_i}\right)\,dx = 1.
$$

Por lo tanto,

$$
p(x\mid \omega_1)=\frac{1}{2b_1}\exp\left(-\frac{|x-a_1|}{b_1}\right),
\qquad
p(x\mid \omega_2)=\frac{1}{2b_2}\exp\left(-\frac{|x-a_2|}{b_2}\right).
$$

### 2.2. Radio de verosimilitud

El likelihood ratio es

$$
\Lambda(x)=\frac{p(x\mid \omega_1)}{p(x\mid \omega_2)}
=
\frac{b_2}{b_1}
\exp\left(
-\frac{|x-a_1|}{b_1}+\frac{|x-a_2|}{b_2}
\right).
$$

### 2.3. Caso $a_1=0$, $b_1=1$, $a_2=1$, $b_2=2$

Sustituyendo,

$$
\Lambda(x)=2\exp\left(-|x|+\frac{|x-1|}{2}\right).
$$

En forma por tramos:

$$
\Lambda(x)=
\begin{cases}
2e^{\frac12+\frac{x}{2}}, & x<0,\\[4pt]
2e^{\frac12-\frac{3x}{2}}, & 0\le x<1,\\[4pt]
2e^{-\frac12-\frac{x}{2}}, & x\ge 1.
\end{cases}
$$

Código para graficar:

_Código movido a los archivos `.py` referenciados en esta sección._

## Ejercicio 3

La regla propuesta decide $\omega_1$ si $x>\theta$ y $\omega_2$ si $x\le \theta$.

### 3.1. Expresión de la probabilidad de error

Hay dos formas de errar:

- el estado verdadero es $\omega_1$ pero se decide $\omega_2$, lo que ocurre cuando $x\le \theta$;
- el estado verdadero es $\omega_2$ pero se decide $\omega_1$, lo que ocurre cuando $x>\theta$.

Por lo tanto,

$$
P(\mathrm{error})=
P(\omega_1)\int_{-\infty}^{\theta}p(x\mid \omega_1)\,dx
+
P(\omega_2)\int_{\theta}^{\infty}p(x\mid \omega_2)\,dx.
$$

### 3.2. Condición necesaria de optimalidad

Derivando respecto de $\theta$:

$$
\frac{d}{d\theta}P(\mathrm{error})
=
P(\omega_1)p(\theta\mid \omega_1)
-
P(\omega_2)p(\theta\mid \omega_2).
$$

En un mínimo interior debe cumplirse

$$
\frac{d}{d\theta}P(\mathrm{error})=0,
$$

luego la condición necesaria es

$$
p(\theta\mid \omega_1)P(\omega_1)=p(\theta\mid \omega_2)P(\omega_2).
$$

### 3.3. ¿La ecuación define un único valor de $\theta$?

No necesariamente. La igualdad

$$
p(\theta\mid \omega_1)P(\omega_1)=p(\theta\mid \omega_2)P(\omega_2)
$$

puede tener:

- una única solución;
- varias soluciones;
- ninguna solución interior.

Depende de cuántas veces se crucen las densidades ponderadas por sus *priors*. En consecuencia, una regla de umbral simple no siempre reproduce toda la frontera de Bayes si las densidades se cruzan más de una vez.

### 3.4. Caso normal

Si

$$
p(x\mid \omega_i)=
\frac{1}{\sqrt{2\pi}\sigma_i}
\exp\left(-\frac{(x-\mu_i)^2}{2\sigma_i^2}\right),
$$

la condición de frontera es

$$
\frac{1}{\sigma_1}\exp\left(-\frac{(\theta-\mu_1)^2}{2\sigma_1^2}\right)P(\omega_1)
=
\frac{1}{\sigma_2}\exp\left(-\frac{(\theta-\mu_2)^2}{2\sigma_2^2}\right)P(\omega_2).
$$

Tomando logaritmos,

$$
\frac{(\theta-\mu_2)^2}{2\sigma_2^2}
-
\frac{(\theta-\mu_1)^2}{2\sigma_1^2}
=
\ln\left(\frac{\sigma_1 P(\omega_2)}{\sigma_2 P(\omega_1)}\right).
$$

#### Caso $\sigma_1=\sigma_2=\sigma$

Los términos cuadráticos se cancelan y queda una única solución lineal:

$$
\theta^\star
=
\frac{\mu_1+\mu_2}{2}
+
\frac{\sigma^2}{\mu_1-\mu_2}
\ln\left(\frac{P(\omega_2)}{P(\omega_1)}\right).
$$

Si además

$$
P(\omega_1)=P(\omega_2),
$$

entonces

$$
\theta^\star=\frac{\mu_1+\mu_2}{2}.
$$

#### Caso $\sigma_1\neq \sigma_2$

Ahora sí aparecen términos cuadráticos y la ecuación puede tener hasta dos raíces. La frontera de decisión ya no tiene por qué ser un único umbral.

## Ejercicio 4

Si la acción elegida es aleatoria, con probabilidades $P(\alpha_i\mid x)$, el riesgo total es la esperanza del riesgo condicional respecto de esa aleatoriedad y luego respecto de $x$.

### 4.1. Fórmula del riesgo

Para un $x$ fijo, el riesgo medio es

$$
\sum_{i=1}^a R(\alpha_i\mid x)P(\alpha_i\mid x).
$$

Integrando en $x$,

$$
R=
\int
\left(
\sum_{i=1}^{a}R(\alpha_i\mid x)P(\alpha_i\mid x)
\right)
p(x)\,dx.
$$

### 4.2. Por qué no conviene aleatorizar

Para cada $x$, la cantidad

$$
\sum_{i=1}^a R(\alpha_i\mid x)P(\alpha_i\mid x)
$$

es una combinación convexa de los riesgos condicionales $R(\alpha_i\mid x)$, porque

$$
P(\alpha_i\mid x)\ge 0,
\qquad
\sum_i P(\alpha_i\mid x)=1.
$$

Una combinación convexa nunca puede ser menor que el mínimo de sus términos. Por lo tanto, el mínimo se alcanza asignando probabilidad 1 a la acción que tiene menor riesgo condicional:

$$
P(\alpha_{i^\star}\mid x)=1,
\qquad
i^\star = \arg\min_i R(\alpha_i\mid x).
$$

Conclusión: **no se obtiene beneficio** introduciendo azar en la regla de decisión.

## Ejercicio 5

La pérdida es

$$
\lambda(\alpha_i\mid \omega_j)=
\begin{cases}
0, & i=j,\\
\lambda_r, & i=c+1,\\
\lambda_s, & \text{en otro caso.}
\end{cases}
$$

### 5.1. Riesgo de decidir una clase

Si decidimos $\alpha_i$ con $i\le c$, el riesgo condicional es

$$
R(\alpha_i\mid x)
=
\sum_{j\neq i}\lambda_s P(\omega_j\mid x)
=
\lambda_s\left(1-P(\omega_i\mid x)\right).
$$

### 5.2. Riesgo de rechazar

Si rechazamos,

$$
R(\alpha_{c+1}\mid x)=\lambda_r.
$$

### 5.3. Regla óptima

Conviene elegir la clase $\omega_i$ si simultáneamente:

1. es la clase más probable a posteriori,

$$
P(\omega_i\mid x)\ge P(\omega_j\mid x)\quad \forall j;
$$

2. clasificar cuesta menos que rechazar,

$$
\lambda_s\left(1-P(\omega_i\mid x)\right)\le \lambda_r.
$$

La segunda desigualdad equivale a

$$
P(\omega_i\mid x)\ge 1-\frac{\lambda_r}{\lambda_s}.
$$

Por lo tanto, la regla óptima es:

- decidir $\alpha_i$ si $P(\omega_i\mid x)$ es máxima y además
  $P(\omega_i\mid x)\ge 1-\lambda_r/\lambda_s$;
- en caso contrario, rechazar.

### 5.4. Casos límite

#### Si $\lambda_r=0$

Entonces el umbral es

$$
1-\frac{\lambda_r}{\lambda_s}=1.
$$

Solo clasificaríamos si alguna clase tuviera probabilidad posterior 1. En un problema continuo con solapamiento, eso casi nunca ocurre. Luego **conviene rechazar casi siempre**.

#### Si $\lambda_r>\lambda_s$

Entonces

$$
1-\frac{\lambda_r}{\lambda_s}<0.
$$

La condición siempre se cumple porque las probabilidades posteriores son no negativas. Luego **nunca conviene rechazar**: es más barato clasificar, aunque sea errando, que rechazar.

## Ejercicio 6

Código ejecutable para la gráfica del inciso 2: `scripts/guide2_ex6_rejection_region.py`.

## 6.1. Funciones discriminantes óptimas

Del ejercicio anterior, para $i\le c$ se decide la clase con mayor posterior siempre que

$$
P(\omega_i\mid x)\ge 1-\frac{\lambda_r}{\lambda_s}.
$$

Usando Bayes,

$$
P(\omega_i\mid x)=\frac{p(x\mid \omega_i)P(\omega_i)}{p(x)},
\qquad
p(x)=\sum_{j=1}^c p(x\mid \omega_j)P(\omega_j).
$$

La condición umbral equivale a

$$
p(x\mid \omega_i)P(\omega_i)
\ge
\frac{\lambda_s-\lambda_r}{\lambda_s}
\sum_{j=1}^{c}p(x\mid \omega_j)P(\omega_j).
$$

Esto justifica las discriminantes

$$
g_i(x)=
\begin{cases}
p(x\mid \omega_i)P(\omega_i), & i=1,\dots,c,\\[4pt]
\dfrac{\lambda_s-\lambda_r}{\lambda_s}
\sum_{j=1}^{c}p(x\mid \omega_j)P(\omega_j), & i=c+1.
\end{cases}
$$

La regla “elegir el mayor $g_i(x)$” reproduce exactamente la decisión de mínimo riesgo.

## 6.2. Caso
$$
p(x\mid \omega_1)\sim \mathcal N(1,1),\quad
p(x\mid \omega_2)\sim \mathcal N(-1,1),\quad
P(\omega_1)=P(\omega_2),\quad
\frac{\lambda_r}{\lambda_s}=\frac14
$$

Como

$$
1-\frac{\lambda_r}{\lambda_s}=1-\frac14=\frac34,
$$

debemos clasificar solo cuando la posterior máxima sea al menos $3/4$.

Con gaussianas de igual varianza y *priors* iguales,

$$
\log\frac{p(x\mid \omega_1)}{p(x\mid \omega_2)} = 2x,
$$

y por lo tanto

$$
P(\omega_1\mid x)=\frac{1}{1+e^{-2x}},
\qquad
P(\omega_2\mid x)=\frac{1}{1+e^{2x}}.
$$

La frontera entre clase 1 y rechazo se obtiene de

$$
P(\omega_1\mid x)=\frac34
\quad\Longrightarrow\quad
\frac{1}{1+e^{-2x}}=\frac34
\quad\Longrightarrow\quad
x=\frac12\ln 3 \approx 0.5493.
$$

Simétricamente, la frontera entre clase 2 y rechazo es

$$
x=-\frac12\ln 3 \approx -0.5493.
$$

### Regiones de decisión

$$
\mathcal R_2 = (-\infty,-0.5493),
\qquad
\mathcal R_R = [-0.5493,0.5493],
\qquad
\mathcal R_1 = (0.5493,\infty).
$$

Código para graficar:

_Código movido a los archivos `.py` referenciados en esta sección._

## 6.3. Qué pasa cuando $\lambda_r/\lambda_s$ aumenta de $0$ a $1$

El umbral es

$$
1-\frac{\lambda_r}{\lambda_s}.
$$

Si el cociente aumenta:

- cuando $\lambda_r/\lambda_s \to 0$, el umbral tiende a 1 y la región de rechazo crece mucho;
- cuando $\lambda_r/\lambda_s \to 1$, el umbral tiende a 0 y la región de rechazo desaparece.

En otras palabras:

- **rechazar barato** $\Rightarrow$ se rechaza mucho;
- **rechazar caro** $\Rightarrow$ se clasifica casi siempre.

## 6.4. Caso
$$
p(x\mid \omega_1)\sim \mathcal N(1,1),\quad
p(x\mid \omega_2)\sim \mathcal N\left(0,\frac14\right),\quad
P(\omega_1)=\frac13,\quad
P(\omega_2)=\frac23,\quad
\frac{\lambda_r}{\lambda_s}=\frac12
$$

Aquí el umbral es

$$
1-\frac{\lambda_r}{\lambda_s}=\frac12.
$$

En un problema de dos clases, la posterior máxima siempre es al menos $1/2$. Por lo tanto, la región de rechazo queda reducida al conjunto de empate exacto, que tiene medida nula. En la práctica, **no hay región de rechazo apreciable**.

La frontera se obtiene de

$$
\frac13\,\phi(x;1,1)=\frac23\,\phi\left(x;0,\frac14\right).
$$

Esto lleva a la ecuación cuadrática

$$
3x^2+2x-1-\ln 16 = 0,
$$

cuyas raíces son aproximadamente

$$
x_1 \approx -1.5032,
\qquad
x_2 \approx 0.8366.
$$

Como la clase $\omega_2$ es más concentrada y además tiene mayor *prior*, domina la zona central, mientras que la gaussiana más ancha $\omega_1$ domina las colas. Entonces:

$$
\mathcal R_1 = (-\infty,-1.5032)\cup(0.8366,\infty),
\qquad
\mathcal R_2 = [-1.5032,0.8366].
$$

No hay región de rechazo relevante.

## Ejercicio 7

Código ejecutable: `scripts/guide2_ex7_lda_simulation.py`.

Este ejercicio mezcla simulación y teoría de LDA. Como la simulación sí puede escribirse sin datos externos, dejo una solución completa.

Partimos de

$$
C=
\begin{pmatrix}
0 & -0.23\\
0.83 & 0.23
\end{pmatrix},
\qquad
\Sigma=C^TC=
\begin{pmatrix}
0.6889 & 0.1909\\
0.1909 & 0.1058
\end{pmatrix}.
$$

Las medias son

$$
\mu_1=(0,0),\qquad \mu_2=(1,1).
$$

## 7.1. Simulación

_Código movido a los archivos `.py` referenciados en esta sección._

## 7.2. Clasificador usando solo $X_1$

Como ambas clases comparten la misma covarianza y los *priors* son iguales, el LDA unidimensional sobre $X_1$ tiene la forma

$$
g_i(x_1)= -\frac{(x_1-\mu_{i1})^2}{2\sigma_{11}^2}+\ln P(\omega_i),
$$

con

$$
\sigma_{11}^2 = 0.6889.
$$

Dado que $P(\omega_1)=P(\omega_2)$ y las varianzas marginales son iguales, la frontera cae en el punto medio entre las medias marginales:

$$
x_1^\star = \frac{0+1}{2}=0.5.
$$

Por lo tanto:

- decidir $\omega_1$ si $x_1<0.5$;
- decidir $\omega_2$ si $x_1>0.5$.

Implementación manual:

_Código movido a los archivos `.py` referenciados en esta sección._

Implementación con `scikit-learn`:

_Código movido a los archivos `.py` referenciados en esta sección._

## 7.3. Error empírico para $n=100,200,\dots,10000$

El enunciado menciona “error de entrenamiento empírico” pero al mismo tiempo pide *split* train/test. La forma más razonable es reportar **ambos**: error en entrenamiento y error en test.

_Código movido a los archivos `.py` referenciados en esta sección._

_Código movido a los archivos `.py` referenciados en esta sección._

## 7.4. Cota de Bhattacharyya

Para dos gaussianas con covarianzas $\Sigma_1,\Sigma_2$ y *priors* $P_1,P_2$, la cota de Bhattacharyya es

$$
P_e \le \sqrt{P_1P_2}\,e^{-k_B},
$$

donde

$$
k_B =
\frac18(\mu_2-\mu_1)^T \Sigma^{-1} (\mu_2-\mu_1)
+
\frac12\ln\left(
\frac{|\Sigma|}{\sqrt{|\Sigma_1||\Sigma_2|}}
\right),
\qquad
\Sigma=\frac{\Sigma_1+\Sigma_2}{2}.
$$

En este ejercicio,

$$
\Sigma_1=\Sigma_2,
$$

así que el término logarítmico desaparece.

### Solo $X_1$

La distancia cuadrática es

$$
r_1^2=\frac{(1-0)^2}{0.6889}\approx 1.4516.
$$

Luego,

$$
k_B=\frac{r_1^2}{8}\approx 0.18145,
$$

y con *priors* iguales:

$$
P_e \le \frac12 e^{-0.18145} \approx 0.4170.
$$

El error exacto de Bayes en 1D, por compartir varianza, es

$$
P_e = 1-\Phi\left(\frac{1}{2\sqrt{0.6889}}\right)\approx 0.2735.
$$

### Usando $X_1$ y $X_2$

Ahora

$$
r^2=(\mu_2-\mu_1)^T\Sigma^{-1}(\mu_2-\mu_1)\approx 11.3301,
$$

por lo que

$$
k_B=\frac{r^2}{8}\approx 1.4163,
$$

y la cota queda

$$
P_e \le \frac12 e^{-1.4163}\approx 0.1213.
$$

El error exacto de Bayes en 2D vale

$$
P_e = 1-\Phi\left(\frac{r}{2}\right)\approx 0.0462.
$$

## 7.5. Repetición usando las dos características

_Código movido a los archivos `.py` referenciados en esta sección._

## 7.6. Análisis de resultados

En este problema, la segunda característica agrega información útil. Por eso, en el régimen ideal y con suficientes datos,

$$
P_e^{(2D)} < P_e^{(1D)}.
$$

De hecho, los errores teóricos son aproximadamente:

- 1D: $0.2735$;
- 2D: $0.0462$.

Sin embargo, para un **conjunto finito** de datos, el error empírico del clasificador aprendido **sí puede aumentar** al aumentar la dimensión. La razón es que no estamos comparando errores de Bayes ideales sino errores de un estimador entrenado con datos finitos. En alta dimensión aumenta la varianza de estimación y puede aparecer peor generalización.

En resumen:

- el **error de Bayes** no empeora al agregar *features* informativas;
- el **error empírico** de un clasificador entrenado con datos finitos sí puede empeorar por varianza de estimación.

## Ejercicio 8

Para una distribución de Poisson,

Código ejecutable para la simulación del inciso 4: `scripts/guide2_ex8_poisson_bayes.py`.

$$
P(x\mid \lambda)=e^{-\lambda}\frac{\lambda^x}{x!},
\qquad x=0,1,2,\dots
$$

y con *priors* iguales se decide la clase con mayor verosimilitud.

### 8.1. Regla de Bayes

Debemos decidir $\omega_1$ si

$$
e^{-\lambda_1}\frac{\lambda_1^x}{x!}
>
e^{-\lambda_2}\frac{\lambda_2^x}{x!}.
$$

Cancelando $x!$ y tomando logaritmos:

$$
-\lambda_1 + x\ln\lambda_1
>
-\lambda_2 + x\ln\lambda_2.
$$

Luego,

$$
x\bigl(\ln\lambda_1-\ln\lambda_2\bigr)
>
\lambda_1-\lambda_2.
$$

Como $\lambda_1>\lambda_2$, se obtiene el umbral

$$
x>\tau,
\qquad
\tau=\frac{\lambda_1-\lambda_2}{\ln(\lambda_1/\lambda_2)}.
$$

Entonces la regla es:

- decidir $\omega_1$ si $x>\tau$;
- decidir $\omega_2$ si $x<\tau$;
- en empate, cualquiera de las dos.

Como $x$ es entero, si definimos

$$
k=\lfloor \tau \rfloor,
$$

la regla queda

$$
\omega_1 \text{ si } x\ge k+1,
\qquad
\omega_2 \text{ si } x\le k.
$$

### 8.2. Tasa de error de Bayes

Con la regla anterior, el error es

$$
P_e
=
\frac12
\left[
P_{\lambda_1}(X\le k)
+
P_{\lambda_2}(X\ge k+1)
\right].
$$

Equivalentemente,

$$
P_e
=
\frac12
\left[
F_{\text{Pois}(\lambda_1)}(k)
+
1-F_{\text{Pois}(\lambda_2)}(k)
\right].
$$

### 8.3. Función discriminante

La discriminante para la clase $i$ puede escribirse como

$$
g_i(x)=\ln P(\omega_i)+\ln P(x\mid \lambda_i).
$$

Con *priors* iguales,

$$
g_i(x)= -\lambda_i + x\ln \lambda_i - \ln(x!) + \text{cte}.
$$

Como el término $-\ln(x!)$ es común, basta usar

$$
g_i(x)=x\ln\lambda_i-\lambda_i.
$$

Para clasificar un nuevo dato entero $x$:

1. se calcula $g_1(x)$ y $g_2(x)$;
2. se asigna la clase con mayor valor.

### 8.4. Caso $\lambda_1=1.8$, $\lambda_2=0.4$

El umbral es

$$
\tau=\frac{1.8-0.4}{\ln(1.8/0.4)}\approx 0.9308.
$$

Como $x$ es entero:

$$
x\ge 1 \Rightarrow \omega_1,
\qquad
x=0 \Rightarrow \omega_2.
$$

La tasa de error de Bayes es

$$
P_e
=
\frac12
\left[
P_{\lambda_1}(X=0)
+
P_{\lambda_2}(X\ge 1)
\right]
=
\frac12
\left[
e^{-1.8}
+
(1-e^{-0.4})
\right]
\approx 0.2475.
$$

Código de simulación y comparación:

_Código movido a los archivos `.py` referenciados en esta sección._

Interpretación esperada: el error empírico fluctúa alrededor de $0.2475$ y se aproxima a ese valor al repetir la simulación muchas veces o al aumentar el tamaño muestral.

---

# Guía 3. Clasificación Binaria

## Ejercicio 1

Sea la matriz de confusión binaria

| Clase real / Predicción | + | - |
| --- | ---: | ---: |
| + | TP | FN |
| - | FP | TN |

Las métricas fundamentales son:

### Accuracy

$$
\operatorname{Accuracy}=\frac{TP+TN}{TP+TN+FP+FN}.
$$

Mide proporción total de aciertos.

### Recall o Sensitivity

$$
\operatorname{Recall}=\frac{TP}{TP+FN}.
$$

Mide qué fracción de los positivos reales fue detectada.

### Precision

$$
\operatorname{Precision}=\frac{TP}{TP+FP}.
$$

Mide qué fracción de los predichos positivos era realmente positiva.

### Specificity

La definición estándar es

$$
\operatorname{Specificity}=\frac{TN}{TN+FP}.
$$

**Observación:** en el enunciado aparece $TN/(TN+FN)$, pero eso es una errata; la definición correcta usa $FP$ en el denominador.

### F1-score

Es la media armónica entre precisión y recall:

$$
F_1
=
2\frac{\operatorname{Precision}\cdot \operatorname{Recall}}
{\operatorname{Precision}+\operatorname{Recall}}
=
\frac{2TP}{2TP+FP+FN}.
$$

### Comentario conceptual

En datasets desbalanceados, una accuracy alta puede ser engañosa. Por eso conviene mirar también:

- `recall`, si importa no perder positivos;
- `precision`, si importa que los positivos predichos sean confiables;
- `F1`, si se busca un compromiso entre ambas.

## Ejercicio 2

Este ejercicio usa el dataset externo *Loan Data* de Kaggle (`itssuru/loan-data`), descargado localmente, y se resuelve con un flujo completamente reproducible.

Código ejecutable: `scripts/guide3_ex2_4_loan_classification.py`.

## 2.1. Carga e inspección

_Código movido a los archivos `.py` referenciados en esta sección._

## 2.2. Identificación del problema de predicción

El problema es de **clasificación supervisada binaria**: predecir la columna objetivo del préstamo (por ejemplo aprobación, incumplimiento o estado del crédito, según cómo esté nombrada en el CSV). Como el dataset exacto no fue adjuntado, conviene parametrizar el nombre de la variable objetivo.

_Código movido a los archivos `.py` referenciados en esta sección._

## 2.3. Desbalance de clases y atributo no numérico

_Código movido a los archivos `.py` referenciados en esta sección._

_Código movido a los archivos `.py` referenciados en esta sección._

Si el enunciado es consistente con el CSV, entonces debería aparecer exactamente un atributo predictor no numérico. Sus valores posibles se inspeccionan así:

_Código movido a los archivos `.py` referenciados en esta sección._

## 2.4. One-hot encoding con `get_dummies`

_Código movido a los archivos `.py` referenciados en esta sección._

Si la variable objetivo también es textual, puede codificarse con:

_Código movido a los archivos `.py` referenciados en esta sección._

## 2.5. Split de entrenamiento y test

_Código movido a los archivos `.py` referenciados en esta sección._

Esto completa los incisos pedidos. Los resultados numéricos concretos quedan guardados en `outputs/guide3_ex2_4/`.

## Ejercicio 3

Se pide construir un clasificador bayesiano con parámetros estimados a partir de los datos de entrenamiento.

Código ejecutable: `scripts/guide3_ex2_4_loan_classification.py`.

## 3.1. Estimación de medias y covarianzas por clase

Para cada clase $\omega_j$:

$$
\hat\mu_j = \frac{1}{n_j}\sum_{x\in D_j}x,
\qquad
\hat\Sigma_j = \frac{1}{n_j}\sum_{x\in D_j}(x-\hat\mu_j)(x-\hat\mu_j)^T,
\qquad
\hat P(\omega_j)=\frac{n_j}{n}.
$$

Implementación:

_Código movido a los archivos `.py` referenciados en esta sección._

## 3.2. Discriminante gaussiana y predicción

Para cada clase:

$$
g_j(x)=
-\frac12(x-\mu_j)^T\Sigma_j^{-1}(x-\mu_j)
-\frac12\ln|\Sigma_j|
+\ln P(\omega_j).
$$

Se omite la constante común $-\frac d2\ln(2\pi)$.

_Código movido a los archivos `.py` referenciados en esta sección._

## 3.3. Evaluación

_Código movido a los archivos `.py` referenciados en esta sección._

## 3.4. Ignorar correlaciones

Ignorar correlaciones significa reemplazar cada covarianza por su diagonal:

$$
\Sigma_j \longrightarrow \operatorname{diag}(\Sigma_j).
$$

En código, esto ya está contemplado con `diagonal=True`.

_Código movido a los archivos `.py` referenciados en esta sección._

## 3.5. Análisis esperado

- El clasificador con covarianza completa aprovecha correlaciones entre variables.
- El clasificador diagonal reduce drásticamente la cantidad de parámetros.
- Si el tamaño muestral es pequeño o la dimensión es alta, el modelo diagonal puede generalizar mejor porque tiene menor varianza de estimación.
- Si las correlaciones son realmente informativas y hay suficientes datos, la covarianza completa puede rendir mejor.

## Ejercicio 4

Naïve Bayes asume independencia condicional de los atributos dada la clase:

Código ejecutable: `scripts/guide3_ex2_4_loan_classification.py`.

$$
p(x\mid \omega_j)=\prod_{k=1}^d p(x_k\mid \omega_j).
$$

En el caso gaussiano continuo, la discriminante queda

$$
g_j(x)=
\ln P(\omega_j)
-\frac12\sum_{k=1}^d \ln(2\pi\sigma_{jk}^2)
-\frac12\sum_{k=1}^d \frac{(x_k-\mu_{jk})^2}{\sigma_{jk}^2}.
$$

## 4.1. Implementación con `scikit-learn`

_Código movido a los archivos `.py` referenciados en esta sección._

## 4.2. Comparación de los tres clasificadores

Podemos resumir así:

1. **Bayes gaussiano con covarianza completa**
   - mejor si las correlaciones importan y hay suficientes datos;
   - más costoso y más sensible a estimaciones inestables.

2. **Bayes gaussiano diagonal**
   - más simple y robusto;
   - ignora correlaciones;
   - puede mejorar cuando $n$ es pequeño respecto de la dimensión.

3. **Naïve Bayes**
   - entrenamiento muy rápido;
   - muy pocos parámetros;
   - suele ser competitivo aun cuando la independencia condicional es solo aproximada.

## 4.3. Conclusión conceptual

No existe un clasificador universalmente mejor. La conveniencia depende de la relación entre:

- tamaño muestral;
- dimensión;
- fuerza de las correlaciones;
- desbalance de clases;
- métrica de evaluación que importe más.

En datasets tabulares pequeños o moderados, una regla práctica razonable es:

- empezar por Naïve Bayes o por el modelo diagonal;
- pasar a covarianza completa solo si hay evidencia de que las correlaciones agregan valor y la estimación es estable.

---

# Cierre

Las partes matemáticas de la guía quedan resueltas en forma cerrada.  
Las partes computacionales quedaron extraídas a archivos `.py`, ejecutadas sobre los datasets descargados y verificadas con salidas reproducibles en `outputs/`.
