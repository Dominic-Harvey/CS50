#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    int all_digits = 0;
    if (argc == 2)
    {
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (argv[1][i] >= '0' && argv[1][i] <= '9')
            {
                all_digits = 1;
            }
            else
            {
                printf("Ussage: /caesar key\n");
                return 1;
            }
        }
    }
    else
    {
        printf("Ussage: /caesar key\n");
        return 1;
    }

    if (all_digits == 1)
    {
        long key = strtol(argv[1], NULL, 10);
        string plaintext = get_string("plaintext: ");
        printf("ciphertext: ");
        if (key > 26)
        {
            key = key % 26;
        }

        for (int i = 0, n  = strlen(plaintext); i < n; i++)
        {
            if ((plaintext[i] >= 'a' && plaintext[i] <= 'z') || (plaintext[i] >= 'A' && plaintext[i] <= 'Z'))
            {
                if ((plaintext[i] + (int) key >= 'a' && plaintext[i] + (int) key <= 'z') || (plaintext[i] + (int) key >= 'A'
                        && plaintext[i] + (int) key <= 'Z'))
                {
                    printf("%c", plaintext[i] + (int) key);
                    
                    
                }

                else
                {
                    printf("%c", plaintext[i] + ((int) key - 26));
                }
            }
            else
            {
                printf("%c", plaintext[i]);
            }
        }

        printf("\n");

    }
}