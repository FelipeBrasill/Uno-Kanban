from .enum import CorCarta, TipoEfeito
from .carta import Carta


class CartaAcao(Carta):
    '''Clase que representa una carta de acción de UNOKAnBAN.'''
    def __init__(self, cor: CorCarta, acao: TipoEfeito ):
        super().__init__(cor)
        self.acao = acao