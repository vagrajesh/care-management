const API_URL = 'http://127.0.0.1:8000/operations/summary';
const response = await fetch(API_URL);
if (!response.ok) {
    throw new Error(`API error ${response.status}`);
}
const data = await response.json();
console.log(JSON.stringify(data, null, 2));
const summaries = [data];
console.log(`Pending reviews: ${data.pending_reviews} of ${data.total_encounters} encounters`);
console.log(`Summaries in array: ${summaries.length}`);
export {};
