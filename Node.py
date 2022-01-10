class Node:
    def __init__(self, order) -> None:
        self.order = order
        self.leaf = False
        self.parent = None
        self.nextKey = None
        self.previousKey = None
        self.keys = []
        self.children = []
    
    def insert_key_leaf(self, key):
        if len(self.keys):
            for i in range(len(self.keys)):
                if (key == self.keys[i]):
                    self.keys = self.keys[:i] + [key] + self.keys[i:]
                    break
                elif (key < self.keys[i]):
                    self.keys = self.keys[:i] + [key] + self.keys[i:]
                    break
                elif (i + 1 == len(self.keys)):
                    self.keys.append(key)
                    break
        else:
            self.keys.append(key)
            
    def split_node(self):
        node = Node(self.order) 
        node.leaf = True
        node.parent = self.parent
        mid = self.order 
        node.keys = self.keys[mid:]
        node.nextKey = self.nextKey
        node.previousKey = self
        self.keys = self.keys[:mid]
        self.nextKey = node
        return node
        
        
        