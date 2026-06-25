from uno.backend.models.jogador import Jogador
from collections import deque
from uno.backend.models.baralho import Baralho
import random
from uno.backend.models.pilha_descarte import PilhaDescarte
from uno.backend.models.config import MAO_INICIAL
class Partida:
    '''Classe que representa uma partida de UNO.'''
    
    def __init__(self, id_partida: int, jogadores: list[Jogador]):
        self._id_partida: int = id_partida
        self._turno: int = 0
        self._jogadores: deque[Jogador] = deque(jogadores)
        self._pilha_descarte: PilhaDescarte = PilhaDescarte()
    
    def jogador_atual(self) -> Jogador:
        '''Retorna o jogador atual da partida.'''
        return self._jogadores[0]

    def iniciar_partida(self, baralho: Baralho) -> None:
        '''Inicia a partida.'''
        baralho.embaralhar()
        self.sortear_ordem_jogadores()
        self.distribuir_cartas(baralho)
        self.tirar_carta_inicial_descarte(baralho)
        self._turno = 0

    def proximo_turno(self) -> None:
        '''Avança para o próximo turno da partida.'''
        self._turno += 1
        self._jogadores.rotate(-1)

    def distribuir_cartas(self, baralho: Baralho, mao_inicial: int = MAO_INICIAL) -> None:
        '''Distribui cartas para os jogadores da partida.'''
        for jogador in self._jogadores:
            for _ in range(mao_inicial):
                jogador.comprar_carta(baralho)

    def tirar_carta_inicial_descarte(self, baralho: Baralho) -> None:
        '''Retira a carta inicial da pilha de descarte.'''
        carta_inicial = baralho.retirar_carta()
        self._pilha_descarte.adicionar_carta(carta_inicial)
    
    def sortear_ordem_jogadores(self) -> None:
        '''Sorteia a ordem dos jogadores da partida.'''
        lista_jogadores = list(self._jogadores)
        random.shuffle(lista_jogadores)
        self._jogadores = deque(lista_jogadores)
    
