const API_URL = 'http://127.0.0.1:8000/care-queue?limit=5';
async function fetchCareQueue() {
    const response = await fetch(API_URL);
    if (!response.ok) {
        throw new Error(`API error ${response.status}`);
    }
    const data = await response.json();
    console.log(JSON.stringify(data, null, 2));
    return data.items;
}
const careQueue = await fetchCareQueue();
console.log(`Loaded ${careQueue.length} care queue items into the array`);
export {};
