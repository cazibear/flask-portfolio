from flask import Flask, render_template, g, request, redirect, url_for, flash, session
from functools import wraps
from __future__ import print_function
import bcrypt
import sqlite3

app = Flask(__name__)
db_location = "var/data.db"
app.secret_key = "secret"


def get_db():
	# gets a database connection
	db = getattr(g, "db", None)
	if db is None:
		db = sqlite3.connect(db_location)
		db.row_factory = sqlite3.Row  # allows for accessing columns by name and not just index
		g.db = db
	return db


@app.teardown_appcontext
def close_db(exception):
	db = getattr(g, "db", None)
	if db is not None:
		db.close()


def init_db():
	# initialises the database
	with app.app_context():
		db = get_db()
		
		# creating the database structure
		with app.open_resource("var/schema.sql", mode="r") as f:
			db.cursor().executescript(f.read())
		
		# inserting some test data
		with app.open_resource("var/sample_data.sql", mode="r") as f:
			db.cursor().executescript(f.read())
		db.commit()


def check_login(username, password):
	db = get_db()
	sql = "SELECT password FROM users WHERE username = ?;"
	result = db.cursor().execute(sql, username)
	
	if password == bcrypt.hashpw(result, result):
		return True
	else:
		return False


def requires_login(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		status = session.get("logged_in", False)
		if not status:
			return redirect(url_for(".root"))
		return f(*args, **kwargs)
	return decorated


@app.route('/')
def root():
	# displays the 10 most recent posts ordered by id
	db = get_db()
	sql = "SELECT * FROM posts ORDER BY id ASC LIMIT 10;"
	result = db.cursor().execute(sql)
	
	return render_template("index.html", results=result)


@app.route("/login/", methods=["POST", "GET"])
def login():
	session["logged_in"] = False
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		check = check_login(username, password)
		if check:
			session["logged_in"] = True
			flash("Logged in")
			redirect(url_for("root"))
		else:
			flash("Username or password invalid")
			render_template("login.html")
	else:
		render_template("login.html")


@app.route("/post/", methods=["POST", "GET"])
@requires_login
def post_article():
	if request.method == "POST":
		print("post")
		form_title = request.form["title"]
		form_content = request.form["content"]
		form_author = request.form["author"]
		
		sql = "INSERT INTO posts (title, author, content) VALUES (?, ?, ?)"
		try:
			db = get_db()
			db.cursor().execute(sql, (form_title, form_content, form_author))
			db.commit()
			print("success")
			flash("Article successfully posted!")
		except sqlite3.Error as e:
			print("fail")
			flash(e)
		
		return render_template("post_article.html")
	else:
		print("get")
		return render_template("post_article.html")


@app.route("/articles/all/")
@app.route("/articles/all/<string:sort>")
def all_articles(sort=""):
	# displays all of the posts defaulting to sorting by time
	
	method = "id"  # sorting method
	if sort.lower() == "title":
		method = "title"
	if sort.lower() == "author":
		method = "author"
	if sort.lower() == "score":
		method = "score"
	sql = "SELECT *, (votes_up - votes_down) AS score FROM posts ORDER BY {};".format(method)
	
	db = get_db()
	result = db.cursor().execute(sql)
	return render_template("all_articles.html", results=result, method=method)


if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)
