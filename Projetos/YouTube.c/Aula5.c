#include <stdio.h>

main()
{
	float prestacao, valor, taxa;
	int tempo;
	printf("Informe o valor de preatacao (R$): ");
	scanf("%f", &valor);
	printf("Quantos dias em atraso? ");
	scanf("%d", &tempo);
	printf("Informe o valor da taxa (%): ");
	scanf("%f", &taxa);
	prestacao = valor + (valor * (taxa / 100) * tempo);
	printf("A prestacao com a taxa de juros (R$): %.2f\n", prestacao);

	return 0;
}
