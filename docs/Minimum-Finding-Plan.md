# Minimum/Maximum Finding Plan (Per-Variable Health)

This plan implements the document “Assets Management for Pumps” where variables are normalized to [0, 1] and lower values mean healthier equipment. We compute argmin/argmax and threshold sets separately for each variable (time of use, maximum current, vibration), without aggregating into a single health score.

## Objectives
- Argmin per variable: find the healthiest pump (minimum value).
- Argmax per variable: find the worst pump (maximum value) for maintenance.
- Threshold set per variable: identify pumps with value ≥ τ (e.g., τ = 0.8) that need attention.

## Data model
- Input: a CSV/JSON with columns: `pump_id`, `time_of_use_norm`, `current_norm`, `vibration_norm`.
- Normalization: each variable is in [0, 1] where 0 ≈ healthy and 1 ≈ risky.
- Fixed-point for quantum comparisons: use b bits (e.g., b = 10) to map [0,1] → {0, …, 2^b − 1}.

## Algorithms
- Argmin (healthiest): Dürr–Høyer minimum finding
  - Initialize with a random index i as current best.
  - Use a Grover-style search oracle that marks indices j where v_j < v_i.
  - Run O(√N) iterations to find a better index; if found, update i and repeat.
  - Expected O(√N) oracle calls; assumes distinct values or a deterministic tie-break rule.
- Argmax (worst): same as argmin but with comparator reversed (v_j > v_i) or negate values.
- Threshold set (maintenance): Grover search with oracle O(j) = 1 if v_j ≥ τ.
  - If number of marked items M is unknown, use the Boyer–Brassard–Høyer–Tapp (BBHT) strategy (randomize iteration count per round) to find items efficiently.

## Oracle and comparator design
- Comparator: reversible fixed-point inequality test using a ripple-borrow comparator on b bits:
  - Compute (a − b) with reversible borrow; the final borrow-out bit indicates a < b.
  - Uncompute to clean ancillae.
- Oracles:
  - Argmin oracle: mark j if v_j < current_threshold.
  - Argmax oracle: mark j if v_j > current_threshold.
  - Threshold oracle: mark j if v_j ≥ τ.
- Value access: for early prototypes, values are classically indexed and embedded in the oracle (multiplexed comparators). For scale-up, consider QRAM and quantum comparators (as in Kang & Heo, 2020).

## Reporting (per variable, kept separate)
- Argmin index → healthiest pump_id.
- Argmax index → worst pump_id.
- Over-threshold set {pump_id | v ≥ τ}.
- Optionally provide a classical sorted list for readability (sorting isn’t required by the quantum workflow).

## Milestones
1) Simulator prototype on small N (e.g., N = 16, b = 8–10) in Qiskit:
   - Implement fixed-point comparator circuits.
   - Implement Dürr–Høyer loop and threshold Grover.
2) Refactor to reusable oracles; add symmetric argmax path and threshold finder.
3) Integrate a real data loader; generate per-variable reports with pump_ids.
4) Evaluate scaling; consider Kang & Heo (2020) improvements (QRAM, quantum comparator) and iteration-count tuning.

## Practical notes
- Distinctness: Dürr–Høyer analysis assumes all values are distinct; if ties exist, define a tie-break (e.g., choose smallest index).
- Noise: On NISQ devices, keep circuits shallow; start in simulation and use small N.
- Threshold choice: τ should reflect maintenance policy (e.g., τ = 0.8 = “urgent check”).

## Libraries
- Qiskit as the primary framework; PennyLane optional for variational experiments.