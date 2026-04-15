

export function display_query_result(query_result) {
    const resultTable = document.getElementById("analysis_result")
    resultTable.innerHTML = '';

    if (!query_result || query_result.length === 0) {
        resultTable.textContent = "検索結果は0件です"
        return
    }

    const columnsVal = Object.keys(query_result[0])
    display_columns(resultTable, columnsVal)
    display_values(resultTable, columnsVal, query_result)
}

function display_columns(resultTable, columnsVal) {
    const thead = document.createElement('thead')
    const headerRow = document.createElement('tr')

    columnsVal.forEach(columnVal => {
        const columnTh = document.createElement("th");
        columnTh.textContent = columnVal;
        headerRow.appendChild(columnTh);
    })

    thead.appendChild(headerRow)
    resultTable.appendChild(thead)
}

function display_values(resultTable, columnsVal, query_result) {
    const tbody = document.createElement('tbody')
    query_result.forEach(record => {
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