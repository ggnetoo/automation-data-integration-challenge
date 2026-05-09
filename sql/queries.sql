-- 1. Top 5 companies with the most posts
SELECT
    c.name AS company,
    COUNT(p.id) AS total_posts
FROM companies c
JOIN users u ON u.company_id = c.id
LEFT JOIN posts p ON p.user_id = u.id
GROUP BY c.name
ORDER BY total_posts DESC, c.name
LIMIT 5;

-- 2. Users by city
SELECT
    city,
    COUNT(*) AS total_users
FROM users
GROUP BY city
ORDER BY total_users DESC, city;

-- 3. Average posts per user by company
SELECT
    c.name AS company,
    ROUND(COUNT(p.id)::numeric / NULLIF(COUNT(DISTINCT u.id), 0), 2) AS avg_posts_per_user
FROM companies c
JOIN users u ON u.company_id = c.id
LEFT JOIN posts p ON p.user_id = u.id
GROUP BY c.name
ORDER BY avg_posts_per_user DESC, c.name;

-- 4. Final table used by spreadsheet/dashboard
SELECT
    user_id,
    name,
    email,
    city,
    company,
    total_posts
FROM processed_user_metrics
ORDER BY user_id;

