from uno.backend.models.baralho import Baralho
from uno.backend.models.mao import Mao
from uno.backend.models.carta import Carta

class Jogador:
    def __init__(self, nome: str):
        self._nome : str = nome
        self._mao : Mao = Mao()
        self._flag_desistiu : bool = False

    def comprar_carta(self, baralho: Baralho) -> None:
        '''Permite que o jogador compre uma carta do baralho.'''
        carta = baralho.retirar_carta()
        self._mao.adicionar_carta(carta)
    
    def desistir(self) -> None:
        '''Permite que o jogador desista da partida.'''
        self._flag_desistiu = True
    
    def passar_vez(self) -> None:
        '''Permite que o jogador passe a vez.'''

    def jogar_carta(self, carta: Carta) -> None:
        '''Permite que o jogador jogue uma carta da sua mão.'''
        self._mao.remover_carta(carta)
    
