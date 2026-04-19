const dialog = document.getElementById('csvFileList');
const openCsvFileListBtn = document.getElementById('openCsvFileList');
const closeCsvFileListBtn = document.getElementById('closeCsvFileList');
const csvFileItems = document.getElementById('csvFileItems');
const csvFileErrorMessage = document.getElementById('csvFileErrorMessage');

let csvData = null;

openCsvFileListBtn.addEventListener('click', async () => {
    const response = await fetch('/get-csv-files');
    csvData = await response.json();

    document.getElementById('csvFilePath').textContent = `※解析対象ファイルは ${csvData.CSV_FILES_DIR} 配下のファイルです`;

    csvFileItems.innerHTML = '';
    csvData.csv_files.forEach((file) => {
        const li = document.createElement('li');
        li.textContent = file;
        csvFileItems.appendChild(li);
    });

    dialog.showModal();
});

closeCsvFileListBtn.addEventListener('click', () => {
    csvFileErrorMessage.textContent = '';
    dialog.close();
});

const determineCsvFile = document.getElementById("determineCsvFile")

determineCsvFile.addEventListener('click', async () => {
    const response = await fetch('/determine-csv-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(csvData),
    })
    if (!response.ok) {
        const error = await response.json();
        csvFileErrorMessage.textContent = error.detail;
        return;
    }
    csvFileErrorMessage.textContent = '';
    dialog.close();
});
