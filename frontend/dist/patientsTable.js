import { fetchEncounters } from './fetchEncounters.js';
// UI column header -> API field. Add, remove or reorder columns here only.
const COLUMNS = [
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
const tableHead = document.getElementById('patients-table-head');
const tableBody = document.getElementById('patients-table-body');
function showHeaders() {
    if (!tableHead)
        return;
    const row = document.createElement('tr');
    for (const column of COLUMNS) {
        const cell = document.createElement('th');
        cell.textContent = column.header;
        row.appendChild(cell);
    }
    tableHead.appendChild(row);
}
async function showPatients() {
    if (!tableBody)
        return;
    try {
        const encounters = await fetchEncounters();
        tableBody.innerHTML = '';
        for (const encounter of encounters) {
            const row = document.createElement('tr');
            for (const column of COLUMNS) {
                const value = encounter[column.field];
                const cell = document.createElement('td');
                cell.textContent = value === null ? '' : String(value);
                row.appendChild(cell);
            }
            tableBody.appendChild(row);
        }
    }
    catch (error) {
        tableBody.innerHTML = `<tr><td colspan="${COLUMNS.length}">Could not load patients. Is the API running?</td></tr>`;
        console.error(error);
    }
}
showHeaders();
await showPatients();
