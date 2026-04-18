import { csvData } from "./main_page.js"

const yesBtn = document.getElementById("yes")
const noBtn = document.getElementById("no")
const confirmAnalyzeTargeDialog = document.getElementById("confirmAnalyzeTarget")

yesBtn.addEventListener('click', async () => {
    const response = await fetch('/determine-csv-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(csvData),
    })
})

noBtn.addEventListener('click', () => {
    confirmAnalyzeTargeDialog.close();
})