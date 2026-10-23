/** Shape of one item returned by GET /encounters, GET /care-queue, GET /encounters/{encounter_id} and GET /patients/{patient_nbr}/encounters. */
export interface Encounter {
  encounter_id: number;
  patient_nbr: number;
  age: string | null;
  time_in_hospital: number | null;
  number_inpatient: number | null;
  number_emergency: number | null;
  number_outpatient: number | null;
  num_medications: number | null;
  readmitted: 'NO' | '<30' | '>30' | null;
  risk_score: number | null;
  risk_level: 'Low' | 'Medium' | 'High' | null;
}

/** Response of GET /encounters?limit=5 */
export interface EncounterList {
  total: number;
  limit: number;
  offset: number;
  items: Encounter[];
}
