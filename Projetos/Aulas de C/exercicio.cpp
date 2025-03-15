#include <iostream>
#include <cstdlib>  // Para a função rand()
#include <ctime>    // Para a função time()

// Função que acrescenta o valor do segundo número ao primeiro número
void acrescentarValor(int &num1, int num2) {
    num1 += num2;  // Soma o valor de num2 ao valor de num1
}

int main() {
    // Inicializa o gerador de números aleatórios
    std::srand(std::time(0));

    // Loop para gerar e testar 10 pares de números aleatórios
    for (int i = 0; i < 10; ++i) {
        int num1 = std::rand() % 100;  // Gera um número aleatório para num1 entre 0 e 99
        int num2 = std::rand() % 100;  // Gera um número aleatório para num2 entre 0 e 99

        std::cout << "Antes da função: num1 = " << num1 << ", num2 = " << num2 << std::endl;

        // Chama a função que acrescenta o valor de num2 a num1
        acrescentarValor(num1, num2);

        std::cout << "Depois da função: num1 = " << num1 << std::endl << std::endl;
    }

    return 0;
}
