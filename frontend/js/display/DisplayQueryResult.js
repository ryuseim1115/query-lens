import { findParentAliasEl } from '../utility.js'

export function displayQueryResult(subqueries) {
    subqueries.forEach(subquery => {
        const parentAlias = findParentAliasEl(subquery)
        if (!parentAlias) return;
        //親エイリアスが押下された時のみイベント追加
        parentAlias.addEventListener('click', () => renderQueryResult(subquery))
    })
}

function renderQueryResult(subquery) {
    const rows = subquery.result
    if (!rows.length) {
        noResult()
        return
    };

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

function noResult() {
    console.log('aa');
    document.getElementById('no-result').style.display = 'block'
}