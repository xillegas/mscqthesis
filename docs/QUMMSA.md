El algoritmo **QUMMSA** (Quantum Maximum or Minimum Searching Algorithm) es una versión optimizada del algoritmo de [[Durr, C., & Hoyer, P. (1996)]] (DHA) para buscar el máximo o mínimo en una base de datos no ordenada utilizando computación cuántica. Este algoritmo utiliza el Grover-Long Algorithm, que elimina la tasa de fallos teóricos del algoritmo de Grover estándar y mejora la eficiencia en escenarios de bases de datos grandes. A continuación, se explica detalladamente:
### Problema

Dado un conjunto de datos no ordenados con N elementos, el objetivo es encontrar el valor máximo o mínimo. En el documento se presenta el caso de búsqueda del mínimo como ejemplo.
### Idea principal

El algoritmo utiliza el Grover-Long Algorithm para encontrar M soluciones (donde M≥1) en la base de datos no ordenada. Se selecciona un valor aleatorio inicial $d_0$ como referencia. Si el algoritmo encuentra un valor $d_1$ menor o igual a $d_0$, este reemplaza a $d_0$ y el proceso se repite hasta que solo quede una solución (M=1). En promedio, el número de iteraciones principales necesarias para encontrar el mínimo es $log_2⁡N$.
### **Hipótesis**

1. Cada valor de datos está representado por una cadena binaria y almacenado en un estado base ortonormal |Ψ⟩.
2. Existe una correspondencia uno a uno entre un valor de datos y su índice.
3. Los valores de datos son enteros y distintos.
4. El estado inicial se prepara en $log_2⁡N$ pasos.
5. El operador de amplitud inicial es $1/\sqrt{N}$.
### **Pseudocódigo**
El pseudocódigo del algoritmo es el siguiente:
1. **Entrada:** Base de datos no ordenada D y un valor aleatorio inicial $d_0$.
2. **Proceso:**
    - Diseñar un oráculo que marque todos los valores menores o iguales a $d_0$.
    - Aplicar el Grover-Long Algorithm al estado inicial |Ψ⟩.
    - Medir el registro cuántico y asignar el resultado a $d_1$.
    - Repetir el proceso hasta que $d_1$<$d_0$.
3. **Salida:** El valor mínimo $d_0$.
### **Mejoras respecto a DHA**
1. **Eliminación de la tasa de fallos teóricos:** Se reemplaza el Quantum Exponential Searching Algorithm (QESA) por el Grover-Long Algorithm, que tiene una tasa de éxito del 100% en teoría.
2. **Condición de interrupción:** Se utiliza una constante c independiente del tamaño de la base de datos para determinar cuándo detener el bucle principal, reduciendo la tasa de fallos exponencialmente.
### **Circuitos cuánticos**
El diseño de los circuitos incluye:
1. **Operador $I_0$:** Realiza una rotación de fase en el estado |0⟩.
2. **Oráculo O:** Marca los estados que cumplen la condición de búsqueda (menores o iguales a $d_0$).
3. **Principios de simplificación:** Se proponen tres principios para reducir la complejidad de los circuitos, minimizando el uso de puertas de control multi-qubit.
### **Demostración experimental**
Se realizaron experimentos en un procesador cuántico IBM de superconductores y simulaciones numéricas con un conjunto de datos real (edades de pasajeros del Titanic). Los resultados mostraron que QUMMSA tiene menor tasa de fallos, menor profundidad de circuitos y menos puertas multi-qubit en comparación con DHA.
### **Ventajas**
1. **Eficiencia:** Menor complejidad con bases de datos grandes.
2. **Flexibilidad:** Puede integrarse como subrutina en otros algoritmos cuánticos.
3. **Implementación práctica:** Los circuitos diseñados son más fáciles de implementar en computadoras cuánticas de propósito general.
### **Conclusión**
QUMMSA es una solución eficiente para problemas de búsqueda de máximo o mínimo en bases de datos no ordenadas, con aplicaciones potenciales en el procesamiento de grandes volúmenes de datos en la era de la computación cuántica.
## Referencias
- [[Chen, Wei, Gao (2019)]]