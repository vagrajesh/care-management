/** Response of GET /operations/readmission-analysis. Rates are percentages. */
export interface ReadmissionOverall {
  total_encounters: number;
  readmitted_30: number;
  readmission_30_rate: number;
}

export interface ReadmissionByLevel {
  risk_level: 'High' | 'Medium' | 'Low';
  encounters: number;
  readmitted_30: number;
  readmission_30_rate: number;
  readmitted_any: number;
  readmission_any_rate: number;
  /** readmission_30_rate divided by the overall rate */
  lift: number;
}

export interface ReadmissionCareQueue {
  queue_size: number;
  queue_readmitted_30: number;
  /** Share of all <30-day readmissions that sit in the Medium/High queue */
  queue_capture_rate: number;
  queue_readmission_30_rate: number;
  lift: number;
}

export interface ReadmissionAnalysis {
  overall: ReadmissionOverall;
  by_risk_level: ReadmissionByLevel[];
  care_queue: ReadmissionCareQueue;
}
