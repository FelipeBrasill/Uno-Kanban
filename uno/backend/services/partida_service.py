from uuid import UUID
from ..models.partida import Partida
from ..models.jogador import Jogador
from ..models.bot import Bot
from ..models.carta import Carta
from ..models.carta_acao import CartaAcao
from ..models.carta_comum import CartaComum
from ..models.enum import CorCarta, TipoEfeito
from ..models.config import MIN_JOGADORES, MAX_JOGADORES, COOLDOWN_BOT_SEGUNDOS, NOMES_BOT_DISPONIVEIS
from ..schemas.schema_saida import *
import random
import time

class PartidaServico:
    def __init__(self):
        self._partidas: dict[int, Partida] = {}
        self._jogadores_cadastrados: dict[str, Jogador] = {}

    # =========================================================
    # AUXILIARES
    # =========================================================

    def buscar_partida(self, id_partida: int) -> Partida:
        partida = self._partidas.get(id_partida)
        if partida is None:
            raise ValueError(f"Partida {id_partida} não encontrada")
        return partida

    def buscar_jogador(self, nome: str) -> Jogador:
        jogador = self._jogadores_cadastrados.get(nome)
        if jogador is None:
            raise ValueError(f"Jogador '{nome}' não encontrado.")
        return jogador

    def _buscar_carta_na_mao(self, jogador: Jogador, id_carta: UUID) -> Carta:
        carta = next((c for c in jogador.obter_mao() if c.id == id_carta), None)
        if carta is None:
            raise ValueError("Carta não encontrada na mão do jogador.")
        return carta

    def _carta_schema(self, carta: Carta) -> CartaAcaoSchema | CartaComumSchema:
        if isinstance(carta, CartaAcao):
            return CartaAcaoSchema(id=carta.id, cor=carta.cor, acao=carta.acao)
        elif isinstance(carta, CartaComum):
            return CartaComumSchema(id=carta.id, cor=carta.cor, valor=carta.valor)
        raise ValueError(f"Tipo de carta desconhecido: {type(carta)}")

    def _jogador_schema(self, jogador: Jogador) -> JogadorSchema:
        return JogadorSchema(
            nome=jogador.nome,
            quantidade_cartas=jogador.quantidade_cartas_mao,
            estado_realiehgay=jogador.estado_realiehgay,
            estado_jogador=jogador.estado_jogador
        )

    # =========================================================
    # BOT
    # =========================================================

    def _tempo_reacao_gritar_uno() -> float:
        return random.uniform(0.5, 1.5)

    def _processar_turnos_bot(self, partida: Partida) -> None:
        """Enquanto o jogador da vez for um Bot, decide e executa a jogada dele sozinho."""

        while not partida.partida_encerrou():
            jogador_atual = partida.jogador_atual()

            if not isinstance(jogador_atual, Bot):
                break

            bot = jogador_atual

            time.sleep(COOLDOWN_BOT_SEGUNDOS)

            cartas_validas = [
                carta
                for carta in bot.obter_mao()
                if partida.verificar_jogada(carta)
            ]

            carta = bot.escolher_jogada(cartas_validas)

            if carta is None:
                partida.orquestrar_compra_voluntaria()
                continue

            partida.orquestrar_jogada_carta(carta)

            if partida.partida_encerrou():
                break

            if (
                isinstance(carta, CartaAcao)
                and carta.acao in (
                    TipoEfeito.TROCAR_COR,
                    TipoEfeito.COMPRA_QUATRO,
                )
            ):
                cor = bot.escolher_cor()
                partida.aplicar_escolha_cor(cor)

                if partida.partida_encerrou():
                    break

            if (
                isinstance(carta, CartaAcao)
                and carta.acao == TipoEfeito.TROCAR_MAO
            ):
                outros = [
                    jogador
                    for jogador in partida.jogadores
                    if jogador is not bot
                ]

                alvo = bot.escolher_alvo_troca(outros)
                partida.aplicar_troca_mao(alvo)

                if partida.partida_encerrou():
                    break

    # =========================================================
    # ESTADO
    # =========================================================

    def estado_partida(self, partida: Partida) -> EstadoPartidaSchema:
        vencedor = next((j for j in partida.jogadores if j.mao_vazia), None)
        return EstadoPartidaSchema(
            jogador_atual=self._jogador_schema(partida.jogador_atual()),
            vencedor=self._jogador_schema(vencedor) if vencedor else None,
            carta_topo=self._carta_schema(partida.carta_topo_descarte),
            jogadores=[
                self._jogador_schema(j)
                for j in sorted(partida.jogadores, key=lambda j: j.nome)
            ]
        )

    # =========================================================
    # CADASTRO
    # =========================================================

    def cadastrar_jogador(self, nome: str) -> JogadorSchema:
        nome_limpo = nome.strip()
        if not nome_limpo:
            raise ValueError("O nome do jogador não pode estar vazio.")
        if nome_limpo in self._jogadores_cadastrados:
            raise ValueError(f"Jogador '{nome_limpo}' já cadastrado.")
        novo_jogador = Jogador(nome=nome_limpo)
        self._jogadores_cadastrados[nome_limpo] = novo_jogador
        return self._jogador_schema(novo_jogador)

    def _gerar_nomes_bots(self, quantidade: int) -> list[str]:
        '''
        Sorteia `quantidade` nomes de bot, sem repetir enquanto a lista de
        NOMES_BOT_DISPONIVEIS não se esgotar. Se pedirem mais bots do que
        nomes existentes, a lista roda de novo com um sufixo numérico
        (ex: "Benyo", depois "Benyo II") pra manter os nomes únicos dentro
        da partida.
        '''
        pool = NOMES_BOT_DISPONIVEIS.copy()
        random.shuffle(pool)
        nomes = []
        for i in range(quantidade):
            base = pool[i % len(pool)]
            rodada = i // len(pool)
            nomes.append(base if rodada == 0 else f"{base} {rodada + 1}")
        return nomes

    def _criar_bot_para_partida(self, nome_bot: str) -> Bot:
        '''
        Cria um Bot com o nome sorteado. Sempre cria uma instância nova --
        se o nome já estiver cadastrado (ex: mesma partida recriada com o
        mesmo id, ou coincidência entre partidas), o bot antigo é
        substituído no registro (sem carregar mão/estado de uma partida
        anterior).
        '''
        bot = Bot(nome=nome_bot)
        self._jogadores_cadastrados[nome_bot] = bot
        return bot

    # =========================================================
    # PARTIDA
    # =========================================================

    def criar_partida(self, id_partida: int, nome_jogador: str, quantidade_bots: int) -> EstadoPartidaSchema:
        '''Cria a partida com o jogador humano (já cadastrado) + N bots.'''
        total_jogadores = 1 + quantidade_bots
        if total_jogadores < MIN_JOGADORES:
            raise ValueError(f"Precisa de pelo menos {MIN_JOGADORES} jogadores (você + bots).")
        if total_jogadores > MAX_JOGADORES:
            raise ValueError(f"Máximo de {MAX_JOGADORES} jogadores permitido.")

        jogador = self.buscar_jogador(nome_jogador)
        nomes_bots = self._gerar_nomes_bots(quantidade_bots)
        bots = [self._criar_bot_para_partida(nome) for nome in nomes_bots]

        partida = Partida(id_partida, [jogador, *bots])
        partida.iniciar_partida()
        self._partidas[id_partida] = partida
        self._processar_turnos_bot(partida)
        return self.estado_partida(partida)

    # =========================================================
    # TURNO
    # =========================================================

    def executar_turno(self, id_partida: int, id_carta: UUID) -> EstadoPartidaSchema:
        partida = self.buscar_partida(id_partida)
        jogador = partida.jogador_atual()
        carta = self._buscar_carta_na_mao(jogador, id_carta)
        partida.orquestrar_jogada_carta(carta)
        self._processar_turnos_bot(partida)
        return self.estado_partida(partida)

    def comprar_carta_turno(self, id_partida: int) -> EstadoPartidaSchema:
        partida = self.buscar_partida(id_partida)
        partida.orquestrar_compra_voluntaria()
        self._processar_turnos_bot(partida)
        return self.estado_partida(partida)

    def escolher_cor(self, id_partida: int, cor: CorCarta) -> EstadoPartidaSchema:
        partida = self.buscar_partida(id_partida)
        if partida.carta_topo_descarte.cor != CorCarta.PRETO:
            raise ValueError("Escolha de cor só é válida após carta preta")
        partida.aplicar_escolha_cor(cor)
        self._processar_turnos_bot(partida)
        return self.estado_partida(partida)

    def gritar_realiehgay(self, id_partida: int, nome_declarante: str, nome_alvo: str) -> EstadoPartidaSchema:
        partida = self.buscar_partida(id_partida)
        declarante = self.buscar_jogador(nome_declarante)
        alvo = self.buscar_jogador(nome_alvo)
        partida.declarar_realiehgay(declarante, alvo)
        return self.estado_partida(partida)

    def obter_mao(self, id_partida: int, nome_jogador: str) -> MaoSchema:
        partida = self.buscar_partida(id_partida)
        jogador = next((j for j in partida.jogadores if j.nome == nome_jogador), None)
        if jogador is None:
            raise ValueError(f"Jogador '{nome_jogador}' não está na partida {id_partida}")
        return MaoSchema(mao=[self._carta_schema(carta) for carta in jogador.obter_mao()])

    def executar_trocar_mao(self, id_partida: int, nome_alvo: str) -> EstadoPartidaSchema:
        partida = self.buscar_partida(id_partida)
        alvo = self.buscar_jogador(nome_alvo)
        partida.aplicar_troca_mao(alvo)
        self._processar_turnos_bot(partida)
        return self.estado_partida(partida)