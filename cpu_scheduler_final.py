"""
CPU Scheduling Simulator
A project simulating different CPU scheduling algorithms

References: OS Concepts textbook, class lecture notes
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from dataclasses import dataclass
from typing import List
from copy import deepcopy


@dataclass
class Process:
    """Process structure with all necessary attributes"""
    pid: int
    arrival_time: int
    burst_time: int
    priority: int = 0
    remaining_time: int = 0
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0
    
    def __post_init__(self):
        self.remaining_time = self.burst_time


class CPUScheduler:
    
    def __init__(self, processes):
        # using deepcopy here because I was getting weird bugs 
        # when running multiple algorithms on same process list
        self.processes = deepcopy(processes)
        self.gantt_chart = []  # stores (pid, start, end) tuples
        
    def calc_metrics(self):
        """Calculate WT and TAT for all processes"""
        for p in self.processes:
            # TAT = completion - arrival
            p.turnaround_time = p.completion_time - p.arrival_time
            # WT = TAT - burst time
            p.waiting_time = p.turnaround_time - p.burst_time
    
    def get_averages(self):
        """Returns avg waiting and turnaround times"""
        n = len(self.processes)
        avg_wt = sum(p.waiting_time for p in self.processes) / n
        avg_tat = sum(p.turnaround_time for p in self.processes) / n
        return avg_wt, avg_tat
    
    def fcfs(self):
        """
        First Come First Serve - processes run in arrival order
        Pretty straightforward, just sort by arrival and execute
        """
        self.processes.sort(key=lambda p: p.arrival_time)
        
        curr_time = 0
        
        for proc in self.processes:
            # CPU idle? jump to next process arrival
            if curr_time < proc.arrival_time:
                curr_time = proc.arrival_time
            
            start = curr_time
            curr_time += proc.burst_time
            proc.completion_time = curr_time
            
            self.gantt_chart.append((proc.pid, start, curr_time))
        
        self.calc_metrics()
    
    def sjf(self):
        """
        Shortest Job First (non-preemptive)
        Pick shortest burst time from ready queue
        """
        # could use a min heap here but this works fine for small n
        n = len(self.processes)
        completed = 0
        curr_time = 0
        done = [False] * n
        
        while completed < n:
            # find shortest job that's arrived
            shortest_idx = -1
            min_burst = float('inf')
            
            for i in range(n):
                if (not done[i] and 
                    self.processes[i].arrival_time <= curr_time and 
                    self.processes[i].burst_time < min_burst):
                    min_burst = self.processes[i].burst_time
                    shortest_idx = i
            
            # no process ready, jump to next arrival
            if shortest_idx == -1:
                curr_time = min([p.arrival_time for i, p in enumerate(self.processes) if not done[i]])
                continue
            
            # execute process
            p = self.processes[shortest_idx]
            start = curr_time
            curr_time += p.burst_time
            p.completion_time = curr_time
            done[shortest_idx] = True
            completed += 1
            
            self.gantt_chart.append((p.pid, start, curr_time))
        
        self.calc_metrics()
    
    def priority_sched(self):
        """
        Priority scheduling - lower number = higher priority
        Similar logic to SJF but checks priority instead
        """
        # TODO: add aging to prevent starvation
        n = len(self.processes)
        completed = 0
        curr_time = 0
        done = [False] * n
        
        while completed < n:
            highest_idx = -1
            highest_priority = float('inf')
            
            for i in range(n):
                if (not done[i] and 
                    self.processes[i].arrival_time <= curr_time and 
                    self.processes[i].priority < highest_priority):
                    highest_priority = self.processes[i].priority
                    highest_idx = i
            
            if highest_idx == -1:
                curr_time = min([p.arrival_time for i, p in enumerate(self.processes) if not done[i]])
                continue
            
            p = self.processes[highest_idx]
            start = curr_time
            curr_time += p.burst_time
            p.completion_time = curr_time
            done[highest_idx] = True
            completed += 1
            
            self.gantt_chart.append((p.pid, start, curr_time))
        
        self.calc_metrics()
    
    def round_robin(self, quantum):
        """
        Round Robin with time quantum
        This one was tricky - had to handle the ready queue carefully
        Bug I fixed: wasn't adding new arrivals to queue at the right time
        """
        self.processes.sort(key=lambda p: p.arrival_time)
        
        ready_q = []
        curr_time = 0
        idx = 0
        n = len(self.processes)
        
        # add first process
        if n > 0:
            ready_q.append(self.processes[0])
            idx = 1
        
        while ready_q:
            proc = ready_q.pop(0)
            
            start = curr_time
            exec_time = min(quantum, proc.remaining_time)
            curr_time += exec_time
            proc.remaining_time -= exec_time
            
            self.gantt_chart.append((proc.pid, start, curr_time))
            
            # add any new arrivals to queue
            while idx < n and self.processes[idx].arrival_time <= curr_time:
                ready_q.append(self.processes[idx])
                idx += 1
            
            # if process not done, back to queue
            if proc.remaining_time > 0:
                ready_q.append(proc)
            else:
                proc.completion_time = curr_time
            
            # handle idle time
            if not ready_q and idx < n:
                curr_time = self.processes[idx].arrival_time
                ready_q.append(self.processes[idx])
                idx += 1
        
        self.calc_metrics()
    
    def print_results(self, algo_name):
        """Print the results table"""
        print(f"\n{'='*80}")
        print(f"{algo_name:^80}")
        print(f"{'='*80}")
        
        # header
        print(f"\n{'PID':<6} {'Arrival':<10} {'Burst':<10} {'Priority':<10} "
              f"{'Complete':<12} {'TAT':<12} {'WT':<10}")
        print("-" * 80)
        
        # data
        for p in sorted(self.processes, key=lambda x: x.pid):
            print(f"{p.pid:<6} {p.arrival_time:<10} {p.burst_time:<10} {p.priority:<10} "
                  f"{p.completion_time:<12} {p.turnaround_time:<12} {p.waiting_time:<10}")
        
        # averages
        avg_wt, avg_tat = self.get_averages()
        print("-" * 80)
        print(f"Average Waiting Time: {avg_wt:.2f}")
        print(f"Average Turnaround Time: {avg_tat:.2f}")
        print(f"{'='*80}\n")
        
        # execution sequence
        print("Execution Order:")
        print(" -> ".join([f"P{pid}" for pid, _, _ in self.gantt_chart]))
        print()
    
    def draw_gantt(self, algo_name):
        """Generate Gantt chart visualization"""
        if not self.gantt_chart:
            return
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # color mapping for processes
        # using Set3 colormap - looks cleaner than random colors
        colors = plt.cm.Set3.colors
        proc_colors = {}
        
        # draw bars
        for pid, start, end in self.gantt_chart:
            if pid not in proc_colors:
                proc_colors[pid] = colors[len(proc_colors) % len(colors)]
            
            ax.barh(0, end - start, left=start, height=0.5, 
                   color=proc_colors[pid], edgecolor='black', linewidth=1.5)
            
            # label
            mid = (start + end) / 2
            ax.text(mid, 0, f'P{pid}', ha='center', va='center', 
                   fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Time', fontsize=12, fontweight='bold')
        ax.set_ylabel('CPU', fontsize=12, fontweight='bold')
        ax.set_title(f'Gantt Chart - {algo_name}', fontsize=14, fontweight='bold', pad=20)
        
        ax.set_yticks([0])
        ax.set_yticklabels(['CPU'])
        ax.set_ylim(-0.5, 0.5)
        
        max_t = max(end for _, _, end in self.gantt_chart)
        ax.set_xlim(0, max_t)
        ax.set_xticks(range(0, max_t + 1, max(1, max_t // 20)))
        
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        # legend
        legend_items = [mpatches.Patch(color=proc_colors[pid], label=f'Process {pid}') 
                       for pid in sorted(proc_colors.keys())]
        ax.legend(handles=legend_items, loc='upper right', bbox_to_anchor=(1.12, 1))
        
        plt.tight_layout()
        filename = f'gantt_{algo_name.replace(" ", "_").lower()}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Gantt chart saved: {filename}\n")


def get_sample_data():
    """Sample process set for testing"""
    return [
        Process(pid=1, arrival_time=0, burst_time=8, priority=3),
        Process(pid=2, arrival_time=1, burst_time=4, priority=1),
        Process(pid=3, arrival_time=2, burst_time=9, priority=4),
        Process(pid=4, arrival_time=3, burst_time=5, priority=2),
        Process(pid=5, arrival_time=4, burst_time=2, priority=5),
    ]
    
    # Test case I used during debugging - all arrive at same time
    # return [
    #     Process(pid=1, arrival_time=0, burst_time=10, priority=2),
    #     Process(pid=2, arrival_time=0, burst_time=1, priority=1),
    #     Process(pid=3, arrival_time=0, burst_time=5, priority=3),
    # ]


def show_menu():
    print("\n" + "="*60)
    print("CPU SCHEDULING SIMULATOR".center(60))
    print("="*60)
    print("\nChoose Algorithm:\n")
    print("  1. FCFS (First Come First Serve)")
    print("  2. SJF (Shortest Job First)")
    print("  3. Priority Scheduling")
    print("  4. Round Robin")
    print("  5. Run All & Compare")
    print("  0. Exit")
    print("\n" + "-"*60)


def run_algo(choice, processes):
    """Execute the selected algorithm"""
    if choice == 1:
        sched = CPUScheduler(processes)
        sched.fcfs()
        sched.print_results("First Come First Serve (FCFS)")
        sched.draw_gantt("FCFS")
        
    elif choice == 2:
        sched = CPUScheduler(processes)
        sched.sjf()
        sched.print_results("Shortest Job First (SJF)")
        sched.draw_gantt("SJF")
        
    elif choice == 3:
        sched = CPUScheduler(processes)
        sched.priority_sched()
        sched.print_results("Priority Scheduling")
        sched.draw_gantt("Priority")
        
    elif choice == 4:
        q = int(input("\nTime quantum: "))
        sched = CPUScheduler(processes)
        sched.round_robin(q)
        sched.print_results(f"Round Robin (Q={q})")
        sched.draw_gantt(f"RR_Q{q}")
        
    elif choice == 5:
        # compare all
        print("\n" + "="*80)
        print("COMPARING ALL ALGORITHMS".center(80))
        print("="*80)
        
        algos = [
            ("FCFS", lambda s: s.fcfs()),
            ("SJF", lambda s: s.sjf()),
            ("Priority", lambda s: s.priority_sched()),
            ("Round Robin (Q=2)", lambda s: s.round_robin(2)),
        ]
        
        for name, func in algos:
            sched = CPUScheduler(processes)
            func(sched)
            sched.print_results(name)
            sched.draw_gantt(name)


def main():
    processes = get_sample_data()
    
    # show input
    print("\n" + "="*60)
    print("PROCESS DATA".center(60))
    print("="*60)
    print(f"\n{'PID':<8} {'Arrival':<12} {'Burst':<12} {'Priority':<10}")
    print("-" * 60)
    for p in processes:
        print(f"{p.pid:<8} {p.arrival_time:<12} {p.burst_time:<12} {p.priority:<10}")
    print("="*60)
    
    while True:
        show_menu()
        
        try:
            choice = int(input("Enter choice: "))
            
            if choice == 0:
                print("\nExiting simulator...")
                break
            
            if choice in [1, 2, 3, 4, 5]:
                run_algo(choice, processes)
                input("\nPress Enter to continue...")
            else:
                print("\nInvalid choice!")
                
        except ValueError:
            print("\nPlease enter a number")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break


if __name__ == "__main__":
    main()
