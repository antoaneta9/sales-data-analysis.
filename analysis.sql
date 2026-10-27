-- 1. Calculate total sales by product
SELECT
    product,
    SUM(total_amount) as total_sales
FROM sales
GROUP BY product
ORDER BY total_sales desc;

-- 2. Sales by categories
SELECT
    category,
    COUNT(*) as number_of_sales,
    SUM(total_amount) as total_sales
FROM sales
GROUP BY category;

-- 3. TOP 3 MOST SOLD PRODUCTS
SELECT
    product,
    SUM(total_amount) AS total_sales
FROM sales
GROUP BY product
ORDER BY total_sales DESC
LIMIT 3;

-- 4.
SELECT
    s.order_id,
    c.customer_name,
    c.city,
    s.product,
    s.total_amount
FROM sales AS s
INNER JOIN customers AS c
    ON s.customer_id = c.customer_id
ORDER BY s.order_id;

-- 5. Find all orders, including orders without matching customers
SELECT
    s.order_id,
    c.customer_name,
    c.city,
    s.product,
    s.total_amount
FROM sales AS s
LEFT JOIN customers AS c
    ON s.customer_id = c.customer_id
ORDER BY s.order_id;

-- 6. Find orders without a matching customer
SELECT
    s.order_id,
    s.customer_id,
    s.product,
    s.total_amount
FROM sales AS s
LEFT JOIN customers AS c
    ON s.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- 7. Total sales by city
SELECT
    c.city,
    SUM(s.total_amount) AS total_sales
FROM sales AS s
INNER JOIN customers AS c
    ON s.customer_id = c.customer_id
GROUP BY c.city
ORDER BY total_sales DESC;

-- 8. Classify orders by sales value
SELECT
    order_id,
    product,
    total_amount,
    CASE
        WHEN total_amount >= 500 THEN 'High'
        WHEN total_amount >= 100 THEN 'Medium'
        ELSE 'Low'
    END AS order_value_category
FROM sales
ORDER BY total_amount DESC;

-- 9. Rank products by total sales
SELECT
    product,
    total_sales,
    RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
FROM (
    SELECT
        product,
        SUM(total_amount) AS total_sales
    FROM sales
    GROUP BY product
) AS product_summary;
