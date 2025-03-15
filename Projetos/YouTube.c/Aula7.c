#include <stdio.h>

main()
{
	float s_minimo, s_funcionario, quant_s;
	printf("Informe o salario minimo atual: R$ ");
	scanf("%f", &s_minimo);
	printf("Informe o seu salario atual: R$ ");
	scanf("%f", &s_funcionario);
	quant_s = s_funcionario / s_minimo;
	printf("Seu salario equivale a %.2f salarios minimos.", quant_s);

	return 0;
}
