import { highlightQuery } from './DisplayQuery.js'
import { displayQueryResult } from './DisplayQueryResult.js'

export function displayTables(subqueries) {
    const tablesEl = document.getElementById('tables')
    tablesEl.innerHTML = ''
    tablesEl.style.display = 'flex'
    tablesEl.style.alignItems = 'flex-start'
    tablesEl.style.position = 'relative'

    let currentDepth = subqueries[0].depth
    let depthGroupEl = createDepthGroup(currentDepth)
    tablesEl.appendChild(depthGroupEl)

    subqueries.forEach(subquery => {
        if (subquery.depth !== currentDepth) {
            currentDepth = subquery.depth
            depthGroupEl = createDepthGroup(currentDepth)
            tablesEl.appendChild(depthGroupEl)
        }

        const subqueryGroupEl = document.createElement('div')
        subqueryGroupEl.className = 'subquery-group'
        subqueryGroupEl.dataset.startIndex = subquery.start_index

        subquery.tables.forEach(table => {
            const tableEl = document.createElement('div')
            tableEl.className = 'table-item'
            tableEl.textContent = table
            tableEl.addEventListener('click', () => highlightQuery(subquery.start_index, subquery.end_index))
            tableEl.addEventListener('click', () => displayQueryResult(subquery.start_index))
            subqueryGroupEl.appendChild(tableEl)
        })

        depthGroupEl.appendChild(subqueryGroupEl)
    })
}

function createDepthGroup(depth) {
    const el = document.createElement('div')
    el.className = 'depth-group'
    el.dataset.depth = depth
    return el
}
