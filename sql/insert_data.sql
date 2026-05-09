INSERT INTO companies (name) VALUES
    ('Romaguera-Crona'),
    ('Deckow-Crist'),
    ('Romaguera-Jacobson'),
    ('Robel-Corkery'),
    ('Keebler LLC'),
    ('Considine-Lockman'),
    ('Johns Group'),
    ('Abernathy Group'),
    ('Yost and Sons'),
    ('Hoeger LLC')
ON CONFLICT (name) DO NOTHING;

INSERT INTO users (external_user_id, name, email, city, company_id)
SELECT *
FROM (
    VALUES
        (1, 'Leanne Graham', 'Sincere@april.biz', 'Gwenborough', 'Romaguera-Crona'),
        (2, 'Ervin Howell', 'Shanna@melissa.tv', 'Wisokyburgh', 'Deckow-Crist'),
        (3, 'Clementine Bauch', 'Nathan@yesenia.net', 'McKenziehaven', 'Romaguera-Jacobson'),
        (4, 'Patricia Lebsack', 'Julianne.OConner@kory.org', 'South Elvis', 'Robel-Corkery'),
        (5, 'Chelsey Dietrich', 'Lucio_Hettinger@annie.ca', 'Roscoeview', 'Keebler LLC'),
        (6, 'Mrs. Dennis Schulist', 'Karley_Dach@jasper.info', 'South Christy', 'Considine-Lockman'),
        (7, 'Kurtis Weissnat', 'Telly.Hoeger@billy.biz', 'Howemouth', 'Johns Group'),
        (8, 'Nicholas Runolfsdottir V', 'Sherwood@rosamond.me', 'Aliyaview', 'Abernathy Group'),
        (9, 'Glenna Reichert', 'Chaim_McDermott@dana.io', 'Bartholomebury', 'Yost and Sons'),
        (10, 'Clementina DuBuque', 'Rey.Padberg@karina.biz', 'Lebsackbury', 'Hoeger LLC')
) AS source_data(external_user_id, name, email, city, company_name)
JOIN companies c ON c.name = source_data.company_name
ON CONFLICT (external_user_id) DO UPDATE SET
    name = EXCLUDED.name,
    email = EXCLUDED.email,
    city = EXCLUDED.city,
    company_id = EXCLUDED.company_id;

INSERT INTO posts (external_post_id, user_id, title, body)
SELECT post_id, u.id, 'Imported post ' || post_id, 'Imported from JSONPlaceholder sample dataset.'
FROM generate_series(1, 100) AS post_id
JOIN users u ON u.external_user_id = ((post_id - 1) / 10) + 1
ON CONFLICT (external_post_id) DO NOTHING;

INSERT INTO processed_user_metrics (user_id, name, email, city, company, total_posts)
SELECT
    u.external_user_id,
    u.name,
    u.email,
    u.city,
    c.name,
    COUNT(p.id) AS total_posts
FROM users u
JOIN companies c ON c.id = u.company_id
LEFT JOIN posts p ON p.user_id = u.id
GROUP BY u.external_user_id, u.name, u.email, u.city, c.name
ON CONFLICT (user_id) DO UPDATE SET
    name = EXCLUDED.name,
    email = EXCLUDED.email,
    city = EXCLUDED.city,
    company = EXCLUDED.company,
    total_posts = EXCLUDED.total_posts,
    processed_at = CURRENT_TIMESTAMP;

