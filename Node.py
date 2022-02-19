from math import ceil

class Node:
    def __init__(self, order) -> None: #Construtor da classe Node, aquela que armazena os registros e indices de páginas não folha
        self.order = order
        self.is_leaf = False
        self.parent = None
        self.next_record = None
        self.previous_record = None
        self.records = []
        self.children = []

    def get_order(self): #Retorna a ordem do nó, seja nó folha ou não. A ordem do nó não folha pode ser maior que o nó folha
        return self.order

    def insert_key_leaf(self, key, record): #Insere o registro no nó folha.
        if len(self.records):
            for i in range(len(self.records)):
                if(key < self.records[i][0]): #Caso o registro seja menor do que a chave do registro analisado, ele é inserido entre os registros
                    self.records = self.records[:i] + [record] + self.records[i:] #inclusão entre os registros
                    break
                elif(i + 1 == len(self.records)): #Caso seja a ultima posição do nó e não foi encontrado registro maior ele é inserido no final da folha
                    self.records.append(record) 
                    break
        else:
            self.records.append(record) #Caso não haja nenhum registro apenas se insere o primeiro registro ao final do nó. 

    def insert_key(self, key): #Insere a chave em nó não folha. Segue a lógica do anterior
        if len(self.records):
            for i in range(len(self.records)):
                if(key < self.records[i]):
                    self.records = self.records[:i] + [key] + self.records[i:]
                    break
                elif(i + 1 == len(self.records)):
                    self.records.append(key)
                    break
        else:
            self.records.append(key)
            
    def delete_key(self, key): #Apaga o registro com o indice key daquele determinado nó
        if len(self.records):
            for i, item in enumerate(self.records): 
                if(item[0] == key): #É verificado se o indice é correspondente ao buscado
                    self.records.pop(i) #Caso seja é apagado o registro daquela posição do nó. 
                    break
            
    def split_node(self, key, record): #Realiza a divisão de chaves, é chamado quando o nó chega ao limite de sua capacidade
        node_right = Node(self.get_order())  #É criado um nó auxiliar com a ordem do nó a ser dividido
        node_right.is_leaf = True
        mid = ceil((self.order/2)) #É definido um pivô para aquele nó
        
        self.insert_key_leaf(key, record) #O novo valor é inserido no nó folha
        #As chaves são reorganizadas
        node_right.records = self.records[mid:] 
        self.records = self.records[:mid]
  
        node_right.parent = self.parent  #É definido como o pai do nó criado o pai do nó no contexto, ou seja aquele que foi dividido
        node_right.next_record = self.next_record #É realizado o reapontamento
        node_right.previous_record = self 
        self.next_record = node_right
        #Caso seja o primeiro nó pode não haver vizinho à esquerda, dessa forma é necessário verificação
        if (node_right.next_record):
            node_right.next_record.previous_record = node_right
        return node_right
    
    def lend(self, node, side): #Responsável por pegar o nó emprestado
        if (side == 0): #Caso seja nessário pegar um nó da esquerda
            record = self.records[len(self.records) - 1]
            self.records.pop() #Removo o registro da ultima posição
            node.insert_key_leaf(record[0], record)  
        elif (side == 1):#Caso seja necessário pegar um nó da direita
            record = self.records[0]
            self.records.pop(0)#Removo o registro da primeira posição
            node.insert_key_leaf(record[0], record)  

    def merge(self, node): #Realiza a fusão dos nós
        self.records += node.records #O nó que chama a fusão recebe as chaves do outro nó
        node_aux = node.next_record
        self.next_record = node_aux
        if(node_aux): #Caso seja um nó na ultima posição pode não haver nós posteriores
            node_aux.previous_record = self
        del node
        return self
        
    def rotate_keys(self, neighbor_left, neighbor_right, index, side): #Responsável por realizar a rotação de chaves da árvores
        if(side == 0):#Caso seja realizado pela esquerda               #Chamado quando existem muitos níveis e é necessário reorganizar os indices das páginas não folha
            key = self.records.pop(index) #A chave do nó pai de uma determinada posição é removida
            neighbor_right.insert_key(key) #A chave removida é inserida no nó a direita
            key = neighbor_left.records.pop(-1) # a key recebe a remoção da chave do nó da esquerda
            self.insert_key(key) # A chave removida é inserida no nó pai
            node_ = neighbor_left.children.pop(-1) #Node recebe os filhos do nó removido da esquerda
            node_.parent = neighbor_right 
            neighbor_right.children = [node_] + neighbor_right.children #Os filhos do nó da direita são reorganizados e recebe os filhos do nó                                                          # removido 
        elif(side == 1): #Caso seja realizado pela direita a mesma lógica é seguida, a diferença é que são removidas os indices de posições diferentes
            key = self.records.pop(index-1)
            neighbor_left.insert_key(key)
            key = neighbor_right.records.pop(0)
            self.insert_key(key)
            node_ = neighbor_right.children.pop(0)
            node_.parent = neighbor_left
            neighbor_left.children += [node_]  #Nesse caso basta incluir os filhos do nó removido ao final do nó à esquerda