'''O arquivo `baralho.py` contém a classe `Baralho`, que representa um baralho de cartas do jogo UNO.'''
from uno.backend.models.carta import Carta
from collections import deque
import random
from uno.backend.models.carta_comum import CartaComum
from uno.backend.models.carta_comum import CartaComum
from uno.backend.models.carta_acao import CartaAcao
from uno.backend.models.config import BASE_NUMERICA_JOGO, EMBARALHAR_PADRAO
from uno.backend.models.enum import CorCarta, TipoEfeito
class Baralho:
    '''Classe que representa um baralho de UNO.'''

    def __init__(self):
        '''Inicializa um baralho vazio.'''
        self._cartas: deque[Carta] = deque()

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
    
        cores_normais = [cor for cor in CorCarta if cor != CorCarta.PRETO]
        carta_acao = [acao for acao in TipoEfeito if acao != TipoEfeito.COMPRAR_QUATRO]
        for cor in cores_normais:
            for valor in range(BASE_NUMERICA_JOGO):
                for _ in range(2):
                    self._cartas.append(CartaComum(cor.value, valor))
            for acao in carta_acao:
                for _ in range(2):
                    self._cartas.append(CartaAcao(cor.value, acao.value))
        
        # coringas — só cor preta, sem número
        for _ in range(QTD_CARTA_CORINGA):  # 4 coringas no UNO padrão
            self._cartas.append(CartaAcao(CorCarta.PRETO.value, TipoEfeito.CORINGA.value))
                