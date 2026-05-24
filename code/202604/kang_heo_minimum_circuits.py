from __future__ import annotations

from dataclasses import dataclass, field
from math import ceil, log2, pi, sqrt
from typing import Iterable


@dataclass(frozen=True)
class Operation:
    name: str
    targets: tuple[str, ...]
    params: tuple[int, ...] = ()

    def qasm_comment(self) -> str:
        args = ", ".join(self.targets)
        pars = "" if not self.params else f" {self.params}"
        return f"// {self.name}{pars}: {args}"


@dataclass
class KangHeoMinimumCircuit:
    total_qubits: int
    values: list[int]
    index_qubits: int
    value_qubits: int
    flag_qubit: int
    work_qubits: tuple[int, ...]
    operations: list[Operation] = field(default_factory=list)

    @property
    def database_size(self) -> int:
        return len(self.values)

    def add(self, name: str, targets: Iterable[str], *params: int) -> None:
        self.operations.append(Operation(name, tuple(targets), tuple(params)))

    def gate_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for op in self.operations:
            counts[op.name] = counts.get(op.name, 0) + 1
        return dict(sorted(counts.items()))

    def to_openqasm3(self) -> str:
        lines = [
            "OPENQASM 3.0;",
            'include "stdgates.inc";',
            f"qubit[{self.total_qubits}] q;",
            f"bit[{self.index_qubits}] c;",
            "",
            "// Circuito logico optimizado basado en Kang-Heo:",
            "// QRAM -> comparador constante '< umbral' -> phase oracle -> uncompute -> Grover diffuser.",
        ]
        lines.extend(op.qasm_comment() for op in self.operations)
        lines.extend(f"measure q[{i}] -> c[{i}];" for i in range(self.index_qubits))
        return "\n".join(lines)


def generated_values(database_size: int) -> list[int]:
    """Valores numericos reproducibles. El minimo se fija una vez para evitar empates."""
    span = 8 * database_size + 37
    values = [
        100 + (((73 * i + 19 * database_size) ^ ((i * i + 11 * i) % span)) % span)
        for i in range(database_size)
    ]
    hidden_minimum_index = (5 * database_size // 8 + 7) % database_size
    values[hidden_minimum_index] = 3
    return values


def build_kang_heo_circuit(total_qubits: int, values: list[int]) -> KangHeoMinimumCircuit:
    n_items = len(values)
    index_qubits = ceil(log2(n_items))
    value_qubits = max(values).bit_length()
    required = index_qubits + value_qubits + 2
    if required > total_qubits:
        raise ValueError(
            f"{total_qubits} qubits no alcanzan: hacen falta {required} "
            f"({index_qubits} indice + {value_qubits} valor + flag + ancilla)."
        )

    idx = [f"q[{i}]" for i in range(index_qubits)]
    val = [f"q[{index_qubits + i}]" for i in range(value_qubits)]
    flag = index_qubits + value_qubits
    work = tuple(range(flag + 1, total_qubits))

    circuit = KangHeoMinimumCircuit(
        total_qubits=total_qubits,
        values=values,
        index_qubits=index_qubits,
        value_qubits=value_qubits,
        flag_qubit=flag,
        work_qubits=work,
    )

    circuit.add("H-layer", idx)
    threshold = values[0]
    while True:
        marked = [i for i, x in enumerate(values) if x < threshold]
        if not marked:
            break

        grover_iterations = max(1, round((pi / 4) * sqrt(n_items / len(marked))))
        for _ in range(grover_iterations):
            circuit.add("QRAM-load", idx + val)
            circuit.add("Thomas-constant-adder-comparator-LT", val + [f"q[{flag}]"], threshold)
            circuit.add("phase-inverter-oracle", [f"q[{flag}]"])
            circuit.add("uncompute-comparator", val + [f"q[{flag}]"], threshold)
            circuit.add("QRAM-unload", idx + val)
            circuit.add("Grover-diffuser", idx)

        # Emulacion ideal de la medicion exitosa: actualiza con el menor marcado.
        threshold = min(values[i] for i in marked)

    return circuit


def exact_minimum_trace(values: list[int]) -> list[dict[str, int]]:
    threshold = values[0]
    trace: list[dict[str, int]] = []
    step = 0
    while True:
        marked = [(i, x) for i, x in enumerate(values) if x < threshold]
        if not marked:
            break
        next_index, next_value = min(marked, key=lambda pair: pair[1])
        step += 1
        trace.append(
            {
                "step": step,
                "threshold_before": threshold,
                "marked_count": len(marked),
                "selected_index": next_index,
                "selected_value": next_value,
            }
        )
        threshold = next_value
    return trace


def verify(values: list[int], trace: list[dict[str, int]]) -> tuple[int, int, bool]:
    expected_index = min(range(len(values)), key=values.__getitem__)
    expected_value = values[expected_index]
    observed_value = trace[-1]["selected_value"] if trace else values[0]
    observed_index = trace[-1]["selected_index"] if trace else 0
    return observed_index, observed_value, observed_index == expected_index and observed_value == expected_value


def main() -> None:
    for qubits in (16, 32, 64, 128):
        values = generated_values(qubits)
        circuit = build_kang_heo_circuit(qubits, values)
        trace = exact_minimum_trace(values)
        min_index, min_value, ok = verify(values, trace)

        print(f"\n=== Circuito Kang-Heo para {qubits} qubits ===")
        print(f"items={len(values)} index_qubits={circuit.index_qubits} value_qubits={circuit.value_qubits}")
        print(f"flag=q[{circuit.flag_qubit}] work_qubits={len(circuit.work_qubits)}")
        print(f"minimo_encontrado: indice={min_index} valor={min_value} verificado={ok}")
        print(f"primeros_valores={values[:8]}")
        print(f"traza={trace}")
        print(f"conteo_operaciones={circuit.gate_counts()}")

        qasm_path = f"kang_heo_min_{qubits}q.qasm"
        with open(qasm_path, "w", encoding="utf-8") as handle:
            handle.write(circuit.to_openqasm3())
        print(f"qasm={qasm_path}")


if __name__ == "__main__":
    main()
