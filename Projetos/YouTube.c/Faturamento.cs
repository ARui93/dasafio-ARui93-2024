using System;
using System.Linq;

class Program
{
    static void Main()
    {
        // Supondo que 'faturamentos' é o vetor já carregado com os valores de faturamento diário
        double[] faturamentos = new double[365]; // Exemplo: preencha com os valores reais

        // Preencher o vetor com valores de exemplo (incluindo zeros para dias sem faturamento)
        Random rand = new Random();
        for (int i = 0; i < 365; i++)
        {
            faturamentos[i] = rand.Next(0, 1000); // Use valores reais em um cenário real
        }

        // Filtrar os dias com faturamento maior que zero
        var faturamentosValidos = faturamentos.Where(f => f > 0).ToArray();

        if (faturamentosValidos.Length == 0)
        {
            Console.WriteLine("Não há faturamento válido para calcular.");
            return;
        }

        // Calcular o menor e o maior valor de faturamento
        double menorFaturamento = faturamentosValidos.Min();
        double maiorFaturamento = faturamentosValidos.Max();

        // Calcular a média anual de faturamento
        double mediaAnual = faturamentosValidos.Average();

        // Contar o número de dias com faturamento superior à média anual
        int diasAcimaDaMedia = faturamentosValidos.Count(f => f > mediaAnual);

        // Exibir os resultados
        Console.WriteLine("Menor valor de faturamento ocorrido em um dia do ano: " + menorFaturamento);
        Console.WriteLine("Maior valor de faturamento ocorrido em um dia do ano: " + maiorFaturamento);
        Console.WriteLine("Número de dias com faturamento superior à média anual: " + diasAcimaDaMedia);
    }
}
