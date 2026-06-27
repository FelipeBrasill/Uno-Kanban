from uno.backend.models.partida import Partida
from uno.backend.models.jogador import Jogador
from uno.backend.models.carta import Carta
from uno.backend.models.enum import CorCarta

class Servico:
    def __init__(self):
        self._partidas: dict[int, Partida] = {}

    def _buscar_partida(self, id_partida: int) -> Partida:
        '''Busca uma partida pelo id, lança erro se não encontrar.'''
        partida = self._partidas.get(id_partida)
        if partida is None:
            raise ValueError(f"Partida {id_partida} não encontrada")
        return partida

    def _validar_vez(self, partida: Partida, jogador: Jogador) -> None:
        '''Lança erro se não for a vez do jogador.'''
        if jogador != partida.jogador_atual():
            raise ValueError("Não é a vez desse jogador")

    def _estado_partida(self, partida: Partida) -> dict:
        '''Retorna o estado atual da partida.'''
        vencedor = next(
            (j.nome for j in partida.jogadores if j.mao_vazia),
            None
        )
        return {
            "jogador_atual": partida.jogador_atual().nome,
            "vencedor":      vencedor,
            "carta_topo": {
                "cor":            partida.carta_topo.cor.name,
                "valor_ou_efeito": (
                    getattr(partida.carta_topo, "valor", None)
                    or getattr(partida.carta_topo, "efeito",  None)
                )
            },
            "jogadores": [
                {
                    "nome":             j.nome,
                    "quantidade_cartas": j.quantidade_cartas_mao
                }
                for j in partida.jogadores
            ]
        }

    def criar_partida(self, id_partida: int, jogadores: list[Jogador]) -> dict:
        '''Cria e inicia uma nova partida.'''
        partida = Partida(id_partida, jogadores)
        partida.iniciar_partida()
        self._partidas[id_partida] = partida
        return self._estado_partida(partida)

    def executar_turno(self, id_partida: int, jogador: Jogador, carta: Carta) -> dict:
        '''Executa a jogada de uma carta no turno atual.'''
        partida = self._buscar_partida(id_partida)
        self._validar_vez(partida, jogador)
        partida.orquestrar_jogada_carta(carta)
        return self._estado_partida(partida)

    def comprar_carta_turno(self, id_partida: int, jogador: Jogador) -> dict:
        '''Executa a compra de carta quando jogador não tem jogada válida.'''
        partida = self._buscar_partida(id_partida)
        self._validar_vez(partida, jogador)
        partida.orquestrar_compra_voluntaria()
        return self._estado_partida(partida)

    def escolher_cor(self, id_partida: int, jogador: Jogador, cor: CorCarta) -> dict:
        partida = self._buscar_partida(id_partida)
        self._validar_vez(partida, jogador)
        if partida.carta_topo.cor != CorCarta.PRETO:
            raise ValueError("Escolha de cor só é válida após carta preta")
        partida.aplicar_escolha_cor(cor)
        return self._estado_partida(partida)

    def gritar_realiehgay(self, id_partida: int, declarante: Jogador, alvo: Jogador) -> dict:
        '''Qualquer jogador declara realiehgay por qualquer outro.'''
        partida = self._buscar_partida(id_partida)
        partida.declarar_realiehgay(declarante, alvo)
        return self._estado_partida(partida)

    def executar_trocar_mao(self, id_partida: int, jogador: Jogador, alvo: Jogador) -> dict:
        '''Jogador escolhe com quem trocar a mão.'''
        partida = self._buscar_partida(id_partida)
        self._validar_vez(partida, jogador)
        partida.aplicar_troca_mao(alvo)
        return self._estado_partida(partida)