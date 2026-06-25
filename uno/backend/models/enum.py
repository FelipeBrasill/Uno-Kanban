'''Enumerações para representar os diferentes tipos de cartas e estados no jogo UNO.'''
from enum import Enum

class CorCarta(Enum):
    VERMELHO = "vermelho"
    AZUL = "azul"
    VERDE = "verde"
    AMARELO = "amarelo"
    PRETO = "preto"  # cor para cartas especiais 

class TipoEfeito(Enum):
    PULAR = "pular"
    INVERTER = "inverter"
    COMPRAR_DOIS = "comprar_dois"
    COMPRAR_QUATRO = "comprar_quatro"

class EstadoPartida(Enum):
    AGUARDANDO = "aguardando"   # esperando jogadores entrarem
    EM_ANDAMENTO = "em_andamento"
    FINALIZADA = "finalizada"

class EstadoJogador(Enum):
    ATIVO = "ativo"
    DESISTIU = "desistiu"
    VENCEU = "venceu"