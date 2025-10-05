"""
Minimum/Maximum finding workflows (per-variable) aligned with 'Assets Management for Pumps'.

- Normalize real-valued inputs in [0,1] to b-bit fixed-point.
- Provide scaffolds for:
  * Argmin (Dürr–Høyer minimum finding)
  * Argmax (invert comparator)
  * Threshold detection with Grover

This is a scaffold to organize data and outline the quantum routines.
Next step: implement comparator circuits and oracles using Qiskit.
"""

from typing import List, Dict


def normalize_values(values: List[float], bits: int = 10) -> List[int]:
    """
    Map floats in [0,1] to fixed-point integers in [0, 2^bits - 1].
    """
    assert all(0.0 <= v <= 1.0 for v in values), "All values must be in [0,1]."
    M = (1 << bits) - 1
    return [max(0, min(M, int(round(v * M)))) for v in values]


def prepare_dataset(
    pump_ids: List[str],
    data: Dict[str, List[float]],
    bits: int = 10,
    threshold: float = 0.8,
) -> Dict[str, Dict]:
    """
    Prepares fixed-point data and threshold per variable.

    Returns a dict:
      var -> {
        "pump_ids": [...],
        "fixed_point_values": [...],  # ints in [0, 2^bits-1]
        "bits": bits,
        "threshold_float": threshold,
        "threshold_fp": int,
        "argmin_index": None,
        "argmax_index": None,
        "over_threshold_indices": []
      }
    """
    assert all(len(pump_ids) == len(vals) for vals in data.values()), "All variable lists must match pump_ids length."
    M = (1 << bits) - 1
    tau_fp = int(round(threshold * M))
    prep: Dict[str, Dict] = {}
    for var, vals in data.items():
        fp_vals = normalize_values(vals, bits)
        prep[var] = {
            "pump_ids": pump_ids[:],
            "fixed_point_values": fp_vals,
            "bits": bits,
            "threshold_float": threshold,
            "threshold_fp": tau_fp,
            "argmin_index": None,
            "argmax_index": None,
            "over_threshold_indices": [],
        }
    return prep


# -------- Placeholders for quantum routines (to be implemented with Qiskit) --------

def durr_hoyer_argmin_index(fp_values: List[int], bits: int) -> int:
    """
    Placeholder for Dürr–Høyer minimum finding.
    Returns the index of the minimum value in fp_values.

    Quantum plan:
      1) Pick random index i as current best.
      2) Use Grover with oracle marking j if v_j < v_i (comparator circuit).
      3) If a better j is found, set i <- j and repeat until convergence.
    """
    # Classical fallback for now:
    return min(range(len(fp_values)), key=lambda i: fp_values[i])


def durr_hoyer_argmax_index(fp_values: List[int], bits: int) -> int:
    """
    Argmax via inverted comparator (or negate values).
    """
    return max(range(len(fp_values)), key=lambda i: fp_values[i])


def grover_threshold_indices(fp_values: List[int], tau_fp: int, bits: int) -> List[int]:
    """
    Placeholder for Grover threshold search: find all indices with v_i >= tau_fp.

    Quantum plan:
      - Oracle marks indices with v_i >= tau_fp.
      - When number of marked items M is unknown, use BBHT strategy
        (randomized number of Grover iterations per round) to discover items.
    """
    # Classical fallback for now:
    return [i for i, v in enumerate(fp_values) if v >= tau_fp]


# -------- High-level report API --------

def report_per_variable(
    pump_ids: List[str],
    data: Dict[str, List[float]],
    bits: int = 10,
    threshold: float = 0.8,
) -> Dict[str, Dict]:
    """
    Computes argmin, argmax, and threshold sets per variable.
    For now, uses classical fallbacks; swap in quantum routines as they are implemented.
    """
    prep = prepare_dataset(pump_ids, data, bits=bits, threshold=threshold)
    for var, info in prep.items():
        vals = info["fixed_point_values"]
        tau = info["threshold_fp"]
        info["argmin_index"] = durr_hoyer_argmin_index(vals, bits)
        info["argmax_index"] = durr_hoyer_argmax_index(vals, bits)
        info["over_threshold_indices"] = grover_threshold_indices(vals, tau, bits)
    return prep


def pretty_print_report(report: Dict[str, Dict]) -> str:
    lines = []
    for var, info in report.items():
        pid = info["pump_ids"]
        amin = info["argmin_index"]
        amax = info["argmax_index"]
        thr = info["over_threshold_indices"]
        lines.append(f"[{var}]")
        lines.append(f"  healthiest (argmin): {pid[amin]} (index {amin})")
        lines.append(f"  worst (argmax):     {pid[amax]} (index {amax})")
        if thr:
            thr_ids = [pid[i] for i in thr]
            lines.append(f"  over-threshold (≥ {info['threshold_float']:.2f}): {thr_ids}")
        else:
            lines.append(f"  over-threshold (≥ {info['threshold_float']:.2f}): none")
    return "\n".join(lines)


if __name__ == "__main__":
    # Example with synthetic data
    pump_ids = [f"P{i:03d}" for i in range(16)]
    data = {
        "time_of_use":  [0.10, 0.52, 0.33, 0.01, 0.72, 0.64, 0.28, 0.41, 0.55, 0.47, 0.12, 0.90, 0.17, 0.24, 0.68, 0.36],
        "max_current":  [0.21, 0.18, 0.11, 0.09, 0.85, 0.67, 0.44, 0.32, 0.29, 0.51, 0.77, 0.61, 0.39, 0.06, 0.27, 0.73],
        "vibration":    [0.03, 0.14, 0.59, 0.20, 0.22, 0.47, 0.18, 0.35, 0.90, 0.26, 0.41, 0.53, 0.08, 0.15, 0.62, 0.30],
    }
    report = report_per_variable(pump_ids, data, bits=10, threshold=0.8)
    print(pretty_print_report(report))
