using System;

class Programa
{
    static void Main()
    {
        int numero1 = 10;
        int numero2 = 2;

        ResultadoOperacoes resultado = CalcularSomaEMultiplicacao(numero1, numero2);

        Console.WriteLine($"Soma: {resultado.Soma}");
        Console.WriteLine($"Multiplicação: {resultado.Multiplicacao}");
    }

    static ResultadoOperacoes CalcularSomaEMultiplicacao(int a, int b)
    {
        int soma = a + b;
        int multiplicacao = a * b;
        
        return new ResultadoOperacoes(soma, multiplicacao);
    }
}

class ResultadoOperacoes
{
    public int Soma { get; private set; }
    public int Multiplicacao { get; private set; }

    public ResultadoOperacoes(int soma, int multiplicacao)
    {
        Soma = soma;
        Multiplicacao = multiplicacao;
    }
}
