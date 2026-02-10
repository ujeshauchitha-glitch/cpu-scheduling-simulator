"""
CPU Scheduling Simulator - Automated Demo
==========================================
This script demonstrates all scheduling algorithms without user interaction.
"""

from cpu_scheduler import CPUScheduler, Process, get_sample_processes


def run_demo():
    """Run all scheduling algorithms and display results."""
    
    processes = get_sample_processes()
    
    # Display initial process information
    print("\n" + "="*80)
    print("CPU SCHEDULING SIMULATOR - AUTOMATED DEMONSTRATION".center(80))
    print("="*80)
    print(f"\n{'PID':<8} {'Arrival':<12} {'Burst':<12} {'Priority':<10}")
    print("-" * 80)
    for p in processes:
        print(f"{p.pid:<8} {p.arrival_time:<12} {p.burst_time:<12} {p.priority:<10}")
    print("="*80)
    
    # Algorithm configurations
    algorithms = [
        ("First Come First Serve (FCFS)", lambda s: s.fcfs()),
        ("Shortest Job First (SJF)", lambda s: s.sjf()),
        ("Priority Scheduling", lambda s: s.priority_scheduling()),
        ("Round Robin (Quantum = 2)", lambda s: s.round_robin(2)),
        ("Round Robin (Quantum = 4)", lambda s: s.round_robin(4)),
    ]
    
    # Run each algorithm
    for name, algo_func in algorithms:
        scheduler = CPUScheduler(processes)
        algo_func(scheduler)
        scheduler.print_results(name)
        scheduler.draw_gantt_chart(name)
    
    # Comparison table
    print("\n" + "="*80)
    print("PERFORMANCE COMPARISON".center(80))
    print("="*80)
    print(f"\n{'Algorithm':<35} {'Avg Waiting':<20} {'Avg Turnaround':<20}")
    print("-" * 80)
    
    for name, algo_func in algorithms:
        scheduler = CPUScheduler(processes)
        algo_func(scheduler)
        avg_waiting, avg_turnaround = scheduler.get_average_metrics()
        print(f"{name:<35} {avg_waiting:<20.2f} {avg_turnaround:<20.2f}")
    
    print("="*80)
    
    print("\n✅ All algorithms executed successfully!")
    print("📊 Gantt charts saved as PNG files in the current directory.\n")


if __name__ == "__main__":
    run_demo()
