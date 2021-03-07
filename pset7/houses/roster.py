from sys import argv, exit
import cs50
import pprint

def main():

    valid_houses = ["gryffindor", "hufflepuff", "ravenclaw", "slytherin"]

    house = argv[1].lower()

    if house not in valid_houses:
        print("Please provide the name of a valid House")
        exit(0)
    if len(argv) != 2:
        print("Ussage: roster.py house")
        exit(0)

    db = cs50.SQL("sqlite:///students.db")
    querry = db.execute(f"SELECT * FROM students WHERE house = '{house.capitalize()}' ORDER BY LAST;")

    for row in querry:
        does_this_person_have_a_middle_name = lambda a: (a + " ") if a != None else "" 
        print(row["first"] + " " + does_this_person_have_a_middle_name(row["middle"]) + row["last"] + ", born", row["birth"])

        #print(row["first"] + " ", end='')
        #if row["middle"] != None:
        #    print(row["middle"] + " ", end='')
        #print(row["LAST"] + ", born", row["birth"])

main()