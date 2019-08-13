import sqlite3


def init_db():
	""" Initialises the database with tables and data"""
	db = sqlite3.connect("var/data.db")
	cur = db.cursor()

	# creating the database structure
	print("Running schema")
	with open("var/schema.sql") as f:
		cur.executescript(f.read())

	# inserting some test data
	print("Running sample data")
	with open("var/sample_data.sql") as f:
		cur.executescript(f.read())
	db.commit()


if __name__ == "__main__":
	init_db()
