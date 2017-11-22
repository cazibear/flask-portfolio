INSERT INTO posts (
	title,
	author,
	author_id,
	content,
	votes_up,
	votes_down
) VALUES
	('First article', 'admin', 1, 'Testing', 30, 10),
	('Second article', 'admin', 1, 'Another test...', 50, 20),
	('Third article', 'admin', 1, 'test the third', 40, 15)
;

INSERT INTO users (username, password) VALUES ("test", '$2b$12$YRDr54UNqpPs.KmAWumHweVtn7CB.zh45AiT0dZ81tgdVikcDZJ5i')