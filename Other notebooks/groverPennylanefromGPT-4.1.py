import pennylane as qml
import numpy as np

n_qubits = 5
qubits = list(range(n_qubits))
dev = qml.device("default.qubit", wires=qubits)

def oracle():
    # Marca el estado |11111>
    qml.Hadamard(wires=qubits[-1])
    qml.MultiControlledX(control_wires=qubits[:-1], wires=qubits[-1])
    qml.Hadamard(wires=qubits[-1])

def diffuser():
    for i in range(n_qubits):
        qml.Hadamard(wires=i)
        qml.PauliX(wires=i)
    qml.Hadamard(wires=n_qubits-1)
    qml.MultiControlledX(control_wires=qubits[:-1], wires=qubits[-1])
    qml.Hadamard(wires=n_qubits-1)
    for i in range(n_qubits):
        qml.PauliX(wires=i)
        qml.Hadamard(wires=i)

@qml.qnode(dev)
def grover_circuit():
    # Superposición uniforme
    for i in range(n_qubits):
        qml.Hadamard(wires=i)
    iterations = int(np.floor(np.pi/4 * np.sqrt(2**n_qubits)))
    for _ in range(iterations):
        oracle()
        diffuser()
    return qml.probs(wires=qubits)

probs = grover_circuit()
print("Probabilidades:", probs)
print("Estado más probable:", np.argmax(probs))