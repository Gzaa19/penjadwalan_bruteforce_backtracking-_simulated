import random
import sys
import os

# Tambahkan root project ke path agar import berjalan di semua environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import RANDOM_SEED, MAX_LOAD
from data.classes import classes_full
from data.slots import all_slots
from data.assistants import assistants_full
from evaluation.runner import run_experiments
from evaluation.display import display_results_table
from evaluation.charts import create_charts
from evaluation.conclusions import display_conclusions

def main():
    random.seed(RANDOM_SEED)

    print("SISTEM PENJADWALAN ULANG PRAKTIKUM ALPRO")
    print("Perbandingan Brute Force, Backtracking, & Simulated Annealing")
    print()

    # informasi data
    print(f"[DATA] Total slot waktu yang dibuat: {len(all_slots)}")
    print(f"[DATA] Jumlah kelas praktikum ALPRO: {len(classes_full)}")
    print(f"[DATA] Jumlah asisten: {len(assistants_full)}")
    print(f"[DATA] Batas beban per asisten: {MAX_LOAD}")
    print()

    # jalankan eksperimen
    all_results, scenarios = run_experiments()

    # tampilkan hasil
    results_df = display_results_table(all_results)

    # buat chart grafik
    create_charts(all_results, scenarios)

    # tampilkan kesimpulan
    display_conclusions(all_results, scenarios)

    # simpan ke csv
    results_df.to_csv("hasil_perbandingan_algoritma.csv", index=False)
    print("\n[OUTPUT] Hasil disimpan ke 'hasil_perbandingan_algoritma.csv'")

if __name__ == "__main__":
    main()
