from uno.backend.models.partida import Partida
from uno.backend.models.jogador import Jogador
from uno.backend.models.carta import Carta
from uno.backend.models.carta_acao import CartaAcao
from uno.backend.models.carta_comum import CartaComum
from uno.backend.models.enum import CorCarta
from uno.backend.schemas.schema_saida import *
class PartidaServico:
    def __init__(self):
        self._partidas: dict[int, Partida] = {}

    def buscar_partida(self, id_partida: int) -> Partida:
        '''Busca uma partida pelo id, lança erro se não encontrar.'''
        partida = self._partidas.get(id_partida)
        if partida is None:
            raise ValueError(f"Partida {id_partida} não encontrada")
        return partida

    def _validar_vez(self, partida: Partida, jogador: Jogador) -> None:
        '''Lança erro se não for a vez do jogador.'''
        if jogador != partida.jogador_atual():
            raise ValueError("Não é a vez desse jogador")

    def estado_partida(self, partida: Partida) -> EstadoPartidaSchema:
        '''Retorna o estado atual da partida.'''
        vencedor = next(
            (j for j in partida.jogadores if j.mao_vazia),
            None
        )

        carta = partida.carta_topo_descarte
        if isinstance(carta, CartaAcao):
            carta_schema = CartaAcaoSchema(
                cor=carta.cor,
                acao =carta.acao
            )
        elif isinstance(carta, CartaComum):
            carta_schema = CartaComumSchema(
                cor=carta.cor,
                valor=carta.valor
            )
        else:
            raise ValueError(f"Tipo de carta desconhecido: {type(carta)}")

        return EstadoPartidaSchema(
            jogador_atual=JogadorSchema(
                nome=partida.jogador_atual().nome,
                quantidade_cartas=partida.jogador_atual().quantidade_cartas_mao,
                estado_realiehgay=partida.jogador_atual().estado_realiehgay,
                estado_jogador=partida.jogador_atual().estado_jogador
            ),
            vencedor=JogadorSchema(
                nome=vencedor.nome,
                quantidade_cartas=vencedor.quantidade_cartas_mao,
                estado_realiehgay=vencedor.estado_realiehgay,
                estado_jogador=vencedor.estado_jogador
            ) if vencedor else None,
            carta_topo=carta_schema,       
            jogadores=[
                JogadorSchema(
                    nome=j.nome,
                    quantidade_cartas=j.quantidade_cartas_mao,
                    estado_realiehgay=j.estado_realiehgay,
                    estado_jogador=j.estado_jogador
                )
                for j in partida.jogadores
            ]
        )
    def criar_partida(self, id_partida: int, jogadores: list[Jogador]) -> EstadoPartidaSchema:
        '''Cria e inicia uma nova partida.'''
        partida = Partida(id_partida, jogadores)
        partida.iniciar_partida()
        self._partidas[id_partida] = partida
        return self.estado_partida(partida)

    def executar_turno(self, id_partida: int, jogador: Jogador, carta: Carta) -> EstadoPartidaSchema:
        '''Executa a jogada de uma carta no turno atual.'''
        partida = self.buscar_partida(id_partida)
        if partida.partida_encerrou():
            raise ValueError("A partida encerrou: Um jogador venceu")
        self._validar_vez(partida, jogador)
        partida.orquestrar_jogada_carta(carta)
        return self.estado_partida(partida)

    def comprar_carta_turno(self, id_partida: int, jogador: Jogador) -> EstadoPartidaSchema:
        '''Executa a compra de carta quando jogador não tem jogada válida.'''
        partida = self.buscar_partida(id_partida)
        self._validar_vez(partida, jogador)
        partida.orquestrar_compra_voluntaria()
        return self.estado_partida(partida)

    def escolher_cor(self, id_partida: int, jogador: Jogador, cor: CorCarta) -> EstadoPartidaSchema:
        partida = self.buscar_partida(id_partida)
        self._validar_vez(partida, jogador)
        if partida.carta_topo_descarte.cor != CorCarta.PRETO:
            raise ValueError("Escolha de cor só é válida após carta preta")
        partida.aplicar_escolha_cor(cor)
        return self.estado_partida(partida)

    def gritar_realiehgay(self, id_partida: int, declarante: Jogador, alvo: Jogador) -> EstadoPartidaSchema:
        '''Qualquer jogador declara realiehgay por qualquer outro.'''
        partida = self.buscar_partida(id_partida)
        partida.declarar_realiehgay(declarante, alvo)
        return self.estado_partida(partida)

    def obter_mao(self, id_partida: int, jogador: Jogador) -> MaoSchema:
        self.buscar_partida(id_partida)
        
        cartas : list[CartaAcaoSchema | CartaComumSchema] = []
        for carta  in jogador.obter_mao():
            if isinstance(carta, CartaAcao):
                cartas.append(CartaAcaoSchema(
                    cor =  carta.cor,
                    acao = carta.acao
                ))
            elif isinstance(carta,CartaComum):
                cartas.append(CartaComumSchema(
                    cor   =  carta.cor,
                    valor =  carta.valor
                ))
        
        return MaoSchema(mao = cartas)

    def executar_trocar_mao(self, id_partida: int, jogador: Jogador, alvo: Jogador) -> EstadoPartidaSchema:
        '''Jogador escolhe com quem trocar a mão.'''
        partida = self.buscar_partida(id_partida)
        self._validar_vez(partida, jogador)
        partida.aplicar_troca_mao(alvo)
        partida.proximo_turno()
        return self.estado_partida(partida)
    