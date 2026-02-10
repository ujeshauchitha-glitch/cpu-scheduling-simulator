# CPU Scheduling Simulator

A comprehensive Python-based simulation of CPU scheduling algorithms with performance analysis and visualization capabilities.

## 🎯 Project Overview

This educational project demonstrates fundamental Operating Systems concepts by implementing four major CPU scheduling algorithms. It provides detailed performance metrics and visual Gantt charts to help understand how different scheduling strategies affect process execution.

## ✨ Features

### Implemented Algorithms

1. **First Come First Serve (FCFS)**
   - Processes executed in arrival order
   - Simple but can cause convoy effect
   - Non-preemptive

2. **Shortest Job First (SJF)**
   - Selects process with shortest burst time
   - Optimal for minimizing average waiting time
   - Non-preemptive

3. **Priority Scheduling**
   - Executes highest priority process first
   - Lower priority number = higher priority
   - Non-preemptive

4. **Round Robin (RR)**
   - Time-sharing with configurable quantum
   - Fair distribution of CPU time
   - Preemptive

### Performance Metrics

For each process:
- **Completion Time**: When the process finishes execution
- **Turnaround Time**: Total time from arrival to completion
- **Waiting Time**: Time spent in ready queue

System-wide:
- **Average Waiting Time**
- **Average Turnaround Time**

### Visualization

- Clean tabular output of all metrics
- Step-by-step execution order
- Color-coded Gantt charts (saved as PNG)

## 🏗️ Architecture

```
cpu_scheduler.py
├── Process (dataclass)
│   └── Represents individual processes with all attributes
├── CPUScheduler (class)
│   ├── fcfs()
│   ├── sjf()
│   ├── priority_scheduling()
│   ├── round_robin()
│   ├── calculate_metrics()
│   ├── print_results()
│   └── draw_gantt_chart()
└── Main Menu Interface
```

### Design Principles

- **Modularity**: Each algorithm is a separate, independent method
- **Extensibility**: Easy to add new scheduling algorithms
- **Clarity**: Comprehensive comments and docstrings
- **Professional**: Clean code following PEP 8 standards

## 🚀 Usage

### Running the Simulator

```bash
python cpu_scheduler.py
```

### Interactive Menu

```
CPU SCHEDULING SIMULATOR
============================================================

Select a Scheduling Algorithm:

  1. First Come First Serve (FCFS)
  2. Shortest Job First (SJF) - Non-preemptive
  3. Priority Scheduling - Non-preemptive
  4. Round Robin (RR)
  5. Run All Algorithms (Comparison)
  0. Exit
```

### Sample Output

```
================================================================================
                     First Come First Serve (FCFS)                            
================================================================================

PID    Arrival    Burst      Priority   Complete     Turnaround   Waiting   
--------------------------------------------------------------------------------
1      0          8          3          8            8            0         
2      1          4          1          12           11           7         
3      2          9          4          21           19           10        
4      3          5          2          26           23           18        
5      4          2          5          28           24           22        
--------------------------------------------------------------------------------
Average Waiting Time:                              11.40
Average Turnaround Time:                           17.00
================================================================================

Execution Order:
P1 -> P2 -> P3 -> P4 -> P5
```

## 📊 Example Process Set

The simulator includes sample processes for immediate testing:

| PID | Arrival Time | Burst Time | Priority |
|-----|-------------|------------|----------|
| 1   | 0           | 8          | 3        |
| 2   | 1           | 4          | 1        |
| 3   | 2           | 9          | 4        |
| 4   | 3           | 5          | 2        |
| 5   | 4           | 2          | 5        |

## 🔧 Customization

### Adding Custom Processes

Modify the `get_sample_processes()` function:

```python
def get_sample_processes() -> List[Process]:
    return [
        Process(pid=1, arrival_time=0, burst_time=5, priority=2),
        Process(pid=2, arrival_time=2, burst_time=3, priority=1),
        # Add more processes...
    ]
```

### Adding New Algorithms

1. Add a new method to the `CPUScheduler` class
2. Implement the scheduling logic
3. Update `self.gantt_chart` for visualization
4. Call `self.calculate_metrics()` at the end
5. Add menu option in `display_menu()` and `run_algorithm()`

Example skeleton:

```python
def shortest_remaining_time_first(self):
    """
    Shortest Remaining Time First (SRTF) - Preemptive SJF.
    """
    # Your implementation here
    # ...
    self.calculate_metrics()
```

## 📚 Algorithm Complexity

| Algorithm  | Time Complexity | Space Complexity | Preemptive |
|-----------|----------------|------------------|------------|
| FCFS      | O(n log n)     | O(1)            | No         |
| SJF       | O(n²)          | O(n)            | No         |
| Priority  | O(n²)          | O(n)            | No         |
| Round Robin| O(n × bt/q)   | O(n)            | Yes        |

*where n = number of processes, bt = total burst time, q = quantum*

## 🎓 Educational Value

This project demonstrates:

- **OS Concepts**: Process scheduling, context switching, time quantum
- **Data Structures**: Queues, sorted lists, process control blocks
- **Algorithms**: Different scheduling strategies and trade-offs
- **Performance Analysis**: Metric calculation and comparison
- **Python Skills**: OOP, dataclasses, type hints, modular design
- **Visualization**: Matplotlib for chart generation

## 📋 Requirements

```
Python 3.7+
matplotlib
```

Install dependencies:
```bash
pip install matplotlib
```

## 🔍 Key Insights

### Algorithm Comparison

- **FCFS**: Simple but inefficient; long processes block shorter ones
- **SJF**: Optimal average waiting time but can starve long processes
- **Priority**: Reflects real-world importance but can cause starvation
- **Round Robin**: Fair and responsive; quantum size critical for performance

### Performance Trade-offs

- **Small quantum**: More context switches, higher overhead
- **Large quantum**: Approaches FCFS behavior
- **Optimal quantum**: Typically 10-100ms in real systems

## 🎯 Future Extensions

Potential enhancements:
- Multilevel Queue Scheduling
- Multilevel Feedback Queue Scheduling
- Shortest Remaining Time First (SRTF)
- Priority with Aging
- Real-time scheduling algorithms
- GUI interface
- CSV import for process data
- Animated Gantt chart generation

## 📝 License

This is an educational project for academic purposes.

## 👨‍💻 Author

Created as a demonstration of Operating Systems concepts and software engineering best practices.

---

**Note**: This simulator is designed for educational purposes to understand CPU scheduling concepts. Real operating systems use far more complex scheduling algorithms with additional considerations like I/O, thread priorities, and multi-core processors.
