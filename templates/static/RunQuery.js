import { displayQueryResult } from "./DisplayQueryResult.js"
import { displayTables } from "./DisplayTables.js"

const analysisStartBtn = document.getElementById('analysisStartBtn')
analysisStartBtn.addEventListener('click', async () => {
    const queryForm = document.getElementById('queryForm')
    const queryInfoDict = new FormData(queryForm)
    const queryInfo = Object.fromEntries(queryInfoDict.entries())

    const response = await fetch('/run-query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(queryInfo),
    });
    if (!response.ok) {
        const error = await response.json();
        document.getElementById('errorMessage').textContent = error.detail;
        return;
    }
    document.getElementById('errorMessage').textContent = '';
    const result = await response.json();
    displayQueryResult(result.query_result);
    displayTables(result.tables);
    document.getElementById('coloredQueryDisplay').innerHTML = result.colored_query;
});
