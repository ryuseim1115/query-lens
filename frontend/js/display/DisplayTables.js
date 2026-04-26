import { highlightQuery } from './DisplayQuery.js'

export function displayTables(subqueries) {
    const tablesEl = document.getElementById('tables')
    tablesEl.innerHTML = ''
    tablesEl.style.display = 'flex'
    tablesEl.style.alignItems = 'flex-start'

    let currentDepth = subqueries[0].depth
    let depthGroupEl = document.createElement('div')
    depthGroupEl.className = 'depth-group'
    tablesEl.appendChild(depthGroupEl)

    subqueries.forEach(subquery => {
        if (subquery.depth !== currentDepth) {
            currentDepth = subquery.depth
            depthGroupEl = document.createElement('div')
            depthGroupEl.className = 'depth-group'
            tablesEl.appendChild(depthGroupEl)
        }
        subquery.tables.forEach(table => {
            const tableEl = document.createElement('div')
            tableEl.className = 'table-item'
            tableEl.textContent = table
            tableEl.addEventListener('click', () => highlightQuery(subquery.start_index, subquery.end_index))
            depthGroupEl.appendChild(tableEl)
        })
    })
}
