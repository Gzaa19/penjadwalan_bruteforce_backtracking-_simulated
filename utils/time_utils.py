def time_to_minutes(time_str):
    parts = time_str.split(":")
    hours = int(parts[0])
    minutes = int(parts[1])
    return hours * 60 + minutes


def format_slot(slot):
    night_marker = " [MALAM]" if slot.get("is_night", False) else ""
    return f"{slot['day']} {slot['start']}-{slot['end']}{night_marker}"
