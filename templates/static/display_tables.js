

export function display_tables(tables) {
    const svg = document.getElementById("tables")
    svg.innerHTML = '';
    tables.forEach((table, i) => {
        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.textContent = table;
        svg.appendChild(text);
    });

    console.log(tables)
}
