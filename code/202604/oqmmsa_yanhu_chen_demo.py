from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


# Demo dataset with 4 items so we can show the full circuit on 2 index qubits.
DATA = [7, 5, 0, 3]


def diffuser(n_qubits: int) -> QuantumCircuit:
    """Standard Grover diffuser."""
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))
    qc.x(range(n_qubits))
    qc.h(n_qubits - 1)
    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    qc.h(n_qubits - 1)
    qc.x(range(n_qubits))
    qc.h(range(n_qubits))
    return qc


def phase_oracle_for_indices(marked_indices: list[int], n_qubits: int) -> QuantumCircuit:
    """
    Phase oracle that flips the sign of the marked basis states.

    For this small demo we build the oracle explicitly from the list of indices
    that satisfy the paper's comparison condition f(x, y) = 1, i.e. data[x] < data[y].
    """
    qc = QuantumCircuit(n_qubits)

    for idx in marked_indices:
        bits = format(idx, f"0{n_qubits}b")

        for qubit, bit in enumerate(bits):
            if bit == "0":
                qc.x(qubit)

        qc.h(n_qubits - 1)
        qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
        qc.h(n_qubits - 1)

        for qubit, bit in enumerate(bits):
            if bit == "0":
                qc.x(qubit)

    return qc


def indices_less_than_threshold(data: list[int], threshold_index: int) -> list[int]:
    threshold_value = data[threshold_index]
    return [i for i, value in enumerate(data) if value < threshold_value]


def build_oqmmsa_iteration(data: list[int], threshold_index: int) -> QuantumCircuit:
    """
    Build one search circuit used inside the optimized maximum/minimum procedure.

    This is the circuit-level core of the paper:
    1. prepare a superposition over candidate indices,
    2. mark states with value lower than the current threshold,
    3. amplify them with Grover's diffuser,
    4. measure the candidate index.

    For N=4 and one marked state, one Grover iteration is exact.
    """
    n_qubits = 2
    marked_indices = indices_less_than_threshold(data, threshold_index)

    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(range(n_qubits))
    qc.compose(phase_oracle_for_indices(marked_indices, n_qubits), inplace=True)
    qc.compose(diffuser(n_qubits), inplace=True)
    qc.measure(range(n_qubits), range(n_qubits))
    return qc


def simulate(circuit: QuantumCircuit, shots: int = 1024) -> dict:
    simulator = AerSimulator()
    result = simulator.run(circuit, shots=shots).result()
    return result.get_counts()


def run_demo() -> None:
    print("OQMMSA inspired by Chen et al. (arXiv:1908.07943)")
    print("Dataset usado en esta demo:")
    for i, value in enumerate(DATA):
        print(f"  indice {i} ({i:02b}) -> {value}")

    current_index = 0
    print(f"\nCandidato inicial y = {current_index:02b}, valor = {DATA[current_index]}")

    round_number = 1
    while True:
        marked = indices_less_than_threshold(DATA, current_index)
        print(f"\nRonda {round_number}")
        print(f"Estados que cumplen data[x] < data[y]: {[format(i, '02b') for i in marked]}")

        if not marked:
            print("No existen indices mejores. Se encontro el minimo.")
            break

        circuit = build_oqmmsa_iteration(DATA, current_index)
        counts = simulate(circuit)
        winner_state = max(counts, key=counts.get)
        winner_index = int(winner_state, 2)

        print(circuit.draw(output='text'))
        print(f"Resultados: {counts}")
        print(f"Medicion dominante: {winner_state} -> valor {DATA[winner_index]}")

        if DATA[winner_index] < DATA[current_index]:
            current_index = winner_index
            print(f"Se actualiza el candidato a {current_index:02b}, valor = {DATA[current_index]}")
        else:
            print("La medicion no mejoro el candidato. En una implementacion completa se reintenta.")
            break

        round_number += 1

    print(f"\nMinimo final: indice {current_index:02b}, valor {DATA[current_index]}")


if __name__ == "__main__":
    run_demo()
