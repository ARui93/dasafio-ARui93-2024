#include <stdio.h>

int main() {
    int matriz[10][10] = {0};  // Inicializa todos os elementos com zero
    int maxValor = matriz[0][0];
    int linhaMax = 0;
    int colunaMax = 0;

    // Lê a matriz
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 10; j++) {
            printf("Digite o valor da matriz [%d][%d]: ", i, j);
            scanf("%d", &matriz[i][j]);

            if (matriz[i][j] > maxValor) {
                maxValor = matriz[i][j];
                linhaMax = i;
                colunaMax = j;
            }
        }
    }

    // Exibe a localizacao do maior valor
    printf("A localizacao do maior valor (%d) e na linha %d e coluna %d.\n", maxValor, linhaMax, colunaMax);

    return 0;
}


