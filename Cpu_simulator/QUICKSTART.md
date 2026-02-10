# Quick Start Guide

## Installation

1. **Ensure Python 3.7+ is installed:**
   ```bash
   python --version
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Simulator

### Interactive Mode (Recommended)
```bash
python cpu_scheduler.py
```

This launches an interactive menu where you can:
- Choose individual algorithms to run
- Set custom quantum values for Round Robin
- Compare all algorithms at once

### Demo Mode (Quick Overview)
```bash
python demo_scheduler.py
```

This automatically runs all algorithms and shows a comparison table.

## Understanding the Output

### 1. Process Information Table
Shows input data for all processes before scheduling.

### 2. Results Table
For each algorithm, you'll see:
- **Completion Time**: When each process finishes
- **Turnaround Time**: Total time in system (Completion - Arrival)
- **Waiting Time**: Time spent waiting (Turnaround - Burst)
- **Average Metrics**: System-wide performance indicators

### 3. Execution Order
Shows the sequence in which processes were executed.

### 4. Gantt Chart
Visual timeline saved as PNG file showing:
- Process execution periods (colored bars)
- Time progression on x-axis
- Each process has a unique color

## Sample Process Set

| PID | Arrival | Burst | Priority |
|-----|---------|-------|----------|
| 1   | 0       | 8     | 3        |
| 2   | 1       | 4     | 1        |
| 3   | 2       | 9     | 4        |
| 4   | 3       | 5     | 2        |
| 5   | 4       | 2     | 5        |

## Interpreting Results

### Which Algorithm is Best?

**For Average Waiting Time:**
- SJF typically has the lowest (optimal for non-preemptive)
- Round Robin depends on quantum size
- FCFS usually has the highest

**For Fairness:**
- Round Robin provides most equal treatment
- Priority can starve low-priority processes
- SJF can starve long processes

**For Simplicity:**
- FCFS is easiest to implement
- No overhead, predictable

**For Real-Time Systems:**
- Priority scheduling preferred
- Round Robin with small quantum for responsiveness

## Customizing Processes

Edit `get_sample_processes()` in `cpu_scheduler.py`:

```python
def get_sample_processes() -> List[Process]:
    return [
        Process(pid=1, arrival_time=0, burst_time=10, priority=1),
        Process(pid=2, arrival_time=2, burst_time=5, priority=2),
        # Add your processes here
    ]
```

## Troubleshooting

**Issue:** Matplotlib doesn't display charts
**Solution:** Charts are saved as PNG files in the current directory

**Issue:** "Module not found" error
**Solution:** Install requirements with `pip install -r requirements.txt`

**Issue:** Charts look crowded
**Solution:** Reduce number of processes or increase quantum for Round Robin

## Academic Use

This project is suitable for:
- Operating Systems course projects
- Algorithm analysis assignments
- Portfolio demonstrations
- Interview preparation
- Teaching scheduling concepts

## Key Formulas

```
Turnaround Time = Completion Time - Arrival Time
Waiting Time = Turnaround Time - Burst Time
Response Time = First CPU Time - Arrival Time (not implemented)
```

## Next Steps

1. Run demo mode to see all algorithms
2. Try different quantum values for Round Robin
3. Modify process data to test edge cases
4. Implement additional algorithms (SRTF, MLFQ)
5. Add your own processes and analyze results

## Output Files

After running the simulator, you'll find:
- `gantt_chart_fcfs.png`
- `gantt_chart_sjf.png`
- `gantt_chart_priority_scheduling.png`
- `gantt_chart_round_robin_(q=x).png`

Happy Scheduling! 🚀
