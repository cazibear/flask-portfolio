DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
	post_id    INTEGER PRIMARY KEY AUTOINCREMENT,
	title      TEXT,
	author_id  INTEGER,
	content    TEXT,
	posted     DATETIME DEFAULT CURRENT_TIMESTAMP,
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
