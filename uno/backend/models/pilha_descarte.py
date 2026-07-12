
from .bolo_cartas import BoloCartas
from .carta import Carta

class PilhaDescarte(BoloCartas):
    '''Classe que representa a pilha de descarte de UNO.'''

    def __init__(self):
        '''Inicializa a pilha de descarte vazia.'''
        super().__init__()

    def obter_carta_topo(self) -> Carta:
        '''Retorna a carta do topo da pilha de descarte.'''
        if self.esta_vazia():
            raise ValueError('A pilha de descarte está vazia.')
        return self._cartas[-1]

    def adicionar_carta(self, carta: Carta) -> None:
        '''Adiciona uma carta ao topo da pilha de descarte.'''
        self._cartas.append(carta)

    def reciclar_descarte(self) -> list[Carta]:
        '''Retira todas as cartas da pilha de descarte exceto o topo.'''
        topo = self._cartas.pop()
        cartas_antigas = list(self._cartas)
        self._cartas.clear()
        self._cartas.append(topo)
        return cartas_antigas