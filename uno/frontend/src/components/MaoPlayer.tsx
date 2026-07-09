import { Carta, CartaVirada } from "./Carta"
import type { Carta as CartaAPI } from "../api/partidaApi"

interface MaoPlayerProps {
  /**
   * Mão virada (oponentes): só sabemos a QUANTIDADE de cartas, nunca o
   * conteúdo -- a API (obter_mao) só devolve a mão do próprio jogador
   * logado, então pra qualquer outro jogador só temos `quantidade_cartas`
   * do EstadoPartida.
   */
  quantidadeCartas?: number
  /**
   * Mão própria (jogador logado): cartas reais vindas de `obterMao`.
   * Quando essa prop é passada, ela manda -- ignora `quantidadeCartas`.
   */
  cartas?: CartaAPI[]
  /** Chamado ao clicar numa carta da própria mão. Não se aplica a mão virada. */
  onJogarCarta?: (carta: CartaAPI) => void
  /** Se false, a mão própria fica visível mas não clicável (ex: não é a vez do jogador). */
  jogavel?: boolean
  rotation?: number
  justify?: string
}

// ângulo máximo de abertura do leque
const ANGULO_MAX = 10

function calcularRotacoes(total: number): number[] {
  const meio = (total - 1) / 2
  return Array.from({ length: total }, (_, i) =>
    total > 1 ? (i - meio) * (ANGULO_MAX / meio) : 0
  )
}

function MaoPlayer({
  quantidadeCartas = 0,
  cartas,
  onJogarCarta,
  jogavel = true,
  rotation = 0,
  justify = "start",
}: MaoPlayerProps) {
  const ehMaoPropria = cartas !== undefined
  const total = ehMaoPropria ? cartas!.length : quantidadeCartas
  const rotacoes = calcularRotacoes(total)

  return (
    <div className="flex items-center p-8 min-h-24 m-0">
      <div
        className="flex"
        style={{ transform: `rotate(${rotation}deg)`, justifyContent: justify }}
      >
        {rotacoes.map((rotate, i) => {
          if (!ehMaoPropria) {
            return (
              <div key={i} style={{ marginLeft: i === 0 ? 0 : "-12px" }}>
                <CartaVirada rotate={rotate} />
              </div>
            )
          }

          const carta = cartas![i]
          return (
            <div
              key={i}
              style={{ marginLeft: i === 0 ? 0 : "-12px" }}
              className={!jogavel ? "opacity-60" : undefined}
            >
              <Carta
                rotate={rotate}
                carta={carta}
                onClick={jogavel ? () => onJogarCarta?.(carta) : undefined}
                clicavel={jogavel}
              />
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default MaoPlayer