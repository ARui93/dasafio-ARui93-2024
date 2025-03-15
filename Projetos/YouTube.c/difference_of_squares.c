#include "difference_of_squares.h"

// Função para calcular a soma dos quadrados dos primeiros N números naturais
unsigned int sum_of_squares(unsigned int number)
{
    unsigned int sum = 0;
    for (unsigned int i = 1; i <= number; i++)
    {
        sum += i * i;
    }
    return sum;
}

// Função para calcular o quadrado da soma dos primeiros N números naturais
unsigned int square_of_sum(unsigned int number)
{
    unsigned int sum = 0;
    for (unsigned int i = 1; i <= number; i++)
    {
        sum += i;
    }
    return sum * sum;
}

// Função para calcular a diferença entre o quadrado da soma e a soma dos quadrados
unsigned int difference_of_squares(unsigned int number)
{
    return square_of_sum(number) - sum_of_squares(number);
}
