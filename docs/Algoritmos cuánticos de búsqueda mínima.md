Estos son algoritmos que consisten en obtener la posición $k$ del valor mínimo de una tabla de $N$ elementos. 
Basándose en el [[Algoritmo de Grover]], estos algoritmos realizan una iteración de Grover marcando valores mínimos, seleccionando uno aleatorio e iterando Grover, hasta hallar el mínimo.
## DHA (Durr & Hoyer Algorithm)
La versión más simple es la abordada por [[Durr, C., & Hoyer, P. (1996)|Durr y Hoyer]] (DHA). Consiste en converger al valor mínimo con alta probabiidad en una serie de pasos repetidos.
## KHA (Kang & Heo Algorithm)
La versión abordada por [[Kang, Y., and Heo, J. IEEE (2020)|Kang]], ofrece innovaciones con respecto a [[Durr, C., & Hoyer, P. (1996)|Durr]]. Entre ellas está la mejora de las iteraciones del algoritmo, explicadas matemáticamente en su paper. La aplicación del concepto de [[QRAM]] propuesto por Giovannetti, V., Lloyd, S., & Maccone, L. (2008). Y el comparador cuántico propuesto por Thomas, S. G. (2017).
## QUMMSA
El [[QUMMSA]] es una versión mejorada de DHA que permite también hallar valores máximos o mínimos, además se usa el Grover-Long para poder obtener un resultado más preciso.
## Referencias
- [[Durr, C., & Hoyer, P. (1996)]]
- [[Kang, Y., and Heo, J. IEEE (2020)]]
- [[Chen, Wei, Gao (2019)]]