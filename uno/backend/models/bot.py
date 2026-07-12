from uno.backend.models.carta import Carta
from uno.backend.models.enum import CorCarta
from uno.backend.models.jogador import Jogador
import random


class Bot(Jogador):
    def __init__(self, nome: str):
        super().__init__(nome)

    def escolher_jogada(self, cartas_validas: list[Carta]) -> Carta | None:
        '''Decide qual carta jogar dentre as válidas.'''
        if not cartas_validas:
            return None
        return random.choice(cartas_validas)

    def escolher_cor(self) -> CorCarta:
        '''Decide qual cor declarar após jogar uma carta preta.'''
        cores_validas = [c for c in CorCarta if c != CorCarta.PRETO]
        return random.choice(cores_validas)
    
    def escolher_alvo_troca(self, outros_jogadores: list[Jogador]) -> Jogador:
        '''Decide com qual jogador trocar a mão.'''
        return random.choice(outros_jogadores)
    