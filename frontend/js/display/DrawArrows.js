export function displayArrows(subqueries) {
    const tablesEl = document.getElementById('tables')
    const tablesRect = tablesEl.getBoundingClientRect()

    const canvas = document.createElement('canvas')
    canvas.style.position = 'absolute'
    canvas.style.top = '0px'
    canvas.style.left = '0px'
    canvas.style.pointerEvents = 'none'
    canvas.width = tablesEl.offsetWidth
    canvas.height = tablesEl.offsetHeight
    tablesEl.appendChild(canvas)

    const ctx = canvas.getContext('2d')
    ctx.strokeStyle = '#ff0000'

    for (const subquery of subqueries) {
        if (!subquery.parent_alias) continue

        const parentEl = findParentAliasEl(subquery)
        const parentRect = parentEl.getBoundingClientRect()
        const toX = parentRect.x - tablesRect.x
        const toY = parentRect.y + parentRect.height / 2 - tablesRect.y

        const subqueryGroupEl = document.querySelector(`.subquery-group[data-start-index="${subquery.start_index}"]`)
        for (const table of subqueryGroupEl.querySelectorAll('.table-item')) {
            const rect = table.getBoundingClientRect()
            const fromX = rect.x + rect.width - tablesRect.x
            const fromY = rect.y + rect.height / 2 - tablesRect.y

            ctx.beginPath()
            ctx.moveTo(fromX, fromY)
            ctx.lineTo(toX, toY)
            ctx.stroke()
        }
    }
}

function findParentAliasEl(subquery) {
    const parentGroupEl = document.querySelector(`.depth-group[data-depth="${subquery.depth - 1}"]`)
    return [...parentGroupEl.querySelectorAll('.table-item')]
        .find(item => item.textContent === subquery.parent_alias)
}
