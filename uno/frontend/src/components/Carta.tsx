import { ehCartaAcao } from "../api/partidaApi"
import type { Carta as CartaAPI, CorCarta, TipoEfeito } from "../api/partidaApi"

interface CartaProps {
  /** Dado real da carta (cor + valor, ou cor + ação) vindo da API. */
  carta?: CartaAPI
  rotate?: number
  onClick?: () => void
  /** Aplica destaque visual de "clicável" -- usado na mão do próprio jogador. */
  clicavel?: boolean
}

// Cor de fundo por CorCarta (backend/models/enum.py)
const CORES_FUNDO: Record<CorCarta, string> = {
  vermelho: "bg-red-600",
  azul: "bg-blue-600",
  verde: "bg-green-600",
  amarelo: "bg-yellow-400",
  preto: "bg-black",
}

// Amarelo é claro, precisa de texto escuro; o resto usa texto branco.
const CORES_TEXTO: Record<CorCarta, string> = {
  vermelho: "text-white",
  azul: "text-white",
  verde: "text-white",
  amarelo: "text-black",
  preto: "text-white",
}

// Rótulo curto exibido pra cada carta de ação (TipoEfeito)
const LABEL_ACAO: Record<TipoEfeito, string> = {
  PULAR: "PULA",
  REVERSO: "⟲",
  COMPRA_DUAS: "+2",
  COMPRA_QUATRO: "+4",
  TROCAR_MAO: "TROCA MÃO",
  TROCAR_COR: "COR",
}

function textoDaCarta(carta: CartaAPI): string {
  return ehCartaAcao(carta) ? LABEL_ACAO[carta.acao] : String(carta.valor)
}

function CartaBase({ carta, rotate = 0, onClick, clicavel = false }: CartaProps) {
  const bgColor = carta ? CORES_FUNDO[carta.cor] : "bg-white"
  const textColor = carta ? CORES_TEXTO[carta.cor] : "text-black"
  const textContent = carta ? textoDaCarta(carta) : "?"
  const ehAcao = carta ? ehCartaAcao(carta) : false
  const textSize = ehAcao ? "text-[15px]" : "text-[30px]"

  return (
    <div
      onClick={onClick}
      className={`flex w-18 h-28 ${bgColor} rounded-lg shadow-lg p-1 border-2 border-primary items-center justify-center text-center ${
        clicavel ? "cursor-pointer hover:-translate-y-2 transition-transform" : ""
      }`}
      style={{ transform: `rotate(${rotate}deg)` }}
    >
      <span className={`${textSize} font-bold underline ${textColor}`}>{textContent}</span>
    </div>
  )
}

/** Carta visível -- exige o dado real (cor + valor/ação) vindo da API. */
function Carta({ carta, rotate, onClick, clicavel }: CartaProps) {
  return <CartaBase carta={carta} rotate={rotate} onClick={onClick} clicavel={clicavel} />
}

/** Carta virada (dorso) -- usada pra mão de oponentes, nunca revela conteúdo. */
function CartaVirada({ rotate = 0 }: { rotate?: number }) {
  return (
    <div
      className="flex w-18 h-28 bg-black rounded-lg shadow-lg p-1 border-2 border-primary items-center justify-center"
      style={{ transform: `rotate(${rotate}deg)` }}
    >
      <span className="text-[17px] font-bold text-white rotate-45">KANBUNO</span>
    </div>
  )
}

export { Carta, CartaVirada, CartaBase }