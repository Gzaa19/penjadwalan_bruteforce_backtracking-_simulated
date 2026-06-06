import random
import math
import copy
import time

from constraints.validators import is_valid_assignment
from objectives.cost import calculate_cost
from config import SA_INITIAL_TEMP, SA_COOLING_RATE, SA_MIN_TEMP, SA_MAX_ITERATIONS

def generate_initial_solution(classes, slots, pairs, asst_schedules,
                               student_scheds, max_load):
    schedule = []
    shuffled_slots = list(slots)
    shuffled_pairs = list(pairs)

    for class_name in classes:
        random.shuffle(shuffled_slots)
        random.shuffle(shuffled_pairs)

        assigned = False
        for slot in shuffled_slots:
            if assigned:
                break
            for pair in shuffled_pairs:
                if is_valid_assignment(class_name, slot, pair, schedule,
                                       asst_schedules, student_scheds, max_load):
                    schedule.append({
                        "class": class_name,
                        "slot": slot,
                        "assistant_pair": pair,
                    })
                    assigned = True
                    break

        # paksa assign acak kalau tidak ada slot valid
        if not assigned:
            slot = random.choice(shuffled_slots)
            pair = random.choice(shuffled_pairs)
            schedule.append({
                "class": class_name,
                "slot": slot,
                "assistant_pair": pair,
            })

    return schedule

def generate_neighbor(schedule, slots, pairs):
    neighbor = copy.deepcopy(schedule)
    if len(neighbor) == 0:
        return neighbor

    move_type = random.randint(0, 2)

    if move_type == 0:
        # ganti slot satu kelas acak
        idx = random.randint(0, len(neighbor) - 1)
        neighbor[idx]["slot"] = random.choice(slots)
    elif move_type == 1:
        # ganti asisten satu kelas acak
        idx = random.randint(0, len(neighbor) - 1)
        neighbor[idx]["assistant_pair"] = random.choice(pairs)
    else:
        # tukar slot dua kelas acak
        if len(neighbor) >= 2:
            idx1, idx2 = random.sample(range(len(neighbor)), 2)
            neighbor[idx1]["slot"], neighbor[idx2]["slot"] = \
                neighbor[idx2]["slot"], neighbor[idx1]["slot"]

    return neighbor

def simulated_annealing_schedule(classes, slots, pairs, asst_schedules,
                                  student_scheds, max_load,
                                  initial_temp=None, cooling_rate=None,
                                  min_temp=None, max_iterations=None):
    if initial_temp is None:
        initial_temp = SA_INITIAL_TEMP
    if cooling_rate is None:
        cooling_rate = SA_COOLING_RATE
    if min_temp is None:
        min_temp = SA_MIN_TEMP
    if max_iterations is None:
        max_iterations = SA_MAX_ITERATIONS

    print(f"  [SA] Memulai dengan {len(classes)} kelas, T0={initial_temp}, cooling={cooling_rate}...")
    start_time = time.time()

    # inisialisasi solusi awal
    current = generate_initial_solution(
        classes, slots, pairs, asst_schedules, student_scheds, max_load
    )
    current_cost = calculate_cost(
        current, classes, asst_schedules, student_scheds, max_load
    )

    best = copy.deepcopy(current)
    best_cost = current_cost

    temperature = initial_temp
    iterations = 0
    accepted_worse = 0
    cost_history = [current_cost]

    # loop utama sa
    while temperature > min_temp and iterations < max_iterations:
        iterations += 1

        # tetangga
        neighbor = generate_neighbor(current, slots, pairs)
        
        # hitung cost
        neighbor_cost = calculate_cost(
            neighbor, classes, asst_schedules, student_scheds, max_load
        )

        # acceptance criteria
        delta = neighbor_cost - current_cost
        if delta < 0:
            current = neighbor
            current_cost = neighbor_cost
        else:
            acceptance_prob = math.exp(-delta / temperature) if temperature > 0 else 0
            if random.random() < acceptance_prob:
                current = neighbor
                current_cost = neighbor_cost
                accepted_worse += 1

        if current_cost < best_cost:
            best = copy.deepcopy(current)
            best_cost = current_cost

        # cooling
        temperature *= cooling_rate

        if iterations % 100 == 0:
            cost_history.append(best_cost)

        if iterations % 10000 == 0:
            elapsed = time.time() - start_time
            print(f"    Iterasi {iterations:,}: T={temperature:.2f}, Best Cost={best_cost:.2f} ({elapsed:.1f}s)")

    elapsed_time = time.time() - start_time
    print(f"  [SA] Selesai. Iterasi: {iterations:,}, Solusi buruk diterima: {accepted_worse:,}, Waktu: {elapsed_time:.3f}s")

    return {
        "algorithm": "Simulated Annealing",
        "schedule": best,
        "cost": best_cost,
        "explored": iterations,
        "time": elapsed_time,
        "found_solution": len(best) == len(classes),
        "cost_history": cost_history,
        "accepted_worse": accepted_worse,
    }
