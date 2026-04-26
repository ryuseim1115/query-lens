export async function getCsvFiles() {
    const response = await fetch('/get-csv-files');
    return response.json();
}

export async function determineCsvFile(csvData) {
    const response = await fetch('/determine-csv-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(csvData),
    });
    return response;
}
