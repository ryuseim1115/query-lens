import { display_query_result } from "./display_query_result.js"
import { display_tables } from "./display_tables.js"



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
        document.getElementById('error_message').textContent = error.detail;
        return;
    }
    document.getElementById('error_message').textContent = '';
    const result = await response.json();
    display_query_result(result.query_result);
    display_tables(result.tables);
    document.getElementById('coloredQueryDisplay').innerHTML = result.colored_query;

});