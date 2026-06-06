def display_conclusions(all_results, scenarios):
    print("\nKESIMPULAN ANALISIS")
    algorithms = ["Brute Force", "Backtracking", "Simulated Annealing"]

    # analisis per algoritma
    for algo in algorithms:
        algo_results = [r for r in all_results if r["algorithm"] == algo]

        total_time = sum(r["time"] for r in algo_results)
        avg_time = total_time / len(algo_results) if algo_results else 0
        solutions_found = sum(1 for r in algo_results if r["found_solution"])
        total_scenarios = len(algo_results)

        avg_explored = (sum(r["explored"] for r in algo_results) / len(algo_results)
                        if algo_results else 0)

        valid_costs = [r["cost"] for r in algo_results
                       if r["found_solution"] and r["cost"] != float('inf')]
        avg_cost = sum(valid_costs) / len(valid_costs) if valid_costs else float('inf')

        print(f"\n{algo.upper()}")
        print(f"  Solusi ditemukan : {solutions_found}/{total_scenarios} skenario")
        print(f"  Rata-rata waktu  : {avg_time:.4f} detik")
        print(f"  Rata-rata eksplorasi: {avg_explored:,.0f} konfigurasi")
        if avg_cost != float('inf'):
            print(f"  Rata-rata cost   : {avg_cost:.2f}")
        else:
            print(f"  Rata-rata cost   : N/A")

    print("\n\nRINGKASAN PERBANDINGAN")

    # kecepatan
    print("\nKECEPATAN EKSEKUSI:")
    for sc in scenarios:
        sc_name = sc["name"]
        sc_results = [r for r in all_results if r["scenario"] == sc_name]
        run_results = [r for r in sc_results if r["time"] > 0]
        if run_results:
            run_results.sort(key=lambda r: r["time"])
            fastest = run_results[0]
            print(f"  Skenario {sc_name}: {fastest['algorithm']} tercepat ({fastest['time']:.4f}s)")
        else:
            print(f"  Skenario {sc_name}: N/A")

    # kualitas solusi
    print("\nKUALITAS SOLUSI (COST TERENDAH):")
    for sc in scenarios:
        sc_name = sc["name"]
        sc_results = [r for r in all_results if r["scenario"] == sc_name
                      and r["found_solution"]]
        if sc_results:
            sc_results.sort(key=lambda r: r["cost"])
            best = sc_results[0]
            print(f"  Skenario {sc_name}: {best['algorithm']} terbaik (Cost: {best['cost']:.2f})")
        else:
            print(f"  Skenario {sc_name}: Tidak ada solusi valid ditemukan")

    # efisiensi
    print("\nEFISIENSI PENCARIAN:")
    for sc in scenarios:
        sc_name = sc["name"]
        sc_results = [r for r in all_results if r["scenario"] == sc_name]
        run_results = [r for r in sc_results if r["explored"] > 0]
        if run_results:
            run_results.sort(key=lambda r: r["explored"])
            most_efficient = run_results[0]
            least_efficient = run_results[-1]
            print(f"  Skenario {sc_name}:")
            print(f"    Paling efisien : {most_efficient['algorithm']} ({most_efficient['explored']:,} konfigurasi)")
            print(f"    Paling boros   : {least_efficient['algorithm']} ({least_efficient['explored']:,} konfigurasi)")
        else:
            print(f"  Skenario {sc_name}: N/A")

    print("\n\nKESIMPULAN AKHIR")

    conclusions = [
        "1. BRUTE FORCE:",
        "   - Mengeksplorasi seluruh ruang solusi secara exhaustive.",
        "   - Menjamin solusi optimal jika waktu tidak dibatasi.",
        "   - Sangat lambat untuk skenario besar (kompleksitas eksponensial).",
        "   - Hanya praktis untuk skenario kecil (≤ 3 kelas).",
        "",
        "2. BACKTRACKING:",
        "   - Lebih efisien daripada brute force berkat mekanisme pruning.",
        "   - Memotong cabang pencarian yang pasti melanggar constraint.",
        "   - Jumlah konfigurasi yang dieksplorasi jauh lebih sedikit.",
        "   - Masih menjamin solusi optimal dalam ruang yang dipangkas.",
        "   - Cocok untuk skenario sedang hingga sulit.",
        "",
        "3. SIMULATED ANNEALING:",
        "   - Algoritma meta-heuristik yang fleksibel dan skalabel.",
        "   - Tidak menjamin solusi optimal, tetapi menemukan solusi baik.",
        "   - Mampu menangani skenario besar yang tidak bisa ditangani BF/BT.",
        "   - Waktu eksekusi relatif konsisten dan dapat dikontrol.",
        "   - Mekanisme penerimaan solusi buruk membantu keluar dari local optima.",
        "   - Paling cocok untuk skenario besar/ekstrem dalam aplikasi nyata.",
    ]

    for line in conclusions:
        print(f"  {line}")

    print("\nProgram selesai dijalankan.")
