from uno.backend.models.baralho import Baralho
from uno.backend.models.mao import Mao
from uno.backend.models.carta import Carta
from uno.backend.models.config import QTD_COMPRA_PADRAO
class Jogador:
    def __init__(self, nome: str):
        self.nome : str = nome
        self._mao : Mao = Mao()
        self._flag_desistiu : bool = False

    def comprar_carta(self, baralho: Baralho, quantidade : int = QTD_COMPRA_PADRAO ) -> None:
        '''Permite que o jogador compre uma carta do baralho.'''
        for _ in range(quantidade):    
            carta = baralho.retirar_carta()
            self._mao.adicionar_carta(carta)
        
    def desistir(self) -> None:
        '''Permite que o jogador desista da partida.'''
        self._flag_desistiu = True
    
    def passar_vez(self) -> None:
        '''Permite que o jogador passe a vez.'''

    def jogar_carta(self, carta: Carta) -> Carta:
        '''Permite que o jogador jogue uma carta da sua mão.'''
        # jogador seleciona uma carta da mão 
        self._mao.remover_carta(carta)
        # carta é adicionada na pilha
        self.adicionar_carta(carta)
        return carta
    
    
    
