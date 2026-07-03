function CartaVirada({ rotate }: { rotate?: number }) {
  return (
    <div
      className="flex w-18 h-28 bg-black rounded-lg shadow-lg p-1 border-2 border-primary items-center justify-center"
      style={{ transform: rotate !== undefined ? `rotate(${rotate}deg)` : 'none' }}
    >
      <h1 className="text-white text-[16px] font-bold rotate-45">KANBUNO</h1>
    </div>
  )
}

function Carta({rotate}: {rotate?: number}) {
    let rot;
    if (rotate != undefined) {
        rot = `rotate-${rotate}`
    } else {
        rot = "rotate-none"
    }
    return (
        <div className={`flex w-18 h-28 bg-white rounded-lg shadow-lg p-1 border-2 border-primary items-center justify-center ${rot}`}>
                <h1 className="text-black text-[30px] font-bold rotate-45">+40</h1>
        </div>
    )
}

export { Carta, CartaVirada }