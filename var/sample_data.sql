INSERT INTO posts (
	title,
	author_id,
	content
) VALUES 
	('First article',  1, 'Testing'),
	('Second article', 1, 'Another test...'),
	('Third article',  1, 'test the third')
;

INSERT INTO users (
	username,
	display_name,
	password
) VALUES
	('alan', 'alan', '$2b$12$a.XxOkaz2AdBAvUM85.a2e3nL9e5IVlLIzHL4Scsy9bwz6PJi.YLe'),
	('jane', 'jane', '$2b$12$3qPMGVOAs3cCzKDqfoTxm.6igP8EttjzRFy/3p5fSUocDfGGfrIHq'),
	('dave', 'dave', '$2b$12$uE3yN0yWnNVNGxwmJIVale9f1FaU/X5hDz4DedFknawXPMi7XDF3u'),
	('mary', 'mary', '$2b$12$B.9UaggaFKD617IpzaMkceflLNldCVG8En9qG64sQsw3fVS4hNk/q')
;
