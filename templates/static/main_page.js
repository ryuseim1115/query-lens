const dialog = document.getElementById('csvFileList');
const openCsvFileListBtn = document.getElementById('openCsvFileList');
const closeCsvFileListBtn = document.getElementById('closeCsvFileList');
const csvFileItems = document.getElementById('csvFileItems');

export let csvData = null;

openCsvFileListBtn.addEventListener('click', async () => {
    const response = await fetch('/get-csv-files');
    csvData = await response.json();
    console.log(csvData)

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
    dialog.close();
});

const determineCsvFile = document.getElementById("determineCsvFile")
const confirmAnalyzeTargetDialog = document.getElementById('confirmAnalyzeTarget');

determineCsvFile.addEventListener('click', () => {
    confirmAnalyzeTargetDialog.showModal();
});
