import type { Intervention } from './types/intervention.ts';

const API_BASE = 'http://127.0.0.1:8000';

/** Latest intervention for the encounter, or null when none has been recorded yet (404). */
export async function fetchIntervention(encounterId: number): Promise<Intervention | null> {
  const response = await fetch(`${API_BASE}/interventions/${encounterId}`);
  if (response.status === 404) {
    return null;
  }
  if (!response.ok) {
    throw new Error(`API error ${response.status}: ${await response.text()}`);
  }
  const data: Intervention = await response.json();
  console.log(JSON.stringify(data, null, 2));
  return data;
}

// Only run standalone under Node; the browser pages import fetchIntervention instead
if (typeof window === 'undefined') {
  const encounterId = Number(process.argv[2] ?? 35754);
  const intervention = await fetchIntervention(encounterId);
  const interventions: Intervention[] = intervention ? [intervention] : [];
  console.log(`Interventions array holds ${interventions.length} item(s) for encounter ${encounterId}`);
}
