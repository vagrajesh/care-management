// Fetch care queue items from the API
import type { CareQueue, CareQueueItem } from './types/careQueue.ts';

const API_URL = 'http://127.0.0.1:8000/care-queue?limit=5';

async function fetchCareQueue(): Promise<CareQueueItem[]> {
  const response = await fetch(API_URL);
  if (!response.ok) {
    throw new Error(`API error ${response.status}`);
  }
  const data: CareQueue = await response.json();
  console.log(JSON.stringify(data, null, 2));
  return data.items;
}

const careQueue: CareQueueItem[] = await fetchCareQueue();
console.log(`Loaded ${careQueue.length} care queue items into the array`);
