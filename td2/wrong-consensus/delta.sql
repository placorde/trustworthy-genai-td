-- C02 delta query: customers aged exactly 25 on 2026-09-25 (born 2000-09-26 to 2001-09-25 included)
-- and their revenue excluding VAT, in euro cents. The reference counts all of them; both faulty
-- queries (gpt-oss-20b, Cohere) keep none of them, so the gap with their 0 is the whole total.
SELECT c.customer_id, c.birth_date,
       SUM(o.quantity_product * p.price) AS revenue_cents
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN product p ON p.product_id = o.product_id
WHERE c.birth_date >= '2000-09-26'
  AND c.birth_date <= '2001-09-25'
GROUP BY c.customer_id, c.birth_date
ORDER BY c.customer_id;
