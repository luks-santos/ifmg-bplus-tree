from Node import Node

class BplusTree:
    def __init__(self, order) -> None:
        self.root = Node(order)
        self.root.leaf = True
    
    def insert(self, key):
        node = self.search(key)
        node.insert_key_leaf(key)
        print(node.keys)


    def search(self, key):
        node1 = self.root

        return node1