"""Read the CSV row by row, clean each row, calculate risk, and insert into patient_encounters."""
import csv
from pathlib import Path

from calculate_risk import calculate_risk
from database_conn import get_connection

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "Diabetic_data_Selected_column.csv"
BATCH_SIZE = 1000

INSERT_SQL = """
    INSERT INTO patient_encounters
        (encounter_id, patient_nbr, age, time_in_hospital, number_inpatient,
         number_emergency, number_outpatient, num_medications, readmitted,
         risk_score, risk_level)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (encounter_id) DO NOTHING
"""

INT_FIELDS = (
    "encounter_id", "patient_nbr", "time_in_hospital", "number_inpatient",
    "number_emergency", "number_outpatient", "num_medications",
)
VALID_READMITTED = {"NO", "<30", ">30"}


def clean_row(row):
    """Trim text and convert numbers; raises ValueError for rows that can't be used."""
    clean = {k: (v or "").strip() for k, v in row.items()}
    for field in INT_FIELDS:
        clean[field] = int(clean[field])
        if clean[field] < 0:
            raise ValueError(f"{field} is negative")
    if clean["readmitted"] not in VALID_READMITTED:
        raise ValueError(f"invalid readmitted value {clean['readmitted']!r}")
    clean["age"] = clean["age"] or None
    return clean


def load_all_rows(csv_path=CSV_PATH):
    loaded = skipped = 0
    batch = []

    with get_connection() as conn, conn.cursor() as cur:
        with open(csv_path, newline="") as f:
            for line_no, raw in enumerate(csv.DictReader(f), start=2):
                try:
                    row = clean_row(raw)
                except (ValueError, TypeError) as e:
                    skipped += 1
                    print(f"Skipping line {line_no}: {e}")
                    continue

                score, level = calculate_risk(row)
                batch.append((
                    row["encounter_id"], row["patient_nbr"], row["age"],
                    row["time_in_hospital"], row["number_inpatient"],
                    row["number_emergency"], row["number_outpatient"],
                    row["num_medications"], row["readmitted"],
                    score, level.title(),
                ))
                if len(batch) >= BATCH_SIZE:
                    cur.executemany(INSERT_SQL, batch)
                    loaded += len(batch)
                    batch.clear()

        if batch:
            cur.executemany(INSERT_SQL, batch)
            loaded += len(batch)

        cur.execute("SELECT count(*) FROM patient_encounters")
        total = cur.fetchone()[0]

    print(f"Processed {loaded} rows, skipped {skipped}; patient_encounters now has {total} rows")
    return loaded


if __name__ == "__main__":
    load_all_rows()
