import { csvData } from "./MainPage.js"

const yesBtn = document.getElementById("yes")
const noBtn = document.getElementById("no")
const confirmAnalyzeTargetDialog = document.getElementById("confirmAnalyzeTarget")

yesBtn.addEventListener('click', async () => {
    const response = await fetch('/determine-csv-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(csvData),
    })
    if (!response.ok) {
        const error = await response.json();
        console.error(error.detail);
        return;
    }
    confirmAnalyzeTargetDialog.close();
})

noBtn.addEventListener('click', () => {
    confirmAnalyzeTargetDialog.close();
})
