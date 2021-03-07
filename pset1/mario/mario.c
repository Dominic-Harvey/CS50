#include <stdio.h>
#include <cs50.h>

void block(int i);

int main(void)
{
    int height;
    do
    {
        height = get_int("Enter Height Of Pyramid\n");

    }
    while (height < 1 || height > 8);

    for (int i = 0; i < height; i++)
    {
        for (int s = height - 1 - i; s > 0; s--)//for loop for printing spaces on left side
        {
            printf(" ");
        }

        block(i);

        printf("  ");

        block(i);

        printf("\n");
    }
}

void block(int i)//funcion for priting the hashes depedning on the inputed height
{
    for (int b = 0; b < i + 1; b++)
    {
        printf("#");
    }
}
