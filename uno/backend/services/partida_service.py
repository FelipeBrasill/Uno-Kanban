from uuid import UUID
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
        self._jogadores_cadastrados: dict[str, Jogador] = {}

    # =========================================================
    # AUXILIARES
    # =========================================================

    def buscar_partida(self, id_partida: int) -> Partida:
        '''Busca uma partida pelo id, lança erro se não encontrar.'''
        partida = self._partidas.get(id_partida)
        if partida is None:
            raise ValueError(f"Partida {id_partida} não encontrada")
        return partida

    def buscar_jogador(self, nome: str) -> Jogador:
        '''Busca um jogador cadastrado pelo nome.'''
        jogador = self._jogadores_cadastrados.get(nome)
        if jogador is None:
            raise ValueError(f"Jogador '{nome}' não encontrado.")
        return jogador

    def _buscar_carta_na_mao(self, jogador: Jogador, id_carta: UUID) -> Carta:
        '''Busca uma carta na mão do jogador pelo UUID.'''
        carta = next((c for c in jogador.obter_mao() if c.id == id_carta), None)
        if carta is None:
            raise ValueError("Carta não encontrada na mão do jogador.")
        return carta

    def _carta_schema(self, carta: Carta) -> CartaAcaoSchema | CartaComumSchema:
        '''Converte uma Carta para o schema correto.'''
        if isinstance(carta, CartaAcao):
            return CartaAcaoSchema(
                id=carta.id,
                cor=carta.cor,
                acao =carta.acao
            )
        elif isinstance(carta, CartaComum):
            return CartaComumSchema(
                id=carta.id,
                cor=carta.cor,
                valor=carta.valor
            )
        raise ValueError(f"Tipo de carta desconhecido: {type(carta)}")

    def _jogador_schema(self, jogador: Jogador) -> JogadorSchema:
        '''Converte um Jogador para JogadorSchema.'''
        return JogadorSchema(
            nome=jogador.nome,
            quantidade_cartas=jogador.quantidade_cartas_mao,
            estado_realiehgay=jogador.estado_realiehgay,
            estado_jogador=jogador.estado_jogador
        )

    # =========================================================
    # ESTADO
    # =========================================================

    def estado_partida(self, partida: Partida) -> EstadoPartidaSchema:
        '''Retorna o estado atual da partida.'''
        vencedor = next(
            (j for j in partida.jogadores if j.mao_vazia),
            None
        )

        return EstadoPartidaSchema(
            jogador_atual=self._jogador_schema(partida.jogador_atual()),
            vencedor=self._jogador_schema(vencedor) if vencedor else None,
            carta_topo=self._carta_schema(partida.carta_topo_descarte),
            jogadores=[self._jogador_schema(j) for j in partida.jogadores]
        )

    # =========================================================
    # CADASTRO
    # =========================================================

    def cadastrar_jogador(self, nome: str) -> JogadorSchema:
        '''Cadastra um novo jogador na memória se o nome for válido e único.'''
        nome_limpo = nome.strip()

        if not nome_limpo:
            raise ValueError("O nome do jogador não pode estar vazio.")

        if nome_limpo in self._jogadores_cadastrados:
            raise ValueError(f"Jogador '{nome_limpo}' já cadastrado.")

        novo_jogador = Jogador(nome=nome_limpo)
        self._jogadores_cadastrados[nome_limpo] = novo_jogador
        return self._jogador_schema(novo_jogador)

    # =========================================================
    # PARTIDA
    # =========================================================

    def criar_partida(self, id_partida: int, nomes_jogadores: list[str]) -> EstadoPartidaSchema:
        '''Cria e inicia uma nova partida buscando jogadores pelo nome.'''
        if len(nomes_jogadores) < 2:
            raise ValueError("Precisa de pelo menos 2 jogadores.")
        jogadores = [self.buscar_jogador(nome) for nome in nomes_jogadores]
        partida = Partida(id_partida, jogadores)
        partida.iniciar_partida()
        self._partidas[id_partida] = partida
        return self.estado_partida(partida)

    # =========================================================
    # TURNO
    # =========================================================

    def executar_turno(self, id_partida: int, id_carta: UUID) -> EstadoPartidaSchema:
        '''Executa a jogada de uma carta no turno atual.'''
        partida = self.buscar_partida(id_partida)
        jogador = partida.jogador_atual()
        carta = self._buscar_carta_na_mao(jogador, id_carta)
        partida.orquestrar_jogada_carta(carta)
        return self.estado_partida(partida)

    def comprar_carta_turno(self, id_partida: int) -> EstadoPartidaSchema:
        '''Executa a compra de carta quando jogador não tem jogada válida.'''
        partida = self.buscar_partida(id_partida)
        partida.orquestrar_compra_voluntaria()
        return self.estado_partida(partida)

    def escolher_cor(self, id_partida: int, cor: CorCarta) -> EstadoPartidaSchema:
        '''Define a cor após jogar TROCAR_COR ou COMPRA_QUATRO.'''
        partida = self.buscar_partida(id_partida)
        if partida.carta_topo_descarte.cor != CorCarta.PRETO:
            raise ValueError("Escolha de cor só é válida após carta preta")
        partida.aplicar_escolha_cor(cor)
        return self.estado_partida(partida)

    def gritar_realiehgay(self, id_partida: int, nome_declarante: str, nome_alvo: str) -> EstadoPartidaSchema:
        '''Qualquer jogador declara realiehgay por qualquer outro.'''
        partida = self.buscar_partida(id_partida)
        declarante = self.buscar_jogador(nome_declarante)
        alvo = self.buscar_jogador(nome_alvo)
        partida.declarar_realiehgay(declarante, alvo)
        return self.estado_partida(partida)

    def obter_mao(self, id_partida: int) -> MaoSchema:
        '''Retorna a mão do jogador atual.'''
        partida = self.buscar_partida(id_partida)
        jogador = partida.jogador_atual()
        return MaoSchema(
            mao=[self._carta_schema(carta) for carta in jogador.obter_mao()]
        )

    def executar_trocar_mao(self, id_partida: int, nome_alvo: str) -> EstadoPartidaSchema:
        '''Jogador atual troca a mão com o alvo escolhido.'''
        partida = self.buscar_partida(id_partida)
        alvo = self.buscar_jogador(nome_alvo)
        partida.aplicar_troca_mao(alvo)
        return self.estado_partida(partida)