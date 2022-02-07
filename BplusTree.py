from Node import Node
from math import ceil
class BplusTree:
    def __init__(self, order) -> None:
        self.root = Node(order)
        self.root.is_leaf = True
    
    def insert(self, key, record):
        node = self.__search(key)
        if (node):
            if (len(node.keys) == (node.get_order())):
                node_right = node.split_node(key, record)
                if(node_right):
                    self.__insert_parent(node, node_right.keys[0][0], node_right)
            else:
                node.insert_key_leaf(key, record)
            print('Raiz: ', self.root.keys)

    def __search(self, key):
        node_ = self.root
        while(not node_.is_leaf):
            temp = node_.keys
            for i in range(len(temp)):     
                if (key == temp[i]):
                    node_ = node_.children[i + 1]
                    break
                elif (key < temp[i]):
                    node_ = node_.children[i]
                    break
                elif (i + 1 == len(node_.keys)):
                    node_ = node_.children[i + 1]
                    break
        return node_

    def __insert_parent(self, node_left, key, node_right):
        if (self.root == node_left):
            node_root = Node(4)
            node_root.keys = [key]
            node_root.children = [node_left, node_right]
            print('node_root:', node_root.keys)
            print('Filho esquerda raiz:', node_root.children[0].keys)
            print('Filho direita raiz:', node_root.children[1].keys)
            self.root = node_root
            node_left.parent = node_root
            node_right.parent = node_root
        else:
            parent_left = node_left.parent
            temp = parent_left.children
            for i in range(len(temp)):
                if (temp[i] == node_left and len(parent_left.keys) == (self.root.order)):
                    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    parent_right = Node(4)
                    parent_right.parent = parent_left.parent
                    mid = ceil(parent_left.order/2)
                    
                    parent_left.keys = parent_left.keys[:i] + [key] + parent_left.keys[i:]
                    parent_left.children = parent_left.children[:i + 1] + [node_right] + parent_left.children[i + 1:]
                    print('KEYS P ESQUERDA:', parent_left.keys)
                    print('FILHOS ESQUERDA: ')
                    for k in parent_left.children:
                        print(k.keys)

                    value = parent_left.keys[mid]

                    parent_right.keys = parent_left.keys[mid + 1:]
                    parent_right.children = parent_left.children[mid + 1:]
                    print('KEYS P DIREITA:',  parent_right.keys)
                    print('FILHOS DIREITA: ')
                    for k in parent_right.children:
                        print(k.keys)

                    parent_left.keys = parent_left.keys[:mid] 
                    parent_left.children = parent_left.children[:mid + 1]
                    print('KEYS P ESQUERDA:', parent_left.keys)
                    print('FILHOS ESQUERDA: ')
                    for k in parent_left.children:
                        print(k.keys)

                    for j in parent_left.children:
                        print("filho esquerda")
                        print(j.keys)
                        j.parent = parent_left
                    for j in parent_right.children:
                        print("filho direita")
                        print(j.keys)
                        j.parent = parent_right

                    self.__insert_parent(parent_left, value, parent_right)
                    print("++++++++++++++++++++++++++++++++++++++++++++++++")
                    break
                elif (temp[i] == node_left):
                    print('Filhos no esquerda')
                    for k in parent_left.children:
                        print(k.keys)
                    parent_left.keys = parent_left.keys[:i] + [key] + parent_left.keys[i:]
                    parent_left.children = parent_left.children[:i + 1] + [node_right] + parent_left.children[i + 1:]

                    print("Subi uma chave para raiz ficou com", len(parent_left.keys), "chaves")
                    print('Filhos no esquerda')
                    for k in parent_left.children:
                        print(k.keys)
                    break
    
    def lend(self,node_lend,node,side):
        if(side == 0):
            record = node_lend.keys[len(node_lend.keys)-1]
            node_lend.keys.pop()
            node.insert_key_leaf(record[0], record)  
        elif(side == 1):
            record = node_lend.keys[0]
            node_lend.keys.pop(0)
            node.insert_key_leaf(record[0], record)  

    def merge(self, node_merge, node):
        node_merge.keys += node.keys
        node_aux = node.next_key
        node_merge.next_key = node.next_key
        if(node_aux):
            node_aux.previous_key = node_merge
        del node
        


    #Há mudanças nas chaves do pai, páginas não folha, somente quando pego emprestado, ou quando tem fusão 
    def delete(self, key):
        node = self.__search(key)
        print("node: " , node)
        #Caso 0 - Só tem chaves na raiz, ainda não houve divisão
        if(node == self.root):
            print("cheguei aqui?")
            self.delete_key(node, key)
            print("é raiz")
            return
       
        #Caso 1.a - Tem quantidade mínima para remoção e não tem índice acima
        if(len(node.keys) > ceil(node.get_order()/2)):
            self.delete_key(node, key)

        #Caso 1.b - Não tem quantidade mínima para remoção e não tem índice acima
        elif(len(node.keys) == ceil(node.get_order()/2)):
            #tratar verificação de pais diferentes
            neighborLeft = node.previous_key
            neighborRight = node.next_key
            if(neighborLeft and neighborLeft.parent == node.parent and len(neighborLeft.keys) > ceil(node.get_order()/2)):
                self.lend(neighborLeft,node,0)
                self.delete_key(node, key)
                for i in range(len(node.parent.keys)):
                    print( "i: ", node.parent.keys)
                    if(node.keys[0][0] <= node.parent.keys[i]):
                        node.parent.keys[i] = node.keys[0][0]
                        break
                print("mudanças: " , node.parent.keys)
            elif(neighborRight and neighborRight.parent == node.parent and len(neighborRight.keys) > ceil(node.get_order()/2)):
                self.lend(neighborRight,node,1)
                self.delete_key(node,key)
                for i in range(len(node.parent.keys)-1,-1,-1):
                    print( "i: ", node.parent.keys)
                    print( "if: ", node.keys[0][0], " - ", node.parent.keys[i])
                    if(neighborRight.keys[0][0] >= node.parent.keys[i]):
                        node.parent.keys[i] = neighborRight.keys[0][0]
                        break
                print("mudanças: " , node.parent.keys)
            else: 
                if(neighborLeft and neighborLeft.parent == node.parent):
                    print("chegou aqui na esquerda!")
                    self.delete_key(node,key)
                    self.merge( neighborLeft, node)
                elif(neighborRight and neighborRight.parent == node.parent):
                    print("cheguei aqui na direita!")
                    self.delete_key(node,key)
                    self.merge( neighborRight, node)

    #teste
    def delete_key(self, node, key):
        if len(node.keys):
            print(node.keys)
            for i,item in enumerate(node.keys):
                if item[0] == key:
                    node.keys.pop(i)
                    print("indice: ", i)
                    break
            
            print(node.keys)

    def print_tree(self):
        if not self.root:
            return None
        
        node = self.root
        while not node.is_leaf:
            node = node.children[0]

        while node:
            print('{}'.format(node.keys), end=' -> ')
            node = node.next_key
