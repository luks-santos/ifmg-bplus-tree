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
        for item in node_.keys:
            if item[0] == key:
                return None
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

    def delete(self, key):
        node = self.search(key)

        #Caso 0 - Só tem chaves na raiz, ainda não houve divisão
        if(node == self.root):
            self.delete_key(node, key)
            print("é raiz")
            return
       
        parentNode, index = self.key_is_index(node.parent, key)
        #Caso 1.a - Tem quantidade mínima para remoção e não tem índice acima
        if(not parentNode and len(node.keys) > self.root.order):
            self.delete_key(node, key)

        #Caso 1.b - Não tem quantidade mínima para remoção e não tem índice acima
        elif(not parentNode and len(node.keys) == self.root.order):
            #tratar verificação de pais diferentes
            neighborLeft = node.previousKey
            neighborRight = node.nextKey

            if(neighborLeft and len(neighborLeft.keys) > self.root.order):
                node.insert_key_leaf(neighborLeft.keys.pop())  
                self.delete_key(node, key)
                print("Irmão da esquerda no remove")
                print(neighborLeft.keys)
                print("Irmão da direita no remove")
                print(neighborRight.keys)
                print("Node")
                print(node.keys)

            elif(neighborRight and len(neighborRight.keys > self.root.order)):
                node.insert_key_leaf(neighborRight.keys.pop(0))  
                self.delete_key(node, key)
                print("Irmão da esquerda no remove")
                print(neighborLeft.keys)
                print("Irmão da direita no remove")
                print(neighborRight.keys)
                print("Node")
                print(node.keys)
                print("ok")
                
            """ elif(i == 1):
                rightnode = node.nextKey
                if(len(rightnode.keys) > self.root.order):
                    value_ = rightnode.keys[0]
                    node.keys.append(rightnode.keys[0])
                    self.delete_key(rightnode, rightnode.keys[0])
                    self.delete_key(node, key)
                    x,y = self.key_is_index(node.parent,value_)
                    node.parent.keys[y] = rightnode.keys[0]
                    
                
                    print("começa aq")
                    print(node.keys)
                    print(rightnode.keys)
                    print(node.parent.keys)
                    print("termina aq")
            """
    #teste
    def delete_key(self, node, key):
        if len(node.keys):
            print(node.keys)
            index = node.keys.index(key)
            node.keys.pop(index)
            print(node.keys)

    #deve passar no node o pai imediato
    def key_is_index(self, node, key):
        while(node):
            for i, item in enumerate(node.keys):
                if(item == key):
                    return item, i
            node = node.parent
        return 0, 0

    def print_tree(self):
        if not self.root:
            return None
        
        node = self.root
        while not node.is_leaf:
            node = node.children[0]

        while node:
            print('{}'.format(node.keys), end=' -> ')
            node = node.next_key
