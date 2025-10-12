# Selección/rotación de bombas mediante QUBO (para QAOA)

Objetivo: elegir la bomba (o conjunto mínimo) a operar en el próximo intervalo minimizando desgaste y riesgo, y cumpliendo restricciones.

Variables:
- x_i ∈ {0,1} para i=1..N: x_i = 1 si selecciono la bomba i para operar ahora (caso simple: una sola bomba).

Datos (normalizados en [0,1], menor = más sano):
- tuse_i: tiempo de uso normalizado
- curr_i: corriente máxima relativa
- vib_i: vibración relativa

Umbrales:
- τ_curr, τ_vib (por ejemplo 0.8) para indicar riesgo alto.

Función de coste (lineal por bomba):
- cost_i = w1·tuse_i + w2·curr_i + w3·vib_i + H·over_i
  donde over_i = 1 si (curr_i ≥ τ_curr) o (vib_i ≥ τ_vib), 0 en caso contrario.
  H es una penalización alta (por ejemplo, H = 5–10) para evitar bombas en riesgo.

Restricción “una sola bomba”: 
- (∑_i x_i − 1)^2 = 0
- En QUBO se agrega como penalización: P·(∑_i x_i − 1)^2, con P ≫ w1,w2,w3 (por ejemplo P = 10).

QUBO resultante:
- Minimizar: ∑_i (cost_i − P)·x_i + 2P·∑_{i<j} x_i x_j + constante
- Puedes ajustar w1, w2, w3 para priorizar desgaste vs riesgo.

Extensiones:
- Seleccionar k bombas: usa (∑_i x_i − k)^2
- Incluir caudal: si cada bomba i aporta q_i, penaliza |∑_i q_i x_i − Q_requerido|
- Evitar selección de bombas “sobre-umbrales” con una penalización H grande o directamente prohibiéndolas (fijando x_i=0 si over_i=1).