import { getCsvFiles, determineCsvFile } from '../../api/DetermineCsv.js';

const dialog = document.getElementById('csvFileList');
const openCsvFileListBtn = document.getElementById('openCsvFileList');
const closeCsvFileListBtn = document.getElementById('closeCsvFileList');
const determineCsvFileBtn = document.getElementById('determineCsvFile');
const csvFilePathEl = document.getElementById('csvFilePath');
const csvFileItems = document.getElementById('csvFileItems');
const csvFileErrorMessage = document.getElementById('csvFileErrorMessage');

let csvData = null;

function closeDialog() {
    csvFileErrorMessage.textContent = '';
    dialog.close();
}

function renderCsvFiles(files) {
    csvFileItems.innerHTML = '';
    files.forEach((file) => {
        const li = document.createElement('li');
        li.textContent = file;
        csvFileItems.appendChild(li);
    });
}

openCsvFileListBtn.addEventListener('click', async () => {
    csvData = await getCsvFiles();
    csvFilePathEl.textContent = `※解析対象ファイルは ${csvData.CSV_FILES_DIR} 配下のファイルです`;
    renderCsvFiles(csvData.csv_files);
    dialog.showModal();
});

closeCsvFileListBtn.addEventListener('click', () => {
    closeDialog();
});

determineCsvFileBtn.addEventListener('click', async () => {
    const response = await determineCsvFile(csvData);
    if (!response.ok) {
        const error = await response.json();
        csvFileErrorMessage.textContent = error.detail;
        return;
    }
    closeDialog();
});
