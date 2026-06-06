import math
from collections import defaultdict

from config import (
    PENALTY_HARD_CONSTRAINT,
    PENALTY_NIGHT_SLOT,
    PENALTY_LOAD_IMBALANCE,
    PENALTY_UNSCHEDULED_CLASS,
)
from constraints.validators import (
    is_forbidden_slot,
    is_slot_conflict_with_students,
    is_slot_conflict_with_assistant,
    is_overlap,
)

def count_hard_violations(schedule, classes, asst_schedules, student_scheds, max_load):
    violations = 0

    # Cek setiap entry dalam jadwal
    for entry in schedule:
        slot = entry["slot"]
        pair = entry["assistant_pair"]
        asst1, asst2 = pair

        # Cek slot terlarang
        if is_forbidden_slot(slot):
            violations += 1

        # Cek bentrok jadwal praktikan
        if is_slot_conflict_with_students(slot, student_scheds):
            violations += 1

        # Cek bentrok jadwal asisten
        if is_slot_conflict_with_assistant(slot, asst1, asst_schedules):
            violations += 1
        if is_slot_conflict_with_assistant(slot, asst2, asst_schedules):
            violations += 1

    # Cek beban asisten
    load_count = defaultdict(int)
    for entry in schedule:
        for a in entry["assistant_pair"]:
            load_count[a] += 1
    for a, load in load_count.items():
        if load > max_load:
            violations += (load - max_load)

    # Cek asisten bentrok antar kelas yang berbeda
    for i in range(len(schedule)):
        for j in range(i + 1, len(schedule)):
            common = set(schedule[i]["assistant_pair"]) & set(schedule[j]["assistant_pair"])
            if common and is_overlap(schedule[i]["slot"], schedule[j]["slot"]):
                violations += 1

    # Cek kelas yang tidak terjadwalkan
    scheduled_classes = {entry["class"] for entry in schedule}
    for c in classes:
        if c not in scheduled_classes:
            violations += 1

    return violations

def calculate_cost(schedule, classes, asst_schedules, student_scheds, max_load):
    cost = 0.0

    # penalti hard constraint
    hard_violations = count_hard_violations(
        schedule, classes, asst_schedules, student_scheds, max_load
    )
    cost += PENALTY_HARD_CONSTRAINT * hard_violations

    # penalti slot malam
    night_count = sum(1 for entry in schedule if entry["slot"].get("is_night", False))
    cost += PENALTY_NIGHT_SLOT * night_count

    # penalti load imbalance
    if schedule:
        all_involved = set()
        for entry in schedule:
            for a in entry["assistant_pair"]:
                all_involved.add(a)

        if all_involved:
            loads = []
            for a in all_involved:
                load = sum(1 for entry in schedule if a in entry["assistant_pair"])
                loads.append(load)

            if len(loads) > 1:
                avg_load = sum(loads) / len(loads)
                variance = sum((l - avg_load) ** 2 for l in loads) / len(loads)
                std_dev = math.sqrt(variance)
                cost += PENALTY_LOAD_IMBALANCE * std_dev

    # penalti kelas tidak terjadwal
    scheduled_classes = {entry["class"] for entry in schedule}
    unscheduled = len(classes) - len(scheduled_classes)
    cost += PENALTY_UNSCHEDULED_CLASS * unscheduled

    return cost

def get_schedule_stats(schedule, classes, assistants, asst_schedules,
                       student_scheds, max_load):
    hard_violations = count_hard_violations(
        schedule, classes, asst_schedules, student_scheds, max_load
    )
    cost = calculate_cost(
        schedule, classes, asst_schedules, student_scheds, max_load
    )
    night_count = sum(1 for e in schedule if e["slot"].get("is_night", False))

    load_dist = defaultdict(int)
    for entry in schedule:
        for a in entry["assistant_pair"]:
            load_dist[a] += 1

    is_valid = (hard_violations == 0) and (len(schedule) == len(classes))

    return {
        "is_valid": is_valid,
        "hard_violations": hard_violations,
        "cost": cost,
        "night_slots": night_count,
        "load_distribution": dict(load_dist),
        "scheduled_count": len(schedule),
        "total_classes": len(classes),
    }
