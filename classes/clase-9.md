---
title: "Evaluación Empírica: Riesgo, Remuestreo y Bootstrap"
---

## Diapositiva 1

**Portada**

- Ciencia de Datos - Clase 8
- FaMAF
- Abril 2026

## Diapositiva 2. Hoja de Ruta

La clase se organiza en dos bloques:

1. **Parcial 1**
   - Ejercicio 1
   - Ejercicio 2
2. **La Ilusión del Entrenamiento**
   - Riesgo empírico vs. riesgo esperado
   - Estimación del riesgo: técnicas de remuestreo
   - Bootstrap

## Diapositiva 3. Parcial 1

**Sección:** Parcial 1.

## Diapositiva 4. Ejercicio 1

**Decision Bayesiana y Análisis de Riesgo Mínimo**

Considere un problema de clasificación binaria con clases $\omega_1$ y $\omega_2$, donde las distribuciones condicionales de una variable real $x$ están dadas por:

$$
p(x \mid \omega_1)=\frac{1}{\pi\left[1+(x-1)^2\right]},
\qquad
p(x \mid \omega_2)=\frac{1}{\pi\left[1+(x+1)^2\right]}.
$$

Las probabilidades a priori son:

$$
P(\omega_1)=\frac{2}{3},
\qquad
P(\omega_2)=\frac{1}{3}.
$$

Se utiliza pérdida 0-1.

Se pide:

1. Derivar la frontera de decisión bayesiana $x^\ast$ y las regiones $R_1$ y $R_2$.
2. Calcular el error de clasificación esperado:

$$
P(\text{error})
=
\int_{R_2} p(x,\omega_1)\,dx
+
\int_{R_1} p(x,\omega_2)\,dx.
$$

3. Interpretar geométricamente qué ocurre con la frontera si $P(\omega_1)\to 1$.

Como ayuda:

$$
\int \frac{1}{1+u^2}\,du=\arctan(u).
$$

## Diapositiva 5. Definición del Problema

Tenemos dos densidades de Cauchy desplazadas:

$$
p(x \mid \omega_1)=\frac{1}{\pi\left[1+(x-1)^2\right]},
\qquad
p(x \mid \omega_2)=\frac{1}{\pi\left[1+(x+1)^2\right]}.
$$

Las probabilidades a priori son:

$$
P(\omega_1)=\frac{2}{3},
\qquad
P(\omega_2)=\frac{1}{3}.
$$

Con pérdida 0-1, la regla de Bayes decide $\omega_1$ si:

$$
P(\omega_1 \mid x)>P(\omega_2 \mid x).
$$

Por la regla de Bayes, esto equivale a:

$$
p(x \mid \omega_1)P(\omega_1)>p(x \mid \omega_2)P(\omega_2).
$$

## Diapositiva 6. Ejercicio 1(i): Frontera Bayesiana

La regla de decisión puede escribirse mediante la razón de verosimilitudes:

$$
\frac{p(x \mid \omega_1)}{p(x \mid \omega_2)}
>
\frac{P(\omega_2)}{P(\omega_1)}.
$$

En este caso:

$$
\frac{
\frac{1}{\pi\left[1+(x-1)^2\right]}
}{
\frac{1}{\pi\left[1+(x+1)^2\right]}
}
>
\frac{1/3}{2/3}
=
\frac{1}{2}.
$$

Por lo tanto:

$$
\frac{1+(x+1)^2}{1+(x-1)^2}>\frac{1}{2}.
$$

Como los denominadores son positivos:

$$
2\left[1+(x+1)^2\right]>1+(x-1)^2.
$$

Expandiendo:

$$
2x^2+4x+4>x^2-2x+2.
$$

Luego:

$$
x^2+6x+2>0.
$$

## Diapositiva 7. Cálculo Exacto de la Frontera

La igualdad que define los puntos frontera es:

$$
x^2+6x+2=0.
$$

Sus raíces son:

$$
x=\frac{-6\pm\sqrt{36-8}}{2}
=
\frac{-6\pm\sqrt{28}}{2}
=
-3\pm\sqrt{7}.
$$

Entonces:

$$
x_a=-3-\sqrt{7}\approx -5.64,
\qquad
x_b=-3+\sqrt{7}\approx -0.35.
$$

La frontera relevante entre los modos de las densidades es:

$$
x^\ast=x_b=-3+\sqrt{7}\approx -0.354.
$$

## Diapositiva 8. Regiones de Decisión

La regla decide $\omega_1$ cuando:

$$
x^2+6x+2>0.
$$

Como la parábola abre hacia arriba, la desigualdad es verdadera fuera del intervalo entre las raíces:

$$
R_1=
\left\{
x\in\mathbb{R}
\mid
x<-3-\sqrt{7}
\;\text{o}\;
x>-3+\sqrt{7}
\right\}.
$$

La región de decisión para $\omega_2$ es:

$$
R_2=
\left\{
x\in\mathbb{R}
\mid
-3-\sqrt{7}<x<-3+\sqrt{7}
\right\}.
$$

La región $R_1$ queda disjunta por el efecto de las colas pesadas de la distribución de Cauchy.

## Diapositiva 9. Riesgo o Error Esperado

El error de clasificación es la probabilidad de decidir la clase incorrecta:

$$
P(e)
=
\int_{R_2}P(\omega_1)p(x\mid \omega_1)\,dx
+
\int_{R_1}P(\omega_2)p(x\mid \omega_2)\,dx.
$$

Sea:

$$
x_a=-3-\sqrt{7},
\qquad
x_b=-3+\sqrt{7}.
$$

Usando la primitiva de la Cauchy:

$$
\int \frac{1}{\pi\left[1+(x-\mu)^2\right]}\,dx
=
\frac{1}{\pi}\arctan(x-\mu),
$$

se obtiene:

$$
\begin{aligned}
P(e)
&=
\frac{2}{3}
\left[
\frac{\arctan(x-1)}{\pi}
\right]_{x_a}^{x_b}
+
\frac{1}{3}
\left(
1-
\left[
\frac{\arctan(x+1)}{\pi}
\right]_{x_a}^{x_b}
\right) \\
&=
\frac{2}{3\pi}
\left[
\arctan(x_b-1)-\arctan(x_a-1)
\right] \\
&\quad+
\frac{1}{3}
\left(
1-
\frac{1}{\pi}
\left[
\arctan(x_b+1)-\arctan(x_a+1)
\right]
\right).
\end{aligned}
$$

## Diapositiva 10. Interpretación Geométrica

Si $P(\omega_1)\to 1$, entonces:

$$
\frac{P(\omega_2)}{P(\omega_1)}\to 0.
$$

La regla exige cada vez menos evidencia de la verosimilitud para decidir $\omega_1$. En consecuencia:

- la frontera se desplaza hacia la izquierda;
- la región $R_2$ se achica;
- el clasificador decide $\omega_1$ para casi todos los valores de $x$.

En el límite, $R_1$ cubre toda la recta real.

## Diapositiva 11. Ejercicio 2

**Gaussianas y Fronteras de Decisión en $\mathbb{R}^d$**

Considere un problema de clasificación con dos clases gaussianas:

$$
p(x\mid \omega_i)=\mathcal{N}(\mu_i,\Sigma_i),
\qquad
i=1,2,
$$

con probabilidades a priori $P(\omega_i)$. La función discriminante bayesiana es:

$$
g_i(x)=\ln p(x\mid \omega_i)+\ln P(\omega_i).
\tag{3}
$$

Se pide analizar:

1. **Caso $\Sigma_1=\Sigma_2=\sigma^2 I$:** probar que $g_1(x)=g_2(x)$ define un hiperplano, obtener su vector normal y determinar cuándo pasa por el punto medio $\frac{1}{2}(\mu_1+\mu_2)$.
2. **Caso $\Sigma_1=\Sigma_2=\Sigma$:** derivar la frontera lineal, dar su interpretación en términos de distancia de Mahalanobis y explicar el rol de $\Sigma^{-1}$ como blanqueo.
3. **Caso $\Sigma_1\ne\Sigma_2$:** probar que la frontera es cuadrática e identificar el término $x^TAx$ y la matriz $A$.

Como ayuda:

$$
\ln p(x\mid \omega_i)
=
-\frac{1}{2}(x-\mu_i)^T\Sigma_i^{-1}(x-\mu_i)
-\frac{d}{2}\ln(2\pi)
-\frac{1}{2}\ln|\Sigma_i|.
\tag{4}
$$

## Diapositiva 12. Caso (i): Covarianza Esférica Común

Supongamos:

$$
\Sigma_1=\Sigma_2=\sigma^2 I.
$$

Entonces:

$$
\Sigma_i^{-1}=\frac{1}{\sigma^2}I,
\qquad
|\Sigma_i|=(\sigma^2)^d.
$$

La función discriminante es:

$$
\begin{aligned}
g_i(x)
&=
-\frac{1}{2}(x-\mu_i)^T
\left(\frac{1}{\sigma^2}I\right)
(x-\mu_i)
-\frac{d}{2}\ln(2\pi)
-\frac{1}{2}\ln(\sigma^{2d})
+\ln P(\omega_i).
\end{aligned}
$$

## Diapositiva 13. Función Discriminante en el Caso Esférico

Expandiendo:

$$
(x-\mu_i)^T(x-\mu_i)
=
x^Tx-2\mu_i^Tx+\mu_i^T\mu_i.
$$

Los términos comunes a ambas clases se cancelan al comparar $g_1$ y $g_2$. Por lo tanto, basta considerar:

$$
g_i(x)
=
\frac{1}{\sigma^2}\mu_i^T x
-\frac{1}{2\sigma^2}\mu_i^T\mu_i
+\ln P(\omega_i).
$$

La frontera $g_1(x)=g_2(x)$ queda:

$$
\frac{1}{\sigma^2}(\mu_1-\mu_2)^Tx
-\frac{1}{2\sigma^2}
\left(\lVert\mu_1\rVert^2-\lVert\mu_2\rVert^2\right)
+\ln\frac{P(\omega_1)}{P(\omega_2)}
=0.
$$

El vector normal del hiperplano es:

$$
w=\frac{1}{\sigma^2}(\mu_1-\mu_2).
$$

Como $\frac{1}{\sigma^2}$ es un escalar positivo, la normal es proporcional a $\mu_1-\mu_2$ y, por lo tanto, perpendicular al segmento que une los centros.

## Diapositiva 14. Ecuación Normal y Punto Medio

Sea:

$$
x_{\text{mid}}=\frac{1}{2}(\mu_1+\mu_2).
$$

Si las probabilidades a priori son iguales, entonces:

$$
\ln\frac{P(\omega_1)}{P(\omega_2)}=0.
$$

Evaluando la frontera en $x_{\text{mid}}$:

$$
\frac{1}{\sigma^2}(\mu_1-\mu_2)^T x_{\text{mid}}
=
\frac{1}{2\sigma^2}
\left(\lVert\mu_1\rVert^2-\lVert\mu_2\rVert^2\right),
$$

por lo que los términos se cancelan. La frontera pasa por el punto medio si y solo si los priors son iguales.

Si $P(\omega_1)>P(\omega_2)$, entonces:

$$
\ln\frac{P(\omega_1)}{P(\omega_2)}>0.
$$

El efecto es desplazar la frontera lejos de $\mu_1$, ampliando la región de decisión $R_1$.

## Diapositiva 15. Caso (ii): Covarianza Común General

Supongamos ahora:

$$
\Sigma_1=\Sigma_2=\Sigma,
$$

con $\Sigma$ definida positiva. La función discriminante es:

$$
g_i(x)
=
-\frac{1}{2}(x-\mu_i)^T\Sigma^{-1}(x-\mu_i)
-\frac{d}{2}\ln(2\pi)
-\frac{1}{2}\ln|\Sigma|
+\ln P(\omega_i).
$$

Al comparar dos clases, los términos constantes comunes se cancelan. Expandiendo:

$$
(x-\mu_i)^T\Sigma^{-1}(x-\mu_i)
=
x^T\Sigma^{-1}x
-2\mu_i^T\Sigma^{-1}x
+\mu_i^T\Sigma^{-1}\mu_i.
$$

El término cuadrático $x^T\Sigma^{-1}x$ también se cancela, por lo que la frontera sigue siendo lineal.

## Diapositiva 16. Frontera Lineal con Covarianza Común

La frontera puede escribirse como:

$$
w^T(x-x_0)=0,
$$

donde:

$$
w=\Sigma^{-1}(\mu_1-\mu_2).
$$

Un punto sobre el hiperplano es:

$$
x_0
=
\frac{1}{2}(\mu_1+\mu_2)
-
\frac{
\ln\frac{P(\omega_1)}{P(\omega_2)}
}{
(\mu_1-\mu_2)^T\Sigma^{-1}(\mu_1-\mu_2)
}
(\mu_1-\mu_2).
$$

También se puede escribir:

$$
w^Tx+w_0=0,
$$

con:

$$
w_0
=
-\frac{1}{2}\mu_1^T\Sigma^{-1}\mu_1
+\frac{1}{2}\mu_2^T\Sigma^{-1}\mu_2
+\ln\frac{P(\omega_1)}{P(\omega_2)}.
$$

## Diapositiva 17. Derivación de la Frontera

La igualdad de discriminantes es:

$$
-\frac{1}{2}(x-\mu_1)^T\Sigma^{-1}(x-\mu_1)
+\ln P(\omega_1)
=
-\frac{1}{2}(x-\mu_2)^T\Sigma^{-1}(x-\mu_2)
+\ln P(\omega_2).
$$

Llevando todo a un lado:

$$
-\frac{1}{2}(x-\mu_1)^T\Sigma^{-1}(x-\mu_1)
+\frac{1}{2}(x-\mu_2)^T\Sigma^{-1}(x-\mu_2)
+\ln\frac{P(\omega_1)}{P(\omega_2)}
=0.
$$

La solución final se interpreta como el punto medio más un desplazamiento inducido por los priors:

$$
x_0
=
\frac{1}{2}(\mu_1+\mu_2)
-
\frac{
\ln\frac{P(\omega_1)}{P(\omega_2)}
}{
(\mu_1-\mu_2)^T\Sigma^{-1}(\mu_1-\mu_2)
}
(\mu_1-\mu_2).
$$

## Diapositiva 18. Expansión Algebraica

Usamos:

$$
(a-b)^TM(a-b)=a^TMa-2b^TMa+b^TMb.
$$

Entonces:

$$
(x-\mu_1)^T\Sigma^{-1}(x-\mu_1)
=
x^T\Sigma^{-1}x
-2\mu_1^T\Sigma^{-1}x
+\mu_1^T\Sigma^{-1}\mu_1,
$$

y:

$$
(x-\mu_2)^T\Sigma^{-1}(x-\mu_2)
=
x^T\Sigma^{-1}x
-2\mu_2^T\Sigma^{-1}x
+\mu_2^T\Sigma^{-1}\mu_2.
$$

Al cancelar los términos cuadráticos:

$$
\begin{aligned}
&-\frac{1}{2}
\left[
-2\mu_1^T\Sigma^{-1}x
+\mu_1^T\Sigma^{-1}\mu_1
+2\mu_2^T\Sigma^{-1}x
-\mu_2^T\Sigma^{-1}\mu_2
\right]
+\ln\frac{P(\omega_1)}{P(\omega_2)}
=0.
\end{aligned}
$$

Luego:

$$
\mu_1^T\Sigma^{-1}x
-\mu_2^T\Sigma^{-1}x
-\frac{1}{2}\mu_1^T\Sigma^{-1}\mu_1
+\frac{1}{2}\mu_2^T\Sigma^{-1}\mu_2
+\ln\frac{P(\omega_1)}{P(\omega_2)}
=0.
$$

Factorizando:

$$
(\mu_1-\mu_2)^T\Sigma^{-1}x
+
\left[
-\frac{1}{2}\mu_1^T\Sigma^{-1}\mu_1
+\frac{1}{2}\mu_2^T\Sigma^{-1}\mu_2
+\ln\frac{P(\omega_1)}{P(\omega_2)}
\right]
=0.
$$

Esta es la forma canónica:

$$
w^Tx+w_0=0,
\qquad
w=\Sigma^{-1}(\mu_1-\mu_2).
$$

## Diapositiva 19. Interpretación Mahalanobis

El denominador que aparece en el desplazamiento por priors es la distancia de Mahalanobis cuadrática entre medias:

$$
d_M^2(\mu_1,\mu_2)
=
(\mu_1-\mu_2)^T\Sigma^{-1}(\mu_1-\mu_2).
$$

Si las medias están muy separadas en distancia de Mahalanobis, el efecto de los priors es pequeño. Si están cerca, los priors desplazan mucho la frontera.

Con priors iguales, decidir por la clase más probable equivale a decidir por el centro más cercano en distancia de Mahalanobis:

$$
r_i^2=(x-\mu_i)^T\Sigma^{-1}(x-\mu_i).
$$

La matriz $\Sigma^{-1}$ actúa como una transformación de blanqueo. Si:

$$
\Sigma^{-1}=\Phi\Phi^T,
\qquad
y=\Phi^Tx,
$$

entonces la transformación decorrela y normaliza las direcciones principales de los datos.

## Diapositiva 20. Caso (iii): Covarianzas Distintas

Cuando:

$$
\Sigma_1\ne\Sigma_2,
$$

cada clase tiene una forma propia. La función discriminante es:

$$
g_i(x)
=
-\frac{1}{2}(x-\mu_i)^T\Sigma_i^{-1}(x-\mu_i)
-\frac{d}{2}\ln(2\pi)
-\frac{1}{2}\ln|\Sigma_i|
+\ln P(\omega_i).
$$

La frontera $g_1(x)-g_2(x)=0$ queda:

$$
x^TAx+b^Tx+c=0.
$$

Por lo tanto, la frontera es cuadrática. Según los autovalores de $A$, puede tomar formas como elipsoides, hiperboloides o paraboloides.

## Diapositiva 21. Coeficientes de la Frontera Cuadrática

El término cuadrático de $g_1(x)-g_2(x)$ es:

$$
x^T
\left(
-\frac{1}{2}\Sigma_1^{-1}
+\frac{1}{2}\Sigma_2^{-1}
\right)
x.
$$

Por lo tanto:

$$
A=\frac{1}{2}\left(\Sigma_2^{-1}-\Sigma_1^{-1}\right).
$$

El término lineal es:

$$
b=\Sigma_1^{-1}\mu_1-\Sigma_2^{-1}\mu_2.
$$

El término independiente es:

$$
c
=
\frac{1}{2}\mu_2^T\Sigma_2^{-1}\mu_2
-\frac{1}{2}\mu_1^T\Sigma_1^{-1}\mu_1
+\ln\frac{|\Sigma_2|^{1/2}}{|\Sigma_1|^{1/2}}
+\ln\frac{P(\omega_1)}{P(\omega_2)}.
$$

## Diapositiva 22. Hoja de Ruta

**¿Dónde estamos en la materia?**

- **Clases 1-5:** modelos paramétricos y decisión bayesiana.
- **Clase 6:** PCA/FDA y cambios de geometría.
- **Clase 7:** k-NN y métodos no paramétricos.
- **Clase 8:** discriminantes lineales.
- **Hoy:** revisión de funciones de optimización e introducción del rigor estadístico de la evaluación empírica.

## Diapositiva 23. La Ilusión del Entrenamiento

**Sección:** La Ilusión del Entrenamiento.

## Diapositiva 24. Entrenemos Diferentes Modelos con los Mismos Datos

Se comparan fronteras finales aprendidas por distintos modelos lineales sobre los mismos datos. La diapositiva referencia los notebooks:

- `linear_classification_from_scratch.ipynb`
- `linear_classification_linearly_separable_from_scratch.ipynb`

![Fronteras finales de distintos modelos lineales](figures/clase-9/fig-24-model-frontiers.png)

## Diapositiva 25. Sesgo de Supervivencia

La diapositiva muestra el ejemplo clásico del análisis de Abraham Wald sobre aviones que regresaban de combate.

La cita destacada es:

> The armor, said Wald, doesn't go where the bullet holes are. It goes where the bullet holes aren't: on the engines.

![Avión con impactos usado para ilustrar sesgo de supervivencia](figures/clase-9/fig-25-survivorship-plane.png)

## Diapositiva 26. Sesgo de Supervivencia en Aprendizaje Automático

Hasta ahora entrenamos y miramos los mismos datos. Si se evalúa clasificando el conjunto de entrenamiento, se corre el riesgo de medir una ilusión.

Un valor:

$$
J=0
$$

puede significar que el modelo separó perfectamente el conjunto observado. Pero en un perceptrón con datos separables, o en 1-NN, también puede indicar memorización de una muestra sesgada.

El objetivo real no es clasificar el pasado, sino predecir datos futuros o nuevos.

## Diapositiva 27. Qué Estamos Minimizando

Las funciones de pérdida vistas pueden escribirse como:

$$
J(w)=\sum_{i=1}^n \Phi\left(y_i f(x_i)\right).
$$

Para un clasificador lineal:

$$
f(x)=w^Tx+b.
$$

El valor:

$$
z=yf(x)
$$

mide si la predicción es correcta y con qué margen:

- si $z>0$, la clasificación es correcta;
- si $z<0$, la clasificación es incorrecta.

El sesgo $b$ también aparece escrito como $w_0$.

## Diapositiva 28. Zoológico de Pérdidas

En función del margen $z=yf(x)$:

- **Pérdida 0-1:**

$$
\mathbb{I}(z<0).
$$

- **Pérdida del perceptrón:**

$$
\max(0,-z).
$$

- **Hinge loss de SVM:**

$$
\max(0,1-z).
$$

- **Pérdida logística:**

$$
\ln(1+e^{-z}).
$$

La pérdida 0-1 es natural para clasificación, pero no es diferenciable.

## Diapositiva 29. Impacto en el Gradiente

Cada pérdida induce un comportamiento distinto durante la optimización:

- el perceptrón aplica una corrección constante mientras el punto esté mal clasificado;
- la pérdida logística reduce gradualmente el efecto de un punto cuanto más lejos está de la frontera;
- SVM ignora los puntos que quedan fuera del margen, lo que induce una solución dispersa basada en vectores soporte.

## Diapositiva 30. Formalización: Riesgo y Pérdida

Sea:

$$
x\in\mathcal{X},
\qquad
y\in\mathcal{Y},
$$

y sea $f(x;\theta)$ un clasificador parametrizado. Definimos una función de pérdida:

$$
L(y,f(x;\theta)).
$$

En las primeras clases, esta pérdida aparecía como:

$$
L=\lambda(a_i\mid \omega_j).
$$

Para clasificación con pérdida 0-1:

$$
L(y,\hat y)
=
\begin{cases}
0 & \text{si } y=\hat y,\\
1 & \text{si } y\ne \hat y.
\end{cases}
$$

Los datos se suponen generados por una distribución conjunta desconocida:

$$
P(x,y).
$$

## Diapositiva 31. Riesgo Real o Riesgo Esperado

El riesgo esperado de un modelo parametrizado por $\theta$ es:

$$
R(\theta)
=
\mathbb{E}_{(x,y)\sim P}
\left[
L(y,f(x;\theta))
\right]
=
\int L(y,f(x;\theta))\,dP(x,y).
$$

El problema es que $P(x,y)$ es desconocida. Por eso, el riesgo real no puede calcularse directamente.

## Diapositiva 32. Estimación de Promedios

Para una colección de números $a(i)$, el promedio es:

$$
\bar a=\frac{1}{n}\sum_{i=1}^n a(i).
$$

Podemos verlo como una esperanza. Sea $X$ una variable discreta uniforme sobre los índices:

$$
P(X=i)=\frac{1}{n}.
$$

Entonces:

$$
\bar a
=
\sum_i \frac{1}{n}a(i)
=
\sum_i P(X=i)a(i)
=
\mathbb{E}[a(X)].
$$

## Diapositiva 33. Estimación y Ley de los Grandes Números

Como:

$$
\bar a=\mathbb{E}[a(X)],
$$

si tomamos muestras independientes $X_1,\ldots,X_k$, podemos estimar:

$$
\hat{\bar a}_k
=
\frac{1}{k}\sum_{i=1}^k a(X_i).
$$

Por la ley de los grandes números:

$$
\hat{\bar a}_k\to \bar a.
$$

Recordatorio: si $X_1,\ldots,X_n$ son iid con media $\mu$, entonces:

$$
S_n=\frac{1}{n}\sum_{i=1}^n X_i
\quad\Longrightarrow\quad
\lim_{n\to\infty}S_n=\mu.
$$

## Diapositiva 34. Integración Monte Carlo

Para una esperanza:

$$
\mathbb{E}[f(x)]
=
I
=
\int_{\mathcal{R}} f(x)p(x)\,dx,
$$

si tenemos muestras iid $x_1,\ldots,x_n$ tomadas de $p$, podemos aproximar:

$$
\hat I_n
=
\frac{1}{n}\sum_{i=1}^n f(x_i).
$$

Propiedades:

- es insesgado: $\mathbb{E}[\hat I_n]=I$;
- es consistente: $\hat I_n\to I$ con probabilidad 1;
- el error de convergencia es $O(n^{-1/2})$, independientemente de la dimensión.

## Diapositiva 35. Riesgo Empírico

Con un conjunto finito de entrenamiento:

$$
\mathcal{D}=\{(x_i,y_i)\}_{i=1}^n,
$$

el riesgo empírico se define como:

$$
R_{\text{emp}}(\theta)
=
\frac{1}{n}\sum_{i=1}^n L(y_i,f(x_i;\theta)).
$$

El principio de minimización del riesgo empírico propone elegir $\theta$ minimizando $R_{\text{emp}}$.

La pregunta crítica es:

$$
R_{\text{emp}}\approx R?
$$

Modelos demasiado complejos, como 1-NN o polinomios de grado alto, pueden memorizar $\mathcal{D}$ y forzar $R_{\text{emp}}\to 0$, mientras que el riesgo esperado $R$ sigue siendo alto. Este fenómeno es sobreajuste.

## Diapositiva 36. Hold-Out

Se divide el conjunto de datos $\mathcal{D}$, de tamaño $n$, en:

- $\mathcal{D}_{\text{train}}$, de tamaño $n-m$, para ajustar $\theta$;
- $\mathcal{D}_{\text{test}}$, de tamaño $m$, para estimar el riesgo real.

El estimador hold-out es:

$$
\hat R_{\text{ho}}
=
\frac{1}{m}
\sum_{(x_i,y_i)\in\mathcal{D}_{\text{test}}}
L(y_i,f(x_i;\theta_{\text{train}})).
$$

Dilema:

- si $m$ es grande, la estimación tiene menor varianza, pero el modelo se entrena con menos datos;
- si $m$ es pequeño, el modelo se entrena con más datos, pero la estimación tiene mayor varianza.

## Diapositiva 37. Cross-Validation: K-Fold

Se divide el conjunto de datos en $K$ particiones:

$$
\mathcal{D}_1,\ldots,\mathcal{D}_K,
$$

cada una de tamaño aproximado $n/K$. Para cada $k$:

- se entrena con $\mathcal{D}\setminus\mathcal{D}_k$;
- se evalúa sobre $\mathcal{D}_k$.

El estimador de validación cruzada es:

$$
\hat R_{\text{cv}}
=
\frac{1}{K}\sum_{k=1}^K R_{\text{test}}^{(k)}.
$$

Es una forma eficiente de usar todos los datos tanto para entrenamiento como para evaluación.

## Diapositiva 38. Esquema de K-Fold

La diapositiva muestra el particionado de los datos en folds y cómo cada fold se usa una vez como test mientras los restantes se usan como entrenamiento.

![Diagrama de validación cruzada K-fold](figures/clase-9/fig-38-kfold-cross-validation.png)

## Diapositiva 39. Leave-One-Out Cross-Validation

Leave-One-Out Cross-Validation corresponde al caso:

$$
K=n.
$$

En cada iteración se entrena con $n-1$ muestras y se evalúa en la muestra restante.

Características:

- el sesgo es bajo, porque cada modelo se entrena con casi todos los datos;
- la varianza puede ser alta, porque los modelos entrenados comparten $n-2$ muestras;
- el costo es $O(nC)$, donde $C$ es el costo de entrenar el modelo.

Para modelos costosos puede ser prohibitivo, pero es especialmente conveniente en k-NN. Para 1-NN, el error LOOCV puede calcularse en $O(1)$ por muestra si ya se precomputó la matriz de distancias.

## Diapositiva 40. Jackknife

El jackknife considera estimadores calculados dejando afuera una observación por vez:

$$
\hat\theta_{(i)}
\quad
\text{omite la muestra } i.
$$

El promedio de estos estimadores es:

$$
\hat\theta_{(\cdot)}
=
\frac{1}{n}\sum_{i=1}^n \hat\theta_{(i)}.
$$

La estimación jackknife de la varianza es:

$$
\widehat{\operatorname{Var}}_{\text{jack}}(\hat\theta)
=
\frac{n-1}{n}
\sum_{i=1}^n
\left(\hat\theta_{(i)}-\hat\theta_{(\cdot)}\right)^2.
$$

El factor $n-1$ corrige la correlación entre estimadores, ya que cada uno comparte casi todos los datos con los demás.

## Diapositiva 41. Bootstrap

El bootstrap fue introducido por B. Efron en 1982.

Idea central:

- usar la muestra disponible como una aproximación de la población;
- remuestrear con reemplazo desde esa muestra;
- aproximar la precisión de un estimador a partir de los remuestreos.

El método ayuda a estimar cantidades como:

- error cuadrático medio;
- desviación estándar;
- varianza;
- distribución aproximada de un estimador cuando la distribución real es desconocida.

## Diapositiva 42. Receta para Realizar el Bootstrap

La idea central del método es simple:

- dada una muestra aleatoria con $n$ observaciones, se trata como si fuera toda la población;
- de esa población empírica se extraen $B$ muestras con reposición;
- para cada una de las $B$ nuevas muestras, se calcula una estimación del parámetro de interés.

Los $B$ valores bootstrap estimados se usan para aproximar la distribución del estimador del parámetro.

![Histograma de estimaciones bootstrap](figures/clase-9/fig-42-bootstrap-histogram.png)

## Diapositiva 43. Error Cuadrático Medio Bootstrap

Sea una muestra:

$$
\{X_i\}_{i=1}^n,
$$

generada por una distribución subyacente $F_X(x;\theta)$. Sea $\theta(F)$ el parámetro de interés y:

$$
\hat\theta=g(X_1,\ldots,X_n)
$$

un estimador de $\theta(F)$.

El objetivo es cuantificar la incertidumbre de $\hat\theta$. El error cuadrático medio es:

$$
\operatorname{ECM}(\theta,F)
=
\mathbb{E}_F
\left[
\left(
g(X_1,\ldots,X_n)-\theta(F)
\right)^2
\right].
$$

Por ejemplo, si $\theta(F)=\mathbb{E}[X_i]$ y $g=\bar X$, entonces:

$$
\operatorname{ECM}(F)=\frac{S^2}{n}.
$$

## Diapositiva 44. Técnica de Bootstrap

El valor:

$$
\operatorname{ECM}(\theta,F)
=
\mathbb{E}_F
\left[
\left(
g(X_1,X_2,\ldots,X_n)-\theta(F)
\right)^2
\right]
$$

podría calcularse si se conociera teóricamente $F$. Sin embargo, muchas veces no se tiene un fundamento teórico para plantear una forma funcional de $F$, y aun si lo hubiera se necesitarían sus parámetros.

La función acumulada empírica $F_e$ brinda una buena aproximación a la función $F$.

![Aproximación de la función acumulada empírica a la función acumulada real](figures/clase-9/fig-44-empirical-cdf-approximation.png)

## Diapositiva 45. Técnica de Bootstrap: Cómputo Directo

Se quieren estimar cantidades como:

$$
\operatorname{Var}(\hat\theta)
\qquad
\text{y}
\qquad
\operatorname{ECM}(\hat\theta,\theta)
=
\mathbb{E}
\left[
(\hat\theta-\theta)^2
\right].
$$

En general, el cálculo directo es difícil. Por ejemplo:

$$
\operatorname{ECM}(\hat\theta,\theta)
=
\int\cdots\int
\left(
g(x_1,\ldots,x_n)-\theta
\right)^2
f(x_1)\cdots f(x_n)
\,dx_1\cdots dx_n.
$$

El bootstrap reemplaza la distribución desconocida por la distribución empírica.

## Diapositiva 46. Distribución Empírica

Dado un conjunto de datos observados $x_1,\ldots,x_n$, se define la función acumulada empírica $F_e$. Primero se ordenan los datos:

$$
x_{(1)},x_{(2)},\ldots,x_{(n)}.
$$

Luego:

$$
F_e(x)
=
\begin{cases}
0 & x<x_{(1)},\\
\frac{i}{n} & x_{(i)}\le x<x_{(i+1)},\quad 1\le i<n,\\
1 & x_{(n)}\le x.
\end{cases}
$$

La interpretación es:

$$
F_e(x_{(i)})=\frac{i}{n}
\approx
\text{proporción de } x_j \text{ menores que } x_{(i)}.
$$

![Función acumulada empírica escalonada](figures/clase-9/fig-46-empirical-cdf-step.png)

## Diapositiva 47. Aproximación mediante $F_e$

Si $n$ es grande, el teorema de Glivenko-Cantelli establece que:

$$
F_e\to F
$$

uniformemente con probabilidad 1 cuando $n\to\infty$.

Por lo tanto:

$$
\operatorname{ECM}(F)
\approx
\operatorname{ECM}(F_e)
=
\mathbb{E}_{F_e}
\left[
\left(
g(X_1,\ldots,X_n)-\theta(F_e)
\right)^2
\right].
$$

Si $\theta(F)$ depende continuamente de $F$, entonces $\theta(F_e)$ aproxima a $\theta(F)$. Así se obtiene una aproximación bootstrap del error cuadrático medio.

## Diapositiva 48. $F_e$ como Distribución de Probabilidad

La función $F_e$ es la distribución acumulada de una variable aleatoria $X_e$ que toma valores en los datos observados:

$$
x_1,\ldots,x_n,
$$

con probabilidad:

$$
P(X_e=x_i)=\frac{1}{n}.
$$

Por ejemplo, si:

$$
\theta(F)=\operatorname{Var}_F(X),
$$

entonces:

$$
\theta(F_e)
=
\operatorname{Var}_{F_e}(X)
=
\frac{1}{n}
\sum_{i=1}^n
(x_i-\bar x)^2.
$$

## Diapositiva 49. Valor de Expectación con $F_e(x)$

Para calcular:

$$
\mathbb{E}_{F_e}
\left[
\left(
g(X_1,X_2,\ldots,X_n)-\theta(F_e)
\right)^2
\right],
$$

tenemos en cuenta que $X_1,X_2,\ldots,X_n$ son iid con distribución $F_e$. Por lo tanto:

$$
(X_1,X_2,\ldots,X_n)
$$

puede tomar valores:

$$
(x_{i_1},x_{i_2},\ldots,x_{i_n}),
\qquad
i_j\in\{1,2,\ldots,n\},
\qquad
j=1,2,\ldots,n.
$$

Cada combinación tiene probabilidad:

$$
\frac{1}{n^n}.
$$

Así, hay $n^n$ posibles permutaciones con igual probabilidad, y:

$$
\operatorname{ECM}(F_e)
=
\sum_{\text{todas las permutaciones}}
\frac{
\left(
g(\vec{x})-\theta(F_e)
\right)^2
}{n^n}.
$$

Cuando $n$ es grande, $n^n$ es un número muy grande. Por ejemplo, si $n=10$:

$$
n^n=10^{10}.
$$

## Diapositiva 50. Técnica de Bootstrap

En lugar de calcular el valor de expectación exacto:

$$
\sum_{1\le i_1\le n}
\cdots
\sum_{1\le i_n\le n}
\frac{
\left(
g(x_{i_1},x_{i_2},\ldots,x_{i_n})-\mu(F_e)
\right)^2
}{n^n},
$$

se hace una aproximación Monte Carlo, eligiendo algunos términos al azar. Esto equivale a tomar $B$ muestras aleatorias:

$$
(X_1^j,X_2^j,\ldots,X_n^j),
\qquad
1\le j\le B.
$$

Para cada muestra bootstrap:

$$
\begin{aligned}
Y_1
&=
\left(
g(X_1^1,X_2^1,\ldots,X_n^1)-\mu(F_e)
\right)^2,\\
Y_2
&=
\left(
g(X_1^2,X_2^2,\ldots,X_n^2)-\mu(F_e)
\right)^2,\\
&\vdots\\
Y_B
&=
\left(
g(X_1^B,X_2^B,\ldots,X_n^B)-\mu(F_e)
\right)^2.
\end{aligned}
$$

Entonces:

$$
\operatorname{ECM}_e(\hat\mu)
\approx
\frac{\sum_{j=1}^B Y_j}{B}.
$$

## Diapositiva 51. Bootstrap y Monte Carlo

La técnica bootstrap se interpreta como una aproximación Monte Carlo de una esperanza bajo $F_e$:

$$
(X_1^j,X_2^j,\ldots,X_n^j),
\qquad
1\le j\le B.
$$

Se definen:

$$
\begin{aligned}
Y_1
&=
\left(
g(X_1^1,X_2^1,\ldots,X_n^1)-\mu(F_e)
\right)^2,\\
Y_2
&=
\left(
g(X_1^2,X_2^2,\ldots,X_n^2)-\mu(F_e)
\right)^2,\\
&\vdots\\
Y_B
&=
\left(
g(X_1^B,X_2^B,\ldots,X_n^B)-\mu(F_e)
\right)^2.
\end{aligned}
$$

Y se estima:

$$
\operatorname{ECM}_e(\hat\mu)
\approx
\frac{\sum_{j=1}^B Y_j}{B}.
$$

## Diapositiva 52. Out-of-Bag

En una muestra bootstrap $\mathcal{D}^\ast$, cada extracción elige una de las $n$ observaciones originales con reemplazo.

La probabilidad de que una observación $x_i$ no sea seleccionada en una extracción es:

$$
1-\frac{1}{n}.
$$

La probabilidad de que no sea seleccionada en las $n$ extracciones es:

$$
P(x_i\notin \mathcal{D}^\ast)
=
\left(1-\frac{1}{n}\right)^n.
$$

Usando:

$$
\lim_{n\to\infty}
\left(1-\frac{1}{n}\right)^n
=
e^{-1}
\approx
0.368,
$$

en promedio una muestra bootstrap contiene aproximadamente el $63.2\%$ de las observaciones originales únicas, y el $36.8\%$ restante queda fuera de bolsa (*out-of-bag*).

## Diapositiva 53. Estimador Bootstrap .632

Como cada modelo bootstrap se entrena con alrededor del $63.2\%$ de observaciones únicas, el error out-of-bag puede ser pesimista.

La corrección de Efron combina el error de entrenamiento, optimista, con el error out-of-bag, más pesimista:

$$
\hat R_{.632}
=
0.368\,R_{\text{emp}}
+
0.632\,R_{\text{OOB}}.
$$

## Diapositiva 54. Bibliografía

Referencia principal:

- T. Hastie, R. Tibshirani y J. Friedman, **The Elements of Statistical Learning**, capítulo 7.

## Diapositiva 55. Resumen

**¿Qué construimos hasta ahora?**

1. **El modelo ideal:** Bayes. Si conocemos todo, la decisión óptima es analítica.
2. **La realidad gaussiana:** estimar $\mu$ y $\Sigma$, y usar PCA/FDA cuando la dimensión es alta.
3. **La rebelión empírica:** Parzen, k-NN y perceptrón. Cuando no conocemos la forma de la distribución, los datos construyen la frontera.
4. **El juez estadístico:** validación cruzada, bootstrap y ROC. Herramientas para verificar que no nos estamos engañando.

Con esto queda preparado el terreno para selección de modelos y regularización.
