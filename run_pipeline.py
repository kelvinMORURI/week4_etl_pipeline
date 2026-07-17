import os
import logging
import sqlite3
import great_expectations as gx

import pandas as pd
from dotenv import load_dotenv

# ===============================
# Load Environment Variables
# ===============================
load_dotenv()

DATA_PATH = os.getenv("DATA_PATH")
DB_PATH = os.getenv("DB_PATH")

TEMP_MAX = float(os.getenv("TEMP_MAX"))
PRESSURE_MIN = float(os.getenv("PRESSURE_MIN"))

# ===============================
# Logging Configuration
# ===============================
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)


# ===============================
# Extract
# ===============================
def extract():

    logging.info("Starting extraction...")

    df = pd.read_csv(DATA_PATH)

    logging.info(f"Extracted {len(df)} rows.")

    return df


# ===============================
# Transform
# ===============================
def transform(df):

    logging.info("Starting transformation...")

    original_rows = len(df)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Remove invalid pressure
    df = df[df["Pressure_PSI"] >= PRESSURE_MIN]

    # Remove invalid temperature
    df = df[df["Temperature_C"] <= TEMP_MAX]

    logging.info(
        f"Transformation complete. Rows before: {original_rows}, Rows after: {len(df)}"
    )

    # Remove rows with missing Zone
    df = df.dropna(subset=["Zone"])

    # Remove rows with invalid Flow Rate
    df = df[df["Flow_Rate_LPM"] > 0]

    return df


def validate(df):

    logging.info("Starting validation...")

    checks = [
        ("No null timestamps", df["timestamp"].notnull().all()),
        ("Pressure >= 0", (df["Pressure_PSI"] >= 0).all()),
        ("Temperature <= TEMP_MAX", (df["Temperature_C"] <= TEMP_MAX).all()),
        ("No null Zone", df["Zone"].notnull().all()),
        ("Flow Rate > 0", (df["Flow_Rate_LPM"] > 0).all()),
    ]

    failed = []

    for name, result in checks:
        print(f"{name}: {'PASS' if result else 'FAIL'}")
        if not result:
            failed.append(name)

    if failed:
        logging.error(f"Validation failed: {failed}")
        raise Exception(f"Pipeline stopped. Failed checks: {failed}")

    logging.info("Validation passed.")
    print("\n✅ Validation Passed")


def load(df):

    logging.info("Starting load process...")

    # Create database folder if it doesn't exist
    os.makedirs("data/database", exist_ok=True)

    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)

    # Idempotency: replace the table every run
    df.to_sql(
        "sensor_data",
        conn,
        if_exists="replace",
        index=False
    )

    conn.commit()
    conn.close()

    logging.info(f"Loaded {len(df)} rows into SQLite database.")

    print("✅ Data loaded successfully into SQLite.")
# ===============================
# Main
# ===============================
if __name__ == "__main__":

    print("Pipeline started...")

    df = extract()

    df = transform(df)

    validate(df)

    load(df)

    print(df.head())

    print(f"\nRows after cleaning: {len(df)}")

    print("Pipeline finished.")
