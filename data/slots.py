# Hari yang tersedia untuk penjadwalan praktikum
days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]

# Rentang waktu yang tersedia
# Format: (jam_mulai, jam_selesai, apakah_slot_malam)
time_ranges = [
    ("07:00", "09:40", False),   # Pagi awal (akan dilarang Sen-Rab)
    ("08:00", "10:00", False),   # Pagi
    ("10:00", "12:00", False),   # Siang awal
    ("13:00", "15:00", False),   # Siang
    ("15:40", "17:40", False),   # Sore
    ("18:15", "20:15", True),    # Malam (penalti)
]

def build_all_slots():
    slots = []
    slot_id = 0
    for day in days:
        for start, end, is_night in time_ranges:
            slots.append({
                "id": slot_id,
                "day": day,
                "start": start,
                "end": end,
                "is_night": is_night,
            })
            slot_id += 1
    return slots

# Daftar semua slot waktu (30 slot total: 5 hari × 6 rentang waktu)
all_slots = build_all_slots()
