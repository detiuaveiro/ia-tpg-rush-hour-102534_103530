# Arquitetura do projeto

Numa primeira fase do projeto, entendemos que deveríamos dividir o desenvolvimento do agente inteligente em dois módulos lógicos:

- tree_search.py - onde implementámos e testámos os algoritmos de pesquisa em árvore.
- student.py - que transmite ao servidor os movimentos do cursor necessários para resolver o puzzle.

## tree_search.py

### Conjunto de classes de suporte

- Matrix: é um nó da árvore, que guarda um estado do puzzle, sendo 2 dos seus atributos:
  - grid: guarda o estado do puzzle. Representa uma matriz (lista 2D), porém é armazenada eficientemente, na forma de string. Sabendo as coordenadas (x,y) de uma posição da matriz, é possível obter facilmente o seu valor, através do método get(x, y).
  - pieces: dicionário que mapeia cada peça do puzzle para a sua posição atual, na forma (minx, maxx, miny, maxy), que denota as suas fronteiras.
- MatrixForGreedy: é uma subclasse de Matrix, que sobrescreve o método **lt**, de modo a que a comparação de dois nós seja feita apenas com base na heurística.
- MatrixForAStar: é uma subclasse de Matrix, que sobrescreve o método **lt**, de modo a que a comparação de dois nós seja feita com base no custo total (custo acumulado do caminho do cursor + heurística).
- AI: classe não instanciável, que disponibiliza os seguintes métodos estáticos auxiliares:
  - copy: copiar uma string por valor (não por referência).
  - replace_char: substituir uma posição da grid, permitindo a movimentação das peças.
  - cost: calcular o custo de uma ação.
  - heuristic: calcular a heurística de um nó.
  - actions: gerar as ações possíveis a partir de um nó, respeitando as restrições do domínio do problema.
  - result: gerar a grid resultante de uma ação, a partir de um nó, atualizando as fronteiras da peça movimentada.
  - goal_test: verificar se a solução foi encontrada, isto é, se o carro "A" alcançou o limite direito da área de jogo.
- SearchTree: representa a árvore de pesquisa, permitindo a exploração e expansão de nós.
  - Destacam-se os seguintes atributos:
    - open_nodes: lista de nós abertos (gerados), mas não explorados.
    - grids_visited: conjunto (set) com os nós já explorados.
    - total_costs: dicionário que mapeia cada nó gerado para o seu custo total (custo acumulado do caminho do cursor OU profundidade + heurística).
  - Inclui quatro variações do método search:
    - search(): não tem em conta custos ou heurísticas. Explora os nós exaustivamente, até encontrar a solução, excluindo aqueles cujas grids já tenham sido visitadas anteriormente. É utilizada pela pesquisa em profundidade e em largura.
    - search2(): tem em conta a profundidade do nó (custo sem conhecimento da posição do cursor) e a sua heurística. É utilizada pela pesquisa gulosa, que ordena os nós, apenas pela heurística, sem atender ao custo supracitado, cujo intuito é a minimização da profundidade da árvore.
    - search3(): tem em conta apenas o custo acumulado do caminho do cursor. É utilizado pela pesquisa uniforme.
    - search4(): tem em conta o custo acumulado do caminho do cursor e a sua heurística. É utilizado pela pesquisa A.

### Otimizações

- Quando um nó é criado, herda alguns dados do nó pai. Aplicando o padrão de software Flyweight, é possível reduzir, não só a memória utilizada, como o tempo de execução, uma vez que se promove a reutilização de objetos, em detrimento da criação de cópias. Por exemplo, os atributos horizontal_pieces e vertical_pieces são constantes, pelo que podem ser copiados por referência. O pieces, por outro lado, é manipulado em cada nó, pelo que é necessário copiá-lo por valor.
- Numa primeira versão do search, a estrutura grid_visited era uma lista. Após discutirmos estratégias de otimização, com o grupo "102536_102778", concluímos que seria mais eficiente utilizar um conjunto (set), uma vez que a operação de verificação de pertença (lookup) apresenta uma complexidade O(1), enquanto que, nas listas, é O(n). Em versões posteriores, mantivemos esta estrutura. Contudo, há que salientar que a complexidade do lookup com chave, nos dicionários, é também O(1).
- Tendo por base conhecimentos prévios de Algoritmos e Estruturas de Dados, ponderámos a utilização de uma min-heap, como estrutura para guardar os nós por explorar. Para esse efeito, aproveitámos o módulo heapq, nativo do Python. Os resultados foram bastante positivos, dado que cada inserção garante a ordenação da heap, não sendo necessária qualquer operação ulterior, com vista a obter o valor mínimo. O critério de ordenação é definido pelo método **lt** da classe de objetos que compõem a heap, neste caso, a Matrix ou a MatrixForGreedy.
- HEURÍSTICA: número de peças a bloquear o caminho da peça 'A' até à saída.

### Agente
Como estudado nesta unidade curricular, um agente é "uma entidade com capacidade de obter
informação sobre o seu ambiente (através de 'sensores') e de executar ações em função dessa informação.
Em cada iteração do seu ciclo principal, o agente capta o estado do puzzle, através dos seus sensores:
- código de deteção de alteração da grid;
- detectCrazy - deteta a ocorrência de um crazy car;
- detectStuck - deteta a ocorrência de uma anomalia que não foi identificada como crazy car, mas impediu a realização com sucesso do comando enviado para o jogo.

De seguida, o agente escolhe a estratégia de resolução do problema, consoante o tamanho da grid:
- pesquisa gulosa, quando a grid tem dimensão superior a 6x6;
- pesquisa uniforme, quando a grid tem dimensão igual ou inferior a 6x6;

A solução do tree_search é convertida em movimentos do cursor, por intermédio da função moveCursor. Esta simula o comportamento do cursor, ao selecionar uma peça a partir da sua fronteira mais próxima (está otimizada, nesse sentido).

O tempo que demora a encontrar a solução e a convertê-la é cronometrado, para assegurar a sincronização com o servidor. Quando esse tempo total é maior do que a taxa de aceitação de comandos por parte do servidor, são enviados comandos vazios.
