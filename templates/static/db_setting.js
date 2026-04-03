const closeBtn = document.getElementById('closeDbConfig');

closeBtn.addEventListener('click', () => {
    const dialog = window.parent.document.getElementById('dbDialog');
    dialog.close();
});


const dbForm = document.getElementById('db_form');

dbForm.addEventListener('submit', send_db_info);

async function send_db_info(event) {
    event.preventDefault();
    const formData = new FormData(dbForm);
    const data = Object.fromEntries(formData.entries());

    const response = await fetch('/db_connector', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    console.log(result)
    if (result['is_connect']) {
        alert("DB接続に成功しました");
        window.parent.postMessage('db_connected', '*');
        window.parent.document.getElementById('dbDialog').close();
    } else {
        alert(`DB接続に失敗しました\n${result['message']}`);


    }

}