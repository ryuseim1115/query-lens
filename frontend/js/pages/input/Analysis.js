import { runQuery } from '../../api/RunQuery.js';

const errorMsg = document.querySelector('.query-error');

document.querySelector('.analysis-btn').addEventListener('click', async () => {
  const queryInfo = Object.fromEntries(
    new FormData(document.querySelector('form')).entries(),
  );

  errorMsg.textContent = '';
  errorMsg.classList.remove('visible');

  const response = await runQuery(queryInfo);

  if (!response.ok) {
    const error = await response.json();
    errorMsg.textContent = error.detail;
    errorMsg.classList.add('visible');
    return;
  }

  const data = await response.json();
  sessionStorage.setItem(
    'querySession',
    JSON.stringify({
      query: queryInfo.query,
      subqueryResults: data.subqueries,
    }),
  );

  location.href = '/result';
});
