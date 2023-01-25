# "Rush Hour" - Agente Inteligente

No projeto prático de Inteligência Artificial, os alunos foram desafiados a implementar um agente inteligente, capaz de resolver autonomamente os níveis do jogo Rush Hour, cujo código fonte foi disponibilizado pelo Prof. Diogo Gomes.

Este jogo 2D consiste num quebra-cabeças de blocos deslizantes, em que o objetivo é mover o "carro" vermelho para "fora da garagem", isto é, mover o bloco para o limite direito da área de jogo (de dimensão variável). Para esse efeito, é necessário desimpedir o caminho, alterando a posição dos outros carros.

<div style="text-align:center">
<img src="https://www.michaelfogleman.com/static/rush/top15.png?bust=1531758494" width="300">
</div>

**Fonte**: [https://www.michaelfogleman.com/static/rush/](https://www.michaelfogleman.com/static/rush/)


## Explicação dos algoritmos implementados
Encontra-se no ficheiro [presentation.pdf](presentation.pdf)

## Instalação de dependências

`$ pip install -r requirements.txt`

_Recomenda-se a criação de um ambiente virtual (virtualenv)._

## Execução do projeto
Servidor:
`$ python3 game/server.py`

*Viewer*:
`$ python3 game/viewer.py`

Cliente:
- `$ python3 game/client.py` (para jogar manualmente com as setas)
- `$ python3 student.py` (para correr o agente inteligente)

## Créditos
- Rafael Gonçalves (102534)
- André Butuc (103530)