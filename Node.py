class Node:
    def __init__(self, order) -> None:
        self.order = order
        self.is_leaf = False
        self.parent = None
        self.next_key = None
        self.previous_key = None
        self.keys = []
        self.children = []
    
    def insert_key_leaf(self, key):
        if len(self.keys):
            for i in range(len(self.keys)):
                if (key == self.keys[i][0]):
                    self.keys[i].append(key)
                    return -1
                elif (key < self.keys[i][0]):
                    self.keys = self.keys[:i] + [[key]] + self.keys[i:]
                    return 0
                elif (i + 1 == len(self.keys)):
                    self.keys.append([key])
                    return 0
        else:
            self.keys.append([key])
            return 0
            
    def split_node(self, key):
        node_right = Node(self.order) 
        node_right.is_leaf = True
        mid = self.order//2
        node_right.keys = self.keys[(mid):]
        self.keys = self.keys[:mid]
        
        if self.keys[mid - 1][0] < key:
            if node_right.insert_key_leaf(key) == -1:
                self.keys = self.keys[:mid] + node_right.keys[:mid]
                del node_right
                return None
        else:
            if self.insert_key_leaf(key) == -1:
                self.keys = self.keys[:mid] + node_right.keys[:mid]
                del node_right
                return None

        node_right.parent = self.parent
        node_right.next_key = self.next_key
        node_right.previous_key = self
        self.next_key = node_right
        return node_right
        
        