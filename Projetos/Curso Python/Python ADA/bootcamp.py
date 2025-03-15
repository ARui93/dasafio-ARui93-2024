# Definir uma função recursiva para calcular o n-ésimo número triangular
def triangular(n):
  # Caso base: se n é 1, retornar 1
  if n == 1:
    return 1
  # Caso recursivo: se n é maior que 1, retornar n + triangular(n-1)
  else:
    return n + triangular(n-1)

# Definir uma função recursiva para imprimir o triângulo correspondente ao n-ésimo número triangular
def imprimir_triangulo(n, i=1):
  # Caso base: se i é igual a n, imprimir i asteriscos e terminar a função
  if i == n:
    print("*" * i)
    return
  # Caso recursivo: se i é menor que n, imprimir i asteriscos e chamar a função novamente com i+1
  else:
    print("*" * i)
    imprimir_triangulo(n, i+1)

# Receber um número natural N do usuário
N = int(input("Digite um número natural N: "))

# Calcular e mostrar o N-ésimo número triangular usando a função triangular
T = triangular(N)
print(f"O {N}-ésimo número triangular é {T}")

# Imprimir o triângulo correspondente usando a função imprimir_triangulo
print(f"O triângulo correspondente é:")
imprimir_triangulo(N)
