'''
Camada exposta ao pywebview via `js_api`. Traduz entre o JSON que o
frontend (JS) manda/recebe e os objetos de domínio que o PartidaServico
espera. Nenhuma regra de jogo mora aqui -- só tradução e orquestração de
chamadas.
'''

from ..models.jogador import Jogador
from ..models.carta import Carta
from ..models.carta_acao import CartaAcao
from ..models.carta_comum import CartaComum
from ..models.enum import CorCarta, TipoEfeito
from ..services.partida_service import PartidaServico


class PartidaAPI:
    '''Classe passada como `js_api` para `webview.create_window(...)`.'''

    def __init__(self):
        self._servico = PartidaServico()

        # ASSUMIDO: Jogador não possui um id único, só `nome` (string).
        # Como o frontend não guarda instâncias Python, precisamos de um
        # jeito de "reencontrar" o Jogador certo a partir do nome que o JS
        # manda de volta. Por isso mantemos esse mapa auxiliar aqui.
        # Se dois jogadores tiverem o mesmo nome na mesma partida, isso
        # quebra -- vale o grupo decidir se quer um id de fato em Jogador.
        self._jogadores_por_partida: dict[int, dict[str, Jogador]] = {}

    # ------------------------------------------------------------------
    # Helpers internos (não expostos ao JS)
    # ------------------------------------------------------------------

    def _obter_jogador(self, id_partida: int, nome_jogador: str) -> Jogador:
        '''Recupera o objeto Jogador a partir do nome enviado pelo JS.'''
        jogadores = self._jogadores_por_partida.get(id_partida)
        if jogadores is None or nome_jogador not in jogadores:
            raise ValueError(
                f"Jogador '{nome_jogador}' não encontrado na partida {id_partida}"
            )
        return jogadores[nome_jogador]

    def _carta_correspondente_na_mao(self, jogador: Jogador, carta_dict: dict) -> Carta:
        '''
        Encontra, na mão real do jogador, a carta que corresponde ao dict
        recebido do JS (ex: {"cor": "vermelho", "valor": 5} ou
        {"cor": "preto", "acao": "COMPRA_QUATRO"}).

        ASSUMIDO: Carta/CartaComum/CartaAcao não implementam __eq__, então a
        comparação abaixo é feita atributo a atributo. O JS manda só os
        dados da carta, não a instância exata -- e Mao.remover_carta precisa
        do objeto certo. Se o grupo implementar __eq__ nas cartas, esse
        método pode ser simplificado.
        '''
        for carta in jogador.obter_mao():
            if carta.cor.value != carta_dict.get("cor"):
                continue
            if isinstance(carta, CartaComum) and "valor" in carta_dict:
                if carta.valor == carta_dict["valor"]:
                    return carta
            elif isinstance(carta, CartaAcao) and "acao" in carta_dict:
                if carta.acao.value == carta_dict["acao"]:
                    return carta
        raise ValueError("Carta informada não está na mão do jogador")

    # ------------------------------------------------------------------
    # Métodos expostos ao frontend (window.pywebview.api.*)
    # Todos retornam dict pronto pra JSON (enums já convertidos em string).
    # ------------------------------------------------------------------

    def criar_partida(self, id_partida: int, nomes_jogadores: list[str]) -> dict:
        '''Cria os jogadores a partir dos nomes e inicia a partida.'''
        jogadores = [Jogador(nome) for nome in nomes_jogadores]
        self._jogadores_por_partida[id_partida] = {j.nome: j for j in jogadores}

        estado = self._servico.criar_partida(id_partida, jogadores)
        return estado.model_dump(mode="json")

    def estado_partida(self, id_partida: int) -> dict:
        '''Retorna o snapshot atual da partida (pra atualizar a tela).'''
        partida = self._servico.buscar_partida(id_partida)
        estado = self._servico.estado_partida(partida)
        return estado.model_dump(mode="json")

    def jogar_carta(self, id_partida: int, nome_jogador: str, carta: dict) -> dict:
        '''Jogador tenta jogar uma carta da própria mão.'''
        jogador = self._obter_jogador(id_partida, nome_jogador)
        carta_obj = self._carta_correspondente_na_mao(jogador, carta)
        estado = self._servico.executar_turno(id_partida, jogador, carta_obj)
        return estado.model_dump(mode="json")

    def comprar_carta(self, id_partida: int, nome_jogador: str) -> dict:
        '''Jogador sem jogada válida compra uma carta.'''
        jogador = self._obter_jogador(id_partida, nome_jogador)
        estado = self._servico.comprar_carta_turno(id_partida, jogador)
        return estado.model_dump(mode="json")

    def escolher_cor(self, id_partida: int, nome_jogador: str, cor: str) -> dict:
        '''Escolhe a nova cor após jogar carta preta (coringa).'''
        jogador = self._obter_jogador(id_partida, nome_jogador)
        estado = self._servico.escolher_cor(id_partida, jogador, CorCarta(cor))
        return estado.model_dump(mode="json")

    def gritar_realiehgay(self, id_partida: int, nome_declarante: str, nome_alvo: str) -> dict:
        '''Um jogador declara "realiehgay" em nome de outro (ou de si mesmo).'''
        declarante = self._obter_jogador(id_partida, nome_declarante)
        alvo = self._obter_jogador(id_partida, nome_alvo)
        estado = self._servico.gritar_realiehgay(id_partida, declarante, alvo)
        return estado.model_dump(mode="json")

    def obter_mao(self, id_partida: int, nome_jogador: str) -> dict:
        '''Retorna a mão de cartas do jogador logado.'''
        jogador = self._obter_jogador(id_partida, nome_jogador)
        mao = self._servico.obter_mao(id_partida, jogador)
        return mao.model_dump(mode="json")

    def trocar_mao(self, id_partida: int, nome_jogador: str, nome_alvo: str) -> dict:
        '''Aplica o efeito da carta de ação TROCAR_MAO.'''
        jogador = self._obter_jogador(id_partida, nome_jogador)
        alvo = self._obter_jogador(id_partida, nome_alvo)
        estado = self._servico.executar_trocar_mao(id_partida, jogador, alvo)
        return estado.model_dump(mode="json")