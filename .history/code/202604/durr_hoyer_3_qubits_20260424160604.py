from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


DATA = [7, 5, 4, 0, 7, 3, 2, 1]


def diffuser(n_qubits: int) -> QuantumCircuit:
    qc = QuantumCircuit(n_qubits)

    qc.h(range(n_qubits))
    qc.x(range(n_qubits))
    qc.h(n_qubits - 1)
    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    qc.h(n_qubits - 1)
    qc.x(range(n_qubits))
    qc.h(range(n_qubits))

    return qc


def oracle_mark_indices(marked_indices: list[int], n_qubits: int = 3) -> QuantumCircuit:
    """Marks selected basis states with a phase flip."""
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


def build_grover_iteration(marked_indices: list[int], n_qubits: int = 3) -> QuantumCircuit:
    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(range(n_qubits))
    qc.compose(oracle_mark_indices(marked_indices, n_qubits), inplace=True)
    qc.compose(diffuser(n_qubits), inplace=True)
    qc.measure(range(n_qubits), range(n_qubits))
    return qc


def simulate_counts(qc: QuantumCircuit, shots: int = 1024) -> dict:
    simulator = AerSimulator()
    result = simulator.run(qc, shots=shots).result()
    return result.get_counts()


def find_better_indices(data: list[int], threshold_index: int) -> list[int]:
    threshold_value = data[threshold_index]
    return [i for i, value in enumerate(data) if value < threshold_value]


def main() -> None:
    current_index = 0
    current_value = DATA[current_index]

    print("Algoritmo de Durr-Hoyer didactico para 8 datos (3 qubits)\n")
    print("Datos:")
    for i, value in enumerate(DATA):
        print(f"  indice {i:>1} ({i:03b}) -> {value}")

    print(f"\nCandidato inicial: indice {current_index} ({current_index:03b}) con valor {current_value}\n")

    round_number = 1
    while True:
        better_indices = find_better_indices(DATA, current_index)

        print(f"Ronda {round_number}")
        print(f"  Umbral actual: valor < {DATA[current_index]} (indice actual {current_index:03b})")
        print(f"  Estados marcados por el oraculo: {[format(i, '03b') for i in better_indices]}")

        if not better_indices:
            print("  No hay elementos menores. El candidato actual es el minimo.")
            break

        qc = build_grover_iteration(better_indices)
        counts = simulate_counts(qc)
        measured_state = max(counts, key=counts.get)
        measured_index = int(measured_state, 2)

        print(qc.draw(output="text"))
        print(f"  Resultados de la simulacion: {counts}")
        print(f"  Estado mas probable medido: {measured_state} -> valor {DATA[measured_index]}")

        if DATA[measured_index] < DATA[current_index]:
            current_index = measured_index
            current_value = DATA[current_index]
            print(f"  Se actualiza el candidato minimo a {current_index:03b} con valor {current_value}\n")
        else:
            print("  La medicion no mejoro el candidato. En la version completa se repiten iteraciones.\n")
            break

        round_number += 1

    print(f"Minimo encontrado: indice {current_index} ({current_index:03b}), valor {current_value}")


if __name__ == "__main__":
    main()
