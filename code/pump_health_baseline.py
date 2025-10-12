from typing import List, Dict, Tuple
import csv

def load_csv(path: str) -> Tuple[List[str], Dict[str, List[float]]]:
    pump_ids, tuse, curr, vib = [], [], [], []
    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pump_ids.append(row["pump_id"])
            tuse.append(float(row["time_of_use_norm"]))
            curr.append(float(row["current_norm"]))
            vib.append(float(row["vibration_norm"]))
    return pump_ids, {"time_of_use": tuse, "max_current": curr, "vibration": vib}

def per_variable_report(
    pump_ids: List[str],
    data: Dict[str, List[float]],
    threshold: float = 0.8
) -> str:
    lines = []
    for var, vals in data.items():
        amin = min(range(len(vals)), key=lambda i: vals[i])
        amax = max(range(len(vals)), key=lambda i: vals[i])
        over = [i for i, v in enumerate(vals) if v >= threshold]
        lines.append(f"[{var}]")
        lines.append(f"  más sana (argmin): {pump_ids[amin]} (idx {amin}) valor={vals[amin]:.3f}")
        lines.append(f"  peor (argmax):     {pump_ids[amax]} (idx {amax}) valor={vals[amax]:.3f}")
        if over:
            ids = [pump_ids[i] for i in over]
            lines.append(f"  sobre umbral (≥ {threshold:.2f}): {ids}")
        else:
            lines.append(f"  sobre umbral (≥ {threshold:.2f}): ninguna")
    return "\n".join(lines)

if __name__ == "__main__":
    # Ejemplo con datos sintéticos
    pump_ids = [f"P{i:03d}" for i in range(8)]
    data = {
        "time_of_use":  [0.10, 0.52, 0.33, 0.01, 0.72, 0.64, 0.28, 0.41],
        "max_current":  [0.21, 0.18, 0.11, 0.09, 0.85, 0.67, 0.44, 0.32],
        "vibration":    [0.03, 0.14, 0.59, 0.20, 0.22, 0.47, 0.18, 0.35],
    }
    print(per_variable_report(pump_ids, data, threshold=0.8))