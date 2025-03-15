#include <stdio.h>

int main()
{
	float deltas, deltat, vm;
	printf("Entre com o delta S ");
	scanf("%f", &deltas);
	printf("Entre com o delta T");
	scanf("%f", &deltat);
	vm = deltas / deltat;
	printf("A velocidade media e %f\n", vm);
	return 0;
}
