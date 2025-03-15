#include <stdio.h> 
#include <stdlib.h>
int main(void)
{
	int n = 10; // atribuindo um valor para a variavèl 
	float n2 = 6.79; // float é uma variavél que possui casas decimais
	char letra = 'a'; // variavél do tipo caracter
	char frase[10] = "Boa noite!";
	double n3 = 1.23456;

	
	printf("Hello world!\n");
	
	printf("Exibindo o numero inteiro %d\n",n);
	printf("Exibindo um numero real %f\n",n2);
	printf("Exibendo um caracter %c\n",letra);
	printf("%s\n",frase);
	printf("Exibindo a variavel do tipo double %f\n",n3);
	
	printf("Valores: %d\n %f\n %c\n %s\n %f\n",n ,n2, letra ,frase,n3);
		
	system("pause"); //Somente para Windows
	return 0;
}
