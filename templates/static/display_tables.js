

export function display_tables(tables) {
    const svg = document.getElementById("tables")
    svg.innerHTML = '';
    tables.forEach((table, i) => {
        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.textContent = table;
        svg.appendChild(text);
    });
    console.log("aa")
    console.log(tables)
}


function display_values(resultTable, columnsVal, sql_result) {
    const tbody = document.createElement('tbody')
    sql_result.forEach(record => {
        const row = document.createElement('tr')

        columnsVal.forEach(columnVal => {
            const recordTd = document.createElement("td");
            const value = record?.[columnVal]
            recordTd.textContent = (value === null || value === undefined) ? '' : String(value)
            row.appendChild(recordTd);
        })

        tbody.appendChild(row)
    })

    resultTable.appendChild(tbody)
}