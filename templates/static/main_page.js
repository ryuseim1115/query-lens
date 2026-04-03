const dialog = document.getElementById('dbDialog');
const openDbCongigBtn = document.getElementById('openDbConfig');


// モーダルとして開く
openDbCongigBtn.addEventListener('click', () => {
    dialog.showModal();
});

// iframeからの接続成功通知を受け取りボタンを非活性化
window.addEventListener('message', (event) => {
    if (event.data === 'db_connected') {
        openDbCongigBtn.textContent = 'DB接続済'
        openDbCongigBtn.disabled = true;
    }
});


