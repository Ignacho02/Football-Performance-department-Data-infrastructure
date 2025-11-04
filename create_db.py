import sqlite3
import pandas as pd
import os

# ----------------------------
# Paths
# ----------------------------
DATA_FOLDER = r"C:\Users\nacho\Desktop\Portafolio\Proyectos\Proyectos\2. Flujo SQL y PowerBI. Carga física y wellness"
DB_FILE = os.path.join(DATA_FOLDER, "football_monitoring.db")

# ----------------------------
# Connect or create database
# ----------------------------
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# ----------------------------
# Create tables
# ----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    name TEXT,
    position TEXT,
    age INTEGER,
    height_cm INTEGER,
    weight_kg INTEGER,
    team TEXT,
    dominant_leg TEXT,
    historical_max_speed_kmh REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS session_metrics (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    day_label TEXT,
    session_type TEXT,
    player_id INTEGER,
    team TEXT,
    duration_min INTEGER,
    total_distance_m REAL,
    high_speed_distance_m REAL,
    sprint_distance_m REAL,
    max_speed_kmh REAL,
    perc_max_speed REAL,
    distance_at_max_speed_m REAL,
    rpe REAL,
    hr_mean REAL,
    hr_zone_1_min INTEGER,
    hr_zone_2_min INTEGER,
    hr_zone_3_min INTEGER,
    hr_zone_4_min INTEGER,
    hr_zone_5_min INTEGER,
    internal_load_rpe REAL,
    internal_load_hr REAL,
    FOREIGN KEY(player_id) REFERENCES players(player_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS wellness (
    wellness_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    player_id INTEGER,
    sleep_quality REAL,
    fatigue REAL,
    muscle_soreness REAL,
    stress REAL,
    motivation REAL,
    FOREIGN KEY(player_id) REFERENCES players(player_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS fitness_tests (
    test_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    test_date TEXT,
    test_type TEXT,
    attempt1 REAL,
    attempt2 REAL,
    attempt3 REAL,
    FOREIGN KEY(player_id) REFERENCES players(player_id)
)
""")

conn.commit()

# ----------------------------
# Load historical CSVs (replace tables)
# ----------------------------
historical_files = ["players.csv", "session_metrics.csv", "wellness.csv", "fitness_tests.csv"]

for file in historical_files:
    path = os.path.join(DATA_FOLDER, file)
    if os.path.exists(path):
        df = pd.read_csv(path)
        table_name = file.replace(".csv","")
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Loaded {file} -> {table_name}")
    else:
        print(f"Warning: {file} not found in {DATA_FOLDER}")

conn.close()
print("Database created successfully from historical CSVs!")
