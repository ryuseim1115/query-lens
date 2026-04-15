const dialog = document.getElementById('csvFileList');
const openCsvFileListBtn = document.getElementById('openCsvFileList');
const closeCsvFileListBtn = document.getElementById('closeCsvFileList');
const csvFileItems = document.getElementById('csvFileItems');

openCsvFileListBtn.addEventListener('click', async () => {
    const response = await fetch('/get-csv-files');
    const data = await response.json();

    document.getElementById('csvFilePath').textContent = `※解析対象ファイルは ${data.CSV_FILES_DIR} 配下のファイルです`;

    csvFileItems.innerHTML = '';
    data.csv_files.forEach((file) => {
        const li = document.createElement('li');
        li.textContent = file;
        csvFileItems.appendChild(li);
    });

    dialog.showModal();
});

closeCsvFileListBtn.addEventListener('click', () => {
    dialog.close();
});


