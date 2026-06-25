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
    
    def retirar_carta(self) -> Carta:
        '''Retira uma carta do topo da pilha de descarte.'''
        if not self._cartas:
            raise ValueError('A pilha de descarte está vazia.')
        return self._cartas.pop()
    
    def adicionar_carta(self, carta: Carta):
        '''Adiciona uma carta ao topo da pilha de descarte.'''
        self._cartas.append(carta)
    