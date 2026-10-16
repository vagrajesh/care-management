import csv
import sys
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "Diabetic_data_Selected_column.csv"


def calculate_risk(row):
    score = 0
    if int(row["number_inpatient"]) >= 3:
        score += 3
    if int(row["number_emergency"]) >= 2:
        score += 2
    if int(row["number_outpatient"]) >= 3:
        score += 1
    if int(row["time_in_hospital"]) >= 7:
        score += 1
    if int(row["num_medications"]) >= 20:
        score += 1

    if score >= 5:
        level = "HIGH"
    elif score >= 3:
        level = "MEDIUM"
    else:
        level = "LOW"
    return score, level


def main():
    # Optional argument: patient_nbr; defaults to the first patient in the file
    patient_nbr = sys.argv[1] if len(sys.argv) > 1 else None

    with open(CSV_PATH, newline="") as f:
        for row in csv.DictReader(f):
            if patient_nbr is None:
                patient_nbr = row["patient_nbr"]
            if row["patient_nbr"] != patient_nbr:
                continue
            score, level = calculate_risk(row)
            print(f"patient_nbr={patient_nbr} encounter_id={row['encounter_id']} "
                  f"inpatient={row['number_inpatient']} emergency={row['number_emergency']} "
                  f"outpatient={row['number_outpatient']} days={row['time_in_hospital']} "
                  f"meds={row['num_medications']} -> score={score} risk={level}")


if __name__ == "__main__":
    main()
