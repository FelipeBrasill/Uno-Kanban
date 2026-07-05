import { Children, cloneElement } from "react"
import type { ReactElement, ComponentProps } from "react"
import { Carta, CartaVirada } from "./Carta"

type CartaElement = ReactElement<ComponentProps<typeof Carta>> | ReactElement<ComponentProps<typeof CartaVirada>>

interface MaoPlayerProps {
  children: CartaElement | CartaElement[]
  rotation?: number
  justify?: string
}

function MaoPlayer({ children, rotation=0, justify="start"}: MaoPlayerProps) {
  const cartas = Children.toArray(children) as CartaElement[]
  const total = cartas.length

  // ângulo máximo de abertura do leque
  const anguloMax = 10

  return (
    <div className={ `flex items-center p-8 min-h-24 m-0 ` }>
      <div className="flex" style={{ transform: `rotate(${rotation}deg)`, justifyContent: `${justify}` }}>
        {cartas.map((carta, i) => {
          // distribui os ângulos simetricamente em torno do centro
          const meio = (total - 1) / 2
          const rotate = total > 1 ? (i - meio) * (anguloMax / meio) : 0

          return (
            <div
              key={i}
              style={{
                marginLeft: i === 0 ? 0 : "-12px", // sobrepõe as cartas
              }}
            >
              {cloneElement(carta, { rotate })}
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default MaoPlayer