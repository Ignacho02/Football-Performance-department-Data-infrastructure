import sqlite3
import pandas as pd
import glob
import os
import shutil

# ----------------------------
# Paths
# ----------------------------
DATA_FOLDER = r"C:\Users\nacho\Desktop\Portafolio\Proyectos\Proyectos\2. Flujo SQL y PowerBI. Carga física y wellness"
DONE_FOLDER = os.path.join(DATA_FOLDER, "done")
DB_FILE = os.path.join(DATA_FOLDER, "football_monitoring.db")

# Ensure 'done' folder exists
os.makedirs(DONE_FOLDER, exist_ok=True)

# ----------------------------
# Connect to database
# ----------------------------
conn = sqlite3.connect(DB_FILE)

# ----------------------------
# Load daily update CSVs
# ----------------------------
update_files = glob.glob(os.path.join(DATA_FOLDER, "*_update.csv"))
print(f"Found {len(update_files)} update files")

for file in update_files:
    print(f"Processing {file}...")

    # Skip empty files
    if os.path.getsize(file) == 0:
        print(f"Skipping empty file: {file}")
        continue

    try:
        df = pd.read_csv(file)
    except pd.errors.EmptyDataError:
        print(f"Skipping empty CSV (no columns): {file}")
        continue
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV {file}: {e}")
        continue

    table_name = os.path.basename(file).replace("_update.csv", "")
    
    try:
        df.to_sql(table_name, conn, if_exists="append", index=False)
        print(f"Appended {file} -> {table_name}")
    except Exception as e:
        print(f"Error writing to database from {file}: {e}")
        continue

    # Move processed CSV to 'done' folder
    try:
        dest = os.path.join(DONE_FOLDER, os.path.basename(file))
        shutil.move(file, dest)
        print(f"Moved {file} -> {dest}")
    except Exception as e:
        print(f"Error moving file {file} to done folder: {e}")

conn.close()
print("Database updated successfully with daily CSVs!")
