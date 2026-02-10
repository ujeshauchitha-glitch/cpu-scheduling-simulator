"""
CPU Scheduling Simulator
========================
A comprehensive simulation of CPU scheduling algorithms with performance metrics
and Gantt chart visualization.

Author: Systems Programming Educational Project
Purpose: Demonstrates understanding of OS scheduling concepts and Python design
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from dataclasses import dataclass
from typing import List, Tuple
from copy import deepcopy


@dataclass
class Process:
    """
    Represents a process in the CPU scheduling system.
    
    Attributes:
        pid: Process ID (unique identifier)
        arrival_time: Time when process arrives in the ready queue
        burst_time: CPU time required for process completion
        priority: Process priority (lower number = higher priority)
        remaining_time: Remaining burst time (used in preemptive algorithms)
        completion_time: Time when process finishes execution
        turnaround_time: Total time from arrival to completion
        waiting_time: Time spent waiting in ready queue
    """
    pid: int
    arrival_time: int
    burst_time: int
    priority: int = 0
    remaining_time: int = 0
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0
    
    def __post_init__(self):
        """Initialize remaining time to burst time"""
        self.remaining_time = self.burst_time


class CPUScheduler:
    """
    CPU Scheduling Simulator implementing multiple scheduling algorithms.
    """
    
    def __init__(self, processes: List[Process]):
        """
        Initialize scheduler with a list of processes.
        
        Args:
            processes: List of Process objects to be scheduled
        """
        self.processes = deepcopy(processes)
        self.gantt_chart = []  # List of (process_id, start_time, end_time)
        
    def calculate_metrics(self):
        """
        Calculate waiting time and turnaround time for all processes.
        
        Formulas:
            Turnaround Time = Completion Time - Arrival Time
            Waiting Time = Turnaround Time - Burst Time
        """
        for process in self.processes:
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
    
    def get_average_metrics(self) -> Tuple[float, float]:
        """
        Calculate average waiting time and turnaround time.
        
        Returns:
            Tuple of (average_waiting_time, average_turnaround_time)
        """
        n = len(self.processes)
        avg_waiting = sum(p.waiting_time for p in self.processes) / n
        avg_turnaround = sum(p.turnaround_time for p in self.processes) / n
        return avg_waiting, avg_turnaround
    
    def fcfs(self):
        """
        First Come First Serve (FCFS) Scheduling Algorithm.
        
        Logic:
            - Processes are executed in the order they arrive
            - Non-preemptive: once started, runs to completion
            - Simple but can cause convoy effect (long process delays shorter ones)
        
        Time Complexity: O(n log n) for sorting
        """
        # Sort by arrival time
        self.processes.sort(key=lambda p: p.arrival_time)
        
        current_time = 0
        
        for process in self.processes:
            # If CPU is idle, jump to next arrival
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            # Record start time for Gantt chart
            start_time = current_time
            
            # Execute process
            current_time += process.burst_time
            process.completion_time = current_time
            
            # Add to Gantt chart
            self.gantt_chart.append((process.pid, start_time, current_time))
        
        self.calculate_metrics()
    
    def sjf(self):
        """
        Shortest Job First (SJF) - Non-preemptive.
        
        Logic:
            - Select process with shortest burst time from ready queue
            - Non-preemptive: runs to completion once started
            - Minimizes average waiting time (optimal for non-preemptive)
            - Can cause starvation of longer processes
        
        Time Complexity: O(n²) in worst case
        """
        n = len(self.processes)
        completed = 0
        current_time = 0
        is_completed = [False] * n
        
        while completed < n:
            # Find process with shortest burst time that has arrived
            idx = -1
            min_burst = float('inf')
            
            for i, process in enumerate(self.processes):
                if (not is_completed[i] and 
                    process.arrival_time <= current_time and 
                    process.burst_time < min_burst):
                    min_burst = process.burst_time
                    idx = i
            
            if idx == -1:
                # No process ready, jump to next arrival
                current_time = min(p.arrival_time for i, p in enumerate(self.processes) 
                                 if not is_completed[i])
                continue
            
            # Execute selected process
            process = self.processes[idx]
            start_time = current_time
            current_time += process.burst_time
            process.completion_time = current_time
            is_completed[idx] = True
            completed += 1
            
            # Add to Gantt chart
            self.gantt_chart.append((process.pid, start_time, current_time))
        
        self.calculate_metrics()
    
    def priority_scheduling(self):
        """
        Priority Scheduling - Non-preemptive.
        
        Logic:
            - Select process with highest priority (lowest priority number)
            - Non-preemptive: runs to completion
            - Can cause starvation of low-priority processes
            - Often combined with aging to prevent starvation
        
        Time Complexity: O(n²) in worst case
        """
        n = len(self.processes)
        completed = 0
        current_time = 0
        is_completed = [False] * n
        
        while completed < n:
            # Find highest priority process that has arrived
            idx = -1
            highest_priority = float('inf')
            
            for i, process in enumerate(self.processes):
                if (not is_completed[i] and 
                    process.arrival_time <= current_time and 
                    process.priority < highest_priority):
                    highest_priority = process.priority
                    idx = i
            
            if idx == -1:
                # No process ready, jump to next arrival
                current_time = min(p.arrival_time for i, p in enumerate(self.processes) 
                                 if not is_completed[i])
                continue
            
            # Execute selected process
            process = self.processes[idx]
            start_time = current_time
            current_time += process.burst_time
            process.completion_time = current_time
            is_completed[idx] = True
            completed += 1
            
            # Add to Gantt chart
            self.gantt_chart.append((process.pid, start_time, current_time))
        
        self.calculate_metrics()
    
    def round_robin(self, quantum: int):
        """
        Round Robin (RR) Scheduling Algorithm.
        
        Logic:
            - Each process gets a time quantum in circular order
            - Preemptive: processes are interrupted after quantum expires
            - Fair time-sharing, good for interactive systems
            - Performance depends on quantum size
        
        Args:
            quantum: Time slice allocated to each process
        
        Time Complexity: O(n × total_burst_time / quantum)
        """
        # Sort by arrival time
        self.processes.sort(key=lambda p: p.arrival_time)
        
        ready_queue = []
        current_time = 0
        idx = 0
        n = len(self.processes)
        
        # Add first process to queue
        if n > 0:
            ready_queue.append(self.processes[0])
            idx = 1
        
        while ready_queue:
            process = ready_queue.pop(0)
            
            # Execute for quantum or remaining time, whichever is smaller
            start_time = current_time
            execution_time = min(quantum, process.remaining_time)
            current_time += execution_time
            process.remaining_time -= execution_time
            
            # Add to Gantt chart
            self.gantt_chart.append((process.pid, start_time, current_time))
            
            # Add newly arrived processes to queue
            while idx < n and self.processes[idx].arrival_time <= current_time:
                ready_queue.append(self.processes[idx])
                idx += 1
            
            # If process not finished, add back to queue
            if process.remaining_time > 0:
                ready_queue.append(process)
            else:
                # Process completed
                process.completion_time = current_time
            
            # If queue empty but processes remain, jump to next arrival
            if not ready_queue and idx < n:
                current_time = self.processes[idx].arrival_time
                ready_queue.append(self.processes[idx])
                idx += 1
        
        self.calculate_metrics()
    
    def print_results(self, algorithm_name: str):
        """
        Print formatted results table with all metrics.
        
        Args:
            algorithm_name: Name of the scheduling algorithm used
        """
        print(f"\n{'='*80}")
        print(f"{algorithm_name:^80}")
        print(f"{'='*80}")
        
        # Table header
        print(f"\n{'PID':<6} {'Arrival':<10} {'Burst':<10} {'Priority':<10} "
              f"{'Complete':<12} {'Turnaround':<12} {'Waiting':<10}")
        print("-" * 80)
        
        # Process data
        for p in sorted(self.processes, key=lambda x: x.pid):
            print(f"{p.pid:<6} {p.arrival_time:<10} {p.burst_time:<10} {p.priority:<10} "
                  f"{p.completion_time:<12} {p.turnaround_time:<12} {p.waiting_time:<10}")
        
        # Average metrics
        avg_waiting, avg_turnaround = self.get_average_metrics()
        print("-" * 80)
        print(f"{'Average Waiting Time:':<50} {avg_waiting:.2f}")
        print(f"{'Average Turnaround Time:':<50} {avg_turnaround:.2f}")
        print(f"{'='*80}\n")
        
        # Execution order
        print("Execution Order:")
        print(" -> ".join([f"P{pid}" for pid, _, _ in self.gantt_chart]))
        print()
    
    def draw_gantt_chart(self, algorithm_name: str):
        """
        Generate and display Gantt chart visualization.
        
        Args:
            algorithm_name: Name of the algorithm for the chart title
        """
        if not self.gantt_chart:
            print("No Gantt chart data available.")
            return
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Color map for different processes
        colors = plt.cm.Set3.colors
        process_colors = {}
        
        # Draw timeline bars
        for pid, start, end in self.gantt_chart:
            if pid not in process_colors:
                process_colors[pid] = colors[len(process_colors) % len(colors)]
            
            ax.barh(0, end - start, left=start, height=0.5, 
                   color=process_colors[pid], edgecolor='black', linewidth=1.5)
            
            # Add process label in the middle of the bar
            mid_point = (start + end) / 2
            ax.text(mid_point, 0, f'P{pid}', ha='center', va='center', 
                   fontsize=10, fontweight='bold')
        
        # Set labels and title
        ax.set_xlabel('Time', fontsize=12, fontweight='bold')
        ax.set_ylabel('CPU', fontsize=12, fontweight='bold')
        ax.set_title(f'Gantt Chart - {algorithm_name}', 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Set y-axis
        ax.set_yticks([0])
        ax.set_yticklabels(['CPU'])
        ax.set_ylim(-0.5, 0.5)
        
        # Set x-axis
        max_time = max(end for _, _, end in self.gantt_chart)
        ax.set_xlim(0, max_time)
        ax.set_xticks(range(0, max_time + 1, max(1, max_time // 20)))
        
        # Grid
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        # Legend
        legend_patches = [mpatches.Patch(color=process_colors[pid], label=f'Process {pid}') 
                         for pid in sorted(process_colors.keys())]
        ax.legend(handles=legend_patches, loc='upper right', 
                 bbox_to_anchor=(1.12, 1), framealpha=0.9)
        
        plt.tight_layout()
        filename = f'gantt_chart_{algorithm_name.replace(" ", "_").lower()}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"Gantt chart saved as 'gantt_chart_{algorithm_name.replace(' ', '_').lower()}.png'\n")


def get_sample_processes() -> List[Process]:
    """
    Returns sample process data for demonstration.
    
    This represents a realistic mix of processes with different characteristics:
    - Short and long burst times
    - Various arrival times
    - Different priorities
    """
    return [
        Process(pid=1, arrival_time=0, burst_time=8, priority=3),
        Process(pid=2, arrival_time=1, burst_time=4, priority=1),
        Process(pid=3, arrival_time=2, burst_time=9, priority=4),
        Process(pid=4, arrival_time=3, burst_time=5, priority=2),
        Process(pid=5, arrival_time=4, burst_time=2, priority=5),
    ]


def display_menu():
    """Display the main menu for algorithm selection."""
    print("\n" + "="*60)
    print("CPU SCHEDULING SIMULATOR".center(60))
    print("="*60)
    print("\nSelect a Scheduling Algorithm:\n")
    print("  1. First Come First Serve (FCFS)")
    print("  2. Shortest Job First (SJF) - Non-preemptive")
    print("  3. Priority Scheduling - Non-preemptive")
    print("  4. Round Robin (RR)")
    print("  5. Run All Algorithms (Comparison)")
    print("  0. Exit")
    print("\n" + "-"*60)


def run_algorithm(choice: int, processes: List[Process]):
    """
    Execute the selected scheduling algorithm.
    
    Args:
        choice: Menu choice number
        processes: List of processes to schedule
    """
    if choice == 1:
        scheduler = CPUScheduler(processes)
        scheduler.fcfs()
        scheduler.print_results("First Come First Serve (FCFS)")
        scheduler.draw_gantt_chart("FCFS")
        
    elif choice == 2:
        scheduler = CPUScheduler(processes)
        scheduler.sjf()
        scheduler.print_results("Shortest Job First (SJF)")
        scheduler.draw_gantt_chart("SJF")
        
    elif choice == 3:
        scheduler = CPUScheduler(processes)
        scheduler.priority_scheduling()
        scheduler.print_results("Priority Scheduling")
        scheduler.draw_gantt_chart("Priority Scheduling")
        
    elif choice == 4:
        quantum = int(input("\nEnter time quantum: "))
        scheduler = CPUScheduler(processes)
        scheduler.round_robin(quantum)
        scheduler.print_results(f"Round Robin (Quantum = {quantum})")
        scheduler.draw_gantt_chart(f"Round Robin (Q={quantum})")
        
    elif choice == 5:
        # Run all algorithms for comparison
        algorithms = [
            ("FCFS", lambda s: s.fcfs()),
            ("SJF", lambda s: s.sjf()),
            ("Priority", lambda s: s.priority_scheduling()),
            ("Round Robin (Q=2)", lambda s: s.round_robin(2)),
        ]
        
        print("\n" + "="*80)
        print("RUNNING ALL ALGORITHMS FOR COMPARISON".center(80))
        print("="*80)
        
        for name, algo_func in algorithms:
            scheduler = CPUScheduler(processes)
            algo_func(scheduler)
            scheduler.print_results(name)
            scheduler.draw_gantt_chart(name)


def main():
    """
    Main entry point for the CPU Scheduling Simulator.
    Provides interactive menu for algorithm selection and execution.
    """
    # Get sample processes
    processes = get_sample_processes()
    
    # Display initial process information
    print("\n" + "="*60)
    print("PROCESS INFORMATION".center(60))
    print("="*60)
    print(f"\n{'PID':<8} {'Arrival':<12} {'Burst':<12} {'Priority':<10}")
    print("-" * 60)
    for p in processes:
        print(f"{p.pid:<8} {p.arrival_time:<12} {p.burst_time:<12} {p.priority:<10}")
    print("="*60)
    
    while True:
        display_menu()
        
        try:
            choice = int(input("Enter your choice: "))
            
            if choice == 0:
                print("\n" + "="*60)
                print("Thank you for using CPU Scheduling Simulator!".center(60))
                print("="*60 + "\n")
                break
            
            if choice in [1, 2, 3, 4, 5]:
                run_algorithm(choice, processes)
                input("\nPress Enter to continue...")
            else:
                print("\n⚠️  Invalid choice. Please select 0-5.")
                
        except ValueError:
            print("\n⚠️  Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break


if __name__ == "__main__":
    main()
