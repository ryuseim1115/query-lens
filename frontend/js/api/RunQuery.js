export async function runQuery(queryInfo) {
  const response = await fetch('/run-query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(queryInfo),
  });
  return response;
}
