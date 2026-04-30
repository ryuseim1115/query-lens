SELECT
    u.id,
    u.name,
    o.total_amount
FROM test1 AS u
JOIN (
    SELECT user_id, SUM(amount) AS total_amount
    FROM test2
    GROUP BY user_id
) AS o ON u.id = o.user_id
