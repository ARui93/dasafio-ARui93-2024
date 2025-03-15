#ifndef RESISTOR_COLOR_H
#define RESISTOR_COLOR_H

// Enumeração para representar as cores das bandas dos resistores
typedef enum
{
    BLACK,  // 0
    BROWN,  // 1
    RED,    // 2
    ORANGE, // 3
    YELLOW, // 4
    GREEN,  // 5
    BLUE,   // 6
    VIOLET, // 7
    GREY,   // 8
    WHITE   // 9
} resistor_band_t;

// Função para obter o valor numérico associado a uma cor específica
int color_code(resistor_band_t color);

// Função para listar as diferentes cores da banda
resistor_band_t *colors(void);

#endif
