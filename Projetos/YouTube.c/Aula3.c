#include <stdio.h>

int main()
{
    int numero1, numero2, soma, sub, multi, resto;
    float div;

    printf("Digite um numero: ");
    scanf("%d", &numero1);

    printf("Digite mais um numero: ");
    scanf("%d", &numero2);

    soma = numero1 + numero2;
    sub = numero1 - numero2;
    multi = numero1 * numero2;
    div = (float)numero1 / numero2;
    resto = numero1 % numero2;

    printf("Soma: %i\n", soma);
    printf("Subtracao: %i\n", sub);
    printf("Multiplicacao: %i\n", multi);
    printf("Divisao: %.2f\n", div);
    printf("Resto: %i\n", resto);

    return 0;
}
