
from uno.backend.models.carta import Carta


class CartaAcao(Carta):
    '''Clase que representa una carta de acción de UNOKAnBAN.'''
    def __init__(self, color: str, acao: str):
        super().__init__(color)
        self.acao = acao