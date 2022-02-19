from BplusTree import BplusTree
import time

def main():
    len_page = int(input('Digite o tamanho da página em bytes: '))
    qty_fields = int(input('Digite a quantidade de campos do registro: '))
    tree = BplusTree(len_page, qty_fields)

    while(True):  #Menu de ações da Arvore B+         
        print('\n1. Inserir registro na Árvore')
        print('2. Remover registro da Árvore')
        print('3. Buscar registro na Árvore')
        print('4. Buscar registros por intervalo na Árvore')
        print('5. Mostrar B+')
        print('6. Executar casos de teste')
        print('0. Sair')
        #try:
        n = int(input('Digite uma opção: '))
        if n == 1:
            #Informe os campos separados por virgula
            record = [int(x) for x in input('Informe o registro completo com todos os campos:').split(',')]
            if len(record) == qty_fields:
                tree.insert(record[0], record)
            else:
                print('Tamanho de campos no registro não corresponde com o informado.')
        elif n == 2:
            key = int(input('Digite a chave do registro para ser removido: '))
            tree.delete(key)
        elif n == 3:
            key = int(input('Digite a chave para ser buscado o registro: '))
            tree.search_key(tree.search(key), key)
        elif n == 4:
            print('A - Maior que um número ( > x)')
            print('B - Menor que um número ( < x)')
            print('C - Menor ou igual que um número ( <= x)')
            print('D - Maior ou igual que um número ( >= x)')
            print('E - Diferente que um número ( <> x)')
            print('F - Entre dois números (x a y)')
            op = input('Digite a opção e o número com espaços: ').split()
            if op[0] == 'A':
                print('entrei aq')
                tree.interval_search(tree.search(int(op[1])),int(op[1]), 0, '>')
            if op[0] == 'B':
                print('entrei aq no B')
                tree.interval_search(tree.search(int(op[1])),int(op[1]), 0, '<')
        elif n == 5:
            tree.print_tree()

        elif n == 6:
            file = open('output.csv', 'r')
            start = time.time()
            for row in file:
                record = row.split(',')
                if(record[0] == '+'):
                    record = [int(x) for x in record[1:]]
                    tree.insert(record[0], record)
                elif(record[0] == '-'):
                    record = [int(x) for x in record[1:]]
                    tree.delete(record[0])
                end = time.time()
                print(end - start)
            
            
        else:
            break
        #except:
         #   print('Algo deu errado!')

if __name__ == '__main__':
    main()
