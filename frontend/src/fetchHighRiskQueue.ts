import type { HighRiskQueue, HighRiskQueueItem } from './types/highRiskQueue.ts';

const API_URL = 'http://127.0.0.1:8000/care-queue/high?limit=5';

const response = await fetch(API_URL);
if (!response.ok) {
  throw new Error(`API error ${response.status}`);
}

const data: HighRiskQueue = await response.json();
console.log(JSON.stringify(data, null, 2));

const highRiskQueue: HighRiskQueueItem[] = data.items;
console.log(`High-risk items in array: ${highRiskQueue.length} of ${data.total}`);
