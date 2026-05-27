Source: [[Y_Chen_et_al_An_Optimized_Quantum_Maximum_or_Minimum_Searching_Algorithm (2).pdf]]
Name: **An Optimized Quantum Maximum or Minimum Searching Algorithm and its Circuits**

Este documento presenta un algoritmo cuántico optimizado para buscar máximos y mínimos en bases de datos, mejorando la eficiencia en comparación con algoritmos clásicos y cuánticos anteriores.

## Algoritmo Cuántico Optimizado para Búsqueda de Máximos y Mínimos

Se presenta un algoritmo cuántico optimizado que mejora la búsqueda de máximos y mínimos en bases de datos no ordenadas, superando las limitaciones de algoritmos clásicos y cuánticos anteriores. - Se propone el algoritmo [[QUMMSA]], que combina el algoritmo de [[Durr, C., & Hoyer, P. (1996)]] (DHA) con el algoritmo de búsqueda cuántica exacta óptima. - El algoritmo logra una probabilidad de éxito cercana al 100% al estimar la relación entre el número de soluciones (M) y el espacio de búsqueda (N). - Se realizaron experimentos en un procesador cuántico IBM, mostrando que QUMMSA es más eficiente que DHA.

## Introducción a la Computación Cuántica

La computación cuántica se presenta como una solución para el procesamiento de grandes volúmenes de datos, superando las limitaciones de los ordenadores clásicos. - Se estima que para 2022 se generarán 77 exabytes de tráfico de datos mensuales. - Algoritmos cuánticos como el de Grover ofrecen una velocidad cuadrática en comparación con algoritmos clásicos. - Se discuten mejoras en el algoritmo de Grover para optimizar la búsqueda de máximos y mínimos.

## Descripción del Algoritmo QUMMSA

El algoritmo QUMMSA se centra en la búsqueda de mínimos en bases de datos no ordenadas utilizando el algoritmo [[Grover-Long]]. 
- Se utiliza un valor de referencia aleatorio y se reemplaza iterativamente hasta encontrar el mínimo. 
- Se estima que el número de iteraciones necesarias es log2(N), donde N es el tamaño de la base de datos. 
- Se eliminan las tasas de fallo teóricas del algoritmo Grover al utilizar el algoritmo Grover-Long.

## Diseño de Circuitos Cuánticos

Se presentan métodos para diseñar circuitos cuánticos que implementan el algoritmo QUMMSA. 
- Se describe la preparación del estado inicial y la construcción de oráculos para marcar soluciones. 
- Se proponen tres principios simplificados para reducir la complejidad de los circuitos. 
- Se enfatiza la importancia de la implementación eficiente en dispositivos cuánticos.
## Experimentos y Simulaciones Realizadas

- Se comparan experimentalmente el algoritmo QUMMSA y el DHA utilizando un procesador cuántico de IBM y simulaciones numéricas. 
- Se realizaron experimentos con 2 qubits, mostrando que QUMMSA tiene menor profundidad de circuito y menor tasa de fallo. 
- En simulaciones con 6 qubits, se utilizó un conjunto de datos de la edad de los pasajeros del Titanic, demostrando la eficiencia del algoritmo. 
- Los resultados indican que QUMMSA es más eficiente que el algoritmo QESA utilizado en DHA.

## Análisis de la Tasa de Fallo

Se analiza la tasa de fallo del algoritmo QUMMSA y se proponen métodos para reducirla. - La tasa de fallo se debe a la incertidumbre en el número de soluciones y a la selección de condiciones de interrupción. - Se sugiere utilizar una función de distribución de muestreo para mejorar la estimación de parámetros. - Se propone un método para determinar cuándo finalizar el bucle principal, aumentando la probabilidad de éxito.

## Comparación de Complejidad entre Algoritmos

Se compara la **complejidad** del algoritmo QUMMSA con el DHA. - La complejidad se basa en el número total de iteraciones de Grover-Long y la preparación del estado inicial. - Se estima que el número de iteraciones necesarias se puede calcular utilizando fórmulas específicas. - Se concluye que QUMMSA tiene una complejidad más baja en comparación con DHA, especialmente en bases de datos grandes.

## Complejidad del Algoritmo QUMMSA

El algoritmo QUMMSA, basado en el algoritmo Grover-Long, presenta ventajas significativas en términos de complejidad en comparación con DHA.

- La complejidad total se expresa como $R = \frac{\pi (2 + \sqrt{2} + c) \sqrt{N} + (log_2 N + c) log_2 N}{2(1 - \epsilon)}$.
- Se considera que $M_0 \approx \frac{1}{N}$ y se ejecuta aproximadamente $log_2 N$ veces para la preparación del estado inicial.
- La tasa de éxito del algoritmo QUMMSA es cercana al 100% y mejora con el aumento del tamaño de la base de datos.

## Comparación de Algoritmos Cuánticos

Se comparan dos algoritmos cuánticos bajo las mismas condiciones, mostrando que QUMMSA es más eficiente.

- Se establece ϵ=0.1 para el cálculo de complejidad.
- QUMMSA requiere preparar un menor número de estados iniciales en comparación con DHA, que requiere aproximadamente $log_2 N$ y $log_2^2 N$ respectivamente.
- A medida que aumenta el tamaño de la base de datos, QUMMSA muestra una ventaja creciente en complejidad.

## Conclusiones sobre el Algoritmo Cuántico

El algoritmo cuántico propuesto alivia los desafíos de manejar grandes volúmenes de datos.

- QUMMSA es una versión mejorada de DHA, con una probabilidad de éxito casi del 100%.
- Se presentan circuitos cuánticos generales y principios simplificados que reducen la complejidad de las puertas.
- El algoritmo puede integrarse como subrutina en otros algoritmos cuánticos que necesiten encontrar valores máximos o mínimos.

## Contribuciones de los Autores

Los autores contribuyeron de diversas maneras al desarrollo del algoritmo y la redacción del manuscrito.

- Yanhu Chen proporcionó la idea original y realizó simulaciones cuánticas.
- Shijie Wei, Jian Wu, Hongxiang Guo, Xiong Gao y Cen Wang hicieron comentarios constructivos y modificaron el manuscrito.

## Datos de Referencia y Fuentes

Se citan múltiples referencias que respaldan la investigación y el desarrollo del algoritmo cuántico.

- Se incluyen artículos relevantes sobre algoritmos cuánticos y su aplicación en la búsqueda y optimización.
- Las referencias abarcan desde 1985 hasta 2019, mostrando la evolución del campo.

## Parámetros del Procesador Cuántico

Se presentan parámetros específicos del procesador cuántico superconductores de IBM.

- Se detallan frecuencias, tiempos de relajación (T1 y T2), y errores de puertas cuánticas.
- Los errores de puertas de un solo qubit varían entre 0.77×10−3 y 6.36×10−3.

## Tamaño Mínimo de Muestra

Se muestra el tamaño mínimo de muestra necesario para diferentes niveles de confianza y errores aceptables.

- Para un error aceptable de 0.01, el tamaño mínimo de muestra varía de 1140 a 19741 según el nivel de confianza.
- A medida que el error aceptable aumenta, el tamaño mínimo de muestra disminuye significativamente.