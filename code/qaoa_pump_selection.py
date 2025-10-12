"""
Selección de una bomba con QAOA (QUBO).
Requiere: qiskit, qiskit-aer, qiskit-optimization
"""

from typing import List, Dict
import numpy as np

# Compatibilidad con versiones
try:
    from qiskit_optimization import QuadraticProgram
    from qiskit_optimization.algorithms import MinimumEigenOptimizer
except Exception:
    from qiskit.optimization import QuadraticProgram
    from qiskit.optimization.algorithms import MinimumEigenOptimizer

from qiskit.algorithms.minimum_eigensolvers import QAOA
from qiskit_aer.primitives import Estimator

def build_qubo(costs: List[float], P: float) -> QuadraticProgram:
    """
    Minimiza: sum_i (cost_i - P) x_i + 2P sum_{i<j} x_i x_j
    con x_i binario y 'una sola bomba': (sum x_i - 1)^2
    """
    N = len(costs)
    qp = QuadraticProgram()
    for i in range(N):
        qp.binary_var(name=f"x_{i}")
    lin = {f"x_{i}": (costs[i] - P) for i in range(N)}
    quad = {}
    for i in range(N):
        for j in range(i + 1, N):
            quad[(f"x_{i}", f"x_{j}")] = 2.0 * P
    qp.minimize(linear=lin, quadratic=quad)
    return qp

def choose_pump_qaoa(
    pump_ids: List[str],
    data: Dict[str, List[float]],
    w=(1.0, 1.0, 1.0),
    tau_curr=0.8, tau_vib=0.8,
    H=8.0, P=10.0,
    reps=1, seed=42
) -> str:
    """
    Devuelve el id de la bomba seleccionada por QAOA.

    costs[i] = w1*tuse_i + w2*curr_i + w3*vib_i + H*over_i
    over_i = 1 si (curr_i >= tau_curr) o (vib_i >= tau_vib), si no 0.
    """
    tuse = data["time_of_use"]
    curr = data["max_current"]
    vib  = data["vibration"]
    assert len(tuse) == len(curr) == len(vib) == len(pump_ids)

    w1, w2, w3 = w
    costs = []
    for i in range(len(pump_ids)):
        over = 1.0 if (curr[i] >= tau_curr or vib[i] >= tau_vib) else 0.0
        costs.append(w1 * tuse[i] + w2 * curr[i] + w3 * vib[i] + H * over)

    qp = build_qubo(costs, P=P)

    qaoa = QAOA(Estimator(), reps=reps, seed=seed)
    opt = MinimumEigenOptimizer(qaoa)
    result = opt.solve(qp)
    x = [int(result.x[i]) for i in range(len(pump_ids))]
    chosen = [i for i, xi in enumerate(x) if xi == 1]

    if len(chosen) != 1:
        i_min = int(np.argmin(costs))
        return pump_ids[i_min]
    return pump_ids[chosen[0]]

if __name__ == "__main__":
    pump_ids = [f"P{i:03d}" for i in range(8)]
    data = {
        "time_of_use":  [0.10, 0.52, 0.33, 0.01, 0.72, 0.64, 0.28, 0.41],
        "max_current":  [0.21, 0.18, 0.11, 0.09, 0.85, 0.67, 0.44, 0.32],
        "vibration":    [0.03, 0.14, 0.59, 0.20, 0.22, 0.47, 0.18, 0.35],
    }
    chosen = choose_pump_qaoa(pump_ids, data, w=(1.0, 0.5, 0.5),
                              tau_curr=0.8, tau_vib=0.8, H=8.0, P=10.0, reps=1)
    print("Bomba seleccionada (QAOA):", chosen)