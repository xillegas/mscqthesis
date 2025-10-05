# _Gestión de recursos mediante algoritmos cuánticos_

Resumen del nuevo modelo de tesis de maestría.
<small>Alfredo Villegas -
octubre 2024</small>

---
## Introducción
En esta presentación, mostraremos un breve enfoque del Assets Management y cómo puede utilizarse para determinar la salud y uso de equipos tales como bombas de hidrocarburos en una estación de llenado. Así como posibles algoritmos cuánticos que pueden contribuir con la gestión de recursos del sistema.

---
# Assets Management

---
Consiste en la gestión de recursos o activos en una organización basándose en valores o variables del sistema que sirvan como indicadores de uso, desgaste o riesgo, que permitan gestionar de forma óptima dichos recursos. 

---
En el presente trabajo, se busca gestionar el uso de bombas de hidrocarburos de una estación de carga a fin de determinar la salud de múltiples bombas a nivel regional. 
El propósito es disminuir la carga de trabajo del sistema de control distribuído de la estación de carga y delegar el manejo de estos datos a un sistema cuántico que, con ayuda de uno o varios algoritmos cuánticos híbridos, permita generar un reporte de los datos de salud de las bombas a nivel nacional.

---
# Variables a considerar

---
Dichas variables son relaciones entre el valor actual y su valor máximo permitido.

---
## Tiempo de uso
El tiempo de uso es uno de los indicadores más relevantes, ya que se pretende que las bombas cumplan con un tiempo de uso considerable para realizar un **mantenimiento preventivo** de las mismas.


---
## Intensidad de corriente máxima permitida
En función del caudal o por restricciones hidráulicas en el sistema, se puede ver afectada la intensidad de corriente (amperaje) de la bomba, esta no debe superar un valor máximo ya que deriva en un desgaste mayor.

---
## Vibración 
Implica la vibración radial y axial máxima permitida, se detecta con unos proximitores magnéticos.

---
La información de estas variables debe estar normalizada, por lo tanto, sus valores van entre 0 y 1. Si los valores son cercanos a cero, eso indica un equipo sano y si los valores son cercanos a 1 o mayores que 1 significa que el equipo está en condiciones alarmantes de operación. 

Además, las variables no se agrupan en aras de obtener un único valor de salud del sistema, ya que cada variable determina un valor o característica única, y además no se debe perder la información del sistema.

---
*⚠️ Importante*

El reporte final entregado por el algoritmo, define el estado de salud de los valores de las bombas por separado, de forma que el gerente de mantenimiento pueda determinar cuál bomba enviar a mantenimiento.

---
## Soluciones
A continuación algunos algoritmos cuánticos revisados que pueden ser implementados para dar solución al problema.

---

![[Algoritmo cuántico de búsqueda mínima]]

---

El paper de **Durr & Hoyer (1996)** se resume en una versión que usa el algoritmo cuántico de búsqueda exponencial de _M. Boyer, G. Brassard, P. Høyer et. al._ como una subrutina para hallar el valor mínimo con una probabilidad de al menos _1/2_ con un tiempo de ejecución de $O(\sqrt{N})$.

---
### Observaciones *(Durr & Hoyer)*
- La versión simplificada considera que todos los $N$ elementos son distintos.
- No ordena, sino que encuentra el mínimo valor.
- Puede servir para hallar la bomba con el menor valor de uno de los parámetros, sean: tiempo de uso, intensidad máxima, o vibración.

---

El trabajo de **Kang & Heo (2020)** aborda el problema de una forma más compleja. Propone tres cosas para modificar el algoritmo cuántico de búsqueda mínima e implementarlo en un espacio de 5-qubit.
- a) Modificar el número total esperado de iteraciones.
- b) Aplicar el concepto de QRAM.
- c) Comparar datos usando un comparador cuántico.

Las sugerencias de esta investigación reducen el numero esperado de iteraciones mientras se mantiene una alta precisión, aunque el tiempo extra del QRAM y del comparador cuántico fueron de $O(log_2 N)$ cada uno.

---

![[Algoritmo cuántico de ordenamiento]]

---
### Observaciones
- Un algoritmo de ordenamiento podría ordenar las bombas en función de su salud.
- Sin embargo hay que evaluar la complejidad de este algoritmo para un número grande de elementos (bombas).

---
cristiam fonlugem 2014
Benjamin barán 2016
baran y villagra 2017: dos horaculos h_1 y h_2
linux strom 2024

---


---
-----------------------------------
