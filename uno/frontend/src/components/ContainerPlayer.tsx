import type { Jogador } from "../api/partidaApi"

import Benyo from "../assets/players/benyo.png"
import Calvo from "../assets/players/calvo.jpeg"
import Reali from "../assets/players/realiehgay.jpeg"
import McLovin from "../assets/players/mclovin.jpeg"

// ASSUMIDO: por enquanto só existem essas 4 fotos mockadas. Como os nomes
// dos jogadores agora vêm digitados na Tela Inicial (não tem "foto do João"
// cadastrada), cada jogador sorteia uma dessas 4 quando aparece em tela
// pela primeira vez.
const FOTOS_DISPONIVEIS = [Benyo, Calvo, Reali, McLovin]

// Cache em nível de módulo: guarda qual foto já saiu no sorteio pra cada
// nome. Sem isso, o polling de estado_partida re-renderizaria o
// ContainerPlayer a cada poucos segundos e a foto "trocaria sozinha" a
// cada sorteio novo. Com o cache, o sorteio só acontece na primeira vez
// que aquele nome aparece nesta sessão; depois disso fica fixo.
const fotoPorJogador = new Map<string, string>()

function fotoParaJogador(nome: string): string {
  if (!fotoPorJogador.has(nome)) {
    const indiceSorteado = Math.floor(Math.random() * FOTOS_DISPONIVEIS.length)
    fotoPorJogador.set(nome, FOTOS_DISPONIVEIS[indiceSorteado])
  }
  return fotoPorJogador.get(nome)!
}

function ContainerPlayerImg({ playerName }: { playerName: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-0 rounded-lg p-1">
      <img
        src={fotoParaJogador(playerName)}
        alt={playerName}
        className="w-12 h-12 rounded-full object-cover"
      />
      <span className="text-lg font-bold">{playerName}</span>
    </div>
  )
}

function ContainerPlayerStatus({ jogador }: { jogador: Jogador }) {
  const foiEliminado = jogador.estado_jogador === "desistiu" || jogador.estado_jogador === "perdeu"
  const venceu = jogador.estado_jogador === "venceu"

  const corFundo = venceu ? "bg-yellow-400" : foiEliminado ? "bg-gray-400" : "bg-purple-500"

  return (
    <div className="flex flex-col items-center gap-1">
      {/* Quantidade de cartas na mão -- antes era um "score" sem relação com o jogo real */}
      <div className={`flex flex-row items-center justify-center gap-2 rounded-lg p-4 ${corFundo}`}>
        <span className="text-xl font-bold">{jogador.quantidade_cartas}</span>
      </div>

      {jogador.estado_realiehgay === "pode_declarar" && (
        <span className="text-xs font-bold text-red-600 animate-pulse">1 carta!</span>
      )}
      {jogador.estado_realiehgay === "declarou" && (
        <span className="text-xs text-green-700">Real-i-eh-gay!</span>
      )}
      {venceu && <span className="text-xs font-bold text-yellow-700">Venceu</span>}
      {foiEliminado && <span className="text-xs text-gray-600">Fora da partida</span>}
    </div>
  )
}

type Orientation = "left" | "right" | "top" | "bottom"

interface ContainerPlayerProps {
  /** Dados reais do jogador (nome, cartas, estados) vindos do EstadoPartida. */
  jogador: Jogador
  Orientation: Orientation
  /** Destaca visualmente o jogador cuja vez é agora. */
  ehVez?: boolean
}

function ContainerPlayer({
  jogador,
  Orientation: orientation,
  ehVez = false,
}: ContainerPlayerProps) {
  const isImageFirst = orientation === "right" || orientation === "bottom"
  const align = orientation === "left" || orientation === "top" ? "justify-start" : "justify-end"
  const flexDirection = orientation === "left" || orientation === "right" ? "flex-row" : "flex-col"

  const image = <ContainerPlayerImg playerName={jogador.nome} />
  const statusElement = <ContainerPlayerStatus jogador={jogador} />

  return (
    <div
      className={`flex ${flexDirection} items-center ${align} gap-1 rounded-lg p-4 h-[65%] ${
        ehVez ? "ring-4 ring-primary rounded-xl" : ""
      }`}
    >
      {isImageFirst ? (
        <>
          {image}
          {statusElement}
        </>
      ) : (
        <>
          {statusElement}
          {image}
        </>
      )}
    </div>
  )
}

export default ContainerPlayer