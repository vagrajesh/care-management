import type { Encounter } from './types/encounter.ts';

const encounterId = process.argv[2] ?? '2278392';
const API_URL = `http://127.0.0.1:8000/encounters/${encounterId}`;

const response = await fetch(API_URL);
if (!response.ok) {
  throw new Error(`API error ${response.status}: ${await response.text()}`);
}

const encounter: Encounter = await response.json();
console.log(JSON.stringify(encounter, null, 2));
