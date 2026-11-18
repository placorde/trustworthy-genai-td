-- C02, reference query (reference-td1.csv), expected 590320
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN product p ON p.product_id = o.product_id
JOIN customers c ON c.customer_id = o.customer_id
WHERE (CAST(strftime('%Y', '2026-09-25') AS INTEGER) - CAST(strftime('%Y', c.birth_date) AS INTEGER) - (strftime('%m-%d', '2026-09-25') < strftime('%m-%d', c.birth_date))) = 25;
