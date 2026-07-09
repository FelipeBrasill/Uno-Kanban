/**
 * Cliente para consumir a PartidaAPI exposta pelo pywebview
 * (window.pywebview.api). Os tipos abaixo espelham:
 *   - backend/models/enum.py
 *   - backend/schemas/schema_saida.py
 *   - backend/api/partida_api.py
 *
 * Sugestão de local: frontend/src/api/partidaApi.ts
 */

// ---------------------------------------------------------------------------
// Tipos que espelham backend/models/enum.py
// ---------------------------------------------------------------------------

export type CorCarta = "vermelho" | "azul" | "verde" | "amarelo" | "preto";

export type TipoEfeito =
  | "PULAR"
  | "REVERSO"
  | "COMPRA_DUAS"
  | "COMPRA_QUATRO"
  | "TROCAR_MAO"
  | "TROCAR_COR";

export type EstadoJogador = "ativo" | "desistiu" | "venceu" | "perdeu";

export type EstadoRealiEhGay =
  | "normal"
  | "pode_declarar"
  | "declarou"
  | "perdeu_chance";

// ---------------------------------------------------------------------------
// Tipos que espelham backend/schemas/schema_saida.py
// ---------------------------------------------------------------------------

export interface CartaComum {
  cor: CorCarta;
  valor: number;
}

export interface CartaAcao {
  cor: CorCarta;
  acao: TipoEfeito;
}

export type Carta = CartaComum | CartaAcao;

/** Type guard: distingue CartaAcao de CartaComum em tempo de execução. */
export function ehCartaAcao(carta: Carta): carta is CartaAcao {
  return "acao" in carta;
}

export interface Jogador {
  nome: string;
  quantidade_cartas: number;
  estado_realiehgay: EstadoRealiEhGay;
  estado_jogador: EstadoJogador;
}

export interface Mao {
  mao: Carta[];
}

export interface EstadoPartida {
  jogador_atual: Jogador;
  vencedor: Jogador | null;
  carta_topo: Carta;
  jogadores: Jogador[];
}

// ---------------------------------------------------------------------------
// Contrato exposto pelo backend (backend/api/partida_api.py) via pywebview.
// Precisa ficar em sincronia manual com os métodos de PartidaAPI.
// ---------------------------------------------------------------------------

interface PywebviewApi {
  criar_partida(idPartida: number, nomesJogadores: string[]): Promise<EstadoPartida>;
  estado_partida(idPartida: number): Promise<EstadoPartida>;
  jogar_carta(idPartida: number, nomeJogador: string, carta: Carta): Promise<EstadoPartida>;
  comprar_carta(idPartida: number, nomeJogador: string): Promise<EstadoPartida>;
  escolher_cor(idPartida: number, nomeJogador: string, cor: CorCarta): Promise<EstadoPartida>;
  gritar_realiehgay(
    idPartida: number,
    nomeDeclarante: string,
    nomeAlvo: string
  ): Promise<EstadoPartida>;
  obter_mao(idPartida: number, nomeJogador: string): Promise<Mao>;
  trocar_mao(idPartida: number, nomeJogador: string, nomeAlvo: string): Promise<EstadoPartida>;
}

declare global {
  interface Window {
    pywebview?: {
      api: PywebviewApi;
    };
  }
}

// ---------------------------------------------------------------------------
// O pywebview injeta `window.pywebview.api` de forma assíncrona e dispara o
// evento "pywebviewready" quando termina. Se algum componente montar antes
// disso (comum, já que o React renderiza rápido), uma chamada direta a
// window.pywebview.api falharia. Por isso, toda chamada passa por aqui.
// ---------------------------------------------------------------------------

let apiPronta: Promise<PywebviewApi> | null = null;

function aguardarApi(): Promise<PywebviewApi> {
  if (window.pywebview?.api) {
    return Promise.resolve(window.pywebview.api);
  }

  if (!apiPronta) {
    apiPronta = new Promise((resolve) => {
      window.addEventListener(
        "pywebviewready",
        () => resolve(window.pywebview!.api),
        { once: true }
      );
    });
  }

  return apiPronta;
}

// ---------------------------------------------------------------------------
// Erro tipado, pra quem consumir a API conseguir distinguir uma falha de
// regra de jogo (ex: "Jogada inválida") de um erro inesperado qualquer.
// ---------------------------------------------------------------------------

export class PartidaApiError extends Error {
  causaOriginal?: unknown;

  constructor(message: string, causaOriginal?: unknown) {
    super(message);
    this.name = "PartidaApiError";
    this.causaOriginal = causaOriginal;
  }
}

async function chamar<T>(fn: (api: PywebviewApi) => Promise<T>): Promise<T> {
  try {
    const api = await aguardarApi();
    return await fn(api);
  } catch (erro) {
    // ASSUMIDO: hoje o backend (partida_api.py) deixa o ValueError "estourar"
    // puro. O pywebview propaga isso como rejeição da Promise aqui. Se o
    // grupo migrar pra um formato {sucesso, erro} no backend, este catch
    // é o único lugar que precisa mudar.
    const mensagem = erro instanceof Error ? erro.message : String(erro);
    throw new PartidaApiError(mensagem, erro);
  }
}

// ---------------------------------------------------------------------------
// Funções públicas — o que os componentes React devem importar e usar.
// Nomes em camelCase (padrão TS), mesmo o backend usando snake_case.
// ---------------------------------------------------------------------------

export const partidaApi = {
  criarPartida(idPartida: number, nomesJogadores: string[]): Promise<EstadoPartida> {
    return chamar((api) => api.criar_partida(idPartida, nomesJogadores));
  },

  buscarEstado(idPartida: number): Promise<EstadoPartida> {
    return chamar((api) => api.estado_partida(idPartida));
  },

  jogarCarta(idPartida: number, nomeJogador: string, carta: Carta): Promise<EstadoPartida> {
    return chamar((api) => api.jogar_carta(idPartida, nomeJogador, carta));
  },

  comprarCarta(idPartida: number, nomeJogador: string): Promise<EstadoPartida> {
    return chamar((api) => api.comprar_carta(idPartida, nomeJogador));
  },

  escolherCor(idPartida: number, nomeJogador: string, cor: CorCarta): Promise<EstadoPartida> {
    return chamar((api) => api.escolher_cor(idPartida, nomeJogador, cor));
  },

  gritarRealiehgay(
    idPartida: number,
    nomeDeclarante: string,
    nomeAlvo: string
  ): Promise<EstadoPartida> {
    return chamar((api) => api.gritar_realiehgay(idPartida, nomeDeclarante, nomeAlvo));
  },

  obterMao(idPartida: number, nomeJogador: string): Promise<Mao> {
    return chamar((api) => api.obter_mao(idPartida, nomeJogador));
  },

  trocarMao(idPartida: number, nomeJogador: string, nomeAlvo: string): Promise<EstadoPartida> {
    return chamar((api) => api.trocar_mao(idPartida, nomeJogador, nomeAlvo));
  },
};