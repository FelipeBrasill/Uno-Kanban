'''O arquivo `baralho.py` contém a classe `Baralho`, que representa um baralho de cartas do jogo UNO.'''
from .carta import Carta
from collections import deque
import random
from .carta_comum import CartaComum
from .carta_acao import CartaAcao
from .config import (
    BASE_NUMERICA_JOGO,
    EMBARALHAR_PADRAO,
    QTD_CARTA_PRETA)
from .enum import CorCarta, TipoEfeito

class Baralho:
    '''Classe que representa um baralho de UNO.'''

    def __init__(self):
        super().__init__()
        '''Inicializa um baralho vazio.'''
        self._cartas: deque[Carta] = deque()
        self._popular_baralho()

    @property
    def quantidade(self) -> int:
        '''Retorna a quantidade de cartas no baralho.'''
        return len(self._cartas)

    def embaralhar(self, numero_embaralhadas: int = EMBARALHAR_PADRAO) -> None:
        '''Embaralha o baralho.'''
        cartas_lista = list(self._cartas)
        for _ in range(numero_embaralhadas):
            random.shuffle(cartas_lista)
        self._cartas = deque(cartas_lista)

    def retirar_carta(self) -> Carta:
        '''Retira uma carta do topo do baralho.'''
        if not self._cartas:
            raise ValueError('O baralho está vazio.')
        return self._cartas.popleft()
    def _popular_baralho(self) -> None:
        '''Adiciona cartas ao baralho em tempo de execução'''
        cores_normais = [cor for cor in CorCarta if cor != CorCarta.PRETO]
        
        efeitos_coloridos = [
            TipoEfeito.BLOQUEIO,
            TipoEfeito.REVERSO,
            TipoEfeito.COMPRA_DUAS,
            TipoEfeito.TROCAR_MAO,
        ]
        
        efeitos_pretos = [
            TipoEfeito.TROCAR_COR,
            TipoEfeito.COMPRA_QUATRO,
        ]

        # cartas comuns -> 2 de cada número por cor
        for cor in cores_normais:
            for valor in range(BASE_NUMERICA_JOGO):
                for _ in range(2):
                    self._cartas.append(CartaComum(cor, valor))

        # cartas de ação coloridas -> 2 de cada efeito por cor
        for cor in cores_normais:
            for efeito in efeitos_coloridos:
                for _ in range(2):
                    self._cartas.append(CartaAcao(cor, efeito))

        # cartas pretas -> QTD_CARTA_PRETA de cada tipo
        for efeito in efeitos_pretos:
            for _ in range(QTD_CARTA_PRETA):
                self._cartas.append(CartaAcao(CorCarta.PRETO, efeito))
    
    def reabastecer_baralho(self, cartas_recicladas : list[Carta])-> None:
        self._cartas.extend(cartas_recicladas)
        self.embaralhar()
    
    def esta_vazio(self)-> bool:
        return self.quantidade == 0