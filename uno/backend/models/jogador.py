from uno.backend.models.baralho import Baralho
from uno.backend.models.mao import Mao
from uno.backend.models.carta import Carta
from uno.backend.models.config import QTD_COMPRA_PADRAO
from uno.backend.models.enum import EstadoRealiEhGay, EstadoJogador
class Jogador:
    def __init__(self, nome: str):
        self.nome: str = nome
        self._mao: Mao = Mao()
        self.estado_jogador: EstadoJogador = EstadoJogador.ATIVO
        self.estado_realiehgay : EstadoRealiEhGay  = EstadoRealiEhGay.NORMAL

    def comprar_carta(self, baralho: Baralho, quantidade: int = QTD_COMPRA_PADRAO) -> Carta | None:
        '''Permite comprar n cartas.'''
        carta = None
        for _ in range(quantidade):
            carta = baralho.retirar_carta()
            self._mao.adicionar_carta(carta)

        if quantidade == QTD_COMPRA_PADRAO:
            return carta
        return None

    def jogar_carta(self, carta: Carta) -> None:
        '''Remove a carta da mão do jogador.'''
        self._mao.remover_carta(carta)

    def desistir(self) -> None:
        '''Marca o jogador como desistente.'''
        self._flag_desistiu = EstadoJogador.DESISTIU

    @property
    def mao_vazia(self) -> bool:
        '''Retorna True se o jogador não tem mais cartas.'''
        return self.quantidade_cartas_mao == 0

    @property
    def quantidade_cartas_mao(self)-> int:
        return self._mao.quantidade
     
    def obter_mao(self)-> Mao:
        return self._mao
    
    def trocar_mao_com(self, outro: 'Jogador') -> None:
        '''Troca a mão com outro jogador.'''
        self._mao, outro._mao = outro._mao, self._mao