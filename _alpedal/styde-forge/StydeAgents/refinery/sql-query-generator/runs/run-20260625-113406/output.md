Schema:
users (id, name, email, created_at)
orders (id, user_id, amount, status, created_at) 

Question: Find all users who placed orders totaling over $1000 in the last 30 days. Return user name, email, and total order amount.

Query:
SELECT u.name, u.email, SUM(o.amount) AS total_amount
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed'
AND o.created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
GROUP BY u.id, u.name, u.email
HAVING SUM(o.amount) > 1000
ORDER BY total_amount DESC;

Explanation: Joins users to their completed orders in the last 30 days, sums order amounts per user, filters for totals over $1000, sorts high to low.