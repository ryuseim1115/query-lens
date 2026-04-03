

export function display_sql_result(sql_result) {
    const resultTable = document.getElementById("analysis_result")
    resultTable.innerHTML = '';

    if (!sql_result || sql_result.length === 0) {
        resultTable.textContent = "検索結果は0件です"
        return
    }

    const columnsVal = Object.keys(sql_result[0])
    display_columns(resultTable, columnsVal)
    display_values(resultTable, columnsVal, sql_result)
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