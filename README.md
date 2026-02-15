# CPU Scheduling Simulator
![Gantt Chart Output](image.png)
A technical tool designed to model and analyze the performance of various Central Processing Unit (CPU) scheduling algorithms. This project provides a quantitative comparison of process management strategies used in modern operating systems.

**Link to Live Project:** https://ujeshauchitha-glitch.github.io/cpu-scheduling-simulator/

## Implementation Details

The simulator evaluates the efficiency of four primary scheduling disciplines. The core logic handles time-sequenced process arrival and execution states using a custom JavaScript engine.

### Supported Algorithms
* First-Come, First-Served (FCFS)
* Shortest Job First (SJF)
* Round Robin (RR)
* Priority Scheduling

## Technical Architecture

### 1. Process State Management
The system maintains a state for each process, tracking its Arrival Time (AT), Burst Time (BT), and Remaining Time. For preemptive algorithms like Round Robin, the engine manages the re-insertion of processes into the ready queue while maintaining data integrity of the remaining burst cycles.

### 2. Analytical Calculations
The engine calculates precise performance metrics:
* Turnaround Time (TAT): Completion Time - Arrival Time
* Waiting Time (WT): Turnaround Time - Burst Time
* System Throughput: Calculation of average wait and turnaround times.

### 3. Interface Design
The front-end is constructed with vanilla HTML/CSS and direct DOM manipulation. This ensures performance during high-frequency calculation updates.
