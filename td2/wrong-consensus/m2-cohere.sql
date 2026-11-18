-- C02, cohere/north-mini-code:free (OpenRouter), TD1 trace 2026-10-21 13:02:41, verdict incorrect, value 0
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE c.birth_date <= '2026-09-25' AND
      date(c.birth_date, '+25 years') > '2026-09-25' AND
      date(c.birth_date, '+26 years') <= '2026-09-25';
