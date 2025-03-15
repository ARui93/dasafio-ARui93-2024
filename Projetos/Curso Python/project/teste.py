def main():
    # Preços para cada tipo de produto na composição Fina
    precos = {
        'Areia': 34.00,   # Areia
        'Pedrita': 42.50,   # Pedrita
        'Brita': 28.00,   # Brita
        'Saibro': 27.00    # Saibro
    }
    
    produto = input("Digite o tipo do produto (Areia, Pedrita, Brita,Saibro): ")
    composicao = input("Digite o tipo de composição (Fina, Média, Grossa): ")
    quantidade = float(input("Digite a quantidade vendida (em metros cúbicos): "))

    if produto not in precos:
        print("Tipo de produto inválido.")
        return

    preco_fina = precos[produto]
    
    # Determina o preço final com base na composição
    if composicao == 'Fina':
        preco_final = preco_fina
    elif composicao == 'Média':
        preco_final = preco_fina * 1.15  # 15% a mais
    elif composicao == 'Grossa':
        preco_final = preco_fina * 1.25  # 25% a mais
    else:
        print("Tipo de composição inválido.")
        return

    # Calcula o valor da venda
    valor_venda = preco_final * quantidade
    if valor_venda < 750:
        valor_venda += 45  # Adiciona taxa de frete

    print(f"Preço Final do Produto: R$ {preco_final:.2f}")
    print(f"Valor da Venda: R$ {valor_venda:.2f}")

if __name__ == "__main__":
    main()
