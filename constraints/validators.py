import itertools
from utils.time_utils import time_to_minutes

def is_overlap(slot1, slot2):
    if slot1["day"] != slot2["day"]:
        return False

    start1 = time_to_minutes(slot1["start"])
    end1 = time_to_minutes(slot1["end"])
    start2 = time_to_minutes(slot2["start"])
    end2 = time_to_minutes(slot2["end"])

    return start1 < end2 and start2 < end1

def is_forbidden_slot(slot):
    forbidden_days = ["Senin", "Selasa", "Rabu"]
    if slot["day"] in forbidden_days:
        start = time_to_minutes(slot["start"])
        end = time_to_minutes(slot["end"])

        forbidden_start = time_to_minutes("07:00")
        forbidden_end = time_to_minutes("09:40")

        # Cek irisan dengan rentang terlarang
        if start < forbidden_end and forbidden_start < end:
            return True
    return False

def generate_assistant_pairs(assistants):
    return list(itertools.combinations(assistants, 2))

def get_valid_slots(all_slots):
    return [s for s in all_slots if not is_forbidden_slot(s)]

def is_slot_conflict_with_students(slot, student_scheds):
    for sched in student_scheds:
        if is_overlap(slot, sched):
            return True
    return False

def is_slot_conflict_with_assistant(slot, assistant_name, asst_schedules):
    if assistant_name not in asst_schedules:
        return False
    for sched in asst_schedules[assistant_name]:
        if is_overlap(slot, sched):
            return True
    return False

def count_assistant_load(assistant_name, current_schedule):
    count = 0
    for entry in current_schedule:
        pair = entry["assistant_pair"]
        if assistant_name in pair:
            count += 1
    return count

def is_assistant_slot_conflict(slot, assistant_name, current_schedule):
    for entry in current_schedule:
        if assistant_name in entry["assistant_pair"]:
            if is_overlap(slot, entry["slot"]):
                return True
    return False

def is_valid_assignment(class_name, slot, assistant_pair, current_schedule,
                         asst_schedules, student_scheds, max_load):
    # slot terlarang
    if is_forbidden_slot(slot):
        return False

    # bentrok jadwal praktikan
    if is_slot_conflict_with_students(slot, student_scheds):
        return False

    # bentrok kuliah asisten
    asst1, asst2 = assistant_pair
    if is_slot_conflict_with_assistant(slot, asst1, asst_schedules):
        return False
    if is_slot_conflict_with_assistant(slot, asst2, asst_schedules):
        return False

    # batas beban
    load1 = count_assistant_load(asst1, current_schedule)
    load2 = count_assistant_load(asst2, current_schedule)
    if load1 >= max_load or load2 >= max_load:
        return False

    # kelas sudah dijadwalkan
    for entry in current_schedule:
        if entry["class"] == class_name:
            return False

    # asisten bentrok di waktu sama
    if is_assistant_slot_conflict(slot, asst1, current_schedule):
        return False
    if is_assistant_slot_conflict(slot, asst2, current_schedule):
        return False

    return True
