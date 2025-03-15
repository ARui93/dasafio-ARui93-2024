#include<stdio.h>
#include<stdlib.h>

int main(){
/*
    int num1 = 10; //Atribuindo valor para a variável.
    float num2 = 6.79; //Float é uma variável que tem casas decimais.
    char letra = 'a'; //Variável tipo caracter.
    char frase[10] = "Boa noite!";
    double num3 = 1.23456; // Variavél real com precisão dupla.
*/
    int valor1, valor2, soma, sub, mult, div, resto, num, dia;
    float nota1, nota2, media;

/*
    //Uso do comando printf com diversas variáveis.
    printf("Hello Word!\n");
    printf("Exibendo o numero Inteiro %d\n.", num1);
    printf("Exibendo o numero Float %.2f\n.", num2); // Quando float podemos usar o %.2f, significa que vai ter apenas 2 digitos depois do ponto(6.79), 
    //não usando isso aparece 6 digitos(6.790000).
    printf("Exibindo o caracter %c\n.", letra);
    printf("%s\n", frase);
    printf("Exibindo variavel do tipo double %f\n", num3);
    printf("Valores: %d %.2f %c %s %f\n", num1,num2,letra,frase,num3);

//Utilização de scanf.
    printf(" Digite um valor inteiro: ");
    scanf("%d", &valor1);
    printf(" Digite outro valor inteiro: ");
    scanf("%d", &valor2);

//Operações aritméticas
    soma = valor1 + valor2;
    sub = valor1 - valor2;
    mult = valor1 * valor2;
    div = valor1 / valor2;
    resto = valor1 % valor2;
    printf("Valor da soma de %d + %d = %d\n.", valor1, valor2, soma);
    printf("Valor da subtracao de %d - %d = %d\n.", valor1, valor2, sub);
    printf("Valor da multiplicacao de %d * %d = %d\n.", valor1, valor2, mult);
    printf("Valor da divisao de %d / %d = %d\n.", valor1, valor2, div);
    printf("Valor do resto da divisao de %d // %d = %d\n.", valor1, valor2, resto);


    printf(" Digite um numero inteiro: ");
    scanf("%d", &num);

    resto = num % 2;

    printf("Resto da divisao de %d.\n", resto);

    if (resto == 0) // Não pode ter o ; pq o else não vai funcionar.
    {
        printf("Numero par!\n");
    }
    else 
        {
            printf("Numero impar!\n");
        }
    

    printf("Digite a primeira nota: ");
    scanf("%f", &nota1);
    printf("Digite a segunda nota: ");
    scanf("%f", &nota2);

    media = (nota1 + nota2) / 2;
    printf("Media = %.2f\n",media);

// If anuinhado
if (media >= 6)
{
    printf("Aluno aprovado!\n");
}
else
{
    if (media< 3)
    {
        printf("Aluno Reprovado!\n");
    }
    else
    {
        printf("Aluno em recuperacao!\n");
    }

}
*/

//Comando switch case.

printf("Digite um numero de 1 a 7: ");
scanf("%d", &dia);
switch (dia)
{
case 1 :
    printf("Domingo\n");
break;

case 2 :
    printf("Segunda\n");
break;

case 3 :
    printf("Terca\n");
break;

case 4 :
    printf("Quarta\n");
break;

case 5 :
    printf("Quinta\n");
break;

case 6 :
    printf("Sexta\n");
break;

case 7 :
    printf("Sabado\n");
break;

default:
    printf("Valor invalido!\n");
    break;
}

    //system("pause"); //comando somente para Windows.

    return 0;
}

