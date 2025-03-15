#include <stdio.h>

main()
{

	float custo, imposto, revenda, preco;

	printf("Informe o valor do preco de fabrica: R$");
	scanf("%f", &custo);

	imposto = custo * 45 / 100;
	revenda = custo * 28 / 100;
	preco = custo + imposto + revenda;

	printf("Para esse valor o imposto e de R$ %.2f\n", imposto);
	printf("Para esse valor o revendedor tem um lucro de R$ %.2f\n", revenda);
	printf("O valor de venda do carro e: R$ %.2f", preco);

	return 0;
}
