from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


def diffuser(n_qubits: int) -> QuantumCircuit:
    """Create the Grover diffuser for n qubits."""
    qc = QuantumCircuit(n_qubits)

    qc.h(range(n_qubits))
    qc.x(range(n_qubits))

    qc.h(n_qubits - 1)
    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    qc.h(n_qubits - 1)

    qc.x(range(n_qubits))
    qc.h(range(n_qubits))

    return qc


def oracle_mark_101() -> QuantumCircuit:
    """Oracle that marks the state |101>."""
    qc = QuantumCircuit(3)

    # Convert |101> into |111>, apply a phase flip, then undo.
    qc.x(1)
    qc.h(2)
    qc.ccx(0, 1, 2)
    qc.h(2)
    qc.x(1)

    return qc


def grover_circuit_3_qubits() -> QuantumCircuit:
    qc = QuantumCircuit(3, 3)

    qc.h([0, 1, 2])
    qc.compose(oracle_mark_101(), inplace=True)
    qc.compose(diffuser(3), inplace=True)
    qc.measure([0, 1, 2], [0, 1, 2])

    return qc


def main() -> None:
    qc = grover_circuit_3_qubits()

    simulator = AerSimulator()
    pass_manager = generate_preset_pass_manager(backend=simulator, optimization_level=1)
    compiled = pass_manager.run(qc)

    result = simulator.run(compiled, shots=1024).result()
    counts = result.get_counts()

    print("Circuito de Grover para 3 qubits")
    print(qc.draw(output="text"))
    print("\nResultados:")
    print(counts)


if __name__ == "__main__":
    main()
