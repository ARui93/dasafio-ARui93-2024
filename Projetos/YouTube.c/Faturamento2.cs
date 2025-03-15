using System;

class FaturamentoAnual
{
    static void Main(string[] args)
    {
        // Declaração do vetor de faturamento diário
        double[] faturamentoDiario = new double[] { 500, 1000, 850, 300 };

        // Variáveis para armazenar os valores máximo e mínimo
        double menorFaturamento = double.MaxValue;
        double maiorFaturamento = double.MinValue;

        // Variáveis para contagem de dias com faturamento acima da média
        int diasAcimaMedia = 0;

        // Cálculo da média anual, ignorando dias sem faturamento
        double somaFaturamento = 0;
        int diasComFaturamento = 0;
        for (int i = 0; i < faturamentoDiario.Length; i++)
        {
            if (faturamentoDiario[i] > 0)
            {
                somaFaturamento += faturamentoDiario[i];
                diasComFaturamento++;
            }
        }

        double mediaAnual = somaFaturamento / diasComFaturamento;

        // Identificação do menor e maior valor de faturamento
        for (int i = 0; i < faturamentoDiario.Length; i++)
        {
            if (faturamentoDiario[i] > 0)
            {
                menorFaturamento = Math.Min(menorFaturamento, faturamentoDiario[i]);
                maiorFaturamento = Math.Max(maiorFaturamento, faturamentoDiario[i]);

                if (faturamentoDiario[i] > mediaAnual)
                {
                    diasAcimaMedia++;
                }
            }
        }

        // Exibição dos resultados
        Console.WriteLine("Menor faturamento diário: " + menorFaturamento);
        Console.WriteLine("Maior faturamento diário: " + maiorFaturamento);
        Console.WriteLine("Dias com faturamento acima da média: " + diasAcimaMedia);
    }
}
