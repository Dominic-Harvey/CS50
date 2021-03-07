from cs50 import get_int
height = 0

while height < 1 or height > 8 :
    height = get_int("Height: ")

spaces = height
blocks = 1
for j in range(height):
    for i in range(spaces-1):
        print(" ", end ="")

    spaces = spaces - 1
    print("#" * blocks, end="")
    print("  ", end="")
    print("#" * blocks, end="")
    blocks = blocks + 1
    print()