DROP TABLE IF EXISTS posts;

CREATE TABLE posts
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    votes_up   INTEGER,
    votes_down INTEGER,
    title   TEXT,
    author  TEXT,
    subject TEXT,
    tags    TEXT
);
