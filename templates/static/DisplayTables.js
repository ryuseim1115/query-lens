
const TABLE_WIDTH = 120;
const TABLE_HEIGHT = 30;
const TABLE_MARGIN = 10;

export function displayTables(tables) {
    const svg = document.getElementById("tables")
    svg.innerHTML = '';
    tables.forEach((table, i) => {
        const y = i * (TABLE_HEIGHT + TABLE_MARGIN);

        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("x", 10);
        rect.setAttribute("y", y);
        rect.setAttribute("width", TABLE_WIDTH);
        rect.setAttribute("height", TABLE_HEIGHT);
        rect.setAttribute("fill", "white");
        rect.setAttribute("stroke", "black");
        svg.appendChild(rect);

        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", 10 + TABLE_WIDTH / 2);
        text.setAttribute("y", y + TABLE_HEIGHT / 2);
        text.setAttribute("text-anchor", "middle");
        text.setAttribute("dominant-baseline", "central");
        text.textContent =
            table == null
                ? ""
                : typeof table === "object"
                    ? (table.name != null ? String(table.name) : JSON.stringify(table))
                    : String(table);
        svg.appendChild(text);
    });
}
