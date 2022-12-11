DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
	post_id    INTEGER PRIMARY KEY AUTOINCREMENT,
	title      TEXT,
	author_id  INTEGER,
	content    TEXT,
	posted     DATETIME DEFAULT CURRENT_TIMESTAMP,
	votes_up   INTEGER,
	votes_down INTEGER,
	FOREIGN KEY(author_id) REFERENCES users(id)
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
	user_id      INTEGER PRIMARY KEY AUTOINCREMENT,
	username     TEXT,
	password     TEXT,
	display_name TEXT,
	dob          TEXT
);

DROP VIEW IF EXISTS view_posts;
CREATE VIEW view_posts AS
    SELECT p.post_id, p.posted, p.title, p.content, u.display_name
      FROM posts p
INNER JOIN users u on p.author_id == u.user_id;
