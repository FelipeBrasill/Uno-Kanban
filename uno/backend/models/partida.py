from uno.backend.models.carta_acao import CartaAcao
from uno.backend.models.carta_comum import CartaComum
from uno.backend.models.jogador import Jogador
from collections import deque
from uno.backend.models.baralho import Baralho
import random
from uno.backend.models.pilha_descarte import PilhaDescarte
from uno.backend.models.config import *
from uno.backend.models.enum import TipoEfeito, CorCarta, EstadoRealiEhGay
from uno.backend.models.carta import Carta

class Partida:
    '''Classe que representa uma partida de UNO.'''

    def __init__(self, id_partida: int, jogadores: list[Jogador]):
        self._id_partida: int = id_partida
        self._turno: int = 0
        self._jogadores: deque[Jogador] = deque(jogadores)
        self._baralho: Baralho = Baralho()
        self._pilha_descarte: PilhaDescarte = PilhaDescarte()
        self._sentido: int = SENTIDO_PADRAO

    # =========================================================
    # PROPERTIES
    # =========================================================

    @property
    def carta_topo(self) -> Carta:
        return self._pilha_descarte.obter_carta_topo()

    @property
    def jogadores(self) -> list[Jogador]:
        return list(self._jogadores)

    # =========================================================
    # SETUP
    # =========================================================

    def jogador_atual(self) -> Jogador:
        return self._jogadores[0]

    def iniciar_partida(self) -> None:
        self._baralho.embaralhar()
        self.sortear_ordem_jogadores()
        self.distribuir_cartas()
        self.tirar_carta_inicial_descarte()
        self._turno = 0

    def distribuir_cartas(self, mao_inicial: int = MAO_INICIAL) -> None:
        for jogador in self._jogadores:
            for _ in range(mao_inicial):
                jogador.comprar_carta(self._baralho)

    def tirar_carta_inicial_descarte(self) -> None:
        carta_inicial = self._baralho.retirar_carta()
        self._pilha_descarte.adicionar_carta(carta_inicial)

    def sortear_ordem_jogadores(self) -> None:
        lista_jogadores = list(self._jogadores)
        random.shuffle(lista_jogadores)
        self._jogadores = deque(lista_jogadores)

    # =========================================================
    # TURNO
    # =========================================================

    def _proximo_jogador(self) -> None:
        self._jogadores.rotate(-self._sentido)

    def proximo_turno(self) -> None:
        jogador = self.jogador_atual()

        if jogador.estado_realiehgay == EstadoRealiEhGay.PODE_DECLARAR:
            jogador.estado_realiehgay = EstadoRealiEhGay.NORMAL
            self.aplicar_punicao(jogador)

        self._turno += 1
        self._proximo_jogador()

    # =========================================================
    # VERIFICAÇÕES
    # =========================================================

    def verificar_jogada(self, carta: Carta) -> bool:
        topo = self.carta_topo

        if carta.cor == CorCarta.PRETO:
            return True

        if carta.cor == topo.cor:
            return True

        if isinstance(carta, CartaAcao) and isinstance(topo, CartaAcao):
            return carta.acao == topo.acao

        if isinstance(carta, CartaComum) and isinstance(topo, CartaComum):
            return carta.valor == topo.valor

        return False

    def pode_jogar(self) -> bool:
        for carta in self.jogador_atual().obter_mao():
            if self.verificar_jogada(carta):
                return True
        return False

    def verificar_vitoria(self) -> bool:
        return self.jogador_atual().mao_vazia

    # =========================================================
    # ORQUESTRAÇÃO
    # =========================================================

    def orquestrar_jogada_carta(self, carta: Carta) -> None:
        '''Organiza o pipeline da jogada de carta do jogador.'''
        if not self.verificar_jogada(carta):
            raise ValueError("Jogada inválida")

        jogador = self.jogador_atual()
        jogador.jogar_carta(carta)
        self._pilha_descarte.adicionar_carta(carta)
        self.atualizar_estado_realiehgay(jogador)

        if self.verificar_vitoria():
            return

        if isinstance(carta, CartaAcao):
            self.ativar_efeito_carta_acao(carta)
            return

        self.proximo_turno()

    def orquestrar_compra_voluntaria(self) -> None:
        '''Jogador não tem jogada válida — compra uma carta e verifica se pode jogar.'''
        jogador = self.jogador_atual()
        carta_comprada = jogador.comprar_carta(self._baralho)
        if carta_comprada and self.verificar_jogada(carta_comprada):
            self.orquestrar_jogada_carta(carta_comprada)
        else:
            self.proximo_turno()

    def ativar_efeito_carta_acao(self, carta: Carta) -> None:
        '''Aplica o efeito da carta de ação no estado da partida.'''
        if not isinstance(carta, CartaAcao):
            return

        match carta.acao:
            case TipoEfeito.REVERSO:
                self._sentido *= -1
                self.proximo_turno()

            case TipoEfeito.BLOQUEIO:
                self._proximo_jogador()
                self.proximo_turno()

            case TipoEfeito.COMPRA_DUAS:
                proximo = self._jogadores[self._sentido]
                proximo.comprar_carta(self._baralho, QTD_COMPRA_MAIS_DOIS)
                self._proximo_jogador()
                self.proximo_turno()

            case TipoEfeito.COMPRA_QUATRO:
                proximo = self._jogadores[self._sentido]
                proximo.comprar_carta(self._baralho, QTD_COMPRA_MAIS_QUATRO)
                self._proximo_jogador()
                self.proximo_turno()

            case TipoEfeito.TROCAR_COR:
                pass  # tratado no serviço

            case TipoEfeito.TROCAR_MAO:
                pass  # tratado no serviço

    # =========================================================
    # EFEITOS 
    # =========================================================

    def aplicar_escolha_cor(self, cor: CorCarta) -> None:
        '''Aplica a cor escolhida pelo jogador após TROCAR_COR ou COMPRA_QUATRO.'''
        self.carta_topo.cor = cor
        self.proximo_turno()

    def aplicar_troca_mao(self, alvo: Jogador) -> None:
        '''Troca a mão do jogador atual com o alvo escolhido.'''
        jogador = self.jogador_atual()
        # Trocamos o objeto Mao inteiro entre os jogadores
        jogador.trocar_mao_com(alvo)
        self.proximo_turno()

    # =========================================================
    # REALIEHGAY
    # =========================================================

    def atualizar_estado_realiehgay(self, jogador: Jogador) -> None:
        if jogador.quantidade_cartas_mao == 1:
            jogador.estado_realiehgay = EstadoRealiEhGay.PODE_DECLARAR
        else:
            jogador.estado_realiehgay = EstadoRealiEhGay.NORMAL

    def aplicar_punicao(self, jogador: Jogador) -> None:
        jogador.comprar_carta(self._baralho, QTD_PUNICAO_REALIEHGAY)

    def declarar_realiehgay(self, declarante: Jogador, alvo: Jogador) -> bool:
        '''Orquestra a declaração do realiehgay.'''
        if alvo.estado_realiehgay != EstadoRealiEhGay.PODE_DECLARAR:
            self.aplicar_punicao(declarante)
            return False

        if alvo != declarante and alvo.estado_realiehgay == EstadoRealiEhGay.PODE_DECLARAR:
            alvo.estado_realiehgay = EstadoRealiEhGay.NORMAL
            self.aplicar_punicao(alvo)

        alvo.estado_realiehgay = EstadoRealiEhGay.DECLAROU
        return True