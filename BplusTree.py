from Node import Node

class BplusTree:
    def __init__(self, order) -> None:
        self.root = Node(order)
        self.root.leaf = True
    
    def insert(self, key):
        node = self.search(key)
        node.insert_key_leaf(key)
        print(node.keys)
        
        if(len(node.keys) == (node.order*2)):
            node1 = node.split_node()
            self.insert_parent(node, node1.keys[0], node1)

        print(self.root.keys)

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
            i = node.parent.children.index(node)
            
            if(i == 0):
                #pedir o irmão da direita 
                print("ok")
            elif(i == len(node.children)):
                #pedir o irmão da direita
                print("ok")
            elif(i == 1):
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


    def search(self, key):
        node1 = self.root
        while(not node1.leaf):
            temp = node1.keys
            for i in range(len(temp)):     
                if (key == temp[i]):
                    node1 = node1.children[i + 1]
                    break
                elif (key < temp[i]):
                    node1 = node1.children[i]
                    break
                elif (i + 1 == len(node1.keys)):
                    node1 = node1.children[i + 1]
                    break
        return node1
    
    def insert_parent(self, leftnode, key, rightnode):
        if(self.root == leftnode):
            rootNode = Node(leftnode.order)
            rootNode.keys = [key]
            rootNode.children = [leftnode, rightnode]
            print('rootNode:', rootNode.keys)
            print(rootNode.children[0].keys)
            print(rootNode.children[1].keys)
            self.root = rootNode
            leftnode.parent = rootNode
            rightnode.parent = rootNode
            return
    
        parentLeft = leftnode.parent
        temp = parentLeft.children
        for i in range(len(temp)):
            if (temp[i] == leftnode):
                parentLeft.keys = parentLeft.keys[:i] + [key] + parentLeft.keys[i:]
                parentLeft.children = parentLeft.children[:i + 1] + [rightnode] + parentLeft.children[i + 1:]
            if (len(parentLeft.keys) == parentLeft.order * 2):
                parentRight = Node(parentLeft.order)
                parentRight.parent = parentLeft.parent
                mid = parentLeft.order
                parentRight.keys = parentLeft.keys[mid + 1:]
                parentRight.children = parentLeft.children[mid + 1:]
                value = parentLeft.keys[mid]
                
                parentLeft.keys = parentLeft.keys[:mid]
                parentLeft.children = parentLeft.children[:mid + 1]
                print("direita:")
                print(parentRight.keys)
                print("esquerda:")
                print(parentLeft.keys)

                for j in parentLeft.children:
                    print("filho esquerda")
                    print(j.keys)
                    j.parent = parentLeft
                for j in parentRight.children:
                    print("filho direita")
                    print(j.keys)
                    j.parent = parentRight
                self.insert_parent(parentLeft, value, parentRight)

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
        while not node.leaf:
            node = node.children[0]

        while node:
            print('{}'.format(node.keys), end=' -> ')
            node = node.nextKey
