from Node import Node
from math import floor, ceil
import sys

class BplusTree:
    def __init__(self, len_page, qty_fields ) -> None: #Construtor da arvore B+
        self.order, self.order_parent  = self.calc_order(len_page, qty_fields) #Recebem os valores da ordem
        self.root = Node(self.order)
        self.root.is_leaf = True
    
    def calc_order(self, len_page, qty_fields): #Calcula a ordem baseada no tamanho da página e quantidade de campos
        vet_ = [1] * qty_fields #Crio um vetor de inteiros auxiliar com a quantidade de campos informados
        order_leaf = len_page//sys.getsizeof(vet_) #tamanho da página em bytes pelo tamanho do registro em bytes
        order_nleaf = len_page//sys.getsizeof(1)
        print("order_folha: ", order_leaf)
        print("order_not_folha: ", order_nleaf)
        return (order_leaf, order_nleaf)

    def insert(self, key, record): #Método para inserção dos registros
        node = self.search(key) #Busco o nó o qual o registro será inserido
        if self.search_key(node, key):
            if len(node.records) == node.get_order(): #Caso o nó esteja cheio 
                node_right = node.split_node(key, record) #Será realizado a divisão 
                if node_right:
                    self.__insert_parent(node, node_right.records[0][0], node_right) #Após isso será inserido a chave no nó pai e realizado os apontamentos
            else:
                node.insert_key_leaf(key, record) #Insere o registro na folha
        else:
            print('Chave já inserida.')

    def search(self, key): #Pesquisa em qual nó será inserido o registro 
        node_ = self.root #Inicia a busca pela raiz
        while not node_.is_leaf: #Enquanto não encontrar um nó folha o laço permanece
            temp = node_.records
            for i in range(len(temp)):     
                if key == temp[i]: #Caso o indice de chave exista retorna o nó da posição i+1
                    node_ = node_.children[i + 1]
                    break
                elif key < temp[i]: #Caso o indice de chave seja menor do que a existente retorna o nó da posição i
                    node_ = node_.children[i]
                    break
                elif i + 1 == len(node_.records): #Caso chegue ao final é retornado o nó da posição i+1
                    node_ = node_.children[i + 1]
                    break
        return node_

    def search_key(self, node_, key): #Pesquisa por igualdade
        for k in node_.records:     #Percorro e verifico se o registro está presente no nó
            if key == k[0]:
                return False
        return True
    
    def interval_search(self, node, key, key2, op): #Função utilizada para busca de intervalos
        if op == '>':
            while node:
                for i in range(len(node.records)): #Busca por valores maiores que um dado índice
                    if node.records[i][0]>key:
                        print(node.records[i:], end="<->")
                        break
                node = node.next_record
        elif op == '<':
            while node:
                for i in range(len(node.records)-1, -1,-1): #Busca por valores menores que um dado índice
                    if(node.records[i][0]<key):
                        print(node.records[:i+1], end="<->")
                        break
                node = node.previous_record
        elif op == '|':
            while node:
                for i in range(len(node.records)): #É realizado um comparativo entre os extremos do intervalo
                                                    # o indice de cada registro é comparado com cada um deles. 
                    if node.records[i][0]>key and node.records[i][0] < key2:
                        print(node.records[i], end="<->")
                    else:
                        return
                node = node.next_record
            
    def __insert_parent(self, node_left, key, node_right): #Utilizada na divisão ao inserir 
        if self.root == node_left: #Caso seja realizada a divisão no no raiz
            node_root = Node(self.order_parent) # Como a raiz não será folha recebe ordem de no não folha
            node_root.records = [key]
            node_root.children = [node_left, node_right]
            self.root = node_root # Atualiza nova raiz
            node_left.parent = node_root # Atualiza os filhos
            node_right.parent = node_root
        else:
            parent_left = node_left.parent #Recebe o pai do nó da esquerda
            temp = parent_left.children #Recebe os filhos do nó da esquerda
            for i in range(len(temp)):
                #Caso o filho do nó analisado seja igual ao node dividido e a quantidade de chaves do pai é igual à ordem daquele nó faz a divisão do pai
                if temp[i] == node_left and len(parent_left.records) == parent_left.get_order():  
                    parent_right = Node(self.order_parent) #Crio um nó auxiliar
                    parent_right.parent = parent_left.parent
                    
                    #Insiro a key entre as records que estão no nó pai
                    parent_left.records = parent_left.records[:i] + [key] + parent_left.records[i:]
                    parent_left.children = parent_left.children[:i + 1] + [node_right] + parent_left.children[i + 1:] #Reorganizo os filhos
                    
                    mid = ceil(parent_left.get_order()/2) #Defino um pivo
                    value = parent_left.records[mid] #Value receberá o valor da chave que se encontra na posição do pivo

                    parent_right.records = parent_left.records[mid + 1:] #O pivo será utilizado para reorganizar as chaves do nó da direita
                    parent_right.children = parent_left.children[mid + 1:] #Bem como seus filhos
                    
                    parent_left.records = parent_left.records[:mid]  #O pivo também será utilizado para reorganizar as chaves do nó da esquerda
                    parent_left.children = parent_left.children[:mid + 1] #Bem como seus filhos

                    #Reorganiza os apontaodres dos filhos para os pais
                    for j in parent_left.children:
                        j.parent = parent_left
                    for j in parent_right.children:
                        j.parent = parent_right

                    self.__insert_parent(parent_left, value, parent_right) # O valor de value será subido na divisão de páginas 
                    break

                elif temp[i] == node_left: #Se a raiz não estiver cheia apenas subo uma chave para ela.
                    parent_left.records = parent_left.records[:i] + [key] + parent_left.records[i:]
                    parent_left.children = parent_left.children[:i + 1] + [node_right] + parent_left.children[i + 1:]
                    break
    
    #Há mudanças nas chaves do pai, páginas não folha, somente quando pego emprestado, ou quando tem fusão 
    def delete(self, key):
        node = self.search(key)
        #caso 0 - Só tem chaves na raiz, ainda não houve divisão
        if node == self.root:
            node.delete_key(key)

        #caso 1 - node é folha e tem quantidade mínima para remoção 
        elif len(node.records) > floor(node.get_order()/2):
            node.delete_key(key)
        else:
            self.delete_aux(node, key)

    def delete_aux(self, node, key):
        #caso 2 - Não tem quantidade mínima para remoção
        if len(node.records) == floor(node.get_order()/2):
            #caso 2.a Irmão imediato esquerda pode emprestar um registro
            neighbor_left = node.previous_record
            if neighbor_left and neighbor_left.parent == node.parent and len(neighbor_left.records) > floor(node.get_order()/2):
                neighbor_left.lend(node, 0) 
                node.delete_key(key)
                for i in range(len(node.parent.records)): #atualizo a chave no pai 
                    if node.records[0][0] <= node.parent.records[i]:
                        node.parent.records[i] = node.records[0][0]
                        break
            else:
                #caso 2.b Irmão imediato direita pode emprestar um registro
                neighbor_right = node.next_record
                if neighbor_right and neighbor_right.parent == node.parent and len(neighbor_right.records) > floor(node.get_order()/2):
                    neighbor_right.lend(node, 1)
                    node.delete_key(key)
                    for i in range(len(node.parent.records)-1, -1, -1): #pecorro as chave do pai ao contrario para atualizar a chave
                        if neighbor_right.records[0][0] >= node.parent.records[i]:
                            node.parent.records[i] = neighbor_right.records[0][0]
                            break
                else: 
                    #caso 3 Faço fusão com irmão esquerdo ou direito
                    node_merge = None
                    index = -1
                    #verifica se possui irmão esquerdo e possui mesmo pai
                    if neighbor_left and neighbor_left.parent == node.parent: 
                        node.delete_key(key)
                        index = node.parent.children.index(node)
                        node_merge = neighbor_left.merge(node)
                    #verifica se possui irmão direito e possui mesmo pai
                    elif neighbor_right and neighbor_right.parent == node.parent: 
                        node.delete_key(key)
                        index = node.parent.children.index(node)
                        node_merge = node.merge(neighbor_right)
                    
                    del node 
                    parent_node = node_merge.parent

                    if parent_node == self.root and len(self.root.records) == 1: #caso a raiz dique vazia
                        parent_node = None
                        self.root = node_merge #atualiza  a raiz pelo novo no que sofreu fusão
                        del node_merge
                        return
                    #remove o apontador para filho e a chave que sofreu fusão
                    if index > 0 and index < len(parent_node.records): 
                        parent_node.children.pop(index)
                        parent_node.records.pop(index - 1)

                    elif index == 0:
                        parent_node.children.pop(index + 1)
                        parent_node.records.pop(index)
                    
                    else:
                        parent_node.children.pop(-1)
                        parent_node.records.pop(-1)
                    #verifica se nó é diferente da raiz e se o numero de chaves for menor que a ordem 
                    # chama função para modifcar nó não folha
                    if parent_node != self.root and len(parent_node.records) < int(floor(parent_node.get_order()/2)):
                        self.modify_parent(parent_node)
    
    def modify_parent(self, node): #Vai ser usado quando precisar reorganizar os pais do nó quando ficar abaixo da ordem mínima
        parent_node = node.parent
        neighbor_left = neighbor_right = None    
        index = parent_node.children.index(node) #Procura pelo nó passado por referencia no pai do nó, ou seja busca a posição daquele nó

        if index != 0 or len(node.parent.records) == index: #Se o índice for diferente de zero ou esse índice é o ultimo 
            neighbor_left = node.parent.children[index - 1]  #O vizinho da esquerda recebe o nó da esquerda do nó passado por referência
            if len(neighbor_left.records) > floor(neighbor_left.get_order()/2): #Se o irmão da esquerda puder emprestar 
                node.parent.rotate_keys(neighbor_left, node, index - 1, 0) #É realizada uma rotação de chaves 
                return
                
        elif index == 0 or index < len(node.parent.records): #Se o índice for igual a zero e ele for menor que o último 
            neighbor_right = node.parent.children[index + 1] #o irmão da direita recebe o nó da direita do nó passado por referência
            if len(neighbor_right.records) > floor(neighbor_right.get_order()/2): #Se o irmão da direita puder emprestar 
                node.parent.rotate_keys(node, neighbor_right, index + 1, 1) #É realizada uma rotação de chaves
                return
        
        if neighbor_left: #Se eu tenho um irmão da esquerda 
            key = parent_node.records.pop(index - 1) #Removo o irmão a esquerda do índice
            neighbor_left.insert_key(key) #Insiro na esquerda esse irmão 
            neighbor_left.records += node.records #Reorganizo os registros
            neighbor_left.children += node.children #Reorganizo os filhos 
            
            for c in node.children: # Para cada filho os pais são atualizados
                c.parent = neighbor_left
            
            parent_node.children.pop(index) #O filho do pai do nó é removido 
            node = neighbor_left #O nó recebe o vizinho da esquerda
        
        elif neighbor_right: #Se eu tenho um vizinho da direita 
            key = parent_node.records.pop(index) #Removo o irmão da direita do índice
            node.insert_key(key) #Insiro na esquerda esse irmão 
            node.records += neighbor_right.records #Reorganizo os registros
            node.children += neighbor_right.children #Reorganizo os filhos
             
            for c in neighbor_right.children: # Para cada filho os pais são atualizados
                c.parent = node
        
            parent_node.children.pop(index + 1)  #O filho do pai do nó é removido 

        if len(parent_node.records) == 0 and parent_node == self.root: #Se o pai do nó ficou sem chaves, seto o nó como raiz
            self.root = node
        
        elif len(parent_node.records) < floor(parent_node.get_order()/2) and parent_node != self.root: #Se o pai do nó ficou abaixo do mínimo e não é raiz
            self.modify_parent(parent_node) #Modifico o pai do nó
    
    
    def print_tree(self): #Print por nível da árvore
        if not len(self.root.records): 
            return

        delimiter = None
        queue = []

        queue.append(self.root)
        queue.append(delimiter)
        while True: 
            curr = queue.pop(0)
            if curr != delimiter: #É utilizado um delimitador para cada nível da árvore
                if curr.is_leaf:
                    print(curr.records, end=' <-> ') 
                else:
                    print(curr.records, end='    ')
                if len(curr.children): #Se ainda estiver no nível adiciono as chaves à fila
                    for n in curr.children:
                        queue.append(n)
            else:
                print()
                if not len(queue):
                    break
                queue.append(delimiter) 