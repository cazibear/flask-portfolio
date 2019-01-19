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

INSERT INTO users (
	'username',
	'password'
) VALUES
	('alan', '$2b$12$a.XxOkaz2AdBAvUM85.a2e3nL9e5IVlLIzHL4Scsy9bwz6PJi.YLe'),
	('jane', '$2b$12$3qPMGVOAs3cCzKDqfoTxm.6igP8EttjzRFy/3p5fSUocDfGGfrIHq'),
	('dave', '$2b$12$uE3yN0yWnNVNGxwmJIVale9f1FaU/X5hDz4DedFknawXPMi7XDF3u'),
	('mary', '$2b$12$B.9UaggaFKD617IpzaMkceflLNldCVG8En9qG64sQsw3fVS4hNk/q');
