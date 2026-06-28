from uno.backend.models.carta import Carta
from collections import deque


class PilhaDescarte:
    '''Classe que representa a pilha de descarte de UNO.'''

    def __init__(self):
        '''Inicializa a pilha de descarte vazio.'''
        self._cartas: deque[Carta] = deque()

    @property
    def quantidade(self) -> int:
        '''Retorna a quantidade de cartas na pilha de descarte.'''
        return len(self._cartas)
    
    def obter_carta_topo(self) -> Carta:
        '''Retorna a carta do topo da pilha de descarte.'''
        if not self._cartas:
            raise ValueError('A pilha de descarte está vazia.')
        topo_descarte = self._cartas[-1]
        return topo_descarte
    
    def adicionar_carta(self, carta: Carta) -> None:
        '''Adiciona uma carta ao topo da pilha de descarte.'''
        self._cartas.append(carta)
    
    def reciclar_descarte(self) -> list[Carta]:
        '''Retira todas as cartas da pilha de descarte exceto o topo'''
        topo = self._cartas.pop()
        cartas_antigas = list(self._cartas)
        self._cartas.clear()
        self._cartas.append(topo)
        
        return cartas_antigas