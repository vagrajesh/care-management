const API_URL = 'http://127.0.0.1:8000/operations/readmission-analysis';
const response = await fetch(API_URL);
if (!response.ok) {
    throw new Error(`API error ${response.status}`);
}
const data = await response.json();
console.log(JSON.stringify(data, null, 2));
const byRiskLevel = data.by_risk_level;
console.log(`Risk levels in array: ${byRiskLevel.length}`);
export {};
