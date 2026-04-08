import { display_sql_result } from "./display_sql_result.js"
import { display_tables } from "./display_tables.js"


const queryForm = document.getElementById('queryForm')
queryForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const query = document.getElementById('sqlInput').value;
    const response = await fetch('/run-query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query }),
    });
    if (!response.ok) {
        const error = await response.json();
        document.getElementById('error_message').textContent = error.detail;
        return;
    }
    document.getElementById('error_message').textContent = '';
    const result = await response.json();
    display_sql_result(result.sql_result);
    display_tables(result.tables);
    document.getElementById('coloredSqlDisplay').innerHTML = result.colored_sql;

});