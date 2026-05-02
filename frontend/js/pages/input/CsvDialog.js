import { getCsvFiles, determineCsvFile } from '../../api/DetermineCsv.js';

const dialog = document.querySelector('.csv-file-dialog');
const openCsvFileListBtn = document.querySelector('.open-csv-btn');
const closeCsvFileListBtn = document.querySelector('.close-btn');
const determineCsvFileBtn = document.querySelector('.determine-btn');
const csvFilePathEl = document.querySelector('.csv-file-path');
const csvFileNames = document.querySelector('.csv-file-names');
const csvFileErrorMessage = document.querySelector('.dialog-error');

let csvData = null;

function closeDialog() {
    csvFileErrorMessage.textContent = '';
    dialog.close();
}

function renderCsvFiles(files) {
    csvFileNames.innerHTML = '';
    files.forEach((file) => {
        const li = document.createElement('li');
        li.textContent = file;
        csvFileNames.appendChild(li);
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
