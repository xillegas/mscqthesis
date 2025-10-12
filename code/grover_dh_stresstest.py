"""
Stress test de Grover (umbral) + Dürr–Høyer (mínimo) con N grande.
- Usa iteraciones óptimas de Grover y bucle robusto (múltiples intentos + BBHT).
- Mide la tasa de acierto del argmin cuántico vs. clásico.
Requiere: qiskit, qiskit-aer
"""

from math import ceil, log2, pi, sqrt, asin, floor, log2 as lg2
from collections import Counter
import random
from typing import List, Tuple

from qiskit import QuantumCircuit, transpile
try:
    from qiskit_aer import Aer
except Exception:
    from qiskit import Aer

# ---------- Utilidades de Grover ----------
def num_qubits_for_n(n_items: int) -> int:
    return max(1, ceil(log2(max(1, n_items))))

def index_to_bits(i: int, n_qubits: int):
    return [int(b) for b in format(i, f"0{n_qubits}b")]

def phase_oracle_gate(n_index: int, marked_indices):
    qc = QuantumCircuit(n_index + 1, name="Oracle")
    for idx in marked_indices:
        bits = index_to_bits(idx, n_index)
        for qb, bit in enumerate(bits):
            if bit == 0:
                qc.x(qb)
        qc.mcx(list(range(n_index)), n_index)
        for qb, bit in enumerate(bits):
            if bit == 0:
                qc.x(qb)
    return qc.to_gate()

def diffuser_gate(n_index: int):
    qc = QuantumCircuit(n_index, name="Diffuser")
    qc.h(range(n_index))
    qc.x(range(n_index))
    if n_index == 1:
        qc.z(0)
    else:
        qc.h(n_index - 1)
        qc.mcx(list(range(n_index - 1)), n_index - 1)
        qc.h(n_index - 1)
    qc.x(range(n_index))
    qc.h(range(n_index))
    return qc.to_gate()

def optimal_grover_iterations(N: int, M: int) -> int:
    if M <= 0 or M > N:
        return 1
    theta = asin(sqrt(M / N))
    k = floor(pi / (4 * theta) - 0.5)
    return max(1, k)

def run_grover_threshold(marked_indices, n_items: int, iterations: int = 1, shots: int = 4096):
    n_index = num_qubits_for_n(n_items)
    qc = QuantumCircuit(n_index + 1, n_index, name="GroverThreshold")
    qc.h(range(n_index))
    qc.x(n_index)
    qc.h(n_index)
    oracle = phase_oracle_gate(n_index, marked_indices)
    diffuser = diffuser_gate(n_index)
    for _ in range(iterations):
        qc.append(oracle, list(range(n_index + 1)))
        qc.append(diffuser, list(range(n_index)))
    qc.measure(list(range(n_index)), list(range(n_index)))
    backend = Aer.get_backend("qasm_simulator")
    tqc = transpile(qc, backend)
    result = backend.run(tqc, shots=shots).result()
    counts = result.get_counts()
    return counts

# ---------- Dürr–Høyer robusto ----------
def dh_min_index(values: List[float], shots=4096, max_rounds=8, tries_per_round=3, rng: random.Random=None) -> Tuple[int, List[Tuple[int, float]]]:
    N = len(values)
    R = rng or random
    current = R.randrange(N)
    current_val = values[current]
    history = [(current, current_val)]
    for _ in range(max_rounds):
        marked = [j for j, v in enumerate(values) if v < current_val]
        if not marked:
            break
        M = len(marked)
        improved = False
        for _ in range(tries_per_round):
            k = optimal_grover_iterations(N, M)
            counts = run_grover_threshold(marked, N, iterations=k, shots=shots)
            candidates = [(int(bs, 2), c) for bs, c in counts.items()]
            candidates.sort(key=lambda x: x[1], reverse=True)
            cand_idx = candidates[0][0]
            cand_val = values[cand_idx]
            history.append((cand_idx, cand_val))
            if cand_val < current_val:
                current, current_val = cand_idx, cand_val
                improved = True
                break
        if not improved:
            k_max = optimal_grover_iterations(N, max(1, M))
            k_rand = R.randint(0, max(1, k_max))
            counts = run_grover_threshold(marked, N, iterations=max(1, k_rand), shots=shots)
            candidates = [(int(bs, 2), c) for bs, c in counts.items()]
            candidates.sort(key=lambda x: x[1], reverse=True)
            cand_idx = candidates[0][0]
            cand_val = values[cand_idx]
            history.append((cand_idx, cand_val))
            if cand_val < current_val:
                current, current_val = cand_idx, cand_val
            else:
                break
    return current, history

# ---------- Generador de datasets ----------
def generate_values_with_unique_min(N: int, rng: random.Random) -> Tuple[List[float], int]:
    vals = [rng.random() for _ in range(N)]
    min_idx = rng.randrange(N)
    vals[min_idx] = 0.0  # mínimo claro
    # Asegura valores distintos (pequeña perturbación)
    eps = 1e-6
    for i in range(N):
        vals[i] += i * eps
    return vals, min_idx

# ---------- Experimento de estrés ----------
def run_trials_over_N(
    Ns=(8, 16, 32, 64, 128),
    trials=20,
    shots=4096,
    base_rounds=6,
    tries_per_round=3,
    seed=0
):
    rng = random.Random(seed)
    results = []
    for N in Ns:
        max_rounds = max(base_rounds, int(2 + lg2(N)))
        success = 0
        for _ in range(trials):
            values, true_min = generate_values_with_unique_min(N, rng)
            found, _ = dh_min_index(values, shots=shots, max_rounds=max_rounds,
                                    tries_per_round=tries_per_round, rng=rng)
            if found == true_min:
                success += 1
        rate = success / trials
        results.append((N, rate))
        print(f"N={N:>3} | tasa de acierto={rate:.2f} ({success}/{trials}) | shots={shots}, rondas={max_rounds}, intentos/ronda={tries_per_round}")
    return results

if __name__ == "__main__":
    print("Stress test Dürr–Høyer (mínimo) con N variable")
    Ns = (8, 16, 32, 64, 128)
    trials = 20
    shots = 4096
    tries_per_round = 3
    base_rounds = 6
    seed = 0

    run_trials_over_N(Ns=Ns, trials=trials, shots=shots,
                      base_rounds=base_rounds, tries_per_round=tries_per_round, seed=seed)