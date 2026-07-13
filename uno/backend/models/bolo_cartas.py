# colecao_cartas.py
from abc import ABC
from collections import deque
from .carta import Carta

class BoloCartas(ABC):
    '''Classe abstrata que representa uma coleção de cartas.'''

    def __init__(self):
        self._cartas: deque[Carta] = deque()

    @property
    def quantidade(self) -> int:
        return len(self._cartas)

    def esta_vazia(self) -> bool:
        return self.quantidade == 0