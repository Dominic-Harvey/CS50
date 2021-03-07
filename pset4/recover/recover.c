#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdint.h>

#define BUFFER_SIZE 512

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Remember filenames
    char *infile = argv[1];
    int outfile = 0;

    // Open input file
    FILE *file = fopen(infile, "r");
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s\n", infile);
        return 1;
    }

    fseek(file, 0, SEEK_END); // seek to end of file
    int file_size = ftell(file); // get current file pointer
    fseek(file, 0, SEEK_SET); // seek back to beginning of file

    unsigned char buffer[BUFFER_SIZE];
    int jpg_index = 0;
    char *filename = "000.jpg";
    filename = (char *)malloc((strlen(filename) + 1) * sizeof(char));
    int jpg_open = 0;
    FILE *img = NULL;

    while (fread(buffer, BUFFER_SIZE, 1, file) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (jpg_open == 1)
            {
                fclose(img);
            }
            else
            {
                jpg_open  = 1;
            }

            sprintf(filename, "%03i.jpg", jpg_index);
            img = fopen(filename, "a");
            jpg_index++;

        }
        if (jpg_open == 1)
        {

            fwrite(&buffer, BUFFER_SIZE, 1, img);
        }

    }

    free(filename);
    fclose(img);


    fclose(file);

    return 0;
}
