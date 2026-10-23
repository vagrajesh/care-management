import type { Encounter } from './types/encounter.ts';

const API_BASE = 'http://127.0.0.1:8000';

export async function fetchEncounterById(encounterId: number): Promise<Encounter> {
  const response = await fetch(`${API_BASE}/encounters/${encounterId}`);
  if (!response.ok) {
    throw new Error(`API error ${response.status}: ${await response.text()}`);
  }
  const encounter: Encounter = await response.json();
  console.log(JSON.stringify(encounter, null, 2));
  return encounter;
}

// Only run standalone under Node; the status page imports fetchEncounterById instead
if (typeof window === 'undefined') {
  await fetchEncounterById(Number(process.argv[2] ?? 2278392));
}
