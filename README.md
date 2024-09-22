# Arvore B+

- Implementação árvore B+ em memória utilizando python, para disciplina de banco de dados II

# Introdução

Para utilização do código implementado há duas possiveis maneiras.

1. [Inserção](#inserção), [deleção](#deleção) e [busca](#busca) manuais.
2. [Caso de testes automatizado](#caso-de-testes-automatizado).

# Como usar

Para realizar ambos casos de testes deve ser execultado o arquivo main.py, seja por linha de comando ou por alguma IDE. Após isso deverá ser informado o tamanho da página e quantidade de campos do registro (recomendado 1024 bytes e 5 campos), em seguida um menu com os possiveis comandos será exibido, para cada opção há instruções de como realizar inserções, deleções e busca por igualde ou intervalo na árvore. 

### Inserção

Para inserir um registro, pressione a opção 1, em seguida realize os seguintes passos:

- Informe o registro com a quantidade de campos passados na inicialização da árvore separados por virgula.
  
        Ex: Uma árvore com registros de 5 campos, digite no input: 78, 96, 4, 56, 8 (Lembre-se o primeiro número será a chave do registro). 

### Deleção 

Para remover um registro, pressione a opção 2, em seguida realize os seguintes passos:

- Informe a key (primeiro número do registro).
       
        Ex: Uma árvore com um registro de 5 campos: [78, 96, 4, 56, 8], digite 78.

### Busca

Possui 4 opções de busca, sendo dividas em 2 categorias:

- 1º Busca por igualdade, pressione a opção 3 e Informe a key (primeiro número do registro).

- 2º Busca por intervalo, pressione opção 4:

        - Para registros maiores que um número, digite A separado por espaço o número (EX: A 35)
        - Para registros menores que um número, digite B separado por espaço o número (EX: B 35)
        - Para registros entre dois números, digite C separado por espaço os dois números (EX: C 35 80)

### Print

Para mostrar a árvore completa, pressione a opção 5.
Os nós folhas são mostrados separados pelo simbolo <-> 
        
### Caso de testes automatizado

Precisa ser usado um arquivo do tipo .csv, o código para ler o arquivo é baseado no csv gerado pela ferramenta [SIOgen](https://ribeiromarcos.github.io/siogen/).

No codigo fonte se necessario mudar o nome do arquivo para outros testes. 

- Basta pressionar a opção 6 e utilizar as opções listadas acima, como inserção, deleção, busca, print.













