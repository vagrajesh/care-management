#// Get the first row from Diabetic_data_Seelcted_column and Turn text into typed values. encounter_id = row["encounter_id"] age = row["age"] time_in_hospital = int( row["time_in_hospital"] ) number_inpatient = int( row["number_inpatient"] ) number_emergency = int( row["number_emergency"] ) 
import csv

with open("data/Diabetic_data_selected_column.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    row = next(reader)
    encounter_id = row["encounter_id"]
    age = row["age"]
    time_in_hospital = int(row["time_in_hospital"])
    number_inpatient = int(row["number_inpatient"])
    number_emergency = int(row["number_emergency"])
