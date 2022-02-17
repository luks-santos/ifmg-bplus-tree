from BplusTree import BplusTree

lenPag = int(input("Digite o tamanho da página: "))
qtdReg = int(input("Digite a quantidade de campos: "))
arvore = BplusTree(lenPag,qtdReg)

while(True):  #Menu de ações da Arvore B+
  #  print("RAIZ: ", arvore.root.keys)          
    print("\n1 - Inserir valor na Árvore")
    print("2 - Remover valor na Árvore")
    print("3 - Buscar valor na Árvore")
    print("4 - Buscar valor por intervalo na Árvore")
    print("5 - Mostrar B+")
    print("0 - sair")
    n = int(input("Digite uma opção: "))
    if n == 1:
        #key = int(input("Digite o valor para ser inserido: "))
       # key = int(input("informe uma chave: "))
        #vv = [7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 30, 40, 50, 51, 52, 53, 54,20,21,22]
        #vv = [7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        vv = [6, 7, 9, 10, 11, 12, 13, 14, 15, 25, 26, 27, 28, 29, 30, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 70, 71, 72, 73, 74, 75]
       #remove 14
        for i in vv:
            arvore.insert(i, [i, 0])
    elif n == 2:
        numero = int(input("Digite o valor para ser removido: "))
        arvore.delete(numero)
    elif n == 3:
        key = int(input("Digite o valor para ser buscado: "))
        arvore.search_key(key)
        #key = int(input("Digite o valor para ser inserido: "))
        #arvore.insert(key, [key, 0])
    elif  n== 4:
        numero1 = int (input("Digite o primeiro valor para ser buscado: "))
        numero2 = int (input("Digite o segundo valor para ser buscado: "))
    elif  n== 5:
        arvore.print_tree()
    else:
        break

    #removi o 75 e 74
