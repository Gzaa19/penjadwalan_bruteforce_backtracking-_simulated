import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['figure.max_open_warning'] = 50


def create_charts(all_results, scenarios):
    # Setup styling
    plt.style.use(
        'seaborn-v0_8-whitegrid'
        if 'seaborn-v0_8-whitegrid' in plt.style.available
        else 'ggplot'
    )
    colors = {
        "Brute Force": "#e74c3c",        # Merah
        "Backtracking": "#3498db",        # Biru
        "Simulated Annealing": "#2ecc71", # Hijau
    }

    algorithms = ["Brute Force", "Backtracking", "Simulated Annealing"]
    scenario_names = [sc["name"] for sc in scenarios]

    # Organisasi data
    data = {algo: {"time": [], "cost": [], "explored": []}
            for algo in algorithms}

    for result in all_results:
        algo = result["algorithm"]
        data[algo]["time"].append(result["time"])
        cost_val = result["cost"] if result["cost"] != float('inf') else 0
        data[algo]["cost"].append(cost_val)
        data[algo]["explored"].append(result["explored"])

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Perbandingan Performa Algoritma Penjadwalan ALPRO",
                 fontsize=16, fontweight='bold', y=1.02)

    x = range(len(scenario_names))
    bar_width = 0.25

    # grafik 1: waktu eksekusi
    ax1 = axes[0, 0]
    for i, algo in enumerate(algorithms):
        offset = (i - 1) * bar_width
        bars = ax1.bar([xi + offset for xi in x], data[algo]["time"],
                       bar_width, label=algo, color=colors[algo], alpha=0.85,
                       edgecolor='white', linewidth=0.5)
        for bar_item in bars:
            height = bar_item.get_height()
            if height > 0:
                ax1.text(bar_item.get_x() + bar_item.get_width() / 2., height,
                         f'{height:.2f}s',
                         ha='center', va='bottom', fontsize=7)

    ax1.set_xlabel("Skenario", fontsize=11)
    ax1.set_ylabel("Waktu (detik)", fontsize=11)
    ax1.set_title("Waktu Eksekusi per Algoritma", fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(scenario_names)
    ax1.legend(fontsize=9)
    ax1.set_yscale('log')
    ax1.grid(axis='y', alpha=0.3)

    # grafik 2: cost
    ax2 = axes[0, 1]
    for i, algo in enumerate(algorithms):
        offset = (i - 1) * bar_width
        bars = ax2.bar([xi + offset for xi in x], data[algo]["cost"],
                       bar_width, label=algo, color=colors[algo], alpha=0.85,
                       edgecolor='white', linewidth=0.5)
        for bar_item in bars:
            height = bar_item.get_height()
            if height > 0:
                ax2.text(bar_item.get_x() + bar_item.get_width() / 2., height,
                         f'{height:.0f}',
                         ha='center', va='bottom', fontsize=7)

    ax2.set_xlabel("Skenario", fontsize=11)
    ax2.set_ylabel("Cost (Objective Function)", fontsize=11)
    ax2.set_title("Nilai Cost per Algoritma", fontsize=13, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(scenario_names)
    ax2.legend(fontsize=9)
    ax2.grid(axis='y', alpha=0.3)

    # grafik 3: jumlah konfigurasi dieksplorasi
    ax3 = axes[1, 0]
    for i, algo in enumerate(algorithms):
        offset = (i - 1) * bar_width
        bars = ax3.bar([xi + offset for xi in x], data[algo]["explored"],
                       bar_width, label=algo, color=colors[algo], alpha=0.85,
                       edgecolor='white', linewidth=0.5)

    ax3.set_xlabel("Skenario", fontsize=11)
    ax3.set_ylabel("Jumlah Konfigurasi", fontsize=11)
    ax3.set_title("Konfigurasi yang Dieksplorasi", fontsize=13, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(scenario_names)
    ax3.legend(fontsize=9)
    ax3.set_yscale('log')
    ax3.grid(axis='y', alpha=0.3)

    # grafik 4: konvergensi SA
    ax4 = axes[1, 1]
    sa_results = [r for r in all_results if r["algorithm"] == "Simulated Annealing"]

    sa_colors = ['#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
    for idx, sa_r in enumerate(sa_results):
        if "cost_history" in sa_r and sa_r["cost_history"]:
            iterations_axis = [i * 100 for i in range(len(sa_r["cost_history"]))]
            color = sa_colors[idx % len(sa_colors)]
            ax4.plot(iterations_axis, sa_r["cost_history"],
                     label=f"SA - {sa_r['scenario']}",
                     color=color, linewidth=1.5, alpha=0.8)

    ax4.set_xlabel("Iterasi", fontsize=11)
    ax4.set_ylabel("Best Cost", fontsize=11)
    ax4.set_title("Konvergensi Simulated Annealing", fontsize=13, fontweight='bold')
    ax4.legend(fontsize=9)
    ax4.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("grafik_perbandingan_algoritma.png", dpi=150, bbox_inches='tight')
    plt.show()

    print("\n[GRAFIK] Grafik disimpan sebagai 'grafik_perbandingan_algoritma.png'")

    # grafik 5: perbandingan slot malam
    fig2, ax5 = plt.subplots(figsize=(10, 5))

    night_data = {algo: [] for algo in algorithms}
    for result in all_results:
        algo = result["algorithm"]
        night_data[algo].append(result["stats"]["night_slots"])

    for i, algo in enumerate(algorithms):
        offset = (i - 1) * bar_width
        ax5.bar([xi + offset for xi in x], night_data[algo],
                bar_width, label=algo, color=colors[algo], alpha=0.85,
                edgecolor='white', linewidth=0.5)

    ax5.set_xlabel("Skenario", fontsize=11)
    ax5.set_ylabel("Jumlah Slot Malam", fontsize=11)
    ax5.set_title("Penggunaan Slot Malam per Algoritma",
                  fontsize=13, fontweight='bold')
    ax5.set_xticks(x)
    ax5.set_xticklabels(scenario_names)
    ax5.legend(fontsize=9)
    ax5.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig("grafik_slot_malam.png", dpi=150, bbox_inches='tight')
    plt.show()

    print("[GRAFIK] Grafik slot malam disimpan sebagai 'grafik_slot_malam.png'")
