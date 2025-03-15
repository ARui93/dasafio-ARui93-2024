#include "leap.h"
#include <stdio.h>

bool leap_year(int year)
{

    if ((year % 4 == 0 && year % 100 != 0) || (year % 400 == 0))
    {
        return true;
        printf("Ano Bissexto.");
    }
    else
    {
        return false;
        printf("Ano não bissexto.");
    }

    return 0;
}