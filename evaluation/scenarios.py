from data.classes import classes_full
from data.slots import all_slots
from data.assistants import assistants_full
from constraints.validators import generate_assistant_pairs, get_valid_slots


def create_scenarios():
    valid_slots = get_valid_slots(all_slots)

    print(f"[SKENARIO] Slot valid (setelah filter terlarang): {len(valid_slots)}")

    scenarios = []

    # skenario 1: mudah
    # 3 kelas, 4 asisten, semua slot valid
    easy_classes = classes_full[:3]
    easy_assistants = assistants_full[:4]
    easy_pairs = generate_assistant_pairs(easy_assistants)

    scenarios.append({
        "name": "Mudah",
        "classes": easy_classes,
        "slots": valid_slots,
        "pairs": easy_pairs,
        "assistants": easy_assistants,
        "description": f"{len(easy_classes)} kelas, {len(valid_slots)} slot, {len(easy_pairs)} pasangan",
        "bf_time_limit": 60,
        "bt_time_limit": 60,
    })

    # skenario 2: sedang
    # 6 kelas, 5 asisten
    medium_classes = classes_full[:6]
    medium_assistants = assistants_full[:5]
    medium_pairs = generate_assistant_pairs(medium_assistants)

    scenarios.append({
        "name": "Sedang",
        "classes": medium_classes,
        "slots": valid_slots,
        "pairs": medium_pairs,
        "assistants": medium_assistants,
        "description": f"{len(medium_classes)} kelas, {len(valid_slots)} slot, {len(medium_pairs)} pasangan",
        "bf_time_limit": 60,
        "bt_time_limit": 120,
    })

    # skenario 3: sulit
    # 9 kelas, 6 asisten
    hard_classes = classes_full[:9]
    hard_assistants = assistants_full
    hard_pairs = generate_assistant_pairs(hard_assistants)

    scenarios.append({
        "name": "Sulit",
        "classes": hard_classes,
        "slots": valid_slots,
        "pairs": hard_pairs,
        "assistants": hard_assistants,
        "description": f"{len(hard_classes)} kelas, {len(valid_slots)} slot, {len(hard_pairs)} pasangan",
        "bf_time_limit": 30,
        "bt_time_limit": 120,
    })

    # skenario 4: ekstrem
    # 12 kelas, 6 asisten, slot lebih terbatas
    extreme_classes = classes_full
    extreme_assistants = assistants_full
    extreme_pairs = generate_assistant_pairs(extreme_assistants)

    # Kurangi slot untuk menambah kesulitan
    extreme_slots = [s for s in valid_slots if not s["is_night"]]
    # Tambahkan kembali beberapa slot malam agar masih ada solusi
    night_slots = [s for s in valid_slots if s["is_night"]]
    extreme_slots.extend(night_slots[:2])

    scenarios.append({
        "name": "Ekstrem",
        "classes": extreme_classes,
        "slots": extreme_slots,
        "pairs": extreme_pairs,
        "assistants": extreme_assistants,
        "description": f"{len(extreme_classes)} kelas, {len(extreme_slots)} slot, {len(extreme_pairs)} pasangan",
        "bf_time_limit": 15,
        "bt_time_limit": 120,
    })

    return scenarios
