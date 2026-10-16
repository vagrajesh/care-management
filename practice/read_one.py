# //read the Diabetic_data_selected Column csv and just print one ResourceWarning
import csv

from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "Diabetic_data_Selected_column.csv"

with open(CSV_PATH, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    first_row = next(reader)
    print(first_row)


# now insert the row in database
from database_conn import get_connection

with get_connection() as conn:
    conn.execute(
        """INSERT INTO patient_encounters
           (encounter_id, patient_nbr, age, time_in_hospital, number_inpatient,
            number_emergency, number_outpatient, num_medications, readmitted,
            risk_score, risk_level)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           ON CONFLICT (encounter_id) DO NOTHING""",
        (
            int(first_row["encounter_id"]),
            int(first_row["patient_nbr"]),
            first_row["age"],
            int(first_row["time_in_hospital"]),
            int(first_row["number_inpatient"]),
            int(first_row["number_emergency"]),
            int(first_row["number_outpatient"]),
            int(first_row["num_medications"]),
            first_row["readmitted"],
            float(first_row["risk_score"]),
            first_row["risk_level"],
        ),
    )
    print(conn.execute("SELECT * FROM patient_encounters WHERE encounter_id = %s",
                       (int(first_row["encounter_id"]),)).fetchone())