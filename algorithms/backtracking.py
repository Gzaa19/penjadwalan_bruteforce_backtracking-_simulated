import copy
import time

from constraints.validators import is_valid_assignment
from objectives.cost import calculate_cost

def backtracking_schedule(classes, slots, pairs, asst_schedules,
                          student_scheds, max_load, time_limit=120):
    print(f"  [Backtracking] Memulai dengan {len(classes)} kelas, "
          f"{len(slots)} slot, {len(pairs)} pasangan...")
    
    start_time = time.time()
    
    # simpan state pencarian
    state = {
        "explored": 0,
        "best_schedule": None,
        "best_cost": float('inf'),
        "found_any": False,
        "time_limit_reached": False,
    }
    
    def backtrack(class_idx, current_schedule):
        # cek timeout
        if time.time() - start_time > time_limit:
            state["time_limit_reached"] = True
            return
            
        # base case
        if class_idx == len(classes):
            state["explored"] += 1
            cost = calculate_cost(current_schedule, classes, asst_schedules,
                                  student_scheds, max_load)
            if cost < state["best_cost"]:
                state["best_cost"] = cost
                state["best_schedule"] = copy.deepcopy(current_schedule)
                state["found_any"] = True
                print(f"    -> Solusi ditemukan! Cost: {cost:.2f}")
            return
            
        class_name = classes[class_idx]
        
        # coba slot & pair
        for slot in slots:
            if state["time_limit_reached"]:
                return
                
            for pair in pairs:
                state["explored"] += 1
                
                # pruning: cek kelayakan
                if is_valid_assignment(class_name, slot, pair, current_schedule,
                                       asst_schedules, student_scheds, max_load):
                    current_schedule.append({
                        "class": class_name,
                        "slot": slot,
                        "assistant_pair": pair,
                    })
                    
                    # rekursi
                    backtrack(class_idx + 1, current_schedule)
                    
                    # backtrack
                    current_schedule.pop()
                    
        # log progress
        if class_idx <= 1 and state["explored"] % 50000 == 0:
            elapsed = time.time() - start_time
            print(f"    ... {state['explored']:,} node dieksplorasi ({elapsed:.1f}s)")
            
    # jalankan
    backtrack(0, [])
    elapsed_time = time.time() - start_time
    
    if state["time_limit_reached"]:
        print(f"  [Backtracking] Batas waktu {time_limit}s tercapai.")
        
    print(f"  [Backtracking] Selesai. Eksplorasi: {state['explored']:,}, Waktu: {elapsed_time:.3f}s")
    
    return {
        "algorithm": "Backtracking",
        "schedule": state["best_schedule"] if state["best_schedule"] else [],
        "cost": state["best_cost"] if state["found_any"] else float('inf'),
        "explored": state["explored"],
        "time": elapsed_time,
        "found_solution": state["found_any"],
    }
