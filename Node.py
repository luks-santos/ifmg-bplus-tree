from math import ceil


class Node:
    def __init__(self, order) -> None: #Construtor da classe Node, aquela que armazena os registros e indices de páginas não folha
        self.order = order
        self.is_leaf = False
        self.parent = None
        self.next_key = None
        self.previous_key = None
        self.keys = []
        self.children = []

    def get_order(self): #Retorna a ordem do nó, seja nó folha ou não. A ordem do nó não folha pode ser maior que o nó folha
        return self.order

    def insert_key_leaf(self, key, record): #Insere o registro no nó folha.
        if len(self.keys):
            for i in range(len(self.keys)):
                if(key < self.keys[i][0]): #Caso o registro seja menor do que a chave do registro analisado, ele é inserido entre os registros
                    self.keys = self.keys[:i] + [record] + self.keys[i:] #inclusão entre os registros
                    break
                elif(i + 1 == len(self.keys)): #Caso seja a ultima posição do nó e não foi encontrado registro maior ele é inserido no final da folha
                    self.keys.append(record) 
                    break
        else:
            self.keys.append(record) #Caso não haja nenhum registro apenas se insere o primeiro registro ao final do nó. 

    def insert_key(self, key): #Insere a chave em nó não folha. Segue a lógica do anterior
        if len(self.keys):
            for i in range(len(self.keys)):
                if(key < self.keys[i]):
                    self.keys = self.keys[:i] + [key] + self.keys[i:]
                    break
                elif(i + 1 == len(self.keys)):
                    self.keys.append(key)
                    break
        else:
            self.keys.append(key)
            
    def delete_key(self, key): #Apaga o registro com o indice key daquele determinado nó
        if len(self.keys):
            for i, item in enumerate(self.keys): 
                if(item[0] == key): #É verificado se o indice é correspondente ao buscado
                    self.keys.pop(i) #Caso seja é apagado o registro daquela posição do nó. 
                    break
            
    def split_node(self, key, record): #Realiza a divisão de chaves, é chamado quando o nó chega ao limite de sua capacidade
        node_right = Node(self.get_order())  #É criado um nó auxiliar com a ordem do nó a ser dividido
        node_right.is_leaf = True
        mid = ceil((self.order/2)) #É definido um pivô para aquele nó
        
        self.insert_key_leaf(key, record) #O novo valor é inserido no nó folha
        #As chaves são reorganizadas
        node_right.keys = self.keys[mid:] 
        self.keys = self.keys[:mid]

        print('No esquerdo depois do split: ', self.keys)
        print('No direito depois do split: ', node_right.keys)
          
        node_right.parent = self.parent  #É definido como o pai do nó criado o pai do nó no contexto, ou seja aquele que foi dividido
        node_right.next_key = self.next_key #É realizado o reapontamento
        node_right.previous_key = self 
        self.next_key = node_right
        #Caso seja o primeiro nó pode não haver vizinho à esquerda, dessa forma é necessário verificação
        if (node_right.next_key):
            node_right.next_key.previous_key = node_right
        return node_right
    
    def lend(self, node, side): #Responsável por pegar o nó emprestado
        if (side == 0): #Caso seja nessário pegar um nó da esquerda
            record = self.keys[len(self.keys) - 1]
            self.keys.pop() #Removo o registro da ultima posição
            node.insert_key_leaf(record[0], record)  
        elif (side == 1):#Caso seja necessário pegar um nó da direita
            record = self.keys[0]
            self.keys.pop(0)#Removo o registro da primeira posição
            node.insert_key_leaf(record[0], record)  

    def merge(self, node): #Realiza a fusão dos nós
        self.keys += node.keys #O nó que chama a fusão recebe as chaves do outro nó
        node_aux = node.next_key
        self.next_key = node_aux
        if(node_aux): #Caso seja um nó na ultima posição pode não haver nós posteriores
            node_aux.previous_key = self
        del node
        return self
        
    def rotate_keys(self, neighbor_left, neighbor_right, index, side): #Responsável por realizar a rotação de chaves da árvores
        if(side == 0):#Caso seja realizado pela esquerda               #Chamado quando existem muitos níveis e é necessário reorganizar os indices das páginas não folha
            key = self.keys.pop(index) #A chave do nó pai de uma determinada posição é removida
            print("no do contexto self: ", self.keys, " - i - ", index)
            neighbor_right.insert_key(key) #A chave removida é inserida no nó a direita
            key = neighbor_left.keys.pop(-1) # a key recebe a remoção da chave do nó da esquerda
            self.insert_key(key) # A chave removida é inserida no nó pai
            node_ = neighbor_left.children.pop(-1) #Node recebe os filhos do nó removido da esquerda
            print("node_: ", node_.keys)
            node_.parent = neighbor_right 
            
            neighbor_right.children = [node_] + neighbor_right.children #Os filhos do nó da direita são reorganizados e recebe os filhos do nó 
                                                                        # removido 
            print('filhos do nó direito')
            for c in neighbor_right.children: 
                print(c.keys)
                print('------')
                print(c.parent.keys)
            
        elif(side == 1): #Caso seja realizado pela direita a mesma lógica é seguida, a diferença é que são removidas os indices de posições diferentes
            key = self.keys.pop(index-1)
            print("no do contexto self: ", self.keys, " - i - ", index)
            neighbor_left.insert_key(key)
            key = neighbor_right.keys.pop(0)
            self.insert_key(key)
            node_ = neighbor_right.children.pop(0)
            node_.parent = neighbor_left
            neighbor_left.children += [node_]  #Nesse caso basta incluir os filhos do nó removido ao final do nó à esquerda
            
            print('filhos do nó esquerdo')
            for c in neighbor_left.children:
                print(c.keys)
                print('------')
                print(c.parent.keys)
