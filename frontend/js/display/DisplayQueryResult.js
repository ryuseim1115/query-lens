
export function displayQueryResult(start_index) {
    const stored = JSON.parse(sessionStorage.getItem('querySession'))
    const subquery = stored.subqueryResults.find(s => s.start_index === start_index)
    const rows = subquery.result

    const thead = document.querySelector('.result-body thead')
    const tbody = document.querySelector('.result-body tbody')
    thead.replaceChildren()
    tbody.replaceChildren()

    const columns = Object.keys(rows[0])
    thead.appendChild(buildHeaderRow(columns))
    rows.forEach(row => tbody.appendChild(buildDataRow(row, columns)))
}

function buildHeaderRow(columns) {
    const tr = document.createElement('tr')
    columns.forEach(col => {
        const th = document.createElement('th')
        th.textContent = col
        tr.appendChild(th)
    })
    return tr
}

function buildDataRow(row, columns) {
    const tr = document.createElement('tr')
    columns.forEach(col => {
        const td = document.createElement('td')
        td.textContent = row[col]
        tr.appendChild(td)
    })
    return tr
}
