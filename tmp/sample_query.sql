SELECT u.name,
    u.email,
    order_summary.total_amount,
    order_summary.order_count
FROM test1 u
    JOIN (
        SELECT o.user_id,
            SUM(o.amount) AS total_amount,
            COUNT(o.id) AS order_count
        FROM test2 o
            JOIN (
                SELECT id
                FROM test3
                WHERE category = '電子機器'
            ) electronics ON o.product_id = electronics.id
            join test2 o on o.id = o.id
        GROUP BY o.user_id
    ) order_summary ON u.id = order_summary.user_id