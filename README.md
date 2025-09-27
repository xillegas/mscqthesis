# Master's Thesis: Quantum-Enhanced Industrial Asset Management

## Project Overview

This repository contains the research and code for my Master's thesis in Quantum Computing. The project focuses on applying hybrid quantum algorithms to solve a real-world industrial problem: the health monitoring of hydrocarbon pumps.

## Problem Statement

In industrial settings like fuel loading stations, Distributed Control Systems (DCS) are responsible for managing equipment. As the number of assets (pumps) grows, monitoring their health status in real-time becomes a significant computational burden on the classical DCS.

This project proposes offloading this data processing task to a hybrid quantum-classical system. The goal is to use quantum algorithms to analyze sensor data from the pumps to efficiently generate health reports, enabling large-scale monitoring (from a regional to a national level) while reducing the load on the classical control systems.

## Key Research Areas

*   **Problem Formulation:** Translating the pump health monitoring task into a problem solvable by a quantum algorithm (e.g., a QUBO for optimization or a quantum machine learning model for classification).
*   **Hybrid Quantum Algorithms:** Investigating algorithms like the Variational Quantum Eigensolver (VQE) or the Quantum Approximate Optimization Algorithm (QAOA) for this task.
*   **Data Simulation:** Simulating sensor data that represents various "health states" of the pumps.
*   **Implementation:** Using quantum computing libraries like Qiskit, PennyLane, or MindSpore Quantum to build and test the proposed solution.

## Repository Structure

*   `/code`: Contains stable, working implementations of the quantum algorithms.
*   `/docs`: Includes summaries, notes, and literature reviews.
*   `/papers`: Stores key research papers relevant to the thesis.
*   `/Other notebooks`: Holds experimental code, library tests, and initial prototypes.