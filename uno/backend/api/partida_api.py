'''
Camada exposta ao pywebview via `js_api`. Traduz entre o JSON que o
frontend (JS) manda/recebe e os objetos de domínio que o PartidaServico
espera. Nenhuma regra de jogo mora aqui -- só tradução e orquestração de
chamadas.
'''

from uuid import UUID

from ..models.enum import CorCarta
from ..services.partida_service import PartidaServico


class PartidaAPI:
    '''Classe passada como `js_api` para `webview.create_window(...)`.'''

    def __init__(self):
        self._servico = PartidaServico()

    # ------------------------------------------------------------------
    # Helpers internos (não expostos ao JS)
    # ------------------------------------------------------------------

    def _garantir_jogador_cadastrado(self, nome: str) -> None:
        '''
        Garante que `nome` existe em PartidaServico._jogadores_cadastrados.

        PartidaServico identifica jogadores só pelo nome (registro global,
        não por partida). Se o nome já estiver cadastrado, `cadastrar_jogador`
        levanta ValueError -- nesse caso só confirmamos que o jogador existe
        de fato (reaproveitando-o) via `buscar_jogador`. Se o erro for por
        outro motivo (ex: nome vazio), `buscar_jogador` vai falhar de novo e
        propagamos o erro real.
        '''
        try:
            self._servico.cadastrar_jogador(nome)
        except ValueError:
            self._servico.buscar_jogador(nome)

    def _validar_turno(self, id_partida: int, nome_jogador: str) -> None:
        '''Garante que quem está tentando agir é realmente o jogador da vez.'''
        partida = self._servico.buscar_partida(id_partida)
        if partida.jogador_atual().nome != nome_jogador:
            raise ValueError(f"Não é a vez de '{nome_jogador}' jogar.")

    # ------------------------------------------------------------------
    # Métodos expostos ao frontend (window.pywebview.api.*)
    # Todos retornam dict pronto pra JSON (enums já convertidos em string).
    # ------------------------------------------------------------------

    def criar_partida(self, id_partida: int, nomes_jogadores: list[str]) -> dict:
        '''Cadastra os jogadores (se ainda não existirem) e inicia a partida.'''
        for nome in nomes_jogadores:
            self._garantir_jogador_cadastrado(nome)

        estado = self._servico.criar_partida(id_partida, nomes_jogadores)
        return estado.model_dump(mode="json")

    def estado_partida(self, id_partida: int) -> dict:
        '''Retorna o snapshot atual da partida (pra atualizar a tela).'''
        partida = self._servico.buscar_partida(id_partida)
        estado = self._servico.estado_partida(partida)
        return estado.model_dump(mode="json")

    def jogar_carta(self, id_partida: int, nome_jogador: str, carta: dict) -> dict:
        '''
        Jogador tenta jogar uma carta da própria mão.

        `carta` vem do JS com pelo menos o campo "id" (uuid da carta, como
        recebido em `obter_mao`) -- é isso que PartidaServico usa para achar
        a carta na mão do jogador da vez.
        '''
        self._validar_turno(id_partida, nome_jogador)
        id_carta = UUID(carta["id"])
        estado = self._servico.executar_turno(id_partida, id_carta)
        return estado.model_dump(mode="json")

    def comprar_carta(self, id_partida: int, nome_jogador: str) -> dict:
        '''Jogador sem jogada válida compra uma carta.'''
        self._validar_turno(id_partida, nome_jogador)
        estado = self._servico.comprar_carta_turno(id_partida)
        return estado.model_dump(mode="json")

    def escolher_cor(self, id_partida: int, nome_jogador: str, cor: str) -> dict:
        '''Escolhe a nova cor após jogar carta preta (coringa).'''
        self._validar_turno(id_partida, nome_jogador)
        estado = self._servico.escolher_cor(id_partida, CorCarta(cor))
        return estado.model_dump(mode="json")

    def gritar_realiehgay(self, id_partida: int, nome_declarante: str, nome_alvo: str) -> dict:
        '''Um jogador declara "realiehgay" em nome de outro (ou de si mesmo).'''
        estado = self._servico.gritar_realiehgay(id_partida, nome_declarante, nome_alvo)
        return estado.model_dump(mode="json")

    def obter_mao(self, id_partida: int, nome_jogador: str) -> dict:
        '''
        Retorna a mão de cartas do jogador logado -- independente de ser a
        vez dele ou não (o frontend faz polling disso o tempo todo pra manter
        a própria mão sempre visível na tela).
        '''
        mao = self._servico.obter_mao(id_partida, nome_jogador)
        return mao.model_dump(mode="json")

    def trocar_mao(self, id_partida: int, nome_jogador: str, nome_alvo: str) -> dict:
        '''Aplica o efeito da carta de ação TROCAR_MAO.'''
        self._validar_turno(id_partida, nome_jogador)
        estado = self._servico.executar_trocar_mao(id_partida, nome_alvo)
        return estado.model_dump(mode="json")