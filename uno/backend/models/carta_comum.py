
from uno.backend.models.carta import Carta


class CartaComum(Carta):
    '''Clase que representa una carta común de UNOKAnBAN.'''
    def __init__(self, cor: str, valor: int):
        super().__init__(cor)
        self.valor = valor