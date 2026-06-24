from uno.backend.models.carta import Carta
from collections import deque
import random

class Baralho:
    '''Classe que representa um baralho de UNO.'''

    def __init__(self):
        '''Inicializa um baralho vazio.'''
        self._cartas: deque[Carta] = deque()

    @property
    def quantidade(self) -> int:
        '''Retorna a quantidade de cartas no baralho.'''
        return len(self._cartas)

    def embaralhar(self) -> None:
        '''Embaralha o baralho.'''
        cartas_lista = list(self._cartas)
        random.shuffle(cartas_lista)
        self._cartas = deque(cartas_lista)

    def retirar_carta(self) -> Carta:
        '''Retira uma carta do topo do baralho.'''
        if not self._cartas:
            raise ValueError('O baralho está vazio.')
        return self._cartas.popleft()
    