
from uno.backend.models.carta import Carta


class Mao:
    def __init__(self):
        '''Classe que representa uma mão de cartas de UNOKanban.'''
        self.cartas : list[Carta] = []
    @property
    def quantidade(self) -> int:
        '''Retorna a quantidade de cartas na mão.'''
        return len(self.cartas)

