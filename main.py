from BplusTree import BplusTree
import sys
registro = sys.getsizeof([1,2,3,4,5]) # Para um registro de 5 campos cada um terá 120 bytes
ordem = (500//registro)

arvore = BplusTree(ordem)
while(True):
    #caso queira mostrar os valores da arvore
    #bMais.mostrarBmais()
    print("\n1 - Inserir valor na Árvore")
    print("2 - Remover valor na Árvore")
    print("3 - Buscar valor na Árvore")
    print("4 - Buscar valor por intervalo na Árvore")
    print("5 - Mostrar B+")
    print("0 - sair")
    n = int(input("Digite uma opção: "))
    if n == 1:
        numero = int(input("Digite o valor para ser inserido: "))
        arvore.insert(numero)
    elif n == 2:
        numero = int(input("Digite o valor para ser removido: "))
        arvore.delete(numero)
    elif n == 3:
        numero = int(input("Digite o valor para ser buscado: "))
        
    elif  n== 4:
        numero1 = int (input("Digite o primeiro valor para ser buscado: "))
        numero2 = int (input("Digite o segundo valor para ser buscado: "))
    elif  n== 5:
        arvore.print_tree()
    else:
        break
