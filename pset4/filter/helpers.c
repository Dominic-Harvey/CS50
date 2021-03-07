#include <stdio.h>
#include "helpers.h"
#include "math.h"
#include <string.h>
#include <stdlib.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            double grey_value = round((double)((image[i][j].rgbtRed) + (image[i][j].rgbtGreen) + (image[i][j].rgbtBlue))/3);
            image[i][j].rgbtRed = grey_value;
            image[i][j].rgbtGreen = grey_value;
            image[i][j].rgbtBlue = grey_value;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            double sepiaRed = round(((double).393 * (image[i][j].rgbtRed)) + (.769 * (image[i][j].rgbtGreen)) + (.189 * (image[i][j].rgbtBlue)));
            double sepiaGreen = round(((double).349 * (image[i][j].rgbtRed)) + (.686 * (image[i][j].rgbtGreen)) + (.168 * (image[i][j].rgbtBlue)));
            double sepiaBlue = round(((double).272 * (image[i][j].rgbtRed)) + (.534 * (image[i][j].rgbtGreen)) + (.131 * (image[i][j].rgbtBlue)));

            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }

            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }

            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width/2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width-j-1];
            image[i][width-j-1] = temp;
        }
    }
    return;
}


// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE imagecopy[height][width];
    memcpy(imagecopy, image, sizeof(RGBTRIPLE) * height * width);

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float pixel_count = 0.0;
            int red_value = 0;
            int green_value = 0;
            int blue_value = 0;

            for (int h = -1; h < 2; h++)
            {
                for (int w = -1; w < 2; w++)
                {
                    if (i + h != height && i + h != -1 && j + w != width && j + w != -1)
                    {
                        red_value = red_value + imagecopy[i+h][j+w].rgbtRed;
                        green_value = green_value + imagecopy[i+h][j+w].rgbtGreen;
                        blue_value = blue_value + imagecopy[i+h][j+w].rgbtBlue;
                        pixel_count++;
                    }
                }
            }

            image[i][j].rgbtRed = round((double)(red_value/pixel_count));
            image[i][j].rgbtGreen = round((double)(green_value/pixel_count));
            image[i][j].rgbtBlue = round((double)(blue_value/pixel_count));
        }
    }

    return;
}