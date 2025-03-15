#include <stdio.h>

main()
{
	float saldo, nsaldo;
	printf("Informe qual o valor da aplicacao: \n");
	scanf("%f", &saldo);
	nsaldo = saldo + saldo * 0.01;
	printf("Saldo reajustado: %.2f\n", nsaldo);
}
