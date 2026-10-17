import type { Encounter, EncounterList } from './encounter.ts';

/** One patient in the care queue (risk level Medium or High). */
export interface CareQueueItem extends Encounter {
  risk_level: 'Medium' | 'High';
}

/** Response of GET /care-queue (High risk first, then by risk_score). */
export interface CareQueue extends Omit<EncounterList, 'items'> {
  items: CareQueueItem[];
}
