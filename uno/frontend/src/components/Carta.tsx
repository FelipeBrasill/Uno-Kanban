interface CartaProps {
  rotate?: number
  virada?: boolean
  valor?: string
}

function CartaBase({ rotate = 0, virada = false, valor = "+40" }: CartaProps) {
  const bgColor = virada ? "bg-black" : "bg-white"
  const textColor = virada ? "text-white" : "text-black"
  const textContent = virada ? "KANBUNO" : valor
  const textSize = virada ? "text-[17px]" : "text-[30px]"
  const rotateStyle = virada ? "rotate-45" : ""
  const underlineStyle = !virada ? "underline" : ""

  return (
    <div
      className={`flex w-18 h-28 ${bgColor} rounded-lg shadow-lg p-1 border-2 border-primary items-center justify-center cursor-pointer`}
      style={{ transform: `rotate(${rotate}deg)` }}
    >
      <span className={`${textSize} font-bold ${rotateStyle} ${textColor} ${underlineStyle}`}>
        {textContent}
      </span>
    </div>
  )
}

function Carta({ rotate, valor }: Omit<CartaProps, "virada">) {
  return <CartaBase rotate={rotate} valor={valor} virada={false} />
}

function CartaVirada({ rotate }: Omit<CartaProps, "virada" | "valor">) {
  return <CartaBase rotate={rotate} virada={true} />
}

export { Carta, CartaVirada, CartaBase }