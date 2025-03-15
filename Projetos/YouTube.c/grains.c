#include "grains.h"

// Função para calcular o número de grãos em um determinado quadrado
uint64_t square(uint8_t index)
{
    // Verifica se o índice está dentro do intervalo válido (1 a 64)
    if (index < 1 || index > 64)
    {
        return 0;
    }
    // Calcula o número de grãos no quadrado usando o deslocamento de bits (bit shift)
    return 1ULL << (index - 1);
}

// Função para calcular o número total de grãos em todo o tabuleiro de xadrez
uint64_t total(void)
{
    // Inicializa a variável para armazenar o número total de grãos
    uint64_t total_grains = 0;
    // Itera sobre cada quadrado do tabuleiro de xadrez e adiciona o número de grãos em cada quadrado ao total
    for (uint8_t i = 1; i <= 64; i++)
    {
        total_grains += square(i);
    }
    return total_grains;
}
