import { fetchIntervention } from './fetchIntervention.ts';
import { fetchPatientEncounters } from './fetchPatientEncounters.ts';
import type { Encounter } from './types/encounter.ts';

const NO_INTERVENTION = 'Not started';

// UI column header -> API field. Add, remove or reorder columns here only.
const COLUMNS: { header: string; field: keyof Encounter }[] = [
  { header: 'Encounter Id', field: 'encounter_id' },
  { header: 'Patient Number', field: 'patient_nbr' },
  { header: 'Age', field: 'age' },
  { header: 'Time in Hospital', field: 'time_in_hospital' },
  { header: 'Inpatient', field: 'number_inpatient' },
  { header: 'Emergency', field: 'number_emergency' },
  { header: 'Outpatient', field: 'number_outpatient' },
  { header: 'Medications', field: 'num_medications' },
  { header: 'Readmitted', field: 'readmitted' },
  { header: 'Risk Score', field: 'risk_score' },
  { header: 'Risk Level', field: 'risk_level' },
];

const form = document.getElementById('search-form') as HTMLFormElement;
const patientInput = document.getElementById('patient-number') as HTMLInputElement;
const riskLevelSelect = document.getElementById('risk-level') as HTMLSelectElement;
const riskScoreInput = document.getElementById('risk-score') as HTMLInputElement;
const message = document.getElementById('search-message') as HTMLParagraphElement;
const tableHead = document.getElementById('results-table-head') as HTMLTableSectionElement;
const tableBody = document.getElementById('results-table-body') as HTMLTableSectionElement;

function showHeaders(): void {
  const row = document.createElement('tr');
  for (const header of [...COLUMNS.map((c) => c.header), 'Intervention Status']) {
    const cell = document.createElement('th');
    cell.textContent = header;
    row.appendChild(cell);
  }
  tableHead.appendChild(row);
}

function statusLink(encounterId: number, text: string): HTMLAnchorElement {
  const link = document.createElement('a');
  link.href = `status.html?encounter_id=${encounterId}`;
  link.textContent = text;
  return link;
}

function showRows(encounters: Encounter[], statuses: string[]): void {
  tableBody.innerHTML = '';
  encounters.forEach((encounter, i) => {
    const row = document.createElement('tr');
    for (const column of COLUMNS) {
      const value = encounter[column.field];
      const cell = document.createElement('td');
      if (column.field === 'encounter_id') {
        cell.appendChild(statusLink(encounter.encounter_id, String(value)));
      } else {
        cell.textContent = value === null ? '' : String(value);
      }
      row.appendChild(cell);
    }
    const statusCell = document.createElement('td');
    statusCell.appendChild(statusLink(encounter.encounter_id, statuses[i]));
    row.appendChild(statusCell);
    tableBody.appendChild(row);
  });
}

// One lookup per encounter; a failed lookup shows in its own row instead of failing the search.
async function fetchStatuses(encounters: Encounter[]): Promise<string[]> {
  const results = await Promise.allSettled(encounters.map((e) => fetchIntervention(e.encounter_id)));
  return results.map((r) => {
    if (r.status === 'rejected') return 'Unavailable';
    return r.value ? r.value.status : NO_INTERVENTION;
  });
}

async function search(): Promise<void> {
  tableBody.innerHTML = '';
  const patientNbr = Number(patientInput.value.trim());
  if (!patientInput.value.trim() || !Number.isInteger(patientNbr)) {
    message.textContent = 'Enter a numeric Patient Number.';
    return;
  }
  try {
    let encounters = await fetchPatientEncounters(patientNbr, 100);
    // The API searches by patient only; risk level and score narrow the list here.
    if (riskLevelSelect.value) {
      encounters = encounters.filter((e) => e.risk_level === riskLevelSelect.value);
    }
    if (riskScoreInput.value.trim()) {
      encounters = encounters.filter((e) => e.risk_score === Number(riskScoreInput.value));
    }
    message.textContent = encounters.length ? `${encounters.length} encounter(s) found.` : 'No encounters match.';
    showRows(encounters, await fetchStatuses(encounters));
  } catch (error) {
    const notFound = error instanceof Error && error.message.includes('404');
    message.textContent = notFound ? 'Patient not found.' : 'Could not load encounters. Is the API running?';
    console.error(error);
  }
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  void search();
});

showHeaders();

// Returning from the status screen re-runs the search for that patient.
const initialPatient = new URLSearchParams(window.location.search).get('patient_nbr');
if (initialPatient) {
  patientInput.value = initialPatient;
  void search();
}
