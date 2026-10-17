---
name: care-frontend-api-client
description: Creates the TypeScript interface and fetch script for a care-management API endpoint from its spec in docs/API.md. Use when adding a frontend type or a fetch*.ts script for an endpoint in frontend/src.
---

# Care frontend API client

Build from the endpoint spec in `docs/API.md` (the response example and field table). Do not guess the shape. Start only after the endpoint's status is `Backend done`.

## Interface (frontend/src/types/<name>.ts)
- One file per endpoint. Reuse an existing interface when the shape is identical (and update its doc comment).
- Field names are `snake_case`, exactly as in the API.
- Nullable columns use `| null`. Fixed value sets use literal unions, e.g. `'High' | 'Medium' | 'Low'`.
- Add a one-line doc comment naming the endpoint, e.g. `/** Response of GET /care-queue/high */`.
- Export wrapper types for list responses (`total`, `limit`, `offset`, `items`).

## Fetch script (frontend/src/fetch<Name>.ts)
One script per endpoint. Never create a second script for the same endpoint; edit the existing one.

```ts
import type { Thing, ThingList } from './types/thing.ts';

const API_URL = 'http://127.0.0.1:8000/things?limit=5';

const response = await fetch(API_URL);
if (!response.ok) {
  throw new Error(`API error ${response.status}`);
}

const data: ThingList = await response.json();
console.log(JSON.stringify(data, null, 2));

const things: Thing[] = data.items;
```

- Use top-level `await` (promise-based), a `const API_URL`, and a typed array for the values.
- Print the response with `JSON.stringify(data, null, 2)`.
- Use `import type` and include the `.ts` extension in relative imports.
- For a single-object response, bind it into an array of one: `const rows: Thing[] = [data];`.

## Verify
1. Start the API (see `docs/SETUP.md`).
2. From `frontend/src` run `node fetch<Name>.ts`.
3. Confirm the output matches the spec example, then set the endpoint's status to `Done` in `docs/API.md`.
