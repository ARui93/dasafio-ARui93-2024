#include <stdio.h>

int main() {
    int a, b;

    printf("Informe o valor de A: ");
    scanf("%d", &a);
    printf("Informe o valor de B: ");
    scanf("%d", &b);
    printf("O valor A: %d\n", a + b - a);
    printf("O valor B: %d\n", b + a - b);
	//	Explica��o do professor.
	//	float A,B,AUX;
	//	printf("Informe o valor de A: ");
	//	scanf("%d", &a);
	//	printf("Informe o valor de B: ");
	//	scanf("%d", &b);
	//	AUX = A
	//	A = B
	//	B = AUX
	//	printf("A = %f\n", A)
	//	printf("B = %f\n", B)

	return 0;
}
