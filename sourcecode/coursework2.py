from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)
db_location = "var/data.db"


def get_db():
	db = getattr(g, "db", None)
	if db is None:
		db = sqlite3.connect(db_location)
		g.db = db
	return db


@app.teardown_appcontext
def close_db(exception):
	db = getattr(g, "db", None)
	if db is not None:
		db.close()


def init_db():
	with app.app_context():
		db = get_db()
		
		with app.open_resource("var/schema.sql", mode="r") as f:
			db.cursor().executescript(f.read())
		
		with app.open_resource("var/main_posts.sql", mode="r") as f:
			db.cursor().executescript(f.read())
		db.commit()


@app.route('/')
def root():
	db = get_db()
	sql = "SELECT * FROM posts;"
	result = db.cursor().execute(sql)
	
	return render_template("index.html", results=result)


if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)
