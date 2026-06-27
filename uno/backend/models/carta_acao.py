
from uno.backend.models.carta import Carta


class CartaAcao(Carta):
    '''Clase que representa una carta de acción de UNOKAnBAN.'''
    def __init__(self, cor: str, acao: str):
        super().__init__(cor)
        self.acao = acao