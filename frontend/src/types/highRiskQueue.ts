/** One item returned by GET /care-queue/high. */
export interface HighRiskQueueItem {
  encounter_id: number;
  patient_nbr: number;
  age: string | null;
  readmitted: 'NO' | '<30' | '>30' | null;
  risk_score: number | null;
  risk_level: 'High' | null;
}

/** Response of GET /care-queue/high */
export interface HighRiskQueue {
  total: number;
  limit: number;
  offset: number;
  items: HighRiskQueueItem[];
}
