import itertools
import copy
import time

from constraints.validators import is_valid_assignment
from objectives.cost import calculate_cost

def brute_force_schedule(classes, slots, pairs, asst_schedules,
                         student_scheds, max_load, time_limit=60):
    print(f"  [Brute Force] Memulai dengan {len(classes)} kelas, "
          f"{len(slots)} slot, {len(pairs)} pasangan...")
    
    start_time = time.time()
    
    # semua kemungkinan assignment
    options_per_class = list(itertools.product(slots, pairs))
    
    best_schedule = None
    best_cost = float('inf')
    explored = 0
    total_combinations = len(options_per_class) ** len(classes)
    
    print(f"  [Brute Force] Total kombinasi teoritis: {total_combinations:,}")
    
    for combo in itertools.product(options_per_class, repeat=len(classes)):
        # cek timeout
        if time.time() - start_time > time_limit:
            print(f"  [Brute Force] Batas waktu {time_limit}s tercapai. Berhenti.")
            break
            
        explored += 1
        
        # susun jadwal
        valid = True
        temp_schedule = []
        
        for idx, (slot, pair) in enumerate(combo):
            class_name = classes[idx]
            
            if is_valid_assignment(class_name, slot, pair, temp_schedule,
                                   asst_schedules, student_scheds, max_load):
                temp_schedule.append({
                    "class": class_name,
                    "slot": slot,
                    "assistant_pair": pair,
                })
            else:
                valid = False
                break
                
        if valid and len(temp_schedule) == len(classes):
            cost = calculate_cost(temp_schedule, classes, asst_schedules,
                                  student_scheds, max_load)
            if cost < best_cost:
                best_cost = cost
                best_schedule = copy.deepcopy(temp_schedule)
                
        # print progress
        if explored % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"    ... {explored:,} kombinasi dieksplorasi ({elapsed:.1f}s)")
            
    elapsed_time = time.time() - start_time
    print(f"  [Brute Force] Selesai. Eksplorasi: {explored:,}, Waktu: {elapsed_time:.3f}s")
    
    return {
        "algorithm": "Brute Force",
        "schedule": best_schedule if best_schedule else [],
        "cost": best_cost if best_schedule else float('inf'),
        "explored": explored,
        "time": elapsed_time,
        "found_solution": best_schedule is not None,
    }
