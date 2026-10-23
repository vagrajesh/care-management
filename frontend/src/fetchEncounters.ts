import type { Encounter, EncounterList } from './types/encounter.ts';

const API_URL = 'http://127.0.0.1:8000/encounters?limit=5';

export async function fetchEncounters(): Promise<Encounter[]> {
  const response = await fetch(API_URL);
  if (!response.ok) {
    throw new Error(`API error ${response.status}`);
  }
  const data: EncounterList = await response.json();
  console.log(JSON.stringify(data, null, 2));
  return data.items;
}

// Only run standalone under Node; the browser page imports fetchEncounters instead
if (typeof window === 'undefined') {
  const encounters: Encounter[] = await fetchEncounters();
  console.log(`Loaded ${encounters.length} encounters into the array`);
}
