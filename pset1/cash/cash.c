#include <stdio.h>
#include <cs50.h>
#include <math.h>
 
int change_calc(int denomination, int *change, int coins);
 
int main(void)
{
    float dollars;
    do 
    {
        dollars = get_float("Change Owed:");
    }
    while (dollars < 0);
 
    int change = round(dollars * 100);
    int coins = 0;
 
    int denominations[4] = {25, 10, 5, 1};
 
    for (int i = 0; 4 > i; i++) 
    {
        coins = change_calc(denominations[i], &change, coins);
 
        if (change == 0) 
        {
            break;
        }
    }
 
    printf("%i\n", coins);
}
 
int change_calc(int denomination, int *change, int coins) 
{
 
    do 
    {
        if (change == 0) 
        {
            break;
        }
        if (denomination <= *change)
        {
            *change = (*change) - denomination;
            coins++;
        }
        else 
        {
            break;
        }
    }
    while ((!(*change) % denomination == 0));
 
    return coins;
}
