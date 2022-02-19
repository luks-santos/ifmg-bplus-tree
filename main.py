from BplusTree import BplusTree

def main():
    len_page = int(input('Digite o tamanho da página em bytes: '))
    qty_fields = int(input('Digite a quantidade de campos do registro: '))
    tree = BplusTree(len_page, qty_fields)

    while(True):  #Menu de ações da Arvore B+         
        print('\n1 - Inserir registro na Árvore')
        print('2 - Remover registro da Árvore')
        print('3 - Buscar registro na Árvore')
        print('4 - Buscar registros por intervalo na Árvore')
        print('5 - Mostrar B+')
        print('0 - sair')
        try:
            n = int(input('Digite uma opção: '))
            if n == 1:
                record = [int(x) for x in input('Informe o registro completo com todos os campos:').split()]
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
            elif  n == 4:
                numero1 = int (input('Digite o primeiro valor para ser buscado: '))
                numero2 = int (input('Digite o segundo valor para ser buscado: '))
            elif  n == 5:
                tree.print_tree()
            else:
                break
        except:
            print('Informe um número de 0 a 5.')

if __name__ == '__main__':
    main()
