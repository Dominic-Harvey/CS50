from sys import argv, exit
import cs50
import csv

def main(argv):

    if len(argv) != 2: #makes sure 2 args have been given
        print("Please provide a valid CSV to load")
        exit(0)

    # Create database
    open(f"students.db", "w").close()
    db = cs50.SQL("sqlite:///students.db")
    db.execute("CREATE TABLE students(id INTEGER PRIMARY KEY AUTOINCREMENT, first VARCHAR(255), middle VARCHAR(255), last VARCHAR(255), house VARCHAR(10), birth INTEGER)")

    with open(argv[1], "r") as students:
        reader = csv.DictReader(students)
        for row in reader:
            name_list = row["name"].split()

            first_name = name_list[0]

            if len(name_list) == 3:
                middle_name = name_list[1]
                last_name = name_list[2]
            else:
                middle_name = None
                last_name = name_list[1]

            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", first_name, middle_name, last_name, row["house"], row["birth"])

main(argv)