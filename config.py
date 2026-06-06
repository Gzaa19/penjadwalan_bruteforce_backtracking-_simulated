# Batas beban asisten
# Setiap asisten tidak boleh mengampu lebih dari MAX_LOAD kelas praktikum.
MAX_LOAD = 4

# Bobot penalti untuk objective function
PENALTY_HARD_CONSTRAINT = 10000
PENALTY_NIGHT_SLOT = 50
PENALTY_LOAD_IMBALANCE = 30
PENALTY_UNSCHEDULED_CLASS = 5000

# Parameter Simulated Annealing
SA_INITIAL_TEMP = 1000.0
SA_COOLING_RATE = 0.995
SA_MIN_TEMP = 0.01
SA_MAX_ITERATIONS = 50000

# Seed untuk acak
RANDOM_SEED = 42
