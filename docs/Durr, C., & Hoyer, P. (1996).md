# A quantum algorithm for finding the minimum

## 1. Introducción
Sea $T[0..N-1]$ una tabla desordenada de N elementos, cada uno contiene un valor de un conjunto ordenado. Para simplificar, asuma que todos los valores son diferentes. El problema de búsqueda del mínimo es encontrar el índice $y$ tal que $T[y]$ es mínimo. Esto claramente requiere de un número lineal de sondeos en una máquina de Turing probabilística clásica.
Acá vamos a dar un algoritmo cuántico simple que resuelve el problema usando $O(\sqrt{N})$ sondeos. La subrutina principal es el **algoritmo cuántico de búsqueda exponencial**, el cual es una generalización del reciente algoritmo [[Grover]]. Debido a un límite inferior general (de la ref. 1), esto está dentro de un factor constante del óptimo.
## 2. El algoritmo
Nuestro algoritmo invoca el algoritmo de búsqueda exponencial cuántica de *M. Boyer, G. Brassard, P. Høyer et. al.* como una subrutina para encontrar el índice de un elemento más pequeño que el valor determinado por un índice de *umbral particular*. El resultado se elige entonces como el nuevo umbral. Este proceso se repite hasta que la probabilidad de que el índice de umbral seleccione el mínimo sea suficientemente grande.
Si hay $t ≥ 1$ entradas marcadas en la tabla, el algoritmo de búsqueda exponencial cuántica devolverá una de ellas con la misma probabilidad después de un número esperado de $O(\sqrt{N/t})$ *iteraciones*. Si no hay ninguna entrada marcada, se ejecutará indefinidamente. Obtenemos el siguiente teorema.

> **Teorema 1** *El algoritmo que se muestra a continuación encuentra el índice del valor mínimo con una probabilidad de al menos 1/2 . Su tiempo de ejecución es O(√N).*

Primero damos el algoritmo de búsqueda mínimo, luego la prueba de la probabilidad de éxito.

**Quantum Minimum Searching Algorithm**
1. Escoger un indice de umbral $0 \leq y \leq N-1$ de manera uniforme y aleatoria.
2. Repetir lo siguiente e interrumpir cuando el tiempo total de ejecución sea más que $22.5\sqrt N + 1.4 log^2 N$ Entonces ir a la etapa 2(2.3)
	1. Inicializar la memoria como $\sum_j \frac{1}{\sqrt{N}} \ket{j} \ket{y}$. Marcar cada item $j$ para el cual $T[j] < T[y]$.
	2. Aplicar el algoritmo cuántico de búsqueda de *M. Boyer, G. Brassard, P. Høyer et. al.*
	3. Observar el primer registro: sea $y'$ la salida. Si $T[y'] < T[y]$, entonces colocar el índice del umbral $y$ a $y'$.
3. Devolver $y$.

(...)
## 3. Observaciones finales
La probabilidad de éxito puede ser mejorada corriendo el algoritmo $c$ veces. Sea $y$ tal que $T[y]$ es el mínimo entre los resultados. Con probabilidad al menos de $1- 1/2^c$ , entonces, $T[y]$ mantiene el mínimo de la tabla. Claramente la probabilidad de éxito es incluso mejor si corremos el algoritmo, solo una vez con time out $c·2m_0$. Porque luego utilizamos la información proporcionada por los pasos anteriores.
Si los valores de $T$ no son distintos, podemos usar el mismo algoritmo para el caso simplificado. El análisis del caso general no cambia, excepto que el lema 1 en la ecuación $p(t,r) = 1/r$ ahora se vuelva una inecuación $p(t,r) \leq 1/r$. Por lo tanto, el límite inferior para la probabilidad de éxito dado en el teorema 1 para el caso simplificado es también un límite inferior para el caso general.
## Cita
Durr, C., & Hoyer, P. (1996). A quantum algorithm for finding the minimum. _arXiv preprint quant-ph/9607014_.

#paper