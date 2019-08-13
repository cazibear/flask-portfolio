from __future__ import print_function
from flask import *
from functools import wraps
import bcrypt
import sqlite3

app = Flask(__name__)
db_location = "var/data.db"
app.secret_key = "secret"


# ---------------------------------------- Helper functions
def get_db():
	""" Returns a connection to the database """
	db = getattr(g, "db", None) # "g" being globals
	if db is None:
		db = sqlite3.connect(db_location)
		db.row_factory = sqlite3.Row  # allows for accessing columns by name
		g.db = db
	return db


@app.teardown_appcontext
def close_db(exception):
	""" Runs upon shutting down the application closing the database properly """
	db = getattr(g, "db", None)
	if db is not None:
		db.close()


def check_login(username, password):
	c = get_db().cursor()
	sql = "SELECT * FROM users WHERE username = ?;"
	c.execute(sql, (username,))
	result = c.fetchone()

	if result["password"] == bcrypt.hashpw(
			password.encode("utf-8"),
			result["password"]):
		return True
	else:
		return False


def create_account(username, password):
	password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

	try:
		sql = "INSERT INTO users (username, password) VALUES (?, ?);"
		db = get_db()
		db.execute(sql, (username, password))
		db.commit()
		return True
	except Exception as e:
		print(e)
		return False


def requires_login(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		status = session.get("logged_in", False)
		if not status:
			return redirect(url_for("root"))
		return f(*args, **kwargs)
	return decorated
# ----------------------------------------


# ---------------------------------------- Page routing
@app.route("/")
def root():
	# displays the 10 most recent posts ordered by id
	db = get_db()
	sql = "SELECT * FROM posts ORDER BY id ASC LIMIT 10;"
	result = db.cursor().execute(sql)

	return render_template("index.html", results=result)


@app.route("/login/", methods=["POST", "GET"])
def login():
	# Page for users to login
	session["logged_in"] = False
	if request.method == "POST":
		# get user details
		username = request.form["username"]
		password = request.form["password"]
		if "" in [username, password]:
			# if any of the form is empty
			flash("Please fill in the required fields.")
			return render_template("register.html")
		check = check_login(username, password)
		del username, password

		if check:
			# if the check was successful
			session["logged_in"] = True
			flash("Logged in successfully")
			return redirect(url_for("root"))
		else:
			# if unsuccessful
			flash("Username or password invalid")
			return render_template("login.html")
	else:
		return render_template("login.html")


@app.route("/logout/")
def logout():
	""" Logs the user out and sends them back to the homepage """
	session["logged_in"] = False
	flash("You are now logged out.")
	return redirect(url_for("root"))


@app.route("/register/", methods=["POST", "GET"])
def register():
	""" Registers a user in the database hashing and salting their password """
	if request.method == "POST":
		# get user details
		username = request.form["username"]
		password = request.form["password"]
		print(repr(username), repr(password))
		if "" in [username, password]:
			# if any of the form is empty
			flash("Please fill in the required fields.")
			return render_template("register.html")
		status = create_account(username, password)
		del username, password

		if status:
			flash("Account created")
			return redirect(url_for("login"))
		else:
			flash("Problem creating account.")
			return render_template("register.html")
	else:
		return render_template("register.html")


@app.route("/post/", methods=["POST", "GET"])
@requires_login
def post_article():
	if request.method == "POST":
		form_title = request.form["title"]
		form_content = request.form["content"]
		form_author = request.form["author"]
		
		sql = "INSERT INTO posts (title, author, content) VALUES (?, ?, ?)"
		try:
			db = get_db()
			db.execute(sql, (form_title, form_content, form_author))
			db.commit()
			flash("Article successfully posted!")
		except sqlite3.Error as e:
			flash(e)
		
		return render_template("post_article.html")
	else:
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
# ----------------------------------------


if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)
