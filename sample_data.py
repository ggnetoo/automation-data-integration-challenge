SAMPLE_USERS = [
    {
        "id": 1,
        "name": "Leanne Graham",
        "email": "Sincere@april.biz",
        "address": {"city": "São Paulo"},
        "company": {"name": "GlobalTech"},
    },
    {
        "id": 2,
        "name": "Ervin Howell",
        "email": "Shanna@melissa.tv",
        "address": {"city": "São Paulo"},
        "company": {"name": "GlobalTech"},
    },
    {
        "id": 3,
        "name": "Clementine Bauch",
        "email": "Nathan@yesenia.net",
        "address": {"city": "São Paulo"},
        "company": {"name": "DataSystems"},
    },
    {
        "id": 4,
        "name": "Patricia Lebsack",
        "email": "Julianne.OConner@kory.org",
        "address": {"city": "New York"},
        "company": {"name": "DataSystems"},
    },
    {
        "id": 5,
        "name": "Chelsey Dietrich",
        "email": "Lucio_Hettinger@annie.ca",
        "address": {"city": "New York"},
        "company": {"name": "CloudBase"},
    },
    {
        "id": 6,
        "name": "Mrs. Dennis Schulist",
        "email": "Karley_Dach@jasper.info",
        "address": {"city": "London"},
        "company": {"name": "CloudBase"},
    },
    {
        "id": 7,
        "name": "Kurtis Weissnat",
        "email": "Telly.Hoeger@billy.biz",
        "address": {"city": "London"},
        "company": {"name": "NovaSoft"},
    },
    {
        "id": 8,
        "name": "Nicholas Runolfsdottir V",
        "email": "Sherwood@rosamond.me",
        "address": {"city": "Berlin"},
        "company": {"name": "NovaSoft"},
    },
    {
        "id": 9,
        "name": "Glenna Reichert",
        "email": "Chaim_McDermott@dana.io",
        "address": {"city": "Tokyo"},
        "company": {"name": "GlobalTech"},
    },
    {
        "id": 10,
        "name": "Clementina DuBuque",
        "email": "Rey.Padberg@karina.biz",
        "address": {"city": "Sydney"},
        "company": {"name": "DataSystems"},
    },
]

# posts per user: [5, 12, 8, 15, 7, 18, 10, 6, 14, 5] — intentionally uneven
_POST_COUNTS = [5, 12, 8, 15, 7, 18, 10, 6, 14, 5]

SAMPLE_POSTS = []
_post_id = 1
for _user_id, _count in enumerate(_POST_COUNTS, start=1):
    for _ in range(_count):
        SAMPLE_POSTS.append({
            "userId": _user_id,
            "id": _post_id,
            "title": f"Sample post {_post_id}",
            "body": "Local fallback record used when the public API is unavailable.",
        })
        _post_id += 1
