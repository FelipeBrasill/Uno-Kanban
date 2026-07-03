import Benyo from '../assets/players/benyo.png'
import Calvo from '../assets/players/calvo.jpeg'
import Reali from '../assets/players/realiehgay.jpeg'
import McLovin from '../assets/players/mclovin.jpeg'

import { Carta, CartaVirada } from '../components/Carta'

function ConteinerPlayer({ playerImage, playerName, Orientation }: { playerImage: string, playerName: string, Orientation: "left" | "right" | "top" | "bottom" }) {

    let align = Orientation in ["left", "top"] ? "justify-start" : "justify-end"
    let flexDirection = Orientation in ["left", "right"] ? "flex-row" : "flex-col"
    
    if (Orientation === "right" || Orientation === "bottom") {
        return (
            <div className={`flex ${flexDirection} items-center ${align} gap-4 rounded-lg p-4`}>
                <div className="flex flex-col items-center justify-center gap-4 rounded-lg p-4">
                    <img src={playerImage} alt={playerName} className="w-16 h-16 rounded-full object-cover" />
                    <h1 className="text-xl font-bold">{playerName}</h1>
                </div>
                <div className="flex flex-row bg-purple-500 gap-4 rounded-lg p-4">
                    <h1 className="text-xl font-bold">0</h1>
                </div>
            </div>
        )
    }

    return (
        <div className={`flex ${flexDirection} items-center ${align} gap-4 rounded-lg p-4`}>
            <div className="flex flex-row bg-purple-500 gap-4 rounded-lg p-4">
                <h1 className="text-xl font-bold">0</h1>
            </div>
            <div className="flex flex-col items-center justify-center gap-4 rounded-lg p-4">
                <img src={playerImage} alt={playerName} className="w-16 h-16 rounded-full object-cover" />
                <h1 className="text-xl font-bold">{playerName}</h1>
            </div>
        </div>
    )
}

function Partida() {
  return (
    <div className="flex flex-col items-center justify-center flex-1 bg-gray-100">
      <div className="flex flex-col w-[90vw] h-[85vh] gap-2 rounded-lg p-8 items-center justify-center">
        {/* Benyo */}
        <div className="flex flex-col items-center justify-start h-2/5rounded-lg p-4 gap-2">
            <ConteinerPlayer playerImage={Benyo} playerName="Benyo" Orientation="top" />
            <CartaVirada rotate={180} />
        </div>
        <div className="flex flex-row items-center justify-between h-1/5 w-2/3 rounded-lg p-4">
            {/* Calvo */}
            <div className="flex flex-row items-center justify-start gap-2">
                <ConteinerPlayer playerImage={Calvo} playerName="Calvo" Orientation="left" />
                <CartaVirada rotate={450} />
            </div>
            <Carta rotate={315} />
            {/* McLovin */}
            <div className="flex flex-row items-center justify-end gap-2">
                <CartaVirada rotate={270} />
                <ConteinerPlayer playerImage={McLovin} playerName="McLovin" Orientation="right" />
            </div>
        </div>
        {/* Reali */}
        <div className="flex flex-col items-center justify-end h-2/5 rounded-lg p-4 gap-2">
            <CartaVirada />
            <ConteinerPlayer playerImage={Reali} playerName="O Gay" Orientation="bottom" />
        </div>
      </div>
    </div>
  )
}

export default Partida