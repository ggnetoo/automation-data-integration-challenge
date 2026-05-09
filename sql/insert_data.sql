INSERT INTO companies (name) VALUES
    ('GlobalTech'),
    ('DataSystems'),
    ('CloudBase'),
    ('NovaSoft')
ON CONFLICT (name) DO NOTHING;

INSERT INTO users (external_user_id, name, email, city, company_id)
SELECT *
FROM (
    VALUES
        (1,  'Leanne Graham',           'Sincere@april.biz',          'São Paulo', 'GlobalTech'),
        (2,  'Ervin Howell',            'Shanna@melissa.tv',          'São Paulo', 'GlobalTech'),
        (3,  'Clementine Bauch',        'Nathan@yesenia.net',         'São Paulo', 'DataSystems'),
        (4,  'Patricia Lebsack',        'Julianne.OConner@kory.org',  'New York',  'DataSystems'),
        (5,  'Chelsey Dietrich',        'Lucio_Hettinger@annie.ca',   'New York',  'CloudBase'),
        (6,  'Mrs. Dennis Schulist',    'Karley_Dach@jasper.info',    'London',    'CloudBase'),
        (7,  'Kurtis Weissnat',         'Telly.Hoeger@billy.biz',     'London',    'NovaSoft'),
        (8,  'Nicholas Runolfsdottir V','Sherwood@rosamond.me',       'Berlin',    'NovaSoft'),
        (9,  'Glenna Reichert',         'Chaim_McDermott@dana.io',    'Tokyo',     'GlobalTech'),
        (10, 'Clementina DuBuque',      'Rey.Padberg@karina.biz',     'Sydney',    'DataSystems')
) AS src(external_user_id, name, email, city, company_name)
JOIN companies c ON c.name = src.company_name
ON CONFLICT (external_user_id) DO UPDATE SET
    name       = EXCLUDED.name,
    email      = EXCLUDED.email,
    city       = EXCLUDED.city,
    company_id = EXCLUDED.company_id;

-- posts distributed unevenly: [5, 12, 8, 15, 7, 18, 10, 6, 14, 5] per user
INSERT INTO posts (external_post_id, user_id, title, body)
SELECT
    post_id,
    u.id,
    'Imported post ' || post_id,
    'Imported from sample dataset.'
FROM generate_series(1, 100) AS post_id
JOIN users u ON u.external_user_id = CASE
    WHEN post_id BETWEEN 1  AND 5   THEN 1
    WHEN post_id BETWEEN 6  AND 17  THEN 2
    WHEN post_id BETWEEN 18 AND 25  THEN 3
    WHEN post_id BETWEEN 26 AND 40  THEN 4
    WHEN post_id BETWEEN 41 AND 47  THEN 5
    WHEN post_id BETWEEN 48 AND 65  THEN 6
    WHEN post_id BETWEEN 66 AND 75  THEN 7
    WHEN post_id BETWEEN 76 AND 81  THEN 8
    WHEN post_id BETWEEN 82 AND 95  THEN 9
    WHEN post_id BETWEEN 96 AND 100 THEN 10
END
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
    name        = EXCLUDED.name,
    email       = EXCLUDED.email,
    city        = EXCLUDED.city,
    company     = EXCLUDED.company,
    total_posts = EXCLUDED.total_posts,
    processed_at = CURRENT_TIMESTAMP;
