import pandas as pd

from utils.time_utils import time_to_minutes, format_slot


def print_schedule(schedule, title=""):
    if title:
        print(f"\n  {title}")

    if not schedule:
        print("  [Tidak ada jadwal yang ditemukan]")
        return

    # Urutkan berdasarkan hari dan waktu
    day_order = {"Senin": 0, "Selasa": 1, "Rabu": 2, "Kamis": 3, "Jumat": 4}
    sorted_schedule = sorted(
        schedule,
        key=lambda e: (day_order.get(e["slot"]["day"], 99),
                       time_to_minutes(e["slot"]["start"])),
    )

    for entry in sorted_schedule:
        slot_str = format_slot(entry["slot"])
        pair_str = f"{entry['assistant_pair'][0]} & {entry['assistant_pair'][1]}"
        print(f"  {entry['class']:<12} | {slot_str:<30} | {pair_str}")


def display_results_table(all_results):
    rows = []

    for result in all_results:
        stats = result["stats"]

        rows.append({
            "Skenario": result["scenario"],
            "Algoritma": result["algorithm"],
            "Jadwal Valid": "✓ Ya" if stats["is_valid"] else "✗ Tidak",
            "Pelanggaran HC": stats["hard_violations"],
            "Cost": f"{result['cost']:.2f}" if result['cost'] != float('inf') else "∞",
            "Konfigurasi Dieksplorasi": f"{result['explored']:,}",
            "Waktu (detik)": f"{result['time']:.4f}",
            "Slot Malam": stats["night_slots"],
            "Kelas Terjadwal": f"{stats['scheduled_count']}/{stats['total_classes']}",
        })

    df = pd.DataFrame(rows)

    print("\nTABEL HASIL PERBANDINGAN ALGORITMA")
    print()

    # Tampilkan per skenario
    for scenario_name in df["Skenario"].unique():
        print(f"\nSkenario: {scenario_name}")
        scenario_df = df[df["Skenario"] == scenario_name]
        print(scenario_df.to_string(index=False))
        print()

    # Tabel ringkasan lengkap
    print("\nTabel Lengkap")
    print(df.to_string(index=False))

    # Tabel distribusi beban
    print("\n\nDISTRIBUSI BEBAN ASISTEN")

    for result in all_results:
        stats = result["stats"]
        if stats["load_distribution"]:
            print(f"\n{result['scenario']} - {result['algorithm']}:")
            for asst, load in sorted(stats["load_distribution"].items()):
                bar = "█" * load
                print(f"  {asst:<12}: {load} kelas {bar}")

    return df
