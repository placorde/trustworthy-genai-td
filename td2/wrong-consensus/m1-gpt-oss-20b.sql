-- C02, openai/gpt-oss-20b (Groq), TD1 trace 2026-10-21 12:59:06, verdict incorrect, value 0
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE c.birth_date > '2025-09-25' AND c.birth_date <= '2026-09-25';
