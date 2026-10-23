import { fetchEncounterById } from './fetchEncounterById.js';
import { fetchIntervention } from './fetchIntervention.js';
import { updateIntervention } from './updateIntervention.js';
import { INTERVENTION_STATUSES } from './types/intervention.js';
// UI column header -> API field. Add, remove or reorder columns here only.
const COLUMNS = [
    { header: 'Encounter Id', field: 'encounter_id' },
    { header: 'Patient Number', field: 'patient_nbr' },
    { header: 'Age', field: 'age' },
    { header: 'Time in Hospital', field: 'time_in_hospital' },
    { header: 'Medications', field: 'num_medications' },
    { header: 'Readmitted', field: 'readmitted' },
    { header: 'Risk Score', field: 'risk_score' },
    { header: 'Risk Level', field: 'risk_level' },
];
const title = document.getElementById('encounter-title');
const backLink = document.getElementById('back-link');
const message = document.getElementById('status-message');
const tableHead = document.getElementById('encounter-table-head');
const tableBody = document.getElementById('encounter-table-body');
const currentStatus = document.getElementById('current-status');
const form = document.getElementById('status-form');
const statusSelect = document.getElementById('status');
const assignedToInput = document.getElementById('assigned-to');
const notesInput = document.getElementById('notes');
const saveButton = document.getElementById('save-button');
function showEncounter(encounter) {
    const headRow = document.createElement('tr');
    const bodyRow = document.createElement('tr');
    for (const column of COLUMNS) {
        const th = document.createElement('th');
        th.textContent = column.header;
        headRow.appendChild(th);
        const td = document.createElement('td');
        const value = encounter[column.field];
        td.textContent = value === null ? '' : String(value);
        bodyRow.appendChild(td);
    }
    tableHead.appendChild(headRow);
    tableBody.appendChild(bodyRow);
}
function showIntervention(intervention) {
    currentStatus.textContent = intervention ? intervention.status : 'Not started';
    statusSelect.value = intervention ? intervention.status : 'Open';
    assignedToInput.value = intervention?.assigned_to ?? '';
    notesInput.value = intervention?.notes ?? '';
}
async function save(encounterId) {
    saveButton.disabled = true;
    try {
        const updated = await updateIntervention(encounterId, {
            status: statusSelect.value,
            assigned_to: assignedToInput.value.trim(),
            notes: notesInput.value.trim(),
        });
        showIntervention(updated);
        message.textContent = `Status updated to ${updated.status}.`;
    }
    catch (error) {
        message.textContent = 'Could not update status. Is the API running?';
        console.error(error);
    }
    finally {
        saveButton.disabled = false;
    }
}
async function load() {
    const params = new URLSearchParams(window.location.search);
    const encounterId = Number(params.get('encounter_id'));
    if (!params.get('encounter_id') || !Number.isInteger(encounterId)) {
        message.textContent = 'No encounter selected. Open this page from the search results.';
        return;
    }
    title.textContent = String(encounterId);
    for (const status of INTERVENTION_STATUSES) {
        statusSelect.add(new Option(status, status));
    }
    try {
        const [encounter, intervention] = await Promise.all([
            fetchEncounterById(encounterId),
            fetchIntervention(encounterId),
        ]);
        backLink.href = `search.html?patient_nbr=${encounter.patient_nbr}`;
        showEncounter(encounter);
        showIntervention(intervention);
        form.hidden = false;
    }
    catch (error) {
        const notFound = error instanceof Error && error.message.includes('404');
        message.textContent = notFound ? 'Encounter not found.' : 'Could not load encounter. Is the API running?';
        console.error(error);
        return;
    }
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        void save(encounterId);
    });
}
await load();
