from Node import Node

class BplusTree:
    def __init__(self, order) -> None:
        self.root = Node(order)
        self.root.is_leaf = True
    
    def insert(self, key):
        node = self.__search(key)
        if (len(node.keys) == (2*self.root.order)):
            node_right = node.split_node(key)
            if(node_right):
                self.__insert_parent(node, node_right.keys[0], node_right)
        else:
            node.insert_key_leaf(key)
        print(self.root.keys)

    def __search(self, key):
        node_ = self.root
        while(not node_.is_leaf):
            temp = node_.keys
            print(temp[0])
            for i in range(len(temp)):     
                if (key == temp[i][0]):
                    node_ = node_.children[i + 1]
                    break
                elif (key < temp[i][0]):
                    node_ = node_.children[i]
                    break
                elif (i + 1 == len(node_.keys)):
                    node_ = node_.children[i + 1]
                    break
            
        return node_

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
    
    def __insert_parent(self, node_left, key, node_right):
        if (self.root == node_left):
            node_root = Node(self.root.order)
            node_root.keys = [key]
            node_root.children = [node_left, node_right]
            print('node_root:', node_root.keys)
            print(node_root.children[0].keys)
            print(node_root.children[1].keys)
            self.root = node_root
            node_left.parent = node_root
            node_right.parent = node_root
        else:
            parent_left = node_left.parent
            temp = parent_left.children
            for i in range(len(temp)):
                if (temp[i] == node_left and len(parent_left.keys) == (2*self.root.order)):
                    parent_right = Node(self.root.order)
                    parent_right.parent = parent_left.parent
                    mid = parent_left.order
                    parent_right.keys = parent_left.keys[mid:]
                    parent_right.children = parent_left.children[mid:]
                    value = parent_left.keys[mid - 1]
                    
                    parent_left.keys = parent_left.keys[:i] + [key] + parent_left.keys[i:mid - 1]
                    parent_left.children = parent_left.children[:i + 1] + [node_right] + parent_left.children[i + 1:mid]
    
                    print("direita:")
                    print(parent_right.keys)
                    print("esquerda:")
                    print(parent_left.keys)

                    for j in parent_left.children:
                        print("filho esquerda")
                        print(j.keys)
                        j.parent = parent_left
                    for j in parent_right.children:
                        print("filho direita")
                        print(j.keys)
                        j.parent = parent_right
                    self.__insert_parent(parent_left, value, parent_right)
                elif (temp[i] == node_left):
                    parent_left.keys = parent_left.keys[:i] + [key] + parent_left.keys[i:]
                    parent_left.children = parent_left.children[:i + 1] + [node_right] + parent_left.children[i + 1:]
                    print("Subi uma chave para raiz ficou com", len(parent_left.keys), "chaves")
                    break


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
