const API_BASE = 'http://127.0.0.1:8000';
export async function fetchPatientEncounters(patientNbr, limit = 5) {
    const response = await fetch(`${API_BASE}/patients/${patientNbr}/encounters?limit=${limit}`);
    if (!response.ok) {
        throw new Error(`API error ${response.status}: ${await response.text()}`);
    }
    const data = await response.json();
    console.log(JSON.stringify(data, null, 2));
    return data.items;
}
// Only run standalone under Node; the browser page imports fetchPatientEncounters instead
if (typeof window === 'undefined') {
    const patientNbr = Number(process.argv[2] ?? 88785891);
    const patientEncounters = await fetchPatientEncounters(patientNbr);
    console.log(`Loaded ${patientEncounters.length} encounters for patient ${patientNbr}`);
}
