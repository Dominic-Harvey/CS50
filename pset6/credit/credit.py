from cs50 import get_string
from sys import exit

card_issuer = {
    51: "MASTERCARD",
    52: "MASTERCARD",
    53: "MASTERCARD",
    54: "MASTERCARD",
    55: "MASTERCARD",
    4: "VISA",
    34: "AMEX",
    37: "AMEX"
}

number = get_string("Number: ")
if len(number) < 13 or len(number) > 16:
    print("INVALID")
    exit()

valid = False
total = 0

for i in range(len(number)-1, -1, -2):
    total = total + int(number[i])

for i in range(len(number)-2, -1, -2):
    if int(number[i])*2 > 9:
        temp = str(int(number[i])*2)
        total = int(temp[0]) + int(temp[1]) + total
    else:
        total = int(number[i])*2 + total

if (total % 10) == 0:
    identifying_number = (int(number[0])*10) + int(number[1])
    if identifying_number in card_issuer:
        print(f"{card_issuer[identifying_number]}")
    else:
        print("VISA")
else:
    print("INVALID")