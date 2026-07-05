from .enum import CorCarta
from .carta import Carta


class CartaComum(Carta):
    '''Classe que representa uma carta comum de UNOKAnBAN.'''
    def __init__(self, cor: CorCarta, valor: int):
        super().__init__(cor)
        self.valor = valor
        