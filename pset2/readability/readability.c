#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);
    float index = 0.0588 * ((float)letters/(float)words*100) - 0.296 * ((float)sentences/(float)words*100) - 15.8;
    int grade = roundf(index);

    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n",grade);
    }

}

int count_letters(string text)
{
    int letters = 0;
    for (int i = 0, n  = strlen(text); i < n; i++)
    {
        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
        {
            letters++;
        }
    }
   return letters;
}

int count_words(string text)
{
    int words = 1;
    for (int i = 0, n  = strlen(text); i < n; i++)
    {
        if (text[i] == ' ')
        words++;
    }
    return words;
}

int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0, n  = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        sentences++;
    }
    return sentences;
}