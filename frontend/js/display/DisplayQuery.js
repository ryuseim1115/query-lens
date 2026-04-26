export function displayQuery(query) {
    const queryDisplayEl = document.getElementById('query-display');
    queryDisplayEl.textContent = query;
}

function escapeHtml(text) {
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
}

export function highlightQuery(start_index, end_index) {
    const queryDisplayEl = document.getElementById('query-display');
    const query = queryDisplayEl.textContent;
    const before = escapeHtml(query.slice(0, start_index));
    const highlighted = escapeHtml(query.slice(start_index, end_index));
    const after = escapeHtml(query.slice(end_index));
    queryDisplayEl.innerHTML = `${before}<mark>${highlighted}</mark>${after}`;
}
