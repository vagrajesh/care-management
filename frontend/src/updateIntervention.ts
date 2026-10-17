import type { Intervention, InterventionUpdate } from './types/intervention.ts';

const ENCOUNTER_ID = 35754;
const API_URL = `http://127.0.0.1:8000/interventions/${ENCOUNTER_ID}`;

const body: InterventionUpdate = {
  status: 'CONTACTED',
  assigned_to: 'Care Team A',
  notes: 'Follow-up initiated',
};

async function updateIntervention(): Promise<Intervention> {
  const response = await fetch(API_URL, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await response.json();
  console.log(JSON.stringify(data, null, 2));
  if (!response.ok) {
    throw new Error(`API error ${response.status}`);
  }
  return data as Intervention;
}

const interventions: Intervention[] = [];
interventions.push(await updateIntervention());
console.log(`Interventions array holds ${interventions.length} item(s)`);
