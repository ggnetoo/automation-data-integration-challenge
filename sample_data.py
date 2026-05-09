SAMPLE_USERS = [
    {
        "id": 1,
        "name": "Leanne Graham",
        "email": "Sincere@april.biz",
        "address": {"city": "Gwenborough"},
        "company": {"name": "Romaguera-Crona"},
    },
    {
        "id": 2,
        "name": "Ervin Howell",
        "email": "Shanna@melissa.tv",
        "address": {"city": "Wisokyburgh"},
        "company": {"name": "Deckow-Crist"},
    },
    {
        "id": 3,
        "name": "Clementine Bauch",
        "email": "Nathan@yesenia.net",
        "address": {"city": "McKenziehaven"},
        "company": {"name": "Romaguera-Jacobson"},
    },
    {
        "id": 4,
        "name": "Patricia Lebsack",
        "email": "Julianne.OConner@kory.org",
        "address": {"city": "South Elvis"},
        "company": {"name": "Robel-Corkery"},
    },
    {
        "id": 5,
        "name": "Chelsey Dietrich",
        "email": "Lucio_Hettinger@annie.ca",
        "address": {"city": "Roscoeview"},
        "company": {"name": "Keebler LLC"},
    },
    {
        "id": 6,
        "name": "Mrs. Dennis Schulist",
        "email": "Karley_Dach@jasper.info",
        "address": {"city": "South Christy"},
        "company": {"name": "Considine-Lockman"},
    },
    {
        "id": 7,
        "name": "Kurtis Weissnat",
        "email": "Telly.Hoeger@billy.biz",
        "address": {"city": "Howemouth"},
        "company": {"name": "Johns Group"},
    },
    {
        "id": 8,
        "name": "Nicholas Runolfsdottir V",
        "email": "Sherwood@rosamond.me",
        "address": {"city": "Aliyaview"},
        "company": {"name": "Abernathy Group"},
    },
    {
        "id": 9,
        "name": "Glenna Reichert",
        "email": "Chaim_McDermott@dana.io",
        "address": {"city": "Bartholomebury"},
        "company": {"name": "Yost and Sons"},
    },
    {
        "id": 10,
        "name": "Clementina DuBuque",
        "email": "Rey.Padberg@karina.biz",
        "address": {"city": "Lebsackbury"},
        "company": {"name": "Hoeger LLC"},
    },
]

SAMPLE_POSTS = [
    {
        "userId": ((post_id - 1) // 10) + 1,
        "id": post_id,
        "title": f"Sample post {post_id}",
        "body": "Local fallback record used when the public API is unavailable.",
    }
    for post_id in range(1, 101)
]

