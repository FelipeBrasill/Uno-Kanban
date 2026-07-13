import { useCallback, useEffect, useState } from "react"
import { useLocation, useNavigate } from "react-router"

import routes_name from "../routes/routes"
import { obterNomeJogador } from "../api/JogadorAtual"
import {
  partidaApi,
  PartidaApiError,
  ehCartaAcao,
} from "../api/partidaApi"
import type {
  EstadoPartida,
  Jogador,
  Carta as CartaAPI,
  CorCarta,
} from "../api/partidaApi"

import { Carta, CartaVirada } from "../components/Carta"
import ContainerPlayer from "../components/ContainerPlayer"
import MaoPlayer from "../components/MaoPlayer"

const CORES_ESCOLHIVEIS: CorCarta[] = ["vermelho", "azul", "verde", "amarelo"]

// Precisa ser um mapa com classes escritas por extenso -- o Tailwind não
// compila classes montadas dinamicamente via template string (ex: `bg-${cor}-600`).
const CLASSE_BOTAO_COR: Record<CorCarta, string> = {
  vermelho: "bg-red-600",
  azul: "bg-blue-600",
  verde: "bg-green-600",
  amarelo: "bg-yellow-400",
  preto: "bg-black",
}

const INTERVALO_POLLING_MS = 2000

/**
 * Distribui os oponentes em 3 grupos (topo / esquerda / direita) de forma
 * simples e cíclica. ASSUMIDO: isso é uma simplificação -- não é um
 * posicionamento circular "de verdade" em volta da mesa. Funciona bem pra
 * poucos oponentes (o caso comum), mas com muitos jogadores os grupos vão
 * empilhar vários ContainerPlayer no mesmo lado. Se o grupo quiser uma
 * disposição mais realista (ângulos ao redor de uma mesa oval, por
 * exemplo), isso pede um componente de layout dedicado -- fica como
 * possível próximo passo.
 */
function distribuirOponentes(oponentes: Jogador[]) {
  const grupos: { topo: Jogador[]; esquerda: Jogador[]; direita: Jogador[] } = {
    topo: [],
    esquerda: [],
    direita: [],
  }
  oponentes.forEach((jogador, i) => {
    const posicao = i % 3
    if (posicao === 0) grupos.topo.push(jogador)
    else if (posicao === 1) grupos.esquerda.push(jogador)
    else grupos.direita.push(jogador)
  })
  return grupos
}

function Partida() {
  const location = useLocation()
  const navigate = useNavigate()

  // idPartida vem via state da navegação (ver Home.tsx) -- a rota "/partida"
  // é fixa, sem parâmetro na URL (ver AppRoutes.tsx).
  const estadoRecebido = location.state as
    | { idPartida?: number; estadoInicial?: EstadoPartida }
    | null

  const [idPartida] = useState<number | null>(estadoRecebido?.idPartida ?? null)
  const [nomeJogador] = useState<string | null>(() => obterNomeJogador())

  const [estado, setEstado] = useState<EstadoPartida | null>(
    estadoRecebido?.estadoInicial ?? null
  )
  const [minhaMao, setMinhaMao] = useState<CartaAPI[]>([])
  const [erro, setErro] = useState<string | null>(null)
  const [carregandoAcao, setCarregandoAcao] = useState(false)

  // Heurísticas client-side: a API não expõe explicitamente "aguardando
  // escolha de cor" ou "aguardando alvo de troca de mão" no EstadoPartida,
  // então deduzimos isso a partir da carta que ACABAMOS de jogar.
  const [aguardandoCor, setAguardandoCor] = useState(false)
  const [aguardandoAlvoTroca, setAguardandoAlvoTroca] = useState(false)

  // Sem idPartida ou nome de jogador, essa tela não tem como funcionar
  // (ex: usuário deu F5 e perdeu o state da navegação) -- volta pra Home.
  useEffect(() => {
    if (!idPartida || !nomeJogador) {
      navigate(routes_name.home)
    }
  }, [idPartida, nomeJogador, navigate])

  function tratarErro(e: unknown) {
    const mensagem = e instanceof PartidaApiError ? e.message : "Ocorreu um erro inesperado."
    setErro(mensagem)
  }

  const atualizarEstado = useCallback(async () => {
    if (!idPartida || !nomeJogador) return
    try {
      const [novoEstado, mao] = await Promise.all([
        partidaApi.buscarEstado(idPartida),
        partidaApi.obterMao(idPartida, nomeJogador),
      ])
      setEstado(novoEstado)
      setMinhaMao(mao.mao)
    } catch (e) {
      tratarErro(e)
    }
  }, [idPartida, nomeJogador])

  // Polling: mantém o estado sincronizado com as jogadas de outros
  // jogadores, já que não há WebSocket/push no pywebview.
  useEffect(() => {
    atualizarEstado()
    const intervalo = setInterval(atualizarEstado, INTERVALO_POLLING_MS)
    return () => clearInterval(intervalo)
  }, [atualizarEstado])

  async function jogarCarta(carta: CartaAPI) {
    if (!idPartida || !nomeJogador) return
    setErro(null)
    setCarregandoAcao(true)
    try {
      const novoEstado = await partidaApi.jogarCarta(idPartida, nomeJogador, carta)
      setEstado(novoEstado)

      // Carta preta (coringa) exige escolha de cor em seguida.
      if (carta.cor === "preto") {
        setAguardandoCor(true)
      }
      // TROCAR_MAO exige escolher um alvo em seguida.
      if (ehCartaAcao(carta) && carta.acao === "TROCAR_MAO") {
        setAguardandoAlvoTroca(true)
      }

      await atualizarEstado()
    } catch (e) {
      tratarErro(e)
    } finally {
      setCarregandoAcao(false)
    }
  }

  async function comprarCarta() {
    if (!idPartida || !nomeJogador) return
    setErro(null)
    setCarregandoAcao(true)
    try {
      const novoEstado = await partidaApi.comprarCarta(idPartida, nomeJogador)
      setEstado(novoEstado)
      await atualizarEstado()
    } catch (e) {
      tratarErro(e)
    } finally {
      setCarregandoAcao(false)
    }
  }

  async function escolherCor(cor: CorCarta) {
    if (!idPartida || !nomeJogador) return

    setErro(null)

    // Fecha imediatamente
    setAguardandoCor(false)

    try {
      const novoEstado = await partidaApi.escolherCor(
        idPartida,
        nomeJogador,
        cor
      )

      setEstado(novoEstado)
    } catch (e) {
      // Reabre caso dê erro
      setAguardandoCor(true)
      tratarErro(e)
    }
}

  async function trocarMaoCom(nomeAlvo: string) {
    if (!idPartida || !nomeJogador) return

    setErro(null)

    setAguardandoAlvoTroca(false)

    try {
      const novoEstado = await partidaApi.trocarMao(
        idPartida,
        nomeJogador,
        nomeAlvo
      )

      setEstado(novoEstado)
      await atualizarEstado()
    } catch (e) {
      setAguardandoAlvoTroca(true)
      tratarErro(e)
    }
}

  async function gritarUno(nomeAlvo: string) {
    if (!idPartida || !nomeJogador) return
    setErro(null)
    try {
      const novoEstado = await partidaApi.gritarRealiehgay(idPartida, nomeJogador, nomeAlvo)
      setEstado(novoEstado)
    } catch (e) {
      tratarErro(e)
    }
  }

  if (!idPartida || !nomeJogador || !estado) {
    return (
      <div className="flex flex-col items-center justify-center flex-1 bg-gray-100">
        <p>Carregando partida...</p>
      </div>
    )
  }

  const minhaVez = estado.jogador_atual.nome === nomeJogador
  const euNaLista = estado.jogadores.find((j) => j.nome === nomeJogador)
  const oponentes = estado.jogadores.filter((j) => j.nome !== nomeJogador)
  const grupos = distribuirOponentes(oponentes)

  function podeGritarUno(jogador: Jogador) {
    return jogador.estado_realiehgay === "pode_declarar"
  }

  function renderizarOponente(jogador: Jogador, orientacao: "top" | "left" | "right") {
    const rotacaoMao = orientacao === "top" ? 180 : orientacao === "left" ? 90 : 270
    return (
      <div
        key={jogador.nome}
        className={`flex ${orientacao === "top" ? "flex-col" : "flex-row"} items-center gap-2`}
      >
        {orientacao === "right" && (
          <MaoPlayer quantidadeCartas={jogador.quantidade_cartas} rotation={rotacaoMao} />
        )}
        <ContainerPlayer
          jogador={jogador}
          Orientation={orientacao}
          ehVez={jogador.nome === ((estado === null)? "nome não encontrado" : estado.jogador_atual.nome)}
        />
        {orientacao !== "right" && (
          <MaoPlayer quantidadeCartas={jogador.quantidade_cartas} rotation={rotacaoMao} />
        )}
        {podeGritarUno(jogador) && (
          <button
            onClick={() => gritarUno(jogador.nome)}
            className="text-xs font-bold text-red-600 underline"
          >
            Real-i-eh-gay!
          </button>
        )}
      </div>
    )
  }

  return (
    <div className="flex flex-col items-center justify-center flex-1 bg-gray-100">
      {erro && (
        <div className="w-full bg-red-100 text-red-700 text-center py-1 text-sm">{erro}</div>
      )}

      {estado.vencedor && (
        <div className="w-full bg-yellow-300 text-center py-2 font-bold">
          {estado.vencedor.nome} venceu a partida!
        </div>
      )}

      <div className="flex flex-col w-[90vw] h-[87vh] gap-2 rounded-lg p-8 items-center justify-between">
        {/* Topo: comprar carta + oponentes do grupo "topo" */}
        <div className="flex flex-row items-start justify-between w-full h-2/5 rounded-lg p-0">
          <div
            className="flex flex-col items-center justify-start h-full w-1/3 rounded-lg p-0 cursor-pointer"
            onClick={() => minhaVez && !carregandoAcao && comprarCarta()}
          >
            <span className="text-2xl font-bold">Comprar Carta</span>
            <div className={!minhaVez ? "opacity-50" : undefined}>
              <CartaVirada />
            </div>
          </div>

          <div className="flex flex-row flex-wrap items-center justify-center gap-4 w-1/3">
            {grupos.topo.map((jogador) => renderizarOponente(jogador, "top"))}
          </div>

          <div className="w-1/3 flex justify-end text-white">Easter Egg</div>
        </div>

        {/* Meio: oponentes da esquerda/direita + carta central */}
        <div className="flex flex-row items-center justify-between h-1/5 w-full rounded-lg p-4">
          <div className="flex flex-row flex-wrap items-center gap-4">
            {grupos.esquerda.map((jogador) => renderizarOponente(jogador, "left"))}
          </div>

          <Carta carta={estado.carta_topo} rotate={45} />

          <div className="flex flex-row flex-wrap items-center gap-4">
            {grupos.direita.map((jogador) => renderizarOponente(jogador, "right"))}
          </div>
        </div>

        {/* Base: o próprio jogador */}
        <div className="flex flex-col items-center justify-end h-2/5 rounded-lg p-0 gap-2">
          <MaoPlayer
            cartas={minhaMao}
            onJogarCarta={jogarCarta}
            jogavel={minhaVez && !carregandoAcao}
            rotation={0}
          />
          {euNaLista && (
            <ContainerPlayer jogador={euNaLista} Orientation="bottom" ehVez={minhaVez} />
          )}
          {euNaLista && podeGritarUno(euNaLista) && (
            <button
              onClick={() => gritarUno(nomeJogador)}
              className="text-xs font-bold text-red-600 underline"
            >
              Real-i-eh-gay!
            </button>
          )}
        </div>
      </div>

      {/* Overlay: escolha de cor após jogar carta preta */}
      {aguardandoCor && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 flex flex-col items-center gap-4">
            <p className="font-bold">Escolha a nova cor</p>
            <div className="flex gap-3">
              {CORES_ESCOLHIVEIS.map((cor) => (
                <button
                  key={cor}
                  onClick={() => escolherCor(cor)}
                  className={`w-12 h-12 rounded-full border-2 ${CLASSE_BOTAO_COR[cor]}`}
                  aria-label={cor}
                />
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Overlay: escolha de alvo após jogar TROCAR_MAO */}
      {aguardandoAlvoTroca && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 flex flex-col items-center gap-4">
            <p className="font-bold">Com quem você quer trocar de mão?</p>
            <div className="flex flex-col gap-2">
              {oponentes.map((jogador) => (
                <button
                  key={jogador.nome}
                  onClick={() => trocarMaoCom(jogador.nome)}
                  className="px-4 py-2 rounded-lg bg-primary text-white"
                >
                  {jogador.nome}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Partida