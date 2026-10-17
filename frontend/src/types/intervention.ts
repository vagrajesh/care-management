/** Request body for PATCH /interventions/{encounter_id}. All fields are optional. */
export interface InterventionUpdate {
  status?: 'Open' | 'Contacted' | 'In Progress' | 'Completed' | 'Cancelled' | string;
  assigned_to?: string | null;
  notes?: string | null;
}

/** Response of PATCH /interventions/{encounter_id}. */
export interface Intervention {
  intervention_id: number;
  encounter_id: number;
  status: string;
  assigned_to: string | null;
  notes: string | null;
}
