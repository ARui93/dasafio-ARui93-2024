#include "resistor_color.h"

// Função para obter o valor numérico associado a uma cor específica
int color_code(resistor_band_t color)
{
    // Switch case para mapear a cor para o valor numérico associado
    switch (color)
    {
    case BLACK:
        return 0;
    case BROWN:
        return 1;
    case RED:
        return 2;
    case ORANGE:
        return 3;
    case YELLOW:
        return 4;
    case GREEN:
        return 5;
    case BLUE:
        return 6;
    case VIOLET:
        return 7;
    case GREY:
        return 8;
    case WHITE:
        return 9;
    }
    // Retorna -1 se a cor não for reconhecida
    return -1;
}

// Função para listar as diferentes cores da banda
resistor_band_t *colors(void)
{
    // Criando uma matriz de cores das bandas
    static resistor_band_t band_colors[] = {
        BLACK, BROWN, RED, ORANGE, YELLOW,
        GREEN, BLUE, VIOLET, GREY, WHITE};
    // Retornando a matriz
    return band_colors;
}
