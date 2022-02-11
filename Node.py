from math import ceil

class Node:
    def __init__(self, order) -> None:
        self.order = order
        self.is_leaf = False
        self.parent = None
        self.next_key = None
        self.previous_key = None
        self.keys = []
        self.children = []

    def get_order(self):
        return self.order

    def insert_key_leaf(self, key, record):
        if len(self.keys):
            for i in range(len(self.keys)):
                if(key < self.keys[i][0]):
                    self.keys = self.keys[:i] + [record] + self.keys[i:]
                    break
                elif(i + 1 == len(self.keys)):
                    self.keys.append(record)
                    break
        else:
            self.keys.append(record)
            
    def delete_key(self, key):
        if len(self.keys):
            for i, item in enumerate(self.keys):
                if(item[0] == key):
                    self.keys.pop(i)
                    break
            
    def split_node(self, key, record):
        node_right = Node(self.get_order()) 
        node_right.is_leaf = True
        mid = int(ceil(self.order/2))
        
        self.insert_key_leaf(key, record)
        node_right.keys = self.keys[mid:]
        self.keys = self.keys[:mid]

        print('No esquerdo depois do split: ', self.keys)
        print('No direito depois do split: ', node_right.keys)
          
        node_right.parent = self.parent
        node_right.next_key = self.next_key
        node_right.previous_key = self
        self.next_key = node_right
        if(node_right.next_key):
            node_right.next_key.previous_key = node_right
        return node_right
    
    def lend(self, node, side):
        if(side == 0):
            record = self.keys[len(self.keys) - 1]
            self.keys.pop()
            node.insert_key_leaf(record[0], record)  
        elif(side == 1):
            record = self.keys[0]
            self.keys.pop(0)
            node.insert_key_leaf(record[0], record)  

    def merge(self, node):
        self.keys += node.keys
        node_aux = node.next_key
        self.next_key = node_aux
        if(node_aux):
            node_aux.previous_key = self
        del node
        return self
        