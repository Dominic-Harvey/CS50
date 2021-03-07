// Implements a dictionary's functionality

#include <stdbool.h>
#include <strings.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 65536; //2^16

// Hash table
node *table[N];

//flag for if the dict has been loaded yet
extern int loaded;
int loaded = 0;

//counter for how many words added into the dict
extern int number_of_words;
int number_of_words = 0;


// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    int index = 0;
    //assigns file pointer to the dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        printf("Could Not Open File\n");
        return false;
    }

    //making a buffer for the new words being loaded
    char buffer[LENGTH + 1];

    //iterates over all of the strings in the file saving them into the buffer
    while (fscanf(file, "%s", buffer) != EOF)
    {
         //creating a new node to add to the hash table
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            unload();
            return false;
        }


        //copying the new word into the node
        strcpy(new_node->word, buffer);

        new_node->next = NULL;
        
        number_of_words++;
        
        //getting the hash value for the new word to add
        index = hash(new_node->word);

        

        if (table[index] == NULL)
        {
            table[index] = new_node;
        }
        else
        {
            new_node->next = table[index];
            table[index] = new_node;
        }
    }
    fclose(file);
    loaded = 1;
    return true;
}

// Hashes word to a number//Hash function from reddit https://www.reddit.com/r/cs50/comments/1x6vc8/pset6_trie_vs_hashtable/cf9nlkn/
unsigned int hash(const char *word)
{
    //Section 6.6 of The C Programming Language
    unsigned int hashval;
    
    for (hashval = 0; *word != '\0'; word++)
    {
        hashval = *word + 31 * hashval;
    }
    
    return hashval % N;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return number_of_words;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int n = strlen(word);
    char word_copy[LENGTH + 1];
    for (int i = 0; i < n; i++)
    {
        word_copy[i] = tolower(word[i]);
    }

    word_copy[n] = '\0';

    int index = hash(word_copy);

    node *crawler = table[index];

    while (crawler != NULL)
    {
        if (strcasecmp(crawler->word, word_copy) == 0)
        {
            return true;
        }
        else
        {
            crawler = crawler->next;
        }
    }
    
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node* temp;
    node* crawler;

    
    for(int n = 0; n < N; n++)
    {   
        if (table[n] != NULL)
        {    
            // If only 1 node free it
            crawler = table[n];
            while (crawler != NULL)
            {
                temp = crawler->next;
                free(crawler);
                crawler = NULL;
                crawler = temp;
            }
            
            // free last node in list
            temp = crawler;
        }        
    }

    return true;
}
