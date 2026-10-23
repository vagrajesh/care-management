/** Status values stored in care_interventions (the API also accepts them case-insensitively). */
export const INTERVENTION_STATUSES = ['Open', 'Contacted', 'In Progress', 'Completed', 'Cancelled'] as const;
export type InterventionStatus = (typeof INTERVENTION_STATUSES)[number];

/** Request body for PATCH /interventions/{encounter_id}. All fields are optional. */
export interface InterventionUpdate {
  status?: InterventionStatus | string;
  assigned_to?: string | null;
  notes?: string | null;
}

/** Response of GET /interventions/{encounter_id} and PATCH /interventions/{encounter_id}. */
export interface Intervention {
  intervention_id: number;
  encounter_id: number;
  status: InterventionStatus;
  assigned_to: string | null;
  notes: string | null;
}
