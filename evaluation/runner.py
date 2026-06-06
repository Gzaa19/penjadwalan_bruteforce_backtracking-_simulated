from data.assistants import assistant_schedules
from data.students import student_schedules
from config import MAX_LOAD

from algorithms.brute_force import brute_force_schedule
from algorithms.backtracking import backtracking_schedule
from algorithms.simulated_annealing import simulated_annealing_schedule
from objectives.cost import get_schedule_stats
from evaluation.scenarios import create_scenarios
from evaluation.display import print_schedule


def run_experiments():
    scenarios = create_scenarios()
    all_results = []

    print("\nMENJALANKAN EKSPERIMEN")

    for sc_idx, scenario in enumerate(scenarios):
        print(f"\nSKENARIO {sc_idx + 1}: {scenario['name'].upper()}")
        print(f"Deskripsi: {scenario['description']}")

        classes = scenario["classes"]
        slots = scenario["slots"]
        pairs = scenario["pairs"]
        assistants = scenario["assistants"]

        # brute force
        print("\nAlgoritma: Brute Force")
        if scenario["name"] in ["Sedang", "Sulit", "Ekstrem"]:
            print("  [Brute Force] Diskip karena ukuran masalah terlalu besar")
            bf_result = {
                "algorithm": "Brute Force",
                "schedule": [],
                "cost": float('inf'),
                "explored": 0,
                "time": 0.0,
                "found_solution": False,
            }
        else:
            bf_result = brute_force_schedule(
                classes, slots, pairs,
                assistant_schedules, student_schedules, MAX_LOAD,
                time_limit=scenario["bf_time_limit"],
            )
        bf_stats = get_schedule_stats(
            bf_result["schedule"], classes, assistants,
            assistant_schedules, student_schedules, MAX_LOAD,
        )
        bf_result["stats"] = bf_stats
        bf_result["scenario"] = scenario["name"]
        all_results.append(bf_result)

        if bf_result["found_solution"]:
            print_schedule(
                bf_result["schedule"],
                f"Jadwal Terbaik Brute Force (Cost: {bf_result['cost']:.2f})",
            )

        # backtracking
        print("\nAlgoritma: Backtracking")
        if scenario["name"] in ["Ekstrem"]:
            print("  [Backtracking] Diskip karena skenario terlalu kompleks")
            bt_result = {
                "algorithm": "Backtracking",
                "schedule": [],
                "cost": float('inf'),
                "explored": 0,
                "time": 0.0,
                "found_solution": False,
            }
        else:
            bt_result = backtracking_schedule(
                classes, slots, pairs,
                assistant_schedules, student_schedules, MAX_LOAD,
                time_limit=scenario["bt_time_limit"],
            )
        bt_stats = get_schedule_stats(
            bt_result["schedule"], classes, assistants,
            assistant_schedules, student_schedules, MAX_LOAD,
        )
        bt_result["stats"] = bt_stats
        bt_result["scenario"] = scenario["name"]
        all_results.append(bt_result)

        if bt_result["found_solution"]:
            print_schedule(
                bt_result["schedule"],
                f"Jadwal Terbaik Backtracking (Cost: {bt_result['cost']:.2f})",
            )

        # simulated annealing
        print("\nAlgoritma: Simulated Annealing")
        sa_result = simulated_annealing_schedule(
            classes, slots, pairs,
            assistant_schedules, student_schedules, MAX_LOAD,
        )
        sa_stats = get_schedule_stats(
            sa_result["schedule"], classes, assistants,
            assistant_schedules, student_schedules, MAX_LOAD,
        )
        sa_result["stats"] = sa_stats
        sa_result["scenario"] = scenario["name"]
        all_results.append(sa_result)

        if sa_result["found_solution"]:
            print_schedule(
                sa_result["schedule"],
                f"Jadwal Terbaik SA (Cost: {sa_result['cost']:.2f})",
            )

    return all_results, scenarios
