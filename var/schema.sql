DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
	post_id    INTEGER PRIMARY KEY AUTOINCREMENT,
	title      TEXT,
	author_id  INTEGER,
	content    TEXT,
	posted     DATETIME DEFAULT CURRENT_TIMESTAMP,
	votes_up   INTEGER DEFAULT 0,
	votes_down INTEGER DEFAULT 0,
	FOREIGN KEY(author_id) REFERENCES users(user_id)
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
    SELECT p.post_id, p.posted, p.title, p.content, p.votes_up, p.votes_down, u.display_name
      FROM posts p
INNER JOIN users u on p.author_id == u.user_id;
