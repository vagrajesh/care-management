import type { Intervention, InterventionUpdate } from './types/intervention.ts';

const API_BASE = 'http://127.0.0.1:8000';

export async function updateIntervention(encounterId: number, body: InterventionUpdate): Promise<Intervention> {
  const response = await fetch(`${API_BASE}/interventions/${encounterId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await response.json();
  console.log(JSON.stringify(data, null, 2));
  if (!response.ok) {
    throw new Error(`API error ${response.status}: ${JSON.stringify(data.detail ?? data)}`);
  }
  return data as Intervention;
}

// Only run standalone under Node; the status page imports updateIntervention instead
if (typeof window === 'undefined') {
  const encounterId = Number(process.argv[2] ?? 35754);
  const body: InterventionUpdate = {
    status: 'CONTACTED',
    assigned_to: 'Care Team A',
    notes: 'Follow-up initiated',
  };
  const interventions: Intervention[] = [];
  interventions.push(await updateIntervention(encounterId, body));
  console.log(`Interventions array holds ${interventions.length} item(s)`);
}
