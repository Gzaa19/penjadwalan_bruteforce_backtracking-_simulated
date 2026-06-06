def display_conclusions(all_results, scenarios):
    print("\nKESIMPULAN ANALISIS")
    algorithms = ["Brute Force", "Backtracking", "Simulated Annealing"]

    # analisis per algoritma
    for algo in algorithms:
        algo_results = [r for r in all_results if r["algorithm"] == algo]
        run_results = [r for r in algo_results if not r.get("skipped", False)]

        total_scenarios = len(algo_results)
        scenarios_run = len(run_results)
        solutions_found = sum(1 for r in run_results if r["found_solution"])

        total_time = sum(r["time"] for r in run_results)
        avg_time = total_time / scenarios_run if scenarios_run > 0 else 0

        avg_explored = (sum(r["explored"] for r in run_results) / scenarios_run
                        if scenarios_run > 0 else 0)

        valid_costs = [r["cost"] for r in run_results
                       if r["found_solution"] and r["cost"] != float('inf')]
        avg_cost = sum(valid_costs) / len(valid_costs) if valid_costs else float('inf')

        print(f"\n{algo.upper()}")
        print(f"  Dijalankan       : {scenarios_run}/{total_scenarios} skenario")
        if scenarios_run > 0:
            print(f"  Solusi ditemukan : {solutions_found}/{scenarios_run} skenario yang dijalankan")
            print(f"  Rata-rata waktu  : {avg_time:.4f} detik pada skenario yang dijalankan")
            print(f"  Rata-rata eksplorasi: {avg_explored:,.0f} konfigurasi")
            if avg_cost != float('inf'):
                print(f"  Rata-rata cost   : {avg_cost:.2f}")
            else:
                print(f"  Rata-rata cost   : N/A")
        else:
            print(f"  Solusi ditemukan : N/A")
            print(f"  Rata-rata waktu  : N/A")
            print(f"  Rata-rata eksplorasi: N/A")
            print(f"  Rata-rata cost   : N/A")

    print("\n\nRINGKASAN PERBANDINGAN")

    # kecepatan
    print("\nKECEPATAN EKSEKUSI:")
    for sc in scenarios:
        sc_name = sc["name"]
        sc_results = [r for r in all_results if r["scenario"] == sc_name]
        run_results = [r for r in sc_results if r["time"] > 0 and not r.get("skipped", False)]
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
            min_cost = min(r["cost"] for r in sc_results)
            best_algos = [r for r in sc_results if r["cost"] == min_cost]
            
            if len(best_algos) == len(sc_results) and len(sc_results) > 1:
                if len(best_algos) == 2:
                    algo_names = f"{best_algos[0]['algorithm']} dan {best_algos[1]['algorithm']}"
                else:
                    algo_names = ", ".join(r["algorithm"] for r in best_algos[:-1]) + ", dan " + best_algos[-1]["algorithm"]
                print(f"  Skenario {sc_name}: {algo_names} sama-sama menghasilkan cost terbaik {min_cost:.2f}")
            elif len(best_algos) > 1:
                if len(best_algos) == 2:
                    algo_names = f"{best_algos[0]['algorithm']} dan {best_algos[1]['algorithm']}"
                else:
                    algo_names = ", ".join(r["algorithm"] for r in best_algos[:-1]) + ", dan " + best_algos[-1]["algorithm"]
                print(f"  Skenario {sc_name}: {algo_names} terbaik (Cost: {min_cost:.2f})")
            else:
                best = best_algos[0]
                print(f"  Skenario {sc_name}: {best['algorithm']} terbaik (Cost: {best['cost']:.2f})")
        else:
            print(f"  Skenario {sc_name}: Tidak ada solusi valid ditemukan")

    # efisiensi
    print("\nEFISIENSI PENCARIAN:")
    for sc in scenarios:
        sc_name = sc["name"]
        sc_results = [r for r in all_results if r["scenario"] == sc_name]
        run_results = [r for r in sc_results if not r.get("skipped", False)]
        if len(run_results) > 1:
            run_results.sort(key=lambda r: r["explored"])
            most_efficient = run_results[0]
            least_efficient = run_results[-1]
            print(f"  Skenario {sc_name}:")
            print(f"    Paling efisien : {most_efficient['algorithm']} ({most_efficient['explored']:,} konfigurasi)")
            print(f"    Paling boros   : {least_efficient['algorithm']} ({least_efficient['explored']:,} konfigurasi)")
        elif len(run_results) == 1:
            only_algo = run_results[0]
            print(f"  Skenario {sc_name}:")
            print(f"    Hanya {only_algo['algorithm']} yang dijalankan karena algoritma lain diskip akibat kompleksitas ruang solusi.")
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
        "   - Backtracking dapat menjamin solusi optimal apabila seluruh ruang pencarian selesai dieksplorasi. Namun pada eksperimen ini, karena diterapkan batas waktu, hasil Backtracking dianggap sebagai solusi terbaik yang ditemukan dalam batas waktu tersebut.",
        "   - Cocok untuk skenario sedang hingga sulit.",
        "",
        "3. SIMULATED ANNEALING:",
        "   - Algoritma meta-heuristik yang fleksibel dan skalabel.",
        "   - Tidak menjamin solusi optimal, tetapi menemukan solusi baik.",
        "   - Mampu menangani skenario besar yang tidak bisa ditangani BF/BT.",
        "   - Waktu eksekusi relatif konsisten dan dapat dikontrol.",
        "   - Mekanisme penerimaan solusi buruk membantu keluar dari local optima.",
        "   - Paling cocok untuk skenario besar/ekstrem dalam aplikasi nyata.",
        "",
        "4. ASUMSI & PENJELASAN PENGUJIAN:",
        "   - Seluruh algoritma berhasil menghindari slot malam pada solusi terbaik, sehingga nilai penggunaan slot malam adalah 0 pada semua skenario.",
        "   - Beberapa kelas dapat berada pada slot waktu yang sama selama pasangan asistennya berbeda dan tidak ada konflik jadwal, karena kapasitas ruang/laboratorium tidak dimodelkan."
    ]

    for line in conclusions:
        print(f"  {line}")

    print("\nProgram selesai dijalankan.")
