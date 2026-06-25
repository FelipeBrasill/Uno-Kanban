from uno.backend.models.carta import Carta
from uno.backend.models.mao import Mao
class Jogador:
    '''Clase que representa un jugador de UNOKanBAN.'''
    def __init__(self, nome: str):
        self.nome : str = nome
        self._mao : Mao = Mao()
    def comprar_carta(self, carta: Carta):
        '''Adiciona uma carta à mão do jogador.'''
        self._mao.appen
