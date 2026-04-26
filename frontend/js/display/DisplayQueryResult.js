export function displayQueryResult(queryResult) {
    const resultTable = document.getElementById("analysisResult")
    resultTable.innerHTML = '';

    if (!queryResult || queryResult.length === 0) {
        resultTable.textContent = "検索結果は0件です"
        return
    }

    const columnsVal = Object.keys(queryResult[0])
    displayColumns(resultTable, columnsVal)
    displayValues(resultTable, columnsVal, queryResult)
}

function displayColumns(resultTable, columnsVal) {
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

function displayValues(resultTable, columnsVal, queryResult) {
    const tbody = document.createElement('tbody')
    queryResult.forEach(record => {
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
