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
		name_data = c.fetchall()
		names = []
		for name_row in name_data:
			names.append(name_row["name"])

		# header of table
		# ------------------------------------------------------------
		line = "┌"
		line += "┬".join(["─" * ROW_LENGTH for i in range(len(names))])
		line += "┐"
		print(line)

		line = "│"
		line += "│".join([("{:" + str(ROW_LENGTH) + "}").format(
			names[i]) for i in range(len(names))])
		line += "│"
		print(line)

		line = "╞"
		line += "╪".join(["═" * ROW_LENGTH for i in range(len(names))])
		line += "╡"
		print(line)
		# ------------------------------------------------------------

		# body of table
		# ------------------------------------------------------------
		for table_row in table_data:
			# for each row in table
			line = "│"
			for column in table_row:\
				# for each column in the row
				if type(column) is int:
					line += ("{:" + str(ROW_LENGTH) + "d}").format(column)
				elif type(column) is float:
					line += ("{:" + str(ROW_LENGTH - 3) + ".3f}").format(column)
				elif type(column) is str:
					line += ("{:" + str(ROW_LENGTH) + "." + str(ROW_LENGTH) + "}").format(column)
				elif type(column) is bytes:
					line += ("{:" + str(ROW_LENGTH) + "." + str(ROW_LENGTH) + "}").format(column.decode())
				elif column is None:
					line += ("{:^" + str(ROW_LENGTH) + "}").format("NULL")
				else:
					raise TypeError("The type " + str(type(column)) +
							"could not be handled.")
				line += "│"
				a = str(ROW_LENGTH) + "." + str(ROW_LENGTH)
				b = ".".join([str(ROW_LENGTH), str(ROW_LENGTH)])
			print(line)
		# ------------------------------------------------------------

		# end of table
		line = "└"
		line += "┴".join(["─" * ROW_LENGTH for i in range(len(names))])
		line += "┘"
		print(line)
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
