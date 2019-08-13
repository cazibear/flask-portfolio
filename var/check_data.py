
from sys import argv
import sqlite3

if __name__ == '__main__':
	"""Tool for checking the tables in the database
	
	With no argument this prints out the sql used to create each table.
	With an argument this takes the first argument as a name of a table
	and prints out the records in that table."""
	db = sqlite3.connect("data.db")

	db.row_factory = sqlite3.Row
	c = db.cursor()
	ROW_LENGTH = 15

	if len(argv) > 1:
		# if a table is selected with argument
		# get table data
		sql = "SELECT * FROM {};".format(argv[1])
		c.execute(sql)
		table_data = c.fetchall()

		# getting column names for the table
		c.execute("PRAGMA table_info({});".format(argv[1]))
		table_info = c.fetchall()
		names = [row["name"] for row in table_info]
		
		print("Fields:", ", ".join(names))
		print()
		
		for table_row in table_data:
			# for each row in table
			print(", ".join(list(map(str, table_row))))
	else:
		# otherwise show schemas
		sql = "SELECT * FROM sqlite_master;"
		c.execute(sql)
		table_data = c.fetchall()
		for result in table_data:
			print("{}: {}".format(result["type"].title(), result["name"]))
			print("SQL:")
			print(result["sql"])
			print()
