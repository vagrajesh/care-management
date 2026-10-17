/** Response of GET /operations/summary. */
export interface OperationsSummary {
  total_encounters: number;
  high_risk: number;
  medium_risk: number;
  pending_reviews: number;
}
