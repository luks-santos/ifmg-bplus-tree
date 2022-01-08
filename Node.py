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
            temp1 = self.keys
            for i in range(len(self.keys)):
                if key == temp1[i]:
                    self.keys = self.keys[:i] + [key] + self.keys[i:]
                    break
                elif key < temp1[i]:
                    self.keys = self.keys[:i] + [key] + self.keys[i:]
                    break
                elif i + 1 == len(temp1):
                    self.keys.append(key)
                    break
        else:
            self.keys.append(key)