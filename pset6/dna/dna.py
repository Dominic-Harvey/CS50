import csv
from sys import argv, exit
import re

def main(argv):
    if len(argv) != 3: #makes sure 2 args have been given
        print("Usage: python dna.py data.csv sequence.txt")
        exit(0)

    STR_id, STR_pairs = count_STR(argv[1], argv[2])
    check_database(argv[1], STR_id)

def count_STR(database, string):

    #reads header of database too make a list of diffrent STRs contained in the database which will need to be searched for
    with open(database, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            del row[0]
            STR_pairs = row
            break

    #reading the unidentified DNA into variable
    with open(string, 'r') as textfile:
        filetext = textfile.read()
        filetext = ''.join(filetext.split())

        STR_id = []
        index = 0

        for pair in STR_pairs:
            p = rf'({pair})\1*'#defines the STR pair to search for
            pattern = re.compile(p)
            match = [match for match in pattern.finditer(filetext)]#creating a list of match objects
            max = 0
            for i in range(len(match)):
                if match[i].group().count(pair) > max:
                    max = match[i].group().count(pair)#updates the max variable with the longest consecutive occurrences of STR pair in the match list
            STR_id.append(str(max))#appends the max number into a list for later use

    return STR_id, STR_pairs

def check_database(database, STR_id):

    #creates a dictionary where the key is the persons STR pairs and the value is their name
    dict_of_STR_pairs = {}
    with open(database, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            dict_of_STR_pairs[tuple(row[1:len(row)])] = row[0]

    #checks and prints the name of the person if there is a matching STR
    if tuple(STR_id) in dict_of_STR_pairs:
        print(dict_of_STR_pairs[tuple(STR_id)])
    else:
        print("No Match")

main(argv)