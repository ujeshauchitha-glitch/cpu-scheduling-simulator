# CPU Scheduling Simulator

A Python simulator implementing core operating system scheduling algorithms with performance metrics and visual Gantt chart analysis.

---

## Features
- FCFS Scheduling  
- Shortest Job First (SJF)  
- Priority Scheduling  
- Round Robin with configurable quantum  
- Waiting and turnaround time calculation  
- Gantt chart visualization using matplotlib  

---

## System Design
Each process is represented with arrival time, burst time, and priority.  
The scheduler module applies different algorithms to the same process set and records execution order and timing metrics.  

Visualization logic generates Gantt charts to illustrate CPU execution patterns and algorithm behavior.

The design separates scheduling logic, metrics computation, and visualization into independent components.

---

## What I Learned
This project helped me understand how operating systems manage CPU time, compare algorithms, and analyze performance tradeoffs between fairness and efficiency.

---

## How to Run
```bash
pip install matplotlib
python cpu_scheduler.py
