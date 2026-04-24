import math
from collections import Counter

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit_aer import AerSimulator


PAPER_EXAMPLES = {
    "2q_2targets": ["00", "01"],
    "5q_2targets": ["00101", "10111"],
    "5q_4targets": ["01011", "10001", "10110", "11101"],
    "6q_3targets": ["100010", "110011", "111010"],
}


def exact_long_phase(n_qubits: int, n_targets: int) -> tuple[float, int]:
    """
    Exact-search phase and iteration count used in the Zhong et al. paper.

    Inference from the paper's extension of Long's exact search:
    beta = asin(sqrt(M / N))
    J = floor((pi/2 - beta) / (2*beta))
    phi = 2 * asin(sin(pi / (4*J + 6)) / sin(beta))
    iterations = J + 1
    """
    search_space_size = 2**n_qubits
    beta = math.asin(math.sqrt(n_targets / search_space_size))
    j_value = math.floor((math.pi / 2 - beta) / (2 * beta))
    phi = 2 * math.asin(math.sin(math.pi / (4 * j_value + 6)) / math.sin(beta))
    return phi, j_value + 1


def optimized_diffuser_gate(n_qubits: int, phi: float) -> UnitaryGate:
    """
    Diffuser as a compact unitary.

    This matches the optimized diffuser operator described in the paper after
    merging H/X and X/H pairs into more efficient rotation blocks.
    """
    size = 2**n_qubits
    uniform = np.ones((size, 1), dtype=complex) / math.sqrt(size)
    projector = uniform @ uniform.conj().T
    diffuser = np.eye(size, dtype=complex) - (1 - np.exp(1j * phi)) * projector
    return UnitaryGate(diffuser, label="D_opt")


def _apply_single_target_oracle(qc: QuantumCircuit, target: str, phi: float) -> None:
    """Apply one oracle block for a single marked computational basis state."""
    n_qubits = len(target)

    for qubit, bit in enumerate(target):
        if bit == "0":
            qc.x(qubit)

    if n_qubits == 1:
        qc.p(phi, 0)
    else:
        qc.mcp(phi, list(range(n_qubits - 1)), n_qubits - 1)

    for qubit, bit in enumerate(target):
        if bit == "0":
            qc.x(qubit)


def multi_target_oracle(targets: list[str], phi: float) -> QuantumCircuit:
    """
    Oracle built as serial single-target oracle blocks, following the paper.
    """
    n_qubits = len(targets[0])
    qc = QuantumCircuit(n_qubits, name="U_w")

    for target in targets:
        _apply_single_target_oracle(qc, target, phi)

    return qc


def build_exact_multi_target_circuit(targets: list[str]) -> tuple[QuantumCircuit, float, int]:
    """
    Build the exact multi-target search circuit from Zhong et al.

    Steps:
    1. Prepare uniform superposition with H^n.
    2. Repeat the exact-search iterate:
       - serial multi-target oracle blocks
       - optimized diffuser
    3. Measure.
    """
    n_qubits = len(targets[0])
    phi, iterations = exact_long_phase(n_qubits, len(targets))
    oracle = multi_target_oracle(targets, phi)
    diffuser = optimized_diffuser_gate(n_qubits, phi)

    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(range(n_qubits))

    for _ in range(iterations):
        qc.compose(oracle, inplace=True)
        qc.append(diffuser, range(n_qubits))

    qc.measure(range(n_qubits), range(n_qubits))
    return qc, phi, iterations


def simulate_counts(qc: QuantumCircuit, shots: int = 2000) -> Counter:
    simulator = AerSimulator()
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts()
    return Counter(counts)


def run_paper_example(example_name: str = "2q_2targets") -> None:
    targets = PAPER_EXAMPLES[example_name]
    qc, phi, iterations = build_exact_multi_target_circuit(targets)
    counts = simulate_counts(qc)

    print(f"Example: {example_name}")
    print(f"Targets: {targets}")
    print(f"Phase phi: {phi:.6f} rad")
    print(f"Iterations: {iterations}")
    print("\nCircuit:")
    print(qc.draw(output="text"))
    print("\nCounts:")
    print(dict(counts))


if __name__ == "__main__":
    run_paper_example("2q_2targets")
