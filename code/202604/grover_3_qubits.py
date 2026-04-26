# Revisar esto con sumo detalle (21-abr-2026)

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


def diffuser(n_qubits: int) -> QuantumCircuit:
    """Create the Grover diffuser for n qubits.

    NOTA: El difusor realiza la inversion sobre la media de amplitudes.
    Despues de que el oraculo invierte la fase del estado objetivo,
    esta etapa amplifica su probabilidad y reduce la de los demas.

    Este circuito implementa el operador D = 2|s><s| - I de forma
    unitaria usando:
    - H para cambiar entre base computacional y base de superposicion,
    - X para convertir la reflexion alrededor de |0...0> en una
        reflexion equivalente alrededor de |1...1>,
    - H + MCX + H para aplicar un cambio de fase selectivo, ***
        y luego deshacer la transformacion.
    """
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
    """Oracle that marks the state |101>.
    NOTA: Este oráculo es específico para marcar el estado |101> en un sistema de 3 qubits. 
    Si se desea marcar otro estado, se deben ajustar los operadores.
    """
    qc = QuantumCircuit(3)

    # Convert |101> into |111>, apply a phase flip, then undo.
    qc.x(1)
    qc.h(2)
    qc.ccx(0, 1, 2)
    qc.h(2)
    qc.x(1)

    return qc


def grover_circuit_3_qubits() -> QuantumCircuit:
    """
    NOTA: Se define el circuito cuántico en esta etapa.
    """
    qc = QuantumCircuit(3, 3)

    # Etapa 1: inicializacion en superposicion
    qc.h([0, 1, 2])
    qc.barrier()

    # Etapa 2: oraculo
    qc.compose(oracle_mark_101(), inplace=True)
    qc.barrier()

    # Etapa 3: difusor
    qc.compose(diffuser(3), inplace=True)
    qc.barrier()

    # Etapa 4: medicion
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
