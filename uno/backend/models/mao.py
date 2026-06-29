from typing import Iterator
from uno.backend.models.carta import Carta


class Mao:
    def __init__(self):
        '''Classe que representa uma mão de cartas de UNOKanban.'''
        self._cartas : list[Carta] = []
    
    def __iter__(self) -> Iterator[Carta]:
        return iter(self._cartas)

    @property
    def quantidade(self) -> int:
        '''Retorna a quantidade de cartas na mão.'''
        return len(self._cartas)
    
    def adicionar_carta(self, carta: Carta):
        '''Adiciona uma carta à mão.'''
        self._cartas.append(carta)
    
    def remover_carta(self, carta: Carta):
        '''Remove uma carta da mão.'''
        if carta in self._cartas:
            self._cartas.remove(carta)
        else:
            raise ValueError('A carta não está na mão.')
